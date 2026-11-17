#!/usr/bin/env python3
"""List Huawei Cloud BMS (Bare Metal Server) instances via KooCLI `hcloud BMS ListBareMetalServers`.

Primary execution path is KooCLI (read-only GET
`/v1/{project_id}/baremetalservers/detail`); when hcloud is not installed the
script falls back to the official `huaweicloudsdkbms` v1 SDK
(`list_bare_metal_servers`). Reads nothing but the active credential profile /
environment. Supports three stdout modes (table / --json / --names-only) plus
an additive Markdown file export (--md-file / --output-md), --name / --status
server-side filters (both are real ListBareMetalServers query parameters) plus
a --server-id client-side filter (the API has no server-id parameter),
page-number offset paging, and a strict write-intent guard: any argument that
looks like a mutating BMS operation (create / delete / update / reboot / rebuild
/ resize / reinstall / reset / attach / detach / change ...) is rejected before
a single command is executed.

Usage:
    python3 scripts/list_bms.py [--region cn-north-4] [--json | --names-only]
                                 [--md-file [PATH]] [--name bms-01]
                                 [--server-id <uuid>] [--status ACTIVE]
                                 [--page-size 100]
                                 [--operation ListBareMetalServers]

Environment overrides (mostly for tests):
    BMS_LIST_HCLOUD_BIN   hcloud executable (default "hcloud")
    BMS_LIST_HCLOUD_ARGS  extra args injected before the BMS operation
"""

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from datetime import datetime

DEFAULT_REGION = "cn-north-4"
DEFAULT_PAGE_SIZE = 100
SERVICE = "BMS"
ALLOWED_OPERATION = "ListBareMetalServers"

# Mutating BMS operations / intents — strictly rejected by the guard.
# Normalized (lower-case, separators stripped) exact-operation names first, then
# the generic mutating verbs that any write argument would carry.
WRITE_INTENT_KEYWORDS = (
    "createbaremetalserver",
    "createbaremetalservers",
    "deletebaremetalserver",
    "deleteservernics",
    "updatebaremetalserver",
    "updatemetadata",
    "updatemetadataoptions",
    "updateserverinterfaceattachments",
    "modifyvmnic",
    "batchrebootbaremetalservers",
    "batchstartbaremetalservers",
    "batchstopbaremetalservers",
    "reinstallbaremetalserveros",
    "resetpwdoneclick",
    "changebaremetalservername",
    "changebaremetalserveros",
    "attachbaremetalservervolume",
    "detachbaremetalservervolume",
    "addservernics",
    "batchcreatebaremetalservertags",
    "batchdeletebaremetalservertags",
    "creating",
    "deleting",
    "updating",
    "rebooting",
    "rebuilding",
    "resizing",
    "reinstalling",
    "resetting",
    "create",
    "delete",
    "update",
    "modify",
    "reboot",
    "rebuild",
    "reinstall",
    "resize",
    "reset",
    "change",
    "attach",
    "detach",
    "stop",
    "start",
    "restore",
    "destroy",
)

# Preferred column order for the table view; remaining keys are appended sorted.
PREFERRED_COLUMNS = [
    "id",
    "name",
    "status",
    "flavor_name",
    "flavor_id",
    "availability_zone",
    "access_i_pv4",
    "access_i_pv6",
    "created",
    "updated",
    "key_name",
    "image_id",
    "enterprise_project_id",
    "os_ext_st_stask_state",
    "os_ext_st_svm_state",
    "tags",
]

# Fixed column subset (key, Chinese header) used by the Markdown inventory
# table. Reuses `normalize_server`'s flattened keys: 名称/ID/状态/规格/可用区/IP.
# Missing values render as `-` through `_md_cell`; a missing name falls back to
# the server ID.
MD_TABLE_COLUMNS = [
    ("name", "名称"),
    ("id", "ID"),
    ("status", "状态"),
    ("flavor_name", "规格"),
    ("availability_zone", "可用区"),
    ("access_i_pv4", "IP"),
]

_SERVER_LIST_KEYS = (
    "servers",
    "baremetal_servers",
    "bare_metal_servers",
    "server_list",
)

# BMS ListBareMetalServers status enumerants — legitimate read-only filters.
# REBOOT / HARD_REBOOT / REBUILD legitimately contain write-looking words, so
# only the value of --status is exempted from the write-intent scan.
_ALLOWED_STATUSES = (
    "ACTIVE",
    "BUILD",
    "ERROR",
    "HARD_REBOOT",
    "REBOOT",
    "REBUILD",
    "SHUTOFF",
)

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
    "does not contain profile",
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


class BmsListError(Exception):
    """Base error for the BMS list skill."""


class GuardError(BmsListError):
    """A write intent was detected and blocked (skill is read-only)."""


class ConfigError(BmsListError):
    """hcloud missing or credentials (AK/SK) not configured."""


class AuthError(BmsListError):
    """Authentication/authorization failure (invalid AK/SK or IAM 403)."""


class ApiError(BmsListError):
    """hcloud / network / unexpected API failure."""


class OutputError(BmsListError):
    """The Markdown report could not be written (bad directory / permission)."""


def guard_write_intent(text):
    """Raise GuardError if `text` carries a mutating intent.

    Normalizes separators so `--create-server`, `CreateBareMetalServers`, and
    `create_server` all hit the same keyword. Read-only vocabulary
    (list/show/get/describe) never matches.
    """
    low = re.sub(r"[\s_\-]+", "", str(text).lower())
    for keyword in WRITE_INTENT_KEYWORDS:
        if keyword in low:
            raise GuardError(
                "检测到写操作意图（关键词: %s）。本 skill 仅支持只读查询"
                "（BMS ListBareMetalServers），创建/删除/重启/重装/扩缩容等变更操作"
                "已被守卫拦截。" % keyword
            )
    return False


def guard_operation(operation):
    """Only the read-only ListBareMetalServers operation may be executed."""
    if operation != ALLOWED_OPERATION:
        raise GuardError(
            "不允许的操作 %r：本 skill 仅允许只读操作 %s。" % (operation, ALLOWED_OPERATION)
        )
    return True


def strip_status_tokens(argv):
    """Drop read-only values before the guard scan.

    Two kinds of argument values are legitimate read / file-system *data* rather
    than cloud operations and must be exempted from the write-intent scan:

    - `--status <value>` — BMS status enumerants (`REBOOT` / `HARD_REBOOT` /
      `REBUILD`) contain write-looking words but are read-only filters.
    - `--md-file <path>` / `--output-md <path>` — the Markdown output path is a
      local file name, so a report such as `bms-delete-report.md` or
      `bms-start-report.md` must not trip the guard.

    The value of `--md-file` / `--output-md` is *optional*, so a token following
    such a flag is stripped only when it is not itself a flag: `--md-file
    --create-server` therefore still exposes the mutating flag to the guard.
    """
    flags = ("--status", "-status", "--md-file", "--output-md")
    kept = []
    skip = False
    for token in argv:
        if skip:
            skip = False
            if not token.startswith("-"):
                continue
        if token in flags:
            skip = True
            continue
        if any(token.startswith(flag + "=") for flag in flags):
            continue
        kept.append(token)
    return kept


def build_command(region, name=None, status=None,
                  limit=DEFAULT_PAGE_SIZE, offset=1):
    """Build the hcloud BMS ListBareMetalServers argv (without the executable).

    Mirrors the real KooCLI parameter list (`hcloud BMS ListBareMetalServers
    --help`): --cli-region / --limit / --offset / --name / --status.
    `offset` is the **page number** (the BMS pagination API starts at page 1),
    not a record offset. There is NO server-id query parameter, so --server-id
    filtering is applied client-side by `filter_by_server_id()`.
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
    if status:
        argv.append("--status=%s" % status)
    return argv


def _hcloud_executable():
    return os.environ.get("BMS_LIST_HCLOUD_BIN", "hcloud")


def run_hcloud(argv):
    """Execute hcloud and return (stdout, stderr, returncode)."""
    cmd = [_hcloud_executable()]
    extra = os.environ.get("BMS_LIST_HCLOUD_ARGS", "").split()
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
    # Missing profile / credentials is reported by KooCLI as a [USE_ERROR] on
    # stdout, so it must be classified as a credential problem BEFORE the
    # generic usage-error branch.
    if any(p in low for p in _CREDENTIAL_MISSING_PATTERNS) and not re.search(
            r"\b40[13]\b", blob):
        return ConfigError(
            "缺少 AK/SK 凭证：hcloud 未配置有效凭证。请先运行 hcloud configure 或"
            "设置凭证环境变量（严禁在对话中粘贴 AK/SK），参见"
            " references/cli-installation-guide.md。详情：%s" % blob[:300]
        )
    if _USE_ERROR_MARKER in low:
        return ApiError(
            "hcloud 参数错误（KooCLI 拒绝了该参数组合，退出码 %s）：BMS ListBareMetalServers "
            "真实参数清单可通过 `hcloud BMS ListBareMetalServers --help` 查看。"
            "详情：%s" % (returncode, blob[:300])
        )
    if any(p in low for p in _AUTH_PATTERNS):
        return AuthError(
            "无权限访问 BMS，请检查 IAM 权限（403：AK/SK 无效或未授予 BMS 只读权限），"
            "参见 references/iam-policies.md。详情：%s" % blob[:300]
        )
    return ApiError(
        "hcloud 调用失败（退出码 %s）：%s" % (returncode, blob[:300])
    )


def extract_servers(payload):
    """Pull the server list out of a ListBareMetalServers response."""
    if isinstance(payload, list):
        return payload
    for key in _SERVER_LIST_KEYS:
        value = payload.get(key)
        if isinstance(value, list):
            return value
    return []


def _total_count(payload):
    if not isinstance(payload, dict):
        return None
    for key in ("count", "total_count", "totalCount", "total"):
        value = payload.get(key)
        if isinstance(value, int):
            return value
    return None


def _has_more(batch, collected, limit, payload):
    if not batch:
        return False
    total = _total_count(payload)
    if total is not None and total >= 0:
        return collected < total
    return len(batch) >= limit


def filter_by_server_id(servers, server_id):
    """Client-side server-id filter (case-insensitive).

    The real BMS ListBareMetalServers API / KooCLI has no server-id query
    parameter, so filtering by exact instance ID happens here, after the full
    (paged) list has been fetched. An empty result is reported as a normal
    empty list.
    """
    if not server_id:
        return list(servers)
    wanted = str(server_id).strip().lower()
    matched = []
    for server in servers:
        value = server.get("id") if isinstance(server, dict) else None
        if value is not None and str(value).strip().lower() == wanted:
            matched.append(server)
    return matched


def list_servers_via_sdk(region, name=None, status=None,
                         limit=DEFAULT_PAGE_SIZE, max_pages=100):
    """SDK fallback: query servers through `huaweicloudsdkbms` v1.

    Only invoked when hcloud is not installed. Credentials are taken from the
    standard environment variables (HUAWEI_*/HW_*/HWC_* AK/SK markers) — never
    passed as literals here. The official SDK has no env-var auto-discovery on
    `BasicCredentials()`, so AK/SK must be read explicitly. Region resolution
    uses the SDK's own `BmsRegion` catalog (official endpoints, no guessing),
    falling back to an explicit `Region(id, endpoint)` for custom regions.
    `ListBareMetalServersRequest` has no server-id attribute, so server-id
    filtering is NOT done here — the caller applies `filter_by_server_id()`.
    `offset` is the page number (starts at 1), matching the CLI/SDK semantics.
    """
    try:
        from huaweicloudsdkcore.auth.credentials import BasicCredentials
        from huaweicloudsdkcore.region.region import Region
        from huaweicloudsdkcore.http.http_config import HttpConfig
        from huaweicloudsdkbms.v1 import BmsClient, ListBareMetalServersRequest
        from huaweicloudsdkbms.v1.region.bms_region import BmsRegion
    except ImportError as exc:
        raise ConfigError(
            "未找到 hcloud（KooCLI），且 huaweicloudsdkcore/huaweicloudsdkbms 未安装，"
            "无法回退到 SDK。请安装 KooCLI 或 pip install huaweicloudsdkcore "
            "huaweicloudsdkbms。详情：%s" % exc
        )

    def _env_credential(markers):
        for key, value in os.environ.items():
            upper = key.upper()
            if not upper.startswith(("HUAWEI", "HW_", "HWC")):
                continue
            if any(marker in upper for marker in markers) and value:
                return value
        return None

    ak = _env_credential(("ACCESS_KEY", "_AK"))
    sk = _env_credential(("SECRET_KEY", "_SK"))
    if not ak or not sk:
        raise ConfigError(
            "SDK 回退缺少 AK/SK 凭证：官方 SDK 的 BasicCredentials 不会自动读取环境"
            "变量，且当前环境未检测到 HUAWEI_*/HW_*/HWC_* 形式的 AK/SK 环境变量。"
            "请在会话外设置 HUAWEICLOUD_SDK_AK / HUAWEICLOUD_SDK_SK（严禁在对话中粘贴"
            " AK/SK），参见 references/cli-installation-guide.md。"
        )
    credentials = BasicCredentials(ak=ak, sk=sk)  # env-sourced, never literals
    try:
        try:
            region_obj = BmsRegion.value_of(region)
        except (ValueError, KeyError, AttributeError):
            region_obj = Region(region, "https://bms.%s.myhuaweicloud.com" % region)
        client = BmsClient.new_builder() \
            .with_credentials(credentials) \
            .with_region(region_obj) \
            .with_http_config(HttpConfig.get_default_config()) \
            .build()
    except Exception as exc:  # region unknown / config broken
        raise ConfigError(
            "SDK 初始化失败（region=%s）：%s。请检查 huaweicloudsdkbms 安装与区域配置。"
            % (region, exc)
        )
    servers = []
    page = 1
    for _ in range(max_pages):
        request = ListBareMetalServersRequest(
            limit=limit, offset=page, name=name, status=status,
        )
        try:
            response = client.list_bare_metal_servers(request)
        except Exception as exc:
            low = str(exc).lower()
            if any(p in low for p in _AUTH_PATTERNS):
                raise AuthError(
                    "无权限访问 BMS，请检查 IAM 权限（403）。详情：%s" % str(exc)[:300]
                )
            raise ApiError("SDK 调用失败：%s" % str(exc)[:300])
        batch = list(response.servers or [])
        servers.extend(server.to_dict() for server in batch)
        total = getattr(response, "count", None)
        if total is not None and len(servers) >= total:
            break
        if len(batch) < limit:
            break
        page += 1
    else:
        raise ApiError("翻页超过 %d 页仍未取完，已中止以防死循环。" % max_pages)
    return servers


def list_servers(region, status=None, name=None, server_id=None,
                 limit=DEFAULT_PAGE_SIZE, max_pages=100):
    """Query all BMS servers (paged); KooCLI first, SDK fallback.

    `--name` / `--status` are forwarded server-side (real ListBareMetalServers
    query parameters); `--server-id` is applied client-side after the full
    paged list is fetched (the API has no server-id parameter).
    """
    servers = []
    page = 1
    for _page in range(max_pages):
        argv = build_command(region, name=name, status=status,
                             limit=limit, offset=page)
        try:
            stdout, stderr, returncode = run_hcloud(argv)
        except ConfigError:
            # hcloud binary missing → one-shot SDK fallback (no CLI retry).
            servers = list_servers_via_sdk(
                region, name=name, status=status,
                limit=limit, max_pages=max_pages,
            )
            break
        if returncode != 0 or _USE_ERROR_MARKER in (stdout + " " + stderr).lower():
            # KooCLI usage errors print [USE_ERROR] on stdout with rc=0.
            raise classify_hcloud_failure(stdout, stderr, returncode)
        payload = extract_json(stdout)
        batch = extract_servers(payload)
        servers.extend(batch)
        if not _has_more(batch, len(servers), limit, payload):
            break
        page += 1
    else:
        raise ApiError("翻页超过 %d 页仍未取完，已中止以防死循环。" % max_pages)
    return filter_by_server_id(servers, server_id)


def normalize_server(server):
    """Flatten nested flavor / image / availability-zone fields for the table."""
    flat = dict(server)
    flavor = server.get("flavor") or {}
    if isinstance(flavor, dict):
        flat.setdefault("flavor_id", flavor.get("id", "-"))
        flat.setdefault("flavor_name", flavor.get("name", "-"))
    else:
        flat.setdefault("flavor_id", "-")
        flat.setdefault("flavor_name", "-")
    if "availability_zone" not in flat:
        flat["availability_zone"] = server.get("os_ext_a_zavailability_zone", "-")
    image = server.get("image") or {}
    if isinstance(image, dict):
        flat.setdefault("image_id", image.get("id", "-"))
    else:
        flat.setdefault("image_id", "-")
    return flat


def _field(server, *names, default="-"):
    for name in names:
        if name in server and server[name] not in (None, ""):
            return server[name]
    return default


def server_names(servers):
    names = []
    for server in servers:
        name = _field(server, "name", "server_name", default=None)
        if name is None:
            name = _field(server, "id", "server_id")
        names.append(str(name))
    return names


def active_filter_descriptions(status=None, name=None, server_id=None):
    """Human-readable description of the filters actually applied.

    `--status` / `--name` are server-side ListBareMetalServers parameters;
    `--server-id` is applied client-side by `filter_by_server_id()`.
    """
    filters = []
    if status:
        filters.append("status=%s" % status)
    if name:
        filters.append("name=%s" % name)
    if server_id:
        filters.append("server_id=%s" % server_id)
    return filters


def _as_datetime(value):
    """Return `value` as a datetime, defaulting to the current local time."""
    if isinstance(value, datetime):
        return value
    return datetime.now().astimezone()


def format_query_time(value=None):
    """Format the query timestamp for the Markdown header (local time + zone)."""
    moment = _as_datetime(value)
    if moment.tzinfo is not None:
        return moment.strftime("%Y-%m-%d %H:%M:%S %Z")
    return moment.strftime("%Y-%m-%d %H:%M:%S")


def default_markdown_name(region, generated_at=None):
    """Default report file name: `bms-list-<region>-<YYYYMMDD>.md`."""
    stamp = _as_datetime(generated_at).strftime("%Y%m%d")
    return "bms-list-%s-%s.md" % (region, stamp)


def _md_cell(value):
    """Escape a value for a Markdown table cell (pipes / newlines / blanks)."""
    text = "" if value is None else str(value)
    text = text.replace("\\", "\\\\").replace("|", "\\|")
    text = re.sub(r"\s*\n\s*", " ", text).strip()
    return text or "-"


def render_markdown(region, servers, generated_at=None, filters=None):
    """Render the BMS inventory as a Markdown report.

    Contains the queried region, the query timestamp, the server total and a
    fixed inventory table (see `MD_TABLE_COLUMNS`: 名称 / ID / 状态 / 规格 /
    可用区 / IP). Values are read through `normalize_server`, so nested `flavor`
    / availability-zone fields are flattened; missing values render as `-` and a
    missing name falls back to the server ID. Cells are escaped by `_md_cell`.
    An empty result renders `共 0 个裸金属服务器` instead of an empty table; the
    filters actually applied are always listed when present.
    """
    filters = list(filters or [])
    servers = list(servers or [])
    lines = [
        "# Huawei Cloud BMS 裸金属服务器清单",
        "",
        "- **Region**: %s" % region,
        "- **查询时间**: %s" % format_query_time(generated_at),
        "- **主机总数**: %d" % len(servers),
    ]
    if filters:
        lines.append("- **过滤条件**: %s" % ", ".join(filters))
    lines.extend(["", "## 裸金属服务器清单", ""])
    if not servers:
        suffix = "（过滤条件: %s）" % ", ".join(filters) if filters else ""
        lines.append("共 0 个裸金属服务器%s" % suffix)
    else:
        lines.append("| %s |" % " | ".join(label for _, label in MD_TABLE_COLUMNS))
        lines.append("| %s |" % " | ".join("---" for _ in MD_TABLE_COLUMNS))
        for server in servers:
            flat = normalize_server(server)
            name = _field(flat, "name", "server_name", default=None)
            if name is None:
                name = _field(flat, "id", "server_id")
            cells = []
            for key, _ in MD_TABLE_COLUMNS:
                value = name if key == "name" else _field(flat, key)
                cells.append(_md_cell(value))
            lines.append("| %s |" % " | ".join(cells))
    lines.append("")
    return "\n".join(lines)


def write_markdown_file(path, content):
    """Write `content` to `path` (UTF-8) and return the absolute path.

    The report is written to a temporary sibling first and moved into place, so
    a failure (missing directory / no permission) never leaves a truncated half
    file behind. Missing parent directories are deliberately *not* created —
    the caller gets an explicit `OutputError` instead.
    """
    target = os.path.abspath(os.path.expanduser(str(path)))
    directory = os.path.dirname(target) or os.getcwd()
    tmp_path = None
    try:
        handle_fd, tmp_path = tempfile.mkstemp(
            prefix=".bms-list-", suffix=".md.tmp", dir=directory)
        with os.fdopen(handle_fd, "w", encoding="utf-8") as handle:
            handle.write(content)
        os.replace(tmp_path, target)
    except OSError as exc:
        if tmp_path:
            try:
                os.unlink(tmp_path)
            except OSError:
                pass
        raise OutputError("无法写入 Markdown 文件 %s: %s" % (target, exc))
    return target


def _cell(value):
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return str(value)


def render_table(servers):
    """Render full-field table output (union of all returned fields)."""
    rows_data = [normalize_server(server) for server in servers]
    columns = []
    for key in PREFERRED_COLUMNS:
        if any(key in i for i in rows_data):
            columns.append(key)
    for key in sorted({k for i in rows_data for k in i}):
        if key not in columns:
            columns.append(key)
    if not columns:
        columns = ["name", "id"]
    rows = [[_cell(_field(i, col)) for col in columns] for i in rows_data]
    widths = [max(len(col), *(len(row[i]) for row in rows)) for i, col in enumerate(columns)]
    header = "  ".join(col.ljust(widths[i]) for i, col in enumerate(columns))
    separator = "  ".join("-" * w for w in widths)
    lines = [header, separator]
    for row in rows:
        lines.append("  ".join(row[i].ljust(widths[i]) for i in range(len(columns))))
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="查询华为云 BMS 裸金属服务器列表（KooCLI hcloud BMS ListBareMetalServers，只读）。")
    parser.add_argument("-r", "--region", default=DEFAULT_REGION,
                        help="目标 Region（默认 %s）" % DEFAULT_REGION)
    parser.add_argument("--json", action="store_true", dest="as_json",
                        help="以 JSON 输出完整原始字段")
    parser.add_argument("--names-only", action="store_true", dest="names_only",
                        help="仅输出服务器名称清单")
    parser.add_argument("--name", help="按裸金属服务器名称过滤（服务端参数）")
    parser.add_argument("--server-id", dest="server_id",
                        help="按裸金属服务器 ID 精确过滤（API 无此参数，全量取回后本地过滤）")
    parser.add_argument("--status",
                        help="按裸金属服务器状态过滤（ACTIVE/BUILD/ERROR/HARD_REBOOT/"
                             "REBOOT/REBUILD/SHUTOFF；服务端参数）")
    parser.add_argument("--page-size", type=int, default=DEFAULT_PAGE_SIZE,
                        dest="page_size", help="分页大小/每页条数（默认 %d，上限 1000）" % DEFAULT_PAGE_SIZE)
    parser.add_argument("--operation", default=ALLOWED_OPERATION,
                        help="hcloud BMS 操作名（仅允许只读 %s）" % ALLOWED_OPERATION)
    parser.add_argument("--md-file", "--output-md", dest="md_file",
                        nargs="?", const="", default=None, metavar="PATH",
                        help="额外把清单写入 Markdown 文件（叠加在 stdout 输出之上）；"
                             "不带路径时写入默认文件名 bms-list-<region>-<YYYYMMDD>.md；"
                             "不指定本参数时不生成任何文件")
    args = parser.parse_args(argv)

    raw_argv = argv if argv is not None else sys.argv[1:]
    try:
        # Write-intent guard: scan the raw argv (excluding the legitimate
        # status enumerant) + validate the operation name. The status value is
        # exempted because REBOOT / HARD_REBOOT / REBUILD are read-only
        # enumerants that contain write-looking words.
        guard_write_intent(" ".join(strip_status_tokens(raw_argv)))
        guard_operation(args.operation)
        if args.name:
            guard_write_intent(args.name)
        if args.status and args.status.strip().upper() not in _ALLOWED_STATUSES:
            guard_write_intent(args.status)
        servers = list_servers(
            args.region,
            status=args.status,
            name=args.name,
            server_id=args.server_id,
            limit=args.page_size,
        )
    except BmsListError as exc:
        print("[错误] %s" % exc, file=sys.stderr)
        return 1

    if args.as_json:
        print(json.dumps(servers, ensure_ascii=False, indent=2))
    elif args.names_only:
        print("Region %s 的 BMS 裸金属服务器名称列表（共 %d 个）：" % (args.region, len(servers)))
        for name in server_names(servers):
            print("- %s" % name)
    elif not servers:
        filters = active_filter_descriptions(
            status=args.status, name=args.name, server_id=args.server_id)
        suffix = "（过滤条件: %s）" % ", ".join(filters) if filters else ""
        print("当前区域（%s）无裸金属服务器%s。" % (args.region, suffix))
    else:
        print("Region %s 的 BMS 裸金属服务器列表（共 %d 个，完整字段）："
              % (args.region, len(servers)))
        print(render_table(servers))

    if args.md_file is not None:
        # `--md-file` without a value (`args.md_file == ""`) picks the default
        # file name; the Markdown export is additive to every stdout mode.
        filters = active_filter_descriptions(
            status=args.status, name=args.name, server_id=args.server_id)
        md_path = args.md_file or default_markdown_name(args.region)
        markdown = render_markdown(args.region, servers, filters=filters)
        try:
            absolute_path = write_markdown_file(md_path, markdown)
        except BmsListError as exc:
            print("[错误] %s" % exc, file=sys.stderr)
            return 1
        print("已生成 Markdown 文件：%s" % absolute_path)

    return 0


if __name__ == "__main__":
    sys.exit(main())
