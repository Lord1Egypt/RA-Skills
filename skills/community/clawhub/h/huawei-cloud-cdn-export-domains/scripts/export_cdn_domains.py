#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Query Huawei Cloud CDN (Content Delivery Network) accelerated domains
(read-only) and export/download them into a local file.

Brings the CDN accelerated-domain list query (KooCLI
``hcloud CDN ListDomains`` — official read-only GET ``/v1.0/cdn/domains``)
together with a local file export. When the hcloud binary is absent, the script
falls back to the official ``huaweicloudsdkcdn`` v1 SDK
(``CdnClient.list_domains``).

Supported output modes (``--format``):

- ``csv`` (default): a CSV file with a ``域名`` (domain name) column, written to
  the local filesystem via a temporary file + atomic rename.
- ``markdown`` (``md``): a Markdown table file.
- ``json``: a JSON array file (raw response records).
- ``table``: an aligned full-field table on stdout (no file written).

A strict write-intent guard rejects any mutating CDN intent so writes never
happen: the only operation ever constructed is the read-only
``hcloud CDN ListDomains`` (or the SDK ``list_domains`` fallback). Nothing is
ever written back to the cloud — the export file is produced locally only.

Usage:
    python3 scripts/export_cdn_domains.py [--region cn-north-1]
                                          [--format csv|markdown|json|table]
                                          [--output /path/out.csv]
                                          [--summary]
                                          [--domain-name example.com]
                                          [--domain-status online]
                                          [--business-type web]
                                          [--service-area mainland_china]
                                          [--enterprise-project-id 0]
                                          [--exact-match true] [--show-tags true]
                                          [--page-size 100]

Environment overrides (mostly for tests):
    CDN_EXPORT_DOMAINS_HCLOUD_BIN   hcloud executable (default "hcloud")
    CDN_EXPORT_DOMAINS_HCLOUD_ARGS  extra args appended AFTER the read-only
                                    ``CDN ListDomains`` arguments
                                    (guard-scanned, read-only)
    CDN_EXPORT_DOMAINS_SQC_BIN      skill-quality-cli executable override
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

# CDN ListDomains is served globally; KooCLI advertises it for cn-north-1 /
# ap-southeast-1 (verified via `hcloud CDN ListDomains --help`).
DEFAULT_REGION = "cn-north-1"
DEFAULT_PAGE_SIZE = 100
DEFAULT_FORMAT = "csv"
SERVICE = "CDN"
ALLOWED_OPERATION = "ListDomains"
REST_PATH = "/v1.0/cdn/domains"

# Skill-quality telemetry: every hcloud call on the script execution path is
# reported through skill-quality-cli. When the CLI is unavailable — or
# SKILL_QUALITY_REPORT=0 — the call degrades to bare hcloud.
SKILL_QUALITY_SKILL_NAME = "huawei-cloud-cdn-export-domains"
_QUALITY_OFF_VALUES = ("0", "false", "no", "off")

# Markdown report column order (the first column is the required domain name).
MD_HEADERS = [
    "域名", "加速域名状态", "CNAME", "业务类型", "服务区域",
    "HTTPS状态", "企业项目 ID", "创建时间", "修改时间",
]
DEFAULT_FILENAME_PREFIX = "cdn_domains"
_FIELD_MISSING = "-"

# Mutating CDN operations / intents — strictly rejected by the guard.
WRITE_INTENT_KEYWORDS = (
    "createdomain",
    "deletedomain",
    "updatedomain",
    "enabledomain",
    "disabledomain",
    "modifydomain",
    "modifydomainconfig",
    "updatedomainfullconfig",
    "updatedomainmulticertificates",
    "updatedomainorigin",
    "createdomainbyfile",
    "createdomainbycopy",
    "batchcreatedomain",
    "batchdeletedomain",
    "createpreheatingtask",
    "createdomaintemplate",
    "createdomaintemplate",
    "deleteconsumerule",
    "createconsumerule",
    "createrefresh",
    "refreshtask",
    "preheating",
    "batchcopy",
    "create",
    "delete",
    "update",
    "modify",
    "enable",
    "disable",
    "refresh",
    "preheat",
    "destroy",
    "remove",
    "reset",
)

# Read-only option flags whose *values* are filter/output data (e.g. a report
# path such as "cdn-delete-report.csv", a domain name, a region label). Their
# values must NOT be scanned by the write-intent guard. The `--operation` value
# is intentionally NOT excluded: it is validated by `guard_operation()` and also
# scanned, as defense in depth.
_VALUE_STRIPPED_FLAGS = (
    "--region",
    "-r",
    "--format",
    "-f",
    "--output",
    "-o",
    "--domain-name",
    "--domain-status",
    "--business-type",
    "--service-area",
    "--enterprise-project-id",
    "--exact-match",
    "--show-tags",
    "--page-size",
)

# Preferred column order for the table / CSV views; remaining keys are appended.
PREFERRED_COLUMNS = [
    "domain_name",
    "domain_status",
    "cname",
    "business_type",
    "service_area",
    "https_status",
    "disabled",
    "locked",
    "origin_status",
    "enterprise_project_id",
    "id",
    "create_time",
    "modify_time",
    "tags",
]

_DOMAIN_LIST_KEYS = ("domains",)

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
    "apigw.0301",
    "cdn.0004",
    "认证失败",
    "权限不足",
    "permission denied",
    "not authorized",
)

# KooCLI prints usage errors (e.g. "[USE_ERROR]Invalid parameter: xxx") on
# stdout WITH exit code 0 — the marker is treated as a hard failure.
_USE_ERROR_MARKER = "[use_error]"


class CdnExportError(Exception):
    """Base error for the CDN accelerated-domain export skill."""


class GuardError(CdnExportError):
    """A write intent was detected and blocked (skill is read-only)."""


class ConfigError(CdnExportError):
    """hcloud/SDK missing or credentials (AK/SK) not configured."""


class AuthError(CdnExportError):
    """Authentication/authorization failure (invalid AK/SK or IAM 403)."""


class ApiError(CdnExportError):
    """hcloud / network / unexpected API failure."""


class ExportError(CdnExportError):
    """The export file could not be produced (bad path / write failure)."""


def guard_write_intent(text):
    """Raise GuardError if ``text`` carries a mutating intent.

    Normalizes separators so ``--create-domain``, ``CreateDomain``, and
    ``create_domain`` all hit the same keyword. Read-only vocabulary
    (list/show/get/describe) never matches.
    """
    low = re.sub(r"[\s_\-]+", "", str(text).lower())
    for keyword in WRITE_INTENT_KEYWORDS:
        if keyword in low:
            raise GuardError(
                "检测到写操作意图（关键词: %s）。本 skill 仅支持只读查询"
                "（CDN ListDomains）并仅在本机导出文件，"
                "创建/删除/更新/启用/停用/刷新/预热等变更操作已被守卫拦截。"
                % keyword
            )
    return False


def guard_operation(operation):
    """Only the read-only ListDomains operation may be executed."""
    if operation != ALLOWED_OPERATION:
        raise GuardError(
            "不允许的操作 %r：本 skill 仅允许只读操作 %s。"
            % (operation, ALLOWED_OPERATION)
        )
    return True


def guard_text_from_argv(argv):
    """Build the text the write-intent guard should scan.

    Scans flag names and positional tokens, but strips the values of the
    read-only filter flags and of the local-output/format flags: those are pure
    read / file-path data and may legitimately contain write-looking words (e.g.
    a report path ``cdn-delete-report.csv`` or a domain ``refresh.example.com``).

    A *flag* following such an option is never swallowed: a following token that
    starts with ``-`` is still scanned, so a mutating flag cannot hide behind a
    value-stripped option.
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


def build_command(region, domain_name=None, business_type=None,
                  domain_status=None, service_area=None,
                  enterprise_project_id=None, exact_match=None,
                  show_tags=None, limit=DEFAULT_PAGE_SIZE, page_number=1):
    """Build the hcloud CDN ListDomains argv (without the executable).

    Mirrors the real KooCLI parameter list for the read-only CDN ListDomains
    operation: --cli-region / --page_size / --page_number plus the real
    server-side filters --domain_name / --business_type / --domain_status /
    --service_area / --enterprise_project_id / --exact_match / --show_tags.
    CDN pages with ``page_size`` + ``page_number`` (the response carries
    ``total``).
    """
    argv = [
        SERVICE,
        ALLOWED_OPERATION,
        "--cli-region=%s" % region,
        "--page_size=%d" % limit,
        "--page_number=%d" % page_number,
    ]
    if domain_name:
        argv.append("--domain_name=%s" % domain_name)
    if business_type:
        argv.append("--business_type=%s" % business_type)
    if domain_status:
        argv.append("--domain_status=%s" % domain_status)
    if service_area:
        argv.append("--service_area=%s" % service_area)
    if enterprise_project_id:
        argv.append("--enterprise_project_id=%s" % enterprise_project_id)
    if exact_match is not None:
        argv.append("--exact_match=%s" % ("true" if exact_match else "false"))
    if show_tags is not None:
        argv.append("--show_tags=%s" % ("true" if show_tags else "false"))
    return argv


def _hcloud_executable():
    return os.environ.get("CDN_EXPORT_DOMAINS_HCLOUD_BIN") or "hcloud"


def _hcloud_resolvable():
    """True when the hcloud executable can actually be launched.

    Checked *before* wrapping the command with skill-quality-cli: the wrapper
    would otherwise swallow a missing-hcloud failure into its own non-zero exit
    (a Python traceback), which ``run_hcloud`` cannot tell apart from a genuine
    CLI error — and that would silently disable the SDK fallback. Probing here
    keeps the documented "hcloud absent → huaweicloudsdkcdn fallback" contract.
    """
    exe = _hcloud_executable()
    if os.path.dirname(exe):
        return os.path.isfile(exe) and os.access(exe, os.X_OK)
    return shutil.which(exe) is not None


def _quality_report_enabled():
    """Quality telemetry is on unless SKILL_QUALITY_REPORT is a falsy value."""
    value = os.environ.get("SKILL_QUALITY_REPORT")
    if value is None:
        return True
    return value.strip().lower() not in _QUALITY_OFF_VALUES


def _skill_quality_executable():
    """Locate skill-quality-cli: env override → PATH → ~/.local/bin, else None."""
    override = os.environ.get("CDN_EXPORT_DOMAINS_SQC_BIN")
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
    """Bare hcloud argv: executable override + read-only argv + trailing extra.

    Extra args (``CDN_EXPORT_DOMAINS_HCLOUD_ARGS``) are appended *after* the
    read-only argv so they can never rewrite the service/operation.
    """
    cmd = [_hcloud_executable()]
    cmd.extend(argv)
    extra = os.environ.get("CDN_EXPORT_DOMAINS_HCLOUD_ARGS", "").split()
    if extra:
        cmd.extend(extra)
    return cmd


def build_hcloud_command(argv):
    """Build the hcloud execution argv, wrapping it with skill-quality-cli.

    Every CLI call is reported as ``skill-quality-cli run --skill-name
    huawei-cloud-cdn-export-domains -- hcloud ...`` (the mandatory wrapping
    口径, enforced here on the script path rather than left to the agent). The
    command degrades to bare hcloud when the telemetry CLI is missing or
    ``SKILL_QUALITY_REPORT=0``; an explicit ``CDN_EXPORT_DOMAINS_HCLOUD_BIN``
    override (offline mock / verification) is always run verbatim.

    When hcloud itself is not resolvable the wrapping is skipped **and** the
    bare argv is returned, so ``run_hcloud`` raises ``FileNotFoundError`` →
    ``ConfigError`` → the SDK fallback, exactly as the SKILL.md promises. This
    probe must happen before the wrapper: skill-quality-cli would otherwise
    turn the missing binary into its own exit code 1 + traceback, which
    ``list_domains`` can only misread as a genuine CLI failure.
    """
    hcloud_cmd = _hcloud_argv(argv)
    if os.environ.get("CDN_EXPORT_DOMAINS_HCLOUD_BIN"):
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
    """Execute hcloud through skill-quality-cli when available.

    Extra args from ``CDN_EXPORT_DOMAINS_HCLOUD_ARGS`` are appended *after* the
    read-only ``CDN ListDomains`` argv (they can never rewrite the
    service/operation) and are guard-scanned for write intent first.
    """
    extra = os.environ.get("CDN_EXPORT_DOMAINS_HCLOUD_ARGS", "").split()
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
            "hcloud 参数错误（KooCLI 拒绝了该参数组合，退出码 %s）：CDN ListDomains "
            "真实参数清单可通过 `hcloud CDN ListDomains --help` 查看。"
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
            "无权限访问内容分发网络（CDN），请检查 IAM 权限"
            "（403：AK/SK 无效或未授予 CDN 域名只读权限），"
            "参见 references/iam-policies.md。详情：%s" % blob[:300]
        )
    return ApiError(
        "hcloud 调用失败（退出码 %s）：%s" % (returncode, blob[:300])
    )


def extract_domains(payload):
    """Pull the accelerated-domain list out of a ListDomains response."""
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        for key in _DOMAIN_LIST_KEYS:
            value = payload.get(key)
            if isinstance(value, list):
                return value
    return []


def _payload_error(payload):
    """Return the error text if a ListDomains payload is an error envelope.

    KooCLI returns HTTP-level API errors (e.g. ``CDN.0004`` insufficient
    permission) as a ``{"error": {"error_code": ..., "error_msg": ...}}`` body on
    **stdout with exit code 0**. Such an envelope must be surfaced as an explicit
    error, never silently treated as an empty domain list.
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
    for ckey in ("error_code", "errorCode", "errorMsg", "error_message"):
        if payload.get(ckey):
            return str(payload[ckey])
    for mkey in ("error_msg", "message"):
        if payload.get(mkey):
            return str(payload[mkey])
    return None


def _total(payload):
    """Read the ``total`` domain count from a ListDomains response (None if absent)."""
    if not isinstance(payload, dict):
        return None
    total = payload.get("total")
    try:
        return int(total)
    except (TypeError, ValueError):
        return None


def _env_value(names):
    """Read the first non-empty value from an explicit whitelist of env names."""
    for name in names:
        value = os.environ.get(name)
        if value:
            return value
    return None


def _jsonable(value):
    """Recursively convert datetimes (SDK to_dict output) to JSON-safe values."""
    return json.loads(json.dumps(value, ensure_ascii=False, default=str))


def list_domains_via_sdk(region, domain_name=None, business_type=None,
                         domain_status=None, service_area=None,
                         enterprise_project_id=None, limit=DEFAULT_PAGE_SIZE,
                         max_pages=100):
    """SDK fallback: query CDN accelerated domains through ``huaweicloudsdkcdn`` v1.

    Only invoked when hcloud is not installed. Credentials are taken from the
    explicitly named AK/SK environment variables (never passed as literals).
    CDN is a global service, so the SDK client is authenticated with
    ``GlobalCredentials``; region resolution uses the SDK's own ``CdnRegion``
    catalog, falling back to an explicit ``Region(id, endpoint)`` for custom
    regions. ``ListDomainsRequest`` accepts ``domain_name`` / ``business_type`` /
    ``domain_status`` / ``service_area`` / ``enterprise_project_id`` plus
    ``page_size`` + ``page_number`` paging.
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
        from huaweicloudsdkcdn.v1 import CdnClient, ListDomainsRequest
        from huaweicloudsdkcdn.v1.region.cdn_region import CdnRegion
    except ImportError as exc:
        raise ConfigError(
            "未找到 hcloud（KooCLI），且 huaweicloudsdkcore/huaweicloudsdkcdn 未安装，"
            "无法回退到 SDK。请安装 KooCLI 或先运行 "
            "`python3 scripts/ensure_env.py`（pip install huaweicloudsdkcore "
            "huaweicloudsdkcdn）。详情：%s" % exc
        )
    credentials = GlobalCredentials(ak=ak, sk=sk)  # env-sourced, never literals
    try:
        try:
            region_obj = CdnRegion.value_of(region)
        except (ValueError, KeyError, AttributeError):
            region_obj = Region(region, "https://cdn.myhuaweicloud.com")
        client = CdnClient.new_builder() \
            .with_credentials(credentials) \
            .with_region(region_obj) \
            .with_http_config(HttpConfig.get_default_config()) \
            .build()
    except Exception as exc:  # region unknown / config broken
        raise ConfigError(
            "SDK 初始化失败（region=%s）：%s。请检查 huaweicloudsdkcdn 安装与区域配置。"
            % (region, exc)
        )
    domains = []
    page_number = 1
    total = None
    for _ in range(max_pages):
        request = ListDomainsRequest(
            domain_name=domain_name,
            business_type=business_type,
            domain_status=domain_status,
            service_area=service_area,
            enterprise_project_id=enterprise_project_id,
            page_size=limit,
            page_number=page_number,
        )
        try:
            response = client.list_domains(request)
        except Exception as exc:
            low = str(exc).lower()
            if any(p in low for p in _AUTH_PATTERNS):
                raise AuthError(
                    "无权限访问内容分发网络（CDN），请检查 IAM 权限（403）。详情：%s"
                    % str(exc)[:300]
                )
            raise ApiError("SDK 调用失败：%s" % str(exc)[:300])
        batch = list(response.domains or [])
        records = [_jsonable(domain.to_dict()) for domain in batch]
        domains.extend(records)
        total = getattr(response, "total", None)
        if not batch or len(batch) < limit:
            break
        if total is not None:
            try:
                if len(domains) >= int(total):
                    break
            except (TypeError, ValueError):
                pass
        page_number += 1
    else:
        raise ApiError("翻页超过 %d 页仍未取完，已中止以防死循环。" % max_pages)
    return domains


def list_domains(region, domain_name=None, business_type=None,
                 domain_status=None, service_area=None,
                 enterprise_project_id=None, exact_match=None,
                 show_tags=None, limit=DEFAULT_PAGE_SIZE, max_pages=100):
    """Query all CDN accelerated domains (page-paged); KooCLI first, SDK fallback."""
    domains = []
    page_number = 1
    total = None
    for _page in range(max_pages):
        argv = build_command(region, domain_name=domain_name,
                             business_type=business_type,
                             domain_status=domain_status,
                             service_area=service_area,
                             enterprise_project_id=enterprise_project_id,
                             exact_match=exact_match, show_tags=show_tags,
                             limit=limit, page_number=page_number)
        try:
            stdout, stderr, returncode = run_hcloud(argv)
        except ConfigError:
            # hcloud binary missing → one-shot SDK fallback (no CLI retry).
            domains = list_domains_via_sdk(
                region, domain_name=domain_name, business_type=business_type,
                domain_status=domain_status, service_area=service_area,
                enterprise_project_id=enterprise_project_id,
                limit=limit, max_pages=max_pages,
            )
            break
        if returncode != 0 or _USE_ERROR_MARKER in (stdout + " " + stderr).lower():
            raise classify_hcloud_failure(stdout, stderr, returncode)
        payload = extract_json(stdout)
        err_text = _payload_error(payload)
        if err_text:
            # HTTP-level API errors arrive on stdout with rc=0 — surface them.
            raise classify_hcloud_failure("", err_text, returncode)
        batch = extract_domains(payload)
        domains.extend(batch)
        total = _total(payload)
        if not batch or len(batch) < limit:
            break
        if total is not None and len(domains) >= total:
            break
        page_number += 1
    else:
        raise ApiError("翻页超过 %d 页仍未取完，已中止以防死循环。" % max_pages)
    return domains


def normalize_domain(domain):
    """Flatten tag lists into a table-friendly string; keep other fields as-is."""
    flat = dict(domain)
    tags = domain.get("tags")
    if isinstance(tags, list):
        pairs = []
        for tag in tags:
            if isinstance(tag, dict):
                key = tag.get("key", "")
                value = tag.get("value", "")
                pairs.append("%s=%s" % (key, value))
            else:
                pairs.append(str(tag))
        flat["tags"] = ",".join(pairs) if pairs else "-"
    elif tags is None:
        flat["tags"] = "-"
    return flat


def _field(domain, *names, default="-"):
    for name in names:
        if name in domain and domain[name] not in (None, ""):
            return domain[name]
    return default


def domain_names(domains):
    names = []
    for domain in domains:
        name = _field(domain, "domain_name", default=None)
        if name is None:
            name = _field(domain, "id")
        names.append(str(name))
    return names


def _cell(value):
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return str(value)


def _md_escape(value):
    """Escape pipe/newline characters so a cell cannot break the Markdown table."""
    return _cell(value).replace("|", "\\|").replace("\n", " ").replace("\r", " ")


def _columns(rows_data):
    """Union of fields: preferred columns first, remaining sorted."""
    columns = []
    for key in PREFERRED_COLUMNS:
        if any(key in c for c in rows_data):
            columns.append(key)
    for key in sorted({k for c in rows_data for k in c}):
        if key not in columns:
            columns.append(key)
    return columns


def render_table(domains):
    """Render full-field table output (union of all returned fields)."""
    rows_data = [normalize_domain(domain) for domain in domains]
    columns = _columns(rows_data) or ["domain_name", "domain_status"]
    rows = [[_cell(_field(c, col)) for col in columns] for c in rows_data]
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


def normalized_md_row(domain, region=None):
    """Map a domain record to the fixed Markdown column order."""
    return [
        _md_escape(_field(domain, "domain_name")),
        _md_escape(_field(domain, "domain_status")),
        _md_escape(_field(domain, "cname")),
        _md_escape(_field(domain, "business_type")),
        _md_escape(_field(domain, "service_area")),
        _md_escape(_field(domain, "https_status")),
        _md_escape(_field(domain, "enterprise_project_id")),
        _md_escape(_field(domain, "create_time")),
        _md_escape(_field(domain, "modify_time")),
    ]


def render_markdown(domains, summary=False, region=None):
    """Render the domain list as a GitHub-flavored Markdown table.

    An empty list still renders a valid (header-only) table, so "no domain" never
    produces a corrupt file — it produces an explicit empty table.
    """
    lines = [
        "| " + " | ".join(MD_HEADERS) + " |",
        "| " + " | ".join(["---"] * len(MD_HEADERS)) + " |",
    ]
    for domain in domains:
        lines.append("| " + " | ".join(normalized_md_row(domain, region=region)) + " |")
    if summary:
        lines.append("")
        lines.append("**汇总**：共 %d 个 CDN 加速域名（Region %s）。"
                     % (len(domains), region or _FIELD_MISSING))
    return "\n".join(lines)


def render_csv(domains):
    """Render the domain list as CSV (union of returned fields).

    An empty list still renders a valid header row (``域名`` up front).
    """
    rows_data = [normalize_domain(domain) for domain in domains]
    columns = _columns(rows_data) or ["domain_name", "domain_status"]
    buffer = io.StringIO()
    writer = csv.writer(buffer, lineterminator="\n")
    writer.writerow(columns)
    for record in rows_data:
        writer.writerow([_cell(_field(record, col)) for col in columns])
    return buffer.getvalue().rstrip("\n")


def render_json(domains):
    """Render the domain list as a JSON array (raw records, stable field order)."""
    return json.dumps(domains, ensure_ascii=False, indent=2)


def _render(domains, fmt, summary=False, region=None):
    if fmt == "json":
        return render_json(domains)
    if fmt == "markdown":
        return render_markdown(domains, summary=summary, region=region)
    return render_csv(domains)


def _extension(fmt):
    return "md" if fmt == "markdown" else fmt


def default_output_path(region, fmt):
    """Default export filename: cdn_domains_<region>_<timestamp>.<ext>"""
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return "%s_%s_%s.%s" % (DEFAULT_FILENAME_PREFIX, region, stamp,
                            _extension(fmt))


def export_report(domains, output_path, fmt, summary=False, region=None):
    """Write the domain list into a report at ``output_path``.

    Args:
        domains:     iterable of domain dicts.
        output_path: absolute or relative path of the file to write.
        fmt:         ``csv`` / ``markdown`` / ``json``.
        summary:     when True, append a trailing summary line (Markdown only).
        region:      optional region label used per row and in the summary line.

    Returns:
        The absolute path of the written file.

    Raises:
        ExportError: path unusable or write failed. No partial/corrupt file is
                     left behind.
    """
    domains = list(domains)
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

    text = _render(domains, fmt, summary=summary, region=region)

    # Save via a temp file + atomic rename: interrupts never leave a corrupt
    # file at the destination.
    fd, tmp_path = tempfile.mkstemp(
        prefix=".%s." % DEFAULT_FILENAME_PREFIX, suffix=".tmp",
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


def active_filter_descriptions(domain_name=None, domain_status=None,
                               business_type=None, service_area=None,
                               enterprise_project_id=None):
    """Human-readable description of the server-side filters actually applied."""
    filters = []
    if domain_name:
        filters.append("domain_name=%s" % domain_name)
    if domain_status:
        filters.append("domain_status=%s" % domain_status)
    if business_type:
        filters.append("business_type=%s" % business_type)
    if service_area:
        filters.append("service_area=%s" % service_area)
    if enterprise_project_id:
        filters.append("enterprise_project_id=%s" % enterprise_project_id)
    return filters


def _str_to_bool(value):
    if value is None:
        return None
    return str(value).strip().lower() in ("1", "true", "yes", "on")


def parse_args(argv):
    parser = argparse.ArgumentParser(
        description="查询华为云 CDN 加速域名列表并导出为本地文件（只读）。")
    parser.add_argument("-r", "--region", default=DEFAULT_REGION,
                        help="目标 Region（默认 %s；CDN ListDomains 经 KooCLI 支持 "
                             "cn-north-1 / ap-southeast-1）" % DEFAULT_REGION)
    parser.add_argument("-f", "--format", default=DEFAULT_FORMAT,
                        choices=["csv", "markdown", "md", "json", "table"],
                        help="输出格式：csv（默认）/ markdown（md）/ json / table")
    parser.add_argument("-o", "--output", default=None,
                        help="导出文件路径（csv/markdown/json；默认 "
                             "cdn_domains_<region>_<timestamp>.<ext>）")
    parser.add_argument("--summary", action="store_true",
                        help="Markdown 报表末尾追加汇总行（域名数量）")
    parser.add_argument("--domain-name", dest="domain_name",
                        help="按加速域名过滤（服务端查询参数，模糊匹配）")
    parser.add_argument("--domain-status", dest="domain_status",
                        help="按加速域名状态过滤（如 online/offline/configuring，服务端查询参数）")
    parser.add_argument("--business-type", dest="business_type",
                        help="按业务类型过滤（如 web/download/video/wholeSite，服务端查询参数）")
    parser.add_argument("--service-area", dest="service_area",
                        help="按服务区域过滤（如 mainland_china/outside_mainland_china/global，服务端查询参数）")
    parser.add_argument("--enterprise-project-id", dest="enterprise_project_id",
                        help="按企业项目 ID 过滤（服务端查询参数，all 表示全部）")
    parser.add_argument("--exact-match", dest="exact_match", default=None,
                        help="域名精确匹配（true/false，服务端查询参数）")
    parser.add_argument("--show-tags", dest="show_tags", default=None,
                        help="是否返回标签（true/false，服务端查询参数）")
    parser.add_argument("--page-size", type=int, default=DEFAULT_PAGE_SIZE,
                        dest="page_size",
                        help="分页大小（默认 %d，范围 1~10000，自动翻页取全量）" % DEFAULT_PAGE_SIZE)
    parser.add_argument("--operation", default=ALLOWED_OPERATION,
                        help="hcloud CDN 操作名（仅允许只读 %s）" % ALLOWED_OPERATION)
    return parser.parse_args(argv)


def main(argv=None):
    raw_argv = argv if argv is not None else sys.argv[1:]

    # Write-intent guard runs on the RAW argv BEFORE argparse, so that a
    # mutating flag (e.g. `--create-domain`) is reported as a guard violation
    # instead of an argparse "unrecognized argument" error.
    try:
        guard_write_intent(guard_text_from_argv(raw_argv))
    except CdnExportError as exc:
        print("[错误] %s" % exc, file=sys.stderr)
        return 1

    args = parse_args(argv)

    try:
        guard_operation(args.operation)
        if args.page_size is None or args.page_size < 1 or args.page_size > 10000:
            raise ApiError("--page-size 超出范围（1~10000）：%s" % args.page_size)
        domains = list_domains(
            args.region,
            domain_name=args.domain_name,
            business_type=args.business_type,
            domain_status=args.domain_status,
            service_area=args.service_area,
            enterprise_project_id=args.enterprise_project_id,
            exact_match=_str_to_bool(args.exact_match),
            show_tags=_str_to_bool(args.show_tags),
            limit=args.page_size,
        )
    except CdnExportError as exc:
        print("[错误] %s" % exc, file=sys.stderr)
        return 1

    filters = active_filter_descriptions(
        domain_name=args.domain_name, domain_status=args.domain_status,
        business_type=args.business_type, service_area=args.service_area,
        enterprise_project_id=args.enterprise_project_id)
    filter_suffix = "（过滤条件: %s）" % ", ".join(filters) if filters else ""

    fmt = "markdown" if args.format == "md" else args.format

    if fmt == "table":
        if not domains:
            print("当前区域（%s）无 CDN 加速域名%s。" % (args.region, filter_suffix))
        else:
            print("Region %s 的 CDN 加速域名列表（共 %d 个，完整字段）："
                  % (args.region, len(domains)))
        print(render_table(domains))
        return 0

    # File export (csv / markdown / json): an empty list still yields a valid
    # header-only artifact — never a corrupt file.
    output_path = args.output or default_output_path(args.region, fmt)
    try:
        written = export_report(domains, output_path, fmt,
                                summary=args.summary, region=args.region)
    except ExportError as exc:
        print("[错误] %s" % exc, file=sys.stderr)
        return 1

    if not domains:
        print("当前区域（%s）无 CDN 加速域名%s，已生成空文件（仅表头）：%s"
              % (args.region, filter_suffix, written))
        return 0

    print("已导出 CDN 加速域名列表（Region %s，共 %d 个，格式 %s，含 域名 列）：%s"
          % (args.region, len(domains), fmt, written))
    return 0


if __name__ == "__main__":
    sys.exit(main())