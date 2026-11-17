#!/usr/bin/env python3
"""List Huawei Cloud Elastic IP (EIP) instances via KooCLI `hcloud EIP ListPublicips`.

Primary execution path is KooCLI (`hcloud EIP ListPublicips`, read-only
GET /v3/{project_id}/eip/publicips); when hcloud is not installed the script
falls back to the official `huaweicloudsdkeip` v3 SDK
(`EipClient.list_publicips`). Reads nothing but the active credential profile /
environment. Supports four output modes (table / --json / --names-only /
Markdown export), --id / --status / --public-ip filters (all real server-side
query parameters), marker-based paging, and a strict write-intent guard: any
argument that looks like a mutating EIP operation is rejected before a single
command is executed.

Usage:
    python3 scripts/list_eip.py [--region cn-north-4] [--json | --names-only]
                                [--markdown] [-o/--output <path.md>]
                                [--id eip-0001] [--status ACTIVE]
                                [--public-ip 1.2.3.4] [--page-size 100]
                                [--project-id <id>] [--operation ListPublicips]

Environment overrides (mostly for tests):
    EIP_LIST_HCLOUD_BIN   hcloud executable (default "hcloud")
    EIP_LIST_HCLOUD_ARGS  extra args injected before the EIP operation
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone

DEFAULT_REGION = "cn-north-4"
DEFAULT_PAGE_SIZE = 100
SERVICE = "EIP"
ALLOWED_OPERATION = "ListPublicips"
REST_PATH = "/v3/{project_id}/eip/publicips"

# Markdown export defaults (naming aligned with the VPC/RDS export skills).
DEFAULT_FILENAME_PREFIX = "eip_list"
MD_TITLE = "华为云 EIP 列表"
MD_COLUMNS = (
    ("公网IP", ("public_ip_address", "public_ipv6_address")),
    ("EIP ID", ("id",)),
    ("别名", ("alias",)),
    ("状态", ("status",)),
    ("类型", ("type",)),
    ("绑定实例类型", ("associate_instance_type",)),
    ("绑定实例 ID", ("associate_instance_id",)),
    ("带宽名称", ("bandwidth_name",)),
    ("带宽大小", ("bandwidth_size",)),
    ("计费方式", ("bandwidth_charge_mode",)),
    ("企业项目 ID", ("enterprise_project_id",)),
    ("创建时间", ("created_at",)),
)

# Local-output flags whose *values* are pure file paths (e.g. a report named
# "eip-release-report.md"). Their values are not cloud-operation intents and
# must not be scanned by the write-intent guard.
_VALUE_STRIPPED_FLAGS = ("--output", "-o")

# Mutating EIP operations / intents — strictly rejected by the guard.
WRITE_INTENT_KEYWORDS = (
    "createpublicip",
    "batchcreatepublicips",
    "deletepublicip",
    "batchdeletepublicips",
    "updatepublicip",
    "associatepublicips",
    "disassociatepublicips",
    "createpublicipbandwidth",
    "changepublicipbandwidth",
    "sharebandwidth",
    "updatebandwidth",
    "create",
    "delete",
    "update",
    "modify",
    "associate",
    "disassociate",
    "dissociate",
    "attach",
    "detach",
    "bind",
    "unbind",
    "release",
    "remove",
    "destroy",
    "change",
    "restart",
    "creating",
    "deleting",
    "updating",
    "associating",
    "disassociating",
    "stop",
    "start",
)

# Preferred column order for the table view; remaining keys are appended sorted.
PREFERRED_COLUMNS = [
    "id",
    "alias",
    "public_ip_address",
    "public_ipv6_address",
    "status",
    "type",
    "ip_version",
    "bandwidth_name",
    "bandwidth_size",
    "bandwidth_share_type",
    "bandwidth_charge_mode",
    "associate_instance_type",
    "associate_instance_id",
    "vnic_private_ip_address",
    "vnic_device_id",
    "vnic_vpc_id",
    "publicip_pool_name",
    "enterprise_project_id",
    "lock_status",
    "description",
    "created_at",
    "updated_at",
]

_PUBLICIP_LIST_KEYS = ("publicips", "public_ips", "publicIps")

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


class EipListError(Exception):
    """Base error for the EIP list skill."""


class GuardError(EipListError):
    """A write intent was detected and blocked (skill is read-only)."""


class ConfigError(EipListError):
    """hcloud missing or credentials (AK/SK) not configured."""


class AuthError(EipListError):
    """Authentication/authorization failure (invalid AK/SK or IAM 403)."""


class ApiError(EipListError):
    """hcloud / network / unexpected API failure."""


class ExportError(EipListError):
    """The local Markdown file could not be created or written."""


def guard_text_from_argv(argv):
    """Build the text the write-intent guard should scan.

    Flag names and positional tokens are scanned; only the values of the local
    output flags (``--output`` / ``-o``) are stripped, because they are file
    paths that may legitimately contain write-looking words (e.g.
    ``eip-release-report.md``). A following flag is never swallowed: a token
    starting with ``-`` is still scanned.
    """
    tokens = list(argv if argv is not None else sys.argv[1:])
    kept = []
    skip_next = False
    for tok in tokens:
        if tok in _VALUE_STRIPPED_FLAGS:
            skip_next = True
            continue
        if tok.startswith("-") and "=" in tok and tok.split("=", 1)[0] in _VALUE_STRIPPED_FLAGS:
            continue
        if skip_next:
            skip_next = False
            if not tok.startswith("-"):
                continue
        kept.append(tok)
    return " ".join(kept)


def guard_write_intent(text):
    """Raise GuardError if `text` carries a mutating intent.

    Normalizes separators so `--create-eip`, `CreatePublicip`,
    and `create_publicip` all hit the same keyword. Read-only vocabulary
    (list/show/get/describe) never matches.
    """
    low = re.sub(r"[\s_\-]+", "", str(text).lower())
    for keyword in WRITE_INTENT_KEYWORDS:
        if keyword in low:
            raise GuardError(
                "检测到写操作意图（关键词: %s）。本 skill 仅支持只读查询"
                "（EIP ListPublicips），创建/删除/更新/绑定/解绑的变更操作已被守卫拦截。" % keyword
            )
    return False


def guard_operation(operation):
    """Only the read-only ListPublicips operation may be executed."""
    if operation != ALLOWED_OPERATION:
        raise GuardError(
            "不允许的操作 %r：本 skill 仅允许只读操作 %s。"
            % (operation, ALLOWED_OPERATION)
        )
    return True


def build_command(region, eip_id=None, status=None, public_ip=None,
                  limit=DEFAULT_PAGE_SIZE, marker=None):
    """Build the hcloud EIP ListPublicips argv (without the executable).

    Mirrors the real KooCLI parameter list for the read-only EIP ListPublicips
    operation: --cli-region / --limit / --marker and the real server-side
    filters --id / --status / --public_ip_address. EIP pages with
    `limit` + `marker` (the next_marker comes from the response page_info).

    `--id` / `--status` / `--public_ip_address` are **array** parameters in
    KooCLI (`array<string>`, format `--xxx.1=value1 ...`). Passing them as
    scalars makes KooCLI 7.x reject the request with
    `[USE_ERROR]Invalid parameter: ...`, so they must always use the `.1`
    array index.
    """
    argv = [
        SERVICE,
        ALLOWED_OPERATION,
        "--cli-region=%s" % region,
        "--limit=%d" % limit,
    ]
    if marker:
        argv.append("--marker=%s" % marker)
    if eip_id:
        argv.append("--id.1=%s" % eip_id)
    if status:
        argv.append("--status.1=%s" % status)
    if public_ip:
        argv.append("--public_ip_address.1=%s" % public_ip)
    return argv


def _hcloud_executable():
    return os.environ.get("EIP_LIST_HCLOUD_BIN", "hcloud")


def run_hcloud(argv):
    """Execute hcloud and return (stdout, stderr, returncode)."""
    cmd = [_hcloud_executable()]
    extra = os.environ.get("EIP_LIST_HCLOUD_ARGS", "").split()
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
            "hcloud 参数错误（KooCLI 拒绝了该参数组合，退出码 %s）：EIP ListPublicips "
            "真实参数清单可通过 `hcloud EIP ListPublicips --help` 查看。"
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
            "无权限访问弹性公网IP（EIP），请检查 IAM 权限（403：AK/SK 无效或未授予 EIP 只读权限），"
            "参见 references/iam-policies.md。详情：%s" % blob[:300]
        )
    return ApiError(
        "hcloud 调用失败（退出码 %s）：%s" % (returncode, blob[:300])
    )


def extract_publicips(payload):
    """Pull the EIP list out of a ListPublicips response."""
    if isinstance(payload, list):
        return payload
    for key in _PUBLICIP_LIST_KEYS:
        value = payload.get(key)
        if isinstance(value, list):
            return value
    return []


def _next_marker(payload):
    """Read the next_marker from a ListPublicips response page_info."""
    if not isinstance(payload, dict):
        return None
    page_info = payload.get("page_info") or payload.get("pageInfo")
    if isinstance(page_info, dict):
        marker = page_info.get("next_marker") or page_info.get("nextMarker")
        if marker:
            return str(marker)
    return None


def _jsonable(value):
    """Recursively convert datetimes (SDK to_dict output) to JSON-safe values."""
    return json.loads(json.dumps(value, ensure_ascii=False, default=str))


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


def list_publicips_via_sdk(region, eip_id=None, status=None, public_ip=None,
                           limit=DEFAULT_PAGE_SIZE, project_id=None,
                           max_pages=100):
    """SDK fallback: query EIPs through `huaweicloudsdkeip` v3.

    Only invoked when hcloud is not installed. Credentials are taken from the
    whitelisted AK/SK environment variables (HW_*/HUAWEI_ACCESS_KEY family) —
    never passed as literals here. The official SDK has no env-var
    auto-discovery on `BasicCredentials()`, so AK/SK (and the project id
    required by the `/v3/{project_id}/...` path) must be read explicitly.
    Region resolution uses the SDK's own `EipRegion` catalog (official
    endpoints, no guessing), falling back to an explicit `Region(id,
    endpoint)` for custom regions.
    `ListPublicipsRequest` accepts `id` / `status` / `public_ip_address` as
    list values; paging uses `limit` + `marker`.
    """
    try:
        from huaweicloudsdkcore.auth.credentials import BasicCredentials
        from huaweicloudsdkcore.region.region import Region
        from huaweicloudsdkcore.http.http_config import HttpConfig
        from huaweicloudsdkeip.v3 import EipClient, ListPublicipsRequest
        from huaweicloudsdkeip.v3.region.eip_region import EipRegion
    except ImportError as exc:
        raise ConfigError(
            "未找到 hcloud（KooCLI），且 huaweicloudsdkcore/huaweicloudsdkeip 未安装，"
            "无法回退到 SDK。请安装 KooCLI 或 pip install huaweicloudsdkcore "
            "huaweicloudsdkeip。详情：%s" % exc
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
            "SDK 回退缺少 project_id：EIP 的 REST 路径为 %s，需要项目 ID。"
            "请通过 --project-id 传入，或设置 HUAWEICLOUD_SDK_PROJECT_ID / "
            "HUAWEI_PROJECT_ID（严禁在对话中粘贴敏感信息）。" % REST_PATH
        )
    credentials = BasicCredentials(ak=ak, sk=sk, project_id=resolved_project_id)  # env-sourced, never literals
    try:
        try:
            region_obj = EipRegion.value_of(region)
        except (ValueError, KeyError, AttributeError):
            region_obj = Region(region, "https://vpc.%s.myhuaweicloud.com" % region)
        client = EipClient.new_builder() \
            .with_credentials(credentials) \
            .with_region(region_obj) \
            .with_http_config(HttpConfig.get_default_config()) \
            .build()
    except Exception as exc:  # region unknown / config broken
        raise ConfigError(
            "SDK 初始化失败（region=%s）：%s。请检查 huaweicloudsdkeip 安装与区域配置。"
            % (region, exc)
        )
    publicips = []
    marker = None
    for _ in range(max_pages):
        request = ListPublicipsRequest(
            limit=limit,
            marker=marker,
            id=[eip_id] if eip_id else None,
            status=[status] if status else None,
            public_ip_address=[public_ip] if public_ip else None,
        )
        try:
            response = client.list_publicips(request)
        except Exception as exc:
            low = str(exc).lower()
            if any(p in low for p in _AUTH_PATTERNS):
                raise AuthError(
                    "无权限访问弹性公网IP（EIP），请检查 IAM 权限（403）。详情：%s"
                    % str(exc)[:300]
                )
            raise ApiError("SDK 调用失败：%s" % str(exc)[:300])
        batch = list(response.publicips or [])
        publicips.extend(_jsonable(publicip.to_dict()) for publicip in batch)
        page_info = getattr(response, "page_info", None)
        next_marker = getattr(page_info, "next_marker", None) if page_info else None
        if not next_marker or not batch:
            break
        marker = str(next_marker)
    else:
        raise ApiError("翻页超过 %d 页仍未取完，已中止以防死循环。" % max_pages)
    return publicips


def list_publicips(region, status=None, eip_id=None, public_ip=None,
                   limit=DEFAULT_PAGE_SIZE, project_id=None, max_pages=100):
    """Query all EIPs (marker-paged); KooCLI first, SDK fallback."""
    publicips = []
    marker = None
    for _page in range(max_pages):
        argv = build_command(region, eip_id=eip_id, status=status,
                             public_ip=public_ip, limit=limit, marker=marker)
        try:
            stdout, stderr, returncode = run_hcloud(argv)
        except ConfigError:
            # hcloud binary missing → one-shot SDK fallback (no CLI retry).
            publicips = list_publicips_via_sdk(
                region, eip_id=eip_id, status=status, public_ip=public_ip,
                limit=limit, project_id=project_id, max_pages=max_pages,
            )
            break
        if returncode != 0 or _USE_ERROR_MARKER in (stdout + " " + stderr).lower():
            # KooCLI usage errors print [USE_ERROR] on stdout with rc=0.
            raise classify_hcloud_failure(stdout, stderr, returncode)
        payload = extract_json(stdout)
        batch = extract_publicips(payload)
        publicips.extend(batch)
        marker = _next_marker(payload)
        if not marker or not batch or len(batch) < limit:
            break
    else:
        raise ApiError("翻页超过 %d 页仍未取完，已中止以防死循环。" % max_pages)
    return publicips


def normalize_publicip(publicip):
    """Expand the nested `bandwidth` / `vnic` objects into flat table columns."""
    flat = dict(publicip)
    bandwidth = publicip.get("bandwidth")
    if isinstance(bandwidth, dict):
        flat["bandwidth_name"] = bandwidth.get("name", "-")
        flat["bandwidth_size"] = bandwidth.get("size", "-")
        flat["bandwidth_share_type"] = bandwidth.get("share_type", "-")
        flat["bandwidth_charge_mode"] = bandwidth.get("charge_mode", "-")
        flat.pop("bandwidth", None)
    vnic = publicip.get("vnic")
    if isinstance(vnic, dict):
        flat["vnic_private_ip_address"] = vnic.get("private_ip_address", "-")
        flat["vnic_device_id"] = vnic.get("device_id", "-")
        flat["vnic_vpc_id"] = vnic.get("vpc_id", "-")
        flat["vnic_port_id"] = vnic.get("port_id", "-")
        flat.pop("vnic", None)
    return flat


def _field(publicip, *names, default="-"):
    for name in names:
        if name in publicip and publicip[name] not in (None, ""):
            return publicip[name]
    return default


def publicip_names(publicips):
    names = []
    for publicip in publicips:
        name = _field(publicip, "alias", "public_ip_address", default=None)
        if name is None:
            name = _field(publicip, "id")
        names.append(str(name))
    return names


def _cell(value):
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return str(value)


def render_table(publicips):
    """Render full-field table output (union of all returned fields)."""
    rows_data = [normalize_publicip(publicip) for publicip in publicips]
    columns = []
    for key in PREFERRED_COLUMNS:
        if any(key in c for c in rows_data):
            columns.append(key)
    for key in sorted({k for c in rows_data for k in c}):
        if key not in columns:
            columns.append(key)
    if not columns:
        columns = ["id", "public_ip_address"]
    rows = [[_cell(_field(c, col)) for col in columns] for c in rows_data]
    widths = [max(len(col), *(len(row[i]) for row in rows)) for i, col in enumerate(columns)]
    header = "  ".join(col.ljust(widths[i]) for i, col in enumerate(columns))
    separator = "  ".join("-" * w for w in widths)
    lines = [header, separator]
    for row in rows:
        lines.append("  ".join(row[i].ljust(widths[i]) for i in range(len(columns))))
    return "\n".join(lines)


def _md_cell(value):
    """Render one Markdown table cell; pipes/newlines are escaped, ``-`` is the fallback."""
    if value is None or value == "":
        return "-"
    if isinstance(value, (dict, list)):
        value = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    text = str(value).replace("\r\n", " ").replace("\n", " ")
    text = text.replace("\r", " ").replace("|", "\\|")
    return text or "-"


def _generated_at():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def active_filter_descriptions(status=None, eip_id=None, public_ip=None):
    """Human-readable description of the server-side filters actually applied."""
    filters = []
    if status:
        filters.append("status=%s" % status)
    if eip_id:
        filters.append("id=%s" % eip_id)
    if public_ip:
        filters.append("public_ip=%s" % public_ip)
    return filters


def render_markdown(publicips, region=None, generated_at=None,
                    filters=None):
    """Render the EIP list as a Markdown document (title + metadata + table).

    The table always carries the full fixed header set, so downstream readers
    get a stable schema. An empty list still renders a valid document with an
    explicit 「无数据」 note — never a corrupt or missing report.
    """
    publicips = list(publicips)
    rows_data = [normalize_publicip(publicip) for publicip in publicips]
    generated_at = generated_at or _generated_at()
    region_label = region or "-"

    lines = [
        "# %s" % MD_TITLE,
        "",
        "> 查询区域：%s | 生成时间：%s | 记录数：%d"
        % (region_label, generated_at, len(rows_data)),
    ]
    if filters:
        lines.append("> 过滤条件：%s" % ", ".join(filters))
    lines += ["", "| " + " | ".join(label for label, _ in MD_COLUMNS) + " |",
              "| " + " | ".join(["---"] * len(MD_COLUMNS)) + " |"]
    for publicip in rows_data:
        cells = [_md_cell(_field(publicip, *keys)) for _, keys in MD_COLUMNS]
        lines.append("| " + " | ".join(cells) + " |")
    if not rows_data:
        lines += ["", "当前区域（%s）无弹性公网IP（EIP）数据，无数据。" % region_label]
    lines.append("")
    return "\n".join(lines)


def default_output_path(region):
    """Default .md filename: eip_list_<region>_<timestamp>.md"""
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return "%s_%s_%s.md" % (DEFAULT_FILENAME_PREFIX, region, stamp)


def export_markdown(publicips, output_path, region=None, generated_at=None,
                    filters=None):
    """Write the EIP list as a Markdown report at ``output_path``.

    Missing parent directories are created; the file is staged through a temp
    file in the same directory and atomically renamed, so an interrupted write
    never leaves a partial/corrupt report behind.

    Returns the absolute path of the written file.
    Raises ExportError when the directory/file cannot be created or written.
    """
    publicips = list(publicips)
    output_path = os.path.abspath(output_path)
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.isdir(output_dir):
        try:
            os.makedirs(output_dir, exist_ok=True)
        except OSError as exc:
            raise ExportError(
                "无法创建输出目录 %r：%s。请检查 --output 路径。"
                % (output_dir, exc)
            )

    text = render_markdown(publicips, region=region,
                          generated_at=generated_at, filters=filters)

    try:
        fd, tmp_path = tempfile.mkstemp(
            prefix=".%s." % DEFAULT_FILENAME_PREFIX, suffix=".tmp",
            dir=output_dir or ".")
        os.close(fd)
    except (OSError, ValueError) as exc:
        raise ExportError("Markdown 临时文件创建失败：%s（%s）"
                          % (output_path, exc))
    try:
        with open(tmp_path, "w", encoding="utf-8") as handle:
            handle.write(text + "\n")
        shutil.move(tmp_path, output_path)
    except Exception as exc:
        if os.path.exists(tmp_path):
            try:
                os.unlink(tmp_path)
            except OSError:
                pass
        raise ExportError("Markdown 文件写出失败：%s（%s）"
                          % (output_path, exc))
    return output_path


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="查询华为云弹性公网IP（EIP）列表（KooCLI hcloud EIP ListPublicips，只读）。")
    parser.add_argument("-r", "--region", default=DEFAULT_REGION,
                        help="目标 Region（默认 %s）" % DEFAULT_REGION)
    parser.add_argument("--json", action="store_true", dest="as_json",
                        help="以 JSON 输出完整原始字段")
    parser.add_argument("--names-only", action="store_true", dest="names_only",
                        help="仅输出 EIP 名称 / 公网IP 清单")
    parser.add_argument("--markdown", action="store_true", dest="markdown",
                        help="导出 Markdown 报表（默认文件名 %s_<region>_<timestamp>.md）"
                             % DEFAULT_FILENAME_PREFIX)
    parser.add_argument("-o", "--output", dest="output", default=None,
                        help="Markdown 输出路径（隐含 --markdown；缺省为 "
                             "%s_<region>_<timestamp>.md）" % DEFAULT_FILENAME_PREFIX)
    parser.add_argument("--id", dest="eip_id",
                        help="按 EIP ID 过滤（服务端查询参数）")
    parser.add_argument("--status", help="按 EIP 状态过滤（如 ACTIVE / DOWN / ERROR，服务端查询参数）")
    parser.add_argument("--public-ip", dest="public_ip",
                        help="按公网 IP 地址过滤（服务端查询参数）")
    parser.add_argument("--page-size", type=int, default=DEFAULT_PAGE_SIZE,
                        dest="page_size", help="分页大小（默认 %d，范围 0~2000）" % DEFAULT_PAGE_SIZE)
    parser.add_argument("--project-id", dest="project_id",
                        help="项目 ID（可选；SDK 回退在 /v3/{project_id}/eip/publicips 路径中需要）")
    parser.add_argument("--operation", default=ALLOWED_OPERATION,
                        help="hcloud EIP 操作名（仅允许只读 %s）" % ALLOWED_OPERATION)
    args = parser.parse_args(argv)

    try:
        # Write-intent guard: scan the raw argv (local output paths excluded)
        # + validate the operation name.
        guard_write_intent(guard_text_from_argv(argv))
        guard_operation(args.operation)
        if args.eip_id:
            guard_write_intent(args.eip_id)
        if args.status:
            guard_write_intent(args.status)
        publicips = list_publicips(
            args.region,
            status=args.status,
            eip_id=args.eip_id,
            public_ip=args.public_ip,
            limit=args.page_size,
            project_id=args.project_id,
        )
    except EipListError as exc:
        print("[错误] %s" % exc, file=sys.stderr)
        return 1

    # Markdown export takes precedence over --json / --names-only.
    if args.markdown or args.output:
        output_path = args.output or default_output_path(args.region)
        filters = active_filter_descriptions(
            status=args.status, eip_id=args.eip_id, public_ip=args.public_ip)
        try:
            written = export_markdown(publicips, output_path, region=args.region,
                                      filters=filters)
        except EipListError as exc:
            print("[错误] %s" % exc, file=sys.stderr)
            return 1
        filters_suffix = "（过滤条件: %s）" % ", ".join(filters) if filters else ""
        if publicips:
            print("已生成 EIP 列表 Markdown 报表（Region %s，共 %d 条记录）：%s"
                  % (args.region, len(publicips), written))
        else:
            print("当前区域（%s）无弹性公网IP（EIP）数据%s，已生成 Markdown 文件"
                  "（标注「无数据」，共 0 条）：%s"
                  % (args.region, filters_suffix, written))
        return 0

    if args.as_json:
        print(json.dumps(publicips, ensure_ascii=False, indent=2))
        return 0

    if args.names_only:
        print("Region %s 的弹性公网IP（EIP）名称列表（共 %d 个）：" % (args.region, len(publicips)))
        for name in publicip_names(publicips):
            print("- %s" % name)
        return 0

    if not publicips:
        filters = []
        if args.status:
            filters.append("status=%s" % args.status)
        if args.eip_id:
            filters.append("id=%s" % args.eip_id)
        if args.public_ip:
            filters.append("public_ip=%s" % args.public_ip)
        suffix = "（过滤条件: %s）" % ", ".join(filters) if filters else ""
        print("当前区域（%s）无弹性公网IP（EIP）%s。" % (args.region, suffix))
        return 0

    print("Region %s 的弹性公网IP（EIP）列表（共 %d 个，完整字段）：" % (args.region, len(publicips)))
    print(render_table(publicips))
    return 0


if __name__ == "__main__":
    sys.exit(main())