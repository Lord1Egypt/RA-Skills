#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""List Huawei Cloud CBR backup vaults via KooCLI ``hcloud CBR ListVault`` (read-only).

Primary execution path is KooCLI; when the hcloud binary is not installed, the
script falls back to the official ``huaweicloudsdkcbr`` v1 SDK
(``CbrClient.list_vault``). Credentials are always resolved by the hcloud
profile / SDK environment — this script never reads, echoes or stores AK/SK
itself.

Supported features:

* Three stdout modes — aligned full-field table (default), ``--json`` (raw
  response array) and ``--names-only`` (compact vault name + ID inventory).
* Read-only query with ``--region`` (default cn-north-4), ``--page-size`` and
  automatic ``limit`` / ``offset`` paging (the CBR response carries
  ``count`` / ``offset`` / ``limit``).
* Server-side filtering via the native ``ListVault`` query parameters
  (``--name`` / ``--status`` / ``--object-type`` / ``--protect-type`` /
  ``--enterprise-project-id`` / ``--vault-id``; the underscore forms are
  accepted as aliases) plus a client-side re-filter so the rendered rows always
  match the requested filters.
* Strict write-intent guard: any mutating CBR intent is rejected before a
  single command is executed.

Usage:
    python3 scripts/list_cbr_vaults.py [--region cn-north-4]
        [--json | --names-only] [--name NAME] [--status STATUS]
        [--object-type TYPE] [--protect-type TYPE]
        [--enterprise-project-id ID] [--vault-id ID] [--page-size 100]
        [--operation ListVault]

Environment overrides (mostly for tests):
    CBR_VAULT_HCLOUD_BIN   hcloud executable (default "hcloud")
    CBR_VAULT_HCLOUD_ARGS  extra args injected before the CBR operation
"""

import argparse
import json
import os
import re
import subprocess
import sys

DEFAULT_REGION = "cn-north-4"
DEFAULT_PAGE_SIZE = 100
SERVICE = "CBR"
ALLOWED_OPERATION = "ListVault"
REST_ENDPOINT = "GET /v3/{project_id}/vaults"

# Mutating CBR intents / operation names — strictly rejected by the guard.
# Read-only vocabulary (list/show/get/describe/details) never matches. The bare
# word "vault" is intentionally NOT a keyword (the read-only operation itself is
# ``ListVault``); only concrete mutating verbs are listed.
WRITE_INTENT_KEYWORDS = (
    "createvault",
    "deletevault",
    "updatevault",
    "batchupdatevault",
    "createpostpaidvault",
    "changevaultchargemode",
    "changechargemode",
    "addvaultresource",
    "removevaultresource",
    "setvaultresource",
    "migratevaultresource",
    "associatevaultpolicy",
    "disassociatevaultpolicy",
    "bindpolicy",
    "unbindpolicy",
    "createpolicy",
    "deletepolicy",
    "updatepolicy",
    "createorganizationpolicy",
    "deleteorganizationpolicy",
    "batchcreateanddeletevaulttags",
    "createvaulttags",
    "deletevaulttag",
    "addvaulttag",
    "addmember",
    "deletemember",
    "updatememberstatus",
    "registeragent",
    "unregisteragent",
    "updateagent",
    "addagentpath",
    "removeagentpath",
    "restorebackup",
    "copybackup",
    "copycheckpoint",
    "importbackup",
    "importcheckpoint",
    "createbackup",
    "deletebackup",
    "updatebackup",
    "createcheckpoint",
    "migratedomain",
    "changeorder",
    "associate",
    "disassociate",
    "create",
    "delete",
    "update",
    "modify",
    "restore",
    "replicate",
    "copy",
    "import",
    "migrate",
    "bind",
    "unbind",
    "attach",
    "detach",
    "register",
    "unregister",
    "add",
    "remove",
    "terminate",
    "destroy",
    "purge",
    "reset",
)

# Read-only option flags whose *values* are filter / query data (e.g. a vault
# literally named "delete-me"). Their values must NOT be scanned by the
# write-intent guard. Both the underscore form (matches the real KooCLI
# parameter) and the hyphenated alias are listed so a user can pass either.
# The ``--operation`` value is intentionally NOT excluded: it is validated by
# ``guard_operation()`` and scanned as defense in depth.
_VALUE_STRIPPED_FLAGS = (
    "--region",
    "-r",
    "--name",
    "--status",
    "--object-type",
    "--object_type",
    "--protect-type",
    "--protect_type",
    "--enterprise-project-id",
    "--enterprise_project_id",
    "--vault-id",
    "--vault_id",
    "--policy-id",
    "--policy_id",
    "--resource-ids",
    "--resource_ids",
    "--cloud-type",
    "--cloud_type",
    "--availability-zone",
    "--availability_zone",
    "--page-size",
    "--page_size",
    "--limit",
    "--offset",
    "--sort",
)

# Preferred column order for the table view; remaining keys are appended sorted.
PREFERRED_COLUMNS = [
    "name",
    "id",
    "status",
    "size",
    "used",
    "allocated",
    "charging_mode",
    "object_type",
    "protect_type",
    "spec_code",
    "cloud_type",
    "availability_zone",
    "enterprise_project_id",
    "created_at",
    "locked",
    "auto_bind",
    "auto_expand",
    "threshold",
    "smn_notify",
    "storage_unit",
    "consistent_level",
    "frozen_scene",
    "is_multi_az",
    "project_id",
    "provider_id",
    "user_id",
    "description",
    "order_id",
    "product_id",
    "resources",
    "tags",
]

# Fields nested under the vault's ``billing`` object that are surfaced at the
# top level of the table so name / ID / status / capacity / charging mode are
# all directly readable.
BILLING_FLATTEN_KEYS = (
    "status",
    "size",
    "used",
    "allocated",
    "charging_mode",
    "object_type",
    "protect_type",
    "spec_code",
    "cloud_type",
    "consistent_level",
    "storage_unit",
    "frozen_scene",
    "is_multi_az",
    "order_id",
    "product_id",
)

_VAULT_LIST_KEYS = (
    "vaults",
    "vault_list",
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
    "0401",
    "0403",
    "unauthorized",
    "forbidden",
    "not authorized",
    "apigw.0301",
    "认证失败",
    "权限不足",
    "permission denied",
)

# KooCLI prints usage errors (e.g. "[USE_ERROR]Invalid parameter: xxx") on
# stdout WITH exit code 0 — the marker must be treated as a hard failure even
# when the return code looks successful.
_USE_ERROR_MARKER = "[use_error]"


class CbrVaultListError(Exception):
    """Base error for the CBR vault list skill."""


class GuardError(CbrVaultListError):
    """A write intent was detected and blocked (skill is read-only)."""


class ConfigError(CbrVaultListError):
    """hcloud missing or credentials (AK/SK) not configured."""


class AuthError(CbrVaultListError):
    """Authentication/authorization failure (invalid AK/SK or IAM 403)."""


class ApiError(CbrVaultListError):
    """hcloud / network / unexpected API failure."""


def guard_write_intent(text):
    """Raise GuardError if ``text`` carries a mutating intent.

    Separators are normalized so ``--delete-vault``, ``DeleteVault`` and
    ``delete_vault`` all hit the same keyword. Read-only vocabulary
    (list/show/get/describe) never matches.
    """
    low = re.sub(r"[\s_\-]+", "", str(text).lower())
    for keyword in WRITE_INTENT_KEYWORDS:
        if keyword in low:
            raise GuardError(
                "检测到写操作意图（关键词: %s）。本 skill 仅支持只读查询"
                "（CBR ListVault），创建/删除/更新/迁移/绑定等变更操作已被守卫拦截。"
                % keyword
            )
    return False


def guard_operation(operation):
    """Only the read-only ListVault operation may be executed."""
    if operation != ALLOWED_OPERATION:
        raise GuardError(
            "不允许的操作 %r：本 skill 仅允许只读操作 %s。"
            % (operation, ALLOWED_OPERATION)
        )
    return True


def guard_text_from_argv(argv):
    """Build the text the write-intent guard should scan.

    Scans flag names and positional tokens, but strips the values of the
    read-only filter flags (``--name`` / ``--status`` / ``--vault-id`` /
    ``--region`` / ``--page-size`` / ...): those are query data and may
    legitimately contain write-looking words (e.g. a vault named ``delete-me``).
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


# Native ListVault query parameters (snake_case) exposed as CLI flags.
#
# KooCLI accepts only the underscore form (``--object_type`` /
# ``--protect_type`` / ``--enterprise_project_id``); the hyphenated form is
# rejected with ``[USE_ERROR]Invalid parameter``. The first element is therefore
# the *real* KooCLI flag emitted by ``build_command()``; the second is the
# filter dict key. The argparse layer additionally accepts the hyphenated alias
# for the user's convenience.
_FILTER_ARG_TO_PARAM = (
    ("--name", "name"),
    ("--status", "status"),
    ("--object_type", "object_type"),
    ("--protect_type", "protect_type"),
    ("--enterprise_project_id", "enterprise_project_id"),
)


def build_command(region, filters=None, limit=DEFAULT_PAGE_SIZE, offset=0):
    """Build the hcloud CBR ListVault argv (without the executable).

    Mirrors the real KooCLI parameter list: ``--cli-region`` / ``--limit`` /
    ``--offset`` plus the native server-side filters. Only read-only
    parameters are ever emitted (verified against
    ``huaweicloudsdkcbr.v1.ListVaultRequest.openapi_types`` and
    ``hcloud CBR ListVault --help``). The vault ID filter uses the KooCLI array
    form ``--id.1=<vault_id>`` (the operation's parameter is ``id.[N]``; there
    is no ``--vault_id`` parameter).
    """
    argv = [
        SERVICE,
        ALLOWED_OPERATION,
        "--cli-region=%s" % region,
        "--limit=%d" % limit,
        "--offset=%d" % offset,
    ]
    filters = filters or {}
    for param, key in _FILTER_ARG_TO_PARAM:
        value = filters.get(key)
        if value:
            argv.append("%s=%s" % (param, value))
    vault_id = filters.get("vault_id")
    if vault_id:
        argv.append("--id.1=%s" % vault_id)
    return argv


def _hcloud_executable():
    return os.environ.get("CBR_VAULT_HCLOUD_BIN", "hcloud")


def run_hcloud(argv):
    """Execute hcloud and return (stdout, stderr, returncode)."""
    cmd = [_hcloud_executable()]
    extra = os.environ.get("CBR_VAULT_HCLOUD_ARGS", "").split()
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


def _payload_error(payload):
    """Return (error_code, error_msg) carried by an API-error JSON payload."""
    if not isinstance(payload, dict):
        return None, None
    code = payload.get("error_code") or payload.get("errorCode")
    msg = payload.get("error_msg") or payload.get("errorMessage")
    if code is None and msg is None:
        return None, None
    return str(code or ""), str(msg or "")


def classify_payload_error(code, message):
    """Map an API error payload (returned with rc=0 by KooCLI) to a domain error."""
    blob = ("%s %s" % (code, message)).strip()
    low = blob.lower()
    if any(p in low for p in _AUTH_PATTERNS):
        return AuthError(
            "无权限访问 CBR，请检查 IAM 权限（403：AK/SK 无效或未授予 CBR 只读权限 "
            "cbr:vaults:list），参见 references/iam-policies.md。详情：%s" % blob[:300]
        )
    return ApiError("CBR API 返回错误（%s）：%s" % (code or "unknown", blob[:300]))


def classify_hcloud_failure(stdout, stderr, returncode):
    """Map a failed hcloud invocation to a domain error with explicit hints."""
    blob = (stderr + " " + stdout).strip()
    low = blob.lower()
    if _USE_ERROR_MARKER in low:
        return ApiError(
            "hcloud 参数错误（KooCLI 拒绝了该参数组合，退出码 %s）：CBR ListVault "
            "真实参数清单可通过 `hcloud CBR ListVault --help` 查看。详情：%s"
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
            "无权限访问 CBR，请检查 IAM 权限（403：AK/SK 无效或未授予 CBR 只读权限），"
            "参见 references/iam-policies.md。详情：%s" % blob[:300]
        )
    return ApiError(
        "hcloud 调用失败（退出码 %s）：%s" % (returncode, blob[:300])
    )


def extract_vaults(payload):
    """Pull the vault list out of a ListVault response."""
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        for key in _VAULT_LIST_KEYS:
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


def _env_project_id():
    return _env_credential(
        "HUAWEICLOUD_SDK_PROJECT_ID", "HUAWEI_PROJECT_ID", "HWC_PROJECT_ID",
        "HUAWEI_CLOUD_PROJECT_ID",
    )


def sdk_vault_to_dict(vault):
    """Convert a ``huaweicloudsdkcbr`` Vault into a wire-name dict.

    The SDK ``to_dict()`` emits Python attribute names; the OpenAPI JSON uses
    wire names. Remapping through ``Vault.attribute_map`` keeps both execution
    paths producing the same shape. Nested ``billing`` is converted likewise.
    """
    if isinstance(vault, dict):
        return dict(vault)
    try:
        raw = vault.to_dict()
    except AttributeError:
        return dict(vault)
    if not isinstance(raw, dict):
        return {}
    try:
        from huaweicloudsdkcbr.v1 import Vault
        attr_map = Vault.attribute_map
    except Exception:
        attr_map = {}
    out = {}
    attr_keys = set(attr_map.keys())
    def _plain(value):
        if hasattr(value, "to_dict"):
            value = value.to_dict()
        if hasattr(value, "isoformat"):
            return value.isoformat()
        if isinstance(value, list):
            return [_plain(item) for item in value]
        if isinstance(value, dict):
            return {k: _plain(v) for k, v in value.items()}
        return value

    for attr, wire in attr_map.items():
        if attr in raw and raw[attr] is not None:
            out[wire] = _plain(raw[attr])
    for key, value in raw.items():
        if key not in attr_keys and key not in out and value is not None:
            out[key] = _plain(value)
    return out


def list_vaults_via_sdk(region, filters=None, limit=DEFAULT_PAGE_SIZE, max_pages=100):
    """SDK fallback: query vaults through ``huaweicloudsdkcbr`` v1.

    Only invoked when hcloud is not installed. Credentials come from the
    whitelisted AK/SK environment variables (HW_*/HUAWEI_ACCESS_KEY family) —
    never passed as literals here. Region resolution uses the SDK's own
    ``CbrRegion`` catalog (official endpoints, no guessing), falling back to an
    explicit ``Region(id, endpoint)`` for custom regions.
    """
    try:
        from huaweicloudsdkcore.auth.credentials import BasicCredentials
        from huaweicloudsdkcore.region.region import Region
        from huaweicloudsdkcore.http.http_config import HttpConfig
        from huaweicloudsdkcbr.v1 import CbrClient, ListVaultRequest
        from huaweicloudsdkcbr.v1.region.cbr_region import CbrRegion
    except ImportError as exc:
        raise ConfigError(
            "未找到 hcloud（KooCLI），且 huaweicloudsdkcore/huaweicloudsdkcbr "
            "未安装，无法回退到 SDK。请安装 KooCLI 或 pip install "
            "huaweicloudsdkcore huaweicloudsdkcbr。详情：%s" % exc
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
    project_id = _env_project_id()
    if project_id:
        credentials = BasicCredentials(ak=ak, sk=sk, project_id=project_id)  # env-sourced, never literals
    else:
        credentials = BasicCredentials(ak=ak, sk=sk)  # env-sourced, never literals
    try:
        try:
            region_obj = CbrRegion.value_of(region)
        except (ValueError, KeyError, AttributeError):
            region_obj = Region(
                region, "https://cbr.%s.myhuaweicloud.com" % region)
        client = CbrClient.new_builder() \
            .with_credentials(credentials) \
            .with_region(region_obj) \
            .with_http_config(HttpConfig.get_default_config()) \
            .build()
    except Exception as exc:  # region unknown / config broken
        raise ConfigError(
            "SDK 初始化失败（region=%s）：%s。请检查 huaweicloudsdkcbr 安装与区域"
            "配置。" % (region, exc)
        )
    filters = filters or {}
    vault_id = filters.get("vault_id")
    vaults = []
    seen = set()
    offset = 0
    for _ in range(max_pages):
        request = ListVaultRequest(
            limit=limit, offset=offset,
            name=filters.get("name"),
            status=filters.get("status"),
            object_type=filters.get("object_type"),
            protect_type=filters.get("protect_type"),
            enterprise_project_id=filters.get("enterprise_project_id"),
            id=[vault_id] if vault_id else None,
        )
        try:
            response = client.list_vault(request)
        except Exception as exc:
            low = str(exc).lower()
            if any(p in low for p in _AUTH_PATTERNS):
                raise AuthError(
                    "无权限访问 CBR，请检查 IAM 权限（403）。详情：%s" % str(exc)[:300]
                )
            raise ApiError("SDK 调用失败：%s" % str(exc)[:300])
        batch = list(response.vaults or [])
        new_rows = 0
        for vault in batch:
            record = sdk_vault_to_dict(vault)
            key = record.get("id") or json.dumps(record, sort_keys=True)
            if key in seen:
                continue
            seen.add(key)
            vaults.append(record)
            new_rows += 1
        total = getattr(response, "count", None)
        if total is not None and len(vaults) >= total:
            break
        if len(batch) < limit:
            break
        if new_rows == 0:
            break
        offset += len(batch)
    else:
        raise ApiError("翻页超过 %d 页仍未取完，已中止以防死循环。" % max_pages)
    return vaults


def list_vaults(region, filters=None, limit=DEFAULT_PAGE_SIZE, max_pages=100):
    """Query all CBR vaults (paged); KooCLI first, SDK fallback."""
    vaults = []
    seen = set()
    offset = 0
    for _page in range(max_pages):
        argv = build_command(region, filters=filters, limit=limit, offset=offset)
        try:
            stdout, stderr, returncode = run_hcloud(argv)
        except ConfigError:
            # hcloud binary missing → one-shot SDK fallback (no CLI retry).
            vaults = list_vaults_via_sdk(
                region, filters=filters, limit=limit, max_pages=max_pages)
            break
        if returncode != 0 or _USE_ERROR_MARKER in (stdout + " " + stderr).lower():
            # KooCLI usage errors print [USE_ERROR] on stdout with rc=0.
            raise classify_hcloud_failure(stdout, stderr, returncode)
        payload = extract_json(stdout)
        # KooCLI prints API errors as an error_code/error_msg JSON document and
        # still exits 0 — surface them before treating the payload as data.
        code, message = _payload_error(payload)
        if code or message:
            raise classify_payload_error(code, message)
        batch = extract_vaults(payload)
        new_rows = 0
        for vault in batch:
            key = vault.get("id") if isinstance(vault, dict) else json.dumps(vault, sort_keys=True)
            if key in seen:
                continue
            seen.add(key)
            vaults.append(vault)
            new_rows += 1
        if not _has_more(batch, len(vaults), limit, payload):
            break
        if new_rows == 0:
            break
        offset += len(batch) if batch else limit
    else:
        raise ApiError("翻页超过 %d 页仍未取完，已中止以防死循环。" % max_pages)
    return vaults


def _field(vault, *names, default="-"):
    for name in names:
        if name in vault and vault[name] not in (None, ""):
            return vault[name]
    return default


def _get(vault, *names, default=None):
    """Return the first present, non-empty value among ``names``."""
    for name in names:
        if name in vault and vault[name] not in (None, ""):
            return vault[name]
    return default


def normalize_vault(vault):
    """Flatten the nested ``billing`` fields and datetime values for the table.

    CBR returns vault capacity / charging mode / status / object type inside the
    ``billing`` object; they are copied to the top level so the default table
    always shows name / ID / status / capacity / charging_mode as first-class
    columns.
    """
    flat = dict(vault)
    billing = vault.get("billing")
    if isinstance(billing, dict):
        for key in BILLING_FLATTEN_KEYS:
            if flat.get(key) in (None, "") and billing.get(key) not in (None, ""):
                flat[key] = billing[key]
    for key in ("created_at", "updated_at"):
        value = flat.get(key)
        if value is not None and hasattr(value, "isoformat"):
            flat[key] = value.isoformat()
    return flat


def filter_vaults(vaults, name=None, status=None, object_type=None,
                  protect_type=None, enterprise_project_id=None, vault_id=None):
    """Apply client-side name / status / type / project / vault filters.

    The native ``ListVault`` request already accepts these as server-side
    parameters; this client-side pass guarantees the rendered rows honour the
    requested filters even if a backend ignores or loosely interprets a
    parameter. ``name`` is a case-insensitive substring match; the rest are
    case-insensitive exact matches. Vault capacity / charging mode / status live
    under ``billing`` in the raw response, so matching is done on the normalized
    view.
    """
    result = []
    for vault in vaults:
        flat = normalize_vault(vault)
        if name and str(name).lower() not in str(
                _field(flat, "name", "id", default="")).lower():
            continue
        if status and str(_field(flat, "status", default="")).lower() != str(status).lower():
            continue
        if object_type and str(_field(flat, "object_type", default="")).lower() != str(object_type).lower():
            continue
        if protect_type and str(_field(flat, "protect_type", default="")).lower() != str(protect_type).lower():
            continue
        if enterprise_project_id and str(
                _field(flat, "enterprise_project_id", default="")).lower() != str(enterprise_project_id).lower():
            continue
        if vault_id and str(_field(flat, "id", "vault_id", default="")).lower() != str(vault_id).lower():
            continue
        result.append(vault)
    return result


def vault_summary_lines(vaults):
    """Compact ``name  (id: ...)`` lines for the --names-only inventory mode."""
    lines = []
    for vault in vaults:
        flat = normalize_vault(vault)
        name = _field(flat, "name", default=None)
        if name is None:
            name = _field(flat, "id")
        vid = _field(flat, "id", default="-")
        extra = _field(flat, "charging_mode", default=None)
        suffix = "  (id: %s" % vid
        if extra is not None:
            suffix += ", charging_mode: %s" % extra
        suffix += ")"
        lines.append("%s%s" % (name, suffix))
    return lines


def active_filter_descriptions(name=None, status=None, object_type=None,
                               protect_type=None, enterprise_project_id=None,
                               vault_id=None):
    """Human-readable description of the filters actually applied."""
    filters = []
    if name:
        filters.append("name=%s" % name)
    if status:
        filters.append("status=%s" % status)
    if object_type:
        filters.append("object_type=%s" % object_type)
    if protect_type:
        filters.append("protect_type=%s" % protect_type)
    if enterprise_project_id:
        filters.append("enterprise_project_id=%s" % enterprise_project_id)
    if vault_id:
        filters.append("vault_id=%s" % vault_id)
    return filters


def _cell(value):
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return str(value)


def render_table(vaults):
    """Render full-field table output (union of all returned fields)."""
    rows_data = [normalize_vault(vault) for vault in vaults]
    columns = []
    for key in PREFERRED_COLUMNS:
        if any(key in v for v in rows_data):
            columns.append(key)
    for key in sorted({k for v in rows_data for k in v}):
        if key not in columns:
            columns.append(key)
    if not columns:
        columns = ["name", "id"]
    rows = [[_cell(_field(v, col)) for col in columns] for v in rows_data]
    widths = [max(len(col), *(len(row[i]) for row in rows)) for i, col in enumerate(columns)]
    header = "  ".join(col.ljust(widths[i]) for i, col in enumerate(columns))
    separator = "  ".join("-" * w for w in widths)
    lines = [header, separator]
    for row in rows:
        lines.append("  ".join(row[i].ljust(widths[i]) for i in range(len(columns))))
    return "\n".join(lines)


def _collect_filters(args):
    return {
        "name": args.name,
        "status": args.status,
        "object_type": args.object_type,
        "protect_type": args.protect_type,
        "enterprise_project_id": args.enterprise_project_id,
        "vault_id": args.vault_id,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="查询华为云 CBR 备份存储库（vault）列表（KooCLI hcloud CBR ListVault，只读）。")
    parser.add_argument("-r", "--region", default=DEFAULT_REGION,
                        help="目标 Region（默认 %s）" % DEFAULT_REGION)
    parser.add_argument("--json", action="store_true", dest="as_json",
                        help="以 JSON 输出原始存储库数组")
    parser.add_argument("--names-only", action="store_true", dest="names_only",
                        help="仅输出精简存储库名称+ID 清单")
    parser.add_argument("--name", help="按存储库名称过滤（服务端 + 客户端子串）")
    parser.add_argument("--status", help="按存储库状态过滤（如 available）")
    parser.add_argument("--object-type", "--object_type", dest="object_type",
                        help="按对象类型过滤（server/disk/turbo/workspace/vmware/rds/file）")
    parser.add_argument("--protect-type", "--protect_type", dest="protect_type",
                        help="按保护类型过滤（backup/replication）")
    parser.add_argument("--enterprise-project-id", "--enterprise_project_id",
                        dest="enterprise_project_id",
                        help="按企业项目 ID 过滤（或 all_granted_eps）")
    parser.add_argument("--vault-id", "--vault_id", dest="vault_id", help="按存储库 ID 过滤")
    parser.add_argument("--page-size", "--page_size", type=int, default=DEFAULT_PAGE_SIZE,
                        dest="page_size", help="分页大小（默认 %d）" % DEFAULT_PAGE_SIZE)
    parser.add_argument("--operation", default=ALLOWED_OPERATION,
                        help="hcloud CBR 操作名（仅允许只读 %s）" % ALLOWED_OPERATION)

    # Write-intent guard runs on the RAW argv before argparse so a mutating flag
    # (e.g. `--delete-vault`) is reported as a guard violation rather than an
    # argparse "unrecognized argument" error. Filter values are read-only data
    # and deliberately not scanned.
    try:
        guard_write_intent(guard_text_from_argv(argv))
    except CbrVaultListError as exc:
        print("[错误] %s" % exc, file=sys.stderr)
        return 1

    args = parser.parse_args(argv)

    try:
        guard_operation(args.operation)
        vaults = list_vaults(args.region, filters=_collect_filters(args),
                             limit=args.page_size)
    except CbrVaultListError as exc:
        print("[错误] %s" % exc, file=sys.stderr)
        return 1

    filters = active_filter_descriptions(
        name=args.name, status=args.status, object_type=args.object_type,
        protect_type=args.protect_type,
        enterprise_project_id=args.enterprise_project_id,
        vault_id=args.vault_id)
    vaults = filter_vaults(
        vaults, name=args.name, status=args.status,
        object_type=args.object_type, protect_type=args.protect_type,
        enterprise_project_id=args.enterprise_project_id,
        vault_id=args.vault_id)
    filter_suffix = "（过滤条件: %s）" % ", ".join(filters) if filters else ""

    if args.as_json:
        print(json.dumps(vaults, ensure_ascii=False, indent=2))
    elif args.names_only:
        print("Region %s 的 CBR 存储库清单（共 %d 个）：" % (args.region, len(vaults)))
        for line in vault_summary_lines(vaults):
            print("- %s" % line)
    elif not vaults:
        print("当前区域（%s）无 CBR 存储库%s。" % (args.region, filter_suffix))
    else:
        print("Region %s 的 CBR 存储库列表（共 %d 个，完整字段）："
              % (args.region, len(vaults)))
        print(render_table(vaults))

    return 0


if __name__ == "__main__":
    sys.exit(main())