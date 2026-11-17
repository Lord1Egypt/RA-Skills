#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""List Huawei Cloud SFS file systems via KooCLI ``hcloud SFSTurbo ListShares`` (read-only).

Primary execution path is KooCLI; when the hcloud binary is not installed, the
script falls back to the official ``huaweicloudsdksfsturbo`` v1 SDK
(``SFSTurboClient.list_shares``). Credentials are always resolved by the
hcloud profile / SDK environment — this script never reads, echoes or stores
AK/SK itself.

Supported features:

* Four stdout modes — aligned full-field table (default), ``--json`` (raw
  response array), ``--names-only`` (compact name + ID inventory) and
  ``--count-only`` (just the number of matching file systems).
* Read-only query with ``--region`` (default cn-north-4), ``--page-size`` and
  automatic ``limit`` / ``offset`` paging.
* Client-side ``--name`` / ``--id`` / ``--status`` / ``--share-proto`` /
  ``--az`` filtering (the SFS ``ListShares`` request itself only accepts
  limit/offset — see ``huaweicloudsdksfsturbo.v1.ListSharesRequest``).
* Strict write-intent guard: any mutating SFS intent is rejected before a
  single command is executed.

Usage:
    python3 scripts/list_sfs.py [--region cn-north-4]
                                [--json | --names-only | --count-only]
                                [--name NAME] [--id ID] [--status STATUS]
                                [--share-proto NFS|CIFS] [--az AZ]
                                [--page-size 200] [--operation ListShares]

Environment overrides (mostly for tests):
    SFS_LIST_HCLOUD_BIN   hcloud executable (default "hcloud")
    SFS_LIST_HCLOUD_ARGS  extra args injected before the SFS operation
"""

import argparse
import json
import os
import re
import subprocess
import sys

DEFAULT_REGION = "cn-north-4"
# SFS Turbo ListShares rejects limit > 200 (`[USE_ERROR]limit invalid (max 200)`),
# so the page size is capped and user input is clamped to [MIN_PAGE_SIZE, MAX_PAGE_SIZE].
DEFAULT_PAGE_SIZE = 200
MIN_PAGE_SIZE = 1
MAX_PAGE_SIZE = 200
SERVICE = "SFSTurbo"
ALLOWED_OPERATION = "ListShares"

# Mutating SFS intents / operation names — strictly rejected by the guard.
# Read-only vocabulary (list/show/get/describe/details) never matches.
WRITE_INTENT_KEYWORDS = (
    "createshare",
    "deleteshare",
    "updateshare",
    "extendshare",
    "expandshare",
    "shrinkshare",
    "resizeshare",
    "changecharge",
    "changestatus",
    "addtarget",
    "addtargets",
    "deletetarget",
    "deletetargets",
    "setacl",
    "putacl",
    "deleteacl",
    "grantaccess",
    "revokeaccess",
    "create",
    "delete",
    "update",
    "modify",
    "extend",
    "expand",
    "shrink",
    "resize",
    "attach",
    "detach",
    "mount",
    "unmount",
    "bind",
    "unbind",
    "restore",
    "backup",
    "clone",
    "reboot",
    "restart",
    "reset",
    "shutdown",
    "terminate",
    "destroy",
    "remove",
    "purge",
)

# Read-only option flags whose *values* are filter / path data (e.g. a file
# system named "delete-test" or a status value). Their values must NOT be
# scanned by the write-intent guard. The ``--operation`` value is intentionally
# NOT excluded: it is validated by ``guard_operation()`` and scanned as defense
# in depth.
_VALUE_STRIPPED_FLAGS = (
    "--region",
    "-r",
    "--name",
    "--id",
    "--share-id",
    "--status",
    "--share-proto",
    "--share-type",
    "--az",
    "--page-size",
    "--limit",
    "--offset",
)

# Preferred column order for the table view; remaining keys are appended sorted.
PREFERRED_COLUMNS = [
    "name",
    "id",
    "status",
    "share_proto",
    "size",
    "availability_zone",
    "share_type",
    "region",
    "export_location",
    "created_at",
    "enterprise_project_id",
    "vpc_id",
    "subnet_id",
    "security_group_id",
]

_SHARE_LIST_KEYS = (
    "shares",
    "file_systems",
    "filesystems",
    "share_list",
    "shares_detail",
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
# stdout WITH exit code 0 — the marker must be treated as a hard failure even
# when the return code looks successful.
_USE_ERROR_MARKER = "[use_error]"


class SfsListError(Exception):
    """Base error for the SFS list skill."""


class GuardError(SfsListError):
    """A write intent was detected and blocked (skill is read-only)."""


class ConfigError(SfsListError):
    """hcloud missing or credentials (AK/SK) not configured."""


class AuthError(SfsListError):
    """Authentication/authorization failure (invalid AK/SK or IAM 403)."""


class ApiError(SfsListError):
    """hcloud / network / unexpected API failure."""


def guard_write_intent(text):
    """Raise GuardError if ``text`` carries a mutating intent.

    Separators are normalized so ``--create-share``, ``CreateShare`` and
    ``create_share`` all hit the same keyword. Read-only vocabulary
    (list/show/get/describe) never matches.
    """
    low = re.sub(r"[\s_\-]+", "", str(text).lower())
    for keyword in WRITE_INTENT_KEYWORDS:
        if keyword in low:
            raise GuardError(
                "检测到写操作意图（关键词: %s）。本 skill 仅支持只读查询"
                "（SFS ListShares），创建/删除/扩容/挂载/卸载/改配等变更操作已被守卫拦截。"
                % keyword
            )
    return False


def guard_operation(operation):
    """Only the read-only ListShares operation may be executed."""
    if operation != ALLOWED_OPERATION:
        raise GuardError(
            "不允许的操作 %r：本 skill 仅允许只读操作 %s。"
            % (operation, ALLOWED_OPERATION)
        )
    return True


def guard_text_from_argv(argv):
    """Build the text the write-intent guard should scan.

    Scans flag names and positional tokens, but strips the values of the
    read-only filter flags (``--name`` / ``--id`` / ``--status`` / ``--region``
    / ``--page-size`` / ...): those are query data and may legitimately contain
    write-looking words (e.g. a file system named ``delete-test``).
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


def clamp_page_size(value):
    """Clamp a requested page size into the ListShares limit range [1, 200].

    SFS Turbo ``ListShares`` rejects ``limit > 200`` with
    ``[USE_ERROR]limit invalid (max 200)``; non-numeric input falls back to
    ``DEFAULT_PAGE_SIZE``.
    """
    try:
        size = int(value)
    except (TypeError, ValueError):
        return DEFAULT_PAGE_SIZE
    if size < MIN_PAGE_SIZE:
        return MIN_PAGE_SIZE
    if size > MAX_PAGE_SIZE:
        return MAX_PAGE_SIZE
    return size


def build_command(region, limit=DEFAULT_PAGE_SIZE, offset=0):
    """Build the hcloud SFSTurbo ListShares argv (without the executable).

    Mirrors the real KooCLI parameter list: ``--cli-region`` / ``--limit`` /
    ``--offset``. The SFS ``ListShares`` request only carries limit/offset
    (verified against ``huaweicloudsdksfsturbo`` v1
    ``ListSharesRequest.openapi_types``); name / ID / status filtering is
    therefore applied client-side.
    """
    return [
        SERVICE,
        ALLOWED_OPERATION,
        "--cli-region=%s" % region,
        "--limit=%d" % limit,
        "--offset=%d" % offset,
    ]


def _hcloud_executable():
    return os.environ.get("SFS_LIST_HCLOUD_BIN", "hcloud")


def run_hcloud(argv):
    """Execute hcloud and return (stdout, stderr, returncode)."""
    cmd = [_hcloud_executable()]
    extra = os.environ.get("SFS_LIST_HCLOUD_ARGS", "").split()
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
        start, end = text.find("["), text.rfind("]")
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
            "hcloud 参数错误（KooCLI 拒绝了该参数组合，退出码 %s）：SFSTurbo ListShares "
            "真实参数清单可通过 `hcloud SFSTurbo ListShares --help` 查看。详情：%s"
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
            "无权限访问 SFS，请检查 IAM 权限（403：AK/SK 无效或未授予 SFS 只读权限），"
            "参见 references/iam-policies.md。详情：%s" % blob[:300]
        )
    return ApiError(
        "hcloud 调用失败（退出码 %s）：%s" % (returncode, blob[:300])
    )


def extract_shares(payload):
    """Pull the file-system list out of a ListShares response."""
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        for key in _SHARE_LIST_KEYS:
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


def _env_credential(*names):
    for name in names:
        value = os.environ.get(name)
        if value:
            return value
    return None


def _env_credentials():
    ak = _env_credential(
        "HW_ACCESS_KEY", "HUAWEI_ACCESS_KEY", "HUAWEICLOUD_SDK_AK",
        "HUAWEI_CLOUD_ACCESS_KEY",
    )
    sk = _env_credential(
        "HW_SECRET_KEY", "HUAWEI_SECRET_KEY", "HUAWEICLOUD_SDK_SK",
        "HUAWEI_CLOUD_SECRET_KEY",
    )
    return ak, sk


def sdk_share_to_dict(share):
    """Convert a ``huaweicloudsdksfsturbo`` ShareInfo into a wire-name dict.

    The SDK ``to_dict()`` emits Python attribute names; the OpenAPI JSON uses
    wire names. Remapping through ``ShareInfo.attribute_map`` keeps both
    execution paths producing the same shape.
    """
    if isinstance(share, dict):
        raw = dict(share)
    else:
        try:
            raw = share.to_dict()
        except AttributeError:
            return dict(share)
    if not isinstance(raw, dict):
        return {}
    try:
        from huaweicloudsdksfsturbo.v1 import ShareInfo
        attr_map = ShareInfo.attribute_map
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


def list_shares_via_sdk(region, limit=DEFAULT_PAGE_SIZE, max_pages=100):
    """SDK fallback: query file systems through ``huaweicloudsdksfsturbo`` v1.

    Only invoked when hcloud is not installed. Credentials come from the
    whitelisted AK/SK environment variables (HW_*/HUAWEI_ACCESS_KEY family) —
    never passed as literals here. Region resolution uses the SDK's own
    ``SFSTurboRegion`` catalog (official endpoints, no guessing), falling back
    to an explicit ``Region(id, endpoint)`` for custom regions.
    """
    limit = clamp_page_size(limit)
    try:
        from huaweicloudsdkcore.auth.credentials import BasicCredentials
        from huaweicloudsdkcore.region.region import Region
        from huaweicloudsdkcore.http.http_config import HttpConfig
        from huaweicloudsdksfsturbo.v1 import SFSTurboClient, ListSharesRequest
        from huaweicloudsdksfsturbo.v1.region.sfsturbo_region import SFSTurboRegion
    except ImportError as exc:
        raise ConfigError(
            "未找到 hcloud（KooCLI），且 huaweicloudsdkcore/huaweicloudsdksfsturbo "
            "未安装，无法回退到 SDK。请安装 KooCLI 或 pip install "
            "huaweicloudsdkcore huaweicloudsdksfsturbo。详情：%s" % exc
        )

    ak, sk = _env_credentials()
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
            region_obj = SFSTurboRegion.value_of(region)
        except (ValueError, KeyError, AttributeError):
            region_obj = Region(
                region, "https://sfs-turbo.%s.myhuaweicloud.com" % region)
        client = SFSTurboClient.new_builder() \
            .with_credentials(credentials) \
            .with_region(region_obj) \
            .with_http_config(HttpConfig.get_default_config()) \
            .build()
    except Exception as exc:  # region unknown / config broken
        raise ConfigError(
            "SDK 初始化失败（region=%s）：%s。请检查 huaweicloudsdksfsturbo 安装与区域"
            "配置。" % (region, exc)
        )
    shares = []
    offset = 0
    for _ in range(max_pages):
        request = ListSharesRequest(limit=limit, offset=offset)
        try:
            response = client.list_shares(request)
        except Exception as exc:
            low = str(exc).lower()
            if any(p in low for p in _AUTH_PATTERNS):
                raise AuthError(
                    "无权限访问 SFS，请检查 IAM 权限（403）。详情：%s" % str(exc)[:300]
                )
            raise ApiError("SDK 调用失败：%s" % str(exc)[:300])
        batch = list(response.shares or [])
        shares.extend(sdk_share_to_dict(share) for share in batch)
        total = getattr(response, "count", None)
        if total is not None and len(shares) >= total:
            break
        if len(batch) < limit:
            break
        offset += len(batch)
    else:
        raise ApiError("翻页超过 %d 页仍未取完，已中止以防死循环。" % max_pages)
    return shares


def list_shares(region, limit=DEFAULT_PAGE_SIZE, max_pages=100):
    """Query all SFS file systems (paged); KooCLI first, SDK fallback."""
    limit = clamp_page_size(limit)
    shares = []
    offset = 0
    for _page in range(max_pages):
        argv = build_command(region, limit=limit, offset=offset)
        try:
            stdout, stderr, returncode = run_hcloud(argv)
        except ConfigError:
            # hcloud binary missing → one-shot SDK fallback (no CLI retry).
            shares = list_shares_via_sdk(region, limit=limit, max_pages=max_pages)
            break
        if returncode != 0 or _USE_ERROR_MARKER in (stdout + " " + stderr).lower():
            # KooCLI usage errors print [USE_ERROR] on stdout with rc=0.
            raise classify_hcloud_failure(stdout, stderr, returncode)
        payload = extract_json(stdout)
        batch = extract_shares(payload)
        shares.extend(batch)
        if not _has_more(batch, len(shares), limit, payload):
            break
        offset += len(batch) if batch else limit
    else:
        raise ApiError("翻页超过 %d 页仍未取完，已中止以防死循环。" % max_pages)
    return shares


def _field(share, *names, default="-"):
    for name in names:
        if name in share and share[name] not in (None, ""):
            return share[name]
    return default


def _get(share, *names, default=None):
    """Return the first present, non-empty value among ``names``."""
    for name in names:
        if name in share and share[name] not in (None, ""):
            return share[name]
    return default


def normalize_share(share):
    """Flatten the availability-zone field into a table-friendly key.

    The SFS API may surface the AZ under ``availability_zone``, ``az_name`` or
    ``az`` depending on the operation; the table always shows
    ``availability_zone``. Other nested fields (e.g. ``metadata``) are rendered
    by ``render_table`` through ``_cell``, which JSON-encodes dict/list values.
    """
    flat = dict(share)
    az = _get(share, "availability_zone", "az_name", "az")
    flat["availability_zone"] = az if az is not None else "-"
    return flat


def filter_shares(shares, name=None, share_id=None, status=None,
                  share_proto=None, az=None):
    """Apply client-side name / ID / status / protocol / AZ filters.

    The SFS ``ListShares`` request has no server-side filter parameters, so the
    requested filtering is applied locally. ``name``, ``id`` and ``az`` are
    case-insensitive substring matches; ``status`` and ``share_proto`` are
    case-insensitive exact matches.
    """
    result = list(shares)
    if name:
        needle = str(name).lower()
        result = [s for s in result
                  if needle in str(_field(s, "name", "id", default="")).lower()]
    if share_id:
        needle = str(share_id).lower()
        result = [s for s in result
                  if needle in str(_field(s, "id", "name", default="")).lower()]
    if status:
        needle = str(status).lower()
        result = [s for s in result
                  if str(_field(s, "status", default="")).lower() == needle]
    if share_proto:
        needle = str(share_proto).lower()
        result = [s for s in result
                  if str(_field(s, "share_proto", "share_type",
                                default="")).lower() == needle]
    if az:
        needle = str(az).lower()
        result = [s for s in result
                  if needle in str(_get(s, "availability_zone", "az_name",
                                        "az", default="")).lower()]
    return result


def share_names(shares):
    names = []
    for share in shares:
        name = _field(share, "name", default=None)
        if name is None:
            name = _field(share, "id")
        names.append(str(name))
    return names


def share_summary_lines(shares):
    """Compact ``name  (id: ...)`` lines for the --names-only inventory mode."""
    lines = []
    for share in shares:
        name = _field(share, "name", default=None)
        if name is None:
            name = _field(share, "id")
        sid = _field(share, "id", default="-")
        lines.append("%s  (id: %s)" % (name, sid))
    return lines


def active_filter_descriptions(name=None, share_id=None, status=None,
                               share_proto=None, az=None):
    """Human-readable description of the filters actually applied."""
    filters = []
    if name:
        filters.append("name=%s" % name)
    if share_id:
        filters.append("id=%s" % share_id)
    if status:
        filters.append("status=%s" % status)
    if share_proto:
        filters.append("share_proto=%s" % share_proto)
    if az:
        filters.append("az=%s" % az)
    return filters


def _cell(value):
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return str(value)


def render_table(shares):
    """Render full-field table output (union of all returned fields)."""
    rows_data = [normalize_share(share) for share in shares]
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
        description="查询华为云 SFS 文件系统列表（KooCLI hcloud SFSTurbo ListShares，只读）。")
    parser.add_argument("-r", "--region", default=DEFAULT_REGION,
                        help="目标 Region（默认 %s）" % DEFAULT_REGION)
    parser.add_argument("--json", action="store_true", dest="as_json",
                        help="以 JSON 输出完整原始字段")
    parser.add_argument("--names-only", action="store_true", dest="names_only",
                        help="仅输出精简文件系统名称+ID 清单")
    parser.add_argument("--count-only", action="store_true", dest="count_only",
                        help="仅输出匹配的文件系统数量")
    parser.add_argument("--name", help="按文件系统名称过滤（客户端子串匹配）")
    parser.add_argument("--id", help="按文件系统 ID 过滤（客户端子串匹配）")
    parser.add_argument("--status",
                        help="按状态过滤（客户端精确匹配，如 available/creating）")
    parser.add_argument("--share-proto", dest="share_proto",
                        help="按协议过滤（客户端精确匹配：NFS / CIFS）")
    parser.add_argument("--az", help="按可用区过滤（客户端子串匹配，如 cn-north-4a）")
    parser.add_argument("--page-size", type=int, default=DEFAULT_PAGE_SIZE,
                        dest="page_size",
                        help="分页大小（默认 %d，最大 %d；超出将被钳制到 [%d, %d]）"
                             % (DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE, MIN_PAGE_SIZE, MAX_PAGE_SIZE))
    parser.add_argument("--operation", default=ALLOWED_OPERATION,
                        help="hcloud SFSTurbo 操作名（仅允许只读 %s）" % ALLOWED_OPERATION)

    # Write-intent guard runs on the RAW argv before argparse so a mutating flag
    # (e.g. `--create-share`) is reported as a guard violation rather than an
    # argparse "unrecognized argument" error. Filter values are read-only data
    # and deliberately not scanned.
    try:
        guard_write_intent(guard_text_from_argv(argv))
    except SfsListError as exc:
        print("[错误] %s" % exc, file=sys.stderr)
        return 1

    args = parser.parse_args(argv)

    try:
        guard_operation(args.operation)
        shares = list_shares(args.region, limit=args.page_size)
    except SfsListError as exc:
        print("[错误] %s" % exc, file=sys.stderr)
        return 1

    filters = active_filter_descriptions(
        name=args.name, share_id=args.id, status=args.status,
        share_proto=args.share_proto, az=args.az)
    shares = filter_shares(
        shares, name=args.name, share_id=args.id, status=args.status,
        share_proto=args.share_proto, az=args.az)
    filter_suffix = "（过滤条件: %s）" % ", ".join(filters) if filters else ""

    if args.count_only:
        print("Region %s 的 SFS 文件系统数量：%d%s"
              % (args.region, len(shares), filter_suffix))
    elif args.as_json:
        print(json.dumps(shares, ensure_ascii=False, indent=2))
    elif args.names_only:
        print("Region %s 的 SFS 文件系统清单（共 %d 个）：" % (args.region, len(shares)))
        for line in share_summary_lines(shares):
            print("- %s" % line)
    elif not shares:
        print("当前区域（%s）无 SFS 文件系统%s。" % (args.region, filter_suffix))
    else:
        print("Region %s 的 SFS 文件系统列表（共 %d 个，完整字段）："
              % (args.region, len(shares)))
        print(render_table(shares))

    return 0


if __name__ == "__main__":
    sys.exit(main())