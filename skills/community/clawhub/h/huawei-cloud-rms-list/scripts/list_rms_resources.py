#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Query the Huawei Cloud RMS (Resource Management Service) resource inventory
(read-only) and render it as a table / JSON / Markdown / CSV.

The skill exposes the read-only RMS "unified resource view" APIs:

- ``ListAllResources`` — every resource under the account
  (``GET /v1/resource-manager/domains/{domain_id}/all-resources``), filterable
  by region / resource type / id / name / tags, marker-paged.
- ``ListResources`` — resources of one provider+type
  (``GET /v1/resource-manager/domains/{domain_id}/provider/{provider}/type/{type}/resources``).
- ``ListProviders`` — the cloud services (providers) that RMS tracks together
  with their resource types (``GET /v1/resource-manager/domains/{domain_id}/providers``).
- ``ListRegions`` — the regions known to RMS
  (``GET /v1/resource-manager/domains/{domain_id}/regions``).

KooCLI (``hcloud RMS <Operation>``) is the primary execution path; when the
hcloud binary is absent the script falls back to the official
``huaweicloudsdkrms`` v1 SDK (``RmsClient``), which resolves the domain id from
the credentials automatically.

A strict write-intent guard rejects any mutating intent so writes never happen:
the only operations ever constructed are the four read-only ones above. Nothing
is ever written back to the cloud.

Usage:
    python3 scripts/list_rms_resources.py [--region cn-north-4]
                                          [--format table|json|markdown|csv]
                                          [--output /path/out.json]
                                          [--list-providers | --list-regions]
                                          [--provider ecs --type cloudservers]
                                          [--type ecs.cloudservers]
                                          [--region-id cn-north-4]
                                          [--ep-id 0] [--id <resource-id>]
                                          [--name web-01]
                                          [--tags key=value ...]
                                          [--limit 100] [--offset 0]
                                          [--track Tracked|Untracked]

Environment overrides (mostly for tests):
    RMS_LIST_HCLOUD_BIN    hcloud executable (default "hcloud")
    RMS_LIST_HCLOUD_ARGS   extra args appended AFTER the read-only argv
                           (guard-scanned, read-only)
    RMS_LIST_SQC_BIN       skill-quality-cli executable override
"""

import argparse
import csv
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime

# Keep the shipped skill directory clean: never emit __pycache__/*.pyc.
sys.dont_write_bytecode = True

DEFAULT_REGION = "cn-north-4"
DEFAULT_PAGE_SIZE = 100
DEFAULT_FORMAT = "table"
SERVICE = "RMS"

# Read-only operations this skill is allowed to call.
ALLOWED_OPERATIONS = (
    "ListAllResources",
    "ListResources",
    "ListProviders",
    "ListRegions",
)
DEFAULT_OPERATION = "ListAllResources"

# Official REST paths (verified in the huaweicloudsdkrms v1 *_http_info metadata).
REST_PATHS = {
    "ListAllResources": "/v1/resource-manager/domains/{domain_id}/all-resources",
    "ListResources": "/v1/resource-manager/domains/{domain_id}/provider/{provider}/type/{type}/resources",
    "ListProviders": "/v1/resource-manager/domains/{domain_id}/providers",
    "ListRegions": "/v1/resource-manager/domains/{domain_id}/regions",
}

# Skill-quality telemetry: every hcloud call on the script execution path is
# reported through skill-quality-cli. When the CLI is unavailable — or
# SKILL_QUALITY_REPORT=0 — the call degrades to bare hcloud.
SKILL_QUALITY_SKILL_NAME = "huawei-cloud-rms-list"
_QUALITY_OFF_VALUES = ("0", "false", "no", "off")

# Markdown report column order for the ListAllResources / ListResources view.
RESOURCE_MD_HEADERS = [
    "资源 ID", "名称", "云服务", "资源类型", "区域", "企业项目",
    "状态", "创建时间", "更新时间",
]

_FIELD_MISSING = "-"

# Mutating RMS operations / intents — strictly rejected by the guard.
WRITE_INTENT_KEYWORDS = (
    "createconfigurationaggregator",
    "deleteconfigurationaggregator",
    "updateconfigurationaggregator",
    "createaggregationauthorization",
    "deleteaggregationauthorization",
    "deletependingaggregationrequest",
    "createorganizationpolicyassignment",
    "deleteorganizationpolicyassignment",
    "createpolicyassignments",
    "deletepolicyassignment",
    "updatepolicyassignment",
    "enablepolicyassignment",
    "disablepolicyassignment",
    "createstoredquery",
    "deletestoredquery",
    "updatestoredquery",
    "createtrackerconfig",
    "deletetrackerconfig",
    "runevaluationbypolicyassignmentid",
    "runaggregateresourcequery",
    "runquery",
    "updatepolicystate",
    "aggregateresourceconfig",
    "create",
    "delete",
    "update",
    "modify",
    "enable",
    "disable",
    "destroy",
    "remove",
    "reset",
    "attach",
    "detach",
)

# Read-only option flags whose *values* are filter/output data (e.g. a report
# path such as "rms-delete-report.json", a resource name, a region label). Their
# values must NOT be scanned by the write-intent guard.
_VALUE_STRIPPED_FLAGS = (
    "--region",
    "-r",
    "--format",
    "-f",
    "--output",
    "-o",
    "--domain-id",
    "--provider",
    "--type",
    "--region-id",
    "--ep-id",
    "--id",
    "--name",
    "--tags",
    "--tag",
    "--limit",
    "--offset",
    "--track",
    "--language",
    "--page-size",
    "--max-pages",
)

# Preferred column order for the table / CSV views; remaining keys are appended.
RESOURCE_PREFERRED_COLUMNS = [
    "id",
    "name",
    "provider",
    "type",
    "region_id",
    "project_name",
    "ep_name",
    "provisioning_state",
    "created",
    "updated",
    "tags",
]
PROVIDER_PREFERRED_COLUMNS = [
    "provider",
    "display_name",
    "category_display_name",
    "resource_types",
]
REGION_PREFERRED_COLUMNS = ["region_id", "display_name"]

# Response container keys per operation.
_CONTAINER_KEYS = {
    "ListAllResources": ("resources",),
    "ListResources": ("resources",),
    "ListProviders": ("resource_providers",),
    "ListRegions": ("value",),
}

# AK/SK environment variable names, read *directly* (never by enumerating
# os.environ). The official SDK's GlobalCredentials does not auto-discover
# credentials, so the fallback path resolves them explicitly.
_AK_ENV_NAMES = (
    "HUAWEICLOUD_SDK_AK",
    "HUAWEI_ACCESS_KEY",
    "HW_ACCESS_KEY",
    "HWC_ACCESS_KEY",
    "HUAWEI_AK",
    "HW_AK",
)
_SK_ENV_NAMES = (
    "HUAWEICLOUD_SDK_SK",
    "HUAWEI_SECRET_KEY",
    "HW_SECRET_KEY",
    "HWC_SECRET_KEY",
    "HUAWEI_SK",
    "HW_SK",
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
    "not authorized",
    "access denied",
    "permission denied",
    "rms:resources:list",
    "rms.00010006",
    "认证失败",
    "权限不足",
)

# KooCLI prints usage errors (e.g. "[USE_ERROR]Invalid parameter: xxx") on
# stdout WITH exit code 0 — the marker is treated as a hard failure.
_USE_ERROR_MARKER = "[use_error]"


class RmsListError(Exception):
    """Base error for the RMS resource inventory skill."""


class GuardError(RmsListError):
    """A write intent was detected and blocked (skill is read-only)."""


class ConfigError(RmsListError):
    """hcloud/SDK missing or credentials (AK/SK) not configured."""


class AuthError(RmsListError):
    """Authentication/authorization failure (invalid AK/SK or IAM 403)."""


class ApiError(RmsListError):
    """hcloud / network / unexpected API failure."""


class ExportError(RmsListError):
    """The export file could not be produced (bad path / write failure)."""


def guard_write_intent(text):
    """Raise GuardError if ``text`` carries a mutating intent.

    Normalizes separators so ``--create-aggregator``, ``CreateConfigurationAggregator``,
    and ``create_aggregator`` all hit the same keyword. Read-only vocabulary
    (list/show/count/collect) never matches.
    """
    low = re.sub(r"[\s_\-]+", "", str(text).lower())
    for keyword in WRITE_INTENT_KEYWORDS:
        if keyword in low:
            raise GuardError(
                "检测到写操作意图（关键词: %s）。本 skill 仅支持 RMS 只读查询"
                "（ListAllResources / ListResources / ListProviders / ListRegions），"
                "创建/删除/更新等变更操作已被守卫拦截。" % keyword
            )
    return False


def guard_operation(operation):
    """Only the four read-only RMS operations may be executed."""
    if operation not in ALLOWED_OPERATIONS:
        raise GuardError(
            "不允许的操作 %r：本 skill 仅允许只读操作 %s。"
            % (operation, "/".join(ALLOWED_OPERATIONS))
        )
    return True


def guard_text_from_argv(argv):
    """Build the text the write-intent guard should scan.

    Scans flag names and positional tokens, but strips the values of the
    read-only filter flags and of the local-output/format flags: those are pure
    read / file-path data and may legitimately contain write-looking words.
    A *flag* following such an option is never swallowed.
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


def resolve_operation(provider=None, resource_type=None, list_providers=False,
                      list_regions=False, explicit=None):
    """Pick the read-only operation from the user's intent.

    ``--list-providers`` / ``--list-regions`` win; a ``--provider`` + ``--type``
    pair selects the provider+type-scoped ListResources; otherwise the
    account-wide ListAllResources is used. An explicit ``--operation`` value is
    honoured (and later validated against the allow-list).
    """
    if list_providers:
        return "ListProviders"
    if list_regions:
        return "ListRegions"
    if provider and resource_type:
        return "ListResources"
    if provider or resource_type:
        raise ApiError(
            "ListResources（按 provider/type 查询）需要同时提供 --provider 与 --type；"
            "只做全量资源清单请省略二者（默认 ListAllResources）。"
        )
    if explicit:
        return explicit
    return DEFAULT_OPERATION


def build_command(operation, region, domain_id=None, provider=None,
                  resource_type=None, region_id=None, ep_id=None,
                  resource_id=None, name=None, tags=None, limit=DEFAULT_PAGE_SIZE,
                  marker=None, offset=None, track=None, language=None):
    """Build the hcloud RMS argv (without the executable).

    Mirrors the real KooCLI parameter list for the four read-only operations.
    ``domain_id`` is a required path parameter for RMS; when omitted KooCLI
    resolves it from the active profile.
    """
    argv = [SERVICE, operation, "--cli-region=%s" % region]
    if domain_id:
        argv.append("--domain_id=%s" % domain_id)
    if language:
        argv.append("--X-Language=%s" % language)
    if operation == "ListAllResources":
        if region_id:
            argv.append("--region_id=%s" % region_id)
        if ep_id:
            argv.append("--ep_id=%s" % ep_id)
        if resource_type:
            argv.append("--type=%s" % resource_type)
        if resource_id:
            argv.append("--id=%s" % resource_id)
        if name:
            argv.append("--name=%s" % name)
        for index, tag in enumerate(tags or [], start=1):
            argv.append("--tags.%d=%s" % (index, tag))
        if limit is not None:
            argv.append("--limit=%d" % limit)
        if marker:
            argv.append("--marker=%s" % marker)
    elif operation == "ListResources":
        argv.append("--provider=%s" % provider)
        argv.append("--type=%s" % resource_type)
        if region_id:
            argv.append("--region_id=%s" % region_id)
        if ep_id:
            argv.append("--ep_id=%s" % ep_id)
        if limit is not None:
            argv.append("--limit=%d" % limit)
        if marker:
            argv.append("--marker=%s" % marker)
    elif operation == "ListProviders":
        if limit is not None:
            argv.append("--limit=%d" % limit)
        # KooCLI fills offset=0 when omitted and the API rejects it (min 1).
        argv.append("--offset=%d" % (1 if offset is None else offset))
        if track:
            argv.append("--track=%s" % track)
    elif operation == "ListRegions":
        pass
    return argv


def _hcloud_executable():
    return os.environ.get("RMS_LIST_HCLOUD_BIN") or "hcloud"


def _hcloud_resolvable():
    """True when the hcloud executable can actually be launched.

    Checked *before* wrapping the command with skill-quality-cli: the wrapper
    would otherwise swallow a missing-hcloud failure into its own non-zero exit,
    which ``run_hcloud`` cannot tell apart from a genuine CLI error — and that
    would silently disable the SDK fallback.
    """
    exe = _hcloud_executable()
    if os.path.dirname(exe):
        return os.path.isfile(exe) and os.access(exe, os.X_OK)
    return shutil.which(exe) is not None


def _quality_report_enabled():
    value = os.environ.get("SKILL_QUALITY_REPORT")
    if value is None:
        return True
    return value.strip().lower() not in _QUALITY_OFF_VALUES


def _skill_quality_executable():
    override = os.environ.get("RMS_LIST_SQC_BIN")
    if override:
        return override
    found = shutil.which("skill-quality-cli")
    if found:
        return found
    local = os.path.join(os.path.expanduser("~"), ".local", "bin",
                         "skill-quality-cli")
    if os.path.isfile(local) and os.access(local, os.X_OK):
        return local
    return None


def _hcloud_argv(argv):
    cmd = [_hcloud_executable()]
    cmd.extend(argv)
    extra = os.environ.get("RMS_LIST_HCLOUD_ARGS", "").split()
    if extra:
        cmd.extend(extra)
    return cmd


def build_hcloud_command(argv):
    """Build the hcloud execution argv, wrapping it with skill-quality-cli.

    Every CLI call is reported as ``skill-quality-cli run --skill-name
    huawei-cloud-rms-list -- hcloud ...`` (the mandatory wrapping 口径, enforced
    here on the script path). The command degrades to bare hcloud when the
    telemetry CLI is missing or ``SKILL_QUALITY_REPORT=0``; an explicit
    ``RMS_LIST_HCLOUD_BIN`` override (offline mock / verification) is run
    verbatim. When hcloud itself is not resolvable the wrapping is skipped so
    ``run_hcloud`` raises ``FileNotFoundError`` → ``ConfigError`` → SDK fallback.
    """
    hcloud_cmd = _hcloud_argv(argv)
    if os.environ.get("RMS_LIST_HCLOUD_BIN"):
        return hcloud_cmd
    if not _hcloud_resolvable():
        return hcloud_cmd
    if not _quality_report_enabled():
        return hcloud_cmd
    quality_cli = _skill_quality_executable()
    if not quality_cli:
        return hcloud_cmd
    return ([quality_cli, "run", "--skill-name", SKILL_QUALITY_SKILL_NAME, "--"]
            + hcloud_cmd)


def run_hcloud(argv):
    """Execute hcloud through skill-quality-cli when available."""
    extra = os.environ.get("RMS_LIST_HCLOUD_ARGS", "").split()
    if extra:
        guard_write_intent(" ".join(extra))
    cmd = build_hcloud_command(argv)
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
            "hcloud 参数错误（KooCLI 拒绝了该参数组合，退出码 %s）：RMS 真实参数清单"
            "可通过 `hcloud RMS ListAllResources --cli-region=<region> --help` 查看。"
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
            "无权限访问资源管理服务（RMS），请检查 IAM 权限"
            "（403：AK/SK 无效或未授予 rms:resources:list 权限），"
            "参见 references/iam-policies.md。详情：%s" % blob[:300]
        )
    return ApiError(
        "hcloud 调用失败（退出码 %s）：%s" % (returncode, blob[:300])
    )


def _payload_error(payload):
    """Return the error text if a response payload is an error envelope.

    KooCLI returns HTTP-level API errors (e.g. ``RMS.00010006`` insufficient
    permission) as a body on **stdout with exit code 0**. Such an envelope must
    be surfaced as an explicit error, never silently treated as an empty list.
    """
    if not isinstance(payload, dict):
        return None
    err = payload.get("error")
    if isinstance(err, dict):
        code = str(err.get("error_code") or err.get("code") or "")
        msg = str(err.get("error_msg") or err.get("message") or "")
        text = ("%s %s" % (code, msg)).strip()
        return text or None
    if isinstance(err, str) and err.strip():
        return err.strip()
    if payload.get("error_code") and payload.get("error_msg"):
        return ("%s %s" % (payload.get("error_code"), payload.get("error_msg"))).strip()
    for ckey in ("errorCode", "errorMsg", "error_message"):
        if payload.get(ckey):
            return str(payload[ckey])
    for mkey in ("error_msg", "message"):
        if payload.get(mkey):
            return str(payload[mkey])
    return None


def extract_items(payload, operation):
    """Pull the item list out of a response payload for the given operation."""
    keys = _CONTAINER_KEYS.get(operation, ())
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        for key in keys:
            value = payload.get(key)
            if isinstance(value, list):
                return value
    return []


def _page_info(payload):
    """Return (current_count, next_marker) from a PageInfo-style payload."""
    if not isinstance(payload, dict):
        return None, None
    info = payload.get("page_info")
    if not isinstance(info, dict):
        return None, None
    current = info.get("current_count")
    try:
        current = int(current)
    except (TypeError, ValueError):
        current = None
    return current, info.get("next_marker") or None


def _total_count(payload):
    if not isinstance(payload, dict):
        return None
    try:
        return int(payload.get("total_count"))
    except (TypeError, ValueError):
        return None


def _env_value(names):
    for name in names:
        value = os.environ.get(name)
        if value:
            return value
    return None


def _jsonable(value):
    return json.loads(json.dumps(value, ensure_ascii=False, default=str))


def list_items_via_sdk(operation, region, domain_id=None, provider=None,
                       resource_type=None, region_id=None, ep_id=None,
                       resource_id=None, name=None, tags=None,
                       limit=DEFAULT_PAGE_SIZE, offset=None, track=None,
                       max_pages=100):
    """SDK fallback: query RMS through ``huaweicloudsdkrms`` v1.

    Only invoked when hcloud is not installed. Credentials are taken from the
    explicitly named AK/SK environment variables (never passed as literals).
    RMS is a global service, so the SDK client is authenticated with
    ``GlobalCredentials`` and the domain id is resolved by the SDK from the
    credentials (the request models carry no domain_id).
    """
    ak = _env_value(_AK_ENV_NAMES)
    sk = _env_value(_SK_ENV_NAMES)
    if not ak or not sk:
        raise ConfigError(
            "SDK 回退缺少 AK/SK 凭证：官方 SDK 的 GlobalCredentials 不会自动读取环境"
            "变量，且当前环境未检测到白名单中的 AK/SK 环境变量（如"
            " HUAWEICLOUD_SDK_AK / HUAWEI_ACCESS_KEY 与 HUAWEICLOUD_SDK_SK /"
            " HUAWEI_SECRET_KEY）。请在会话外设置其中之一（严禁在对话中粘贴 AK/SK），"
            "参见 references/cli-installation-guide.md。"
        )
    try:
        from huaweicloudsdkcore.auth.credentials import GlobalCredentials
        from huaweicloudsdkcore.region.region import Region
        from huaweicloudsdkcore.http.http_config import HttpConfig
        from huaweicloudsdkrms.v1 import (
            RmsClient,
            ListAllResourcesRequest,
            ListResourcesRequest,
            ListProvidersRequest,
            ListRegionsRequest,
        )
        from huaweicloudsdkrms.v1.region.rms_region import RmsRegion
    except ImportError as exc:
        raise ConfigError(
            "未找到 hcloud（KooCLI），且 huaweicloudsdkcore/huaweicloudsdkrms 未安装，"
            "无法回退到 SDK。请安装 KooCLI 或先运行 "
            "`python3 scripts/ensure_env.py`（pip install huaweicloudsdkcore "
            "huaweicloudsdkrms）。详情：%s" % exc
        )
    credentials = GlobalCredentials(ak=ak, sk=sk)  # env-sourced, never literals
    try:
        try:
            region_obj = RmsRegion.value_of(region)
        except (ValueError, KeyError, AttributeError):
            region_obj = Region(region, "https://rms.myhuaweicloud.com")
        client = RmsClient.new_builder() \
            .with_credentials(credentials) \
            .with_region(region_obj) \
            .with_http_config(HttpConfig.get_default_config()) \
            .build()
    except Exception as exc:
        raise ConfigError(
            "SDK 初始化失败（region=%s）：%s。请检查 huaweicloudsdkrms 安装与区域配置。"
            % (region, exc)
        )

    items = []
    if operation == "ListAllResources":
        marker = None
        for _ in range(max_pages):
            request = ListAllResourcesRequest(
                region_id=region_id, ep_id=ep_id, type=resource_type,
                limit=limit, marker=marker, id=resource_id, name=name,
                tags=tags,
            )
            response = _sdk_call(client.list_all_resources, request)
            batch = [_jsonable(r.to_dict()) for r in (response.resources or [])]
            items.extend(batch)
            _, marker = _page_info(_jsonable(response.to_dict()))
            if not batch or not marker:
                break
        else:
            raise ApiError("翻页超过 %d 页仍未取完，已中止以防死循环。" % max_pages)
        return items
    if operation == "ListResources":
        marker = None
        for _ in range(max_pages):
            request = ListResourcesRequest(
                provider=provider, type=resource_type, region_id=region_id,
                ep_id=ep_id, limit=limit, marker=marker,
            )
            response = _sdk_call(client.list_resources, request)
            batch = [_jsonable(r.to_dict()) for r in (response.resources or [])]
            items.extend(batch)
            _, marker = _page_info(_jsonable(response.to_dict()))
            if not batch or not marker:
                break
        else:
            raise ApiError("翻页超过 %d 页仍未取完，已中止以防死循环。" % max_pages)
        return items
    if operation == "ListProviders":
        offset_val = 1 if offset is None else offset
        for _ in range(max_pages):
            request = ListProvidersRequest(offset=offset_val, limit=limit,
                                           track=track)
            response = _sdk_call(client.list_providers, request)
            batch = [_jsonable(p.to_dict()) for p in (response.resource_providers or [])]
            items.extend(batch)
            total = getattr(response, "total_count", None)
            if not batch or len(batch) < limit:
                break
            if total is not None:
                try:
                    if len(items) >= int(total):
                        break
                except (TypeError, ValueError):
                    pass
            offset_val += limit
        else:
            raise ApiError("翻页超过 %d 页仍未取完，已中止以防死循环。" % max_pages)
        return items
    if operation == "ListRegions":
        request = ListRegionsRequest()
        response = _sdk_call(client.list_regions, request)
        return [_jsonable(r.to_dict()) for r in (response.value or [])]
    raise GuardError("不允许的操作 %r" % operation)


def _sdk_call(fn, request):
    try:
        return fn(request)
    except Exception as exc:
        low = str(exc).lower()
        if any(p in low for p in _AUTH_PATTERNS):
            raise AuthError(
                "无权限访问资源管理服务（RMS），请检查 IAM 权限（403）。详情：%s"
                % str(exc)[:300]
            )
        raise ApiError("SDK 调用失败：%s" % str(exc)[:300])


def list_items(operation, region, domain_id=None, provider=None,
               resource_type=None, region_id=None, ep_id=None,
               resource_id=None, name=None, tags=None, limit=DEFAULT_PAGE_SIZE,
               offset=None, track=None, language=None, max_pages=100):
    """Query RMS items (page-paged); KooCLI first, SDK fallback on missing hcloud."""
    items = []
    if operation in ("ListAllResources", "ListResources"):
        marker = None
        for _page in range(max_pages):
            argv = build_command(
                operation, region, domain_id=domain_id, provider=provider,
                resource_type=resource_type, region_id=region_id, ep_id=ep_id,
                resource_id=resource_id, name=name, tags=tags, limit=limit,
                marker=marker, language=language,
            )
            try:
                stdout, stderr, returncode = run_hcloud(argv)
            except ConfigError:
                return list_items_via_sdk(
                    operation, region, domain_id=domain_id, provider=provider,
                    resource_type=resource_type, region_id=region_id, ep_id=ep_id,
                    resource_id=resource_id, name=name, tags=tags, limit=limit,
                    max_pages=max_pages,
                )
            if returncode != 0 or _USE_ERROR_MARKER in (stdout + " " + stderr).lower():
                raise classify_hcloud_failure(stdout, stderr, returncode)
            payload = extract_json(stdout)
            err_text = _payload_error(payload)
            if err_text:
                raise classify_hcloud_failure("", err_text, returncode)
            batch = extract_items(payload, operation)
            items.extend(batch)
            _, marker = _page_info(payload)
            if not batch or not marker:
                break
        else:
            raise ApiError("翻页超过 %d 页仍未取完，已中止以防死循环。" % max_pages)
        return items
    if operation == "ListProviders":
        offset_val = 1 if offset is None else offset
        for _page in range(max_pages):
            argv = build_command(operation, region, domain_id=domain_id,
                                 limit=limit, offset=offset_val, track=track,
                                 language=language)
            try:
                stdout, stderr, returncode = run_hcloud(argv)
            except ConfigError:
                return list_items_via_sdk(
                    operation, region, domain_id=domain_id, limit=limit,
                    offset=offset, track=track, max_pages=max_pages,
                )
            if returncode != 0 or _USE_ERROR_MARKER in (stdout + " " + stderr).lower():
                raise classify_hcloud_failure(stdout, stderr, returncode)
            payload = extract_json(stdout)
            err_text = _payload_error(payload)
            if err_text:
                raise classify_hcloud_failure("", err_text, returncode)
            batch = extract_items(payload, operation)
            items.extend(batch)
            total = _total_count(payload)
            if not batch or len(batch) < limit:
                break
            if total is not None and len(items) >= total:
                break
            offset_val += limit
        else:
            raise ApiError("翻页超过 %d 页仍未取完，已中止以防死循环。" % max_pages)
        return items
    if operation == "ListRegions":
        argv = build_command(operation, region, domain_id=domain_id,
                             language=language)
        try:
            stdout, stderr, returncode = run_hcloud(argv)
        except ConfigError:
            return list_items_via_sdk(operation, region, domain_id=domain_id,
                                      max_pages=max_pages)
        if returncode != 0 or _USE_ERROR_MARKER in (stdout + " " + stderr).lower():
            raise classify_hcloud_failure(stdout, stderr, returncode)
        payload = extract_json(stdout)
        err_text = _payload_error(payload)
        if err_text:
            raise classify_hcloud_failure("", err_text, returncode)
        return extract_items(payload, operation)
    raise GuardError("不允许的操作 %r" % operation)


def normalize_record(record):
    """Flatten provider.resource_types and tags into table-friendly strings."""
    flat = dict(record)
    if "tags" in record:
        tags = record.get("tags")
        if isinstance(tags, dict):
            flat["tags"] = ",".join("%s=%s" % (k, v) for k, v in tags.items()) or _FIELD_MISSING
        elif isinstance(tags, list):
            pairs = []
            for tag in tags:
                if isinstance(tag, dict):
                    pairs.append("%s=%s" % (tag.get("key", ""), tag.get("value", "")))
                else:
                    pairs.append(str(tag))
            flat["tags"] = ",".join(pairs) if pairs else _FIELD_MISSING
        else:
            flat["tags"] = _FIELD_MISSING
    rtypes = record.get("resource_types")
    if isinstance(rtypes, list):
        names = []
        for rt in rtypes:
            if isinstance(rt, dict):
                names.append(rt.get("name") or rt.get("display_name") or "")
            else:
                names.append(str(rt))
        flat["resource_types"] = ",".join(n for n in names if n) or _FIELD_MISSING
    return flat


def _field(record, *names, default=_FIELD_MISSING):
    for name in names:
        if name in record and record[name] not in (None, ""):
            return record[name]
    return default


def _cell(value):
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return str(value)


def _md_escape(value):
    return _cell(value).replace("|", "\\|").replace("\n", " ").replace("\r", " ")


def _columns(rows_data, preferred):
    columns = []
    for key in preferred:
        if any(key in c for c in rows_data):
            columns.append(key)
    for key in sorted({k for c in rows_data for k in c}):
        if key not in columns:
            columns.append(key)
    return columns


def _preferred_for(operation):
    if operation == "ListProviders":
        return PROVIDER_PREFERRED_COLUMNS
    if operation == "ListRegions":
        return REGION_PREFERRED_COLUMNS
    return RESOURCE_PREFERRED_COLUMNS


def render_table(items, operation):
    rows_data = [normalize_record(i) for i in items]
    columns = _columns(rows_data, _preferred_for(operation))
    if not columns:
        columns = ["(empty)"]
    rows = [[_cell(_field(r, col)) for col in columns] for r in rows_data]
    if rows:
        widths = [max(len(col), *(len(row[i]) for row in rows))
                  for i, col in enumerate(columns)]
    else:
        widths = [len(col) for col in columns]
    header = "  ".join(col.ljust(widths[i]) for i, col in enumerate(columns))
    separator = "  ".join("-" * w for w in widths)
    lines = [header, separator]
    for row in rows:
        lines.append("  ".join(row[i].ljust(widths[i]) for i in range(len(columns))))
    return "\n".join(lines)


def _resource_md_row(record):
    return [
        _md_escape(_field(record, "id")),
        _md_escape(_field(record, "name")),
        _md_escape(_field(record, "provider")),
        _md_escape(_field(record, "type")),
        _md_escape(_field(record, "region_id")),
        _md_escape(_field(record, "ep_name", "ep_id")),
        _md_escape(_field(record, "provisioning_state", "status")),
        _md_escape(_field(record, "created")),
        _md_escape(_field(record, "updated")),
    ]


def render_markdown(items, operation, summary=False, region=None):
    """Render the inventory as a GitHub-flavored Markdown table.

    An empty list still renders a valid (header-only) table.
    """
    rows_data = [normalize_record(i) for i in items]
    if operation in ("ListAllResources", "ListResources"):
        headers = RESOURCE_MD_HEADERS
        body = [_resource_md_row(r) for r in rows_data]
    else:
        headers = [c for c in _preferred_for(operation)]
        body = [[_md_escape(_field(r, c)) for c in headers] for r in rows_data]
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in body:
        lines.append("| " + " | ".join(row) + " |")
    if summary:
        lines.append("")
        lines.append("**汇总**：共 %d 条 %s（Region %s）。"
                     % (len(items), operation, region or _FIELD_MISSING))
    return "\n".join(lines)


def render_csv(items, operation):
    rows_data = [normalize_record(i) for i in items]
    columns = _columns(rows_data, _preferred_for(operation)) or ["(empty)"]
    buffer = io.StringIO()
    writer = csv.writer(buffer, lineterminator="\n")
    writer.writerow(columns)
    for record in rows_data:
        writer.writerow([_cell(_field(record, col)) for col in columns])
    return buffer.getvalue().rstrip("\n")


def render_json(items):
    return json.dumps(items, ensure_ascii=False, indent=2)


def _render(items, operation, fmt, summary=False, region=None):
    if fmt == "json":
        return render_json(items)
    if fmt == "markdown":
        return render_markdown(items, operation, summary=summary, region=region)
    if fmt == "csv":
        return render_csv(items, operation)
    return render_table(items, operation)


def _extension(fmt):
    return "md" if fmt == "markdown" else fmt


def default_output_path(operation, region, fmt):
    prefix = {
        "ListAllResources": "rms_all_resources",
        "ListResources": "rms_resources",
        "ListProviders": "rms_providers",
        "ListRegions": "rms_regions",
    }.get(operation, "rms_resources")
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return "%s_%s_%s.%s" % (prefix, region, stamp, _extension(fmt))


def export_report(items, output_path, operation, fmt, summary=False, region=None):
    """Write the inventory into a report at ``output_path`` (atomic rename).

    Raises ExportError on an unusable path / write failure; no partial file is
    left behind.
    """
    items = list(items)
    output_path = os.path.abspath(output_path)
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.isdir(output_dir):
        try:
            os.makedirs(output_dir, exist_ok=True)
        except OSError as exc:
            raise ExportError(
                "无法创建输出目录 %r：%s。请检查 --output 路径。" % (output_dir, exc)
            )
    text = _render(items, operation, fmt, summary=summary, region=region)
    fd, tmp_path = tempfile.mkstemp(prefix=".rms_", suffix=".tmp",
                                    dir=output_dir or ".")
    os.close(fd)
    try:
        with open(tmp_path, "w", encoding="utf-8", newline="") as handle:
            handle.write(text + "\n")
        shutil.move(tmp_path, output_path)
    except Exception as exc:
        if os.path.exists(tmp_path):
            try:
                os.unlink(tmp_path)
            except OSError:
                pass
        raise ExportError("导出文件写出失败：%s（%s）" % (output_path, exc))
    return output_path


def active_filter_descriptions(domain_id=None, provider=None, resource_type=None,
                               region_id=None, ep_id=None, resource_id=None,
                               name=None, tags=None):
    filters = []
    if provider:
        filters.append("provider=%s" % provider)
    if resource_type:
        filters.append("type=%s" % resource_type)
    if region_id:
        filters.append("region_id=%s" % region_id)
    if ep_id:
        filters.append("ep_id=%s" % ep_id)
    if resource_id:
        filters.append("id=%s" % resource_id)
    if name:
        filters.append("name=%s" % name)
    if tags:
        filters.append("tags=%s" % ",".join(tags))
    return filters


def parse_args(argv):
    parser = argparse.ArgumentParser(
        description="查询华为云 RMS（资源管理服务）资源清单（只读）。")
    parser.add_argument("-r", "--region", default=DEFAULT_REGION,
                        help="目标 Region（默认 %s）" % DEFAULT_REGION)
    parser.add_argument("-f", "--format", default=DEFAULT_FORMAT,
                        choices=["table", "json", "markdown", "md", "csv"],
                        help="输出格式：table（默认）/ json / markdown（md）/ csv")
    parser.add_argument("-o", "--output", default=None,
                        help="导出文件路径（json/markdown/csv；默认 "
                             "rms_<view>_<region>_<timestamp>.<ext>）")
    parser.add_argument("--summary", action="store_true",
                        help="markdown 报表末尾追加汇总行")
    parser.add_argument("--domain-id", dest="domain_id", default=None,
                        help="账号 domain id（RMS 接口的必填路径参数，缺省由 KooCLI "
                             "profile / SDK 凭据解析）")
    parser.add_argument("--list-providers", dest="list_providers",
                        action="store_true", help="列出 RMS 支持的云服务（provider）与资源类型")
    parser.add_argument("--list-regions", dest="list_regions",
                        action="store_true", help="列出 RMS 已知的区域")
    parser.add_argument("--provider", default=None,
                        help="云服务名称（与 --type 同时给出时改用 ListResources 查询）")
    parser.add_argument("--type", dest="resource_type", default=None,
                        help="资源类型名称；全量模式下为 provider.type（如 ecs.cloudservers）")
    parser.add_argument("--region-id", dest="region_id", default=None,
                        help="按区域 ID 过滤（服务端查询参数）")
    parser.add_argument("--ep-id", dest="ep_id", default=None,
                        help="按企业项目 ID 过滤（服务端查询参数）")
    parser.add_argument("--id", dest="resource_id", default=None,
                        help="按资源 ID 过滤（ListAllResources 服务端查询参数）")
    parser.add_argument("--name", default=None,
                        help="按资源名称过滤（ListAllResources 服务端查询参数）")
    parser.add_argument("--tags", action="append", default=None,
                        help="按标签过滤，可重复（ListAllResources 服务端查询参数）")
    parser.add_argument("--limit", type=int, default=DEFAULT_PAGE_SIZE,
                        help="分页大小（默认 %d，自动翻页取全量）" % DEFAULT_PAGE_SIZE)
    parser.add_argument("--offset", type=int, default=None,
                        help="分页偏移（ListProviders）")
    parser.add_argument("--track", default=None,
                        help="资源是否默认收集（ListProviders，如 Tracked/Untracked）")
    parser.add_argument("--language", default=None,
                        help="返回信息语言（X-Language，默认 zh-cn）")
    parser.add_argument("--max-pages", type=int, default=100, dest="max_pages",
                        help="自动翻页的最大页数（默认 100，防死循环）")
    parser.add_argument("--operation", default=None,
                        help="显式指定只读操作（ListAllResources/ListResources/"
                             "ListProviders/ListRegions）")
    return parser.parse_args(argv)


def main(argv=None):
    raw_argv = argv if argv is not None else sys.argv[1:]

    # Write-intent guard runs on the RAW argv BEFORE argparse, so that a
    # mutating flag is reported as a guard violation rather than an argparse
    # "unrecognized argument" error.
    try:
        guard_write_intent(guard_text_from_argv(raw_argv))
    except RmsListError as exc:
        print("[错误] %s" % exc, file=sys.stderr)
        return 1

    args = parse_args(argv)

    try:
        operation = resolve_operation(
            provider=args.provider, resource_type=args.resource_type,
            list_providers=args.list_providers, list_regions=args.list_regions,
            explicit=args.operation,
        )
        guard_operation(operation)
        if args.limit is None or args.limit < 1:
            raise ApiError("--limit 必须是正整数：%s" % args.limit)
        items = list_items(
            operation, args.region,
            domain_id=args.domain_id, provider=args.provider,
            resource_type=args.resource_type, region_id=args.region_id,
            ep_id=args.ep_id, resource_id=args.resource_id, name=args.name,
            tags=args.tags, limit=args.limit, offset=args.offset,
            track=args.track, language=args.language, max_pages=args.max_pages,
        )
    except RmsListError as exc:
        print("[错误] %s" % exc, file=sys.stderr)
        return 1

    filters = active_filter_descriptions(
        domain_id=args.domain_id, provider=args.provider,
        resource_type=args.resource_type, region_id=args.region_id,
        ep_id=args.ep_id, resource_id=args.resource_id, name=args.name,
        tags=args.tags)
    filter_suffix = "（过滤条件: %s）" % ", ".join(filters) if filters else ""

    fmt = "markdown" if args.format == "md" else args.format

    if fmt == "table":
        if not items:
            print("当前区域（%s）无 %s 结果%s。" % (args.region, operation, filter_suffix))
        else:
            print("RMS %s（Region %s，共 %d 条）：" % (operation, args.region, len(items)))
        print(render_table(items, operation))
        return 0

    output_path = args.output or default_output_path(operation, args.region, fmt)
    try:
        written = export_report(items, output_path, operation, fmt,
                                summary=args.summary, region=args.region)
    except ExportError as exc:
        print("[错误] %s" % exc, file=sys.stderr)
        return 1

    if not items:
        print("当前区域（%s）无 %s 结果%s，已生成空文件（仅表头）：%s"
              % (args.region, operation, filter_suffix, written))
        return 0

    print("已导出 RMS %s（Region %s，共 %d 条，格式 %s）：%s"
          % (operation, args.region, len(items), fmt, written))
    return 0


if __name__ == "__main__":
    sys.exit(main())
