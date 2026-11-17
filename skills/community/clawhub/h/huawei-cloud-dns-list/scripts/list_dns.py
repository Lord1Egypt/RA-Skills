#!/usr/bin/env python3
"""List Huawei Cloud DNS (云解析服务) zones / record sets via KooCLI `hcloud DNS`.

Primary execution path is KooCLI:
    hcloud DNS ListPublicZones  --cli-region=<region>   (read-only GET /v2/zones)
    hcloud DNS ListPrivateZones --cli-region=<region>   (read-only GET /v2/zones, type=private)
    hcloud DNS ListRecordSets   --cli-region=<region>   (read-only GET /v2/recordsets)
When hcloud is not installed the script falls back to the official
`huaweicloudsdkdns` v2 SDK (`DnsClient.list_public_zones` /
`list_private_zones` / `list_record_sets`). Reads nothing but the active
credential profile / environment. Supports three output modes
(table / --json / --names-only), --type / --id / --name filters (all real
server-side query parameters), marker-based paging, and a strict write-intent
guard: any argument that looks like a mutating DNS operation is rejected before
a single command is executed. API error bodies printed on stdout with exit code
0 (``errCode`` / ``externalMessage``, ``error_code`` / ``error_msg``,
``code`` / ``message``, nested ``error`` — e.g. ``DNS.1802``) are classified as
explicit failures, never as an empty list. ``--output`` / ``-o [FILE]``
additionally writes the current table view to a UTF-8 Markdown file (default
`dns_zones.md` for zones, `dns_recordsets.md` for record sets) without changing
the stdout modes.

Usage:
    python3 scripts/list_dns.py [--region cn-north-4]
                                [--type public|private] [--recordsets]
                                [--json | --names-only]
                                [--id <zone-id>] [--name <domain>]
                                [--record-type A] [--page-size 100]
                                [--project-id <id>] [--operation ListPublicZones]
                                [--output [FILE]]

Environment overrides (mostly for tests):
    DNS_LIST_HCLOUD_BIN   hcloud executable (default "hcloud")
    DNS_LIST_HCLOUD_ARGS  extra args injected before the DNS operation
"""

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile

DEFAULT_REGION = "cn-north-4"
DEFAULT_PAGE_SIZE = 100
SERVICE = "DNS"

OP_LIST_PUBLIC_ZONES = "ListPublicZones"
OP_LIST_PRIVATE_ZONES = "ListPrivateZones"
OP_LIST_RECORD_SETS = "ListRecordSets"
ALLOWED_OPERATIONS = (
    OP_LIST_PUBLIC_ZONES,
    OP_LIST_PRIVATE_ZONES,
    OP_LIST_RECORD_SETS,
)

# Official read-only REST paths, verified from the huaweicloudsdkdns v2
# `DnsClient._*_http_info` metadata (never inferred).
REST_PATH_ZONES = "/v2/zones"
REST_PATH_RECORD_SETS = "/v2/recordsets"

# Mutating DNS operations / intents — strictly rejected by the guard.
WRITE_INTENT_KEYWORDS = (
    "createpubliczone",
    "createprivatezone",
    "deletepubliczone",
    "deleteprivatezone",
    "updatepubliczone",
    "updateprivatezone",
    "batchcreatepubliczones",
    "batchdeletepubliczones",
    "batchupdatzones",
    "createrecordset",
    "createrecordsets",
    "createpublicrecordset",
    "createprivateset",
    "deleterecordset",
    "deleterecordsets",
    "updaterecordset",
    "updaterecordsets",
    "batchcreaterecordsets",
    "batchdeleterecordsets",
    "batchupdaterecordsets",
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
    "transfer",
    "restore",
    "enable",
    "disable",
    "import",
    "export",
    "restart",
    "creating",
    "deleting",
    "updating",
    "enabling",
    "disabling",
)

# Views share one column-union builder so the terminal table and the Markdown
# export never drift apart. Preferred columns come first; every other returned
# field is appended in sorted order.
VIEW_ZONES = "zones"
VIEW_RECORD_SETS = "recordsets"

VIEW_PREFERRED_COLUMNS = {
    VIEW_ZONES: ["name", "zone_type", "status", "record_num", "email", "ttl"],
    VIEW_RECORD_SETS: ["name", "type", "ttl", "records", "zone_name"],
}

# Default Markdown file names per view (used by ``-o`` without a value).
DEFAULT_OUTPUT_FILES = {
    VIEW_ZONES: "dns_zones.md",
    VIEW_RECORD_SETS: "dns_recordsets.md",
}

_ITEM_LIST_KEYS = ("zones", "recordsets", "record_sets", "recordSets")

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
    "not authorized",
    "no identity-based policy",
    "dns.1802",
    "认证失败",
    "权限不足",
    "permission denied",
)

# KooCLI prints usage errors (e.g. "[USE_ERROR]Invalid parameter: xxx") on
# stdout WITH exit code 0 — the marker must be treated as a hard failure even
# when the return code looks successful.
_USE_ERROR_MARKER = "[use_error]"


class DnsListError(Exception):
    """Base error for the DNS list skill."""


class GuardError(DnsListError):
    """A write intent was detected and blocked (skill is read-only)."""


class ConfigError(DnsListError):
    """hcloud missing or credentials (AK/SK) not configured."""


class AuthError(DnsListError):
    """Authentication/authorization failure (invalid AK/SK or IAM 403)."""


class ApiError(DnsListError):
    """hcloud / network / unexpected API failure."""


def guard_write_intent(text):
    """Raise GuardError if `text` carries a mutating intent.

    Normalizes separators so `--create-zone`, `CreatePublicZone`, and
    `create_zone` all hit the same keyword. Read-only vocabulary
    (list/show/get/describe) never matches.
    """
    low = re.sub(r"[\s_\-]+", "", str(text).lower())
    for keyword in WRITE_INTENT_KEYWORDS:
        if keyword in low:
            raise GuardError(
                "检测到写操作意图（关键词: %s）。本 skill 仅支持只读查询"
                "（DNS ListPublicZones / ListPrivateZones / ListRecordSets），"
                "创建/删除/更新域名的变更操作已被守卫拦截。" % keyword
            )
    return False


def _strip_output_value(raw_argv):
    """Drop the ``--output`` / ``-o`` value before the write-intent scan.

    The output path is caller data, not an operation intent, so a path such as
    ``./delete-report.md`` must not trip the guard. All four supported forms
    are handled: ``-o`` (no value), ``-o PATH``, ``--output PATH`` and
    ``--output=PATH``. A following token that starts with ``-`` is a flag, not
    the optional value (argparse ``nargs="?"`` semantics), so it is kept.
    """
    result = []
    skip_value = False
    for arg in raw_argv:
        if skip_value:
            skip_value = False
            if not arg.startswith("-"):
                continue
            result.append(arg)
            continue
        if arg in ("--output", "-o"):
            skip_value = True
            continue
        if arg.startswith("--output="):
            continue
        if arg.startswith("-o") and not arg.startswith("--") and len(arg) > 2:
            continue
        result.append(arg)
    return result


def guard_operation(operation):
    """Only the read-only list operations may be executed."""
    if operation not in ALLOWED_OPERATIONS:
        raise GuardError(
            "不允许的操作 %r：本 skill 仅允许只读操作 %s。"
            % (operation, " / ".join(ALLOWED_OPERATIONS))
        )
    return True


def resolve_operation(type_arg, recordsets):
    """Map --type / --recordsets to the concrete read-only DNS operation."""
    if recordsets:
        return OP_LIST_RECORD_SETS
    if type_arg == "private":
        return OP_LIST_PRIVATE_ZONES
    return OP_LIST_PUBLIC_ZONES


def build_command(region, operation, zone_type="public", item_id=None,
                  name=None, record_type=None, limit=DEFAULT_PAGE_SIZE,
                  marker=None):
    """Build the hcloud DNS argv (without the executable).

    Mirrors the real KooCLI parameter list for the read-only DNS list
    operations: --cli-region / --limit / --marker plus the real server-side
    filters. ListPrivateZones declares ``--type`` as a **required** parameter
    (range: private), so ``--type=private`` is always appended for it —
    ListPublicZones has no such required parameter and keeps the service
    default. Record-set listings take --zone_type (public/private) and an
    optional --type (record type, e.g. A/AAAA/CNAME).
    """
    argv = [
        SERVICE,
        operation,
        "--cli-region=%s" % region,
        "--limit=%d" % limit,
    ]
    if marker:
        argv.append("--marker=%s" % marker)
    if item_id:
        argv.append("--id=%s" % item_id)
    if name:
        argv.append("--name=%s" % name)
    if operation == OP_LIST_PRIVATE_ZONES:
        # `hcloud DNS ListPrivateZones --help` marks `--type` as required
        # (range: private). Without it KooCLI fails with
        # `[USE_ERROR] The following parameters are required: type`.
        argv.append("--type=private")
    elif operation == OP_LIST_RECORD_SETS:
        argv.append("--zone_type=%s" % zone_type)
        if record_type:
            argv.append("--type=%s" % record_type)
    return argv


def _hcloud_executable():
    return os.environ.get("DNS_LIST_HCLOUD_BIN", "hcloud")


def run_hcloud(argv):
    """Execute hcloud and return (stdout, stderr, returncode)."""
    cmd = [_hcloud_executable()]
    extra = os.environ.get("DNS_LIST_HCLOUD_ARGS", "").split()
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
    """Parse hcloud stdout as JSON, tolerating trailing diagnostic text.

    KooCLI may append diagnostics after the JSON body, so when a plain
    ``json.loads`` fails the first complete JSON value is decoded starting at
    the first ``{`` via ``raw_decode`` instead of slicing through the last
    ``}`` (which trailing text would break).
    """
    text = stdout.strip()
    if not text:
        return {}
    try:
        return json.loads(text)
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
        return payload


def _payload_error(payload):
    """Return the error text when a payload is a DNS/KooCLI error envelope.

    KooCLI returns HTTP-level API errors on stdout with exit code 0, e.g.
    ``{"errCode": "DNS.1802", "externalMessage": "..."}`` or
    ``{"code": "DNS.1802", "message": "..."}``. Such an envelope must surface
    as an explicit error, never as an empty zone / record-set list.
    """
    if not isinstance(payload, dict):
        return None
    for code_key, msg_key in (
        ("errCode", "externalMessage"),
        ("error_code", "error_msg"),
        ("errorCode", "errorMsg"),
        ("code", "message"),
    ):
        code = payload.get(code_key)
        if code:
            msg = payload.get(msg_key) or ""
            return ("%s %s" % (code, msg)).strip()
    err = payload.get("error")
    if isinstance(err, dict):
        code = err.get("error_code") or err.get("code") or err.get("errCode") or ""
        msg = (err.get("error_msg") or err.get("message")
               or err.get("externalMessage") or "")
        text = ("%s %s" % (code, msg)).strip()
        return text or None
    if isinstance(err, str) and err.strip():
        return err.strip()
    return None


def classify_hcloud_failure(stdout, stderr, returncode):
    """Map a failed hcloud invocation to a domain error with explicit hints."""
    blob = (stderr + " " + stdout).strip()
    low = blob.lower()
    if _USE_ERROR_MARKER in low:
        return ApiError(
            "hcloud 参数错误（KooCLI 拒绝了该参数组合，退出码 %s）：DNS 列表操作"
            "真实参数清单可通过 `hcloud DNS ListPublicZones --help` 查看。"
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
            "无权限访问云解析服务（DNS），请检查 IAM 权限（DNS.1802 / 403："
            "AK/SK 无效、未授予 DNS 只读权限或身份策略不允许该操作），"
            "参见 references/iam-policies.md。详情：%s" % blob[:300]
        )
    return ApiError(
        "hcloud 调用失败（退出码 %s）：%s" % (returncode, blob[:300])
    )


def extract_items(payload):
    """Pull the zone / record-set list out of a DNS list response."""
    if isinstance(payload, list):
        return payload
    for key in _ITEM_LIST_KEYS:
        value = payload.get(key)
        if isinstance(value, list):
            return value
    return []


def _item_id(item):
    if isinstance(item, dict):
        return item.get("id")
    return None


def _total_count(payload):
    """Read `metadata.total_count` from a DNS list response, if present."""
    if isinstance(payload, dict):
        meta = payload.get("metadata") or payload.get("page_info") \
            or payload.get("pageInfo")
        if isinstance(meta, dict):
            total = meta.get("total_count")
            if total is None:
                total = meta.get("totalCount")
            if isinstance(total, int) and not isinstance(total, bool):
                return total
    return None


def _next_marker(payload, items):
    """Determine the marker for the next page.

    The DNS list APIs page by the **id of the last resource of the previous
    page** (their responses carry `metadata.total_count` but no
    `next_marker`); a `next_marker` is honoured first if a proxy ever
    provides one.
    """
    if isinstance(payload, dict):
        page_info = (payload.get("page_info") or payload.get("pageInfo")
                     or payload.get("metadata"))
        if isinstance(page_info, dict):
            marker = page_info.get("next_marker") or page_info.get("nextMarker")
            if marker:
                return str(marker)
    if items:
        last_id = _item_id(items[-1])
        if last_id:
            return str(last_id)
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


def list_dns_via_sdk(region, operation, zone_type="public", item_id=None,
                     name=None, record_type=None, limit=DEFAULT_PAGE_SIZE,
                     project_id=None, max_pages=100):
    """SDK fallback: query DNS through `huaweicloudsdkdns` v2.

    Only invoked when hcloud is not installed. Credentials are taken from the
    whitelisted AK/SK environment variables (HW_*/HUAWEI_ACCESS_KEY family) —
    never passed as literals here. The official SDK has no env-var
    auto-discovery on `BasicCredentials()`, so AK/SK and the project id must be
    read explicitly. Region resolution uses the SDK's own `DnsRegion` catalog
    (official endpoints, no guessing), falling back to an explicit
    `Region(id, endpoint)` for custom regions.
    """
    try:
        from huaweicloudsdkcore.auth.credentials import BasicCredentials
        from huaweicloudsdkcore.region.region import Region
        from huaweicloudsdkcore.http.http_config import HttpConfig
        from huaweicloudsdkdns.v2 import (
            DnsClient, ListPublicZonesRequest, ListPrivateZonesRequest,
            ListRecordSetsRequest,
        )
        from huaweicloudsdkdns.v2.region.dns_region import DnsRegion
    except ImportError as exc:
        raise ConfigError(
            "未找到 hcloud（KooCLI），且 huaweicloudsdkcore/huaweicloudsdkdns 未安装，"
            "无法回退到 SDK。请安装 KooCLI 或 pip install huaweicloudsdkcore "
            "huaweicloudsdkdns。详情：%s" % exc
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
            "SDK 回退缺少 project_id：DNS 的 REST 路径为 %s / %s，需要项目 ID。"
            "请通过 --project-id 传入，或设置 HUAWEICLOUD_SDK_PROJECT_ID / "
            "HUAWEI_PROJECT_ID（严禁在对话中粘贴敏感信息）。"
            % (REST_PATH_ZONES, REST_PATH_RECORD_SETS)
        )
    credentials = BasicCredentials(ak=ak, sk=sk, project_id=resolved_project_id)  # env-sourced, never literals
    try:
        try:
            region_obj = DnsRegion.value_of(region)
        except (ValueError, KeyError, AttributeError):
            region_obj = Region(region, "https://dns.%s.myhuaweicloud.com" % region)
        client = DnsClient.new_builder() \
            .with_credentials(credentials) \
            .with_region(region_obj) \
            .with_http_config(HttpConfig.get_default_config()) \
            .build()
    except Exception as exc:  # region unknown / config broken
        raise ConfigError(
            "SDK 初始化失败（region=%s）：%s。请检查 huaweicloudsdkdns 安装与区域配置。"
            % (region, exc)
        )
    items = []
    marker = None
    for _ in range(max_pages):
        if operation == OP_LIST_RECORD_SETS:
            request = ListRecordSetsRequest(
                zone_type=zone_type, limit=limit, marker=marker,
                id=item_id, name=name, type=record_type,
            )
        elif operation == OP_LIST_PRIVATE_ZONES:
            request = ListPrivateZonesRequest(
                type="private", limit=limit, marker=marker,
                id=item_id, name=name,
            )
        else:
            request = ListPublicZonesRequest(
                type="public", limit=limit, marker=marker,
                id=item_id, name=name,
            )
        try:
            if operation == OP_LIST_RECORD_SETS:
                response = client.list_record_sets(request)
                batch_objs = list(response.recordsets or [])
            elif operation == OP_LIST_PRIVATE_ZONES:
                response = client.list_private_zones(request)
                batch_objs = list(response.zones or [])
            else:
                response = client.list_public_zones(request)
                batch_objs = list(response.zones or [])
        except Exception as exc:
            low = str(exc).lower()
            if any(p in low for p in _AUTH_PATTERNS):
                raise AuthError(
                    "无权限访问云解析服务（DNS），请检查 IAM 权限（403）。详情：%s"
                    % str(exc)[:300]
                )
            raise ApiError("SDK 调用失败：%s" % str(exc)[:300])
        batch = [_jsonable(obj.to_dict()) for obj in batch_objs]
        items.extend(batch)
        try:
            total = _total_count(_jsonable(response.to_dict()))
        except Exception:
            total = None
        if total is not None and len(items) >= total:
            break
        next_marker = _next_marker({}, batch)
        if not next_marker or not batch or len(batch) < limit \
                or next_marker == marker:
            break
        marker = next_marker
    else:
        raise ApiError("翻页超过 %d 页仍未取完，已中止以防死循环。" % max_pages)
    return items


def list_dns(region, operation, zone_type="public", item_id=None, name=None,
             record_type=None, limit=DEFAULT_PAGE_SIZE, project_id=None,
             max_pages=100):
    """Query all DNS zones / record sets (marker-paged); KooCLI first, SDK fallback."""
    items = []
    marker = None
    for _page in range(max_pages):
        argv = build_command(region, operation, zone_type=zone_type,
                             item_id=item_id, name=name,
                             record_type=record_type, limit=limit, marker=marker)
        try:
            stdout, stderr, returncode = run_hcloud(argv)
        except ConfigError:
            # hcloud binary missing → one-shot SDK fallback (no CLI retry).
            items = list_dns_via_sdk(
                region, operation, zone_type=zone_type, item_id=item_id,
                name=name, record_type=record_type, limit=limit,
                project_id=project_id, max_pages=max_pages,
            )
            break
        if returncode != 0 or _USE_ERROR_MARKER in (stdout + " " + stderr).lower():
            # KooCLI usage errors print [USE_ERROR] on stdout with rc=0.
            raise classify_hcloud_failure(stdout, stderr, returncode)
        payload = extract_json(stdout)
        err_text = _payload_error(payload)
        if err_text:
            raise classify_hcloud_failure("", err_text, returncode)
        batch = extract_items(payload)
        items.extend(batch)
        total = _total_count(payload)
        if total is not None and len(items) >= total:
            break
        new_marker = _next_marker(payload, batch)
        if not new_marker or not batch or len(batch) < limit \
                or new_marker == marker:
            break
        marker = new_marker
    else:
        raise ApiError("翻页超过 %d 页仍未取完，已中止以防死循环。" % max_pages)
    return items


def _field(item, *names, default="-"):
    for name in names:
        if name in item and item[name] not in (None, ""):
            return item[name]
    return default


def item_names(items):
    """Compact name list (DNS domain name, falling back to id)."""
    names = []
    for item in items:
        name = _field(item, "name", default=None)
        if name is None:
            name = _field(item, "id")
        names.append(str(name))
    return names


def _cell(value):
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return str(value)


def _table_columns(items, view=VIEW_ZONES):
    """Build the column list shared by the terminal table and Markdown export.

    Preferred columns for the view come first (only if any item carries them),
    then every other returned field in sorted order. An empty result falls back
    to the view's preferred columns so a header-only table is still emitted.
    """
    preferred = VIEW_PREFERRED_COLUMNS.get(view, VIEW_PREFERRED_COLUMNS[VIEW_ZONES])
    rows_data = [dict(item) for item in items]
    columns = [key for key in preferred if any(key in row for row in rows_data)]
    for key in sorted({k for row in rows_data for k in row}):
        if key not in columns:
            columns.append(key)
    if not columns:
        columns = list(preferred)
    return columns


def render_table(items, view=VIEW_ZONES):
    """Render full-field table output (union of all returned fields)."""
    rows_data = [dict(item) for item in items]
    columns = _table_columns(items, view)
    rows = [[_cell(_field(row, col)) for col in columns] for row in rows_data]
    widths = [max(len(col), *(len(row[i]) for row in rows))
              for i, col in enumerate(columns)]
    header = "  ".join(col.ljust(widths[i]) for i, col in enumerate(columns))
    separator = "  ".join("-" * w for w in widths)
    lines = [header, separator]
    for row in rows:
        lines.append("  ".join(row[i].ljust(widths[i])
                               for i in range(len(columns))))
    return "\n".join(lines)


def _md_escape(text):
    """Escape a cell for a Markdown table (pipe + line breaks)."""
    escaped = str(text).replace("|", "\\|")
    return (escaped.replace("\r\n", "<br>")
            .replace("\n", "<br>")
            .replace("\r", "<br>"))


def render_markdown(items, columns):
    """Render ``items`` as a GitHub-flavoured Markdown table.

    Missing fields render as ``-`` and nested ``tags`` / ``links`` as compact
    JSON (both via ``_field`` / ``_cell``); pipes and newlines are escaped so
    the table stays valid. An empty ``items`` list still yields a header-only
    table.
    """
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, separator]
    for item in items:
        row = [_md_escape(_cell(_field(item, col))) for col in columns]
        lines.append("| " + " | ".join(row) + " |")
    return "\n".join(lines) + "\n"


def write_markdown(path, text):
    """Write ``text`` to ``path`` atomically as UTF-8 (temp file + rename).

    The parent directory must already exist and be writable; otherwise an
    ``ApiError`` is raised and no partial / temporary file is left behind.
    """
    target = os.path.abspath(path)
    directory = os.path.dirname(target) or "."
    if not os.path.isdir(directory):
        raise ApiError(
            "Markdown 文件写出失败（目录不存在：%s）" % directory)
    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(
                mode="w", encoding="utf-8", dir=directory,
                prefix=".dns-md-", suffix=".tmp", delete=False) as handle:
            tmp_path = handle.name
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp_path, target)
        tmp_path = None
    except OSError as exc:
        raise ApiError("Markdown 文件写出失败（%s）：%s" % (path, exc))
    finally:
        if tmp_path is not None:
            try:
                os.unlink(tmp_path)
            except OSError:
                pass
    return target


def resolve_output_path(value, view=VIEW_ZONES):
    """Resolve ``--output`` into a path (``None`` when export is disabled).

    ``value is True`` means the flag was given without a value (argparse
    ``nargs="?"`` const), so the view's default file name under the current
    directory is used.
    """
    if value is None:
        return None
    if value is True or value == "":
        default_name = DEFAULT_OUTPUT_FILES.get(
            view, DEFAULT_OUTPUT_FILES[VIEW_ZONES])
        return os.path.join(os.getcwd(), default_name)
    return str(value)


def _zone_type_label(zone_type):
    return "私网" if zone_type == "private" else "公网"


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="查询华为云云解析服务（DNS）域名/记录集名称列表"
                    "（KooCLI hcloud DNS ListPublicZones/ListPrivateZones/ListRecordSets，只读）。")
    parser.add_argument("-r", "--region", default=DEFAULT_REGION,
                        help="目标 Region（默认 %s）" % DEFAULT_REGION)
    parser.add_argument("--type", choices=("public", "private"), default="public",
                        help="域名类型：public 公网域名（默认）/ private 私网域名")
    parser.add_argument("--recordsets", action="store_true", dest="recordsets",
                        help="改为查询记录集列表（ListRecordSets）而非域名列表")
    parser.add_argument("--json", action="store_true", dest="as_json",
                        help="以 JSON 输出完整原始字段")
    parser.add_argument("--names-only", action="store_true", dest="names_only",
                        help="仅输出域名 / 记录集名称清单")
    parser.add_argument("--id", dest="item_id",
                        help="按域名 ID（或记录集 ID）过滤（服务端查询参数）")
    parser.add_argument("--name",
                        help="按域名过滤（服务端模糊查询参数）")
    parser.add_argument("--record-type", dest="record_type",
                        help="记录集类型过滤（仅 --recordsets 有效，如 A / AAAA / CNAME）")
    parser.add_argument("--page-size", type=int, default=DEFAULT_PAGE_SIZE,
                        dest="page_size",
                        help="分页大小（默认 %d，范围 0~500）" % DEFAULT_PAGE_SIZE)
    parser.add_argument("--project-id", dest="project_id",
                        help="项目 ID（可选；SDK 回退在 /v2/zones、/v2/recordsets 路径中需要）")
    parser.add_argument("--operation", default=None,
                        help="hcloud DNS 操作名（仅允许只读 %s）"
                             % " / ".join(ALLOWED_OPERATIONS))
    parser.add_argument("-o", "--output", nargs="?", const=True, default=None,
                        metavar="FILE",
                        help="导出当前表格视图为 Markdown 文件并打印绝对路径；"
                             "仅传 -o 时 zone 视图默认 dns_zones.md、记录集视图"
                             "默认 dns_recordsets.md")
    args = parser.parse_args(argv)

    raw_argv = argv if argv is not None else sys.argv[1:]

    try:
        # Write-intent guard: scan the raw argv (minus the --output value) +
        # validate the operation name.
        guard_write_intent(" ".join(_strip_output_value(raw_argv)))
        operation = args.operation or resolve_operation(args.type, args.recordsets)
        guard_operation(operation)
        items = list_dns(
            args.region,
            operation,
            zone_type=args.type,
            item_id=args.item_id,
            name=args.name,
            record_type=args.record_type,
            limit=args.page_size,
            project_id=args.project_id,
        )
    except DnsListError as exc:
        print("[错误] %s" % exc, file=sys.stderr)
        return 1

    is_record_sets = operation == OP_LIST_RECORD_SETS
    view = VIEW_RECORD_SETS if is_record_sets else VIEW_ZONES
    zone_type = "private" if operation == OP_LIST_PRIVATE_ZONES else "public"
    subject = ("DNS 记录集" if is_record_sets
               else "DNS %s域名" % _zone_type_label(zone_type))
    columns = _table_columns(items, view)

    if args.as_json:
        print(json.dumps(items, ensure_ascii=False, indent=2))
        return 0

    if args.names_only:
        print("Region %s 的 %s名称列表（共 %d 个）："
              % (args.region, subject, len(items)))
        for name in item_names(items):
            print("- %s" % name)
        return 0

    output_path = resolve_output_path(args.output, view)
    if output_path is not None:
        try:
            write_markdown(output_path, render_markdown(items, columns))
        except DnsListError as exc:
            print("[错误] %s" % exc, file=sys.stderr)
            return 1
        print(os.path.abspath(output_path))

    if not items:
        filters = []
        if args.item_id:
            filters.append("id=%s" % args.item_id)
        if args.name:
            filters.append("name=%s" % args.name)
        if args.record_type and is_record_sets:
            filters.append("record_type=%s" % args.record_type)
        suffix = "（过滤条件: %s）" % ", ".join(filters) if filters else ""
        print("当前区域（%s）无 %s%s。" % (args.region, subject, suffix))
        return 0

    print("Region %s 的 %s列表（共 %d 个，完整字段）："
          % (args.region, subject, len(items)))
    print(render_table(items, view))
    return 0


if __name__ == "__main__":
    sys.exit(main())