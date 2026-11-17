#!/usr/bin/env python3
"""List Huawei Cloud RDS instances and export them as a Markdown table file.

Primary execution path is KooCLI `hcloud RDS ListInstances` (official read-only
GET /v3/{project_id}/instances); when hcloud is not installed the script falls
back to the official `huaweicloudsdkrds` v3 SDK (`list_instances`). The result
is rendered as a Markdown table and written to a local `.md` file (default
`rds_instances.md` in the current directory). Nothing is ever written back to
the cloud: this skill is strictly read-only.

A built-in write-intent guard rejects mutating operations and mutating
vocabulary before any command is executed: the only allowed operation is the
read-only `ListInstances`; create / delete / update / resize / restart / stop /
restore intents are refused.

Usage:
    python3 scripts/list_rds_export_markdown.py [--region cn-north-4]
                                   [--project_id <project_id>]
                                   [--output rds_instances.md]
                                   [--name rds-01] [--status ACTIVE]
                                   [--sort-by name|created]
                                   [--page-size 100] [--operation ListInstances]
                                   [--stdout]

`--sort-by` orders the exported rows locally after the full (paged) list has
been fetched — the real RDS ListInstances API has no ordering parameter. Omit
it to keep the API order (byte-identical output to the previous behaviour).

Environment overrides (mostly for tests):
    RDS_LIST_MD_HCLOUD_BIN   hcloud executable (default "hcloud")
    RDS_LIST_MD_HCLOUD_ARGS  extra args injected before the RDS operation
"""

import argparse
import datetime
import json
import os
import re
import subprocess
import sys
import tempfile

DEFAULT_REGION = "cn-north-4"
DEFAULT_PAGE_SIZE = 100
DEFAULT_OUTPUT = "rds_instances.md"
SERVICE = "RDS"
ALLOWED_OPERATION = "ListInstances"

# Mutating RDS operations / intents — strictly rejected by the guard.
WRITE_INTENT_KEYWORDS = (
    "createinstance",
    "deleteinstance",
    "updateinstance",
    "modifyinstance",
    "resizeflavor",
    "resize",
    "restartinstance",
    "stopinstance",
    "startinstance",
    "shutdowninstance",
    "changeflavor",
    "changepassword",
    "setbackuppolicy",
    "updatebackuppolicy",
    "createreadreplica",
    "deletereadreplica",
    "creating",
    "deleting",
    "updating",
    "resizing",
    "restoring",
    "create",
    "delete",
    "update",
    "modify",
    "restart",
    "stop",
    "start",
    "shutdown",
    "restore",
    "destroy",
)

# Values of these read-only flags are caller data (filters, local output paths,
# local ordering options), not RDS operations — they are excluded from the
# mutating-intent scan. `--sort-by` MUST stay in this set: its value "created"
# contains the mutating keyword "create", so scanning it would reject a
# perfectly read-only export.
READ_ONLY_VALUE_FLAGS = frozenset((
    "--output", "-o",
    "--region", "-r",
    "--project_id", "--project-id",
    "--name",
    "--status",
    "--datastore-type",
    "--instance-id",
    "--page-size",
    "--limit",
    "--offset",
    "--sort-by",
))

# Locally supported `--sort-by` values. The real ListInstances API has no
# ordering parameter, so ordering is always applied client-side.
SORTABLE_KEYS = ("name", "created")

_INSTANCE_LIST_KEYS = ("instances", "instance_list", "instanceInfos")

# Whitelisted credential environment variables — read by name only, never by
# enumerating os.environ (avoids harvesting unrelated environment variables).
_AK_ENV_NAMES = (
    "HW_ACCESS_KEY",
    "HUAWEI_ACCESS_KEY",
    "HUAWEICLOUD_SDK_AK",
    "HUAWEI_CLOUD_ACCESS_KEY",
)
_SK_ENV_NAMES = (
    "HW_SECRET_KEY",
    "HUAWEI_SECRET_KEY",
    "HUAWEICLOUD_SDK_SK",
    "HUAWEI_CLOUD_SECRET_KEY",
)


def _env_value(names):
    """Read the first non-empty value from an explicit whitelist of env names."""
    for name in names:
        value = os.environ.get(name)
        if value:
            return value
    return None

_CREDENTIAL_MISSING_PATTERNS = (
    "cli-ak",
    "cli-sk",
    "access key",
    "secret key",
    "credential",
    "configure",
    "未配置",
    "配置为空",
    "no ak",
    "no sk",
    "ak/sk",
)

_AUTH_PATTERNS = (
    "401",
    "403",
    "unauthorized",
    "forbidden",
    "apigw.0301",
    "认证失败",
    "权限不足",
    "permission denied",
)

# KooCLI prints usage errors (e.g. "[USE_ERROR]Invalid parameter: xxx") on
# stdout WITH exit code 0 — the marker must be treated as a hard failure even
# when the return code looks successful.
_USE_ERROR_MARKER = "[use_error]"

# Markdown table columns: header label -> candidate source keys (first hit wins).
MD_COLUMNS = (
    ("实例名称", ("name", "instance_name")),
    ("实例ID", ("id", "instance_id")),
    ("状态", ("status",)),
    ("引擎", ("engine",)),
    ("版本", ("engineVersion", "engine_version")),
    ("规格", ("flavor_ref", "flavorRef")),
    ("私网IP", ("privateIps",)),
    ("可用区", ("availability_zone",)),
    ("创建时间", ("created",)),
)


class RdsListError(Exception):
    """Base error for the RDS list-markdown skill."""


class GuardError(RdsListError):
    """A write intent was detected and blocked (skill is read-only)."""


class ConfigError(RdsListError):
    """hcloud missing or credentials (AK/SK) not configured."""


class AuthError(RdsListError):
    """Authentication/authorization failure (invalid AK/SK or IAM 403)."""


class ApiError(RdsListError):
    """hcloud / network / unexpected API / file export failure."""


class SortError(RdsListError):
    """The requested `--sort-by` value is not supported."""


def guard_write_intent(text):
    """Raise GuardError if `text` carries a mutating intent.

    Normalizes separators so `--create-instance`, `CreateInstance`, and
    `create_instance` all hit the same keyword. Read-only vocabulary
    (list/show/get/describe) never matches.
    """
    low = re.sub(r"[\s_\-]+", "", str(text).lower())
    for keyword in WRITE_INTENT_KEYWORDS:
        if keyword in low:
            raise GuardError(
                "检测到写操作意图（关键词: %s）。本 skill 仅支持只读查询"
                "（RDS ListInstances）并导出 Markdown 文件，创建/删除/扩缩容/重启等"
                "变更操作已被守卫拦截。" % keyword
            )
    return False


def guard_operation(operation):
    """Only the read-only ListInstances operation may be executed."""
    if operation != ALLOWED_OPERATION:
        raise GuardError(
            "不允许的操作 %r：本 skill 仅允许只读操作 %s。" % (operation, ALLOWED_OPERATION)
        )
    return True


def scrub_read_only_values(argv):
    """Drop the values of read-only flags before the write-intent scan.

    Values such as the local `--output` path or a `--name` filter are caller
    data, not RDS operations; scanning them would cause false positives (e.g. a
    file named under `downloads/`, or `--sort-by created` whose value contains
    the keyword `create`). Both `--flag value` and `--flag=value` forms are
    scrubbed; the flag itself and every other token are kept and still scanned.
    """
    out = []
    skip_next = False
    for token in argv:
        if skip_next:
            skip_next = False
            continue
        if token in READ_ONLY_VALUE_FLAGS:
            out.append(token)
            skip_next = True
            continue
        for flag in READ_ONLY_VALUE_FLAGS:
            if token.startswith(flag + "="):
                out.append(flag)
                break
        else:
            out.append(token)
    return " ".join(out)


def build_command(region, name=None, datastore_type=None,
                  instance_id=None, limit=DEFAULT_PAGE_SIZE, offset=0,
                  project_id=None):
    """Build the hcloud RDS ListInstances argv (without the executable).

    Mirrors the real KooCLI parameter list (`hcloud RDS ListInstances --help`):
    --cli-region / --limit / --offset / --name / --datastore_type / --id. The
    global `--cli-project-id` is appended only when the caller supplies a
    project id. There is NO --status parameter on the server side — status
    filtering is applied client-side by `filter_by_status()`.
    """
    argv = [
        SERVICE,
        ALLOWED_OPERATION,
        "--cli-region=%s" % region,
        "--limit=%d" % limit,
        "--offset=%d" % offset,
    ]
    if project_id:
        argv.append("--cli-project-id=%s" % project_id)
    if name:
        argv.append("--name=%s" % name)
    if datastore_type:
        argv.append("--datastore_type=%s" % datastore_type)
    if instance_id:
        argv.append("--id=%s" % instance_id)
    return argv


def _hcloud_executable():
    return os.environ.get("RDS_LIST_MD_HCLOUD_BIN", "hcloud")


def run_hcloud(argv):
    """Execute hcloud and return (stdout, stderr, returncode)."""
    cmd = [_hcloud_executable()]
    extra = os.environ.get("RDS_LIST_MD_HCLOUD_ARGS", "").split()
    if extra:
        cmd.extend(extra)
    cmd.extend(argv)
    try:
        proc = subprocess.run(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            timeout=120, universal_newlines=True,
        )
    except FileNotFoundError:
        raise ConfigError(
            "未找到 hcloud（KooCLI）。请先安装 KooCLI 并完成认证配置，"
            "参见 references/cli-installation-guide.md。"
        )
    except subprocess.TimeoutExpired:
        raise ApiError("hcloud 执行超时（120s），请检查网络后重试。")
    return proc.stdout or "", proc.stderr or "", proc.returncode


def extract_json(stdout):
    """Parse hcloud stdout as JSON; tolerate wrapper/noise lines."""
    text = stdout.strip()
    if not text:
        return {}
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start, end = text.find("{"), text.rfind("}")
        if start >= 0 and end > start:
            try:
                return json.loads(text[start:end + 1])
            except json.JSONDecodeError:
                pass
        raise ApiError("hcloud 输出无法解析为 JSON：%s" % text[:200])


def classify_hcloud_failure(stdout, stderr, returncode):
    """Map a failed hcloud invocation to a domain error with explicit hints."""
    blob = (stderr + " " + stdout).strip()
    low = blob.lower()
    if _USE_ERROR_MARKER in low:
        return ApiError(
            "hcloud 参数错误（KooCLI 拒绝了该参数组合，退出码 %s）：RDS ListInstances "
            "真实参数清单可通过 `hcloud RDS ListInstances --help` 查看。"
            "详情：%s" % (returncode, blob[:300])
        )
    if any(p in low for p in _CREDENTIAL_MISSING_PATTERNS) and not re.search(
            r"\b40[13]\b", blob):
        return ConfigError(
            "缺少 AK/SK 凭证：hcloud 未配置有效凭证。请先运行 hcloud configure 或"
            "设置凭证环境变量（严禁在对话中粘贴 AK/SK），参见"
            " references/cli-installation-guide.md。详情：%s" % blob[:300]
        )
    if any(p in low for p in _AUTH_PATTERNS):
        return AuthError(
            "无权限访问 RDS，请检查 IAM 权限（403：AK/SK 无效或未授予 RDS 只读权限），"
            "参见 references/iam-policies.md。详情：%s" % blob[:300]
        )
    return ApiError(
        "hcloud 调用失败（退出码 %s）：%s" % (returncode, blob[:300])
    )


def extract_instances(payload):
    """Pull the instance list out of a ListInstances response."""
    if isinstance(payload, list):
        return payload
    for key in _INSTANCE_LIST_KEYS:
        value = payload.get(key)
        if isinstance(value, list):
            return value
    return []


def _has_more(batch, collected, limit, payload):
    if not batch:
        return False
    total = None
    if isinstance(payload, dict):
        for key in ("total_count", "totalCount", "total"):
            if isinstance(payload.get(key), int):
                total = payload[key]
                break
    if total is not None and total >= 0:
        return collected < total
    return len(batch) >= limit


def filter_by_status(instances, status):
    """Client-side status filter (case-insensitive).

    The real RDS ListInstances API / KooCLI has no `status` parameter, so
    filtering by instance state happens here, after the full (paged) list has
    been fetched. An empty result is reported as a normal empty list.
    """
    if not status:
        return list(instances)
    wanted = str(status).strip().lower()
    matched = []
    for instance in instances:
        value = instance.get("status") if isinstance(instance, dict) else None
        if value is not None and str(value).strip().lower() == wanted:
            matched.append(instance)
    return matched


def resolve_sort_by(sort_by):
    """Normalize and validate a `--sort-by` value (None when omitted).

    Values are matched case-insensitively; anything other than `name` /
    `created` raises `SortError` so `main()` can fail fast with exit code 1
    (argparse `choices` would exit with 2 and break the skill's error contract).
    """
    if sort_by is None:
        return None
    value = str(sort_by).strip().lower()
    if not value:
        return None
    if value not in SORTABLE_KEYS:
        raise SortError("--sort-by 仅支持 name 或 created（收到: %s）" % sort_by)
    return value


def parse_created(value):
    """Parse an instance `created` timestamp into an aware UTC datetime.

    Huawei Cloud returns several ISO-8601 variants: `2026-01-02T03:04:05Z`,
    `2026-01-02T03:04:05+0800`, and space-separated `2026-01-02 03:04:05`.
    Naive values (no timezone) are treated as UTC so that aware and naive
    timestamps remain comparable — mixing them directly raises `TypeError`.
    Returns None for missing / unparseable values.
    """
    text = str(value).strip()
    if not text:
        return None
    candidate = text
    if candidate[-1:] in ("Z", "z"):
        candidate = candidate[:-1] + "+00:00"
    if " " in candidate:
        candidate = candidate.replace(" ", "T", 1)
    # Python < 3.11 rejects the compact ±HHMM offset form, so normalize it to
    # ±HH:MM (keeps sorted order correct on the skill's minimum Python 3.8).
    compact_offset = re.search(r"([+-]\d{2})(\d{2})$", candidate)
    if compact_offset:
        candidate = "%s%s:%s" % (candidate[:compact_offset.start()],
                                 compact_offset.group(1),
                                 compact_offset.group(2))
    try:
        parsed = datetime.datetime.fromisoformat(candidate)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=datetime.timezone.utc)
    return parsed.astimezone(datetime.timezone.utc)


def _sort_value(instance, sort_by):
    """Return (usable, comparable) for one instance under `sort_by`.

    `usable=False` marks a missing key; such records are always placed last.
    `created` values whose text cannot be parsed fall back to lowercased text
    comparison (flagged by the tuple's first element so a float and a string
    are never compared directly).
    """
    if not isinstance(instance, dict):
        return False, None
    if sort_by == "name":
        value = _field(instance, "name", "instance_name", default=None)
        if value is None:
            value = _field(instance, "id", "instance_id", default=None)
        if value is None:
            return False, None
        text = str(value).strip()
        if not text:
            return False, None
        return True, text.lower()
    raw = _field(instance, "created", default=None)
    if raw is None:
        return False, None
    text = str(raw).strip()
    if not text or text == "-":
        return False, None
    parsed = parse_created(text)
    if parsed is None:
        return True, (1, text.lower())
    return True, (0, parsed.timestamp())


def sort_instances(instances, sort_by=None):
    """Sort instances locally by `name` or `created` (ascending).

    `sort_by` empty → the API order is preserved (a copy is returned, so the
    caller's list is never mutated). `name` compares case-insensitively with an
    id fallback; `created` compares parsed timestamps oldest-first with a text
    fallback for unparseable values. Records missing the sort key are always
    last, and `sorted()` keeps ties in their original relative order.
    """
    key = resolve_sort_by(sort_by)
    if key is None:
        return list(instances)
    valid, invalid = [], []
    for instance in instances:
        usable, _value = _sort_value(instance, key)
        (valid if usable else invalid).append(instance)
    valid.sort(key=lambda item: _sort_value(item, key)[1])
    return valid + invalid


def list_instances_via_sdk(region, name=None,
                           datastore_type=None, instance_id=None,
                           limit=DEFAULT_PAGE_SIZE, max_pages=100,
                           project_id=None):
    """SDK fallback: query instances through `huaweicloudsdkrds` v3.

    Only invoked when hcloud is not installed. Credentials are read by name
    from an explicit whitelist (HW_*/HUAWEI_ACCESS_KEY family) — never by
    enumerating os.environ, and never passed as literals here. `project_id` is
    a path parameter resolved by the
    SDK client from the credential + region; it is accepted for signature
    parity with the CLI path but not set on the request. `ListInstancesRequest`
    has no `status` attribute, so status filtering is NOT done here — the
    caller applies `filter_by_status()` on the returned list.
    """
    try:
        from huaweicloudsdkcore.auth.credentials import BasicCredentials
        from huaweicloudsdkcore.region.region import Region
        from huaweicloudsdkcore.http.http_config import HttpConfig
        from huaweicloudsdkrds.v3 import RdsClient, ListInstancesRequest
        from huaweicloudsdkrds.v3.region.rds_region import RdsRegion
    except ImportError as exc:
        raise ConfigError(
            "未找到 hcloud（KooCLI），且 huaweicloudsdkcore/huaweicloudsdkrds 未安装，"
            "无法回退到 SDK。请安装 KooCLI 或 pip install huaweicloudsdkcore "
            "huaweicloudsdkrds。详情：%s" % exc
        )

    ak = _env_value(_AK_ENV_NAMES)
    sk = _env_value(_SK_ENV_NAMES)
    if not ak or not sk:
        raise ConfigError(
            "SDK 回退缺少 AK/SK 凭证：官方 SDK 的 BasicCredentials 不会自动读取环境"
            "变量，且当前环境未检测到白名单中的 AK/SK 环境变量（HW_ACCESS_KEY /"
            " HUAWEI_ACCESS_KEY / HUAWEICLOUD_SDK_AK 等）。"
            "请在会话外设置 HUAWEI_ACCESS_KEY / HUAWEI_SECRET_KEY（严禁在对话中粘贴"
            " AK/SK），参见 references/cli-installation-guide.md。"
        )
    credentials = BasicCredentials(ak=ak, sk=sk)  # env-sourced, never literals
    try:
        try:
            region_obj = RdsRegion.value_of(region)
        except (ValueError, KeyError, AttributeError):
            region_obj = Region(region, "https://rds.%s.myhuaweicloud.com" % region)
        client = RdsClient.new_builder() \
            .with_credentials(credentials) \
            .with_region(region_obj) \
            .with_http_config(HttpConfig.get_default_config()) \
            .build()
    except Exception as exc:  # region unknown / config broken
        raise ConfigError(
            "SDK 初始化失败（region=%s）：%s。请检查 huaweicloudsdkrds 安装与区域配置。"
            % (region, exc)
        )
    instances = []
    offset = 0
    for _ in range(max_pages):
        request = ListInstancesRequest(
            limit=limit, offset=offset,
            id=instance_id, name=name,
            datastore_type=datastore_type,
        )
        try:
            response = client.list_instances(request)
        except Exception as exc:
            low = str(exc).lower()
            if any(p in low for p in _AUTH_PATTERNS):
                raise AuthError(
                    "无权限访问 RDS，请检查 IAM 权限（403）。详情：%s" % str(exc)[:300]
                )
            raise ApiError("SDK 调用失败：%s" % str(exc)[:300])
        batch = list(response.instances or [])
        instances.extend(instance.to_dict() for instance in batch)
        total = getattr(response, "total_count", None)
        if total is not None and len(instances) >= total:
            break
        if len(batch) < limit:
            break
        offset += len(batch)
    else:
        raise ApiError("翻页超过 %d 页仍未取完，已中止以防死循环。" % max_pages)
    return instances


def list_instances(region, status=None, name=None, datastore_type=None,
                   instance_id=None, limit=DEFAULT_PAGE_SIZE, max_pages=100,
                   project_id=None):
    """Query all RDS instances (paged); KooCLI first, SDK fallback.

    `status` is intentionally NOT forwarded to hcloud or the SDK — the real
    RDS ListInstances API has no status parameter. Instead the full list is
    fetched first, then `filter_by_status()` is applied client-side.
    """
    instances = []
    offset = 0
    for _page in range(max_pages):
        argv = build_command(region, name=name,
                             datastore_type=datastore_type,
                             instance_id=instance_id,
                             limit=limit, offset=offset,
                             project_id=project_id)
        try:
            stdout, stderr, returncode = run_hcloud(argv)
        except ConfigError:
            # hcloud binary missing → one-shot SDK fallback (no CLI retry).
            instances = list_instances_via_sdk(
                region, name=name,
                datastore_type=datastore_type, instance_id=instance_id,
                limit=limit, max_pages=max_pages, project_id=project_id,
            )
            break
        if returncode != 0 or _USE_ERROR_MARKER in (stdout + " " + stderr).lower():
            # KooCLI usage errors print [USE_ERROR] on stdout with rc=0.
            raise classify_hcloud_failure(stdout, stderr, returncode)
        payload = extract_json(stdout)
        batch = extract_instances(payload)
        instances.extend(batch)
        if not _has_more(batch, len(instances), limit, payload):
            break
        offset += len(batch) if batch else limit
    else:
        raise ApiError("翻页超过 %d 页仍未取完，已中止以防死循环。" % max_pages)
    return filter_by_status(instances, status)


def normalize_instance(instance):
    """Flatten nested datastore / ip list fields into table-friendly keys."""
    flat = dict(instance)
    datastore = instance.get("datastore") or {}
    if isinstance(datastore, dict):
        flat.setdefault("engine", datastore.get("type", "-"))
        flat.setdefault("engineVersion", datastore.get("version", "-"))
    else:
        flat.setdefault("engine", "-")
        flat.setdefault("engineVersion", "-")
    private_ips = instance.get("private_ips") or instance.get("ips")
    if isinstance(private_ips, list):
        flat["privateIps"] = ",".join(str(ip) for ip in private_ips) if private_ips else "-"
    elif isinstance(private_ips, str):
        flat["privateIps"] = private_ips
    else:
        flat["privateIps"] = "-"
    nodes = instance.get("nodes") or []
    if isinstance(nodes, list) and nodes and "availability_zone" not in flat:
        az = nodes[0].get("availability_zone") if isinstance(nodes[0], dict) else None
        if az:
            flat["availability_zone"] = az
    return flat


def _field(instance, *names, default="-"):
    for name in names:
        if name in instance and instance[name] not in (None, ""):
            return instance[name]
    return default


def instance_names(instances):
    names = []
    for instance in instances:
        name = _field(instance, "name", "instance_name", default=None)
        if name is None:
            name = _field(instance, "id", "instance_id")
        names.append(str(name))
    return names


def _md_cell(value):
    """Render one Markdown table cell, escaping pipes and collapsing newlines."""
    if isinstance(value, (dict, list)):
        value = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    text = str(value)
    text = text.replace("\r\n", " ").replace("\n", " ").replace("\r", " ")
    text = text.replace("|", "\\|")
    return text or "-"


def render_markdown(instances, region, generated_at=None):
    """Render the instance list as a Markdown document (title + table).

    An empty instance list still produces a valid document: the table header +
    separator followed by an explicit "no instances" note (never an error).
    """
    rows_data = [normalize_instance(instance) for instance in instances]
    header = "| " + " | ".join(label for label, _ in MD_COLUMNS) + " |"
    separator = "| " + " | ".join("---" for _ in MD_COLUMNS) + " |"
    lines = [
        "# Huawei Cloud RDS Instances — %s" % region,
        "",
        "> Region: %s | Instances: %d" % (region, len(rows_data)),
    ]
    if generated_at:
        lines.append("> Generated at: %s" % generated_at)
    lines += ["", header, separator]
    for instance in rows_data:
        cells = []
        for _label, keys in MD_COLUMNS:
            cells.append(_md_cell(_field(instance, *keys)))
        lines.append("| " + " | ".join(cells) + " |")
    if not rows_data:
        lines += ["", "_当前区域（%s）无 RDS 实例。_" % region]
    lines.append("")
    return "\n".join(lines)


def write_markdown(content, output_path):
    """Write `content` to `output_path` atomically (temp file + rename).

    Missing parent directories are created. An interrupted write never leaves
    a corrupt / partial file behind.
    """
    try:
        directory = os.path.dirname(os.path.abspath(output_path))
        os.makedirs(directory, exist_ok=True)
        tmp_fd, tmp_path = tempfile.mkstemp(prefix=".rds-md-", suffix=".tmp",
                                            dir=directory)
    except (OSError, ValueError) as exc:
        raise ApiError("Markdown 文件写出失败（目录 %s 不可创建）：%s"
                       % (os.path.dirname(os.path.abspath(output_path)), exc))
    try:
        with os.fdopen(tmp_fd, "w", encoding="utf-8") as handle:
            handle.write(content)
        os.replace(tmp_path, output_path)
    except (OSError, ValueError) as exc:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise ApiError("Markdown 文件写出失败（%s）：%s" % (output_path, exc))
    return output_path


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="查询华为云 RDS 实例并渲染为 Markdown 文件（KooCLI hcloud RDS "
                    "ListInstances，只读）。")
    parser.add_argument("-r", "--region", default=DEFAULT_REGION,
                        help="目标 Region（默认 %s）" % DEFAULT_REGION)
    parser.add_argument("--project_id", "--project-id", dest="project_id",
                        default=None,
                        help="项目 ID（CLI 路径映射为全局参数 --cli-project-id；"
                             "SDK 路径由凭据+Region 解析，缺省即可）")
    parser.add_argument("-o", "--output", default=None,
                        help="Markdown 输出文件路径（默认当前目录 %s）"
                             % DEFAULT_OUTPUT)
    parser.add_argument("--name", help="按实例名称过滤")
    parser.add_argument("--status",
                        help="按实例状态过滤（ACTIVE/FAILED/BUILDING 等；"
                             "RDS ListInstances API 无此参数，全量取回后本地过滤）")
    parser.add_argument("--sort-by", dest="sort_by", default=None,
                        help="排序字段：name（按实例名，大小写不敏感）或 "
                             "created（按创建时间，旧→新）；排序在拉取列表后于本地"
                             "执行，缺省保持 API 原序")
    parser.add_argument("--page-size", type=int, default=DEFAULT_PAGE_SIZE,
                        dest="page_size", help="分页大小（默认 %d）" % DEFAULT_PAGE_SIZE)
    parser.add_argument("--operation", default=ALLOWED_OPERATION,
                        help="hcloud RDS 操作名（仅允许只读 %s）" % ALLOWED_OPERATION)
    parser.add_argument("--stdout", action="store_true",
                        help="除写文件外，同时把 Markdown 内容打印到标准输出")
    args = parser.parse_args(argv)

    try:
        # Write-intent guard: scan the scrubbed raw argv + validate the operation.
        raw_argv = argv if argv is not None else sys.argv[1:]
        guard_write_intent(scrub_read_only_values(raw_argv))
        guard_operation(args.operation)
        # Validate --sort-by before any API call so an unknown value fails fast
        # and never writes a file.
        sort_by = resolve_sort_by(args.sort_by)
        instances = list_instances(
            args.region,
            status=args.status,
            name=args.name,
            limit=args.page_size,
            project_id=args.project_id,
        )
        instances = sort_instances(instances, sort_by)
        output_path = args.output or os.path.join(os.getcwd(), DEFAULT_OUTPUT)
        generated_at = datetime.datetime.now(datetime.timezone.utc).strftime(
            "%Y-%m-%dT%H:%M:%SZ")
        content = render_markdown(instances, args.region, generated_at)
        write_markdown(content, output_path)
    except RdsListError as exc:
        print("[错误] %s" % exc, file=sys.stderr)
        return 1

    if args.stdout:
        print(content)
    if instances:
        print("已生成 Markdown 文件：%s（Region %s，共 %d 个 RDS 实例）。"
              % (os.path.abspath(output_path), args.region, len(instances)))
    else:
        filters = []
        if args.status:
            filters.append("status=%s" % args.status)
        if args.name:
            filters.append("name=%s" % args.name)
        if sort_by:
            filters.append("sort-by=%s" % sort_by)
        suffix = "过滤条件: %s" % ", ".join(filters) if filters else "无过滤条件"
        print("已生成 Markdown 文件：%s（Region %s 无 RDS 实例，%s；"
              "已输出表头与空表提示）。"
              % (os.path.abspath(output_path), args.region, suffix))
    return 0


if __name__ == "__main__":
    sys.exit(main())