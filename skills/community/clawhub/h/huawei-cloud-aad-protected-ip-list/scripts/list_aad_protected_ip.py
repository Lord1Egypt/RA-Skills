#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Huawei Cloud Anti-DDoS (AAD) protected-IP list helper.

Queries the Anti-DDoS protected-IP inventory of the current account through
KooCLI (``hcloud AAD ListProtectedIp``) and falls back to the official
``huaweicloudsdkaad`` SDK when the CLI is unavailable.

Executed operation (read-only GET, REST path from the SDK
``_list_protected_ip_http_info``):

    ListProtectedIp   GET /v1/cnad/protected-ips

Output modes:

- default: a concise list of 防护 IP | 封堵状态.
- ``--table``: 防护 IP | 状态 | 绑定策略 | 套餐 | region.
- ``--json``: the raw response body (merged across pages when paging).

Write intents (add / delete / associate / disassociate / execute-unblock /
modify / update / create / batch / ...) are rejected before any command runs -
this skill is strictly read-only.

Secrets are never hardcoded or echoed: KooCLI uses its own profile, and the SDK
fallback only reads credential environment variables. The script never reads,
prints or stores secret values.

Usage:
    python3 scripts/list_aad_protected_ip.py --region cn-north-4
    python3 scripts/list_aad_protected_ip.py --table --region cn-north-4
    python3 scripts/list_aad_protected_ip.py --json --region cn-north-4
    python3 scripts/list_aad_protected_ip.py --ip 192.0.2.10 --limit 50
    python3 scripts/list_aad_protected_ip.py --policy-id <id> --package-id <id>
    python3 scripts/list_aad_protected_ip.py --tag web --region cn-north-4
"""

import argparse
import json
import os
import shutil
import subprocess
import sys

SKILL_NAME = "huawei-cloud-aad-protected-ip-list"
DEFAULT_REGION = "cn-north-4"
DEFAULT_TIMEOUT = 60
DEFAULT_PAGE_SIZE = 100
MAX_PAGE_SIZE = 100
MAX_PAGES = 1000

# Whitelisted credential environment variables. They are read one by one by
# name via os.environ.get; the whole environment is never enumerated, so no
# unrelated variable can be harvested by accident.
_AK_ENV_NAMES = (
    "HUAWEICLOUD_SDK_AK",
    "HUAWEI_ACCESS_KEY",
    "HUAWEI_CLOUD_ACCESS_KEY",
    "HW_ACCESS_KEY",
    "HWC_ACCESS_KEY",
)
_SK_ENV_NAMES = (
    "HUAWEICLOUD_SDK_SK",
    "HUAWEI_SECRET_KEY",
    "HUAWEI_CLOUD_SECRET_KEY",
    "HW_SECRET_KEY",
    "HWC_SECRET_KEY",
)
_TOKEN_ENV_NAMES = (
    "HUAWEICLOUD_SDK_SECURITY_TOKEN",
    "HUAWEI_SECURITY_TOKEN",
    "HW_SECURITY_TOKEN",
    "HWC_SECURITY_TOKEN",
)

# ---------------------------------------------------------------------------
# Error types (mapped to executable hints in main)
# ---------------------------------------------------------------------------


class AadError(Exception):
    """Base error for this helper."""


class AadCredentialError(AadError):
    """No usable credentials were found."""


class AadPermissionError(AadError):
    """The caller lacks the required read-only IAM permission."""


class AadNetworkError(AadError):
    """The endpoint could not be reached."""


class CliUnavailable(AadError):
    """KooCLI is missing or cannot serve this operation."""


# ---------------------------------------------------------------------------
# CLI backend helpers
# ---------------------------------------------------------------------------


def _hcloud_binary():
    """Return the hcloud binary path, or None when it is not installed."""
    return shutil.which("hcloud")


def _hcloud(args, timeout=DEFAULT_TIMEOUT):
    """Run hcloud and return the parsed JSON body.

    Raises RuntimeError on a non-zero exit or unparseable output.
    """
    proc = subprocess.run(
        args,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    if proc.returncode != 0:
        detail = (proc.stderr or proc.stdout or "").strip()
        raise RuntimeError(
            "hcloud command failed (exit={0}): {1}".format(
                proc.returncode, detail[:800]
            )
        )
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError:
        raise RuntimeError(
            "hcloud returned non-JSON output: {0}".format(
                (proc.stdout or "")[:400]
            )
        )


def _build_cli_command(cli_bin, region, limit, offset, filters):
    cmd = [
        cli_bin,
        "AAD",
        "ListProtectedIp",
        "--cli-region=" + str(region),
        "--limit=" + str(limit),
        "--offset=" + str(offset),
    ]
    for key in ("ip", "policy_id", "package_id", "tag"):
        value = filters.get(key)
        if value is not None and str(value) != "":
            cmd.append("--{0}={1}".format(key, value))
    return cmd


def _extract_items(data):
    """Return the item list from a response body (tolerant of wrappers)."""
    if not isinstance(data, dict):
        return []
    for key in ("items", "protected_ips", "protectedIps"):
        value = data.get(key)
        if isinstance(value, list):
            return value
    return []


def _as_int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _collect_cli(region, page_size, start_offset, filters, timeout):
    """Page through ListProtectedIp via KooCLI until the full set is fetched."""
    cli_bin = _hcloud_binary()
    if not cli_bin:
        raise CliUnavailable("未找到 hcloud CLI")

    collected = []
    total = None
    offset = start_offset
    for _ in range(MAX_PAGES):
        cmd = _build_cli_command(cli_bin, region, page_size, offset, filters)
        try:
            data = _hcloud(cmd, timeout)
        except RuntimeError as exc:
            raise _classify_cli_error(str(exc))
        if not isinstance(data, dict):
            raise AadError("接口返回格式异常（不是 JSON 对象）")
        if total is None:
            total = _as_int(data.get("total"), 0)
        items = _extract_items(data)
        collected.extend(items)
        if not items:
            break
        if len(items) < page_size:
            break
        if total and start_offset + len(collected) >= total:
            break
        offset += page_size

    if total is None:
        total = len(collected)
    if total < len(collected):
        total = len(collected)
    return total, collected


def _classify_cli_error(message):
    """Translate a raw hcloud error into a typed error."""
    lowered = message.lower()
    if "[use_error]" in lowered:
        if "parameter format" in lowered or "format must be" in lowered:
            return AadError(message)
        return CliUnavailable(message)
    if any(tok in lowered for tok in (
        "403", "forbidden", "not authorized", "not allowed",
        "pdp.permission", "insufficient permission", "permission denied",
        "aad.0401",
    )):
        return AadPermissionError(message)
    if any(tok in lowered for tok in (
        "401", "ak/sk", "access key", "secret key", "credential",
        "securitytoken", "security token", "authenticate", "auth failed",
    )):
        return AadCredentialError(message)
    if any(tok in lowered for tok in (
        "timeout", "timed out", "connection", "network", "unreachable",
        "name or service not known", "ssl", "max retries", "proxy",
    )):
        return AadNetworkError(message)
    return AadError(message)


# ---------------------------------------------------------------------------
# SDK fallback
# ---------------------------------------------------------------------------


def _sdk_available():
    try:
        import huaweicloudsdkaad  # noqa: F401
    except ImportError:
        return False
    try:
        import huaweicloudsdkcore  # noqa: F401
    except ImportError:
        return False
    return True


def _first_env(names):
    """Return the first non-empty value among the whitelisted names."""
    for name in names:
        value = os.environ.get(name)
        if value and value.strip():
            return value.strip()
    return ""


def _resolve_credentials():
    """Read AK/SK/security token from the whitelisted environment names only."""
    return (
        _first_env(_AK_ENV_NAMES),
        _first_env(_SK_ENV_NAMES),
        _first_env(_TOKEN_ENV_NAMES),
    )


def _list_via_sdk(region, page_size, start_offset, filters, timeout=DEFAULT_TIMEOUT):
    """Page through ListProtectedIp through huaweicloudsdkaad."""
    if not _sdk_available():
        raise CliUnavailable(
            "未安装 huaweicloudsdkaad SDK（pip install huaweicloudsdkaad）"
        )
    ak, sk, token = _resolve_credentials()
    if not ak or not sk:
        raise AadCredentialError(
            "SDK 回退需要 AK/SK 环境变量（HUAWEICLOUD_SDK_AK / HUAWEICLOUD_SDK_SK）"
        )

    from huaweicloudsdkaad.v1 import AadClient, ListProtectedIpRequest
    from huaweicloudsdkaad.v1.region.aad_region import AadRegion
    from huaweicloudsdkcore.auth.credentials import BasicCredentials

    try:
        aad_region = AadRegion.value_of(region)
    except KeyError:
        raise AadError(
            "SDK 回退不支持区域 {0}（支持 cn-north-4 / ap-southeast-1）".format(region)
        )

    credentials = BasicCredentials(ak, sk)
    if token:
        credentials = credentials.with_security_token(token)
    client = (
        AadClient.new_builder()
        .with_credentials(credentials)
        .with_region(aad_region)
        .build()
    )

    collected = []
    total = None
    offset = start_offset
    for _ in range(MAX_PAGES):
        request = ListProtectedIpRequest(
            offset=offset,
            limit=page_size,
            ip=filters.get("ip"),
            policy_id=filters.get("policy_id"),
            package_id=filters.get("package_id"),
            tag=filters.get("tag"),
        )
        try:
            response = client.list_protected_ip(request)
        except Exception as exc:  # SDK raises typed exceptions
            raise _classify_cli_error(str(exc))
        data = _response_to_dict(response)
        if total is None:
            total = _as_int(data.get("total"), 0)
        items = _extract_items(data)
        collected.extend(items)
        if not items:
            break
        if len(items) < page_size:
            break
        if total and start_offset + len(collected) >= total:
            break
        offset += page_size

    if total is None:
        total = len(collected)
    if total < len(collected):
        total = len(collected)
    return total, collected


def _response_to_dict(response):
    """Convert an SDK response object to a plain dict.

    The SDK response classes expose a fixed set of serialisation helpers, so
    each is probed explicitly instead of resolving attribute names at runtime.
    """
    if isinstance(response, dict):
        return dict(response)
    if hasattr(response, "to_json_object"):
        try:
            value = response.to_json_object()
        except Exception:
            value = None
        if isinstance(value, dict):
            return value
    if hasattr(response, "to_dict"):
        try:
            value = response.to_dict()
        except Exception:
            value = None
        if isinstance(value, dict):
            return value
    if hasattr(response, "to_str"):
        try:
            value = response.to_str()
        except Exception:
            value = None
        if isinstance(value, str):
            try:
                value = json.loads(value)
            except json.JSONDecodeError:
                value = None
            if isinstance(value, dict):
                return value
    return {}


# ---------------------------------------------------------------------------
# Presentation
# ---------------------------------------------------------------------------

_STATUS_DESC = {
    0: "正常",
    1: "清洗中",
    2: "黑洞中（封堵中）",
}

_PACKAGE_VERSION_DESC = {
    "cnad_pro": "专业版",
    "cnad_ip": "标准版",
    "cnad_ep": "铂金版",
    "cnad_full_high": "全力防高级版",
    "cnad_vic": "按需版",
    "cnad_intl_ep": "国际站铂金版",
}


def _status_text(value):
    try:
        return _STATUS_DESC.get(int(value), str(value))
    except (TypeError, ValueError):
        return "" if value is None else str(value)


def _package_text(item):
    name = item.get("package_name") or ""
    version = item.get("package_version") or ""
    version_text = _PACKAGE_VERSION_DESC.get(version, version)
    if name and version_text:
        return "{0}（{1}）".format(name, version_text)
    return name or version_text or ""


def _policy_text(item):
    if item.get("is_resale"):
        return "转售版（无策略）"
    return item.get("policy_name") or ""


def _render_concise(items):
    header = ["防护 IP", "封堵状态"]
    rows = [[str(i.get("ip") or ""), _status_text(i.get("status"))] for i in items]
    return _render_rows(header, rows)


def _render_table(items):
    header = ["防护 IP", "状态", "绑定策略", "套餐", "region"]
    rows = [[
        str(i.get("ip") or ""),
        _status_text(i.get("status")),
        _policy_text(i),
        _package_text(i),
        str(i.get("region") or ""),
    ] for i in items]
    return _render_rows(header, rows)


def _render_rows(header, rows):
    widths = []
    for idx, title in enumerate(header):
        width = len(title)
        for row in rows:
            width = max(width, len(str(row[idx])))
        widths.append(width)
    lines = [" | ".join(header[i].ljust(widths[i]) for i in range(len(header)))]
    lines.append("-+-".join("-" * w for w in widths))
    for row in rows:
        lines.append(" | ".join(str(row[i]).ljust(widths[i])
                                for i in range(len(header))))
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Guard: strictly read-only
# ---------------------------------------------------------------------------

_WRITE_INTENT = (
    "add", "create", "delete", "remove", "update", "modify", "set",
    "associate", "disassociate", "unblock", "block", "execute", "batch",
    "apply", "switch", "change", "rename", "migrate", "import", "export",
    "publish", "restore", "enable", "disable",
)

_READ_ACTIONS = ("list", "query", "search", "show")


def _detect_write_intent(texts):
    for text in texts:
        if text is None:
            continue
        lowered = str(text).lower()
        for token in _WRITE_INTENT:
            if token in lowered:
                return token, text
    return None, None


def _read_only_guard(args):
    """Return an error message when a write intent is detected, else None."""
    if args.action is not None:
        action = str(args.action).lower()
        if action not in _READ_ACTIONS:
            return (
                "此技能为只读查询（Anti-DDoS 防护 IP 列表），不支持操作: {0}。"
                "仅支持 list / query / search / show。".format(args.action)
            )
    token, source = _detect_write_intent([
        args.ip, args.policy_id, args.package_id, args.tag,
    ])
    if token:
        return (
            "此技能为只读查询（Anti-DDoS 防护 IP 列表），不支持对防护 IP 执行写操作。"
            "检测到疑似写操作意图: {0}（参数值: {1}）".format(token, source)
        )
    return None


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def _build_parser():
    parser = argparse.ArgumentParser(
        prog="list_aad_protected_ip.py",
        description="查询华为云 Anti-DDoS 防护 IP 列表（只读）",
    )
    parser.add_argument(
        "--region",
        default=os.environ.get("HUAWEICLOUD_SDK_REGION", DEFAULT_REGION),
        help="区域，默认 cn-north-4",
    )
    parser.add_argument("--json", action="store_true",
                        help="输出原始 JSON 响应体（分页合并后的 total/items）")
    parser.add_argument("--table", action="store_true",
                        help="输出明细表：防护 IP / 状态 / 绑定策略 / 套餐 / region")
    parser.add_argument("--ip", default=None, help="按防护 IP 精确过滤")
    parser.add_argument("--policy-id", dest="policy_id", default=None,
                        help="按策略 ID 过滤")
    parser.add_argument("--package-id", dest="package_id", default=None,
                        help="按防护实例（套餐）ID 过滤")
    parser.add_argument("--tag", default=None, help="按本地标签过滤")
    parser.add_argument("--limit", type=int, default=DEFAULT_PAGE_SIZE,
                        help="每页数量 1~100（超过 100 自动收敛为 100），默认 100")
    parser.add_argument("--offset", type=int, default=0,
                        help="起始偏移量，默认 0")
    parser.add_argument("--action", default=None,
                        help="兼容参数：仅接受 list/query/search/show；其他值按写意图拦截")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT,
                        help="单次命令超时秒数，默认 60")
    return parser


def _normalize_page_size(limit):
    if limit is None:
        return DEFAULT_PAGE_SIZE
    if limit <= 0:
        raise AadError("--limit 必须为 1~100 的正整数")
    if limit > MAX_PAGE_SIZE:
        print("[提示] --limit={0} 超过单页上限，已收敛为 {1}".format(
            limit, MAX_PAGE_SIZE), file=sys.stderr)
        return MAX_PAGE_SIZE
    return limit


def _fetch_all(region, page_size, start_offset, filters, timeout):
    """Fetch every page, trying KooCLI first and the SDK as fallback."""
    cli_errors = []
    last_exc = None
    cli_present = bool(_hcloud_binary())
    if cli_present:
        try:
            total, items = _collect_cli(
                region, page_size, start_offset, filters, timeout)
            return total, items, "cli", ""
        except (AadCredentialError, AadPermissionError):
            raise
        except (CliUnavailable, AadNetworkError, AadError) as exc:
            last_exc = exc
            cli_errors.append(str(exc))

    if _sdk_available():
        try:
            total, items = _list_via_sdk(
                region, page_size, start_offset, filters, timeout)
            note = "；".join(cli_errors) or (
                "未找到 hcloud CLI" if not cli_present else "")
            return total, items, "sdk", note
        except (AadCredentialError, AadPermissionError):
            raise
        except (CliUnavailable, AadNetworkError, AadError) as exc:
            last_exc = exc
            cli_errors.append(str(exc))

    if not cli_present and not _sdk_available():
        raise CliUnavailable(
            "未找到 hcloud CLI，且未安装 huaweicloudsdkaad SDK。"
            "请安装 KooCLI（https://support.huaweicloud.com/qs-hcli/hcli_02_003.html）"
            "或执行 pip install huaweicloudsdkaad。"
        )
    if last_exc is not None:
        raise last_exc
    raise AadError("；".join(cli_errors) or "未获取到防护 IP 数据")


def _print_error(message):
    print(message, file=sys.stderr)


def _classify_and_print(exc):
    """Print an executable, traceback-free hint for a typed error."""
    if isinstance(exc, AadPermissionError):
        _print_error(
            "无权限访问 Anti-DDoS 防护 IP 列表（403 / not authorized）。"
            "请检查 IAM 只读权限 aad:protectedIp:list，"
            "最小策略见 references/iam-policies.md。"
        )
    elif isinstance(exc, AadCredentialError):
        _print_error(
            "未找到可用的华为云凭据。请先离线配置 KooCLI profile"
            "（hcloud configure list 验证），或为 SDK 回退设置 "
            "HUAWEICLOUD_SDK_AK / HUAWEICLOUD_SDK_SK 环境变量。"
        )
    elif isinstance(exc, AadNetworkError):
        _print_error(
            "访问 Anti-DDoS 接口失败（网络超时或不可达）。请检查出网代理与 "
            "*.myhuaweicloud.com 连通性后重试。"
        )
    elif isinstance(exc, CliUnavailable):
        _print_error(
            "KooCLI 不可用或该操作不受支持：{0}。"
            "请升级 KooCLI（hcloud update -y）或安装 huaweicloudsdkaad SDK 后重试。"
            .format(exc)
        )
    else:
        _print_error(
            "查询 Anti-DDoS 防护 IP 失败：{0}".format(exc)
        )


def main(argv=None):
    parser = _build_parser()
    args = parser.parse_args(argv)

    guard_msg = _read_only_guard(args)
    if guard_msg:
        _print_error(guard_msg)
        return 1

    try:
        page_size = _normalize_page_size(args.limit)
    except AadError as exc:
        _print_error(str(exc))
        return 1

    if args.offset < 0:
        _print_error("--offset 不能为负数")
        return 1

    filters = {
        "ip": args.ip,
        "policy_id": args.policy_id,
        "package_id": args.package_id,
        "tag": args.tag,
    }

    try:
        total, items, backend, fallback_note = _fetch_all(
            args.region, page_size, args.offset, filters, args.timeout)
    except AadError as exc:
        _classify_and_print(exc)
        return 1
    except Exception as exc:  # never leak a traceback
        _print_error("查询 Anti-DDoS 防护 IP 失败：{0}".format(exc))
        return 1

    if fallback_note:
        print("[提示] KooCLI 不可用，已回退 SDK：{0}".format(fallback_note),
              file=sys.stderr)

    if args.json:
        print(json.dumps({"total": total, "items": items},
                         ensure_ascii=False, indent=2))
        return 0

    if not items:
        if any(filters.values()):
            print("未找到匹配的 Anti-DDoS 防护 IP。")
        else:
            print("未找到 Anti-DDoS 防护 IP。")
        return 0

    if args.table:
        print(_render_table(items))
    else:
        print(_render_concise(items))
    print("\n共 {0} 个防护 IP（区域: {1}，数据来源: {2}）".format(
        len(items), args.region, "KooCLI" if backend == "cli" else "SDK"))
    return 0


if __name__ == "__main__":
    sys.exit(main())