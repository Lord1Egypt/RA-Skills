#!/usr/bin/env python3
"""List Huawei Cloud CSE microservice engines (read-only) via KooCLI.

Primary path (KooCLI):

    hcloud CSE ListEngines --cli-region=<region> --limit=<n> --offset=<n> [--type=ALL] [--project_id=<id>]
    GET /v2/{project_id}/enginemgr/engines

Fallback when the hcloud binary is not installed: the official Python SDK
(``huaweicloudsdkcse.v1`` — the SDK module that exposes the same v2 REST API)
via ``CseClient.list_engines``. Credentials are only ever taken from the active
KooCLI profile / standard environment variables; the script never reads,
echoes or stores secrets itself.

Output modes:

    default        concise inventory (name + id + type + version + status + instances)
    --table        full-field table (union of all returned fields)
    --json         normalized raw items as JSON

Filters: ``--type`` (server-side: ALL / CSE / Nacos / MicroGateway),
``--name`` (client-side exact, case-insensitive) and ``--fuzzy`` (client-side
substring), ``--region`` (default cn-north-4).

A strict write-intent guard rejects any mutating intent (create / delete /
update / upgrade / modify / remove / start / stop / resize ...) before a single
command is executed: this skill is strictly read-only.

Usage:
    python3 scripts/list_cse_engines.py [--region cn-north-4]
                                        [--type ALL|CSE|Nacos|MicroGateway]
                                        [--name NAME] [--fuzzy]
                                        [--project-id <id>]
                                        [--table | --json] [--page-size 100]

Environment overrides (mostly for tests):
    CSE_LIST_HCLOUD_BIN   hcloud executable (default "hcloud")
    CSE_LIST_HCLOUD_ARGS  extra args injected before the operation
"""

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone

DEFAULT_REGION = "cn-north-4"
DEFAULT_PAGE_SIZE = 100
MAX_PAGES = 100

SERVICE = "CSE"
OPERATION = "ListEngines"
REST_PATH = "GET /v2/{project_id}/enginemgr/engines"
ENGINE_TYPES = ("ALL", "CSE", "Nacos", "MicroGateway")
_ENGINE_TYPE_BY_LOWER = {t.lower(): t for t in ENGINE_TYPES}


def normalize_engine_type(value):
    """Canonicalize ``--type`` case-insensitively (nacos -> Nacos)."""
    return _ENGINE_TYPE_BY_LOWER.get(str(value).lower(), value)
ALLOWED_OPERATIONS = frozenset((OPERATION,))

# Mutating CSE intents — strictly rejected by the guard. Read-only vocabulary
# (list / show / get / describe / query) and words inside our own operation
# name must never be listed here.
WRITE_INTENT_KEYWORDS = (
    "create",
    "delete",
    "update",
    "upgrade",
    "modify",
    "remove",
    "destroy",
    "terminate",
    "start",
    "stop",
    "restart",
    "reboot",
    "resize",
    "scale",
    "bind",
    "unbind",
    "batchcreate",
    "batchdelete",
    "batchupdate",
    "batchmodify",
    "createengine",
    "deleteengine",
    "updateengine",
    "upgradeengine",
    "modifyengine",
    "resizeengine",
    "rebootengine",
    "startengine",
    "stopengine",
)

# Flags whose *values* are pure read data (filters / selectors) and must NOT be
# scanned by the write-intent guard. `--operation` is validated separately
# against the operation whitelist.
_VALUE_STRIPPED_FLAGS = (
    "--region",
    "-r",
    "--type",
    "--name",
    "--project-id",
    "--page-size",
)

# Canonical field aliases (KooCLI returns camelCase, the SDK exposes snake_case).
NAME_KEYS = ("name", "engine_name", "engineName")
ID_KEYS = ("id", "engine_id", "engineId")
TYPE_KEYS = ("type", "engine_type", "engineType")
VERSION_KEYS = ("version",)
STATUS_KEYS = ("status",)
FLAVOR_KEYS = ("flavor", "spec", "spec_type", "specType")
TOTAL_INSTANCE_KEYS = ("total_instance", "totalInstance")
USED_INSTANCE_KEYS = ("used_instance", "usedInstance")
AVAILABLE_INSTANCE_KEYS = ("available_instance", "availableInstance")
CREATE_TIME_KEYS = ("create_time", "createTime")
REGION_KEYS = ("region",)

PREFERRED_COLUMNS = [
    "name",
    "id",
    "type",
    "version",
    "status",
    "flavor",
    "total_instance",
    "used_instance",
    "available_instance",
    "create_time",
    "region",
    "enterprise_project_id",
    "enterprise_project_name",
    "description",
    "payment",
    "auth_type",
    "external_address",
    "public_address",
    "latest_version",
    "due_to",
]

TIME_COLUMNS = frozenset(("create_time", "due_to"))

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
    "profile",
)

_AUTH_PATTERNS = (
    "401",
    "403",
    "unauthorized",
    "forbidden",
    "not authorized",
    "not authorized to perform",
    "does not have valid roles",
    "permission denied",
    "认证失败",
    "权限不足",
    "svcstg.00509431",
    "cse:engine:list",
)

_NETWORK_PATTERNS = (
    "timed out",
    "timeout",
    "connection refused",
    "connection reset",
    "could not resolve",
    "name or service not known",
    "network is unreachable",
    "temporary failure in name resolution",
    "ssl error",
    "proxy",
)

# KooCLI prints usage errors (e.g. "[USE_ERROR]Invalid parameter: xxx") on
# stdout WITH exit code 0 — the marker must be treated as a hard failure even
# when the return code looks successful.
_USE_ERROR_MARKER = "[use_error]"


class CseListError(Exception):
    """Base error for the CSE engine list skill."""


class GuardError(CseListError):
    """A write intent was detected and blocked (skill is read-only)."""


class ConfigError(CseListError):
    """hcloud missing or credentials (AK/SK) not configured."""


class AuthError(CseListError):
    """Authentication/authorization failure (invalid AK/SK or IAM 403)."""


class ApiError(CseListError):
    """hcloud / network / unexpected API failure."""


def guard_write_intent(text):
    """Raise GuardError if `text` carries a mutating intent.

    Separators are normalized so ``--create-engine``, ``CreateEngine`` and
    ``create_engine`` all hit the same keyword. Read-only vocabulary never
    matches.
    """
    low = re.sub(r"[\s_\-:]+", "", str(text).lower())
    for keyword in WRITE_INTENT_KEYWORDS:
        if keyword in low:
            raise GuardError(
                "检测到写操作意图（关键词: %s）。本 skill 仅支持只读查询"
                "（CSE ListEngines），创建/删除/更新/升级/变更等操作已被守卫拦截。"
                % keyword
            )
    return False


def guard_operation(operation):
    """Only the read-only ListEngines operation may run."""
    if operation not in ALLOWED_OPERATIONS:
        raise GuardError(
            "不允许的操作 %r：本 skill 仅允许只读操作 %s。" % (operation, OPERATION)
        )
    return True


def guard_text_from_argv(argv):
    """Build the text the write-intent guard should scan.

    Scans flag names and positional tokens, but strips the values of the
    read-only selector/filter flags (region / type / name / project-id /
    page-size): those are pure read data and may legitimately contain
    write-looking words (e.g. an engine named ``update-prod``).
    """
    tokens = list(argv if argv is not None else sys.argv[1:])
    kept = []
    skip_next = False
    for tok in tokens:
        if skip_next:
            skip_next = False
            continue
        key = tok.split("=", 1)[0]
        if tok in _VALUE_STRIPPED_FLAGS:
            skip_next = True
            continue
        if tok.startswith("-") and "=" in tok and key in _VALUE_STRIPPED_FLAGS:
            continue
        kept.append(tok)
    return " ".join(kept)


def build_command(region, engine_type="ALL", project_id=None,
                  limit=DEFAULT_PAGE_SIZE, offset=0):
    """Build the hcloud argv (without executable) for ListEngines.

    Parameter names mirror the live KooCLI metadata exactly:
    ``--cli-region`` ``--limit`` (string) ``--offset`` (integer) ``--type``
    and optional ``--project_id``.
    """
    argv = [
        SERVICE,
        OPERATION,
        "--cli-region=%s" % region,
        "--limit=%s" % limit,
        "--offset=%d" % offset,
    ]
    if engine_type:
        argv.append("--type=%s" % engine_type)
    if project_id:
        argv.append("--project_id=%s" % project_id)
    return argv


def _hcloud_executable():
    return os.environ.get("CSE_LIST_HCLOUD_BIN", "hcloud")


def run_hcloud(argv):
    """Execute hcloud and return (stdout, stderr, returncode)."""
    cmd = [_hcloud_executable()]
    extra = os.environ.get("CSE_LIST_HCLOUD_ARGS", "").split()
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
        raise ApiError(
            "网络异常或 hcloud 执行超时（120s），请检查网络后重试。"
        )
    return proc.stdout or "", proc.stderr or "", proc.returncode


def extract_json(stdout):
    """Parse hcloud stdout as JSON; tolerate wrapper/noise lines.

    Handles both JSON objects (``{"total":N,"data":[...]}``) and bare JSON
    arrays (defensive: some list endpoints return a top-level array).
    """
    text = stdout.strip()
    if not text:
        return {}
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    obj_at, arr_at = text.find("{"), text.find("[")
    candidates = []
    if arr_at >= 0 and (obj_at < 0 or arr_at < obj_at):
        candidates = [("[", "]"), ("{", "}")]
    else:
        candidates = [("{", "}"), ("[", "]")]
    for open_ch, close_ch in candidates:
        start, end = text.find(open_ch), text.rfind(close_ch)
        if start >= 0 and end > start:
            try:
                return json.loads(text[start:end + 1])
            except json.JSONDecodeError:
                continue
    raise ApiError("hcloud 输出无法解析为 JSON：%s" % text[:200])


def _looks_like_auth(blob):
    low = blob.lower()
    return any(p in low for p in _AUTH_PATTERNS)


def _looks_like_missing_credential(blob):
    low = blob.lower()
    return any(p in low for p in _CREDENTIAL_MISSING_PATTERNS)


def _looks_like_network(blob):
    low = blob.lower()
    return any(p in low for p in _NETWORK_PATTERNS)


def auth_error(blob):
    return AuthError(
        "无权限访问 CSE 微服务引擎，请检查 IAM 权限"
        "（需要 cse:engine:list，403：AK/SK 无效、区域不符或未授予只读权限），"
        "参见 references/iam-policies.md。详情：%s" % blob[:300]
    )


def error_from_payload(payload):
    """Turn an API error body into a domain error (hcloud may return rc=0).

    KooCLI prints ``{"error_code": "...", "error_message": "..."}`` on stdout
    while still exiting 0; the body must be classified explicitly.
    """
    if not isinstance(payload, dict):
        return None
    code = payload.get("error_code") or payload.get("errorCode")
    message = payload.get("error_message") or payload.get("errorMessage")
    if not code and not message:
        return None
    blob = "%s %s" % (code or "", message or "")
    if _looks_like_auth(blob):
        return auth_error(blob)
    if _looks_like_missing_credential(blob):
        return config_missing_credential_error(blob)
    return ApiError(
        "CSE 接口返回错误（%s）：%s" % (code or "-", (message or "")[:300])
    )


def config_missing_credential_error(blob):
    return ConfigError(
        "缺少 AK/SK 凭证：hcloud 未配置有效凭证。请先运行 hcloud configure 或"
        "设置凭证环境变量（严禁在对话中粘贴 AK/SK），参见"
        " references/cli-installation-guide.md。详情：%s" % blob[:300]
    )


def classify_hcloud_failure(stdout, stderr, returncode):
    """Map a failed hcloud invocation to a domain error with explicit hints."""
    blob = (stderr + " " + stdout).strip()
    low = blob.lower()
    if _USE_ERROR_MARKER in low:
        return ApiError(
            "hcloud 参数错误（KooCLI 拒绝了该参数组合，退出码 %s）：真实参数清单可通过 "
            "`hcloud %s %s --help` 查看。详情：%s"
            % (returncode, SERVICE, OPERATION, blob[:300])
        )
    if _looks_like_auth(blob):
        return auth_error(blob)
    if _looks_like_missing_credential(blob):
        return config_missing_credential_error(blob)
    if _looks_like_network(blob):
        return ApiError(
            "网络异常：无法连接 CSE 服务（退出码 %s）。请检查网络/代理后重试。详情：%s"
            % (returncode, blob[:300])
        )
    return ApiError("hcloud 调用失败（退出码 %s）：%s" % (returncode, blob[:300]))


def extract_engines(payload):
    """Return ``(engines, total)`` from a ListEngines response.

    Compatible with ``{"total": N, "data": [...]}`` and a bare ``[...]`` array.
    """
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)], None
    if not isinstance(payload, dict):
        return [], None
    data = None
    for key in ("data", "engines", "items", "result"):
        value = payload.get(key)
        if isinstance(value, list):
            data = value
            break
    total = payload.get("total")
    if not isinstance(total, int) or isinstance(total, bool):
        total = None
    return ([item for item in (data or []) if isinstance(item, dict)], total)


def _payload_total(payload):
    if not isinstance(payload, dict):
        return None
    total = payload.get("total")
    if isinstance(total, int) and not isinstance(total, bool):
        return total
    return None


def _has_more(batch, collected, limit, payload):
    if not batch:
        return False
    total = _payload_total(payload)
    if total is not None and total >= 0:
        return collected < total
    return len(batch) >= limit


def _field(item, *names, **kwargs):
    default = kwargs.get("default", "-")
    if not isinstance(item, dict):
        return default
    for name in names:
        if name in item and item[name] not in (None, ""):
            return item[name]
    return default


def _pick(item, keys):
    for key in keys:
        if key in item and item[key] not in (None, ""):
            return item[key]
    return None


def format_time(value):
    """Render an epoch (seconds or milliseconds) or ISO string readably."""
    if value in (None, ""):
        return "-"
    if isinstance(value, bool):
        return str(value)
    if isinstance(value, (int, float)) or (
            isinstance(value, str) and value.strip().isdigit()):
        number = int(value)
        seconds = number / 1000.0 if number > 10 ** 12 else float(number)
        try:
            return datetime.fromtimestamp(
                seconds, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        except (OverflowError, OSError, ValueError):
            return str(value)
    return str(value)


def filter_by_name(items, name, fuzzy=False):
    """Client-side name filter (case-insensitive).

    Default is an exact match; ``--fuzzy`` switches to a substring match.
    """
    if not name:
        return list(items)
    wanted = str(name).strip().lower()
    out = []
    for item in items:
        value = _field(item, *NAME_KEYS, default=None)
        if value is None:
            continue
        probe = str(value).strip().lower()
        if (wanted in probe) if fuzzy else (probe == wanted):
            out.append(item)
    return out


def normalize_engine(item, region):
    """Flatten one engine object into table-friendly canonical keys."""
    flat = dict(item) if isinstance(item, dict) else {}
    canonical = {
        "name": _pick(flat, NAME_KEYS),
        "id": _pick(flat, ID_KEYS),
        "type": _pick(flat, TYPE_KEYS),
        "version": _pick(flat, VERSION_KEYS),
        "status": _pick(flat, STATUS_KEYS),
        "flavor": _pick(flat, FLAVOR_KEYS),
        "total_instance": _pick(flat, TOTAL_INSTANCE_KEYS),
        "used_instance": _pick(flat, USED_INSTANCE_KEYS),
        "available_instance": _pick(flat, AVAILABLE_INSTANCE_KEYS),
        "create_time": _pick(flat, CREATE_TIME_KEYS),
        "region": _pick(flat, REGION_KEYS) or region,
    }
    for key, value in canonical.items():
        if value is not None:
            flat[key] = value
    flat.setdefault("region", region)
    return flat


def _cell(value, column=None):
    if column in TIME_COLUMNS:
        return format_time(value)
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return str(value)


def render_table(items, region):
    """Render full-field table output (union of all returned fields)."""
    rows_data = [normalize_engine(item, region) for item in items]
    columns = []
    for key in PREFERRED_COLUMNS:
        if any(key in i for i in rows_data):
            columns.append(key)
    for key in sorted({k for i in rows_data for k in i}):
        if key not in columns:
            columns.append(key)
    if not columns:
        columns = ["name", "id"]
    rows = [[_cell(_field(i, col), col) for col in columns] for i in rows_data]
    widths = [max(len(col), *(len(row[i]) for row in rows))
              for i, col in enumerate(columns)]
    header = "  ".join(col.ljust(widths[i]) for i, col in enumerate(columns))
    separator = "  ".join("-" * w for w in widths)
    lines = [header, separator]
    for row in rows:
        lines.append("  ".join(row[i].ljust(widths[i])
                               for i in range(len(columns))))
    return "\n".join(lines)


def item_summary_lines(items, region):
    """Compact inventory lines for the default (concise) output mode."""
    lines = []
    for item in items:
        flat = normalize_engine(item, region)
        name = _field(flat, "name", default=None) or _field(flat, "id")
        engines = _field(flat, "total_instance")
        used = _field(flat, "used_instance")
        instances = "-"
        if engines not in (None, "-"):
            instances = str(engines)
            if used not in (None, "-"):
                instances = "%s/%s" % (used, engines)
        lines.append(
            "%s  (id: %s, type: %s, version: %s, status: %s, instances: %s, region: %s)"
            % (name,
               _field(flat, "id"),
               _field(flat, "type"),
               _field(flat, "version"),
               _field(flat, "status"),
               instances,
               _field(flat, "region"))
        )
    return lines


# --- SDK fallback -----------------------------------------------------------

# Explicit allowlist of environment variable names that may carry AK/SK.
# Only these exact names are read; os.environ is never enumerated, so unrelated
# HUAWEI_*/HW_*/HWC_* variables (tokens, regions, endpoints ...) are never
# harvested or exposed.
AK_ENV_VARS = (
    "HUAWEI_ACCESS_KEY",
    "HUAWEI_AK",
    "HW_ACCESS_KEY",
    "HW_AK",
    "HWC_ACCESS_KEY",
    "HWC_AK",
    "HUAWEICLOUD_SDK_AK",
    "CLOUD_SDK_AK",
)
SK_ENV_VARS = (
    "HUAWEI_SECRET_KEY",
    "HUAWEI_SK",
    "HW_SECRET_KEY",
    "HW_SK",
    "HWC_SECRET_KEY",
    "HWC_SK",
    "HUAWEICLOUD_SDK_SK",
    "CLOUD_SDK_SK",
)


def _env_credential(names):
    """Return the first non-empty value from an explicit allowlist of names."""
    for name in names:
        value = os.environ.get(name)
        if value:
            return value
    return None


def _sdk_item_to_dict(item):
    if isinstance(item, dict):
        return dict(item)
    try:
        return item.to_dict()
    except AttributeError:
        return dict(item) if item else {}


def list_engines_via_sdk(region, engine_type="ALL", project_id=None,
                         limit=DEFAULT_PAGE_SIZE, max_pages=MAX_PAGES):
    """SDK fallback: query CSE engines through huaweicloudsdkcse.

    The official package exposes ``list_engines`` in module ``v1`` while the
    REST path is the v2 ``/v2/{project_id}/enginemgr/engines`` endpoint; the
    same call is what KooCLI issues. Credentials are read explicitly from a
    fixed allowlist of standard AK/SK environment variable names because
    ``BasicCredentials`` performs no environment auto-discovery.
    """
    try:
        from huaweicloudsdkcore.auth.credentials import BasicCredentials
        from huaweicloudsdkcore.region.region import Region
        from huaweicloudsdkcore.http.http_config import HttpConfig
        from huaweicloudsdkcse.v1 import CseClient, ListEnginesRequest
        from huaweicloudsdkcse.v1.region.cse_region import CseRegion
    except ImportError as exc:
        raise ConfigError(
            "未找到 hcloud（KooCLI），且 CSE SDK（huaweicloudsdkcse）未安装，"
            "无法回退到 SDK。请安装 KooCLI 或 pip install huaweicloudsdkcore "
            "huaweicloudsdkcse。详情：%s" % exc
        )

    ak = _env_credential(AK_ENV_VARS)
    sk = _env_credential(SK_ENV_VARS)
    if not ak or not sk:
        raise ConfigError(
            "SDK 回退缺少 AK/SK 凭证：官方 SDK 的 BasicCredentials 不会自动读取环境"
            "变量，且当前环境未检测到受支持的 AK/SK 环境变量（%s / %s）。"
            "请在会话外设置 HUAWEI_ACCESS_KEY / HUAWEI_SECRET_KEY（严禁在对话中粘贴"
            " AK/SK），参见 references/cli-installation-guide.md。"
            % (" / ".join(AK_ENV_VARS), " / ".join(SK_ENV_VARS))
        )
    credentials = BasicCredentials(ak=ak, sk=sk)  # env-sourced, never literals
    if project_id:
        credentials.with_project_id(project_id)
    try:
        try:
            region_obj = CseRegion.value_of(region)
        except (ValueError, KeyError, AttributeError):
            region_obj = Region(region,
                                "https://cse.%s.myhuaweicloud.com" % region)
        client = CseClient.new_builder() \
            .with_credentials(credentials) \
            .with_region(region_obj) \
            .with_http_config(HttpConfig.get_default_config()) \
            .build()
    except Exception as exc:  # region unknown / config broken
        raise ConfigError(
            "SDK 初始化失败（region=%s）：%s。请检查 huaweicloudsdkcse 安装与区域配置。"
            % (region, exc)
        )

    items = []
    offset = 0
    for _ in range(max_pages):
        request = ListEnginesRequest(
            offset=offset, limit=str(limit), type=engine_type)
        try:
            response = client.list_engines(request)
        except Exception as exc:
            blob = str(exc)
            if _looks_like_auth(blob):
                raise auth_error(blob)
            if _looks_like_network(blob):
                raise ApiError("网络异常：SDK 调用 CSE 失败。详情：%s" % blob[:300])
            raise ApiError("SDK 调用失败：%s" % blob[:300])
        batch = [_sdk_item_to_dict(item)
                 for item in (getattr(response, "data", None) or [])]
        items.extend(batch)
        total = getattr(response, "total", None)
        if total is not None and len(items) >= total:
            break
        if len(batch) < limit:
            break
        offset += len(batch)
    else:
        raise ApiError("翻页超过 %d 页仍未取完，已中止以防死循环。" % max_pages)
    return items


# --- Orchestration ----------------------------------------------------------

def _collect(region, engine_type="ALL", project_id=None,
             limit=DEFAULT_PAGE_SIZE, max_pages=MAX_PAGES):
    """Fetch all pages (KooCLI first, SDK fallback when hcloud is absent)."""
    items = []
    offset = 0
    for _page in range(max_pages):
        argv = build_command(region, engine_type=engine_type,
                             project_id=project_id, limit=limit, offset=offset)
        try:
            stdout, stderr, returncode = run_hcloud(argv)
        except ConfigError:
            # hcloud binary missing → one-shot SDK fallback (no CLI retry).
            return list_engines_via_sdk(
                region, engine_type=engine_type, project_id=project_id,
                limit=limit, max_pages=max_pages,
            )
        if returncode != 0 or _USE_ERROR_MARKER in (stdout + " " + stderr).lower():
            raise classify_hcloud_failure(stdout, stderr, returncode)
        payload = extract_json(stdout)
        error = error_from_payload(payload)
        if error is not None:
            raise error
        batch, _total = extract_engines(payload)
        items.extend(batch)
        if not _has_more(batch, len(items), limit, payload):
            break
        offset += len(batch) if batch else limit
    else:
        raise ApiError("翻页超过 %d 页仍未取完，已中止以防死循环。" % max_pages)
    return items


def list_cse_engines(region=DEFAULT_REGION, engine_type="ALL", name=None,
                     fuzzy=False, project_id=None,
                     limit=DEFAULT_PAGE_SIZE, max_pages=MAX_PAGES):
    """Query the CSE engine list (paged) and apply the client-side name filter."""
    items = _collect(region, engine_type=engine_type, project_id=project_id,
                     limit=limit, max_pages=max_pages)
    return filter_by_name(items, name, fuzzy=fuzzy)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="查询华为云 CSE 微服务引擎列表（KooCLI 只读 ListEngines）。")
    parser.add_argument("-r", "--region", default=DEFAULT_REGION,
                        help="目标 Region（默认 %s）" % DEFAULT_REGION)
    parser.add_argument("--type", dest="engine_type", default="ALL",
                        type=normalize_engine_type, choices=ENGINE_TYPES,
                        help="引擎类型：ALL/CSE/Nacos/MicroGateway（默认 ALL）")
    parser.add_argument("--name",
                        help="按名称过滤（客户端，默认精确匹配，大小写不敏感）")
    parser.add_argument("--fuzzy", action="store_true",
                        help="--name 使用子串（模糊）匹配")
    parser.add_argument("--project-id", dest="project_id",
                        help="项目 ID（省略时使用 KooCLI 配置的默认项目）")
    parser.add_argument("--table", action="store_true",
                        help="输出完整字段表格（默认输出简洁清单）")
    parser.add_argument("--json", action="store_true", dest="as_json",
                        help="以 JSON 输出归一化后的引擎清单")
    parser.add_argument("--page-size", type=int, default=DEFAULT_PAGE_SIZE,
                        dest="page_size",
                        help="分页大小（默认 %d）" % DEFAULT_PAGE_SIZE)
    parser.add_argument("--operation", default=None,
                        help="hcloud 操作名（仅允许只读 ListEngines）")

    # Guard runs on the RAW argv before argparse so a mutating flag is reported
    # as a guard violation rather than an argparse error. Filter/selector
    # *values* are read data and deliberately not scanned.
    try:
        guard_write_intent(guard_text_from_argv(argv))
    except CseListError as exc:
        print("[错误] %s" % exc, file=sys.stderr)
        return 1

    args = parser.parse_args(argv)

    try:
        guard_operation(args.operation or OPERATION)
        items = list_cse_engines(
            args.region,
            engine_type=args.engine_type,
            name=args.name,
            fuzzy=args.fuzzy,
            project_id=args.project_id,
            limit=args.page_size,
        )
    except CseListError as exc:
        print("[错误] %s" % exc, file=sys.stderr)
        return 1
    except Exception as exc:  # never leak a traceback to the caller
        print("[错误] 未预期的失败：%s" % exc, file=sys.stderr)
        return 1

    scope = "region=%s，type=%s" % (args.region, args.engine_type)
    if args.name:
        scope += "，name%s=%s" % ("~" if args.fuzzy else "=", args.name)

    if args.as_json:
        print(json.dumps([normalize_engine(item, args.region) for item in items],
                         ensure_ascii=False, indent=2))
        return 0

    if not items:
        print("未找到微服务引擎（%s）。" % scope)
        return 0

    if args.table:
        print("CSE 微服务引擎（%s，共 %d 个，完整字段）：" % (scope, len(items)))
        print(render_table(items, args.region))
        return 0

    print("CSE 微服务引擎（%s，共 %d 个）：" % (scope, len(items)))
    for line in item_summary_lines(items, args.region):
        print("- %s" % line)
    return 0


if __name__ == "__main__":
    sys.exit(main())