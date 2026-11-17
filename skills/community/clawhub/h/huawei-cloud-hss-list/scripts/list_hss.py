#!/usr/bin/env python3
"""List Huawei Cloud HSS (Host Security Service) protected hosts via KooCLI.

Primary execution path is KooCLI (`hcloud HSS ListHostStatus`, read-only
GET /v5/{project_id}/host-management/hosts); when hcloud is not installed the
script falls back to the official `huaweicloudsdkhss` v5 SDK
(`HssClient.list_host_status`). Reads nothing but the active credential
profile / environment. Supports three output modes
(table / --json / --names-only), real server-side filters
(--host-name / --host-id / --agent-status / --host-status / --protect-status /
--os-type / --ip-addr / --version / --enterprise-project-id), offset paging,
and a strict write-intent guard: any mutating HSS argument is rejected before
a single command is executed.

Usage:
    python3 scripts/list_hss.py [--region cn-north-4] [--json | --names-only]
                                [--host-name <name>] [--host-id <id>]
                                [--agent-status online|offline|not_installed]
                                [--host-status ACTIVE|SHUTOFF|BUILDING|ERROR]
                                [--protect-status closed|opened|protection_exception]
                                [--os-type Linux|Windows] [--ip-addr <ip>]
                                [--version hss.version.basic|...]
                                [--enterprise-project-id <id>]
                                [--page-size 10] [--project-id <id>]
                                [--operation ListHostStatus]

Environment overrides (mostly for tests):
    HSS_LIST_HCLOUD_BIN   hcloud executable (default "hcloud")
    HSS_LIST_HCLOUD_ARGS  extra args injected before the HSS operation
"""

import argparse
import json
import os
import re
import subprocess
import sys

DEFAULT_REGION = "cn-north-4"
DEFAULT_PAGE_SIZE = 10
SERVICE = "HSS"
ALLOWED_OPERATION = "ListHostStatus"
REST_PATH = "/v5/{project_id}/host-management/hosts"

# Mutating HSS operations / intents — strictly rejected by the guard.
WRITE_INTENT_KEYWORDS = (
    "create",
    "delete",
    "update",
    "modify",
    "change",
    "add",
    "remove",
    "associate",
    "disassociate",
    "attach",
    "detach",
    "bind",
    "unbind",
    "release",
    "restart",
    "installagent",
    "uninstallagent",
    "upgradeagent",
    "activatehost",
    "cancelhostsquota",
    "quarantine",
    "isolate",
    "kill",
    "unlock",
    "recover",
    "ignoreevent",
    "changeevent",
    "changerealstatus",
    "batchupdate",
)

# Preferred column order for the table view; remaining keys are appended sorted.
PREFERRED_COLUMNS = [
    "host_name",
    "private_ip",
    "public_ip",
    "os_name",
    "os_type",
    "host_status",
    "agent_status",
    "version",
    "protect_status",
    "detect_result",
    "group_name",
    "enterprise_project_name",
    "host_id",
    "agent_id",
    "asset_value",
]

_HOST_LIST_KEYS = ("data_list", "host_list")

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
    "not authorized",
    "forbidden",
    "apigw.0301",
    "common.01010013",
    "认证失败",
    "权限不足",
    "permission denied",
)

# KooCLI prints usage errors (e.g. "[USE_ERROR]Invalid parameter: xxx") on
# stdout WITH exit code 0 — the marker must be treated as a hard failure even
# when the return code looks successful.
_USE_ERROR_MARKER = "[use_error]"


class HssListError(Exception):
    """Base error for the HSS list skill."""


class GuardError(HssListError):
    """A write intent was detected and blocked (skill is read-only)."""


class ConfigError(HssListError):
    """hcloud missing or credentials (AK/SK) not configured."""


class AuthError(HssListError):
    """Authentication/authorization failure (invalid AK/SK or IAM 403)."""


class ApiError(HssListError):
    """hcloud / network / unexpected API failure."""


def guard_write_intent(text):
    """Raise GuardError if `text` carries a mutating intent.

    Normalizes separators so `--create-host`, `CreateHost`, and `create_host`
    all hit the same keyword. Read-only vocabulary (list/show/get/describe)
    never matches.
    """
    low = re.sub(r"[\s_\-]+", "", str(text).lower())
    for keyword in WRITE_INTENT_KEYWORDS:
        if keyword in low:
            raise GuardError(
                "检测到写操作意图（关键词: %s）。本 skill 仅支持只读查询"
                "（HSS ListHostStatus），安装/卸载/修改/隔离/删除等变更操作已被守卫拦截。"
                % keyword
            )
    return False


def guard_operation(operation):
    """Only the read-only ListHostStatus operation may be executed."""
    if operation != ALLOWED_OPERATION:
        raise GuardError(
            "不允许的操作 %r：本 skill 仅允许只读操作 %s。"
            % (operation, ALLOWED_OPERATION)
        )
    return True


def build_command(region, host_name=None, host_id=None, agent_status=None,
                  host_status=None, protect_status=None, os_type=None,
                  ip_addr=None, version=None, enterprise_project_id=None,
                  limit=DEFAULT_PAGE_SIZE, offset=0):
    """Build the hcloud HSS ListHostStatus argv (without the executable).

    Mirrors the real KooCLI parameter list for the read-only HSS
    ListHostStatus operation: --cli-region / --limit / --offset and the real
    server-side filters. Parameter names are exactly the ones reported by
    `hcloud HSS ListHostStatus --help`.
    """
    argv = [
        SERVICE,
        ALLOWED_OPERATION,
        "--cli-region=%s" % region,
        "--limit=%d" % limit,
        "--offset=%d" % offset,
    ]
    if host_name:
        argv.append("--host_name=%s" % host_name)
    if host_id:
        argv.append("--host_id=%s" % host_id)
    if agent_status:
        argv.append("--agent_status=%s" % agent_status)
    if host_status:
        argv.append("--host_status=%s" % host_status)
    if protect_status:
        argv.append("--protect_status=%s" % protect_status)
    if os_type:
        argv.append("--os_type=%s" % os_type)
    if ip_addr:
        argv.append("--ip_addr=%s" % ip_addr)
    if version:
        argv.append("--version=%s" % version)
    if enterprise_project_id:
        argv.append("--enterprise_project_id=%s" % enterprise_project_id)
    return argv


def _hcloud_executable():
    return os.environ.get("HSS_LIST_HCLOUD_BIN", "hcloud")


def run_hcloud(argv):
    """Execute hcloud and return (stdout, stderr, returncode)."""
    cmd = [_hcloud_executable()]
    extra = os.environ.get("HSS_LIST_HCLOUD_ARGS", "").split()
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
            "hcloud 参数错误（KooCLI 拒绝了该参数组合，退出码 %s）：HSS ListHostStatus "
            "真实参数清单可通过 `hcloud HSS ListHostStatus --help` 查看。"
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
            "无权限访问主机安全服务（HSS），请检查 IAM 权限（403：AK/SK 无效或未授予 "
            "HSS 只读权限 hss:host:listHostStatus），参见 references/iam-policies.md。"
            "详情：%s" % blob[:300]
        )
    return ApiError(
        "hcloud 调用失败（退出码 %s）：%s" % (returncode, blob[:300])
    )


def extract_hosts(payload):
    """Pull the protected-host list out of a ListHostStatus response."""
    if isinstance(payload, list):
        return payload
    for key in _HOST_LIST_KEYS:
        value = payload.get(key)
        if isinstance(value, list):
            return value
    return []


def _total_num(payload):
    """Read total_num from a ListHostStatus response."""
    if not isinstance(payload, dict):
        return None
    return payload.get("total_num")


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


def list_hosts_via_sdk(region, host_name=None, host_id=None, agent_status=None,
                       host_status=None, protect_status=None, os_type=None,
                       ip_addr=None, version=None, enterprise_project_id=None,
                       limit=DEFAULT_PAGE_SIZE, project_id=None, max_pages=100):
    """SDK fallback: query protected hosts through `huaweicloudsdkhss` v5.

    Only invoked when hcloud is not installed. Credentials are taken from the
    whitelisted AK/SK environment variables (HW_*/HUAWEI_ACCESS_KEY family) —
    never passed as literals here. The official SDK has no env-var
    auto-discovery on `BasicCredentials()`, so AK/SK and the project id
    (required by the `/v5/{project_id}/...` path) must be read explicitly.
    Region resolution uses the SDK's own `HssRegion` catalog (official
    endpoints, no guessing), falling back to an explicit `Region(id, endpoint)`.
    Paging uses `limit` + `offset` (max offset 2,000,000).
    """
    try:
        from huaweicloudsdkcore.auth.credentials import BasicCredentials
        from huaweicloudsdkcore.region.region import Region
        from huaweicloudsdkcore.http.http_config import HttpConfig
        from huaweicloudsdkhss.v5 import HssClient, ListHostStatusRequest
        from huaweicloudsdkhss.v5.region.hss_region import HssRegion
    except ImportError as exc:
        raise ConfigError(
            "未找到 hcloud（KooCLI），且 huaweicloudsdkcore/huaweicloudsdkhss 未安装，"
            "无法回退到 SDK。请安装 KooCLI 或 pip install huaweicloudsdkcore "
            "huaweicloudsdkhss。详情：%s" % exc
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
            "SDK 回退缺少 project_id：HSS 的 REST 路径为 %s，需要项目 ID。"
            "请通过 --project-id 传入，或设置 HUAWEICLOUD_SDK_PROJECT_ID / "
            "HUAWEI_PROJECT_ID（严禁在对话中粘贴敏感信息）。" % REST_PATH
        )
    credentials = BasicCredentials(ak=ak, sk=sk, project_id=resolved_project_id)  # env-sourced, never literals
    try:
        try:
            region_obj = HssRegion.value_of(region)
        except (ValueError, KeyError, AttributeError):
            region_obj = Region(region, "https://hss.%s.myhuaweicloud.com" % region)
        client = HssClient.new_builder() \
            .with_credentials(credentials) \
            .with_region(region_obj) \
            .with_http_config(HttpConfig.get_default_config()) \
            .build()
    except Exception as exc:  # region unknown / config broken
        raise ConfigError(
            "SDK 初始化失败（region=%s）：%s。请检查 huaweicloudsdkhss 安装与区域配置。"
            % (region, exc)
        )
    hosts = []
    offset = 0
    for _ in range(max_pages):
        request = ListHostStatusRequest(
            region=region,
            host_name=host_name,
            host_id=host_id,
            agent_status=agent_status,
            host_status=host_status,
            protect_status=protect_status,
            os_type=os_type,
            ip_addr=ip_addr,
            version=version,
            enterprise_project_id=enterprise_project_id,
            limit=limit,
            offset=offset,
        )
        try:
            response = client.list_host_status(request)
        except Exception as exc:
            low = str(exc).lower()
            if any(p in low for p in _AUTH_PATTERNS):
                raise AuthError(
                    "无权限访问主机安全服务（HSS），请检查 IAM 权限（403）。详情：%s"
                    % str(exc)[:300]
                )
            raise ApiError("SDK 调用失败：%s" % str(exc)[:300])
        batch = list(response.data_list or [])
        records = [_jsonable(host.to_dict()) for host in batch]
        hosts.extend(records)
        total = response.total_num if response.total_num is not None else len(records)
        if not batch or len(hosts) >= int(total):
            break
        offset += len(batch)
    return hosts


def list_hosts(region, host_name=None, host_id=None, agent_status=None,
               host_status=None, protect_status=None, os_type=None,
               ip_addr=None, version=None, enterprise_project_id=None,
               limit=DEFAULT_PAGE_SIZE, project_id=None, max_pages=100):
    """Query all protected hosts (offset paged); KooCLI first, SDK fallback."""
    hosts = []
    offset = 0
    for _page in range(max_pages):
        argv = build_command(
            region, host_name=host_name, host_id=host_id,
            agent_status=agent_status, host_status=host_status,
            protect_status=protect_status, os_type=os_type, ip_addr=ip_addr,
            version=version, enterprise_project_id=enterprise_project_id,
            limit=limit, offset=offset,
        )
        try:
            stdout, stderr, returncode = run_hcloud(argv)
        except ConfigError:
            # hcloud binary missing → one-shot SDK fallback (no CLI retry).
            hosts = list_hosts_via_sdk(
                region, host_name=host_name, host_id=host_id,
                agent_status=agent_status, host_status=host_status,
                protect_status=protect_status, os_type=os_type,
                ip_addr=ip_addr, version=version,
                enterprise_project_id=enterprise_project_id,
                limit=limit, project_id=project_id, max_pages=max_pages,
            )
            break
        if returncode != 0 or _USE_ERROR_MARKER in (stdout + " " + stderr).lower():
            # KooCLI usage errors print [USE_ERROR] on stdout with rc=0.
            raise classify_hcloud_failure(stdout, stderr, returncode)
        payload = extract_json(stdout)
        if isinstance(payload, dict) and payload.get("error_code"):
            # Cloud API returns an error envelope with rc=0 (e.g. IAM 403).
            raise classify_hcloud_failure(stdout, "", returncode)
        batch = extract_hosts(payload)
        hosts.extend(batch)
        total = _total_num(payload)
        if not batch or (total is not None and len(hosts) >= int(total)):
            break
        offset += len(batch)
    else:
        raise ApiError("翻页超过 %d 页仍未取完，已中止以防死循环。" % max_pages)
    return hosts


def normalize_host(host):
    """Flatten a Host record for the table view (all scalars preserved)."""
    flat = dict(host)
    for key in ("asset", "vulnerability", "baseline", "intrusion", "labels",
                "common_login_area_codes", "node_runtime_info"):
        if isinstance(flat.get(key), (dict, list)):
            flat[key] = json.dumps(flat[key], ensure_ascii=False,
                                   separators=(",", ":"))
    return flat


def _field(host, *names, default="-"):
    for name in names:
        if name in host and host[name] not in (None, ""):
            return host[name]
    return default


def host_names(hosts):
    names = []
    for host in hosts:
        name = _field(host, "host_name", default=None)
        if name is None:
            name = _field(host, "host_id")
        names.append(str(name))
    return names


def _cell(value):
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return str(value)


def render_table(hosts):
    """Render full-field table output (union of all returned fields)."""
    rows_data = [normalize_host(host) for host in hosts]
    columns = []
    for key in PREFERRED_COLUMNS:
        if any(key in c for c in rows_data):
            columns.append(key)
    for key in sorted({k for c in rows_data for k in c}):
        if key not in columns:
            columns.append(key)
    if not columns:
        columns = ["host_name", "host_id", "private_ip"]
    rows = [[_cell(_field(c, col)) for col in columns] for c in rows_data]
    widths = [max(len(col), *(len(row[i]) for row in rows)) for i, col in enumerate(columns)]
    header = "  ".join(col.ljust(widths[i]) for i, col in enumerate(columns))
    separator = "  ".join("-" * w for w in widths)
    lines = [header, separator]
    for row in rows:
        lines.append("  ".join(row[i].ljust(widths[i]) for i in range(len(columns))))
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="查询华为云主机安全服务（HSS）已接入服务器的防护/Agent状态列表"
                    "（KooCLI hcloud HSS ListHostStatus，只读）。")
    parser.add_argument("-r", "--region", default=DEFAULT_REGION,
                        help="目标 Region（默认 %s）" % DEFAULT_REGION)
    parser.add_argument("--json", action="store_true", dest="as_json",
                        help="以 JSON 输出完整原始字段")
    parser.add_argument("--names-only", action="store_true", dest="names_only",
                        help="仅输出主机名称清单")
    parser.add_argument("--host-name", dest="host_name",
                        help="按服务器名称过滤（服务端查询参数）")
    parser.add_argument("--host-id", dest="host_id",
                        help="按服务器 ID 过滤（服务端查询参数）")
    parser.add_argument("--agent-status", dest="agent_status",
                        help="按 Agent 状态过滤：online/offline/installing/"
                             "install_failed/not_installed/not_online")
    parser.add_argument("--host-status", dest="host_status",
                        help="按主机状态过滤：ACTIVE/SHUTOFF/BUILDING/ERROR")
    parser.add_argument("--protect-status", dest="protect_status",
                        help="按防护状态过滤：opened/closed/protection_exception")
    parser.add_argument("--os-type", dest="os_type",
                        help="按操作系统类型过滤：Linux/Windows")
    parser.add_argument("--ip-addr", dest="ip_addr",
                        help="按 IP 地址过滤（服务端查询参数）")
    parser.add_argument("--version", dest="version",
                        help="按防护版本过滤：hss.version.basic / advanced / "
                             "enterprise / premium / wtp 等")
    parser.add_argument("--enterprise-project-id", dest="enterprise_project_id",
                        help="按企业项目 ID 过滤（服务端查询参数，0 表示默认企业项目，"
                             "all_granted_eps 表示所有已授权企业项目）")
    parser.add_argument("--page-size", type=int, default=DEFAULT_PAGE_SIZE,
                        dest="page_size",
                        help="分页大小（默认 %d，范围 10~200）" % DEFAULT_PAGE_SIZE)
    parser.add_argument("--project-id", dest="project_id",
                        help="项目 ID（可选；SDK 回退在 %s 路径中需要）" % REST_PATH)
    parser.add_argument("--operation", default=ALLOWED_OPERATION,
                        help="hcloud HSS 操作名（仅允许只读 %s）" % ALLOWED_OPERATION)
    args = parser.parse_args(argv)

    try:
        # Write-intent guard: scan the raw argv + validate the operation name.
        guard_write_intent(" ".join(argv if argv is not None else sys.argv[1:]))
        guard_operation(args.operation)
        if args.host_name:
            guard_write_intent(args.host_name)
        hosts = list_hosts(
            args.region,
            host_name=args.host_name,
            host_id=args.host_id,
            agent_status=args.agent_status,
            host_status=args.host_status,
            protect_status=args.protect_status,
            os_type=args.os_type,
            ip_addr=args.ip_addr,
            version=args.version,
            enterprise_project_id=args.enterprise_project_id,
            limit=args.page_size,
            project_id=args.project_id,
        )
    except HssListError as exc:
        print("[错误] %s" % exc, file=sys.stderr)
        return 1

    if args.as_json:
        print(json.dumps(hosts, ensure_ascii=False, indent=2))
        return 0

    if args.names_only:
        print("Region %s 的 HSS 已接入服务器名称列表（共 %d 台）：" % (args.region, len(hosts)))
        for name in host_names(hosts):
            print("- %s" % name)
        return 0

    if not hosts:
        filters = []
        for label, value in (
                ("host_name", args.host_name),
                ("host_id", args.host_id),
                ("agent_status", args.agent_status),
                ("host_status", args.host_status),
                ("protect_status", args.protect_status),
                ("os_type", args.os_type),
                ("ip_addr", args.ip_addr),
                ("version", args.version),
                ("enterprise_project_id", args.enterprise_project_id)):
            if value:
                filters.append("%s=%s" % (label, value))
        suffix = "（过滤条件: %s）" % ", ".join(filters) if filters else ""
        print("当前区域（%s）无已接入 HSS 的服务器%s。" % (args.region, suffix))
        return 0

    print("Region %s 的 HSS 主机防护列表（共 %d 台，完整字段）：" % (args.region, len(hosts)))
    print(render_table(hosts))
    return 0


if __name__ == "__main__":
    sys.exit(main())