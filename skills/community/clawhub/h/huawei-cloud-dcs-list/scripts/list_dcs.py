#!/usr/bin/env python3
"""List Huawei Cloud DCS (Distributed Cache Service, Redis/Memcached) instances
via KooCLI `hcloud DCS ListInstances` (read-only GET /v2/{project_id}/instances).

Primary execution path is KooCLI; when hcloud is not installed, the script falls
back to the official `huaweicloudsdkdcs` v2 SDK (`DcsClient.list_instances`).
Reads nothing but the active credential profile / environment. Supports four
output modes (--names-only / table / --json / Markdown table), --name /
--instance-id / --ip / --status / --tags filtering, optional --sort-by
name|created ordering (client-side, case-insensitive name / ascending
created_at, stable) and automatic --limit / --offset paging (the real
ListInstances API parameters, verified against `hcloud DCS ListInstances
--help` and the huaweicloudsdkdcs v2 ListInstancesRequest model), plus a
strict write-intent guard: any argument that looks like a mutating DCS
operation is rejected before a single command is executed.

Markdown mode (--md / --format md) prints a GitHub-flavored table whose ten
columns match huawei-cloud-dcs-export-markdown verbatim (名称/ID/引擎/版本/
容量/规格/状态/连接地址/端口/可用区, missing values rendered as "-"), and can
optionally persist exactly that text with --md-output <path> (temp file +
atomic rename).

Usage:
    python3 scripts/list_dcs.py [--region cn-north-4]
                                 [--names-only | --table | --json | --md]
                                 [--format names|table|json|md] [--md-output <path>]
                                 [--name cache] [--instance-id <id>] [--ip <ip>]
                                 [--status RUNNING] [--tags env=prod]
                                 [--sort-by name|created]
                                 [--page-size 100] [--operation ListInstances]

Environment overrides (mostly for tests):
    DCS_LIST_HCLOUD_BIN   hcloud executable (default "hcloud")
    DCS_LIST_HCLOUD_ARGS  extra args injected before the DCS operation
"""

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile

# Keep the shipped skill directory clean: never emit __pycache__/*.pyc.
sys.dont_write_bytecode = True

DEFAULT_REGION = "cn-north-4"
DEFAULT_PAGE_SIZE = 100
SERVICE = "DCS"
ALLOWED_OPERATION = "ListInstances"
REST_PATH = "/v2/{project_id}/instances"

# Output modes (--format values + the legacy boolean flags).
MODE_NAMES = "names"
MODE_TABLE = "table"
MODE_JSON = "json"
MODE_MD = "md"
MODE_CHOICES = (MODE_NAMES, MODE_TABLE, MODE_JSON, MODE_MD)
DEFAULT_MODE = MODE_NAMES

# Client-side ordering (--sort-by). Both orders are ascending and stable.
SORT_NAME = "name"
SORT_CREATED = "created"
SORT_CHOICES = (SORT_NAME, SORT_CREATED)

# Markdown table contract — kept byte-identical to
# huawei-cloud-dcs-export-markdown/scripts/export_markdown.py::MD_HEADERS so
# both skills describe a DCS instance with the same ten columns.
MD_HEADERS = [
    "名称", "ID", "引擎", "版本", "容量", "规格", "状态", "连接地址", "端口", "可用区",
]
# One column spec per MD_HEADERS entry; the first key present wins.
MD_COLUMNS = (
    ("name",),
    ("instance_id", "id"),
    ("engine",),
    ("engine_version",),
    ("capacity",),
    ("spec_code",),
    ("status",),
    ("ip",),
    ("port",),
    ("az_codes",),
)
# Fallback marker used when a per-instance field was not returned by DCS.
MD_FIELD_MISSING = "-"

# Mutating DCS operations / intents — strictly rejected by the guard.
WRITE_INTENT_KEYWORDS = (
    "createinstance",
    "batchdeleteinstances",
    "deletesingleinstance",
    "deleteinstance",
    "updateinstance",
    "modifyinstance",
    "resizeinstance",
    "restartinstance",
    "restartorflushinstances",
    "flushinstance",
    "restoreinstance",
    "upgradeinstanceminorversion",
    "exchangerinstanceip",
    "exchangeinstanceip",
    "rollbackexchangeinstanceip",
    "copyinstance",
    "updateinstancebandwidth",
    "updateinstanceconfig",
    "setinstancepassword",
    "resetinstancepassword",
    "create",
    "delete",
    "update",
    "modify",
    "resize",
    "restart",
    "reboot",
    "flush",
    "clear",
    "restore",
    "upgrade",
    "rollback",
    "backup",
    "freeze",
    "unfreeze",
    "release",
    "stop",
    "start",
    "terminate",
    "destroy",
    "creating",
    "deleting",
    "updating",
    "restarting",
    "resizing",
    "restoring",
    "upgrading",
    "rebooting",
    "flushing",
    "clearing",
)

# Preferred column order for the table view; remaining keys are appended sorted.
PREFERRED_COLUMNS = [
    "name",
    "instance_id",
    "engine",
    "engine_version",
    "capacity",
    "spec_code",
    "status",
    "port",
    "ip",
    "domain_name",
    "readonly_domain_name",
    "access_user",
    "no_password_access",
    "enable_ssl",
    "enable_publicip",
    "publicip_address",
    "charging_mode",
    "vpc_name",
    "vpc_id",
    "subnet_id",
    "security_group_id",
    "az_codes",
    "max_memory",
    "used_memory",
    "cpu_type",
    "user_name",
    "maintain_begin",
    "maintain_end",
    "description",
    "tags",
    "enterprise_project_id",
    "created_at",
    "updated_at",
    "sub_status",
]

_INSTANCE_LIST_KEYS = ("instances", "instance_list", "instances_detail")

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


class DcsListError(Exception):
    """Base error for the DCS list skill."""


class GuardError(DcsListError):
    """A write intent was detected and blocked (skill is read-only)."""


class ConfigError(DcsListError):
    """hcloud missing or credentials (AK/SK) not configured."""


class AuthError(DcsListError):
    """Authentication/authorization failure (invalid AK/SK or IAM 403)."""


class ApiError(DcsListError):
    """hcloud / network / unexpected API failure."""


def guard_write_intent(text):
    """Return False for read-only text; raise GuardError if `text` is mutating.

    Normalizes separators so `--create-instance`, `CreateInstance`, and
    `create_instance` all hit the same keyword. Read-only vocabulary
    (list/show/get/describe) never matches.
    """
    low = re.sub(r"[\s_\-]+", "", str(text).lower())
    for keyword in WRITE_INTENT_KEYWORDS:
        if keyword in low:
            raise GuardError(
                "检测到写操作意图（关键词: %s）。本 skill 仅支持只读查询"
                "（DCS ListInstances），创建/删除/扩缩容/重启/清空等变更操作已被守卫拦截。"
                % keyword
            )
    return False


def guard_operation(operation):
    """Only the read-only ListInstances operation may be executed."""
    if operation != ALLOWED_OPERATION:
        raise GuardError(
            "不允许的操作 %r：本 skill 仅允许只读操作 %s。" % (operation, ALLOWED_OPERATION)
        )
    return True


def build_command(region, name=None, instance_id=None, ip=None, status=None,
                  tags=None, limit=DEFAULT_PAGE_SIZE, offset=0):
    """Build the hcloud DCS ListInstances argv (without the executable).

    Mirrors the real KooCLI parameter list (verified in the DCS
    ListInstances help output):
    --cli-region / --name / --instance_id / --ip / --status / --tags are all
    real server-side query parameters; paging uses --limit (1..1000, default
    10 per page when unset) + --offset. The marker is never sent on the first
    page (offset starts at 0).
    """
    argv = [
        SERVICE,
        ALLOWED_OPERATION,
        "--cli-region=%s" % region,
        "--limit=%d" % limit,
        "--offset=%d" % offset,
    ]
    if name:
        argv.append("--name=%s" % name)
    if instance_id:
        argv.append("--instance_id=%s" % instance_id)
    if ip:
        argv.append("--ip=%s" % ip)
    if status:
        argv.append("--status=%s" % status)
    if tags:
        argv.append("--tags=%s" % tags)
    return argv


def _hcloud_executable():
    return os.environ.get("DCS_LIST_HCLOUD_BIN", "hcloud")


def run_hcloud(argv):
    """Execute hcloud and return (stdout, stderr, returncode)."""
    cmd = [_hcloud_executable()]
    extra = os.environ.get("DCS_LIST_HCLOUD_ARGS", "").split()
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


def _payload_error(payload):
    """Map an API error body returned with exit code 0 to a domain error.

    KooCLI can print the DCS error body on stdout and still exit 0, so the
    payload must be inspected before any success handling. A normal
    ListInstances response never carries error_code/error_msg, so those keys
    are an unambiguous error marker.
    """
    if not isinstance(payload, dict):
        return None
    code = payload.get("error_code")
    msg = payload.get("error_msg") or payload.get("error_message")
    if not code and not msg:
        return None
    detail = "DCS API 错误 %s: %s" % (code or "-", msg or "-")
    blob = ("%s %s" % (code or "", msg or "")).lower()
    if any(pattern in blob for pattern in _AUTH_PATTERNS):
        return AuthError(
            "无权限访问分布式缓存服务（DCS），请检查 IAM 权限"
            "（403：AK/SK 无效或未授予 DCS 只读权限），"
            "参见 references/iam-policies.md。详情：%s" % detail
        )
    return ApiError(detail)


def extract_json(stdout):
    """Parse hcloud stdout as JSON; tolerate wrapper/noise lines.

    KooCLI may append a diagnostic table after the JSON body, so the first
    complete JSON value is decoded starting at the first ``{`` instead of
    slicing through the last ``}`` (which the trailing table would break).
    An error body returned with exit code 0 is raised as an API/auth error
    rather than being reported as unparseable output.
    """
    text = stdout.strip()
    if not text:
        return {}
    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        payload = None
        start = text.find("{")
        if start >= 0:
            try:
                payload, _end = json.JSONDecoder().raw_decode(text, start)
            except json.JSONDecodeError:
                payload = None
        if payload is None:
            raise ApiError("hcloud 输出无法解析为 JSON：%s" % text[:200])
    error = _payload_error(payload)
    if error is not None:
        raise error
    return payload


def classify_hcloud_failure(stdout, stderr, returncode):
    """Map a failed hcloud invocation to a domain error with explicit hints."""
    blob = (stderr + " " + stdout).strip()
    low = blob.lower()
    if _USE_ERROR_MARKER in low:
        return ApiError(
            "hcloud 参数错误（KooCLI 拒绝了该参数组合，退出码 %s）：DCS ListInstances "
            "真实参数清单可通过 `hcloud DCS ListInstances --help` 查看。"
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
            "无权限访问分布式缓存服务（DCS），请检查 IAM 权限"
            "（403：AK/SK 无效或未授予 DCS 只读权限），"
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
    """Decide whether another ListInstances page should be fetched."""
    if not batch:
        return False
    total = None
    if isinstance(payload, dict):
        for key in ("instance_num", "total_num", "total_count", "totalCount", "total"):
            if isinstance(payload.get(key), int):
                total = payload[key]
                break
    if total is not None and total >= 0:
        return collected < total
    return len(batch) >= limit


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
_PROJECT_ID_ENV_NAMES = (
    "HW_PROJECT_ID",
    "HUAWEI_PROJECT_ID",
    "HUAWEICLOUD_SDK_PROJECT_ID",
    "HUAWEI_CLOUD_PROJECT_ID",
)


def _env_value(names):
    """Read the first non-empty value from an explicit whitelist of env names."""
    for name in names:
        value = os.environ.get(name)
        if value:
            return value
    return None


def resolve_project_id(explicit=None):
    """Resolve the project id from --project-id or the whitelisted env names."""
    if explicit:
        return explicit
    return _env_value(_PROJECT_ID_ENV_NAMES)


def _jsonable(value):
    """Recursively convert datetimes (SDK to_dict output) to JSON-safe values."""
    return json.loads(json.dumps(value, ensure_ascii=False, default=str))


def list_instances_via_sdk(region, name=None, instance_id=None, ip=None,
                           status=None, tags=None, limit=DEFAULT_PAGE_SIZE,
                           project_id=None, max_pages=100):
    """SDK fallback: query instances through `huaweicloudsdkdcs` v2.

    Only invoked when hcloud is not installed. Credentials are taken from the
    whitelisted AK/SK environment variables (HW_*/HUAWEI_ACCESS_KEY family) —
    never passed as literals here. The official SDK has no env-var
    auto-discovery on `BasicCredentials()`, so AK/SK (and the project id
    required by the `/v2/{project_id}/instances` path) must be read explicitly.
    Region resolution uses the SDK's own `DcsRegion` catalog (official
    endpoints, no guessing), falling back to an explicit `Region(id, endpoint)`
    for custom regions. `ListInstancesRequest` accepts name / instance_id /
    ip / status / tags / limit / offset (verified against the installed SDK);
    paging follows `instance_num` + the batch size.
    """
    try:
        from huaweicloudsdkcore.auth.credentials import BasicCredentials
        from huaweicloudsdkcore.region.region import Region
        from huaweicloudsdkcore.http.http_config import HttpConfig
        from huaweicloudsdkdcs.v2 import DcsClient, ListInstancesRequest
        from huaweicloudsdkdcs.v2.region.dcs_region import DcsRegion
    except ImportError as exc:
        raise ConfigError(
            "未找到 hcloud（KooCLI），且 huaweicloudsdkcore/huaweicloudsdkdcs 未安装，"
            "无法回退到 SDK。请安装 KooCLI 或 pip install huaweicloudsdkcore "
            "huaweicloudsdkdcs。详情：%s" % exc
        )

    ak = _env_value(_AK_ENV_NAMES)
    sk = _env_value(_SK_ENV_NAMES)
    if not ak or not sk:
        raise ConfigError(
            "SDK 回退缺少 AK/SK 凭证：官方 SDK 的 BasicCredentials 不会自动读取环境"
            "变量，且当前环境未检测到 HW_ACCESS_KEY / HUAWEI_ACCESS_KEY / "
            "HUAWEICLOUD_SDK_AK 形式的 AK/SK 环境变量。"
            "请在会话外设置 HUAWEI_ACCESS_KEY / HUAWEI_SECRET_KEY（严禁在对话中粘贴"
            " AK/SK），参见 references/cli-installation-guide.md。"
        )
    resolved_project_id = resolve_project_id(project_id)
    if not resolved_project_id:
        raise ConfigError(
            "SDK 回退缺少 project_id：DCS 的 REST 路径为 %s，需要项目 ID。"
            "请通过 --project-id 传入，或设置 HUAWEICLOUD_SDK_PROJECT_ID / "
            "HUAWEI_PROJECT_ID（严禁在对话中粘贴敏感信息）。" % REST_PATH
        )
    credentials = BasicCredentials(ak=ak, sk=sk, project_id=resolved_project_id)  # env-sourced, never literals
    try:
        try:
            region_obj = DcsRegion.value_of(region)
        except (ValueError, KeyError, AttributeError):
            region_obj = Region(region, "https://dcs.%s.myhuaweicloud.com" % region)
        client = DcsClient.new_builder() \
            .with_credentials(credentials) \
            .with_region(region_obj) \
            .with_http_config(HttpConfig.get_default_config()) \
            .build()
    except Exception as exc:  # region unknown / config broken
        raise ConfigError(
            "SDK 初始化失败（region=%s）：%s。请检查 huaweicloudsdkdcs 安装与区域配置。"
            % (region, exc)
        )
    instances = []
    offset = 0
    for _ in range(max_pages):
        request = ListInstancesRequest(
            limit=limit, offset=offset,
            name=name, instance_id=instance_id,
            ip=ip, status=status, tags=tags,
        )
        try:
            response = client.list_instances(request)
        except Exception as exc:
            low = str(exc).lower()
            if any(p in low for p in _AUTH_PATTERNS):
                raise AuthError(
                    "无权限访问分布式缓存服务（DCS），请检查 IAM 权限（403）。详情：%s"
                    % str(exc)[:300]
                )
            raise ApiError("SDK 调用失败：%s" % str(exc)[:300])
        batch = list(response.instances or [])
        instances.extend(_jsonable(instance.to_dict()) for instance in batch)
        total = getattr(response, "instance_num", None)
        if total is not None and len(instances) >= total:
            break
        if len(batch) < limit:
            break
        offset += len(batch)
    else:
        raise ApiError("翻页超过 %d 页仍未取完，已中止以防死循环。" % max_pages)
    return instances


def list_instances(region, name=None, instance_id=None, ip=None, status=None,
                   tags=None, limit=DEFAULT_PAGE_SIZE, project_id=None,
                   max_pages=100):
    """Query all DCS instances (offset-paged); KooCLI first, SDK fallback."""
    instances = []
    offset = 0
    for _page in range(max_pages):
        argv = build_command(region, name=name, instance_id=instance_id,
                             ip=ip, status=status, tags=tags,
                             limit=limit, offset=offset)
        try:
            stdout, stderr, returncode = run_hcloud(argv)
        except ConfigError:
            # hcloud binary missing → one-shot SDK fallback (no CLI retry).
            return list_instances_via_sdk(
                region, name=name, instance_id=instance_id, ip=ip,
                status=status, tags=tags, limit=limit,
                project_id=project_id, max_pages=max_pages,
            )
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
    return instances


def normalize_instance(instance):
    """Flatten az_codes / tags lists into table-friendly cells."""
    flat = dict(instance)
    if "instance_id" not in flat and "id" in flat:
        flat["instance_id"] = flat["id"]
    az_codes = flat.get("az_codes")
    if isinstance(az_codes, list):
        flat["az_codes"] = ",".join(str(code) for code in az_codes) or "-"
    tags = flat.get("tags")
    if isinstance(tags, list):
        cells = []
        for tag in tags:
            if isinstance(tag, dict):
                cells.append("%s=%s" % (tag.get("key", ""), tag.get("value", "")))
            else:
                cells.append(str(tag))
        flat["tags"] = ",".join(cells) if cells else "-"
    return flat


def _field(instance, *names, default="-"):
    for name in names:
        if name in instance and instance[name] not in (None, ""):
            return instance[name]
    return default


def _sort_name_key(instance):
    """Case-insensitive instance-name key, falling back to the instance id."""
    name = _field(instance, "name", "instance_name", default=None)
    if name is None:
        name = _field(instance, "instance_id", "id", default="")
    return str(name).strip().lower()


def _sort_created_key(instance):
    """Ascending created_at key (ISO8601 sorts lexicographically); missing last."""
    created = _field(instance, "created_at", default=None)
    if created is None:
        return (1, "")
    return (0, str(created))


def sort_instances(instances, sort_by):
    """Return a stably ordered copy of ``instances`` (ascending).

    ``name`` sorts case-insensitively by instance name (missing name falls
    back to the instance id); ``created`` sorts by the ISO8601 ``created_at``
    string, with instances missing that field pushed to the end. Ties keep
    their original (paged) order because ``sorted`` is stable.
    """
    if not sort_by:
        return list(instances)
    if sort_by == SORT_NAME:
        return sorted(instances, key=_sort_name_key)
    return sorted(instances, key=_sort_created_key)


def instance_names(instances):
    names = []
    for instance in instances:
        name = _field(instance, "name", "instance_name", default=None)
        if name is None:
            name = _field(instance, "instance_id", "id")
        names.append(str(name))
    return names


def _cell(value):
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return str(value)


def render_table(instances):
    """Render full-field table output (union of all returned fields)."""
    rows_data = [normalize_instance(instance) for instance in instances]
    columns = []
    for key in PREFERRED_COLUMNS:
        if any(key in i for i in rows_data):
            columns.append(key)
    for key in sorted({k for i in rows_data for k in i}):
        if key not in columns:
            columns.append(key)
    if not columns:
        columns = ["name", "instance_id"]
    rows = [[_cell(_field(i, col)) for col in columns] for i in rows_data]
    widths = [max(len(col), *(len(row[i]) for row in rows)) for i, col in enumerate(columns)]
    header = "  ".join(col.ljust(widths[i]) for i, col in enumerate(columns))
    separator = "  ".join("-" * w for w in widths)
    lines = [header, separator]
    for row in rows:
        lines.append("  ".join(row[i].ljust(widths[i]) for i in range(len(columns))))
    return "\n".join(lines)


# ---------------------------------------------------------------- Markdown ---

def _md_escape(value):
    """Render one Markdown cell; ``-`` for missing data, no table-breaking chars.

    Pipes and line breaks are neutralized so a value can never split a row or
    inject an extra column; missing values follow the export-markdown rule.
    """
    if value is None or value == "":
        return MD_FIELD_MISSING
    if isinstance(value, (dict, list)):
        value = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return str(value).replace("|", "\\|").replace("\n", " ").replace("\r", " ")


def normalized_row(instance):
    """Map a DCS instance to the fixed ten-column Markdown order."""
    flat = normalize_instance(instance)
    row = []
    for keys in MD_COLUMNS:
        value = _field(flat, *keys, default=None)
        row.append(_md_escape(value))
    return row


def render_markdown(instances):
    """Render the instance list as a GitHub-flavored Markdown table.

    The header row and separator are emitted only when there is at least one
    instance (callers print the empty hint instead and never write a file).
    """
    lines = [
        "| " + " | ".join(MD_HEADERS) + " |",
        "| " + " | ".join(["---"] * len(MD_HEADERS)) + " |",
    ]
    for instance in instances:
        lines.append("| " + " | ".join(normalized_row(instance)) + " |")
    return "\n".join(lines)


class OutputError(DcsListError):
    """The Markdown output file could not be written."""


def write_markdown_file(text, output_path):
    """Write ``text`` to ``output_path`` atomically; returns the absolute path.

    A temp file inside the destination directory is fsynced and renamed over
    the target, so an interrupted/failed write never leaves a partial file.
    """
    if not output_path:
        raise OutputError("--md-output 需要非空的文件路径。")
    path = os.path.abspath(output_path)
    out_dir = os.path.dirname(path) or "."
    tmp_path = None
    try:
        if out_dir and not os.path.isdir(out_dir):
            os.makedirs(out_dir, exist_ok=True)
        fd, tmp_path = tempfile.mkstemp(
            prefix=".dcs_list_md.", suffix=".tmp", dir=out_dir)
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(text)
            if not text.endswith("\n"):
                handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp_path, path)
        tmp_path = None
    except OSError as exc:
        raise OutputError(
            "Markdown 文件写入失败（%s）：%s。未留下残缺文件。" % (path, exc)
        )
    finally:
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except OSError:
                pass
    return path


# ------------------------------------------------------- mode / empty hint ---

def resolve_mode(fmt=None, as_json=False, as_table=False, names_only=False,
                 as_md=False):
    """Resolve the effective output mode, keeping the legacy precedence.

    Backwards compatible order: ``--json`` > ``--names-only`` (default) >
    ``--table`` > ``--md`` > ``--format`` value > default names list.
    """
    if as_json:
        return MODE_JSON
    if names_only:
        return MODE_NAMES
    if as_table:
        return MODE_TABLE
    if as_md:
        return MODE_MD
    if fmt:
        return fmt
    return DEFAULT_MODE


def _empty_hint(region, args):
    """Build the shared 「无 DCS 实例」 hint (identical text for all modes)."""
    filters = []
    if args.name:
        filters.append("name=%s" % args.name)
    if args.instance_id:
        filters.append("instance_id=%s" % args.instance_id)
    if args.ip:
        filters.append("ip=%s" % args.ip)
    if args.status:
        filters.append("status=%s" % args.status)
    if args.tags:
        filters.append("tags=%s" % args.tags)
    suffix = "（过滤条件: %s）" % ", ".join(filters) if filters else ""
    return "当前区域（%s）无 DCS 实例%s。" % (region, suffix)


# The local Markdown output path is not a DCS operation — it is stripped from
# the write-intent scan so a path such as ``.../dcs-backup.md`` never trips it.
_MD_OUTPUT_FLAGS = ("--md-output", "--md_output")
# --sort-by values are ordering choices, not DCS operations. The value
# ``created`` contains the substring ``create``, so the value must be skipped
# (the argument itself is still validated against SORT_CHOICES in main()).
_SORT_BY_FLAGS = ("--sort-by", "--sort_by")


def guard_argv(argv):
    """Scan user argv for write intent, ignoring --md-output/--sort-by values."""
    tokens = []
    skip_next = False
    for token in argv:
        if skip_next:
            skip_next = False
            continue
        name = str(token)
        if name in _MD_OUTPUT_FLAGS or name in _SORT_BY_FLAGS:
            skip_next = True
            continue
        if (name.startswith("--md-output=") or name.startswith("--md_output=")
                or name.startswith("--sort-by=") or name.startswith("--sort_by=")):
            continue
        tokens.append(name)
    return guard_write_intent(" ".join(tokens))


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="查询华为云 DCS（分布式缓存服务）实例列表"
                    "（KooCLI hcloud DCS ListInstances，只读）。")
    parser.add_argument("-r", "--region", default=DEFAULT_REGION,
                        help="目标 Region（默认 %s）" % DEFAULT_REGION)
    parser.add_argument("--names-only", action="store_true", dest="names_only",
                        help="仅输出实例名称清单（默认即名称清单模式）")
    parser.add_argument("--json", action="store_true", dest="as_json",
                        help="以 JSON 输出完整原始字段")
    parser.add_argument("--table", action="store_true", dest="as_table",
                        help="输出全字段表格（名称/ID/引擎/容量/状态/连接地址/端口等）")
    parser.add_argument("--md", action="store_true", dest="as_md",
                        help="输出 Markdown 表格（固定 10 列，与 dcs-export-markdown 口径一致）")
    parser.add_argument("--format", dest="fmt", choices=MODE_CHOICES,
                        default=None,
                        help="输出格式：names（默认）/ table / json / md")
    parser.add_argument("--md-output", dest="md_output", default=None,
                        help="md 模式可选：把表格原子写入该 .md 文件（内容与 stdout 一致）")
    parser.add_argument("--name",
                        help="按实例名称过滤（服务端查询参数，模糊匹配；"
                             "name_equal 精确匹配开关由 --name-equal 提供）")
    parser.add_argument("--name-equal", action="store_true", dest="name_equal",
                        help="按实例名称精确匹配（转发服务端 name_equal=true）")
    parser.add_argument("--instance-id", dest="instance_id",
                        help="按实例 ID 过滤（服务端查询参数）")
    parser.add_argument("--ip",
                        help="按连接 IP 地址过滤（服务端查询参数）")
    parser.add_argument("--status",
                        help="按实例状态过滤（服务端查询参数，如 RUNNING/ERROR）")
    parser.add_argument("--tags",
                        help="按标签过滤（服务端查询参数，格式 key1=value1,key2=value2）")
    parser.add_argument("--sort-by", dest="sort_by", default=None,
                        help="按 name（实例名，大小写不敏感升序）或 created"
                             "（创建时间升序）排序；不传保持接口返回顺序")
    parser.add_argument("--page-size", type=int, default=DEFAULT_PAGE_SIZE,
                        dest="page_size",
                        help="分页大小（默认 %d，范围 1~1000，自动翻页取全量）" % DEFAULT_PAGE_SIZE)
    parser.add_argument("--project-id", dest="project_id",
                        help="项目 ID（可选；SDK 回退在 /v2/{project_id}/instances 路径中需要）")
    parser.add_argument("--operation", default=ALLOWED_OPERATION,
                        help="hcloud DCS 操作名（仅允许只读 %s）" % ALLOWED_OPERATION)
    args = parser.parse_args(argv)

    try:
        # Write-intent guard: scan the raw argv + validate the operation name.
        # The local --md-output path is excluded (it is not a DCS operation).
        guard_argv(argv if argv is not None else sys.argv[1:])
        guard_operation(args.operation)
        for value in (args.name, args.instance_id, args.ip, args.status, args.tags):
            if value:
                guard_write_intent(value)
        if args.page_size is not None:
            if args.page_size < 1 or args.page_size > 1000:
                raise ApiError("--page-size 超出范围（1~1000）：%d" % args.page_size)
        if args.sort_by is not None and args.sort_by not in SORT_CHOICES:
            raise ApiError(
                "--sort-by 取值非法：%r。仅支持 %s（按实例名升序）或 %s"
                "（按创建时间升序）。" % (args.sort_by, SORT_NAME, SORT_CREATED))
        mode = resolve_mode(args.fmt, as_json=args.as_json,
                            as_table=args.as_table, names_only=args.names_only,
                            as_md=args.as_md)
        if args.md_output and mode != MODE_MD:
            raise ApiError(
                "--md-output 仅在 Markdown 模式（--md / --format md）下可用，"
                "当前输出模式为 %s。" % mode)
        instances = list_instances(
            args.region,
            name=args.name if not args.name_equal else None,
            instance_id=args.instance_id,
            ip=args.ip,
            status=args.status,
            tags=args.tags if not args.name_equal else None,
            limit=args.page_size,
            project_id=args.project_id,
        )
    except DcsListError as exc:
        print("[错误] %s" % exc, file=sys.stderr)
        return 1

    # --name-equal: exact name matching (server name param is fuzzy by default).
    if args.name_equal:
        if args.name:
            wanted = str(args.name).strip().lower()
            instances = [
                i for i in instances
                if str(i.get("name", "")).strip().lower() == wanted
            ]
        else:
            instances = []

    # --sort-by: order the full paged + filtered result before every output
    # branch (including the early --json return), so names/table/md/json agree.
    instances = sort_instances(instances, args.sort_by)

    if mode == MODE_JSON:
        print(json.dumps(instances, ensure_ascii=False, indent=2))
        return 0

    if not instances:
        print(_empty_hint(args.region, args))
        return 0

    if mode == MODE_NAMES:
        print("Region %s 的 DCS 实例名称列表（共 %d 个）：" % (args.region, len(instances)))
        for name in instance_names(instances):
            print("- %s" % name)
        return 0

    if mode == MODE_MD:
        text = render_markdown(instances)
        print(text)
        if args.md_output:
            try:
                written = write_markdown_file(text, args.md_output)
            except DcsListError as exc:
                print("[错误] %s" % exc, file=sys.stderr)
                return 1
            print("[已写入] %s" % written, file=sys.stderr)
        return 0

    print("Region %s 的 DCS 实例列表（共 %d 个，完整字段）：" % (args.region, len(instances)))
    print(render_table(instances))
    return 0


if __name__ == "__main__":
    sys.exit(main())
