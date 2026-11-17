#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""List Huawei Cloud CBR backups via KooCLI ``hcloud CBR ListBackups`` (read-only).

Primary execution path is KooCLI; when the hcloud binary is not installed, the
script falls back to the official ``huaweicloudsdkcbr`` v1 SDK
(``CbrClient.list_backups``). Credentials are always resolved by the hcloud
profile / SDK environment — this script never reads, echoes or stores AK/SK
itself.

Supported features:

* Three stdout modes — aligned full-field table (default), ``--json`` (raw
  response array) and ``--names-only`` (compact name + ID inventory).
* Read-only query with ``--region`` (default cn-north-4), ``--page-size`` and
  automatic ``limit`` / ``offset`` paging (the CBR response carries
  ``count`` / ``offset`` / ``limit``).
* Server-side filtering via the native ``ListBackups`` query parameters
  (``--name`` / ``--status`` / ``--resource_id`` / ``--resource_name`` /
  ``--resource_type`` / ``--vault_id`` / ``--image_type``; the hyphenated forms
  are accepted as aliases) plus a client-side re-filter so the rendered rows
  always match the requested filters.
* Strict write-intent guard: any mutating CBR intent is rejected before a
  single command is executed.

Usage:
    python3 scripts/list_cbr_backups.py [--region cn-north-4]
        [--json | --names-only] [--name NAME] [--status STATUS]
        [--resource_id ID] [--resource_name NAME] [--resource_type TYPE]
        [--vault_id ID] [--image_type TYPE] [--page-size 1000]
        [--operation ListBackups]

Environment overrides (mostly for tests):
    CBR_LIST_HCLOUD_BIN   hcloud executable (default "hcloud")
    CBR_LIST_HCLOUD_ARGS  extra args injected before the CBR operation
"""

import argparse
import json
import os
import re
import subprocess
import sys

DEFAULT_REGION = "cn-north-4"
DEFAULT_PAGE_SIZE = 1000
SERVICE = "CBR"
ALLOWED_OPERATION = "ListBackups"
REST_ENDPOINT = "GET /v3/{project_id}/backups"

# Mutating CBR intents / operation names — strictly rejected by the guard.
# Read-only vocabulary (list/show/get/describe/details) never matches. The bare
# word "backup" is intentionally NOT a keyword (the read-only operation itself
# is ``ListBackups``); only concrete mutating verbs are listed.
WRITE_INTENT_KEYWORDS = (
    "createbackup",
    "deletebackup",
    "updatebackup",
    "restorebackup",
    "copybackup",
    "importbackup",
    "syncbackup",
    "backuprestore",
    "backupreplicate",
    "createvault",
    "deletevault",
    "updatevault",
    "batchupdatevault",
    "changefvaultcharge",
    "changecharge",
    "addvaultresource",
    "removevaultresource",
    "migratevaultresource",
    "associatevaultpolicy",
    "disassociatevaultpolicy",
    "bindpolicy",
    "unbindpolicy",
    "addresource",
    "removeresource",
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
    "terminate",
    "destroy",
    "remove",
    "purge",
    "reset",
)

# Read-only option flags whose *values* are filter / query data (e.g. a backup
# literally named "delete-me"). Their values must NOT be scanned by the
# write-intent guard. Both the underscore form (matches the real KooCLI
# parameter, e.g. ``--resource_id``) and the hyphenated alias are listed so a
# user can pass either. The ``--operation`` value is intentionally NOT excluded:
# it is validated by ``guard_operation()`` and scanned as defense in depth.
_VALUE_STRIPPED_FLAGS = (
    "--region",
    "-r",
    "--name",
    "--status",
    "--resource-id",
    "--resource_id",
    "--resource-name",
    "--resource_name",
    "--resource-type",
    "--resource_type",
    "--vault-id",
    "--vault_id",
    "--image-type",
    "--image_type",
    "--checkpoint-id",
    "--checkpoint_id",
    "--resource-az",
    "--resource_az",
    "--enterprise-project-id",
    "--enterprise_project_id",
    "--own-type",
    "--own_type",
    "--member-status",
    "--member_status",
    "--parent-id",
    "--parent_id",
    "--used-percent",
    "--used_percent",
    "--sort",
    "--marker",
    "--start-time",
    "--start_time",
    "--end-time",
    "--end_time",
    "--page-size",
    "--page_size",
    "--limit",
    "--offset",
)

# Preferred column order for the table view; remaining keys are appended sorted.
PREFERRED_COLUMNS = [
    "name",
    "id",
    "status",
    "resource_name",
    "resource_id",
    "resource_type",
    "resource_size",
    "vault_id",
    "image_type",
    "incremental",
    "created_at",
    "expired_at",
    "updated_at",
    "protected_at",
    "resource_az",
    "checkpoint_id",
    "parent_id",
    "enterprise_project_id",
    "provider_id",
    "version",
]

_BACKUP_LIST_KEYS = (
    "backups",
    "backup_list",
    "backup_resp",
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


class CbrListError(Exception):
    """Base error for the CBR backup list skill."""


class GuardError(CbrListError):
    """A write intent was detected and blocked (skill is read-only)."""


class ConfigError(CbrListError):
    """hcloud missing or credentials (AK/SK) not configured."""


class AuthError(CbrListError):
    """Authentication/authorization failure (invalid AK/SK or IAM 403)."""


class ApiError(CbrListError):
    """hcloud / network / unexpected API failure."""


def guard_write_intent(text):
    """Raise GuardError if ``text`` carries a mutating intent.

    Separators are normalized so ``--delete-backup``, ``DeleteBackup`` and
    ``delete_backup`` all hit the same keyword. Read-only vocabulary
    (list/show/get/describe) never matches.
    """
    low = re.sub(r"[\s_\-]+", "", str(text).lower())
    for keyword in WRITE_INTENT_KEYWORDS:
        if keyword in low:
            raise GuardError(
                "检测到写操作意图（关键词: %s）。本 skill 仅支持只读查询"
                "（CBR ListBackups），创建/删除/恢复/复制/迁移/绑定等变更操作已被守卫拦截。"
                % keyword
            )
    return False


def guard_operation(operation):
    """Only the read-only ListBackups operation may be executed."""
    if operation != ALLOWED_OPERATION:
        raise GuardError(
            "不允许的操作 %r：本 skill 仅允许只读操作 %s。"
            % (operation, ALLOWED_OPERATION)
        )
    return True


def guard_text_from_argv(argv):
    """Build the text the write-intent guard should scan.

    Scans flag names and positional tokens, but strips the values of the
    read-only filter flags (``--name`` / ``--status`` / ``--resource-id`` /
    ``--region`` / ``--page-size`` / ...): those are query data and may
    legitimately contain write-looking words (e.g. a backup named
    ``delete-me``).
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


# Native ListBackups query parameters (snake_case) exposed as CLI flags.
#
# KooCLI accepts only the underscore form (``--resource_id`` / ``--vault_id`` /
# ``--image_type`` / ...); the hyphenated form is rejected with
# ``[USE_ERROR]Invalid parameter``. The first element is therefore the *real*
# KooCLI flag emitted by ``build_command()``; the second is the filter dict key.
# The argparse layer additionally accepts the hyphenated alias for the user's
# convenience.
_FILTER_ARG_TO_PARAM = (
    ("--name", "name"),
    ("--status", "status"),
    ("--resource_id", "resource_id"),
    ("--resource_name", "resource_name"),
    ("--resource_type", "resource_type"),
    ("--vault_id", "vault_id"),
    ("--image_type", "image_type"),
)


def build_command(region, filters=None, limit=DEFAULT_PAGE_SIZE, offset=0):
    """Build the hcloud CBR ListBackups argv (without the executable).

    Mirrors the real KooCLI parameter list: ``--cli-region`` / ``--limit`` /
    ``--offset`` plus the native server-side filters. Only read-only
    parameters are ever emitted (verified against
    ``huaweicloudsdkcbr.v1.ListBackupsRequest.openapi_types``). Filter flags are
    emitted in the underscore form KooCLI requires (``--resource_id``,
    ``--resource_name``, ``--resource_type``, ``--vault_id``, ``--image_type``).
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
    return argv


def _hcloud_executable():
    return os.environ.get("CBR_LIST_HCLOUD_BIN", "hcloud")


def run_hcloud(argv):
    """Execute hcloud and return (stdout, stderr, returncode)."""
    cmd = [_hcloud_executable()]
    extra = os.environ.get("CBR_LIST_HCLOUD_ARGS", "").split()
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
            "hcloud 参数错误（KooCLI 拒绝了该参数组合，退出码 %s）：CBR ListBackups "
            "真实参数清单可通过 `hcloud CBR ListBackups --help` 查看。详情：%s"
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


def extract_backups(payload):
    """Pull the backup list out of a ListBackups response."""
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        for key in _BACKUP_LIST_KEYS:
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


def sdk_backup_to_dict(backup):
    """Convert a ``huaweicloudsdkcbr`` BackupResp into a wire-name dict.

    The SDK ``to_dict()`` emits Python attribute names; the OpenAPI JSON uses
    wire names. Remapping through ``BackupResp.attribute_map`` keeps both
    execution paths producing the same shape.
    """
    if isinstance(backup, dict):
        raw = dict(backup)
    else:
        try:
            raw = backup.to_dict()
        except AttributeError:
            return dict(backup)
    if not isinstance(raw, dict):
        return {}
    try:
        from huaweicloudsdkcbr.v1 import BackupResp
        attr_map = BackupResp.attribute_map
    except Exception:
        attr_map = {}
    out = {}
    attr_keys = set(attr_map.keys())
    for attr, wire in attr_map.items():
        if attr in raw and raw[attr] is not None:
            value = raw[attr]
            out[wire] = value.isoformat() if hasattr(value, "isoformat") else value
    for key, value in raw.items():
        if key not in attr_keys and key not in out and value is not None:
            out[key] = value.isoformat() if hasattr(value, "isoformat") else value
    return out


def list_backups_via_sdk(region, filters=None, limit=DEFAULT_PAGE_SIZE, max_pages=100):
    """SDK fallback: query backups through ``huaweicloudsdkcbr`` v1.

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
        from huaweicloudsdkcbr.v1 import CbrClient, ListBackupsRequest
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
    backups = []
    offset = 0
    for _ in range(max_pages):
        request = ListBackupsRequest(
            limit=limit, offset=offset,
            name=filters.get("name"),
            status=filters.get("status"),
            resource_id=filters.get("resource_id"),
            resource_name=filters.get("resource_name"),
            resource_type=filters.get("resource_type"),
            vault_id=filters.get("vault_id"),
            image_type=filters.get("image_type"),
        )
        try:
            response = client.list_backups(request)
        except Exception as exc:
            low = str(exc).lower()
            if any(p in low for p in _AUTH_PATTERNS):
                raise AuthError(
                    "无权限访问 CBR，请检查 IAM 权限（403）。详情：%s" % str(exc)[:300]
                )
            raise ApiError("SDK 调用失败：%s" % str(exc)[:300])
        batch = list(response.backups or [])
        backups.extend(sdk_backup_to_dict(backup) for backup in batch)
        total = getattr(response, "count", None)
        if total is not None and len(backups) >= total:
            break
        if len(batch) < limit:
            break
        offset += len(batch)
    else:
        raise ApiError("翻页超过 %d 页仍未取完，已中止以防死循环。" % max_pages)
    return backups


def list_backups(region, filters=None, limit=DEFAULT_PAGE_SIZE, max_pages=100):
    """Query all CBR backups (paged); KooCLI first, SDK fallback."""
    backups = []
    offset = 0
    for _page in range(max_pages):
        argv = build_command(region, filters=filters, limit=limit, offset=offset)
        try:
            stdout, stderr, returncode = run_hcloud(argv)
        except ConfigError:
            # hcloud binary missing → one-shot SDK fallback (no CLI retry).
            backups = list_backups_via_sdk(
                region, filters=filters, limit=limit, max_pages=max_pages)
            break
        if returncode != 0 or _USE_ERROR_MARKER in (stdout + " " + stderr).lower():
            # KooCLI usage errors print [USE_ERROR] on stdout with rc=0.
            raise classify_hcloud_failure(stdout, stderr, returncode)
        payload = extract_json(stdout)
        batch = extract_backups(payload)
        backups.extend(batch)
        if not _has_more(batch, len(backups), limit, payload):
            break
        offset += len(batch) if batch else limit
    else:
        raise ApiError("翻页超过 %d 页仍未取完，已中止以防死循环。" % max_pages)
    return backups


def _field(backup, *names, default="-"):
    for name in names:
        if name in backup and backup[name] not in (None, ""):
            return backup[name]
    return default


def _get(backup, *names, default=None):
    """Return the first present, non-empty value among ``names``."""
    for name in names:
        if name in backup and backup[name] not in (None, ""):
            return backup[name]
    return default


def normalize_backup(backup):
    """Flatten datetime-ish / nested fields into table-friendly keys."""
    flat = dict(backup)
    for key in ("created_at", "expired_at", "updated_at", "protected_at"):
        value = _get(backup, key)
        if value is not None and hasattr(value, "isoformat"):
            flat[key] = value.isoformat()
    az = _get(backup, "resource_az", "az_name", "az")
    if az is not None:
        flat["resource_az"] = az
    return flat


def filter_backups(backups, name=None, status=None, resource_id=None,
                   resource_name=None, resource_type=None, vault_id=None,
                   image_type=None):
    """Apply client-side name / status / resource / vault filters.

    The native ``ListBackups`` request already accepts these as server-side
    parameters; this client-side pass guarantees the rendered rows honour the
    requested filters even if a backend ignores or loosely interprets a
    parameter. ``name`` / ``resource_name`` are case-insensitive substring
    matches; the rest are case-insensitive exact matches.
    """
    result = list(backups)
    if name:
        needle = str(name).lower()
        result = [b for b in result
                  if needle in str(_field(b, "name", "id", default="")).lower()]
    if status:
        needle = str(status).lower()
        result = [b for b in result
                  if str(_field(b, "status", default="")).lower() == needle]
    if resource_id:
        needle = str(resource_id).lower()
        result = [b for b in result
                  if str(_field(b, "resource_id", default="")).lower() == needle]
    if resource_name:
        needle = str(resource_name).lower()
        result = [b for b in result
                  if needle in str(_field(b, "resource_name", default="")).lower()]
    if resource_type:
        needle = str(resource_type).lower()
        result = [b for b in result
                  if str(_field(b, "resource_type", default="")).lower() == needle]
    if vault_id:
        needle = str(vault_id).lower()
        result = [b for b in result
                  if str(_field(b, "vault_id", default="")).lower() == needle]
    if image_type:
        needle = str(image_type).lower()
        result = [b for b in result
                  if str(_field(b, "image_type", default="")).lower() == needle]
    return result


def backup_names(backups):
    names = []
    for backup in backups:
        name = _field(backup, "name", default=None)
        if name is None:
            name = _field(backup, "id")
        names.append(str(name))
    return names


def backup_summary_lines(backups):
    """Compact ``name  (id: ...)`` lines for the --names-only inventory mode."""
    lines = []
    for backup in backups:
        name = _field(backup, "name", default=None)
        if name is None:
            name = _field(backup, "id")
        bid = _field(backup, "id", default="-")
        lines.append("%s  (id: %s)" % (name, bid))
    return lines


def active_filter_descriptions(name=None, status=None, resource_id=None,
                               resource_name=None, resource_type=None,
                               vault_id=None, image_type=None):
    """Human-readable description of the filters actually applied."""
    filters = []
    if name:
        filters.append("name=%s" % name)
    if status:
        filters.append("status=%s" % status)
    if resource_id:
        filters.append("resource_id=%s" % resource_id)
    if resource_name:
        filters.append("resource_name=%s" % resource_name)
    if resource_type:
        filters.append("resource_type=%s" % resource_type)
    if vault_id:
        filters.append("vault_id=%s" % vault_id)
    if image_type:
        filters.append("image_type=%s" % image_type)
    return filters


def _cell(value):
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return str(value)


def render_table(backups):
    """Render full-field table output (union of all returned fields)."""
    rows_data = [normalize_backup(backup) for backup in backups]
    columns = []
    for key in PREFERRED_COLUMNS:
        if any(key in b for b in rows_data):
            columns.append(key)
    for key in sorted({k for b in rows_data for k in b}):
        if key not in columns:
            columns.append(key)
    if not columns:
        columns = ["name", "id"]
    rows = [[_cell(_field(b, col)) for col in columns] for b in rows_data]
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
        "resource_id": args.resource_id,
        "resource_name": args.resource_name,
        "resource_type": args.resource_type,
        "vault_id": args.vault_id,
        "image_type": args.image_type,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="查询华为云 CBR 备份列表（KooCLI hcloud CBR ListBackups，只读）。")
    parser.add_argument("-r", "--region", default=DEFAULT_REGION,
                        help="目标 Region（默认 %s）" % DEFAULT_REGION)
    parser.add_argument("--json", action="store_true", dest="as_json",
                        help="以 JSON 输出完整原始字段")
    parser.add_argument("--names-only", action="store_true", dest="names_only",
                        help="仅输出精简备份名称+ID 清单")
    parser.add_argument("--name", help="按备份名称过滤（服务端 + 客户端子串）")
    parser.add_argument("--status", help="按备份状态过滤（如 available/error）")
    parser.add_argument("--resource-id", "--resource_id", dest="resource_id",
                        help="按所属资源 ID 过滤（如云服务器/云硬盘 ID）")
    parser.add_argument("--resource-name", "--resource_name", dest="resource_name",
                        help="按所属资源名称过滤（客户端子串）")
    parser.add_argument("--resource-type", "--resource_type", dest="resource_type",
                        help="按资源类型过滤（如 OS::Nova::Server / OS::Cinder::Volume）")
    parser.add_argument("--vault-id", "--vault_id", dest="vault_id", help="按存储库 ID 过滤")
    parser.add_argument("--image-type", "--image_type", dest="image_type",
                        help="按备份类型过滤（如 backup / replication）")
    parser.add_argument("--page-size", "--page_size", type=int, default=DEFAULT_PAGE_SIZE,
                        dest="page_size", help="分页大小（默认 %d）" % DEFAULT_PAGE_SIZE)
    parser.add_argument("--operation", default=ALLOWED_OPERATION,
                        help="hcloud CBR 操作名（仅允许只读 %s）" % ALLOWED_OPERATION)

    # Write-intent guard runs on the RAW argv before argparse so a mutating flag
    # (e.g. `--delete-backup`) is reported as a guard violation rather than an
    # argparse "unrecognized argument" error. Filter values are read-only data
    # and deliberately not scanned.
    try:
        guard_write_intent(guard_text_from_argv(argv))
    except CbrListError as exc:
        print("[错误] %s" % exc, file=sys.stderr)
        return 1

    args = parser.parse_args(argv)

    try:
        guard_operation(args.operation)
        backups = list_backups(args.region, filters=_collect_filters(args),
                               limit=args.page_size)
    except CbrListError as exc:
        print("[错误] %s" % exc, file=sys.stderr)
        return 1

    filters = active_filter_descriptions(
        name=args.name, status=args.status, resource_id=args.resource_id,
        resource_name=args.resource_name, resource_type=args.resource_type,
        vault_id=args.vault_id, image_type=args.image_type)
    backups = filter_backups(
        backups, name=args.name, status=args.status,
        resource_id=args.resource_id, resource_name=args.resource_name,
        resource_type=args.resource_type, vault_id=args.vault_id,
        image_type=args.image_type)
    filter_suffix = "（过滤条件: %s）" % ", ".join(filters) if filters else ""

    if args.as_json:
        print(json.dumps(backups, ensure_ascii=False, indent=2))
    elif args.names_only:
        print("Region %s 的 CBR 备份清单（共 %d 个）：" % (args.region, len(backups)))
        for line in backup_summary_lines(backups):
            print("- %s" % line)
    elif not backups:
        print("当前区域（%s）无 CBR 备份%s。" % (args.region, filter_suffix))
    else:
        print("Region %s 的 CBR 备份列表（共 %d 个，完整字段）："
              % (args.region, len(backups)))
        print(render_table(backups))

    return 0


if __name__ == "__main__":
    sys.exit(main())