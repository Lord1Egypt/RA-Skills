#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""List Huawei Cloud Virtual Private Cloud (VPC) instances (read-only) and export
a local Markdown report.

Brings the VPC list query (KooCLI ``hcloud VPC ListVpcs`` — official read-only
GET ``/v1/{project_id}/vpcs``) together with a local Markdown export. When the
hcloud binary is absent, the script falls back to the official
``huaweicloudsdkvpc`` v2 SDK (``VpcClient.list_vpcs``).

Three output modes are supported:

- ``--format md`` (default): write the VPC list into a ``.md`` report (headers
  VPC 名称 / VPC ID / 区域 / 网段 / 状态 / 企业项目 ID / 描述 / 创建时间,
  optional summary line), written to the local filesystem via a temporary file
  + atomic rename.
- ``--format table``: aligned full-field table on stdout.
- ``--format json``: structured JSON array for downstream tooling.

A strict write-intent guard rejects any mutating VPC intent so writes never
happen: the only operation ever constructed is read-only
``hcloud VPC ListVpcs`` (or the SDK ``list_vpcs`` fallback). No data is ever
written back to the cloud — the Markdown file is produced locally only.

Usage:
    python3 scripts/export_vpc_markdown.py [--region cn-north-4]
                                          [--format md|table|json]
                                          [--output /path/out.md]
                                          [--summary] [--id vpc-0001]
                                          [--enterprise-project-id 0]
                                          [--page-size 100]

Environment overrides (mostly for tests):
    VPC_EXPORT_MARKDOWN_HCLOUD_BIN   hcloud executable (default "hcloud")
    VPC_EXPORT_MARKDOWN_HCLOUD_ARGS  extra args appended AFTER the read-only
                                     ``VPC ListVpcs`` arguments
                                     (guard-scanned, read-only)
    VPC_EXPORT_MARKDOWN_SQC_BIN      skill-quality-cli executable override
"""

import argparse
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
DEFAULT_FORMAT = "md"
SERVICE = "VPC"
ALLOWED_OPERATION = "ListVpcs"
REST_PATH = "/v1/{project_id}/vpcs"

# Skill-quality telemetry: every hcloud call on the script execution path is
# reported through skill-quality-cli. When the CLI is unavailable — or
# SKILL_QUALITY_REPORT=0 — the call degrades to bare hcloud.
SKILL_QUALITY_SKILL_NAME = "huawei-cloud-vpc-export-markdown"
_QUALITY_OFF_VALUES = ("0", "false", "no", "off")

# Markdown report column order (the first column is the required VPC name).
MD_HEADERS = [
    "VPC 名称", "VPC ID", "区域", "网段", "状态",
    "企业项目 ID", "描述", "创建时间",
]
DEFAULT_FILENAME_PREFIX = "vpc_list"
_FIELD_MISSING = "-"

# Mutating VPC operations / intents — strictly rejected by the guard.
WRITE_INTENT_KEYWORDS = (
    "createvpc",
    "batchcreatevpcs",
    "deletevpc",
    "batchdeletevpcs",
    "updatevpc",
    "createsubnet",
    "batchcreatesubnets",
    "deletesubnet",
    "batchdeletesubnets",
    "updatesubnet",
    "createsecuritygroup",
    "deletesecuritygroup",
    "updatesecuritygroup",
    "createsecuritygrouprule",
    "deletesecuritygrouprule",
    "createport",
    "deleteport",
    "updateport",
    "createroutetable",
    "deleteroutetable",
    "createroute",
    "deleteroute",
    "createflowlog",
    "deleteflowlog",
    "updateflowlog",
    "createvpcpeering",
    "deletevpcpeering",
    "acceptvpcpeering",
    "rejectvpcpeering",
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
    "creating",
    "deleting",
    "updating",
    "associating",
    "disassociating",
)

# Read-only option flags whose *values* are filter/output data (e.g. a report
# path such as "vpc-delete-report.md", a region label, or a VPC id). Their
# values must NOT be scanned by the write-intent guard. The `--operation` value
# is intentionally NOT excluded: it is validated by `guard_operation()` and also
# scanned, as defense in depth.
_VALUE_STRIPPED_FLAGS = (
    "--region",
    "-r",
    "--id",
    "--enterprise-project-id",
    "--page-size",
    "--output",
    "-o",
    "--format",
    "-f",
    "--project-id",
)

# Preferred column order for the table view; remaining keys are appended sorted.
PREFERRED_COLUMNS = [
    "name",
    "id",
    "cidr",
    "status",
    "description",
    "enterprise_project_id",
    "tenant_id",
    "routes",
    "created_at",
    "updated_at",
]

_VPC_LIST_KEYS = ("vpcs", "vpc")

# AK/SK environment variable names, read *directly* (never by enumerating
# os.environ). The official SDK's BasicCredentials does not auto-discover
# credentials, so the fallback path resolves them explicitly.
_AK_ENV_NAMES = (
    "HUAWEI_ACCESS_KEY",
    "HW_ACCESS_KEY",
    "HWC_ACCESS_KEY",
    "HUAWEICLOUD_SDK_AK",
    "HUAWEI_CLOUD_ACCESS_KEY",
)
_SK_ENV_NAMES = (
    "HUAWEI_SECRET_KEY",
    "HW_SECRET_KEY",
    "HWC_SECRET_KEY",
    "HUAWEICLOUD_SDK_SK",
    "HUAWEI_CLOUD_SECRET_KEY",
)
_PROJECT_ID_ENV_NAMES = (
    "HW_PROJECT_ID",
    "HUAWEI_PROJECT_ID",
    "HUAWEICLOUD_SDK_PROJECT_ID",
    "HUAWEI_CLOUD_PROJECT_ID",
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
# stdout WITH exit code 0 — the marker is treated as a hard failure.
_USE_ERROR_MARKER = "[use_error]"


class VpcExportError(Exception):
    """Base error for the VPC list Markdown export skill."""


class GuardError(VpcExportError):
    """A write intent was detected and blocked (skill is read-only)."""


class ConfigError(VpcExportError):
    """hcloud/SDK missing or credentials (AK/SK) not configured."""


class AuthError(VpcExportError):
    """Authentication/authorization failure (invalid AK/SK or IAM 403)."""


class ApiError(VpcExportError):
    """hcloud / network / unexpected API failure."""


class ExportError(VpcExportError):
    """The Markdown file could not be produced (bad path / write failure)."""


def guard_write_intent(text):
    """Raise GuardError if ``text`` carries a mutating intent.

    Normalizes separators so ``--create-vpc``, ``CreateVpc``, and
    ``create_vpc`` all hit the same keyword. Read-only vocabulary
    (list/show/get/describe) never matches.
    """
    low = re.sub(r"[\s_\-]+", "", str(text).lower())
    for keyword in WRITE_INTENT_KEYWORDS:
        if keyword in low:
            raise GuardError(
                "检测到写操作意图（关键词: %s）。本 skill 仅支持只读查询"
                "（VPC ListVpcs）并仅在本机生成 Markdown 报表，"
                "创建/删除/更新/绑定/解绑等变更操作已被守卫拦截。"
                % keyword
            )
    return False


def guard_operation(operation):
    """Only the read-only ListVpcs operation may be executed."""
    if operation != ALLOWED_OPERATION:
        raise GuardError(
            "不允许的操作 %r：本 skill 仅允许只读操作 %s。"
            % (operation, ALLOWED_OPERATION)
        )
    return True


def guard_text_from_argv(argv):
    """Build the text the write-intent guard should scan.

    Scans flag names and positional tokens, but strips the values of the
    read-only filter flags (``--region`` / ``--id`` / ``--enterprise-project-id``
    / ``--page-size`` / ``--project-id``) and of the local-output/format flags
    (``--output`` / ``-o`` / ``--format`` / ``-f``): those are pure read /
    file-path data and may legitimately contain write-looking words (e.g. a
    report path ``vpc-delete-report.md``).

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


def build_command(region, vpc_id=None, enterprise_project_id=None,
                  limit=DEFAULT_PAGE_SIZE, marker=None):
    """Build the hcloud VPC ListVpcs argv (without the executable).

    Mirrors the real KooCLI parameter list for the read-only VPC ListVpcs
    operation: --cli-region / --limit / --marker and the real server-side
    filters --id / --enterprise_project_id. VPC pages with ``limit`` + ``marker``
    (the next_marker comes from the response page_info).
    """
    argv = [
        SERVICE,
        ALLOWED_OPERATION,
        "--cli-region=%s" % region,
        "--limit=%d" % limit,
    ]
    if marker:
        argv.append("--marker=%s" % marker)
    if vpc_id:
        argv.append("--id=%s" % vpc_id)
    if enterprise_project_id:
        argv.append("--enterprise_project_id=%s" % enterprise_project_id)
    return argv


def _hcloud_executable():
    return os.environ.get("VPC_EXPORT_MARKDOWN_HCLOUD_BIN") or "hcloud"


def _quality_report_enabled():
    """Quality telemetry is on unless SKILL_QUALITY_REPORT is a falsy value."""
    value = os.environ.get("SKILL_QUALITY_REPORT")
    if value is None:
        return True
    return value.strip().lower() not in _QUALITY_OFF_VALUES


def _skill_quality_executable():
    """Locate skill-quality-cli: env override → PATH → ~/.local/bin, else None."""
    override = os.environ.get("VPC_EXPORT_MARKDOWN_SQC_BIN")
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

    Extra args (``VPC_EXPORT_MARKDOWN_HCLOUD_ARGS``) are appended *after* the
    read-only argv so they can never rewrite the service/operation.
    """
    cmd = [_hcloud_executable()]
    cmd.extend(argv)
    extra = os.environ.get("VPC_EXPORT_MARKDOWN_HCLOUD_ARGS", "").split()
    if extra:
        cmd.extend(extra)
    return cmd


def build_hcloud_command(argv):
    """Build the hcloud execution argv, wrapping it with skill-quality-cli.

    Every CLI call is reported as ``skill-quality-cli run --skill-name
    huawei-cloud-vpc-export-markdown -- hcloud ...`` (the mandatory wrapping
    口径, enforced here on the script path rather than left to the agent). The
    command degrades to bare hcloud when the telemetry CLI is missing or
    ``SKILL_QUALITY_REPORT=0``; an explicit ``VPC_EXPORT_MARKDOWN_HCLOUD_BIN``
    override (offline mock / verification) is always run verbatim.
    """
    hcloud_cmd = _hcloud_argv(argv)
    if os.environ.get("VPC_EXPORT_MARKDOWN_HCLOUD_BIN"):
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

    Extra args from ``VPC_EXPORT_MARKDOWN_HCLOUD_ARGS`` are appended *after* the
    read-only ``VPC ListVpcs`` argv (they can never rewrite the service/operation)
    and are guard-scanned for write intent first.
    """
    extra = os.environ.get("VPC_EXPORT_MARKDOWN_HCLOUD_ARGS", "").split()
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
            "hcloud 参数错误（KooCLI 拒绝了该参数组合，退出码 %s）：VPC ListVpcs "
            "真实参数清单可通过 `hcloud VPC ListVpcs --help` 查看。"
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
            "无权限访问虚拟私有云（VPC），请检查 IAM 权限"
            "（403：AK/SK 无效或未授予 VPC 只读权限），"
            "参见 references/iam-policies.md。详情：%s" % blob[:300]
        )
    return ApiError(
        "hcloud 调用失败（退出码 %s）：%s" % (returncode, blob[:300])
    )


def extract_vpcs(payload):
    """Pull the VPC list out of a ListVpcs response."""
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        for key in _VPC_LIST_KEYS:
            value = payload.get(key)
            if isinstance(value, list):
                return value
    return []


def _next_marker(payload):
    """Read the next_marker from a ListVpcs response page_info."""
    if not isinstance(payload, dict):
        return None
    page_info = payload.get("page_info") or payload.get("pageInfo")
    if isinstance(page_info, dict):
        marker = page_info.get("next_marker") or page_info.get("nextMarker")
        if marker:
            return str(marker)
    return None


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


def list_vpcs_via_sdk(region, vpc_id=None, enterprise_project_id=None,
                      limit=DEFAULT_PAGE_SIZE, project_id=None, max_pages=100):
    """SDK fallback: query VPCs through ``huaweicloudsdkvpc`` v2.

    Only invoked when hcloud is not installed. Credentials are taken from the
    explicitly named AK/SK environment variables (never passed as literals).
    Region resolution uses the SDK's own ``VpcRegion`` catalog, falling back to
    an explicit ``Region(id, endpoint)`` for custom regions. `ListVpcsRequest`
    accepts ``id`` / ``enterprise_project_id`` as string values; paging uses
    ``limit`` + ``marker``.
    """
    ak = _env_value(_AK_ENV_NAMES)
    sk = _env_value(_SK_ENV_NAMES)
    if not ak or not sk:
        raise ConfigError(
            "SDK 回退缺少 AK/SK 凭证：官方 SDK 的 BasicCredentials 不会自动读取环境"
            "变量，且当前环境未检测到 HUAWEI_ACCESS_KEY / HUAWEI_SECRET_KEY 形式的"
            " AK/SK 环境变量。请在会话外设置（严禁在对话中粘贴 AK/SK）；若同时未安装"
            " SDK，请先运行 `python3 scripts/ensure_env.py`。参见 "
            "references/cli-installation-guide.md。"
        )
    resolved_project_id = resolve_project_id(project_id)
    if not resolved_project_id:
        raise ConfigError(
            "SDK 回退缺少 project_id：VPC 的 REST 路径为 %s，需要项目 ID。"
            "请通过 --project-id 传入，或设置 HUAWEICLOUD_SDK_PROJECT_ID / "
            "HUAWEI_PROJECT_ID（严禁在对话中粘贴敏感信息）。" % REST_PATH
        )
    try:
        from huaweicloudsdkcore.auth.credentials import BasicCredentials
        from huaweicloudsdkcore.region.region import Region
        from huaweicloudsdkcore.http.http_config import HttpConfig
        from huaweicloudsdkvpc.v2 import VpcClient, ListVpcsRequest
        from huaweicloudsdkvpc.v2.region.vpc_region import VpcRegion
    except ImportError as exc:
        raise ConfigError(
            "未找到 hcloud（KooCLI），且 huaweicloudsdkcore/huaweicloudsdkvpc 未安装，"
            "无法回退到 SDK。请安装 KooCLI 或先运行 "
            "`python3 scripts/ensure_env.py`（pip install huaweicloudsdkcore "
            "huaweicloudsdkvpc）。详情：%s" % exc
        )
    credentials = BasicCredentials(ak=ak, sk=sk, project_id=resolved_project_id)  # env-sourced, never literals
    try:
        try:
            region_obj = VpcRegion.value_of(region)
        except (ValueError, KeyError, AttributeError):
            region_obj = Region(region, "https://vpc.%s.myhuaweicloud.com" % region)
        client = VpcClient.new_builder() \
            .with_credentials(credentials) \
            .with_region(region_obj) \
            .with_http_config(HttpConfig.get_default_config()) \
            .build()
    except Exception as exc:  # region unknown / config broken
        raise ConfigError(
            "SDK 初始化失败（region=%s）：%s。请检查 huaweicloudsdkvpc 安装与区域配置。"
            % (region, exc)
        )
    vpcs = []
    marker = None
    for _ in range(max_pages):
        request = ListVpcsRequest(
            limit=limit,
            marker=marker,
            id=vpc_id,
            enterprise_project_id=enterprise_project_id,
        )
        try:
            response = client.list_vpcs(request)
        except Exception as exc:
            low = str(exc).lower()
            if any(p in low for p in _AUTH_PATTERNS):
                raise AuthError(
                    "无权限访问虚拟私有云（VPC），请检查 IAM 权限（403）。详情：%s"
                    % str(exc)[:300]
                )
            raise ApiError("SDK 调用失败：%s" % str(exc)[:300])
        batch = list(response.vpcs or [])
        records = [_jsonable(vpc.to_dict()) for vpc in batch]
        vpcs.extend(records)
        page_info = getattr(response, "page_info", None)
        next_marker = getattr(page_info, "next_marker", None) if page_info else None
        if not next_marker and records and len(records) >= limit:
            # The typed ListVpcsResponse does not surface page_info; the VPC
            # marker is the resource id, so continue from the last returned id
            # when the page is full.
            next_marker = records[-1].get("id")
        if not next_marker or not batch:
            break
        marker = str(next_marker)
    else:
        raise ApiError("翻页超过 %d 页仍未取完，已中止以防死循环。" % max_pages)
    return vpcs


def list_vpcs(region, vpc_id=None, enterprise_project_id=None,
              limit=DEFAULT_PAGE_SIZE, project_id=None, max_pages=100):
    """Query all VPCs (marker-paged); KooCLI first, SDK fallback."""
    vpcs = []
    marker = None
    for _page in range(max_pages):
        argv = build_command(region, vpc_id=vpc_id,
                             enterprise_project_id=enterprise_project_id,
                             limit=limit, marker=marker)
        try:
            stdout, stderr, returncode = run_hcloud(argv)
        except ConfigError:
            # hcloud binary missing → one-shot SDK fallback (no CLI retry).
            vpcs = list_vpcs_via_sdk(
                region, vpc_id=vpc_id,
                enterprise_project_id=enterprise_project_id,
                limit=limit, project_id=project_id, max_pages=max_pages,
            )
            break
        if returncode != 0 or _USE_ERROR_MARKER in (stdout + " " + stderr).lower():
            raise classify_hcloud_failure(stdout, stderr, returncode)
        payload = extract_json(stdout)
        batch = extract_vpcs(payload)
        vpcs.extend(batch)
        marker = _next_marker(payload)
        if not marker or not batch or len(batch) < limit:
            break
    else:
        raise ApiError("翻页超过 %d 页仍未取完，已中止以防死循环。" % max_pages)
    return vpcs


def normalize_vpc(vpc):
    """Flatten a VPC record for the table view.

    The nested ``routes`` array is compacted into a single JSON cell so the
    table stays readable; all other scalar fields are preserved.
    """
    flat = dict(vpc)
    routes = flat.get("routes")
    if isinstance(routes, list):
        flat["routes"] = json.dumps(routes, ensure_ascii=False,
                                    separators=(",", ":"))
    return flat


def _field(vpc, *names, default="-"):
    for name in names:
        if name in vpc and vpc[name] not in (None, ""):
            return vpc[name]
    return default


def vpc_names(vpcs):
    names = []
    for vpc in vpcs:
        name = _field(vpc, "name", default=None)
        if name is None:
            name = _field(vpc, "id")
        names.append(str(name))
    return names


def _cell(value):
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return str(value)


def _md_escape(value):
    """Escape pipe/newline characters so a cell cannot break the Markdown table."""
    return _cell(value).replace("|", "\\|").replace("\n", " ").replace("\r", " ")


def render_table(vpcs):
    """Render full-field table output (union of all returned fields)."""
    rows_data = [normalize_vpc(vpc) for vpc in vpcs]
    columns = []
    for key in PREFERRED_COLUMNS:
        if any(key in c for c in rows_data):
            columns.append(key)
    for key in sorted({k for c in rows_data for k in c}):
        if key not in columns:
            columns.append(key)
    if not columns:
        columns = ["id", "name"]
    rows = [[_cell(_field(c, col)) for col in columns] for c in rows_data]
    if rows:
        widths = [max(len(col), *(len(row[i]) for row in rows)) for i, col in enumerate(columns)]
    else:
        widths = [len(col) for col in columns]
    header = "  ".join(col.ljust(widths[i]) for i, col in enumerate(columns))
    separator = "  ".join("-" * w for w in widths)
    lines = [header, separator]
    for row in rows:
        lines.append("  ".join(row[i].ljust(widths[i]) for i in range(len(columns))))
    return "\n".join(lines)


def normalized_row(vpc, region=None):
    """Map a VPC record to the fixed Markdown column order."""
    return [
        _md_escape(_field(vpc, "name")),
        _md_escape(_field(vpc, "id")),
        _md_escape(region if region else _FIELD_MISSING),
        _md_escape(_field(vpc, "cidr")),
        _md_escape(_field(vpc, "status")),
        _md_escape(_field(vpc, "enterprise_project_id")),
        _md_escape(_field(vpc, "description")),
        _md_escape(_field(vpc, "created_at")),
    ]


def render_markdown(vpcs, summary=False, region=None):
    """Render the VPC list as a GitHub-flavored Markdown table.

    An empty list still renders a valid (header-only) table, so "no VPC" never
    produces a corrupt file — it produces an explicit empty table.
    """
    lines = [
        "| " + " | ".join(MD_HEADERS) + " |",
        "| " + " | ".join(["---"] * len(MD_HEADERS)) + " |",
    ]
    for vpc in vpcs:
        lines.append("| " + " | ".join(normalized_row(vpc, region=region)) + " |")
    if summary:
        lines.append("")
        lines.append("**汇总**：共 %d 个 VPC（Region %s）。"
                     % (len(vpcs), region or _FIELD_MISSING))
    return "\n".join(lines)


def default_output_path(region):
    """Default .md filename: vpc_list_<region>_<timestamp>.md"""
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return "%s_%s_%s.md" % (DEFAULT_FILENAME_PREFIX, region, stamp)


def export_markdown(vpcs, output_path, summary=False, region=None):
    """Write the VPC list as a Markdown report at ``output_path``.

    Args:
        vpcs:        iterable of VPC dicts.
        output_path: absolute or relative path of the ``.md`` file to write.
        summary:     when True, append a trailing summary line (VPC count).
        region:      optional region label used per row and in the summary line.

    Returns:
        The absolute path of the written file.

    Raises:
        ExportError: path unusable or write failed. No partial/corrupt file is
                     left behind.
    """
    vpcs = list(vpcs)
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

    text = render_markdown(vpcs, summary=summary, region=region)

    # Save via a temp file + atomic rename: interrupts never leave a corrupt
    # .md at the destination.
    fd, tmp_path = tempfile.mkstemp(
        prefix=".%s." % DEFAULT_FILENAME_PREFIX, suffix=".tmp",
        dir=output_dir or ".")
    os.close(fd)
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
        raise ExportError("Markdown 文件写出失败：%s（%s）"
                          % (output_path, exc))
    return output_path


def active_filter_descriptions(vpc_id=None, enterprise_project_id=None):
    """Human-readable description of the server-side filters actually applied."""
    filters = []
    if vpc_id:
        filters.append("id=%s" % vpc_id)
    if enterprise_project_id:
        filters.append("enterprise_project_id=%s" % enterprise_project_id)
    return filters


def parse_args(argv):
    parser = argparse.ArgumentParser(
        description="查询华为云虚拟私有云（VPC）列表并导出 Markdown 报表（只读）。")
    parser.add_argument("-r", "--region", default=DEFAULT_REGION,
                        help="目标 Region（默认 %s）" % DEFAULT_REGION)
    parser.add_argument("-f", "--format", default=DEFAULT_FORMAT,
                        choices=["md", "table", "json"],
                        help="输出格式：md（默认）/ table / json")
    parser.add_argument("-o", "--output", default=None,
                        help="Markdown 输出路径（--format md；默认 "
                             "vpc_list_<region>_<timestamp>.md）")
    parser.add_argument("--summary", action="store_true",
                        help="Markdown 报表末尾追加汇总行（VPC 数量）")
    parser.add_argument("--id", dest="vpc_id",
                        help="按 VPC ID 过滤（服务端查询参数）")
    parser.add_argument("--enterprise-project-id", dest="enterprise_project_id",
                        help="按企业项目 ID 过滤（服务端查询参数，0 表示默认企业项目）")
    parser.add_argument("--page-size", type=int, default=DEFAULT_PAGE_SIZE,
                        dest="page_size",
                        help="分页大小（默认 %d，范围 1~2000，自动翻页取全量）" % DEFAULT_PAGE_SIZE)
    parser.add_argument("--project-id", dest="project_id",
                        help="项目 ID（可选；SDK 回退在 /v1/{project_id}/vpcs 路径中需要）")
    parser.add_argument("--operation", default=ALLOWED_OPERATION,
                        help="hcloud VPC 操作名（仅允许只读 %s）" % ALLOWED_OPERATION)
    return parser.parse_args(argv)


def main(argv=None):
    raw_argv = argv if argv is not None else sys.argv[1:]

    # Write-intent guard runs on the RAW argv BEFORE argparse, so that a
    # mutating flag (e.g. `--create-vpc`) is reported as a guard violation
    # instead of an argparse "unrecognized argument" error.
    try:
        guard_write_intent(guard_text_from_argv(raw_argv))
    except VpcExportError as exc:
        print("[错误] %s" % exc, file=sys.stderr)
        return 1

    args = parse_args(argv)

    try:
        guard_operation(args.operation)
        if args.page_size is None or args.page_size < 1 or args.page_size > 2000:
            raise ApiError("--page-size 超出范围（1~2000）：%s" % args.page_size)
        vpcs = list_vpcs(
            args.region,
            vpc_id=args.vpc_id,
            enterprise_project_id=args.enterprise_project_id,
            limit=args.page_size,
            project_id=args.project_id,
        )
    except VpcExportError as exc:
        print("[错误] %s" % exc, file=sys.stderr)
        return 1

    filters = active_filter_descriptions(vpc_id=args.vpc_id,
                                         enterprise_project_id=args.enterprise_project_id)
    filter_suffix = "（过滤条件: %s）" % ", ".join(filters) if filters else ""
    fmt = args.format

    if fmt == "json":
        print(json.dumps(vpcs, ensure_ascii=False, indent=2))
        return 0

    if fmt == "table":
        if not vpcs:
            print("当前区域（%s）无虚拟私有云（VPC）%s。" % (args.region, filter_suffix))
            print(render_table([]))
            return 0
        print("Region %s 的虚拟私有云（VPC）列表（共 %d 个，完整字段）："
              % (args.region, len(vpcs)))
        print(render_table(vpcs))
        return 0

    # fmt == "md": an empty list still yields a valid header-only (empty) table.
    output_path = args.output or default_output_path(args.region)
    try:
        written = export_markdown(vpcs, output_path,
                                  summary=args.summary, region=args.region)
    except ExportError as exc:
        print("[错误] %s" % exc, file=sys.stderr)
        return 1

    if not vpcs:
        print("当前区域（%s）无虚拟私有云（VPC）%s，已生成空表（仅表头）：%s"
              % (args.region, filter_suffix, written))
        return 0

    print("已生成 VPC 列表 Markdown 报表（Region %s，共 %d 个 VPC，含 VPC 名称列）：%s"
          % (args.region, len(vpcs), written))
    return 0


if __name__ == "__main__":
    sys.exit(main())