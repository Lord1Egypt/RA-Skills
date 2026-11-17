#!/usr/bin/env python3
"""List Huawei Cloud DDS (Document Database Service) instances via KooCLI,
read-only.

Primary execution path is KooCLI:

    hcloud DDS ListInstances --cli-region=<region> --limit=<1..100> --offset=<n>

The operation is GET /v3/{project_id}/instances (verified against
the KooCLI `DDS ListInstances` help output on KooCLI 7.2.12: "Method: GET", and a live
read-only call returning `{"instances": [], "total_count": 0}`).

When the hcloud binary is not installed the script falls back to the official
SDK (huaweicloudsdkdds v3 `DdsClient.list_instances`); when the SDK is missing
too, the final fallback issues the same read-only
GET /v3/{project_id}/instances directly over HTTPS with local AK/SK signing.
Credentials are taken from the active KooCLI profile or a fixed whitelist of
AK/SK environment variable names — the script never reads, echoes or stores
secrets.

Output modes: default compact instance-name list, `--table` fixed-column table
(实例ID/名称/状态/引擎版本/规格/节点数/创建时间/模式, missing values rendered
as "-"), and `--json` raw instance array. A strict write-intent guard rejects
any mutating intent before a single command is executed: this skill is
strictly read-only.

Usage:
    python3 scripts/list_dds.py [--region cn-north-4] [--names-only|--table|--json]
                                [--name demo] [--fuzzy] [--instance-id <id>]
                                [--mode Sharding|ReplicaSet|Single]
                                [--datastore-type DDS-Community]
                                [--vpc-id <id>] [--subnet-id <id>] [--tags k=v]
                                [--status normal] [--limit 100] [--offset 0]
                                [--single-page] [--project-id <id>]

Environment overrides (test-only hooks — not user-facing options):
    DDS_LIST_HCLOUD_BIN   hcloud executable (default "hcloud")
    DDS_LIST_HCLOUD_ARGS  extra args injected before the DDS service/operation;
                          unit tests use it to simulate a foreign operation
    DDS_LIST_CLI_MODE     KooCLI auth mode used by --cli-mode when the API
                          `mode` filter is forwarded (default "AKSK")
"""

import argparse
import datetime
import hashlib
import hmac
import json
import os
import re
import subprocess
import sys
import unicodedata
import urllib.error
import urllib.parse
import urllib.request

DEFAULT_REGION = "cn-north-4"
DEFAULT_LIMIT = 100         # server-side maximum page size for DDS ListInstances
MAX_LIMIT = 100
DEFAULT_MAX_PAGES = 50
REST_PATH = "/v3/{project_id}/instances"
REST_TIMEOUT = 120
SIGN_ALGORITHM = "SDK-HMAC-SHA256"

SERVICE_NAME = "DDS"
ALLOWED_OPERATIONS = ("ListInstances",)

# Server-side query parameters, verified via the KooCLI DDS ListInstances help output.
# NOTE: there is NO server-side --status parameter on this API — the --status
# filter of this script is applied client-side after the pages are fetched.
SERVER_FILTER_PARAMS = ("id", "mode", "name", "datastore_type", "subnet_id",
                        "vpc_id")

# Human-readable names for the instance `type`/`mode` values.
TYPE_LABELS = {
    "Sharding": "集群",
    "ReplicaSet": "副本集",
    "Single": "单节点",
}

# Mutating DDS intents — strictly rejected by the guard. Gerund forms such as
# CREATING / DELETING / RESIZING are legitimate *status* values and therefore
# are deliberately not listed here.
#
# Verbs are matched against whole tokens (separator- and camelCase-normalized),
# so legitimate read-only filter values such as `--name checkpoint-demo` or
# `--name dds-copy-01` are not mis-flagged. Compound operation names
# (CreateInstance, StopInstance, UnbindEip, ...) are matched as substrings of
# the separator-normalized text, which is unambiguous for long keywords.
WRITE_INTENT_KEYWORDS = (
    "createinstance",
    "deleteinstance",
    "batchdelete",
    "restartinstance",
    "resizeinstance",
    "scaleinstance",
    "modifyinstance",
    "updateinstance",
    "switchinstance",
    "startupinstance",
    "stopinstance",
    "create",
    "delete",
    "drop",
    "update",
    "modify",
    "resize",
    "scale",
    "restart",
    "reboot",
    "restore",
    "backup",
    "freeze",
    "unfreeze",
    "release",
    "terminate",
    "destroy",
    "upgrade",
    "rollback",
    "migrate",
    "reset",
    "attach",
    "unbind",
    "unbindeip",
    "configure",
    "kill",
)

# Keywords matched as plain substrings of the separator-normalized text. Only
# long, unambiguous operation names qualify; short verbs would otherwise hit
# ordinary words ("check" in checkpoint-demo, "copy" in dds-copy-01).
SUBSTRING_KEYWORDS = tuple(k for k in WRITE_INTENT_KEYWORDS if len(k) >= 8)

# Options whose value is read-only filter data (instance name, IDs, state,
# paging, ...). Their values are data, not commands: an instance legitimately
# named `create-me` must not trip the guard. Only option names and
# standalone/operation positions are scanned — never these values.
READONLY_VALUE_OPTIONS = (
    "-r", "--region",
    "--name", "--instance-id", "--mode", "--datastore-type",
    "--vpc-id", "--subnet-id", "--tags", "--status",
    "--limit", "--offset", "--max-pages", "--project-id",
)

# Fixed table columns: (header, candidate field names). Ordered per the
# Issue #163 spec: 实例ID/名称/状态/引擎版本/规格/节点数/创建时间/模式.
# The candidates follow the official ListInstances response
# (GET /v3/{project_id}/instances -> QueryInstanceResponse): instance creation
# time is `created` (`updated` for the update time), the instance type is `mode`
# (there is no top-level `type`), the flavor spec lives under
# `groups[].nodes[].spec_code` and the node count is the number of
# `groups[].nodes[]` entries — resolved by `_engine_version`,
# `_flavor_spec_code` and `_node_count`.
TABLE_COLUMNS = (
    ("实例ID", ("id", "instance_id")),
    ("名称", ("name",)),
    ("状态", ("status",)),
    ("引擎版本", ("version",)),
    ("规格", ("spec_code",)),
    ("节点数", ("node_count",)),
    ("创建时间", ("created", "created_at")),
    ("模式", ("mode", "type")),
)

_INSTANCE_LIST_KEYS = ("instances",)

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


class DdsListError(Exception):
    """Base error for the DDS list skill."""


class GuardError(DdsListError):
    """A write intent was detected and blocked (skill is read-only)."""


class ConfigError(DdsListError):
    """hcloud missing / credentials (AK/SK) not configured / SDK unavailable."""


class HcloudMissingError(ConfigError):
    """The hcloud executable is not installed (triggers the SDK fallback)."""


class AuthError(DdsListError):
    """Authentication/authorization failure (invalid AK/SK or IAM 403)."""


class ApiError(DdsListError):
    """hcloud / network / unexpected API failure."""


def _guard_tokens(text):
    """Split text into lowercase alphanumeric tokens (separator + camelCase).

    `--create-instance`, `create_instance`, `CreateInstance` and `CREATE-INSTANCE`
    all yield the tokens ("create", "instance"), while ordinary words stay
    whole ("checkpoint-demo" -> "checkpoint", "demo").
    """
    spaced = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", str(text))
    return re.findall(r"[a-z0-9]+", spaced.lower())


def _guard_segments(text):
    """Return the command-line positions the guard must scan.

    A write verb is only meaningful as an operation / option name, never as a
    read-only filter *value* (an instance named `create-me` is still an
    instance). Values of `READONLY_VALUE_OPTIONS` passed as a separate
    argument and the value half of `--flag=value` are therefore dropped;
    everything else — option names, standalone operation words and positional
    arguments — is kept for the verb scan.
    """
    words = str(text).split()
    segments = []
    skip_next = False
    for word in words:
        if skip_next:
            skip_next = False
            continue
        if word.startswith("-") and "=" in word:
            segments.append(word.split("=", 1)[0])
            continue
        if word in READONLY_VALUE_OPTIONS:
            skip_next = True
            continue
        segments.append(word)
    return segments


def guard_write_intent(text):
    """Return False for read-only text; raise GuardError if `text` is mutating.

    Verbs are matched against whole tokens so legitimate read-only values
    (`--name checkpoint-demo`, `--name create-me`) are not mis-flagged, and
    long compound operation names are matched against the separator-normalized
    text so `CreateInstance` / `StopInstance` are caught. Read-only vocabulary
    (list/show/get/describe) never matches. Values of read-only filter options
    are exempt from the verb scan by `_guard_segments`.
    """
    raw = " ".join(_guard_segments(text))
    low = re.sub(r"[\s_\-]+", "", raw.lower())
    tokens = set(_guard_tokens(raw))
    for keyword in WRITE_INTENT_KEYWORDS:
        hit = keyword in tokens
        if not hit and keyword in SUBSTRING_KEYWORDS:
            hit = keyword in low
        if hit:
            raise GuardError(
                "检测到写操作意图（关键词: %s）。本 skill 仅支持只读查询"
                "（DDS ListInstances），创建/删除/重启/扩缩容/备份等变更操作"
                "已被守卫拦截。" % keyword
            )
    return False


def guard_operation(operation):
    """Only the read-only list operation may run."""
    if operation not in ALLOWED_OPERATIONS:
        raise GuardError(
            "不允许的操作 %r：本 skill 仅允许只读操作 %s。"
            % (operation, "/".join(ALLOWED_OPERATIONS))
        )
    return True


def build_command(region, name=None, instance_id=None, mode=None,
                  datastore_type=None, vpc_id=None, subnet_id=None, tags=None,
                  limit=DEFAULT_LIMIT, offset=0, project_id=None, fuzzy=False,
                  cli_mode="AKSK"):
    """Build the hcloud argv (without the executable) for one page.

    Mirrors the real KooCLI parameter list (DDS ListInstances help output):
    --project_id (path; resolved from the profile when omitted), --limit
    (1..100), --offset (>=0), --id, --mode (Sharding|ReplicaSet|Single), --name
    (leading `*` = fuzzy, otherwise exact), --datastore_type, --vpc_id,
    --subnet_id, --tags. No parameter outside that list is ever emitted, and
    no mutating flag exists in this function.

    The API parameter `mode` collides with the KooCLI system parameter
    `--mode` (authentication mode). KooCLI resolves the ambiguity by taking
    `--cli-mode` for the system parameter, so whenever `mode` is forwarded the
    command also carries `--cli-mode=<cli_mode>` (the active auth mode,
    default AKSK). See references/cli-installation-guide.md.
    """
    if mode and mode not in ("Sharding", "ReplicaSet", "Single"):
        raise ApiError(
            "--mode 仅支持 Sharding / ReplicaSet / Single：%r" % mode
        )
    if datastore_type and datastore_type not in ("DDS-Community", "DDS-Enhanced"):
        raise ApiError(
            "--datastore-type 仅支持 DDS-Community / DDS-Enhanced：%r"
            % datastore_type
        )
    argv = [
        SERVICE_NAME,
        "ListInstances",
        "--cli-region=%s" % region,
        "--limit=%d" % limit,
        "--offset=%d" % offset,
    ]
    if project_id:
        argv.append("--project_id=%s" % project_id)
    if instance_id:
        argv.append("--id=%s" % instance_id)
    if mode:
        argv.append("--cli-mode=%s" % cli_mode)
        argv.append("--mode=%s" % mode)
    if name:
        argv.append("--name=%s" % ("*%s" % name if fuzzy else name))
    if datastore_type:
        argv.append("--datastore_type=%s" % datastore_type)
    if vpc_id:
        argv.append("--vpc_id=%s" % vpc_id)
    if subnet_id:
        argv.append("--subnet_id=%s" % subnet_id)
    if tags:
        argv.append("--tags=%s" % tags)
    return argv


def _hcloud_executable():
    return os.environ.get("DDS_LIST_HCLOUD_BIN", "hcloud")


def run_hcloud(argv):
    """Execute hcloud and return (stdout, stderr, returncode)."""
    cmd = [_hcloud_executable()]
    extra = os.environ.get("DDS_LIST_HCLOUD_ARGS", "").split()
    if extra:
        cmd.extend(extra)
    cmd.extend(argv)
    try:
        proc = subprocess.run(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            timeout=120, universal_newlines=True,
        )
    except FileNotFoundError:
        raise HcloudMissingError(
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
            "hcloud 参数错误（KooCLI 拒绝了该参数组合，退出码 %s）："
            "真实参数清单可通过 DDS ListInstances 的 --help 查看。详情：%s"
            % (returncode, blob[:300])
        )
    if any(p in low for p in _CREDENTIAL_MISSING_PATTERNS) and not re.search(
            r"\b40[13]\b", blob):
        return ConfigError(
            "缺少 AK/SK 凭证：hcloud 未配置有效凭证。请先运行 hcloud configure "
            "或设置凭证环境变量（严禁在对话中粘贴 AK/SK），参见 "
            "references/cli-installation-guide.md。详情：%s" % blob[:300]
        )
    if any(p in low for p in _AUTH_PATTERNS):
        return AuthError(
            "无权限访问文档数据库服务（DDS），请检查 IAM 权限"
            "（403：AK/SK 无效或未授予 DDS 只读权限 dds:instance:listAll），"
            "参见 references/iam-policies.md。详情：%s" % blob[:300]
        )
    return ApiError(
        "hcloud 调用失败（退出码 %s）：%s" % (returncode, blob[:300])
    )


def extract_instances(payload):
    """Pull the instance list out of a ListInstances response."""
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        for key in _INSTANCE_LIST_KEYS:
            value = payload.get(key)
            if isinstance(value, list):
                return value
    return []


def _total_count(payload):
    if isinstance(payload, dict):
        for key in ("total_count", "totalCount", "total"):
            if isinstance(payload.get(key), int):
                return payload[key]
    return None


def _has_more(batch, collected, limit, payload):
    """Decide whether another page should be fetched."""
    if not batch:
        return False
    total = _total_count(payload)
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
_PROJECT_ID_ENV_NAMES = (
    "HW_PROJECT_ID",
    "HUAWEI_PROJECT_ID",
    "HUAWEICLOUD_SDK_PROJECT_ID",
    "HUAWEI_CLOUD_PROJECT_ID",
)
_SECURITY_TOKEN_ENV_NAMES = (
    "HW_SECURITY_TOKEN",
    "HUAWEI_SECURITY_TOKEN",
    "HUAWEICLOUD_SDK_SECURITY_TOKEN",
    "HUAWEI_CLOUD_SECURITY_TOKEN",
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


def _jsonable(value):
    """Recursively convert datetimes (SDK to_dict output) to JSON-safe values."""
    return json.loads(json.dumps(value, ensure_ascii=False, default=str))


# ------------------------------------------------------------- REST fallback ---
#
# Third execution tier, used only when both KooCLI and the official SDK are
# unavailable. The request is the same read-only
# GET /v3/{project_id}/instances, signed locally with the AK/SK (SDK-HMAC-SHA256
# Signature V4); credentials come from the same whitelisted environment names
# as the SDK fallback. Only standard-library modules are used.

def _uri_encode(value):
    """RFC 3986 encoding as required by the Huawei Cloud canonical request."""
    return urllib.parse.quote(str(value), safe="-_.~")


def _canonical_query(params):
    """Sort and encode query parameters for the canonical request."""
    pairs = []
    for key in sorted(params):
        value = params[key]
        if value is None or value == "":
            continue
        pairs.append("%s=%s" % (_uri_encode(key), _uri_encode(value)))
    return "&".join(pairs)


def _sign_headers(method, path, query, host, ak, sk, security_token=None,
                  now=None):
    """Build the Signature V4 headers for one Huawei Cloud request.

    Returns a dict containing Host, X-Sdk-Date, the optional X-Security-Token
    and Authorization. The signature covers host + x-sdk-date (+
    x-security-token when a temporary AK/SK is used).
    """
    if not ak or not sk:
        raise ConfigError(
            "REST 兜底缺少 AK/SK 凭证：请设置 HUAWEI_ACCESS_KEY / "
            "HUAWEI_SECRET_KEY（或 HUAWEICLOUD_SDK_AK / HUAWEICLOUD_SDK_SK）"
            "环境变量，严禁在对话中粘贴 AK/SK。"
        )
    moment = now or datetime.datetime.now(datetime.timezone.utc)
    x_sdk_date = moment.strftime("%Y%m%dT%H%M%SZ")
    signed = {"host": host, "x-sdk-date": x_sdk_date}
    if security_token:
        signed["x-security-token"] = security_token
    names = sorted(signed)
    canonical_headers = "".join("%s:%s\n" % (name, signed[name])
                                for name in names)
    signed_headers = ";".join(names)
    payload_hash = hashlib.sha256(b"").hexdigest()
    canonical_request = "\n".join([
        method.upper(),
        path,
        _canonical_query(query),
        canonical_headers,
        signed_headers,
        payload_hash,
    ])
    string_to_sign = "\n".join([
        SIGN_ALGORITHM,
        x_sdk_date,
        hashlib.sha256(canonical_request.encode("utf-8")).hexdigest(),
    ])
    signature = hmac.new(
        sk.encode("utf-8"), string_to_sign.encode("utf-8"),
        hashlib.sha256).hexdigest()
    headers = {
        "Host": host,
        "X-Sdk-Date": x_sdk_date,
        "Authorization": "%s Access=%s, SignedHeaders=%s, Signature=%s"
                         % (SIGN_ALGORITHM, ak, signed_headers, signature),
        "Content-Type": "application/json",
    }
    if security_token:
        headers["X-Security-Token"] = security_token
    return headers


def build_rest_url(region, project_id, params=None):
    """Build the DDS ListInstances REST URL (GET /v3/{project_id}/instances)."""
    host = "dds.%s.myhuaweicloud.com" % region
    path = REST_PATH.format(project_id=project_id)
    query = _canonical_query(params or {})
    return "https://%s%s%s" % (host, path, ("?" + query) if query else "")


def _http_get_json(url, headers, timeout=REST_TIMEOUT):
    """GET `url` and decode the JSON body; map auth/network failures."""
    request = urllib.request.Request(url, headers=headers, method="GET")
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        raw = ""
        try:
            raw = exc.read().decode("utf-8", "replace")
        except Exception:  # pragma: no cover - body unreadable
            pass
        detail = raw or str(exc)
        blob = detail.lower()
        if exc.code in (401, 403) or any(p in blob for p in _AUTH_PATTERNS):
            raise AuthError(
                "无权限访问文档数据库服务（DDS），请检查 IAM 权限"
                "（HTTP %s：AK/SK 无效或未授予 dds:instance:list），"
                "参见 references/iam-policies.md。详情：%s"
                % (exc.code, detail[:300])
            )
        raise ApiError("DDS REST 调用失败（HTTP %s）：%s"
                       % (exc.code, detail[:300]))
    except urllib.error.URLError as exc:
        raise ApiError("DDS REST 调用失败（网络错误）：%s" % str(exc)[:300])
    try:
        return json.loads(body)
    except json.JSONDecodeError:
        raise ApiError("DDS REST 响应无法解析为 JSON：%s" % body[:200])


def _rest_payload_error(payload):
    """Map an error body returned by the REST API to a domain error."""
    if not isinstance(payload, dict):
        return None
    code = payload.get("error_code") or payload.get("errorCode")
    msg = (payload.get("error_msg") or payload.get("error_message")
           or payload.get("message"))
    if not code and not msg:
        return None
    blob = ("%s %s" % (code or "", msg or "")).lower()
    if any(p in blob for p in _AUTH_PATTERNS):
        return AuthError(
            "无权限访问文档数据库服务（DDS），请检查 IAM 权限（403）。详情：%s"
            % blob[:300]
        )
    return ApiError("DDS API 错误 %s: %s" % (code or "-", msg or "-"))


def list_instances_via_rest(region, name=None, instance_id=None, mode=None,
                            datastore_type=None, vpc_id=None, subnet_id=None,
                            tags=None, limit=DEFAULT_LIMIT, offset=0,
                            project_id=None, max_pages=DEFAULT_MAX_PAGES,
                            allow_truncation=False, get_json=None):
    """REST fallback: GET /v3/{project_id}/instances with local AK/SK signing.

    Used only when both hcloud and huaweicloudsdkdds are unavailable. The
    credentials and project id come from the same whitelisted environment
    names as the SDK fallback; paging follows `total_count`.
    """
    ak = _env_value(_AK_ENV_NAMES)
    sk = _env_value(_SK_ENV_NAMES)
    token = _env_value(_SECURITY_TOKEN_ENV_NAMES)
    resolved_project_id = resolve_project_id(project_id)
    if not resolved_project_id:
        raise ConfigError(
            "REST 兜底缺少 project_id：DDS 的 REST 路径为 %s，需要项目 ID。"
            "请通过 --project-id 传入，或设置 HUAWEICLOUD_SDK_PROJECT_ID / "
            "HUAWEI_PROJECT_ID（严禁在对话中粘贴敏感信息）。" % REST_PATH
        )
    fetcher = get_json or _http_get_json
    instances = []
    current_offset = offset
    paged_out = False
    for _ in range(max_pages):
        params = {
            "id": instance_id,
            "name": name,
            "mode": mode,
            "datastore_type": datastore_type,
            "vpc_id": vpc_id,
            "subnet_id": subnet_id,
            "tags": tags,
            "offset": current_offset,
            "limit": limit,
        }
        host = "dds.%s.myhuaweicloud.com" % region
        path = REST_PATH.format(project_id=resolved_project_id)
        url = build_rest_url(region, resolved_project_id, params)
        headers = _sign_headers("GET", path, params, host, ak, sk,
                                security_token=token)
        payload = fetcher(url, headers)
        error = _rest_payload_error(payload)
        if error is not None:
            raise error
        batch = extract_instances(payload)
        instances.extend(batch)
        if not _has_more(batch, len(instances), limit, payload):
            paged_out = True
            break
        current_offset += len(batch) if batch else limit
    if not paged_out and not allow_truncation:
        raise ApiError("翻页超过 %d 页仍未取完，已中止以防死循环。" % max_pages)
    return instances


_SDK_API = None


def _sdk_api():
    """Return (api_version, DdsClient, ListInstancesRequest, DdsRegion).

    The published `huaweicloudsdkdds` package ships a `v3` module only (checked
    against 3.0.45 .. 3.1.220), so v3 is the real fallback API; the v2 layout is
    kept as a best-effort second chance for older/private builds.
    """
    global _SDK_API
    if _SDK_API is None:
        try:
            from huaweicloudsdkdds.v3 import DdsClient, ListInstancesRequest
            from huaweicloudsdkdds.v3.region.dds_region import DdsRegion
            _SDK_API = ("v3", DdsClient, ListInstancesRequest, DdsRegion)
        except ImportError:
            from huaweicloudsdkdds.v2 import DdsClient, ListInstancesRequest
            from huaweicloudsdkdds.v2.region.dds_region import DdsRegion
            _SDK_API = ("v2", DdsClient, ListInstancesRequest, DdsRegion)
    return _SDK_API


def _sdk_imports():
    """Import the official SDK classes (no network).

    Returns (api_version, BasicCredentials, Region, HttpConfig, DdsClient,
    ListInstancesRequest, DdsRegion).
    """
    from huaweicloudsdkcore.auth.credentials import BasicCredentials
    from huaweicloudsdkcore.region.region import Region
    from huaweicloudsdkcore.http.http_config import HttpConfig
    api, DdsClient, ListInstancesRequest, DdsRegion = _sdk_api()
    return (api, BasicCredentials, Region, HttpConfig,
            DdsClient, ListInstancesRequest, DdsRegion)


def _sdk_client(region, project_id=None):
    """Build an official SDK client (credentials from env whitelist)."""
    try:
        (_api, BasicCredentials, Region, HttpConfig,
         ClientClass, _RequestClass, RegionClass) = _sdk_imports()
    except ImportError as exc:
        raise ConfigError(
            "未找到 hcloud（KooCLI），且官方 SDK（huaweicloudsdkcore + "
            "huaweicloudsdkdds）未安装，无法回退到 SDK。请安装 KooCLI 或 "
            "pip install huaweicloudsdkcore huaweicloudsdkdds。详情：%s" % exc
        )
    ak = _env_value(_AK_ENV_NAMES)
    sk = _env_value(_SK_ENV_NAMES)
    if not ak or not sk:
        raise ConfigError(
            "SDK 回退缺少 AK/SK 凭证：官方 SDK 的 BasicCredentials 不会自动读取"
            "环境变量，且当前环境未检测到 HW_ACCESS_KEY / HUAWEI_ACCESS_KEY / "
            "HUAWEICLOUD_SDK_AK 形式的 AK/SK 环境变量。"
            "请在会话外设置 HUAWEI_ACCESS_KEY / HUAWEI_SECRET_KEY（严禁在对话中"
            "粘贴 AK/SK），参见 references/cli-installation-guide.md。"
        )
    resolved_project_id = resolve_project_id(project_id)
    if not resolved_project_id:
        raise ConfigError(
            "SDK 回退缺少 project_id：DDS 的 REST 路径为 %s，需要项目 ID。"
            "请通过 --project-id 传入，或设置 HUAWEICLOUD_SDK_PROJECT_ID / "
            "HUAWEI_PROJECT_ID（严禁在对话中粘贴敏感信息）。" % REST_PATH
        )
    credentials = BasicCredentials(ak=ak, sk=sk, project_id=resolved_project_id)  # env-sourced, never literals
    try:
        try:
            region_obj = RegionClass.value_of(region)
        except (ValueError, KeyError, AttributeError):
            region_obj = Region(region, "https://dds.%s.myhuaweicloud.com" % region)
        return ClientClass.new_builder() \
            .with_credentials(credentials) \
            .with_region(region_obj) \
            .with_http_config(HttpConfig.get_default_config()) \
            .build()
    except Exception as exc:  # region unknown / config broken
        raise ConfigError(
            "SDK 初始化失败（region=%s）：%s。请检查官方 SDK 安装与区域配置。"
            % (region, exc)
        )


def list_instances_via_sdk(region, name=None, instance_id=None, mode=None,
                           datastore_type=None, vpc_id=None, subnet_id=None,
                           tags=None, limit=DEFAULT_LIMIT, offset=0,
                           project_id=None, max_pages=DEFAULT_MAX_PAGES,
                           allow_truncation=False, client=None):
    """SDK fallback (only used when hcloud is not installed).

    `DdsClient.list_instances` is the official SDK counterpart of
    `hcloud DDS ListInstances`; it hits GET /v3/{project_id}/instances.
    Request parameters are strings in the generated SDK models. Paging follows
    the response `total_count`. When the official SDK is not installed either,
    the REST fallback (third tier) takes over instead of failing outright.
    """
    try:
        api, _, _, _, _, RequestClass, _ = _sdk_imports()
    except ImportError:
        return list_instances_via_rest(
            region, name=name, instance_id=instance_id, mode=mode,
            datastore_type=datastore_type, vpc_id=vpc_id, subnet_id=subnet_id,
            tags=tags, limit=limit, offset=offset, project_id=project_id,
            max_pages=max_pages, allow_truncation=allow_truncation,
        )
    sdk_client = client or _sdk_client(region, project_id=project_id)
    instances = []
    current_offset = offset
    paged_out = False
    # v3 request models type limit/offset as int, v2 as str.
    as_int = api == "v3"
    for _ in range(max_pages):
        request = RequestClass(
            name=name,
            id=instance_id,
            mode=mode,
            datastore_type=datastore_type,
            vpc_id=vpc_id,
            subnet_id=subnet_id,
            tags=tags,
            limit=limit if as_int else str(limit),
            offset=current_offset if as_int else str(current_offset),
        )
        try:
            response = sdk_client.list_instances(request)
        except Exception as exc:
            low = str(exc).lower()
            if any(p in low for p in _AUTH_PATTERNS):
                raise AuthError(
                    "无权限访问文档数据库服务（DDS），请检查 IAM 权限（403）。"
                    "详情：%s" % str(exc)[:300]
                )
            raise ApiError("SDK 调用失败：%s" % str(exc)[:300])
        batch = list(response.instances or [])
        for item in batch:
            flat = _jsonable(item.to_dict())
            instances.append(flat)
        total = getattr(response, "total_count", None)
        if total is not None and len(instances) >= total:
            paged_out = True
            break
        if len(batch) < limit:
            paged_out = True
            break
        current_offset += len(batch)
    if not paged_out and not allow_truncation:
        raise ApiError("翻页超过 %d 页仍未取完，已中止以防死循环。" % max_pages)
    return instances


def list_instances(region, name=None, instance_id=None, mode=None,
                   datastore_type=None, vpc_id=None, subnet_id=None, tags=None,
                   limit=DEFAULT_LIMIT, offset=0, project_id=None,
                   max_pages=DEFAULT_MAX_PAGES, allow_truncation=False,
                   fuzzy=False):
    """Query DDS instances (offset-paged); KooCLI first, SDK fallback."""
    instances = []
    current_offset = offset
    paged_out = False
    for _page in range(max_pages):
        argv = build_command(
            region, name=name, instance_id=instance_id, mode=mode,
            datastore_type=datastore_type, vpc_id=vpc_id, subnet_id=subnet_id,
            tags=tags, limit=limit, offset=current_offset,
            project_id=project_id, fuzzy=fuzzy,
            cli_mode=os.environ.get("DDS_LIST_CLI_MODE", "AKSK"),
        )
        try:
            stdout, stderr, returncode = run_hcloud(argv)
        except HcloudMissingError:
            # hcloud binary missing → one-shot SDK fallback (no CLI retry).
            return list_instances_via_sdk(
                region, name=("*%s" % name) if (name and fuzzy) else name,
                instance_id=instance_id, mode=mode,
                datastore_type=datastore_type, vpc_id=vpc_id,
                subnet_id=subnet_id, tags=tags, limit=limit, offset=offset,
                project_id=project_id, max_pages=max_pages,
                allow_truncation=allow_truncation,
            )
        if returncode != 0 or _USE_ERROR_MARKER in (stdout + " " + stderr).lower():
            # KooCLI usage errors print [USE_ERROR] on stdout with rc=0.
            raise classify_hcloud_failure(stdout, stderr, returncode)
        payload = extract_json(stdout)
        batch = extract_instances(payload)
        instances.extend(batch)
        if not _has_more(batch, len(instances), limit, payload):
            paged_out = True
            break
        current_offset += len(batch) if batch else limit
    if not paged_out and not allow_truncation:
        raise ApiError("翻页超过 %d 页仍未取完，已中止以防死循环。" % max_pages)
    return instances


def _field(instance, names, default="-"):
    for name in names:
        if isinstance(instance, dict) and instance.get(name) not in (None, ""):
            return instance[name]
    return default


def _flavor_spec_code(instance):
    """Spec codes of an instance, in the official ListInstances response shape.

    `GET /v3/{project_id}/instances` returns the flavor per node group:
    `groups[].nodes[].spec_code` (QueryInstanceResponse.groups[].nodes[]) —
    there is no top-level `flavor` array. A legacy top-level `flavor[]` /
    `spec_code` is still accepted as a fallback for hand-built payloads.
    Codes are de-duplicated in response order and joined with commas.
    """
    if not isinstance(instance, dict):
        return None
    codes = []
    groups = instance.get("groups")
    if isinstance(groups, list):
        for group in groups:
            nodes = group.get("nodes") if isinstance(group, dict) else None
            if not isinstance(nodes, list):
                continue
            for node in nodes:
                if isinstance(node, dict) and node.get("spec_code"):
                    codes.append(node["spec_code"])
    if not codes:
        flavors = instance.get("flavor")
        if isinstance(flavors, list):
            codes = [f.get("spec_code") for f in flavors
                     if isinstance(f, dict) and f.get("spec_code")]
    if not codes and instance.get("spec_code"):
        codes = [instance["spec_code"]]
    if not codes:
        return None
    seen, ordered = set(), []
    for code in codes:
        code = str(code)
        if code not in seen:
            seen.add(code)
            ordered.append(code)
    return ",".join(ordered)


def _instance_version(instance):
    datastore = instance.get("datastore") if isinstance(instance, dict) else None
    if isinstance(datastore, dict):
        return datastore.get("version") or datastore.get("type")
    return None


def _node_count(instance):
    """Number of nodes across `groups[].nodes` (official response shape).

    Returns None when the instance carries no group information, so the table
    renders the fixed `-` placeholder. A legacy top-level `nodes[]` list is
    accepted as a fallback for hand-built payloads.
    """
    if not isinstance(instance, dict):
        return None
    groups = instance.get("groups")
    if isinstance(groups, list):
        count = 0
        seen = False
        for group in groups:
            nodes = group.get("nodes") if isinstance(group, dict) else None
            if isinstance(nodes, list):
                seen = True
                count += len(nodes)
        if seen:
            return count
    nodes = instance.get("nodes")
    if isinstance(nodes, list):
        return len(nodes)
    return None


def instance_names(instances):
    names = []
    for instance in instances:
        name = _field(instance, ("name",), default=None)
        if name is None:
            name = _field(instance, ("id",))
        names.append(str(name))
    return names


def _table_cell(header, instance):
    if header == "引擎版本":
        value = _instance_version(instance)
    elif header == "规格":
        value = _flavor_spec_code(instance)
    elif header == "节点数":
        value = _node_count(instance)
    else:
        value = _field(instance, _column_names(header))
    if value in (None, ""):
        return "-"
    if header == "模式":
        return TYPE_LABELS.get(str(value), str(value))
    if isinstance(value, (list, tuple)):
        return ",".join(str(v) for v in value) or "-"
    return str(value)


def _column_names(header):
    for hdr, names in TABLE_COLUMNS:
        if hdr == header:
            return names
    return ()


def _display_width(text):
    """Display width of `text` (CJK wide/fullwidth characters count as 2)."""
    return sum(2 if unicodedata.east_asian_width(ch) in ("W", "F") else 1
               for ch in str(text))


def _pad(text, width):
    """Right-pad `text` to `width` display columns."""
    return text + " " * max(0, width - _display_width(text))


def render_table(instances):
    """Render the fixed 8-column table (missing values as "-").

    Works on an empty collection too (header + rule only), and pads by display
    width so CJK headers/cells stay aligned.
    """
    headers = [header for header, _names in TABLE_COLUMNS]
    rows = [[_table_cell(header, instance) for header, _ in TABLE_COLUMNS]
            for instance in instances]
    widths = [max([_display_width(headers[i])]
                  + [_display_width(row[i]) for row in rows])
              for i in range(len(headers))]
    lines = [
        "  ".join(_pad(headers[i], widths[i]) for i in range(len(headers))),
        "  ".join("-" * w for w in widths),
    ]
    for row in rows:
        lines.append("  ".join(_pad(row[i], widths[i]) for i in range(len(headers))))
    return "\n".join(lines)


def filter_by_status(instances, status):
    """Client-side status filter (the API has no server-side status param)."""
    if not status:
        return instances
    wanted = str(status).lower()
    return [i for i in instances
            if str(i.get("status", "")).lower() == wanted]


def _filter_suffix(args):
    filters = []
    if args.name:
        filters.append("name=%s%s" % ("*" if args.fuzzy else "", args.name))
    if args.instance_id:
        filters.append("id=%s" % args.instance_id)
    if args.mode:
        filters.append("mode=%s" % args.mode)
    if args.datastore_type:
        filters.append("datastore_type=%s" % args.datastore_type)
    if args.vpc_id:
        filters.append("vpc_id=%s" % args.vpc_id)
    if args.subnet_id:
        filters.append("subnet_id=%s" % args.subnet_id)
    if args.tags:
        filters.append("tags=%s" % args.tags)
    if args.status:
        filters.append("status=%s（客户端过滤）" % args.status)
    return "（过滤条件: %s）" % ", ".join(filters) if filters else ""


def main(argv=None):
    raw_argv = list(argv if argv is not None else sys.argv[1:])
    # Write-intent guard: scan the operation/option positions of the raw argv
    # *before* parsing and before anything executes. Read-only filter values
    # are data and are deliberately exempt (`_guard_segments`), so
    # `--name create-me` passes while `CreateInstance` / `--delete-instance`
    # are rejected with exit code 1 and no hcloud call.
    try:
        guard_write_intent(" ".join(raw_argv))
        guard_operation("ListInstances")
    except DdsListError as exc:
        print("[错误] %s" % exc, file=sys.stderr)
        return 1

    parser = argparse.ArgumentParser(
        description="查询华为云 DDS（文档数据库服务）实例列表 —— 只读"
                    "（KooCLI hcloud DDS ListInstances，GET /v3/{project_id}/instances）。")
    parser.add_argument("-r", "--region", default=DEFAULT_REGION,
                        help="目标 Region（默认 %s）" % DEFAULT_REGION)
    parser.add_argument("--names-only", action="store_true", dest="names_only",
                        help="仅输出实例名称清单（默认即名称清单模式）")
    parser.add_argument("--json", action="store_true", dest="as_json",
                        help="以 JSON 输出完整原始字段数组")
    parser.add_argument("--table", action="store_true", dest="as_table",
                        help="输出固定列表格（实例ID/名称/状态/引擎版本/规格/"
                             "节点数/创建时间/模式）")
    parser.add_argument("--name",
                        help="按实例名称过滤（服务端查询参数；默认精确，--fuzzy 转模糊）")
    parser.add_argument("--fuzzy", action="store_true",
                        help="名称模糊匹配（转发服务端 *name 前缀通配）")
    parser.add_argument("--instance-id", dest="instance_id",
                        help="按实例 ID 过滤（服务端查询参数）")
    parser.add_argument("--mode", choices=("Sharding", "ReplicaSet", "Single"),
                        help="按实例类型过滤（服务端查询参数：Sharding=集群 / "
                             "ReplicaSet=副本集 / Single=单节点）")
    parser.add_argument("--datastore-type", dest="datastore_type",
                        help="按数据库类型过滤（服务端查询参数：DDS-Community / "
                             "DDS-Enhanced）")
    parser.add_argument("--vpc-id", dest="vpc_id",
                        help="按 VPC ID 过滤（服务端查询参数）")
    parser.add_argument("--subnet-id", dest="subnet_id",
                        help="按子网 ID 过滤（服务端查询参数）")
    parser.add_argument("--tags",
                        help="按标签过滤（服务端查询参数，格式 key1=value1,key2=value2）")
    parser.add_argument("--status",
                        help="按实例状态过滤（客户端过滤：该 API 无服务端 status "
                             "参数，如 normal/abnormal/creating/frozen）")
    parser.add_argument("--limit", type=int, default=DEFAULT_LIMIT,
                        help="分页大小（服务端范围 1~%d，默认 %d；自动翻页取全量）"
                             % (MAX_LIMIT, DEFAULT_LIMIT))
    parser.add_argument("--offset", type=int, default=0,
                        help="起始偏移量（服务端参数，默认 0）")
    parser.add_argument("--max-pages", type=int, default=DEFAULT_MAX_PAGES,
                        dest="max_pages",
                        help="自动翻页的最大页数（默认 %d，防止死循环）"
                             % DEFAULT_MAX_PAGES)
    parser.add_argument("--single-page", action="store_true", dest="single_page",
                        help="只取一页（不透传后续 offset，便于分页演示/调试）")
    parser.add_argument("--project-id", dest="project_id",
                        help="项目 ID（可选；缺省由 KooCLI profile / SDK 环境变量解析）")
    args = parser.parse_args(raw_argv)

    try:
        if args.limit < 1 or args.limit > MAX_LIMIT:
            raise ApiError("--limit 超出范围（1~%d）：%d" % (MAX_LIMIT, args.limit))
        if args.offset < 0:
            raise ApiError("--offset 不能为负数：%d" % args.offset)
        if args.max_pages < 1:
            raise ApiError("--max-pages 必须 ≥ 1：%d" % args.max_pages)
        instances = filter_by_status(list_instances(
            args.region,
            name=args.name,
            instance_id=args.instance_id,
            mode=args.mode,
            datastore_type=args.datastore_type,
            vpc_id=args.vpc_id,
            subnet_id=args.subnet_id,
            tags=args.tags,
            limit=args.limit,
            offset=args.offset,
            project_id=args.project_id,
            fuzzy=args.fuzzy,
            max_pages=1 if args.single_page else args.max_pages,
            allow_truncation=args.single_page,
        ), args.status)
    except DdsListError as exc:
        print("[错误] %s" % exc, file=sys.stderr)
        return 1

    if args.as_json:
        print(json.dumps(instances, ensure_ascii=False, indent=2))
        return 0

    if not instances:
        print("当前区域（%s）无 DDS 实例%s。" % (args.region, _filter_suffix(args)))
        return 0

    if args.as_table:
        print("Region %s 的 DDS 实例列表（共 %d 个）：" % (args.region, len(instances)))
        print(render_table(instances))
        return 0

    # Default output mode: the compact instance-name list (--names-only).
    print("Region %s 的 DDS 实例名称列表（共 %d 个）：" % (args.region, len(instances)))
    for name in instance_names(instances):
        print("- %s" % name)
    return 0


if __name__ == "__main__":
    sys.exit(main())
