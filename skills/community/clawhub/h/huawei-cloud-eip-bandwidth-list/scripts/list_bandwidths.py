#!/usr/bin/env python3
"""List / show Huawei Cloud EIP bandwidths via KooCLI (read-only).

Primary execution path is KooCLI:
  * ``hcloud EIP ListBandwidths`` (GET /v3/{project_id}/eip/bandwidths)
  * ``hcloud EIP ShowBandwidth``  (GET /v3/{project_id}/eip/bandwidths/{bandwidth_id})

When hcloud is not installed the script falls back to the official
``huaweicloudsdkeip`` v3 SDK (``EipClient.list_bandwidths`` /
``EipClient.show_bandwidth``). Credentials are read by the CLI profile or the
official SDK environment variables; this script never reads, echoes or stores
secrets.

Output modes: default fixed-header table, ``--json`` (raw response array /
object), ``--format md -o <file>`` (archivable Markdown report). Marker paging
is automatic for the list path. A write-intent guard rejects every mutating
intent before a single command is executed.

Usage:
    python3 scripts/list_bandwidths.py [--region cn-north-4]
                                       [--share-type PER|WHOLE]
                                       [--enterprise-project-id <id>]
                                       [--limit 10]
                                       [--bandwidth-id <id>]
                                       [--json | --format md [-o <path.md>]]
                                       [--project-id <id>]

Environment overrides (mostly for tests):
    EIP_BANDWIDTH_HCLOUD_BIN   hcloud executable (default "hcloud")
    EIP_BANDWIDTH_HCLOUD_ARGS  extra args injected before the EIP operation
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

SCRIPT_VERSION = "1.0.0"

DEFAULT_REGION = "cn-north-4"
DEFAULT_LIMIT = 10
MAX_PAGES = 100
SERVICE = "EIP"
ALLOWED_OPERATIONS = ("ListBandwidths", "ShowBandwidth")
LIST_OPERATION = "ListBandwidths"
SHOW_OPERATION = "ShowBandwidth"
LIST_REST_PATH = "/v3/{project_id}/eip/bandwidths"
SHOW_REST_PATH = "/v3/{project_id}/eip/bandwidths/{bandwidth_id}"

DEFAULT_FILENAME_PREFIX = "eip_bandwidth_list"
MD_TITLE = "华为云 EIP 带宽列表"
MD_DETAIL_TITLE = "华为云 EIP 带宽明细"

MD_COLUMNS = (
    ("带宽名称", ("name",)),
    ("带宽 ID", ("id",)),
    ("大小(Mbit/s)", ("size",)),
    ("共享类型", ("share_type",)),
    ("计费方式", ("charge_mode",)),
    ("关联公网 IP 数", ("publicip_info_count",)),
    ("状态", ("status",)),
    ("企业项目 ID", ("enterprise_project_id",)),
    ("创建时间", ("created_at",)),
)

DETAIL_IP_COLUMNS = (
    ("公网 IP", ("publicip_address",)),
    ("公网 IP ID", ("publicip_id",)),
    ("类型", ("publicip_type",)),
    ("IP 版本", ("ip_version",)),
)

_VALUE_STRIPPED_FLAGS = ("--output", "-o")

WRITE_INTENT_KEYWORDS = (
    "createbandwidth",
    "batchcreatebandwidths",
    "deletebandwidth",
    "batchdeletebandwidths",
    "updatebandwidth",
    "batchupdatebandwidths",
    "changebandwidth",
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
    "sharebandwidth",
    "creating",
    "deleting",
    "updating",
    "associating",
    "start",
    "stop",
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

_NOT_FOUND_PATTERNS = (
    "404",
    "not found",
    "notfound",
    "not exist",
    "does not exist",
    "不存在",
)

# KooCLI prints usage errors on stdout with exit code 0.
_USE_ERROR_MARKER = "[use_error]"

# KooCLI also prints an API error body on stdout with exit code 0, e.g.
# {"code": "VPC.0305", "message": "...No Eip bandwidth exist with id ..."}.
# These must be classified from the parsed payload, not from the exit code.
_API_ERROR_BODY_MARKERS = ("noeipbandwidthexist", "not exist", "not found",
                           "不存在", "permission denied", "forbidden")
_API_NOT_FOUND_CODES = ("vpc.0305",)
_API_AUTH_CODES = ("apigw.0301", "apigw.0302", "apigw.0303")

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


class BandwidthListError(Exception):
    """Base error for the EIP bandwidth list skill."""


class GuardError(BandwidthListError):
    """A write intent was detected and blocked (skill is read-only)."""


class ConfigError(BandwidthListError):
    """hcloud/SDK missing or credentials (AK/SK) not configured."""


class AuthError(BandwidthListError):
    """Authentication/authorization failure (invalid AK/SK or IAM 403)."""


class ApiError(BandwidthListError):
    """hcloud / network / unexpected API failure."""


class ExportError(BandwidthListError):
    """The local Markdown file could not be created or written."""


def guard_text_from_argv(argv):
    """Build the text scanned by the write-intent guard.

    Only values of the local output flags (``--output`` / ``-o``) are stripped,
    since they are file paths that may legitimately contain write-looking
    words. A following flag is never swallowed.
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
    """Raise GuardError when `text` carries a mutating bandwidth intent."""
    low = re.sub(r"[\s_\-]+", "", str(text).lower())
    for keyword in WRITE_INTENT_KEYWORDS:
        if keyword in low:
            raise GuardError(
                "检测到写操作意图（关键词: %s）。本 skill 仅支持只读查询"
                "（EIP ListBandwidths / ShowBandwidth），创建/修改/删除带宽、"
                "变更计费模式、绑定/解绑公网 IP 的变更操作已被守卫拦截。" % keyword
            )
    return False


def guard_operation(operation):
    """Only ListBandwidths / ShowBandwidth (both read-only GET) may run."""
    if operation not in ALLOWED_OPERATIONS:
        raise GuardError(
            "不允许的操作 %r：本 skill 仅允许只读操作 %s。"
            % (operation, " / ".join(ALLOWED_OPERATIONS))
        )
    return True


def build_list_command(region, share_type=None, enterprise_project_id=None,
                       limit=DEFAULT_LIMIT, marker=None):
    """Build `hcloud EIP ListBandwidths` argv (without the executable).

    Parameter list verified live against KooCLI 7.3.12:
    --cli-region / --project_id / --enterprise_project_id / --limit / --marker
    / --share_type (WHOLE|PER). All are scalar query parameters.
    """
    argv = [
        SERVICE,
        LIST_OPERATION,
        "--cli-region=%s" % region,
        "--limit=%d" % limit,
    ]
    if marker:
        argv.append("--marker=%s" % marker)
    if share_type:
        argv.append("--share_type=%s" % share_type)
    if enterprise_project_id:
        argv.append("--enterprise_project_id=%s" % enterprise_project_id)
    return argv


def build_show_command(region, bandwidth_id):
    """Build `hcloud EIP ShowBandwidth` argv (without the executable).

    Verified live params: --cli-region / --bandwidth_id / --project_id.
    """
    return [
        SERVICE,
        SHOW_OPERATION,
        "--cli-region=%s" % region,
        "--bandwidth_id=%s" % bandwidth_id,
    ]


def _hcloud_executable():
    return os.environ.get("EIP_BANDWIDTH_HCLOUD_BIN", "hcloud")


def run_hcloud(argv):
    """Execute hcloud and return (stdout, stderr, returncode)."""
    cmd = [_hcloud_executable()]
    extra = os.environ.get("EIP_BANDWIDTH_HCLOUD_ARGS", "").split()
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
            "或安装 huaweicloudsdkcore + huaweicloudsdkeip 以启用 SDK 回退，"
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


def classify_hcloud_failure(stdout, stderr, returncode, operation=LIST_OPERATION):
    """Map a failed hcloud invocation to a domain error with explicit hints."""
    blob = (stderr + " " + stdout).strip()
    low = blob.lower()
    if _USE_ERROR_MARKER in low:
        return ApiError(
            "hcloud 参数错误（KooCLI 拒绝了该参数组合，退出码 %s）：EIP %s "
            "真实参数清单可通过 `hcloud EIP %s --help` 查看。详情：%s"
            % (returncode, operation, operation, blob[:300])
        )
    if any(p in low for p in _CREDENTIAL_MISSING_PATTERNS) and not re.search(
            r"\b40[13]\b", blob):
        return ConfigError(
            "缺少 AK/SK 凭证：hcloud 未配置有效凭证。请先运行 hcloud configure 或"
            "设置凭证环境变量（严禁在对话中粘贴 AK/SK），参见"
            " references/cli-installation-guide.md。详情：%s" % blob[:300]
        )
    if any(p in low for p in _AUTH_PATTERNS):
        if operation == SHOW_OPERATION:
            permission_hint = "eip:bandwidths:get"
        else:
            permission_hint = "eip:bandwidths:list"
        return AuthError(
            "无权限访问 EIP 带宽（Bandwidth），请检查 IAM 权限（403：AK/SK 无效或"
            "未授予 %s），参见 references/iam-policies.md。详情：%s"
            % (permission_hint, blob[:300])
        )
    if operation == SHOW_OPERATION and any(p in low for p in _NOT_FOUND_PATTERNS):
        return ApiError(
            "带宽不存在或已删除（404）：请确认 --bandwidth-id 是否正确。"
            "可用 ListBandwidths 查询现有带宽 ID。详情：%s" % blob[:300]
        )
    return ApiError(
        "hcloud 调用失败（退出码 %s）：%s" % (returncode, blob[:300])
    )


def _api_error_fields(payload):
    """Return ``(code, message)`` from an embedded API error body, else (None, None)."""
    if not isinstance(payload, dict):
        return None, None
    code = payload.get("code") or payload.get("error_code")
    message = payload.get("message") or payload.get("error_msg")
    if not isinstance(code, str) or not code.strip():
        return None, None
    if message is None:
        message = ""
    elif not isinstance(message, str):
        message = json.dumps(message, ensure_ascii=False)
    return code.strip(), message.strip()


def classify_api_error_payload(payload, operation=LIST_OPERATION):
    """Map an API error body printed by KooCLI with exit code 0 to a domain error.

    KooCLI does not always use a non-zero exit code for API errors: for a
    non-existent bandwidth it prints ``{"code": "VPC.0305", "message": ...}``
    and exits 0. Without this check the payload silently parses to an empty
    object and the caller reports the generic "response is empty" hint.

    Returns the exception instance, or ``None`` when the payload is not an
    error body.
    """
    code, message = _api_error_fields(payload)
    if not code:
        return None
    low = ("%s %s" % (code, message)).lower()
    if code.lower() in _API_NOT_FOUND_CODES or any(
            marker in low for marker in _API_ERROR_BODY_MARKERS):
        if operation == SHOW_OPERATION:
            return ApiError(
                "带宽不存在或已删除（接口返回 %s）：请先不带 --bandwidth-id 运行 "
                "ListBandwidths 核对当前 Region 的带宽 ID，再用正确的 --bandwidth-id "
                "重试。详情：%s" % (code, message[:300])
            )
        return ApiError(
            "查询带宽列表时接口返回 %s：请确认 Region / 过滤条件，或检查 "
            "--bandwidth-id 对应的带宽是否存在。详情：%s"
            % (code, message[:300])
        )
    if code.lower() in _API_AUTH_CODES or any(
            marker in low for marker in ("forbidden", "permission denied",
                                         "认证失败", "权限不足")):
        permission_hint = ("eip:bandwidths:get" if operation == SHOW_OPERATION
                           else "eip:bandwidths:list")
        return AuthError(
            "无权限访问 EIP 带宽（Bandwidth）：接口返回 %s，请检查 IAM 权限"
            "（%s），参见 references/iam-policies.md。详情：%s"
            % (code, permission_hint, message[:300])
        )
    return ApiError(
        "EIP 接口返回错误（%s）：%s" % (code, message[:300] or "无错误详情")
    )


def extract_bandwidths(payload):
    """Pull the bandwidth list out of a ListBandwidths response."""
    if isinstance(payload, list):
        return payload
    for key in ("bandwidths", "bandWidths", "bandwidth"):
        value = payload.get(key)
        if isinstance(value, list):
            return value
    return []


def extract_bandwidth(payload):
    """Pull the single bandwidth object out of a ShowBandwidth response."""
    if not isinstance(payload, dict):
        return {}
    value = payload.get("bandwidth")
    if isinstance(value, dict):
        return value
    # Tolerate a response that returns the object at the top level.
    if "id" in payload:
        return payload
    return {}


def _next_marker(payload):
    """Read next_marker from a page_info object when the API returns one."""
    if not isinstance(payload, dict):
        return None
    page_info = payload.get("page_info") or payload.get("pageInfo")
    if isinstance(page_info, dict):
        marker = page_info.get("next_marker") or page_info.get("nextMarker")
        if marker:
            return str(marker)
    return None


def _last_id(batch):
    if not batch:
        return None
    last = batch[-1]
    if isinstance(last, dict):
        value = last.get("id")
        if value:
            return str(value)
    return None


def _jsonable(value):
    return json.loads(json.dumps(value, ensure_ascii=False, default=str))


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


def _sdk_paged_list(client, ListBandwidthsRequest, limit, share_type,
                    enterprise_project_id, max_pages):
    bandwidths = []
    marker = None
    for _ in range(max_pages):
        request = ListBandwidthsRequest(
            limit=limit,
            marker=marker,
            share_type=share_type,
            enterprise_project_id=enterprise_project_id,
        )
        try:
            response = client.list_bandwidths(request)
        except Exception as exc:
            low = str(exc).lower()
            if any(p in low for p in _AUTH_PATTERNS):
                raise AuthError(
                    "无权限访问 EIP 带宽（Bandwidth），请检查 IAM 权限"
                    "（eip:bandwidths:list，403）。详情：%s" % str(exc)[:300]
                )
            raise ApiError("SDK 调用失败：%s" % str(exc)[:300])
        batch = list(getattr(response, "bandwidths", None) or [])
        bandwidths.extend(
            _jsonable(item.to_dict()) if hasattr(item, "to_dict") else _jsonable(item)
            for item in batch
        )
        page_info = getattr(response, "page_info", None)
        next_marker = getattr(page_info, "next_marker", None) if page_info else None
        if next_marker:
            marker = str(next_marker)
            continue
        if len(batch) < limit:
            break
        marker = _last_id(_jsonable([i.to_dict() if hasattr(i, "to_dict") else i
                                     for i in batch]))
        if not marker:
            break
    else:
        raise ApiError("翻页超过 %d 页仍未取完，已中止以防死循环。" % max_pages)
    return bandwidths


def _build_sdk_client(region, project_id):
    try:
        from huaweicloudsdkcore.auth.credentials import BasicCredentials
        from huaweicloudsdkcore.region.region import Region
        from huaweicloudsdkcore.http.http_config import HttpConfig
        from huaweicloudsdkeip.v3 import EipClient
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
            "SDK 回退缺少 project_id：EIP 带宽的 REST 路径为 %s，需要项目 ID。"
            "请通过 --project-id 传入，或设置 HUAWEICLOUD_SDK_PROJECT_ID / "
            "HUAWEI_PROJECT_ID（严禁在对话中粘贴敏感信息）。" % LIST_REST_PATH
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
    except Exception as exc:
        raise ConfigError(
            "SDK 初始化失败（region=%s）：%s。请检查 huaweicloudsdkeip 安装与区域配置。"
            % (region, exc)
        )
    return client


def list_bandwidths_via_sdk(region, share_type=None, enterprise_project_id=None,
                            limit=DEFAULT_LIMIT, project_id=None,
                            max_pages=MAX_PAGES):
    """SDK fallback: query bandwidths through `huaweicloudsdkeip` v3."""
    try:
        from huaweicloudsdkeip.v3 import ListBandwidthsRequest
    except ImportError as exc:
        raise ConfigError(
            "未找到 hcloud（KooCLI），且 huaweicloudsdkcore/huaweicloudsdkeip 未安装，"
            "无法回退到 SDK。请安装 KooCLI 或 pip install huaweicloudsdkcore "
            "huaweicloudsdkeip。详情：%s" % exc
        )
    client = _build_sdk_client(region, project_id)
    return _sdk_paged_list(client, ListBandwidthsRequest, limit, share_type,
                           enterprise_project_id, max_pages)


def show_bandwidth_via_sdk(region, bandwidth_id, project_id=None):
    """SDK fallback: show one bandwidth through `huaweicloudsdkeip` v3."""
    try:
        from huaweicloudsdkeip.v3 import ShowBandwidthRequest
    except ImportError as exc:
        raise ConfigError(
            "未找到 hcloud（KooCLI），且 huaweicloudsdkcore/huaweicloudsdkeip 未安装，"
            "无法回退到 SDK。请安装 KooCLI 或 pip install huaweicloudsdkcore "
            "huaweicloudsdkeip。详情：%s" % exc
        )
    client = _build_sdk_client(region, project_id)
    try:
        response = client.show_bandwidth(ShowBandwidthRequest(bandwidth_id=bandwidth_id))
    except Exception as exc:
        low = str(exc).lower()
        if any(p in low for p in _AUTH_PATTERNS):
            raise AuthError(
                "无权限访问 EIP 带宽（Bandwidth），请检查 IAM 权限"
                "（eip:bandwidths:get，403）。详情：%s" % str(exc)[:300]
            )
        if any(p in low for p in _NOT_FOUND_PATTERNS):
            raise ApiError(
                "带宽不存在或已删除（404）：请确认 --bandwidth-id 是否正确。详情：%s"
                % str(exc)[:300]
            )
        raise ApiError("SDK 调用失败：%s" % str(exc)[:300])
    bandwidth = getattr(response, "bandwidth", None)
    if bandwidth is None:
        return {}
    return _jsonable(bandwidth.to_dict()) if hasattr(bandwidth, "to_dict") else _jsonable(bandwidth)


def list_bandwidths(region, share_type=None, enterprise_project_id=None,
                    limit=DEFAULT_LIMIT, project_id=None, max_pages=MAX_PAGES):
    """Query all bandwidths (marker-paged); KooCLI first, SDK fallback."""
    bandwidths = []
    marker = None
    for _page in range(max_pages):
        argv = build_list_command(region, share_type=share_type,
                                  enterprise_project_id=enterprise_project_id,
                                  limit=limit, marker=marker)
        try:
            stdout, stderr, returncode = run_hcloud(argv)
        except ConfigError:
            return list_bandwidths_via_sdk(
                region, share_type=share_type,
                enterprise_project_id=enterprise_project_id,
                limit=limit, project_id=project_id, max_pages=max_pages,
            )
        if returncode != 0 or _USE_ERROR_MARKER in (stdout + " " + stderr).lower():
            raise classify_hcloud_failure(stdout, stderr, returncode, LIST_OPERATION)
        payload = extract_json(stdout)
        api_error = classify_api_error_payload(payload, LIST_OPERATION)
        if api_error is not None:
            raise api_error
        batch = extract_bandwidths(payload)
        bandwidths.extend(batch)
        next_marker = _next_marker(payload)
        if next_marker:
            marker = next_marker
            continue
        if len(batch) < limit or not batch:
            break
        marker = _last_id(batch)
        if not marker:
            break
    else:
        raise ApiError("翻页超过 %d 页仍未取完，已中止以防死循环。" % max_pages)
    return bandwidths


def show_bandwidth(region, bandwidth_id, project_id=None):
    """Query one bandwidth; KooCLI first, SDK fallback."""
    argv = build_show_command(region, bandwidth_id)
    try:
        stdout, stderr, returncode = run_hcloud(argv)
    except ConfigError:
        return show_bandwidth_via_sdk(region, bandwidth_id, project_id=project_id)
    if returncode != 0 or _USE_ERROR_MARKER in (stdout + " " + stderr).lower():
        raise classify_hcloud_failure(stdout, stderr, returncode, SHOW_OPERATION)
    payload = extract_json(stdout)
    api_error = classify_api_error_payload(payload, SHOW_OPERATION)
    if api_error is not None:
        raise api_error
    bandwidth = extract_bandwidth(payload)
    if not bandwidth:
        raise ApiError(
            "未取到带宽 %s 的明细：接口响应中既没有 bandwidth 对象也没有 id 字段，"
            "请先用 ListBandwidths 核对当前 Region 的带宽 ID。响应摘录：%s"
            % (bandwidth_id, json.dumps(payload, ensure_ascii=False)[:300])
        )
    return bandwidth


def normalize_bandwidth(bandwidth):
    """Flatten a bandwidth record into stable, renderable key/value pairs."""
    flat = dict(bandwidth)
    publicips = bandwidth.get("publicip_info") or []
    if not isinstance(publicips, list):
        publicips = []
    flat["publicip_info_count"] = len(publicips)
    flat["publicip_info"] = publicips
    return flat


def _field(record, *names, default="-"):
    for name in names:
        if name in record and record[name] not in (None, ""):
            return record[name]
    return default


def _cell(value):
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return str(value)


def _render_fixed_table(columns, records):
    rows = [[_cell(_field(record, *keys)) for _, keys in columns] for record in records]
    headers = [label for label, _ in columns]
    widths = [max(len(headers[i]), *(len(row[i]) for row in rows)) for i in range(len(headers))]
    lines = [
        "  ".join(headers[i].ljust(widths[i]) for i in range(len(headers))),
        "  ".join("-" * width for width in widths),
    ]
    for row in rows:
        lines.append("  ".join(row[i].ljust(widths[i]) for i in range(len(headers))))
    return "\n".join(lines)


def render_table(bandwidths):
    """Render the fixed-header list table (name/id/size/share_type/...)."""
    records = [normalize_bandwidth(bandwidth) for bandwidth in bandwidths]
    return _render_fixed_table(MD_COLUMNS, records)


def render_detail(bandwidth, region=None):
    """Render a detailed text view: summary + public IPs + bandwidth rules."""
    record = normalize_bandwidth(bandwidth)
    lines = []
    if region:
        lines.append("Region %s 的 EIP 带宽明细（%s）：" % (region, _field(record, "id")))
    else:
        lines.append("EIP 带宽明细（%s）：" % _field(record, "id"))
    lines.append(_render_fixed_table(MD_COLUMNS, [record]))
    lines.append("")
    lines.append("关联公网 IP（%d）：" % record["publicip_info_count"])
    publicips = record["publicip_info"]
    if publicips:
        lines.append(_render_fixed_table(DETAIL_IP_COLUMNS, publicips))
    else:
        lines.append("  ".join(label for label, _ in DETAIL_IP_COLUMNS))
        lines.append("无数据")
    lines.append("")
    lines.append("带宽规则：")
    lines.append("- 规则配额（rule_quota）：%s" % _field(record, "rule_quota"))
    lines.append("- 启用带宽规则（enable_bandwidth_rules）：%s"
                 % _field(record, "enable_bandwidth_rules"))
    rules = record.get("bandwidth_rules")
    if rules:
        lines.append("- 规则（bandwidth_rules）：%s" % _cell(rules))
    else:
        lines.append("- 规则（bandwidth_rules）：无")
    return "\n".join(lines)


def active_filter_descriptions(share_type=None, enterprise_project_id=None):
    filters = []
    if share_type:
        filters.append("share_type=%s" % share_type)
    if enterprise_project_id:
        filters.append("enterprise_project_id=%s" % enterprise_project_id)
    return filters


def empty_message(region, share_type=None, enterprise_project_id=None):
    """Explicit empty-result hint, distinguishing overall vs filtered-empty."""
    if share_type == "WHOLE":
        base = "当前 region（%s）无 share_type=WHOLE 的带宽（共享带宽）数据" % region
    elif share_type == "PER":
        base = "当前 region（%s）无 share_type=PER 的带宽（独占带宽）数据" % region
    else:
        base = "当前 region（%s）无带宽（Bandwidth）数据" % region
    if enterprise_project_id:
        base += "（企业项目 %s）" % enterprise_project_id
    return base + "。"


def _md_cell(value):
    if value is None or value == "":
        return "-"
    if isinstance(value, (dict, list)):
        value = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    text = str(value).replace("\r\n", " ").replace("\n", " ")
    text = text.replace("\r", " ").replace("|", "\\|")
    return text or "-"


def _generated_at():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _markdown_table(columns, records):
    lines = [
        "| " + " | ".join(label for label, _ in columns) + " |",
        "| " + " | ".join(["---"] * len(columns)) + " |",
    ]
    for record in records:
        lines.append("| " + " | ".join(
            _md_cell(_field(record, *keys)) for _, keys in columns) + " |")
    return lines


def render_markdown(bandwidths, region=None, generated_at=None, filters=None):
    """Render the bandwidth list as a Markdown report (empty → 表头 + 无数据)."""
    records = [normalize_bandwidth(bandwidth) for bandwidth in bandwidths]
    generated_at = generated_at or _generated_at()
    region_label = region or "-"

    lines = [
        "# %s" % MD_TITLE,
        "",
        "> 查询区域：%s | 生成时间：%s | 记录数：%d"
        % (region_label, generated_at, len(records)),
    ]
    if filters:
        lines.append("> 过滤条件：%s" % ", ".join(filters))
    lines.append("")
    lines.extend(_markdown_table(MD_COLUMNS, records))
    if not records:
        lines += ["", "> 无数据：%s" % empty_message(region_label, *filters_to_args(filters))]
    lines.append("")
    return "\n".join(lines)


def filters_to_args(filters):
    """Best-effort reverse mapping of filter descriptions to empty_message args."""
    share_type = None
    enterprise_project_id = None
    for item in filters or []:
        if item.startswith("share_type="):
            share_type = item.split("=", 1)[1]
        elif item.startswith("enterprise_project_id="):
            enterprise_project_id = item.split("=", 1)[1]
    return share_type, enterprise_project_id


def render_markdown_detail(bandwidth, region=None, generated_at=None):
    """Render one bandwidth detail as a Markdown report."""
    record = normalize_bandwidth(bandwidth)
    generated_at = generated_at or _generated_at()
    region_label = region or "-"
    lines = [
        "# %s" % MD_DETAIL_TITLE,
        "",
        "> 查询区域：%s | 生成时间：%s | 带宽 ID：%s"
        % (region_label, generated_at, _field(record, "id")),
        "",
        "## 带宽概要",
        "",
    ]
    lines.extend(_markdown_table(MD_COLUMNS, [record]))
    lines += ["", "## 关联公网 IP（%d）" % record["publicip_info_count"], ""]
    publicips = record["publicip_info"]
    lines.extend(_markdown_table(DETAIL_IP_COLUMNS, publicips))
    if not publicips:
        lines += ["", "无数据。"]
    lines += ["", "## 带宽规则", ""]
    lines.append("- 规则配额（rule_quota）：%s" % _md_cell(_field(record, "rule_quota")))
    lines.append("- 启用带宽规则（enable_bandwidth_rules）：%s"
                 % _md_cell(_field(record, "enable_bandwidth_rules")))
    rules = record.get("bandwidth_rules")
    lines.append("- 规则（bandwidth_rules）：%s" % (_md_cell(rules) if rules else "无"))
    lines.append("")
    return "\n".join(lines)


def default_output_path(region):
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return "%s_%s_%s.md" % (DEFAULT_FILENAME_PREFIX, region, stamp)


def _atomic_write(text, output_path):
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
    try:
        fd, tmp_path = tempfile.mkstemp(
            prefix=".%s." % DEFAULT_FILENAME_PREFIX, suffix=".tmp",
            dir=output_dir or ".")
        os.close(fd)
    except (OSError, ValueError) as exc:
        raise ExportError("Markdown 临时文件创建失败：%s（%s）" % (output_path, exc))
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
        raise ExportError("Markdown 文件写出失败：%s（%s）" % (output_path, exc))
    return output_path


def export_markdown(bandwidths, output_path, region=None, generated_at=None,
                    filters=None):
    """Write the bandwidth list as a Markdown report (atomic write)."""
    text = render_markdown(bandwidths, region=region,
                           generated_at=generated_at, filters=filters)
    return _atomic_write(text, output_path)


def export_markdown_detail(bandwidth, output_path, region=None, generated_at=None):
    """Write one bandwidth detail as a Markdown report (atomic write)."""
    text = render_markdown_detail(bandwidth, region=region, generated_at=generated_at)
    return _atomic_write(text, output_path)


def _resolve_format(args):
    if args.output:
        return "md"
    if args.format == "md":
        return "md"
    if args.as_json:
        return "json"
    return args.format


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="查询华为云 EIP 带宽（Bandwidth）列表 / 明细"
                    "（KooCLI hcloud EIP ListBandwidths / ShowBandwidth，只读）。")
    parser.add_argument("-r", "--region", default=DEFAULT_REGION,
                        help="目标 Region（默认 %s）" % DEFAULT_REGION)
    parser.add_argument("--bandwidth-id", dest="bandwidth_id", default=None,
                        help="按带宽 ID 查询单条明细（切换为 ShowBandwidth）")
    parser.add_argument("--share-type", dest="share_type", default=None,
                        choices=("PER", "WHOLE"),
                        help="按共享类型过滤（服务端参数）：PER 独占 / WHOLE 共享")
    parser.add_argument("--enterprise-project-id", dest="enterprise_project_id",
                        default=None,
                        help="按企业项目 ID 过滤（服务端参数；0 = 默认企业项目，all_granted_eps = 全部）")
    parser.add_argument("--limit", type=int, default=DEFAULT_LIMIT,
                        help="分页大小（默认 %d）" % DEFAULT_LIMIT)
    parser.add_argument("--json", action="store_true", dest="as_json",
                        help="以 JSON 输出原始响应（列表为数组，明细为对象）")
    parser.add_argument("--format", choices=("table", "json", "md"),
                        default="table", dest="format",
                        help="输出形态：table（默认）/ json / md")
    parser.add_argument("-o", "--output", dest="output", default=None,
                        help="Markdown 输出路径（隐含 --format md；缺省为 "
                             "%s_<region>_<timestamp>.md）" % DEFAULT_FILENAME_PREFIX)
    parser.add_argument("--project-id", dest="project_id", default=None,
                        help="项目 ID（可选；SDK 回退在 /v3/{project_id}/... 路径中需要）")
    parser.add_argument("--operation", default=LIST_OPERATION,
                        help="hcloud EIP 操作名（仅允许 %s）"
                             % " / ".join(ALLOWED_OPERATIONS))
    args = parser.parse_args(argv)

    try:
        guard_write_intent(guard_text_from_argv(argv))
        guard_operation(args.operation)
        if args.bandwidth_id:
            guard_write_intent(args.bandwidth_id)
        if args.limit < 1:
            raise ApiError("--limit 必须为正整数（默认 %d）。" % DEFAULT_LIMIT)
        if args.bandwidth_id:
            bandwidth = show_bandwidth(
                args.region, args.bandwidth_id, project_id=args.project_id)
            if not bandwidth:
                raise ApiError(
                    "未取到带宽 %s 的明细（响应为空）。" % args.bandwidth_id)
        else:
            bandwidths = list_bandwidths(
                args.region,
                share_type=args.share_type,
                enterprise_project_id=args.enterprise_project_id,
                limit=args.limit,
                project_id=args.project_id,
            )
    except BandwidthListError as exc:
        print("[错误] %s" % exc, file=sys.stderr)
        return 1

    output_format = _resolve_format(args)
    filters = active_filter_descriptions(args.share_type, args.enterprise_project_id)

    if output_format == "md":
        output_path = args.output or default_output_path(args.region)
        try:
            if args.bandwidth_id:
                written = export_markdown_detail(
                    bandwidth, output_path, region=args.region)
                print("已生成 EIP 带宽明细 Markdown 报表（Region %s，带宽 %s）：%s"
                      % (args.region, args.bandwidth_id, written))
            else:
                written = export_markdown(
                    bandwidths, output_path, region=args.region, filters=filters)
                if bandwidths:
                    print("已生成 EIP 带宽列表 Markdown 报表（Region %s，共 %d 条记录）：%s"
                          % (args.region, len(bandwidths), written))
                else:
                    print("%s已生成 Markdown 文件（标注「无数据」，共 0 条）：%s"
                          % (empty_message(args.region, args.share_type,
                                           args.enterprise_project_id),
                             written))
        except BandwidthListError as exc:
            print("[错误] %s" % exc, file=sys.stderr)
            return 1
        return 0

    if output_format == "json":
        if args.bandwidth_id:
            print(json.dumps(bandwidth, ensure_ascii=False, indent=2))
        else:
            print(json.dumps(bandwidths, ensure_ascii=False, indent=2))
        return 0

    if args.bandwidth_id:
        print(render_detail(bandwidth, region=args.region))
        return 0

    if not bandwidths:
        print(empty_message(args.region, args.share_type, args.enterprise_project_id))
        return 0

    print("Region %s 的 EIP 带宽（Bandwidth）列表（共 %d 个）："
          % (args.region, len(bandwidths)))
    print(render_table(bandwidths))
    return 0


if __name__ == "__main__":
    sys.exit(main())