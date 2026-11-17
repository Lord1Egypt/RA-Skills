#!/usr/bin/env python3
"""List Huawei Cloud GaussDB(for MySQL) instances via KooCLI

Primary execution path is KooCLI
`hcloud GaussDB ListGaussMySqlInstances` (official read-only
`GET /v3/{project_id}/instances`). When the hcloud binary is absent the script
falls back to the official `huaweicloudsdkgaussdb` v3 SDK
(`GaussDBClient.list_gauss_my_sql_instances`).

The skill is strictly read-only: a write-intent guard rejects any mutating
GaussDB intent (create / delete / resize / restart / backup ...) and any
operation other than `ListGaussMySqlInstances` before a single command runs.

Output modes:
  * default / --table  aligned Chinese-header table
                       (名称/ID/状态/引擎版本/规格/存储/可用区等)
  * --json             raw instance array as returned by the API
  * --format md        Markdown table written to a file (--output FILE),
                       default name gaussdb_instances_<region>_<timestamp>.md

Filters:
  * --name     server-side fuzzy query (a leading ``*`` is added when missing)
  * --status   client-side exact match (the real API has no status parameter)
  * --region   region override (default cn-north-4)

Usage:
    python3 scripts/list_gaussdb.py [--region cn-north-4]
                                    [--table | --json]
                                    [--format table|md] [-o/--output FILE]
                                    [--name gauss-demo] [--status ACTIVE]
                                    [--page-size 100] [--project-id <id>]
                                    [--operation ListGaussMySqlInstances]

Environment overrides (mostly for tests):
    GAUSSDB_LIST_HCLOUD_BIN   hcloud executable (default "hcloud")
    GAUSSDB_LIST_HCLOUD_ARGS  extra args injected before the operation
"""

import argparse
import datetime
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
MAX_PAGE_SIZE = 100
MAX_PAGES = 100
DEFAULT_OUTPUT_TEMPLATE = "gaussdb_instances_%s_%s.md"
SERVICE = "GaussDB"
ALLOWED_OPERATION = "ListGaussMySqlInstances"
REST_PATH = "/v3/{project_id}/instances"

MODE_TABLE = "table"
MODE_JSON = "json"
MODE_MD = "md"

# Fixed, human-friendly table columns. Nested SDK/CLI fields are flattened by
# normalize_instance() before rendering.
TABLE_COLUMNS = (
    ("名称", "name"),
    ("实例ID", "id"),
    ("状态", "status"),
    ("引擎", "engine_type"),
    ("引擎版本", "engine_version"),
    ("内核版本", "kernel_version"),
    ("规格", "flavor_ref"),
    ("CPU/内存", "cpu_mem"),
    ("存储类型", "volume_type"),
    ("存储(GB)", "volume_size"),
    ("私网IP", "private_ips"),
    ("公网IP", "public_ips"),
    ("端口", "port"),
    ("类型", "type"),
    ("区域", "region"),
    ("VPC", "vpc_id"),
    ("子网", "subnet_id"),
    ("创建时间", "created"),
)
# Markdown table columns: header label -> normalized key (same field order as
# the terminal table so both outputs stay consistent).
MD_COLUMNS = (
    ("名称", "name"),
    ("实例ID", "id"),
    ("状态", "status"),
    ("引擎", "engine_type"),
    ("引擎版本", "engine_version"),
    ("内核版本", "kernel_version"),
    ("规格", "flavor_ref"),
    ("CPU/内存", "cpu_mem"),
    ("存储类型", "volume_type"),
    ("存储(GB)", "volume_size"),
    ("私网IP", "private_ips"),
    ("公网IP", "public_ips"),
    ("端口", "port"),
    ("类型", "type"),
    ("区域", "region"),
    ("VPC", "vpc_id"),
    ("子网", "subnet_id"),
    ("创建时间", "created"),
)
MISSING = "-"

# Mutating GaussDB operations / intents — strictly rejected by the guard.
WRITE_INTENT_KEYWORDS = (
    "creategaussmysqlinstance",
    "creategaussmysql",
    "createinstance",
    "deletegaussmysqlinstance",
    "deleteinstance",
    "batchdelete",
    "updateinstance",
    "modifyinstance",
    "changegaussmysqlinstancespecification",
    "changespecification",
    "resizeflavor",
    "resize",
    "restartgaussmysqlinstance",
    "restartinstance",
    "reboot",
    "stopinstance",
    "startinstance",
    "shutdown",
    "restore",
    "backup",
    "createdatabase",
    "deletedatabase",
    "createuser",
    "deleteuser",
    "changepassword",
    "resetpassword",
    "bind",
    "unbind",
    "expandvolume",
    "enlarge",
    "reduce",
    "upgrade",
    "downgrade",
    "switchover",
    "failover",
    "create",
    "delete",
    "update",
    "modify",
    "restart",
    "stop",
    "start",
    "destroy",
    "freeze",
    "unfreeze",
    "release",
    "terminate",
)

# Values of these read-only flags are caller data (filters / region / local
# output settings), not GaussDB operations — excluded from the guard scan so a
# status value such as ``CREATING`` never trips the guard.
READ_ONLY_VALUE_FLAGS = frozenset((
    "--region", "-r",
    "--name",
    "--status",
    "--project-id", "--project_id",
    "--page-size",
    "--limit",
    "--offset",
    "--operation",
    "--datastore-type", "--datastore_type",
    "--type",
    "--id",
    "--vpc-id", "--vpc_id",
    "--subnet-id", "--subnet_id",
    "--private-ip", "--private_ip",
    "--format",
    "--output", "-o",
))

_INSTANCE_LIST_KEYS = ("instances", "instance_list", "instance_infos", "instanceInfos")
_TOTAL_KEYS = ("total_count", "total_num", "instance_num", "total")

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
# stdout WITH exit code 0 — the marker is a hard failure even when rc looks 0.
_USE_ERROR_MARKER = "[use_error]"


class GaussdbListError(Exception):
    """Base error for the GaussDB list skill."""


class GuardError(GaussdbListError):
    """A write intent was detected and blocked (skill is read-only)."""


class ConfigError(GaussdbListError):
    """hcloud missing or credentials (AK/SK) not configured."""


class AuthError(GaussdbListError):
    """Authentication/authorization failure (invalid AK/SK or IAM 403)."""


class ApiError(GaussdbListError):
    """hcloud / network / unexpected API failure."""


def _normalize_token(text):
    return re.sub(r"[\s_\-]+", "", str(text).lower())


def guard_write_intent(text):
    """Raise GuardError when ``text`` carries a mutating GaussDB intent."""
    low = _normalize_token(text)
    for keyword in WRITE_INTENT_KEYWORDS:
        if keyword in low:
            raise GuardError(
                "检测到写操作意图（关键词: %s）。本 skill 仅支持只读查询"
                "（GaussDB ListGaussMySqlInstances），创建/删除/规格变更/重启/备份等"
                "变更操作已被守卫拦截。" % keyword
            )
    return False


def guard_operation(operation):
    """Only the read-only ListGaussMySqlInstances operation may be executed."""
    if operation != ALLOWED_OPERATION:
        raise GuardError(
            "不允许的操作 %r：本 skill 仅允许只读操作 %s。"
            % (operation, ALLOWED_OPERATION)
        )
    return True


def guard_argv(argv):
    """Scan the raw argv for write intent, skipping read-only flag values."""
    kept = []
    skip_next = False
    for token in argv:
        if skip_next:
            skip_next = False
            continue
        name = str(token)
        if name in READ_ONLY_VALUE_FLAGS:
            skip_next = True
            continue
        if any(name.startswith(flag + "=") for flag in READ_ONLY_VALUE_FLAGS):
            continue
        kept.append(name)
    return guard_write_intent(" ".join(kept))


def fuzzy_name(value):
    """Return the server-side fuzzy form of a name (leading ``*`` required)."""
    value = str(value)
    return value if value.startswith("*") else "*" + value


def build_command(region, name=None, instance_id=None, datastore_type=None,
                  instance_type=None, vpc_id=None, subnet_id=None,
                  project_id=None, limit=DEFAULT_PAGE_SIZE, offset=0):
    """Build the hcloud GaussDB ListGaussMySqlInstances argv.

    Parameters mirror the real KooCLI help output:
    --cli-region / --project_id / --name / --id / --datastore_type / --type /
    --vpc_id / --subnet_id / --limit (1..100) / --offset.
    """
    argv = [
        SERVICE,
        ALLOWED_OPERATION,
        "--cli-region=%s" % region,
        "--limit=%d" % limit,
        "--offset=%d" % offset,
    ]
    if project_id:
        argv.append("--project_id=%s" % project_id)
    if name:
        argv.append("--name=%s" % fuzzy_name(name))
    if instance_id:
        argv.append("--id=%s" % instance_id)
    if datastore_type:
        argv.append("--datastore_type=%s" % datastore_type)
    if instance_type:
        argv.append("--type=%s" % instance_type)
    if vpc_id:
        argv.append("--vpc_id=%s" % vpc_id)
    if subnet_id:
        argv.append("--subnet_id=%s" % subnet_id)
    return argv


def _hcloud_executable():
    return os.environ.get("GAUSSDB_LIST_HCLOUD_BIN", "hcloud")


def run_hcloud(argv):
    """Execute hcloud and return (stdout, stderr, returncode)."""
    cmd = [_hcloud_executable()]
    extra = os.environ.get("GAUSSDB_LIST_HCLOUD_ARGS", "").split()
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
    """Map an API error body returned with exit code 0 to a domain error."""
    if not isinstance(payload, dict):
        return None
    code = payload.get("error_code")
    msg = payload.get("error_msg") or payload.get("error_message")
    if not code and not msg:
        return None
    detail = "GaussDB API 错误 %s: %s" % (code or "-", msg or "-")
    blob = ("%s %s" % (code or "", msg or "")).lower()
    if any(pattern in blob for pattern in _AUTH_PATTERNS):
        return AuthError(
            "无权限访问 GaussDB（云数据库 GaussDB），请检查 IAM 权限"
            "（403：AK/SK 无效或未授予 GaussDB 只读权限）。详情：%s" % detail
        )
    return ApiError(detail)


def extract_json(stdout):
    """Parse hcloud stdout as JSON, tolerating trailing diagnostic tables."""
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
            "hcloud 参数错误（KooCLI 拒绝了该参数组合，退出码 %s）：GaussDB "
            "ListGaussMySqlInstances 真实参数清单可通过 "
            "`hcloud GaussDB ListGaussMySqlInstances --help` 查看。详情：%s"
            % (returncode, blob[:300])
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
            "无权限访问 GaussDB（云数据库 GaussDB），请检查 IAM 权限"
            "（403：AK/SK 无效或未授予 GaussDB 只读权限）。"
            "参见 references/iam-policies.md。详情：%s" % blob[:300]
        )
    return ApiError(
        "hcloud 调用失败（退出码 %s）：%s" % (returncode, blob[:300])
    )


def extract_instances(payload):
    """Pull the instance list out of a ListGaussMySqlInstances response."""
    if isinstance(payload, list):
        return payload
    if not isinstance(payload, dict):
        return []
    for key in _INSTANCE_LIST_KEYS:
        value = payload.get(key)
        if isinstance(value, list):
            return value
    return []


def _total_count(payload):
    if not isinstance(payload, dict):
        return None
    for key in _TOTAL_KEYS:
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
    for name in names:
        value = os.environ.get(name)
        if value:
            return value
    return None


def resolve_project_id(explicit=None):
    if explicit:
        return explicit
    return _env_value(_PROJECT_ID_ENV_NAMES)


def _jsonable(value):
    return json.loads(json.dumps(value, ensure_ascii=False, default=str))


def list_instances_via_sdk(region, name=None, instance_id=None,
                           datastore_type=None, instance_type=None,
                           vpc_id=None, subnet_id=None, limit=DEFAULT_PAGE_SIZE,
                           project_id=None, max_pages=MAX_PAGES):
    """SDK fallback: query instances through `huaweicloudsdkgaussdb` v3."""
    try:
        from huaweicloudsdkcore.auth.credentials import BasicCredentials
        from huaweicloudsdkcore.region.region import Region
        from huaweicloudsdkcore.http.http_config import HttpConfig
        from huaweicloudsdkgaussdb.v3 import GaussDBClient, ListGaussMySqlInstancesRequest
        from huaweicloudsdkgaussdb.v3.region.gaussdb_region import GaussDBRegion
    except ImportError as exc:
        raise ConfigError(
            "未找到 hcloud（KooCLI），且 huaweicloudsdkcore/huaweicloudsdkgaussdb "
            "未安装，无法回退到 SDK。请安装 KooCLI 或 "
            "pip install huaweicloudsdkcore huaweicloudsdkgaussdb。详情：%s" % exc
        )

    ak = _env_value(_AK_ENV_NAMES)
    sk = _env_value(_SK_ENV_NAMES)
    if not ak or not sk:
        raise ConfigError(
            "SDK 回退缺少 AK/SK 凭证：官方 SDK 的 BasicCredentials 不会自动读取"
            "环境变量，且当前环境未检测到 HW_ACCESS_KEY / HUAWEI_ACCESS_KEY / "
            "HUAWEICLOUD_SDK_AK 形式的 AK/SK 环境变量。请在会话外设置"
            " HUAWEI_ACCESS_KEY / HUAWEI_SECRET_KEY（严禁在对话中粘贴 AK/SK），"
            "参见 references/cli-installation-guide.md。"
        )
    resolved_project_id = resolve_project_id(project_id)
    if not resolved_project_id:
        raise ConfigError(
            "SDK 回退缺少 project_id：GaussDB 的 REST 路径为 %s，需要项目 ID。"
            "请通过 --project-id 传入，或设置 HUAWEICLOUD_SDK_PROJECT_ID / "
            "HUAWEI_PROJECT_ID（严禁在对话中粘贴敏感信息）。" % REST_PATH
        )
    credentials = BasicCredentials(ak=ak, sk=sk, project_id=resolved_project_id)  # env-sourced, never literals
    try:
        try:
            region_obj = GaussDBRegion.value_of(region)
        except (ValueError, KeyError, AttributeError):
            region_obj = Region(region, "https://gaussdb.%s.myhuaweicloud.com" % region)
        client = GaussDBClient.new_builder() \
            .with_credentials(credentials) \
            .with_region(region_obj) \
            .with_http_config(HttpConfig.get_default_config()) \
            .build()
    except Exception as exc:
        raise ConfigError(
            "SDK 初始化失败（region=%s）：%s。请检查 huaweicloudsdkgaussdb 安装与区域配置。"
            % (region, exc)
        )

    instances = []
    offset = 0
    for _ in range(max_pages):
        request = ListGaussMySqlInstancesRequest(
            limit=limit, offset=offset,
            name=fuzzy_name(name) if name else None,
            id=instance_id,
            datastore_type=datastore_type,
            type=instance_type,
            vpc_id=vpc_id,
            subnet_id=subnet_id,
        )
        try:
            response = client.list_gauss_my_sql_instances(request)
        except Exception as exc:
            low = str(exc).lower()
            if any(p in low for p in _AUTH_PATTERNS):
                raise AuthError(
                    "无权限访问 GaussDB（云数据库 GaussDB），请检查 IAM 权限（403）。"
                    "详情：%s" % str(exc)[:300]
                )
            raise ApiError("SDK 调用失败：%s" % str(exc)[:300])
        batch = list(response.instances or [])
        instances.extend(_jsonable(instance.to_dict()) for instance in batch)
        total = getattr(response, "total_count", None)
        if total is not None and len(instances) >= total:
            break
        if len(batch) < limit:
            break
        offset += len(batch)
    else:
        raise ApiError("翻页超过 %d 页仍未取完，已中止以防死循环。" % max_pages)
    return instances


def list_instances(region, name=None, instance_id=None, datastore_type=None,
                   instance_type=None, vpc_id=None, subnet_id=None,
                   limit=DEFAULT_PAGE_SIZE, project_id=None,
                   max_pages=MAX_PAGES):
    """Query all GaussDB instances (offset-paged); KooCLI first, SDK fallback."""
    instances = []
    offset = 0
    for _page in range(max_pages):
        argv = build_command(region, name=name, instance_id=instance_id,
                             datastore_type=datastore_type,
                             instance_type=instance_type, vpc_id=vpc_id,
                             subnet_id=subnet_id, project_id=project_id,
                             limit=limit, offset=offset)
        try:
            stdout, stderr, returncode = run_hcloud(argv)
        except ConfigError:
            # hcloud binary missing → one-shot SDK fallback (no CLI retry).
            return list_instances_via_sdk(
                region, name=name, instance_id=instance_id,
                datastore_type=datastore_type, instance_type=instance_type,
                vpc_id=vpc_id, subnet_id=subnet_id, limit=limit,
                project_id=project_id, max_pages=max_pages,
            )
        if returncode != 0 or _USE_ERROR_MARKER in (stdout + " " + stderr).lower():
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


def _join(values):
    if isinstance(values, list):
        cells = [str(v) for v in values if v not in (None, "")]
        return ",".join(cells) if cells else MISSING
    if values in (None, ""):
        return MISSING
    return str(values)


def normalize_instance(instance):
    """Flatten nested GaussDB fields into a table-friendly dict."""
    flat = dict(instance) if isinstance(instance, dict) else {}

    datastore = flat.get("datastore") if isinstance(flat.get("datastore"), dict) else {}
    volume = flat.get("volume") if isinstance(flat.get("volume"), dict) else {}
    flavor_info = flat.get("flavor_info") if isinstance(flat.get("flavor_info"), dict) else {}

    cpu = flavor_info.get("vcpus")
    ram = flavor_info.get("ram")
    if cpu is not None and ram is not None:
        cpu_mem = "%sC%sGB" % (cpu, ram)
    else:
        cpu_mem = MISSING

    normalized = {
        "name": flat.get("name"),
        "id": flat.get("id") or flat.get("instance_id"),
        "status": flat.get("status"),
        "engine_type": datastore.get("type") or flat.get("datastore_type"),
        "engine_version": datastore.get("version"),
        "kernel_version": datastore.get("kernel_version"),
        "flavor_ref": flat.get("flavor_ref"),
        "cpu_mem": cpu_mem,
        "volume_type": volume.get("type"),
        "volume_size": volume.get("size"),
        "private_ips": _join(flat.get("private_ips")),
        "public_ips": _join(flat.get("public_ips")),
        "port": flat.get("port"),
        "type": flat.get("type"),
        "region": flat.get("region"),
        "vpc_id": flat.get("vpc_id"),
        "subnet_id": flat.get("subnet_id"),
        "created": flat.get("created"),
    }
    return normalized


def _cell(value):
    if value is None or value == "":
        return MISSING
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return str(value)


def render_table(instances):
    """Render the default aligned table with fixed Chinese headers."""
    rows_data = [normalize_instance(instance) for instance in instances]
    headers = [header for header, _key in TABLE_COLUMNS]
    rows = [[_cell(row.get(key)) for _header, key in TABLE_COLUMNS]
            for row in rows_data]
    widths = []
    for i, header in enumerate(headers):
        width = len(header)
        for row in rows:
            # CJK characters are wide; approximate with 2 columns each.
            width = max(width, _display_width(row[i]))
        widths.append(width)
    lines = [_pad_row(headers, widths), "  ".join("-" * w for w in widths)]
    for row in rows:
        lines.append(_pad_row(row, widths))
    return "\n".join(lines)


def _display_width(text):
    width = 0
    for char in str(text):
        width += 2 if _is_wide(char) else 1
    return width


def _is_wide(char):
    code = ord(char)
    return (
        0x1100 <= code <= 0x115F
        or 0x2E80 <= code <= 0xA4CF
        or 0xAC00 <= code <= 0xD7A3
        or 0xF900 <= code <= 0xFAFF
        or 0xFE30 <= code <= 0xFE4F
        or 0xFF00 <= code <= 0xFF60
        or 0xFFE0 <= code <= 0xFFE6
    )


def _pad_row(cells, widths):
    padded = []
    for i, cell in enumerate(cells):
        pad = widths[i] - _display_width(cell)
        padded.append(str(cell) + " " * max(pad, 0))
    return "  ".join(padded).rstrip()


def _md_cell(value):
    """Render one Markdown table cell, escaping pipes and collapsing newlines."""
    if value is None:
        value = MISSING
    if isinstance(value, (dict, list)):
        value = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    text = str(value)
    text = text.replace("\r\n", " ").replace("\n", " ").replace("\r", " ")
    text = text.replace("|", "\\|")
    return text or MISSING


def render_markdown(instances, region, generated_at=None):
    """Render the instance list as a Markdown document (title + table).

    Columns follow MD_COLUMNS (中文列头); every instance is normalized first so
    nested ``datastore`` / ``volume`` / ``flavor_info`` / IP fields render as
    flat cells. The 区域 cell falls back to the queried region when the API
    response carries no ``region`` field.

    An empty instance list still produces a valid document: the table header +
    separator followed by an explicit "no instances" note (never an error).
    """
    rows_data = [normalize_instance(instance) for instance in instances]
    header = "| " + " | ".join(label for label, _key in MD_COLUMNS) + " |"
    separator = "| " + " | ".join("---" for _label, _key in MD_COLUMNS) + " |"
    lines = [
        "# 华为云 GaussDB 实例列表 — %s" % region,
        "",
        "> Region: %s | Instances: %d" % (region, len(rows_data)),
    ]
    if generated_at:
        lines.append("> Generated at: %s" % generated_at)
    lines += ["", header, separator]
    for row in rows_data:
        cells = []
        for _label, key in MD_COLUMNS:
            value = row.get(key)
            if key == "region" and value in (None, ""):
                value = region
            cells.append(_md_cell(value))
        lines.append("| " + " | ".join(cells) + " |")
    if not rows_data:
        lines += ["", "_当前区域（%s）无 GaussDB 实例。_" % region]
    lines.append("")
    return "\n".join(lines)


def default_output_path(region, now=None):
    """Default Markdown file name: gaussdb_instances_<region>_<timestamp>.md."""
    stamp = (now or datetime.datetime.now(datetime.timezone.utc)).strftime(
        "%Y%m%dT%H%M%SZ")
    return os.path.join(os.getcwd(), DEFAULT_OUTPUT_TEMPLATE % (region, stamp))


def write_markdown(content, output_path):
    """Write ``content`` to ``output_path`` atomically (temp file + rename).

    Missing parent directories are created. An interrupted write never leaves a
    corrupt / partial file behind.
    """
    directory = os.path.dirname(os.path.abspath(output_path))
    try:
        os.makedirs(directory, exist_ok=True)
        tmp_fd, tmp_path = tempfile.mkstemp(prefix=".gaussdb-md-", suffix=".tmp",
                                            dir=directory)
    except (OSError, ValueError) as exc:
        raise ApiError("Markdown 文件写出失败（目录 %s 不可创建）：%s"
                       % (directory, exc))
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


def filter_by_status(instances, status):
    """Client-side exact status filter (case-insensitive)."""
    if not status:
        return instances
    wanted = str(status).strip().lower()
    return [
        instance for instance in instances
        if str(_field(instance, "status", default="")).strip().lower() == wanted
    ]


def _field(instance, key, default=MISSING):
    if isinstance(instance, dict):
        value = instance.get(key)
        if value not in (None, ""):
            return value
    return default


def _empty_hint(region, args):
    filters = []
    if args.name:
        filters.append("name=%s" % args.name)
    if args.status:
        filters.append("status=%s" % args.status)
    if getattr(args, "instance_id", None):
        filters.append("id=%s" % args.instance_id)
    suffix = "（过滤条件: %s）" % ", ".join(filters) if filters else ""
    return "当前区域（%s）无 GaussDB 实例%s。" % (region, suffix)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="查询华为云 GaussDB（云数据库 GaussDB for MySQL）实例列表"
                    "（KooCLI hcloud GaussDB ListGaussMySqlInstances，只读）。")
    parser.add_argument("-r", "--region", default=DEFAULT_REGION,
                        help="目标 Region（默认 %s）" % DEFAULT_REGION)
    parser.add_argument("--table", action="store_true", dest="as_table",
                        help="输出表格（默认即表格模式）")
    parser.add_argument("--json", action="store_true", dest="as_json",
                        help="以 JSON 输出原始实例数组")
    parser.add_argument("--name",
                        help="按实例名称过滤（服务端模糊查询；缺少前导 * 时自动补 *）")
    parser.add_argument("--status",
                        help="按实例状态过滤（本地过滤，大小写不敏感，如 ACTIVE）")
    parser.add_argument("--id", dest="instance_id",
                        help="按实例 ID 过滤（服务端查询参数）")
    parser.add_argument("--datastore-type", dest="datastore_type",
                        help="按数据库类型过滤（服务端查询参数，目前仅 gaussdb-mysql）")
    parser.add_argument("--type", dest="instance_type",
                        help="按实例类型过滤（服务端查询参数，目前仅 Cluster）")
    parser.add_argument("--vpc-id", dest="vpc_id", help="按 VPC ID 过滤（服务端查询参数）")
    parser.add_argument("--subnet-id", dest="subnet_id", help="按子网 ID 过滤（服务端查询参数）")
    parser.add_argument("--page-size", type=int, default=DEFAULT_PAGE_SIZE,
                        dest="page_size",
                        help="分页大小（默认 %d，范围 1~%d，自动翻页取全量）"
                             % (DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE))
    parser.add_argument("--project-id", dest="project_id",
                        help="项目 ID（可选；SDK 回退在 /v3/{project_id}/instances 路径中需要）")
    parser.add_argument("--operation", default=ALLOWED_OPERATION,
                        help="hcloud GaussDB 操作名（仅允许只读 %s）" % ALLOWED_OPERATION)
    parser.add_argument("--format", dest="export_format",
                        choices=(MODE_TABLE, MODE_MD), default=MODE_TABLE,
                        help="输出格式：table（默认，终端表格）或 md"
                             "（Markdown 文件，配合 --output）")
    parser.add_argument("-o", "--output", default=None,
                        help="Markdown 输出文件路径（隐含 --format md；默认当前目录 "
                             "gaussdb_instances_<region>_<timestamp>.md）")
    args = parser.parse_args(argv)

    if args.output:
        args.export_format = MODE_MD
    if args.export_format == MODE_MD and args.as_json:
        parser.error("--format md / --output 与 --json 不能同时使用")
    if args.export_format == MODE_MD and args.as_table:
        parser.error("--format md / --output 与 --table 不能同时使用")

    try:
        guard_argv(argv if argv is not None else sys.argv[1:])
        guard_operation(args.operation)
        for value in (args.name, args.status, args.instance_id,
                      args.datastore_type, args.instance_type,
                      args.vpc_id, args.subnet_id):
            if value:
                # Read filter values are caller data, not operations; only the
                # operation name and free-form tokens are guard-scanned above.
                pass
        if args.page_size is None or args.page_size < 1 or args.page_size > MAX_PAGE_SIZE:
            raise ApiError("--page-size 超出范围（1~%d）：%s"
                           % (MAX_PAGE_SIZE, args.page_size))
        instances = list_instances(
            args.region,
            name=args.name,
            instance_id=args.instance_id,
            datastore_type=args.datastore_type,
            instance_type=args.instance_type,
            vpc_id=args.vpc_id,
            subnet_id=args.subnet_id,
            limit=args.page_size,
            project_id=args.project_id,
        )
    except GaussdbListError as exc:
        print("[错误] %s" % exc, file=sys.stderr)
        return 1

    instances = filter_by_status(instances, args.status)

    if args.as_json:
        print(json.dumps(instances, ensure_ascii=False, indent=2))
        return 0

    if args.export_format == MODE_MD:
        output_path = args.output or default_output_path(args.region)
        generated_at = datetime.datetime.now(datetime.timezone.utc).strftime(
            "%Y-%m-%dT%H:%M:%SZ")
        try:
            content = render_markdown(instances, args.region, generated_at)
            write_markdown(content, output_path)
        except GaussdbListError as exc:
            print("[错误] %s" % exc, file=sys.stderr)
            return 1
        if instances:
            print("已生成 Markdown 文件：%s（Region %s，共 %d 个 GaussDB 实例）。"
                  % (os.path.abspath(output_path), args.region, len(instances)))
        else:
            print("已生成 Markdown 文件：%s（Region %s 无 GaussDB 实例，已输出表头与"
                  "空表提示）。" % (os.path.abspath(output_path), args.region))
        return 0

    if not instances:
        print(_empty_hint(args.region, args))
        return 0

    print("Region %s 的 GaussDB 实例列表（共 %d 个）：" % (args.region, len(instances)))
    print(render_table(instances))
    return 0


if __name__ == "__main__":
    sys.exit(main())