#!/usr/bin/env python3
"""List Huawei Cloud ECS instances via KooCLI `hcloud ECS ListServersDetails` (read-only GET).

Primary execution path is KooCLI; when hcloud is not installed, the script falls
back to the official `huaweicloudsdkecs` v2 SDK (`list_servers_details`). Reads
nothing but the active credential profile / environment. Supports three stdout
modes (table / --json / --names-only), --status / --name server-side filters,
offset paging, and a strict write-intent guard: any argument that looks like a
mutating ECS operation is rejected before a single command is executed. Output
goes to stdout only — the script never writes a file.

Usage:
    python3 scripts/list_ecs.py [--region cn-north-4] [--json | --names-only]
                                 [--status ACTIVE] [--name ecs-web]
                                 [--page-size 100]
                                 [--operation ListServersDetails]

Environment overrides (mostly for tests):
    ECS_LIST_HCLOUD_BIN   hcloud executable (default "hcloud")
    ECS_LIST_HCLOUD_ARGS  extra args injected before the ECS operation
"""

import argparse
import json
import os
import re
import subprocess
import sys

DEFAULT_REGION = "cn-north-4"
DEFAULT_PAGE_SIZE = 100
SERVICE = "ECS"
ALLOWED_OPERATION = "ListServersDetails"

# Mutating ECS operations / intents — strictly rejected by the guard.
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

# Read-only option flags whose *values* are filter data (e.g. an instance named
# "restart-me", or the ECS status value "REBUILD"). Their values must NOT be
# scanned by the write-intent guard, otherwise legitimate read filters such as
# `--status REBUILD` / `--status RESIZE` would be rejected. The `--operation`
# value is intentionally NOT excluded: it is validated by `guard_operation()`
# and also scanned, as defense in depth.
_VALUE_STRIPPED_FLAGS = (
    "--region",
    "-r",
    "--status",
    "--name",
    "--page-size",
)

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
    "image_id",
    "key_name",
    "created",
    "updated",
    "enterprise_project_id",
    "tags",
    "host_id",
]

_SERVER_LIST_KEYS = ("servers", "server_list", "servers_detail", "serverInfos")

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


class EcsListError(Exception):
    """Base error for the ECS list skill."""


class GuardError(EcsListError):
    """A write intent was detected and blocked (skill is read-only)."""


class ConfigError(EcsListError):
    """hcloud missing or credentials (AK/SK) not configured."""


class AuthError(EcsListError):
    """Authentication/authorization failure (invalid AK/SK or IAM 403)."""


class ApiError(EcsListError):
    """hcloud / network / unexpected API failure."""


def guard_write_intent(text):
    """Raise GuardError if `text` carries a mutating intent.

    Normalizes separators so `--create-server`, `CreateServers`, and
    `create_server` all hit the same keyword. Read-only vocabulary
    (list/show/get/describe) never matches.
    """
    low = re.sub(r"[\s_\-]+", "", str(text).lower())
    for keyword in WRITE_INTENT_KEYWORDS:
        if keyword in low:
            raise GuardError(
                "检测到写操作意图（关键词: %s）。本 skill 仅支持只读查询"
                "（ECS ListServersDetails），创建/删除/启停/重启/变配等变更操作已被守卫拦截。" % keyword
            )
    return False


def guard_operation(operation):
    """Only the read-only ListServersDetails operation may be executed."""
    if operation != ALLOWED_OPERATION:
        raise GuardError(
            "不允许的操作 %r：本 skill 仅允许只读操作 %s。" % (operation, ALLOWED_OPERATION)
        )
    return True


def guard_text_from_argv(argv):
    """Build the text the write-intent guard should scan.

    Scans flag names and positional tokens, but strips the values of the
    read-only filter flags (`--status` / `--name` / `--region` / `--page-size`):
    those are pure read data and may legitimately contain write-looking words
    (e.g. the ECS status value `REBUILD` or an instance named `restart-me`).

    A *flag* following such an option is never swallowed: skipping the next
    token unconditionally would let `--status --create-server` hide a mutating
    flag from the guard.
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

    Mirrors the real KooCLI parameter list (`hcloud ECS ListServersDetails
    --help`): --cli-region / --limit / --offset / --status / --name. Both
    --status and --name are real server-side ECS query parameters (verified
    against `huaweicloudsdkecs` v2 `ListServersDetailsRequest.openapi_types`).
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
    return os.environ.get("ECS_LIST_HCLOUD_BIN", "hcloud")


def run_hcloud(argv):
    """Execute hcloud and return (stdout, stderr, returncode)."""
    cmd = [_hcloud_executable()]
    extra = os.environ.get("ECS_LIST_HCLOUD_ARGS", "").split()
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


def to_jsonable(value):
    """Recursively convert `value` into JSON-serializable primitives.

    The official `huaweicloudsdkecs` model `to_dict()` does not recurse into
    every container: a `ServerDetail.addresses` value is a *dict of lists* of
    `ServerAddress` model objects, and the objects inside those inner lists
    survive `to_dict()` untouched. Such objects are not JSON-serializable and
    crash `json.dumps` (TypeError: Object of type ServerAddress is not JSON
    serializable). This helper normalizes any nested structure: SDK models are
    converted via their own `to_dict()`, containers are rebuilt element-wise,
    and anything else non-primitive degrades to `str()` (never raises).
    """
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, dict):
        return {key: to_jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [to_jsonable(item) for item in value]
    to_dict = getattr(value, "to_dict", None)
    if callable(to_dict):
        try:
            return to_jsonable(to_dict())
        except Exception:
            return str(value)
    return str(value)


def sdk_server_to_dict(server):
    """Convert a `huaweicloudsdkecs` ServerDetail into wire-name-keyed dict.

    The SDK `to_dict()` emits Python attribute names (`access_i_pv4`,
    `os_ext_a_zavailability_zone`); the KooCLI/OpenAPI JSON uses wire names
    (`accessIPv4`, `OS-EXT-AZ:availability_zone`). Remapping through the
    official `ServerDetail.attribute_map` keeps both execution paths producing
    the same shape.
    """
    if isinstance(server, dict):
        raw = dict(server)
    else:
        try:
            raw = server.to_dict()
        except AttributeError:
            return dict(server)
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
            out[wire] = to_jsonable(raw[attr])
    for key, value in raw.items():
        if key not in attr_keys and key not in out and value is not None:
            out[key] = to_jsonable(value)
    return out


def list_servers_via_sdk(region, status=None, name=None,
                         limit=DEFAULT_PAGE_SIZE, max_pages=100):
    """SDK fallback: query servers through `huaweicloudsdkecs` v2.

    Only invoked when hcloud is not installed. Credentials are taken from the
    whitelisted AK/SK environment variables (HW_*/HUAWEI_ACCESS_KEY family) —
    never passed as literals here. The official SDK has no env-var auto-discovery on
    `BasicCredentials()`, so AK/SK must be read explicitly. Region resolution
    uses the SDK's own `EcsRegion` catalog (official endpoints, no guessing),
    falling back to an explicit `Region(id, endpoint)` for custom regions.
    """
    try:
        from huaweicloudsdkcore.auth.credentials import BasicCredentials
        from huaweicloudsdkcore.region.region import Region
        from huaweicloudsdkcore.http.http_config import HttpConfig
        from huaweicloudsdkecs.v2 import EcsClient, ListServersDetailsRequest
        from huaweicloudsdkecs.v2.region.ecs_region import EcsRegion
    except ImportError as exc:
        raise ConfigError(
            "未找到 hcloud（KooCLI），且 huaweicloudsdkcore/huaweicloudsdkecs 未安装，"
            "无法回退到 SDK。请安装 KooCLI 或 pip install huaweicloudsdkcore "
            "huaweicloudsdkecs。详情：%s" % exc
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
    credentials = BasicCredentials(ak=ak, sk=sk)  # env-sourced, never literals
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
    """Query all ECS servers (paged); KooCLI first, SDK fallback.

    `status` and `name` are real ECS ListServersDetails server-side query
    parameters and are forwarded to both execution paths.
    """
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
    """Split a ServerDetail `addresses` map into (private_ips, public_ips)."""
    private, public = [], []
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
    """Flatten nested flavor / addresses / AZ fields into table-friendly keys."""
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
    return flat


def _field(server, *names, default="-"):
    for name in names:
        if name in server and server[name] not in (None, ""):
            return server[name]
    return default


def server_names(servers):
    names = []
    for server in servers:
        name = _field(server, "name", "instance_name", default=None)
        if name is None:
            name = _field(server, "id", "server_id")
        names.append(str(name))
    return names


def server_summary_lines(servers):
    """Compact `name  (id: ...)` lines for the --names-only inventory mode."""
    lines = []
    for server in servers:
        name = _field(server, "name", "instance_name", default=None)
        if name is None:
            name = _field(server, "id", "server_id")
        sid = _field(server, "id", "server_id", default="-")
        lines.append("%s  (id: %s)" % (name, sid))
    return lines


def active_filter_descriptions(status=None, name=None):
    """Human-readable description of the server-side filters actually applied."""
    filters = []
    if status:
        filters.append("status=%s" % status)
    if name:
        filters.append("name=%s" % name)
    return filters


def _cell(value):
    if isinstance(value, (dict, list, tuple)):
        # Normalize first: a container may still hold a non-serializable SDK
        # model object (defense in depth — the SDK path already normalizes).
        try:
            return json.dumps(to_jsonable(value), ensure_ascii=False,
                              separators=(",", ":"))
        except (TypeError, ValueError):
            return str(value)
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


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="查询华为云 ECS 实例列表（KooCLI hcloud ECS ListServersDetails，只读）。")
    parser.add_argument("-r", "--region", default=DEFAULT_REGION,
                        help="目标 Region（默认 %s）" % DEFAULT_REGION)
    parser.add_argument("--json", action="store_true", dest="as_json",
                        help="以 JSON 输出完整原始字段")
    parser.add_argument("--names-only", action="store_true", dest="names_only",
                        help="仅输出精简实例名称+ID 清单")
    parser.add_argument("--status",
                        help="按实例状态过滤（ACTIVE/BUILD/ERROR/SHUTOFF/REBUILD/"
                             "RESIZE 等；为 ECS ListServersDetails 服务端参数）")
    parser.add_argument("--name", help="按实例名称过滤（服务端参数，模糊匹配）")
    parser.add_argument("--page-size", type=int, default=DEFAULT_PAGE_SIZE,
                        dest="page_size", help="分页大小（默认 %d）" % DEFAULT_PAGE_SIZE)
    parser.add_argument("--operation", default=ALLOWED_OPERATION,
                        help="hcloud ECS 操作名（仅允许只读 %s）" % ALLOWED_OPERATION)

    # Write-intent guard runs on the RAW argv before argparse, so that a
    # mutating flag (e.g. `--create-server`) is reported as a guard violation
    # instead of an argparse "unrecognized argument" error. Filter *values*
    # (status/name) are read-only data and deliberately not scanned — they may
    # contain write-looking words (e.g. the ECS status `REBUILD`).
    try:
        guard_write_intent(guard_text_from_argv(argv))
    except EcsListError as exc:
        print("[错误] %s" % exc, file=sys.stderr)
        return 1

    args = parser.parse_args(argv)

    try:
        guard_operation(args.operation)
        servers = list_servers(
            args.region,
            status=args.status,
            name=args.name,
            limit=args.page_size,
        )
    except EcsListError as exc:
        print("[错误] %s" % exc, file=sys.stderr)
        return 1

    filters = active_filter_descriptions(status=args.status, name=args.name)
    filter_suffix = "（过滤条件: %s）" % ", ".join(filters) if filters else ""

    if args.as_json:
        # Normalize before serialization: never leak an SDK model object
        # (e.g. ServerAddress nested in `addresses`) into json.dumps.
        print(json.dumps(to_jsonable(servers), ensure_ascii=False, indent=2))
    elif args.names_only:
        print("Region %s 的 ECS 实例清单（共 %d 个）：" % (args.region, len(servers)))
        for line in server_summary_lines(servers):
            print("- %s" % line)
    elif not servers:
        print("当前区域（%s）无 ECS 实例%s。" % (args.region, filter_suffix))
    else:
        print("Region %s 的 ECS 实例列表（共 %d 个，完整字段）："
              % (args.region, len(servers)))
        print(render_table(servers))

    return 0


if __name__ == "__main__":
    sys.exit(main())
