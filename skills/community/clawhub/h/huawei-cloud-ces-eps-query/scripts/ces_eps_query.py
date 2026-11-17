#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Read-only Huawei Cloud CES / EPS management-plane queries (natural-language triggerable).

This skill queries **management-plane metadata only**:

CES (Cloud Eye Service, `huaweicloudsdkces` v2) — 7 categories:
    alarm-rules        告警规则列表        GET /v2/{project_id}/alarms
    alarm-histories    告警历史列表        GET /v2/{project_id}/alarm-histories
    alarm-templates    告警模板列表        GET /v2/{project_id}/alarm-templates
    dashboards         仪表盘列表          GET /v2/{project_id}/dashboards
    notification-masks 通知掩码列表        POST /v2/{project_id}/notification-masks/batch-query (read)
    resource-groups    资源分组列表        GET /v2/{project_id}/resource-groups
    one-click-alarms   一键告警列表        GET /v2/{project_id}/one-click-alarms

EPS (Enterprise Project Service, `huaweicloudsdkeps` v1) — 5 categories:
    eps-projects           企业项目列表    GET /v1.0/enterprise-projects
    eps-project-detail     企业项目详情    GET /v1.0/enterprise-projects/{enterprise_project_id}
    eps-quotas             企业项目配额    GET /v1.0/enterprise-projects/quotas
    eps-resources          企业项目绑定资源 POST /v1.0/enterprise-projects/{enterprise_project_id}/resources/filter (read)
    eps-migration-records  企业项目迁移记录 GET /v1.0/enterprise-projects/migrate-record/list

Execution order is KooCLI (`hcloud`) first, then the official SDK
(`huaweicloudsdkces` v2 / `huaweicloudsdkeps` v1), then a token-based REST GET
fallback. Every path is strictly read-only; a write-intent guard rejects
mutating intents before any command runs.

Every `hcloud` invocation on the CLI path is wrapped with `skill-quality-cli`
(`skill-quality-cli run --skill-name huawei-cloud-ces-eps-query -- hcloud ...`)
for quality telemetry; when the CLI is unavailable the path degrades to bare
`hcloud` and the CLI→SDK→REST fallback contract is unchanged. Disable telemetry
with `SKILL_QUALITY_REPORT=0`.

Explicitly OUT OF SCOPE (never executed by this skill): raw metric data points
(`ShowMetricData` / `ListMetrics` / `BatchListMetricData`), service-level metric
values (RDS / DCS / DMS / EVS / ELB ...), and every write operation
(create/update/delete/enable/disable/migrate/batch-*).

Usage:
    python3 scripts/ces_eps_query.py --query "查询告警规则" --region cn-north-4
    python3 scripts/ces_eps_query.py --category alarm-rules --json
    python3 scripts/ces_eps_query.py --category eps-project-detail --id <project_id>
    python3 scripts/ces_eps_query.py --list-categories
"""

import argparse
import importlib
import json
import os
import re
import shutil
import subprocess
import sys

DEFAULT_REGION = "cn-north-4"
DEFAULT_PAGE_SIZE = 50
HCLOUD_TIMEOUT = 120

# Skill-quality telemetry: every hcloud call on the script execution path is
# reported through skill-quality-cli (the mandatory wrapping口径). When the CLI
# is unavailable the path degrades to bare hcloud without changing the
# CLI→SDK→REST fallback contract.
SKILL_QUALITY_SKILL_NAME = "huawei-cloud-ces-eps-query"
_QUALITY_OFF_VALUES = ("0", "false", "no", "off")

# --------------------------------------------------------------------------
# Category registry (authoritative: SDK method + resource_path from
# huaweicloudsdkces v2 / huaweicloudsdkeps v1 source, verified via _http_info).
# --------------------------------------------------------------------------
CATEGORIES = {
    # ---- CES (7) ----
    "alarm-rules": {
        "label": "CES 告警规则",
        "service": "CES",
        "group": "ces",
        "cli_operation": "ListAlarmRules",
        "sdk_package": "huaweicloudsdkces.v2",
        "sdk_client": "CesClient",
        "sdk_method": "list_alarm_rules",
        "request": "ListAlarmRulesRequest",
        "sdk_region_module": "huaweicloudsdkces.v2.region.ces_region",
        "sdk_region_class": "CesRegion",
        "rest_path": "/v2/{project_id}/alarms",
        "result": ("list", "alarms"),
        "params": ("alarm_id", "name", "namespace", "resource_id",
                   "enterprise_project_id", "product_name", "resource_level",
                   "offset", "limit"),
    },
    "alarm-histories": {
        "label": "CES 告警历史",
        "service": "CES",
        "group": "ces",
        "cli_operation": "ListAlarmHistories",
        "sdk_package": "huaweicloudsdkces.v2",
        "sdk_client": "CesClient",
        "sdk_method": "list_alarm_histories",
        "request": "ListAlarmHistoriesRequest",
        "sdk_region_module": "huaweicloudsdkces.v2.region.ces_region",
        "sdk_region_class": "CesRegion",
        "rest_path": "/v2/{project_id}/alarm-histories",
        "result": ("list", "alarm_histories"),
        "params": ("alarm_id", "name", "status", "level", "namespace",
                   "resource_id", "offset", "limit"),
    },
    "alarm-templates": {
        "label": "CES 告警模板",
        "service": "CES",
        "group": "ces",
        "cli_operation": "ListAlarmTemplates",
        "sdk_package": "huaweicloudsdkces.v2",
        "sdk_client": "CesClient",
        "sdk_method": "list_alarm_templates",
        "request": "ListAlarmTemplatesRequest",
        "sdk_region_module": "huaweicloudsdkces.v2.region.ces_region",
        "sdk_region_class": "CesRegion",
        "rest_path": "/v2/{project_id}/alarm-templates",
        "result": ("list", "alarm_templates"),
        "params": ("offset", "limit", "namespace", "template_name"),
    },
    "dashboards": {
        "label": "CES 仪表盘",
        "service": "CES",
        "group": "ces",
        "cli_operation": "ListDashboardInfos",
        "sdk_package": "huaweicloudsdkces.v2",
        "sdk_client": "CesClient",
        "sdk_method": "list_dashboard_infos",
        "request": "ListDashboardInfosRequest",
        "sdk_region_module": "huaweicloudsdkces.v2.region.ces_region",
        "sdk_region_class": "CesRegion",
        "rest_path": "/v2/{project_id}/dashboards",
        "result": ("list", "dashboards"),
        "params": ("dashboard_id", "dashboard_name", "enterprise_id",
                   "is_favorite", "dashboard_type"),
    },
    "notification-masks": {
        "label": "CES 通知掩码",
        "service": "CES",
        "group": "ces",
        "cli_operation": "ListNotificationMasks",
        "sdk_package": "huaweicloudsdkces.v2",
        "sdk_client": "CesClient",
        "sdk_method": "list_notification_masks",
        "request": "ListNotificationMasksRequest",
        "sdk_region_module": "huaweicloudsdkces.v2.region.ces_region",
        "sdk_region_class": "CesRegion",
        "rest_path": "/v2/{project_id}/notification-masks/batch-query",
        "result": ("list", "notification_masks"),
        "params": ("offset", "limit", "sort_key", "sort_dir"),
    },
    "resource-groups": {
        "label": "CES 资源分组",
        "service": "CES",
        "group": "ces",
        "cli_operation": "ListResourceGroups",
        "sdk_package": "huaweicloudsdkces.v2",
        "sdk_client": "CesClient",
        "sdk_method": "list_resource_groups",
        "request": "ListResourceGroupsRequest",
        "sdk_region_module": "huaweicloudsdkces.v2.region.ces_region",
        "sdk_region_class": "CesRegion",
        "rest_path": "/v2/{project_id}/resource-groups",
        "result": ("list", "resource_groups"),
        "params": ("group_id", "group_name", "enterprise_project_id",
                   "offset", "limit"),
    },
    "one-click-alarms": {
        "label": "CES 一键告警",
        "service": "CES",
        "group": "ces",
        "cli_operation": "ListOneClickAlarms",
        "sdk_package": "huaweicloudsdkces.v2",
        "sdk_client": "CesClient",
        "sdk_method": "list_one_click_alarms",
        "request": "ListOneClickAlarmsRequest",
        "sdk_region_module": "huaweicloudsdkces.v2.region.ces_region",
        "sdk_region_class": "CesRegion",
        "rest_path": "/v2/{project_id}/one-click-alarms",
        "result": ("list", "one_click_alarms"),
        "params": (),
    },
    # ---- EPS (5) ----
    "eps-projects": {
        "label": "EPS 企业项目列表",
        "service": "EPS",
        "group": "eps",
        "cli_operation": "ListEnterpriseProject",
        "sdk_package": "huaweicloudsdkeps.v1",
        "sdk_client": "EpsClient",
        "sdk_method": "list_enterprise_project",
        "request": "ListEnterpriseProjectRequest",
        "sdk_region_module": "huaweicloudsdkeps.v1.region.eps_region",
        "sdk_region_class": "EpsRegion",
        "rest_path": "/v1.0/enterprise-projects",
        "result": ("list", "enterprise_projects"),
        "params": ("id", "name", "status", "type", "offset", "limit",
                   "sort_key", "sort_dir"),
    },
    "eps-project-detail": {
        "label": "EPS 企业项目详情",
        "service": "EPS",
        "group": "eps",
        "cli_operation": "ShowEnterpriseProject",
        "sdk_package": "huaweicloudsdkeps.v1",
        "sdk_client": "EpsClient",
        "sdk_method": "show_enterprise_project",
        "request": "ShowEnterpriseProjectRequest",
        "sdk_region_module": "huaweicloudsdkeps.v1.region.eps_region",
        "sdk_region_class": "EpsRegion",
        "rest_path": "/v1.0/enterprise-projects/{enterprise_project_id}",
        "result": ("single", "enterprise_project"),
        "params": ("enterprise_project_id",),
        "requires": ("enterprise_project_id",),
    },
    "eps-quotas": {
        "label": "EPS 企业项目配额",
        "service": "EPS",
        "group": "eps",
        "cli_operation": "ShowEnterpriseProjectQuota",
        "sdk_package": "huaweicloudsdkeps.v1",
        "sdk_client": "EpsClient",
        "sdk_method": "show_enterprise_project_quota",
        "request": "ShowEnterpriseProjectQuotaRequest",
        "sdk_region_module": "huaweicloudsdkeps.v1.region.eps_region",
        "sdk_region_class": "EpsRegion",
        "rest_path": "/v1.0/enterprise-projects/quotas",
        "result": ("list", "quotas"),
        "params": (),
    },
    "eps-resources": {
        "label": "EPS 企业项目绑定资源",
        "service": "EPS",
        "group": "eps",
        "cli_operation": "ShowResourceBindEnterpriseProject",
        "sdk_package": "huaweicloudsdkeps.v1",
        "sdk_client": "EpsClient",
        "sdk_method": "show_resource_bind_enterprise_project",
        "request": "ShowResourceBindEnterpriseProjectRequest",
        "sdk_region_module": "huaweicloudsdkeps.v1.region.eps_region",
        "sdk_region_class": "EpsRegion",
        "rest_path": "/v1.0/enterprise-projects/{enterprise_project_id}/resources/filter",
        "result": ("list", "resources"),
        "params": ("enterprise_project_id", "offset", "limit"),
        "requires": ("enterprise_project_id",),
    },
    "eps-migration-records": {
        "label": "EPS 企业项目迁移记录",
        "service": "EPS",
        "group": "eps",
        "cli_operation": "ListMigrationRecord",
        "sdk_package": "huaweicloudsdkeps.v1",
        "sdk_client": "EpsClient",
        "sdk_method": "list_migration_record",
        "request": "ListMigrationRecordRequest",
        "sdk_region_module": "huaweicloudsdkeps.v1.region.eps_region",
        "sdk_region_class": "EpsRegion",
        "rest_path": "/v1.0/enterprise-projects/migrate-record/list",
        "result": ("list", "records"),
        "params": ("resource_id", "start_time", "end_time", "offset", "limit"),
    },
}

CES_CATEGORIES = [k for k, v in CATEGORIES.items() if v["group"] == "ces"]
EPS_CATEGORIES = [k for k, v in CATEGORIES.items() if v["group"] == "eps"]

# --------------------------------------------------------------------------
# Natural-language intent routing. Ordered: the most specific phrases win.
# --------------------------------------------------------------------------
_NL_RULES = (
    # CES
    ("alarm-rules", ("告警规则", "alarm rule", "alarm-rules", "alarmrule")),
    ("alarm-histories", ("告警历史", "alarm histor", "告警记录")),
    ("alarm-templates", ("告警模板", "alarm template")),
    ("dashboards", ("仪表盘", "dashboard", "看板")),
    ("notification-masks", ("通知掩码", "掩码", "notification mask", "notification-mask")),
    ("resource-groups", ("资源分组", "resource group")),
    ("one-click-alarms", ("一键告警", "one-click alarm", "one click alarm",
                          "one-click-alarm")),
    # EPS — specific before generic "企业项目"
    ("eps-project-detail", ("企业项目详情", "enterprise project detail",
                            "show enterprise project")),
    ("eps-project-detail", ("企业项目 id", "企业项目ID", "企业项目 id 为")),
    ("eps-quotas", ("企业项目配额", "配额", "enterprise project quota", "quota")),
    ("eps-resources", ("绑定资源", "绑定的资源", "企业项目资源", "bound resource",
                       "bind enterprise project", "resources/filter")),
    ("eps-migration-records", ("迁移记录", "migration record", "migrate-record")),
    ("eps-projects", ("企业项目列表", "企业项目", "enterprise project")),
)


def classify_query(text):
    """Map a natural-language query to a category key, or None when unknown."""
    low = str(text or "").strip().lower()
    if not low:
        return None
    for category, phrases in _NL_RULES:
        for phrase in phrases:
            if phrase.lower() in low:
                return category
    return None


# --------------------------------------------------------------------------
# Write-intent guard (read-only skill).
# --------------------------------------------------------------------------
# Curated mutating vocabulary. Deliberately narrow so that legitimate read
# categories ("迁移记录"/"migration record", "绑定资源") are NOT flagged:
# e.g. "migrate" alone is excluded, only the write op "migrate resource" /
# "迁移资源" is a hit.
_WRITE_INTENT_KEYWORDS = (
    # CES writes
    "createalarm", "deletealarm", "updatealarm", "createalarmrule",
    "updatealarmrule", "deletealarmrule", "batchdeletealarmrules",
    "batchdeletealarmtemplates", "enablealarmrule", "createalarmtemplate",
    "updatealarmtemplate", "deletealarmtemplate", "createresourcegroup",
    "updateresourcegroup", "deleteresourcegroup", "createoneclickalarm",
    "deleteoneclickalarm", "createdashboard", "deletedashboard",
    "createdashboardwidget", "updatedashboard", "updatenotificationmask",
    "deletenotificationmask", "batchupdatenotificationmasks",
    # EPS writes
    "createenterpriseproject", "updateenterpriseproject",
    "deleteenterpriseproject", "enableenterpriseproject",
    "disableenterpriseproject", "migrateresource",
    # generic verbs
    "create", "delete", "remove", "update", "modify", "overwrite",
    "enable", "disable", "attach", "detach", "associate", "dissociate",
)
_WRITE_INTENT_ZH = (
    "创建", "删除", "移除", "修改", "更新", "启用", "停用",
    "解绑", "迁移资源", "批量创建", "批量删除", "批量更新",
)

# Values of these flags are read-only data (region, ids, filters, paging) and
# must NOT be scanned for generic write vocabulary. `--query` is intentionally
# NOT stripped: the natural-language intent itself is scanned, and the
# keyword list is curated so legitimate read phrases ("查询迁移记录",
# "查询企业项目绑定资源") are never mistaken for a write.
_VALUE_STRIPPED_FLAGS = (
    "--region", "-r", "--category", "--id", "-i",
    "--name", "--limit", "--offset", "--project-id", "--filter",
    "--sort-key", "--sort-dir", "--time-from", "--time-to", "--resource-id",
)


class CesEpsError(Exception):
    """Base error for the CES/EPS query skill."""


class GuardError(CesEpsError):
    """A write intent was detected and blocked (the skill is read-only)."""


class ConfigError(CesEpsError):
    """hcloud missing / credentials not configured / no execution backend."""


class AuthError(CesEpsError):
    """Authentication or authorization failure (invalid AK/SK or IAM 403)."""


class ApiError(CesEpsError):
    """hcloud / SDK / network / unexpected API failure."""


def _normalize(text):
    return re.sub(r"[\s_\-]+", "", str(text).lower())


def guard_write_intent(text):
    """Raise GuardError when `text` carries a mutating intent."""
    low = _normalize(text)
    for keyword in _WRITE_INTENT_KEYWORDS:
        if _normalize(keyword) and _normalize(keyword) in low:
            raise GuardError(
                "检测到写操作意图（关键词: %s）。本 skill 为只读查询"
                "（CES/EPS 管理面），创建/删除/修改/启停/迁移等写操作已被守卫拦截。"
                % keyword)
    raw = str(text)
    for keyword in _WRITE_INTENT_ZH:
        if keyword in raw:
            raise GuardError(
                "检测到写操作意图（关键词: %s）。本 skill 为只读查询"
                "（CES/EPS 管理面），写操作已被守卫拦截。" % keyword)
    return False


def guard_operation(category, operation=None):
    """Only whitelisted read-only categories/operations may be executed."""
    if category not in CATEGORIES:
        raise GuardError(
            "不允许的查询类别 %r：仅支持 %s。" % (category, ", ".join(sorted(CATEGORIES))))
    if operation is not None:
        spec = CATEGORIES[category]
        read_ops = {spec["cli_operation"], spec["sdk_method"]}
        if operation not in read_ops:
            raise GuardError(
                "不允许的操作 %r：类别 %s 仅允许只读操作 %s。"
                % (operation, category, spec["cli_operation"]))
    return True


def guard_text_from_argv(argv):
    """Build the text the write-intent guard scans (flag values stripped)."""
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


# --------------------------------------------------------------------------
# CLI (KooCLI) path
# --------------------------------------------------------------------------
def _hcloud_executable():
    return os.environ.get("CES_EPS_HCLOUD_BIN", "hcloud")


def _quality_report_enabled():
    """Quality telemetry is on unless SKILL_QUALITY_REPORT is set to a falsy value."""
    value = os.environ.get("SKILL_QUALITY_REPORT")
    if value is None:
        return True
    return value.strip().lower() not in _QUALITY_OFF_VALUES


def _skill_quality_executable():
    """Locate skill-quality-cli: env override → PATH → ~/.local/bin, else None."""
    override = os.environ.get("CES_EPS_SQC_BIN")
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
    """Bare hcloud argv: CES_EPS_HCLOUD_BIN override + extra args + argv."""
    cmd = [_hcloud_executable()]
    extra = os.environ.get("CES_EPS_HCLOUD_ARGS", "").split()
    if extra:
        cmd.extend(extra)
    cmd.extend(argv)
    return cmd


def build_hcloud_command(argv):
    """Build the hcloud execution argv, wrapping it with skill-quality-cli.

    Every CLI call is reported as ``skill-quality-cli run --skill-name
    huawei-cloud-ces-eps-query -- hcloud ...`` (the skill's mandatory wrapping
    口径, enforced here on the script path rather than left to the agent). The
    command degrades to bare hcloud when the telemetry CLI is missing or
    ``SKILL_QUALITY_REPORT=0``; an explicit ``CES_EPS_HCLOUD_BIN`` override
    (offline mock / verification) is always run verbatim.
    """
    hcloud_cmd = _hcloud_argv(argv)
    if os.environ.get("CES_EPS_HCLOUD_BIN"):
        return hcloud_cmd
    if not _quality_report_enabled():
        return hcloud_cmd
    quality_cli = _skill_quality_executable()
    if not quality_cli:
        return hcloud_cmd
    return ([quality_cli, "run", "--skill-name", SKILL_QUALITY_SKILL_NAME, "--"]
            + hcloud_cmd)


def build_cli_command(category, region, limit, offset, params=None):
    """Build the `hcloud <Service> <Operation> --cli-region=<region> ...` argv."""
    spec = CATEGORIES[category]
    argv = [spec["service"], spec["cli_operation"], "--cli-region=%s" % region]
    if limit is not None:
        argv.append("--limit=%d" % limit)
    if offset:
        argv.append("--offset=%d" % offset)
    for key, value in (params or {}).items():
        if value is None:
            continue
        if isinstance(value, bool):
            value = "true" if value else "false"
        argv.append("--%s=%s" % (key, value))
    return argv


def run_hcloud(argv):
    """Execute hcloud through skill-quality-cli when available.

    Returns ``(stdout, stderr, returncode)``; the CLI→SDK→REST fallback contract
    is unchanged.
    """
    cmd = build_hcloud_command(argv)
    try:
        proc = subprocess.run(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            timeout=HCLOUD_TIMEOUT, universal_newlines=True,
        )
    except FileNotFoundError:
        raise ConfigError(
            "未找到 hcloud（KooCLI）。将回退到 huaweicloudsdkces / huaweicloudsdkeps SDK；"
            "参见 references/cli-installation-guide.md。")
    except subprocess.TimeoutExpired:
        raise ApiError("hcloud 执行超时（%ds），请检查网络后重试。" % HCLOUD_TIMEOUT)
    return proc.stdout or "", proc.stderr or "", proc.returncode


def extract_json(stdout):
    """Parse hcloud stdout as JSON, tolerating wrapper/noise lines."""
    text = (stdout or "").strip()
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
        bracket_start, bracket_end = text.find("["), text.rfind("]")
        if bracket_start >= 0 and bracket_end > bracket_start:
            try:
                return json.loads(text[bracket_start:bracket_end + 1])
            except json.JSONDecodeError:
                pass
        raise ApiError("hcloud 输出无法解析为 JSON：%s" % text[:200])


_USE_ERROR_MARKER = "[use_error]"
_CREDENTIAL_MISSING_PATTERNS = (
    "cli-ak", "cli-sk", "access key", "secret key", "credential",
    "configure", "未配置", "配置为空", "no ak", "no sk", "ak/sk",
)
_AUTH_PATTERNS = (
    "401", "403", "unauthorized", "forbidden", "apigw.0301",
    "认证失败", "权限不足", "permission denied",
)


def classify_hcloud_failure(stdout, stderr, returncode):
    """Map a failed hcloud invocation to a domain error with explicit hints."""
    blob = (stderr + " " + stdout).strip()
    low = blob.lower()
    if _USE_ERROR_MARKER in low:
        return ApiError(
            "hcloud 参数错误（KooCLI 拒绝了该参数组合，退出码 %s）；"
            "该服务/操作可能未在当前 KooCLI 版本中提供，将回退 SDK。详情：%s"
            % (returncode, blob[:300]))
    if any(p in low for p in _CREDENTIAL_MISSING_PATTERNS) and not re.search(r"\b40[13]\b", blob):
        return ConfigError(
            "缺少 AK/SK 凭证：hcloud 未配置有效凭证。请设置凭证环境变量或运行 "
            "hcloud configure（严禁在对话中粘贴 AK/SK），参见 "
            "references/cli-installation-guide.md。详情：%s" % blob[:300])
    if any(p in low for p in _AUTH_PATTERNS):
        return AuthError(
            "无权限访问 CES/EPS，请检查 IAM 权限（403：AK/SK 无效或未授予只读权限），"
            "参见 references/iam-policies.md。详情：%s" % blob[:300])
    return ApiError("hcloud 调用失败（退出码 %s）：%s" % (returncode, blob[:300]))


# --------------------------------------------------------------------------
# Response normalization
# --------------------------------------------------------------------------
def to_plain(value):
    """Convert an SDK model / nested structure to plain JSON-friendly data."""
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, dict):
        return {k: to_plain(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [to_plain(v) for v in value]
    to_dict = getattr(value, "to_dict", None)
    if callable(to_dict):
        try:
            return to_plain(to_dict())
        except Exception:
            pass
    to_json = getattr(value, "to_json_object", None)
    if callable(to_json):
        try:
            return to_plain(to_json())
        except Exception:
            pass
    return value


def extract_result(category, response):
    """Pull the payload (list or single object) out of a response object."""
    kind, key = CATEGORIES[category]["result"]
    if isinstance(response, dict):
        payload = response.get(key)
    else:
        payload = getattr(response, key, None)
    payload = to_plain(payload)
    if kind == "single":
        return payload if payload is not None else {}
    if payload is None:
        return []
    if isinstance(payload, list):
        return payload
    return [payload]


def _extract_list_from_payload(category, payload):
    """Best-effort extraction of the list from a raw JSON CLI/REST payload."""
    kind, key = CATEGORIES[category]["result"]
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        value = payload.get(key)
        if kind == "single":
            return value if value is not None else payload
        if isinstance(value, list):
            return value
        for candidate in ("items", "data", "results"):
            value = payload.get(candidate)
            if isinstance(value, list):
                return value
    return []


# --------------------------------------------------------------------------
# SDK path
# --------------------------------------------------------------------------
_AK_ENV_NAMES = (
    "HW_ACCESS_KEY", "HUAWEI_ACCESS_KEY", "HUAWEICLOUD_SDK_AK",
    "HUAWEI_CLOUD_ACCESS_KEY", "HUAWEI_AK", "HW_AK", "HWC_ACCESS_KEY",
)
_SK_ENV_NAMES = (
    "HW_SECRET_KEY", "HUAWEI_SECRET_KEY", "HUAWEICLOUD_SDK_SK",
    "HUAWEI_CLOUD_SECRET_KEY", "HUAWEI_SK", "HW_SK", "HWC_SECRET_KEY",
)


def _env_value(names):
    """Read the first non-empty value from an explicit env-name whitelist."""
    for name in names:
        value = os.environ.get(name)
        if value:
            return value
    return None


def _load_sdk(category):
    """Import and return the SDK symbols needed for `category`."""
    spec = CATEGORIES[category]
    core_credentials = importlib.import_module("huaweicloudsdkcore.auth.credentials")
    core_region = importlib.import_module("huaweicloudsdkcore.region.region")
    core_http = importlib.import_module("huaweicloudsdkcore.http.http_config")
    package = importlib.import_module(spec["sdk_package"])
    region_module = importlib.import_module(spec["sdk_region_module"])
    return {
        "credentials": core_credentials.BasicCredentials,
        "region": core_region.Region,
        "http_config": core_http.HttpConfig,
        "client": getattr(package, spec["sdk_client"]),
        "request": getattr(package, spec["request"]),
        "region_catalog": getattr(region_module, spec["sdk_region_class"]),
        "spec": spec,
    }


def build_sdk_request(category, loader, params):
    """Construct the SDK request object for `category` from generic params."""
    spec = loader["spec"]
    kwargs = {}
    for key, value in (params or {}).items():
        if value is None:
            continue
        if key in spec["params"]:
            kwargs[key] = value
    return loader["request"](**kwargs)


def query_via_sdk(category, region, params, loader=None):
    """Query through the official SDK. Returns (kind, payload).

    `loader` is injectable for offline tests.
    """
    if loader is None:
        try:
            loader = _load_sdk(category)
        except ImportError as exc:
            raise ConfigError(
                "SDK 不可用：未安装 huaweicloudsdkcore/huaweicloudsdkces/"
                "huaweicloudsdkeps（%s）。请运行 scripts/ensure_env.py 安装。" % exc)
    spec = loader["spec"]
    ak = _env_value(_AK_ENV_NAMES)
    sk = _env_value(_SK_ENV_NAMES)
    if not ak or not sk:
        raise ConfigError(
            "SDK 回退缺少 AK/SK 凭证：官方 SDK 的 BasicCredentials 不会自动读取环境变量，"
            "且未检测到 HUAWEI_ACCESS_KEY / HW_ACCESS_KEY / HUAWEICLOUD_SDK_AK 形式的"
            " AK/SK 环境变量。请在会话外设置凭证（严禁在对话中粘贴 AK/SK），参见 "
            "references/cli-installation-guide.md。")
    credentials = loader["credentials"](ak=ak, sk=sk)
    try:
        try:
            region_obj = loader["region_catalog"].value_of(region)
        except (ValueError, KeyError, AttributeError):
            region_obj = loader["region"](region, "https://%s.%s.myhuaweicloud.com"
                                          % (spec["group"], region))
    except Exception as exc:
        raise ConfigError("SDK 区域解析失败（region=%s）：%s" % (region, exc))
    try:
        client = loader["client"].new_builder() \
            .with_credentials(credentials) \
            .with_region(region_obj) \
            .with_http_config(loader["http_config"].get_default_config()) \
            .build()
    except Exception as exc:
        raise ConfigError("SDK 初始化失败（region=%s）：%s" % (region, exc))
    request = build_sdk_request(category, loader, params)
    try:
        response = getattr(client, spec["sdk_method"])(request)
    except Exception as exc:
        low = str(exc).lower()
        if any(p in low for p in _AUTH_PATTERNS):
            raise AuthError("无权限访问 %s，请检查 IAM 权限（403）。详情：%s"
                            % (spec["service"], str(exc)[:300]))
        raise ApiError("SDK 调用失败（%s.%s）：%s"
                       % (spec["service"], spec["sdk_method"], str(exc)[:300]))
    return extract_result(category, response)


# --------------------------------------------------------------------------
# REST fallback (token-based, read-only)
# --------------------------------------------------------------------------
_TOKEN_ENV_NAMES = ("CES_EPS_TOKEN", "HW_AUTH_TOKEN", "HUAWEI_AUTH_TOKEN")


def _http_get_json(url, token):
    import urllib.error
    import urllib.request
    request = urllib.request.Request(url, method="GET")
    request.add_header("X-Auth-Token", token)
    request.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            body = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        if exc.code in (401, 403):
            raise AuthError("REST 调用认证失败（HTTP %s）：请检查 token 与 IAM 权限。"
                            % exc.code)
        raise ApiError("REST 调用失败（HTTP %s）：%s" % (exc.code, exc.reason))
    except Exception as exc:
        raise ApiError("REST 调用失败：%s" % exc)
    try:
        return json.loads(body)
    except json.JSONDecodeError:
        raise ApiError("REST 响应无法解析为 JSON：%s" % body[:200])


def query_via_rest(category, region, params, project_id=None, token=None):
    """Token-based REST GET fallback (needs a project id + an auth token)."""
    spec = CATEGORIES[category]
    token = token or _env_value(_TOKEN_ENV_NAMES)
    project_id = project_id or os.environ.get("CES_EPS_PROJECT_ID") \
        or os.environ.get("HUAWEI_PROJECT_ID")
    if not token:
        raise ConfigError(
            "REST 回退缺少认证 token（设置 CES_EPS_TOKEN / HW_AUTH_TOKEN，"
            "或提供 CES_EPS_PROJECT_ID）。")
    path = spec["rest_path"].replace("{project_id}", project_id or "")
    for name, value in (params or {}).items():
        path = path.replace("{%s}" % name, str(value))
    if "{" in path:
        raise ConfigError("REST 路径缺少必要参数：%s" % path)
    url = "https://%s.%s.myhuaweicloud.com%s" % (spec["group"], region, path)
    payload = _http_get_json(url, token)
    return _extract_list_from_payload(category, payload)


# --------------------------------------------------------------------------
# Orchestration: CLI → SDK → REST
# --------------------------------------------------------------------------
def _params_from_args(args, category):
    """Assemble generic query params from parsed CLI args."""
    spec = CATEGORIES[category]
    params = {}
    if args.limit is not None:
        params["limit"] = args.limit
    if args.offset is not None:
        params["offset"] = args.offset
    if args.name:
        params["name"] = args.name
    if args.resource_id:
        params["resource_id"] = args.resource_id
    if args.filter:
        params["filter"] = args.filter
    # category-specific id
    if args.id:
        if category == "eps-project-detail":
            params["enterprise_project_id"] = args.id
        elif category == "eps-resources":
            params["enterprise_project_id"] = args.id
        elif spec["result"][1] in ("alarms",):
            params["alarm_id"] = args.id
        elif "resource_group" in spec["result"][1]:
            params["group_id"] = args.id
        else:
            params["id"] = args.id
    # only keep params declared by the category
    return {k: v for k, v in params.items() if k in spec["params"] and v is not None}


def query(category, region, args):
    """Run a query via CLI → SDK → REST, returning (payload, backend)."""
    spec = CATEGORIES[category]
    params = _params_from_args(args, category)
    for required in spec.get("requires", ()):
        if not params.get(required):
            raise ApiError("类别 %s 缺少必填参数 --id（%s）。" % (category, required))

    # 1) CLI
    try:
        argv = build_cli_command(category, region, args.limit, args.offset, params)
        stdout, stderr, returncode = run_hcloud(argv)
    except ConfigError:
        stdout = stderr = None
    if stdout is not None:
        if returncode == 0 and _USE_ERROR_MARKER not in (stdout + " " + stderr).lower():
            payload = extract_json(stdout)
            return _extract_list_from_payload(category, payload), "cli"
        # CLI failed (missing service/op, credentials...) → fall through to SDK.

    # 2) SDK
    try:
        result = query_via_sdk(category, region, params)
        return result, "sdk"
    except ConfigError as exc:
        sdk_error = exc
    except (AuthError, ApiError):
        raise

    # 3) REST
    try:
        return query_via_rest(category, region, params), "rest"
    except (AuthError, ApiError):
        raise
    except ConfigError as rest_exc:
        raise ConfigError(
            "无可用执行后端：CLI 不可用、SDK 不可用（%s）、REST 不可用（%s）"
            % (sdk_error, rest_exc))


# --------------------------------------------------------------------------
# Rendering
# --------------------------------------------------------------------------
def _cell(value):
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    if value is None:
        return "-"
    return str(value)


_PREFERRED_KEYS = (
    "name", "alarm_name", "id", "alarm_id", "group_name", "group_id",
    "template_name", "template_id", "dashboard_name", "dashboard_id",
    "enterprise_project_name", "enterprise_project_id", "mask_name",
    "mask_id", "one_click_alarm_name", "one_click_alarm_id", "status",
    "type", "enabled", "create_time", "update_time",
)


def render_table(rows):
    """Render a list of dict rows as an aligned text table."""
    rows = [r for r in rows if isinstance(r, dict)]
    if not rows:
        return ""
    columns = [k for k in _PREFERRED_KEYS if any(k in r for r in rows)]
    for key in sorted({k for r in rows for k in r}):
        if key not in columns:
            columns.append(key)
    if not columns:
        return ""
    widths = [max(len(col), *(len(_cell(r.get(col))) for r in rows))
              for col in columns]
    header = "  ".join(col.ljust(widths[i]) for i, col in enumerate(columns))
    separator = "  ".join("-" * w for w in widths)
    lines = [header, separator]
    for row in rows:
        lines.append("  ".join(_cell(row.get(col)).ljust(widths[i])
                               for i, col in enumerate(columns)))
    return "\n".join(lines)


def print_result(category, rows, region, backend, as_json):
    spec = CATEGORIES[category]
    if as_json:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
        return
    if isinstance(rows, list) and not rows:
        print("Region %s 的 %s：无数据。" % (region, spec["label"]))
        return
    if isinstance(rows, list):
        print("Region %s 的 %s（共 %d 条，backend=%s）："
              % (region, spec["label"], len(rows), backend))
        table = render_table(rows)
        if table:
            print(table)
        else:
            print(json.dumps(rows, ensure_ascii=False, indent=2))
    else:
        print("Region %s 的 %s（backend=%s）：" % (region, spec["label"], backend))
        print(json.dumps(rows, ensure_ascii=False, indent=2))


def list_categories():
    for key in CATEGORIES:
        spec = CATEGORIES[key]
        print("%-22s %-26s %s %s" % (key, spec["label"],
                                     spec["service"], spec["cli_operation"]))


# --------------------------------------------------------------------------
# Entry point
# --------------------------------------------------------------------------
def build_parser():
    parser = argparse.ArgumentParser(
        description="查询华为云 CES/EPS 管理面元数据（只读，自然语言可触发）。")
    parser.add_argument("-q", "--query", help="自然语言查询意图，自动路由到某个查询类别")
    parser.add_argument("--category", choices=sorted(CATEGORIES),
                        help="直接指定查询类别（与 --query 二选一）")
    parser.add_argument("-r", "--region", default=DEFAULT_REGION,
                        help="目标 Region（默认 %s）" % DEFAULT_REGION)
    parser.add_argument("--json", action="store_true", dest="as_json",
                        help="以 JSON 输出完整字段")
    parser.add_argument("--id", "-i", default=None,
                        help="资源 ID（告警规则/企业项目/分组/模板等，按类别解释）")
    parser.add_argument("--name", default=None, help="按名称过滤（服务端参数）")
    parser.add_argument("--resource-id", dest="resource_id", default=None,
                        help="按资源 ID 过滤（CES）")
    parser.add_argument("--filter", default=None, help="额外过滤表达式（透传）")
    parser.add_argument("--limit", type=int, default=DEFAULT_PAGE_SIZE,
                        help="分页大小（默认 %d）" % DEFAULT_PAGE_SIZE)
    parser.add_argument("--offset", type=int, default=0, help="分页偏移（默认 0）")
    parser.add_argument("--operation", default=None,
                        help="显式指定操作名（仅允许只读操作，用于守卫校验）")
    parser.add_argument("--list-categories", action="store_true",
                        dest="list_categories", help="列出全部支持的查询类别")
    return parser


def main(argv=None):
    # Write-intent guard runs on the RAW argv before argparse so that a
    # mutating flag is reported as a guard violation.
    try:
        guard_write_intent(guard_text_from_argv(argv))
    except CesEpsError as exc:
        print("[错误] %s" % exc, file=sys.stderr)
        return 1

    args = build_parser().parse_args(argv)

    if args.list_categories:
        list_categories()
        return 0

    category = args.category or classify_query(args.query)
    if not category:
        print("[错误] 无法识别查询意图：请提供 --query '<自然语言>' 或 --category。"
              "可用类别：%s" % ", ".join(sorted(CATEGORIES)), file=sys.stderr)
        return 1

    try:
        guard_operation(category, args.operation)
        rows_or_obj, backend = query(category, args.region, args)
    except CesEpsError as exc:
        print("[错误] %s" % exc, file=sys.stderr)
        return 1

    print_result(category, rows_or_obj, args.region, backend, args.as_json)
    return 0


if __name__ == "__main__":
    sys.exit(main())