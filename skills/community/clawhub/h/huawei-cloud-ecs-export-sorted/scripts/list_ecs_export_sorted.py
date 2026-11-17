#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""List Huawei Cloud ECS instances (read-only), sort them locally, and export a
report as xlsx / csv / json / table.

Brings the ECS instance-list query paradigm (KooCLI
``hcloud ECS ListServersDetails`` — official read-only GET
``/v1/{project_id}/cloudservers/detail``) together with a **local** sorting
layer and a local export. When the hcloud binary is absent, the script falls
back to the official ``huaweicloudsdkecs`` v2 SDK
(``EcsClient.list_servers_details``).

Sorting runs entirely on the locally fetched result set: ``ListServersDetails``
has no server-side ordering parameter, so ``--sort-by`` maps a friendly field
name to a normalized record key and ``--order`` picks ascending / descending.
Numeric fields (vCPU / 内存) compare numerically, ``created`` compares as a
timestamp, the rest compare case-insensitively as text; records whose sort key
is missing or unparseable are always placed last (regardless of ``--order``).

A strict write-intent guard rejects any mutating ECS intent so writes never
happen: the only operation ever constructed is read-only
``hcloud ECS ListServersDetails`` (or the SDK ``list_servers_details``
fallback). No data is ever written back to the cloud — the report file is
produced on the local filesystem only.

Usage:
    python3 scripts/list_ecs_export_sorted.py [--region cn-north-4]
                                              [--format xlsx|csv|json|table]
                                              [--sort-by name] [--order asc|desc]
                                              [--output /path/out.xlsx]
                                              [--summary] [--status ACTIVE]
                                              [--name ecs-web] [--page-size 100]

Environment overrides (mostly for tests):
    ECS_EXPORT_SORTED_HCLOUD_BIN   hcloud executable (default "hcloud")
    ECS_EXPORT_SORTED_HCLOUD_ARGS  extra args appended AFTER the read-only
                                   ``ECS ListServersDetails`` arguments
                                   (guard-scanned, read-only)
"""

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime

# Keep the shipped skill directory clean: never emit __pycache__/*.pyc when
# this script (or its tests) import the bundled export module.
sys.dont_write_bytecode = True

from export_report import (
    ExportError,
    REPORT_HEADERS,
    default_output_path,
    export_csv,
    export_xlsx,
)

DEFAULT_REGION = "cn-north-4"
DEFAULT_PAGE_SIZE = 100
DEFAULT_FORMAT = "xlsx"
DEFAULT_ORDER = "asc"
SERVICE = "ECS"
ALLOWED_OPERATION = "ListServersDetails"

# Mutating ECS operations / intents — strictly rejected by the guard.
# Read-only vocabulary (list/show/get/describe) never matches.
WRITE_INTENT_KEYWORDS = (
    "createserver",
    "createservers",
    "deleteserver",
    "deleteservers",
    "updateserver",
    "modifyserver",
    "rebuildserver",
    "resizeserver",
    "serveraction",
    "batchaction",
    "startserver",
    "stopserver",
    "restartserver",
    "rebootserver",
    "resetserver",
    "migrateserver",
    "lockserver",
    "unlockserver",
    "attachvolume",
    "detachvolume",
    "createservergroup",
    "deleteservergroup",
    "batchstart",
    "batchstop",
    "batchreboot",
    "addservergroup",
    "delete",
    "create",
    "update",
    "modify",
    "restart",
    "reboot",
    "resize",
    "rebuild",
    "migrate",
    "attach",
    "detach",
    "start",
    "stop",
    "shutdown",
    "reset",
    "destroy",
    "restore",
    "terminate",
)

# Read-only option flags whose *values* are filter/output data (e.g. an
# instance named "restart-me", the ECS status "REBUILD", a sort field, or a
# report path such as "ecs-delete-report.xlsx"). Their values must NOT be
# scanned by the write-intent guard. The `--operation` value is intentionally
# NOT excluded: it is validated by `guard_operation()` and also scanned.
_VALUE_STRIPPED_FLAGS = (
    "--region",
    "-r",
    "--status",
    "--name",
    "--page-size",
    "--output",
    "-o",
    "--sort-by",
    "-s",
    "--order",
)

# Friendly sort-field aliases → normalized record key.
SORT_FIELD_ALIASES = {
    "name": "name",
    "id": "id",
    "status": "status",
    "flavor": "flavor",
    "vcpus": "vcpus",
    "vcpu": "vcpus",
    "ram": "ram",
    "memory": "ram",
    "availability_zone": "availability_zone",
    "az": "availability_zone",
    "created": "created",
    "created_at": "created",
    "privateips": "privateIps",
    "private_ips": "privateIps",
    "publicips": "publicIps",
    "public_ips": "publicIps",
    "名称": "name",
    "实例名": "name",
    "状态": "status",
    "规格": "flavor",
    "vcpu": "vcpus",
    "内存": "ram",
    "可用区": "availability_zone",
    "创建时间": "created",
    "私网ip": "privateIps",
    "公网ip": "publicIps",
}
SORT_FIELDS_HELP = (
    "name / id / status / flavor / vcpus / ram / availability_zone / "
    "created / privateIps / publicIps"
)

# Numeric and timestamp sort keys; everything else compares as lowercased text.
_NUMERIC_SORT_FIELDS = ("vcpus", "ram")
_DATETIME_SORT_FIELDS = ("created",)

# Preferred column order for the table view; remaining keys are appended sorted.
PREFERRED_COLUMNS = [
    "name",
    "id",
    "status",
    "flavor",
    "vcpus",
    "ram",
    "availability_zone",
    "privateIps",
    "publicIps",
    "created",
    "image_id",
    "key_name",
    "updated",
    "enterprise_project_id",
    "tags",
    "host_id",
]

_SERVER_LIST_KEYS = ("servers", "server_list", "servers_detail", "serverInfos")

# AK/SK environment variable names, read *directly* (never by enumerating
# os.environ). The official SDK's BasicCredentials does not auto-discover
# credentials, so the fallback path resolves them explicitly.
_AK_ENV_NAMES = (
    "HUAWEI_ACCESS_KEY",
    "HW_ACCESS_KEY",
    "HWC_ACCESS_KEY",
    "HUAWEICLOUD_SDK_AK",
    "HUAWEI_CLOUD_ACCESS_KEY",
)
_SK_ENV_NAMES = (
    "HUAWEI_SECRET_KEY",
    "HW_SECRET_KEY",
    "HWC_SECRET_KEY",
    "HUAWEICLOUD_SDK_SK",
    "HUAWEI_CLOUD_SECRET_KEY",
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
# stdout WITH exit code 0 — the marker is treated as a hard failure.
_USE_ERROR_MARKER = "[use_error]"


class EcsExportError(Exception):
    """Base error for the ECS instance-list sorted export skill."""


class GuardError(EcsExportError):
    """A write intent was detected and blocked (skill is read-only)."""


class ConfigError(EcsExportError):
    """hcloud/SDK missing or credentials (AK/SK) not configured."""


class AuthError(EcsExportError):
    """Authentication/authorization failure (invalid AK/SK or IAM 403)."""


class ApiError(EcsExportError):
    """hcloud / network / unexpected API failure."""


class SortError(EcsExportError):
    """The requested --sort-by field is unknown."""


def guard_write_intent(text):
    """Raise GuardError if ``text`` carries a mutating intent.

    Normalizes separators so ``--create-server``, ``CreateServers``, and
    ``create_server`` all hit the same keyword. Read-only vocabulary
    (list/show/get/describe) never matches.
    """
    low = re.sub(r"[\s_\-]+", "", str(text).lower())
    for keyword in WRITE_INTENT_KEYWORDS:
        if keyword in low:
            raise GuardError(
                "检测到写操作意图（关键词: %s）。本 skill 仅支持只读查询"
                "（ECS ListServersDetails）并在本机生成报表，"
                "创建/删除/启停/重启/变配等操作已被守卫拦截。" % keyword
            )
    return False


def guard_operation(operation):
    """Only the read-only ListServersDetails operation may be executed."""
    if operation != ALLOWED_OPERATION:
        raise GuardError(
            "不允许的操作 %r：本 skill 仅允许只读操作 %s。"
            % (operation, ALLOWED_OPERATION)
        )
    return True


def guard_text_from_argv(argv):
    """Build the text the write-intent guard should scan.

    Scans flag names and positional tokens, but strips the values of the
    read-only / local-output flags (``--status`` / ``--name`` / ``--region`` /
    ``--page-size`` / ``--sort-by`` / ``--order`` / ``--output`` / ``-o`` /
    ``-s`` / ``-r``): those are pure read / file-path data and may
    legitimately contain write-looking words.

    A *flag* following such an option is never swallowed: a following token
    that starts with ``-`` is still scanned, so a mutating flag cannot hide
    behind a value-stripped option.
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
                # This token is the filter/output value — strip it.
                continue
        kept.append(tok)
    return " ".join(kept)


def build_command(region, status=None, name=None,
                  limit=DEFAULT_PAGE_SIZE, offset=0):
    """Build the hcloud ECS ListServersDetails argv (without the executable).

    Mirrors the real KooCLI parameter list: --cli-region / --limit / --offset /
    --status / --name. Both --status and --name are real server-side ECS query
    parameters (verified against ``huaweicloudsdkecs`` v2
    ``ListServersDetailsRequest.openapi_types``).
    """
    argv = [
        SERVICE,
        ALLOWED_OPERATION,
        "--cli-region=%s" % region,
        "--limit=%d" % limit,
        "--offset=%d" % offset,
    ]
    if status:
        argv.append("--status=%s" % status)
    if name:
        argv.append("--name=%s" % name)
    return argv


def _hcloud_executable():
    return os.environ.get("ECS_EXPORT_SORTED_HCLOUD_BIN", "hcloud")


def run_hcloud(argv):
    """Execute hcloud and return (stdout, stderr, returncode).

    Extra args from ``ECS_EXPORT_SORTED_HCLOUD_ARGS`` are appended *after* the
    read-only ``ECS ListServersDetails`` argv (they can never rewrite the
    service/operation) and are guard-scanned for write intent first.
    """
    cmd = [_hcloud_executable()]
    cmd.extend(argv)
    extra = os.environ.get("ECS_EXPORT_SORTED_HCLOUD_ARGS", "").split()
    if extra:
        guard_write_intent(" ".join(extra))
        cmd.extend(extra)
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
            "hcloud 参数错误（KooCLI 拒绝了该参数组合，退出码 %s）：ECS ListServersDetails "
            "真实参数清单可通过 `hcloud ECS ListServersDetails --help` 查看。"
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
            "无权限访问 ECS，请检查 IAM 权限（403：AK/SK 无效或未授予 ECS 只读权限），"
            "参见 references/iam-policies.md。详情：%s" % blob[:300]
        )
    return ApiError(
        "hcloud 调用失败（退出码 %s）：%s" % (returncode, blob[:300])
    )


def extract_servers(payload):
    """Pull the server list out of a ListServersDetails response."""
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        for key in _SERVER_LIST_KEYS:
            value = payload.get(key)
            if isinstance(value, list):
                return value
    return []


def _payload_total(payload):
    if not isinstance(payload, dict):
        return None
    for key in ("count", "total_count", "totalCount", "total"):
        value = payload.get(key)
        if isinstance(value, int) and not isinstance(value, bool):
            return value
    return None


def _has_more(batch, collected, limit, payload):
    if not batch:
        return False
    total = _payload_total(payload)
    if total is not None and total >= 0:
        return collected < total
    return len(batch) >= limit


def _env_credential(names):
    """Return the first non-empty value among the explicitly named env vars."""
    for name in names:
        value = os.environ.get(name)
        if value:
            return value
    return None


def _to_jsonable(value):
    """Recursively convert SDK model objects into JSON-native Python values.

    The huaweicloud SDK ``to_dict()`` keeps nested model objects as-is for
    ``dict``-typed attributes (e.g. ``ServerDetail.addresses`` stays a mapping
    of network name → ``list[ServerAddress]``), so the result is *not* JSON
    serializable and ``json.dumps`` raised ``TypeError: Object of type
    ServerAddress is not JSON serializable``. Any object exposing ``to_dict``
    is expanded recursively; anything else non-native degrades to ``str`` so
    the value can always be serialized.
    """
    if value is None or isinstance(value, (str, bool, int, float)):
        return value
    if isinstance(value, dict):
        return {str(key): _to_jsonable(val) for key, val in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_to_jsonable(item) for item in value]
    to_dict = getattr(value, "to_dict", None)
    if callable(to_dict):
        try:
            return _to_jsonable(to_dict())
        except Exception:
            pass
    return str(value)


def sdk_server_to_dict(server):
    """Convert a ``huaweicloudsdkecs`` ServerDetail into wire-name-keyed dict.

    The SDK ``to_dict()`` emits Python attribute names (``access_i_pv4``,
    ``os_ext_a_zavailability_zone``); the KooCLI/OpenAPI JSON uses wire names
    (``accessIPv4``, ``OS-EXT-AZ:availability_zone``). Remapping through the
    official ``ServerDetail.attribute_map`` keeps both execution paths
    producing the same shape.

    Nested SDK model objects (notably the ``ServerAddress`` entries under
    ``addresses``) are recursively expanded to plain dicts via
    :func:`_to_jsonable`, so the fallback path yields records that
    ``json.dumps`` / the table renderer can handle.
    """
    if isinstance(server, dict):
        raw = _to_jsonable(dict(server))
    else:
        try:
            raw = _to_jsonable(server.to_dict())
        except AttributeError:
            return _to_jsonable(dict(server))
    if not isinstance(raw, dict):
        return {}
    try:
        from huaweicloudsdkecs.v2 import ServerDetail
        attr_map = ServerDetail.attribute_map
    except Exception:
        attr_map = {}
    out = {}
    attr_keys = set(attr_map.keys())
    for attr, wire in attr_map.items():
        if attr in raw and raw[attr] is not None:
            out[wire] = raw[attr]
    for key, value in raw.items():
        if key not in attr_keys and key not in out and value is not None:
            out[key] = value
    return out


def list_servers_via_sdk(region, status=None, name=None,
                         limit=DEFAULT_PAGE_SIZE, max_pages=100):
    """SDK fallback: query servers through ``huaweicloudsdkecs`` v2.

    Only invoked when hcloud is not installed. Credentials are taken from the
    explicitly named AK/SK environment variables (never passed as literals).
    """
    ak = _env_credential(_AK_ENV_NAMES)
    sk = _env_credential(_SK_ENV_NAMES)
    if not ak or not sk:
        raise ConfigError(
            "SDK 回退缺少 AK/SK 凭证：官方 SDK 的 BasicCredentials 不会自动读取环境"
            "变量，且当前环境未检测到 HUAWEI_ACCESS_KEY / HUAWEI_SECRET_KEY 形式的"
            " AK/SK 环境变量。请在会话外设置（严禁在对话中粘贴 AK/SK）；若同时未安装"
            " SDK，请先运行 `python3 scripts/ensure_env.py`。参见 "
            "references/cli-installation-guide.md。"
        )
    try:
        from huaweicloudsdkcore.auth.credentials import BasicCredentials
        from huaweicloudsdkcore.region.region import Region
        from huaweicloudsdkcore.http.http_config import HttpConfig
        from huaweicloudsdkecs.v2 import EcsClient, ListServersDetailsRequest
        from huaweicloudsdkecs.v2.region.ecs_region import EcsRegion
    except ImportError as exc:
        raise ConfigError(
            "未找到 hcloud（KooCLI），且 huaweicloudsdkcore/huaweicloudsdkecs 未安装，"
            "无法回退到 SDK。请安装 KooCLI 或先运行 "
            "`python3 scripts/ensure_env.py`（pip install huaweicloudsdkcore "
            "huaweicloudsdkecs）。详情：%s" % exc
        )
    credentials = BasicCredentials(ak, sk)  # env-sourced values, never literals
    try:
        try:
            region_obj = EcsRegion.value_of(region)
        except (ValueError, KeyError, AttributeError):
            region_obj = Region(region, "https://ecs.%s.myhuaweicloud.com" % region)
        client = EcsClient.new_builder() \
            .with_credentials(credentials) \
            .with_region(region_obj) \
            .with_http_config(HttpConfig.get_default_config()) \
            .build()
    except Exception as exc:  # region unknown / config broken
        raise ConfigError(
            "SDK 初始化失败（region=%s）：%s。请检查 huaweicloudsdkecs 安装与区域配置。"
            % (region, exc)
        )
    servers = []
    offset = 0
    for _ in range(max_pages):
        request = ListServersDetailsRequest(
            limit=limit, offset=offset, name=name, status=status,
        )
        try:
            response = client.list_servers_details(request)
        except Exception as exc:
            low = str(exc).lower()
            if any(p in low for p in _AUTH_PATTERNS):
                raise AuthError(
                    "无权限访问 ECS，请检查 IAM 权限（403）。详情：%s" % str(exc)[:300]
                )
            raise ApiError("SDK 调用失败：%s" % str(exc)[:300])
        batch = list(response.servers or [])
        servers.extend(sdk_server_to_dict(server) for server in batch)
        total = getattr(response, "count", None)
        if total is not None and len(servers) >= total:
            break
        if len(batch) < limit:
            break
        offset += len(batch)
    else:
        raise ApiError("翻页超过 %d 页仍未取完，已中止以防死循环。" % max_pages)
    return servers


def list_servers(region, status=None, name=None,
                 limit=DEFAULT_PAGE_SIZE, max_pages=100):
    """Query all ECS servers (paged); KooCLI first, SDK fallback."""
    servers = []
    offset = 0
    for _page in range(max_pages):
        argv = build_command(region, status=status, name=name,
                             limit=limit, offset=offset)
        try:
            stdout, stderr, returncode = run_hcloud(argv)
        except ConfigError:
            # hcloud binary missing → one-shot SDK fallback (no CLI retry).
            servers = list_servers_via_sdk(
                region, status=status, name=name,
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
        offset += len(batch) if batch else limit
    else:
        raise ApiError("翻页超过 %d 页仍未取完，已中止以防死循环。" % max_pages)
    return servers


def _extract_ips(addresses):
    """Split a ServerDetail ``addresses`` map into (private_ips, public_ips)."""
    private, public = [], []
    addresses = _to_jsonable(addresses)
    if not isinstance(addresses, dict):
        return private, public
    for entries in addresses.values():
        if not isinstance(entries, list):
            continue
        for entry in entries:
            if not isinstance(entry, dict):
                continue
            addr = entry.get("addr") or entry.get("ip_address")
            if not addr:
                continue
            ip_type = (entry.get("OS-EXT-IPS:type")
                       or entry.get("os_ext_ip_stype")
                       or entry.get("type"))
            if ip_type and "float" in str(ip_type).lower():
                public.append(str(addr))
            else:
                private.append(str(addr))
    return private, public


def normalize_server(server):
    """Flatten nested flavor / addresses / AZ fields into sortable keys.

    The incoming record is deep-converted to JSON-native types first
    (:func:`_to_jsonable`): the SDK fallback may hand over a ``ServerDetail``
    model — or a plain dict still holding nested ``ServerAddress`` models in
    ``addresses`` — and ``dict(model)`` / ``json.dumps`` would otherwise raise
    ``TypeError: Object of type ServerAddress is not JSON serializable``.
    """
    server = _to_jsonable(server)
    if not isinstance(server, dict):
        server = {}
    flat = dict(server)
    flavor = server.get("flavor")
    if isinstance(flavor, dict):
        flat["flavor"] = flavor.get("name") or flavor.get("id") or "-"
        flat.setdefault("vcpus", flavor.get("vcpus", "-"))
        flat.setdefault("ram", flavor.get("ram", "-"))
    elif flavor is None:
        flat["flavor"] = "-"
    az = (server.get("OS-EXT-AZ:availability_zone")
          or server.get("os_ext_a_zavailability_zone")
          or server.get("availability_zone"))
    flat["availability_zone"] = az or "-"
    private, public = _extract_ips(server.get("addresses"))
    flat["privateIps"] = ",".join(private) if private else "-"
    public_ips = list(public)
    access_v4 = server.get("accessIPv4") or server.get("access_i_pv4")
    if access_v4 and str(access_v4) not in public_ips:
        public_ips.insert(0, str(access_v4))
    flat["publicIps"] = ",".join(public_ips) if public_ips else "-"
    image = server.get("image")
    if isinstance(image, dict):
        flat.setdefault("image_id", image.get("id", "-"))
    flat.setdefault("created", server.get("created") or "-")
    return flat


def _field(server, *names, default="-"):
    for name in names:
        if name in server and server[name] not in (None, ""):
            return server[name]
    return default


def active_filter_descriptions(status=None, name=None, sort_by=None, order=None):
    """Human-readable description of the filters / ordering actually applied."""
    filters = []
    if status:
        filters.append("status=%s" % status)
    if name:
        filters.append("name=%s" % name)
    if sort_by:
        filters.append("sort-by=%s order=%s" % (sort_by, order))
    return filters


def resolve_sort_field(sort_by):
    """Map a friendly ``--sort-by`` value to a normalized record key.

    Raises SortError with the list of accepted fields when unknown.
    """
    if sort_by is None:
        return None
    key = SORT_FIELD_ALIASES.get(str(sort_by).strip().lower())
    if key is None:
        raise SortError(
            "未知的排序字段 %r。可用字段：%s（也支持对应中文别名）。"
            % (sort_by, SORT_FIELDS_HELP)
        )
    return key


def _sort_key_value(server, key):
    """Return (valid, comparable) for one record's sort key.

    ``valid=False`` marks a missing / unparseable value; such records are
    always placed last. Numeric and timestamp fields are compared natively,
    text fields compare case-insensitively.
    """
    raw = server.get(key)
    if raw is None or raw == "" or raw == "-":
        return False, None
    if key in _NUMERIC_SORT_FIELDS:
        try:
            return True, float(str(raw).strip())
        except (TypeError, ValueError):
            return False, None
    if key in _DATETIME_SORT_FIELDS:
        text = str(raw).strip()
        try:
            return True, datetime.fromisoformat(text.replace("Z", "+00:00"))
        except ValueError:
            return True, text.lower()
    return True, str(raw).lower()


def sort_servers(servers, sort_by=None, order=DEFAULT_ORDER):
    """Sort normalized records locally; invalid sort keys always go last.

    When ``sort_by`` is None the query order is preserved. The sort is stable,
    so records sharing a key keep their original relative order. Non-dict
    records (e.g. a ``ServerDetail`` SDK model) are deep-converted first so a
    model object never reaches ``.get()`` / ``dict()``.
    """
    key = resolve_sort_field(sort_by)
    if key is None:
        return list(servers)
    if order not in ("asc", "desc"):
        raise SortError("未知的排序方向 %r（仅支持 asc / desc）。" % order)
    servers = [s if isinstance(s, dict) else _to_jsonable(s) for s in servers]
    valid, invalid = [], []
    for server in servers:
        ok, _value = _sort_key_value(server, key)
        (valid if ok else invalid).append(server)
    valid.sort(key=lambda s: _sort_key_value(s, key)[1],
               reverse=(order == "desc"))
    return valid + invalid


def _cell(value):
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return str(value)


def render_table(servers):
    """Render full-field table output (union of all returned fields)."""
    rows_data = [normalize_server(server) for server in servers]
    columns = []
    for key in PREFERRED_COLUMNS:
        if any(key in s for s in rows_data):
            columns.append(key)
    for key in sorted({k for s in rows_data for k in s}):
        if key not in columns:
            columns.append(key)
    if not columns:
        columns = ["name", "id"]
    rows = [[_cell(_field(s, col)) for col in columns] for s in rows_data]
    widths = [max(len(col), *(len(row[i]) for row in rows)) for i, col in enumerate(columns)]
    header = "  ".join(col.ljust(widths[i]) for i, col in enumerate(columns))
    separator = "  ".join("-" * w for w in widths)
    lines = [header, separator]
    for row in rows:
        lines.append("  ".join(row[i].ljust(widths[i]) for i in range(len(columns))))
    return "\n".join(lines)


def parse_args(argv):
    parser = argparse.ArgumentParser(
        description="查询华为云 ECS 实例列表，按指定字段本地排序后导出报表（只读）。")
    parser.add_argument("-r", "--region", default=DEFAULT_REGION,
                        help="目标 Region（默认 %s）" % DEFAULT_REGION)
    parser.add_argument("-f", "--format", default=DEFAULT_FORMAT,
                        choices=["table", "json", "xlsx", "csv"],
                        help="输出格式：xlsx（默认）/ csv / json / table")
    parser.add_argument("-o", "--output", default=None,
                        help="报表输出路径（xlsx/csv；默认 "
                             "ecs_instances_<region>_<timestamp>.<ext>）")
    parser.add_argument("-s", "--sort-by", default=None, dest="sort_by",
                        help="本地排序字段：%s（缺省保持查询原序）" % SORT_FIELDS_HELP)
    parser.add_argument("--order", default=DEFAULT_ORDER,
                        choices=["asc", "desc"],
                        help="排序方向：asc（默认，升序）/ desc（降序）")
    parser.add_argument("--summary", action="store_true",
                        help="xlsx/csv 报表末尾追加汇总行（实例数量）")
    parser.add_argument("--status",
                        help="按实例状态过滤（ACTIVE/BUILD/ERROR/SHUTOFF/REBUILD/"
                             "RESIZE 等；为 ECS ListServersDetails 服务端参数）")
    parser.add_argument("--name", help="按实例名称过滤（服务端参数，模糊匹配）")
    parser.add_argument("--page-size", type=int, default=DEFAULT_PAGE_SIZE,
                        dest="page_size", help="分页大小（默认 %d）" % DEFAULT_PAGE_SIZE)
    parser.add_argument("--operation", default=ALLOWED_OPERATION,
                        help="hcloud ECS 操作名（仅允许只读 %s）" % ALLOWED_OPERATION)
    return parser.parse_args(argv)


def main(argv=None):
    raw_argv = argv if argv is not None else sys.argv[1:]

    # Write-intent guard runs on the RAW argv BEFORE argparse, so that a
    # mutating flag (e.g. `--create-server`) is reported as a guard violation
    # instead of an argparse "unrecognized argument" error. Filter/output
    # values are read-only data and deliberately not scanned.
    try:
        guard_write_intent(guard_text_from_argv(raw_argv))
    except EcsExportError as exc:
        print("[错误] %s" % exc, file=sys.stderr)
        return 1

    args = parse_args(argv)

    try:
        guard_operation(args.operation)
        # Validate the sort field up front so an unknown field fails fast,
        # before any cloud query is issued.
        sort_key = resolve_sort_field(args.sort_by)
        servers = list_servers(
            args.region,
            status=args.status,
            name=args.name,
            limit=args.page_size,
        )
        # Normalize before sorting: the flattened sort keys (vcpus / ram /
        # availability_zone / privateIps / publicIps) only exist on normalized
        # records, so sorting the raw wire records silently ignored them.
        normalized = [normalize_server(server) for server in servers]
        normalized = sort_servers(normalized, args.sort_by, args.order)
    except EcsExportError as exc:
        print("[错误] %s" % exc, file=sys.stderr)
        return 1

    servers = normalized
    filters = active_filter_descriptions(
        status=args.status, name=args.name,
        sort_by=args.sort_by if sort_key else None, order=args.order)
    filter_suffix = "（%s）" % ", ".join(filters) if filters else ""
    fmt = args.format

    if fmt == "json":
        print(json.dumps(normalized, ensure_ascii=False, indent=2))
        return 0

    if fmt == "table":
        if not servers:
            print("当前区域（%s）无 ECS 实例%s。" % (args.region, filter_suffix))
            return 0
        print("Region %s 的 ECS 实例列表（共 %d 个%s）："
              % (args.region, len(servers), filter_suffix))
        print(render_table(servers))
        return 0

    # xlsx / csv: empty instance list → friendly hint, never a broken file.
    if not normalized:
        print("当前区域（%s）无 ECS 实例%s，未生成报表文件。"
              % (args.region, filter_suffix))
        return 0

    extension = "csv" if fmt == "csv" else "xlsx"
    output_path = args.output or default_output_path(args.region, extension)
    try:
        if fmt == "csv":
            written = export_csv(normalized, output_path,
                                 summary=args.summary, region=args.region)
        else:
            written = export_xlsx(normalized, output_path,
                                  summary=args.summary, region=args.region)
    except ExportError as exc:
        print("[错误] %s" % exc, file=sys.stderr)
        return 1

    print("已生成 ECS 实例列表 %s 报表（Region %s，共 %d 个实例%s）：%s"
          % (fmt.upper(), args.region, len(normalized), filter_suffix, written))
    return 0


if __name__ == "__main__":
    sys.exit(main())