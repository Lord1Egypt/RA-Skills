#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Read-only Huawei Cloud AOM (Application Operations Management) name-list query.

This skill queries **management-plane metadata only**: it lists AOM resources and
renders their names. Every category maps to a single *read* operation whose REST
path was verified against the official `huaweicloudsdkaom` v2 SDK source
(`_http_info.resource_path`); no mutating operation is constructible.

AOM name-list categories (12, `huaweicloudsdkaom` v2):

    alarm-rules                告警规则列表          GET /v2/{project_id}/alarm-rules
    alarm-rule-templates       告警规则模板列表      GET /v4/{project_id}/alarm-rules-template
    metric-or-event-alarm-rules 指标/事件告警规则列表 GET /v4/{project_id}/alarm-rules
    event2alarm-rules          事件告警规则列表      GET /v2/{project_id}/event2alarm-rule
    action-rules               行动规则列表          GET /v2/{project_id}/alert/action-rules
    mute-rules                 静默规则列表          GET /v2/{project_id}/alert/mute-rules
    dashboards                 仪表盘列表            GET /v2/{project_id}/aom/dashboards
    dashboard-folders          仪表盘分组列表        GET /v2/{project_id}/aom/dashboards-folder
    notification-templates     通知模板列表          GET /v2/{project_id}/events/notification/templates
    prom-instances             Prometheus 实例列表   GET /v1/{project_id}/aom/prometheus
    access-codes               接入码列表            GET /v1/{project_id}/access-code
    service-discovery-rules    服务发现规则列表      GET /v1/{project_id}/inv/servicediscoveryrules

Execution order is KooCLI (`hcloud`) first, then the official SDK
(`huaweicloudsdkaom` v2), then a token-based REST GET fallback. Every path is
strictly read-only; a write-intent guard rejects mutating intents before any
command runs.

Explicitly OUT OF SCOPE (never executed by this skill): raw metric data points
(`ListMetricItems` / `ShowMetricsData` / Prometheus `query` / `query_range`),
log items (`ListLogItems`), the AOM CMDB resource detail lookups
(`ShowAppByName` / `ShowComponentByName` / `ShowEnvByName` — these have no list
endpoint), and every write operation (create/update/delete/batch-*).

Usage:
    python3 scripts/list_aom.py --query "查询告警规则" --region cn-north-4
    python3 scripts/list_aom.py --category prom-instances --json
    python3 scripts/list_aom.py --category dashboards --names-only
    python3 scripts/list_aom.py --list-categories
"""

import argparse
import importlib
import json
import os
import re
import subprocess
import sys

DEFAULT_REGION = "cn-north-4"
DEFAULT_PAGE_SIZE = 50
HCLOUD_TIMEOUT = 120

# --------------------------------------------------------------------------
# Category registry (authoritative: SDK method + resource_path from
# huaweicloudsdkaom v2 source, verified via _http_info). `name_field` is the
# response field that carries the human-readable resource name.
# --------------------------------------------------------------------------
CATEGORIES = {
    "alarm-rules": {
        "label": "AOM 告警规则",
        "service": "AOM",
        "group": "aom",
        "cli_operation": "ListAlarmRule",
        "sdk_package": "huaweicloudsdkaom.v2",
        "sdk_client": "AomClient",
        "sdk_method": "list_alarm_rule",
        "request": "ListAlarmRuleRequest",
        "rest_path": "/v2/{project_id}/alarm-rules",
        "result": ("list", "thresholds"),
        "name_field": "alarm_rule_name",
        "params": ("offset", "limit"),
    },
    "alarm-rule-templates": {
        "label": "AOM 告警规则模板",
        "service": "AOM",
        "group": "aom",
        "cli_operation": "ListAlarmRuleTemplate",
        "sdk_package": "huaweicloudsdkaom.v2",
        "sdk_client": "AomClient",
        "sdk_method": "list_alarm_rule_template",
        "request": "ListAlarmRuleTemplateRequest",
        "rest_path": "/v4/{project_id}/alarm-rules-template",
        "result": ("list", "alarm_rule_templates"),
        "name_field": "alarm_rule_template_name",
        "params": ("enterprise_project_id", "id", "type"),
        # KooCLI exposes a parameter by its API definition name; the AOM
        # Enterprise-Project-Id parameter is a *header*, so the CLI flag keeps
        # the header casing instead of the SDK's snake_case field name.
        "cli_param_names": {"enterprise_project_id": "Enterprise-Project-Id"},
    },
    "metric-or-event-alarm-rules": {
        "label": "AOM 指标/事件告警规则",
        "service": "AOM",
        "group": "aom",
        "cli_operation": "ListMetricOrEventAlarmRule",
        "sdk_package": "huaweicloudsdkaom.v2",
        "sdk_client": "AomClient",
        "sdk_method": "list_metric_or_event_alarm_rule",
        "request": "ListMetricOrEventAlarmRuleRequest",
        "rest_path": "/v4/{project_id}/alarm-rules",
        "result": ("list", "alarm_rules"),
        "name_field": "alarm_rule_name",
        "params": ("name", "limit", "offset", "sort_by", "event_source",
                   "event_severity", "alarm_rule_status", "alarm_rule_type",
                   "prom_instance_id", "bind_notification_rule_id",
                   "related_cce_clusters", "enterprise_project_id"),
        "cli_param_names": {"enterprise_project_id": "Enterprise-Project-Id"},
    },
    "event2alarm-rules": {
        "label": "AOM 事件告警规则",
        "service": "AOM",
        "group": "aom",
        "cli_operation": "ListEvent2alarmRule",
        "sdk_package": "huaweicloudsdkaom.v2",
        "sdk_client": "AomClient",
        "sdk_method": "list_event2alarm_rule",
        "request": "ListEvent2alarmRuleRequest",
        "rest_path": "/v2/{project_id}/event2alarm-rule",
        "result": ("list", "body"),
        "name_field": "name",
        "params": (),
    },
    "action-rules": {
        "label": "AOM 行动规则",
        "service": "AOM",
        "group": "aom",
        "cli_operation": "ListActionRule",
        "sdk_package": "huaweicloudsdkaom.v2",
        "sdk_client": "AomClient",
        "sdk_method": "list_action_rule",
        "request": "ListActionRuleRequest",
        "rest_path": "/v2/{project_id}/alert/action-rules",
        "result": ("list", "action_rules"),
        "name_field": "rule_name",
        "params": (),
    },
    "mute-rules": {
        "label": "AOM 静默规则",
        "service": "AOM",
        "group": "aom",
        "cli_operation": "ListMuteRule",
        "sdk_package": "huaweicloudsdkaom.v2",
        "sdk_client": "AomClient",
        "sdk_method": "list_mute_rule",
        "request": "ListMuteRuleRequest",
        "rest_path": "/v2/{project_id}/alert/mute-rules",
        "result": ("list", "body"),
        "name_field": "name",
        "params": (),
    },
    "dashboards": {
        "label": "AOM 仪表盘",
        "service": "AOM",
        "group": "aom",
        "cli_operation": "ListDashBoards",
        "sdk_package": "huaweicloudsdkaom.v2",
        "sdk_client": "AomClient",
        "sdk_method": "list_dash_boards",
        "request": "ListDashBoardsRequest",
        "rest_path": "/v2/{project_id}/aom/dashboards",
        "result": ("list", "dashboards"),
        "name_field": "dashboard_title",
        "params": ("dashboard_type", "enterprise_project_id"),
        "cli_param_names": {"enterprise_project_id": "Enterprise-Project-Id"},
    },
    "dashboard-folders": {
        "label": "AOM 仪表盘分组",
        "service": "AOM",
        "group": "aom",
        "cli_operation": "ListDashboardsFolder",
        "sdk_package": "huaweicloudsdkaom.v2",
        "sdk_client": "AomClient",
        "sdk_method": "list_dashboards_folder",
        "request": "ListDashboardsFolderRequest",
        "rest_path": "/v2/{project_id}/aom/dashboards-folder",
        "result": ("list", "body"),
        "name_field": "folder_title",
        "params": ("enterprise_project_id",),
        "cli_param_names": {"enterprise_project_id": "Enterprise-Project-Id"},
    },
    "notification-templates": {
        "label": "AOM 通知模板",
        "service": "AOM",
        "group": "aom",
        "cli_operation": "ListNotificationTemplates",
        "sdk_package": "huaweicloudsdkaom.v2",
        "sdk_client": "AomClient",
        "sdk_method": "list_notification_templates",
        "request": "ListNotificationTemplatesRequest",
        "rest_path": "/v2/{project_id}/events/notification/templates",
        "result": ("list", "body"),
        "name_field": "name",
        "params": ("enterprise_project_id",),
        "cli_param_names": {"enterprise_project_id": "Enterprise-Project-Id"},
    },
    "prom-instances": {
        "label": "AOM Prometheus 实例",
        "service": "AOM",
        "group": "aom",
        "cli_operation": "ListPromInstance",
        "sdk_package": "huaweicloudsdkaom.v2",
        "sdk_client": "AomClient",
        "sdk_method": "list_prom_instance",
        "request": "ListPromInstanceRequest",
        "rest_path": "/v1/{project_id}/aom/prometheus",
        "result": ("list", "prometheus"),
        "name_field": "prom_name",
        "params": ("prom_id", "prom_type", "cce_cluster_enable", "prom_status",
                   "enterprise_project_id"),
        # ListPromInstance's Enterprise-Project-Id is a *header* in the AOM API
        # (SDK attribute_map: enterprise_project_id -> "Enterprise-Project-Id").
        # KooCLI only accepts the header form, so the CLI flag must be
        # `--Enterprise-Project-Id`; passing `--enterprise_project_id` yields
        # "[USE_ERROR]Invalid parameter: enterprise_project_id" and kills both
        # the CLI primary path and the SDK-403 degrade retry.
        "cli_param_names": {"enterprise_project_id": "Enterprise-Project-Id"},
        # Default it to the default enterprise project ("0") so the CLI path
        # stays viable when the caller does not pass --enterprise-project-id.
        "default_params": {"enterprise_project_id": "0"},
    },
    "access-codes": {
        "label": "AOM 接入码",
        "service": "AOM",
        "group": "aom",
        "cli_operation": "ListAccessCode",
        "sdk_package": "huaweicloudsdkaom.v2",
        "sdk_client": "AomClient",
        "sdk_method": "list_access_code",
        "request": "ListAccessCodeRequest",
        "rest_path": "/v1/{project_id}/access-code",
        "result": ("list", "access_codes"),
        "name_field": "access_code",
        "params": (),
    },
    "service-discovery-rules": {
        "label": "AOM 服务发现规则",
        "service": "AOM",
        "group": "aom",
        "cli_operation": "ListServiceDiscoveryRules",
        "sdk_package": "huaweicloudsdkaom.v2",
        "sdk_client": "AomClient",
        "sdk_method": "list_service_discovery_rules",
        "request": "ListServiceDiscoveryRulesRequest",
        "rest_path": "/v1/{project_id}/inv/servicediscoveryrules",
        "result": ("list", "app_rules"),
        "name_field": "name",
        "params": ("id",),
    },
}

AOM_CATEGORIES = [k for k, v in CATEGORIES.items() if v["group"] == "aom"]

# --------------------------------------------------------------------------
# Natural-language intent routing. Ordered: the most specific phrases win.
# --------------------------------------------------------------------------
_NL_RULES = (
    ("alarm-rule-templates", ("告警规则模板", "告警模板", "alarm rule template",
                              "alarm template")),
    ("metric-or-event-alarm-rules", ("指标事件告警", "指标/事件告警", "指标告警规则",
                                     "metric or event alarm", "metric alarm rule",
                                     "event alarm rule v4")),
    ("event2alarm-rules", ("事件告警规则", "事件转告警", "event2alarm", "event to alarm")),
    ("alarm-rules", ("告警规则", "alarm rule", "alarm-rules", "alarmrule")),
    ("action-rules", ("行动规则", "action rule")),
    ("mute-rules", ("静默规则", "静默", "mute rule", "mute-rules")),
    ("dashboard-folders", ("仪表盘分组", "看板分组", "dashboard folder")),
    ("dashboards", ("仪表盘", "看板", "dashboard")),
    ("notification-templates", ("通知模板", "通知规则模板", "notification template")),
    ("prom-instances", ("prometheus 实例", "prom 实例", "prometheus instance",
                        "prom instance", "普罗米修斯实例")),
    ("access-codes", ("接入码", "access code")),
    ("service-discovery-rules", ("服务发现规则", "服务发现", "service discovery rule",
                                 "servicediscovery")),
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
# Curated mutating vocabulary. Generic verbs are intentionally narrow so that
# legitimate read phrases are never flagged.
_WRITE_INTENT_KEYWORDS = (
    # AOM writes (alarm / rule / template / dashboard / notification / prom)
    "createalarmrule", "deletealarmrule", "updatealarmrule", "addalarmrule",
    "batchupdatealarmrule", "addorupdatealarmrule", "deletealarmrules",
    "createalarmruletemplate", "deletealarmruletemplate",
    "addactionrule", "deleteactionrule", "updateactionrule",
    "addmuterules", "deletemuterules", "updatemuterules",
    "createdashboard", "deletedashboard", "deletedashboardsfolder",
    "createnotificationtemplate", "deletenotificationtemplate",
    "updatenotificationtemplate", "addservice_discovery",
    "createservicediscoveryrules", "updateservicediscoveryrules",
    "deleteservicediscoveryrules", "addmetricdata", "push_events",
    "createprominstance", "deleteprominstance", "updateprominstance",
    "createrecordingrule", "addevent2alarmrule", "deleteevent2alarmrule",
    "updateeventrule", "createsubapp", "deletesubapp", "updatesubapp",
    "createapp", "deleteapp", "updateapp",
    "createcomponent", "deletecomponent", "updatecomponent",
    "createenvironment", "deleteenvironment", "updateenvironment",
    # generic verbs
    "create", "delete", "remove", "update", "modify", "overwrite",
    "enable", "disable", "attach", "detach", "associate", "dissociate",
    "import", "upgrade", "terminate",
)
_WRITE_INTENT_ZH = (
    "创建", "删除", "移除", "修改", "更新", "启用", "停用",
    "解绑", "绑定", "批量创建", "批量删除", "批量更新", "升级", "导入",
)

# Values of these flags are read-only data (region, ids, filters, paging) and
# must NOT be scanned for the generic write vocabulary. `--query` is
# intentionally NOT stripped: the natural-language intent itself is scanned,
# and the keyword list is curated so legitimate read phrases ("查询告警规则",
# "查询服务发现规则") are never mistaken for a write.
_VALUE_STRIPPED_FLAGS = (
    "--region", "-r", "--category", "--id", "-i",
    "--name", "--limit", "--offset", "--project-id", "--filter",
    "--sort-by", "--sort-dir", "--type", "--prom-id", "--prom-type",
    "--dashboard-type", "--enterprise-project-id",
)


class AomListError(Exception):
    """Base error for the AOM name-list skill."""


class GuardError(AomListError):
    """A write intent was detected and blocked (the skill is read-only)."""


class ConfigError(AomListError):
    """hcloud missing / credentials not configured / no execution backend."""


class AuthError(AomListError):
    """Authentication or authorization failure (invalid AK/SK or IAM 403)."""


class ApiError(AomListError):
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
                "（AOM 管理面名称列表），创建/删除/修改/启停/升级等写操作已被守卫拦截。"
                % keyword)
    raw = str(text)
    for keyword in _WRITE_INTENT_ZH:
        if keyword in raw:
            raise GuardError(
                "检测到写操作意图（关键词: %s）。本 skill 为只读查询"
                "（AOM 管理面名称列表），写操作已被守卫拦截。" % keyword)
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
    return os.environ.get("AOM_HCLOUD_BIN", "hcloud")


def build_cli_command(category, region, params=None):
    """Build the `hcloud AOM <Operation> --cli-region=<region> ...` argv.

    A parameter is emitted under the name KooCLI expects: header parameters
    keep the API header casing (e.g. `enterprise_project_id` →
    `Enterprise-Project-Id`), overridable per category via `cli_param_names`;
    everything else uses the SDK snake_case field name.
    """
    spec = CATEGORIES[category]
    cli_names = spec.get("cli_param_names", {})
    argv = [spec["service"], spec["cli_operation"], "--cli-region=%s" % region]
    for key, value in (params or {}).items():
        if value is None:
            continue
        if isinstance(value, bool):
            value = "true" if value else "false"
        argv.append("--%s=%s" % (cli_names.get(key, key), value))
    return argv


def run_hcloud(argv):
    """Execute hcloud and return (stdout, stderr, returncode)."""
    cmd = [_hcloud_executable()]
    extra = os.environ.get("AOM_HCLOUD_ARGS", "").split()
    if extra:
        cmd.extend(extra)
    cmd.extend(argv)
    try:
        proc = subprocess.run(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            timeout=HCLOUD_TIMEOUT, universal_newlines=True,
        )
    except FileNotFoundError:
        raise ConfigError(
            "未找到 hcloud（KooCLI）。将回退到 huaweicloudsdkaom SDK；"
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
            "无权限访问 AOM，请检查 IAM 权限（403：AK/SK 无效或未授予只读权限），"
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
        for candidate in ("items", "data", "results", "body"):
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
    region_module = importlib.import_module(
        "huaweicloudsdkaom.v2.region.aom_region")
    return {
        "credentials": core_credentials.BasicCredentials,
        "region": core_region.Region,
        "http_config": core_http.HttpConfig,
        "client": getattr(package, spec["sdk_client"]),
        "request": getattr(package, spec["request"]),
        "region_catalog": getattr(region_module, "AomRegion"),
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
                "SDK 不可用：未安装 huaweicloudsdkcore/huaweicloudsdkaom（%s）。"
                "请运行 scripts/ensure_env.py 安装。" % exc)
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
            region_obj = loader["region"](
                region, "https://aom.%s.myhuaweicloud.com" % region)
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
_TOKEN_ENV_NAMES = ("AOM_TOKEN", "HW_AUTH_TOKEN", "HUAWEI_AUTH_TOKEN")


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
    project_id = project_id or os.environ.get("AOM_PROJECT_ID") \
        or os.environ.get("HUAWEI_PROJECT_ID")
    if not token:
        raise ConfigError(
            "REST 回退缺少认证 token（设置 AOM_TOKEN / HW_AUTH_TOKEN，"
            "或提供 AOM_PROJECT_ID）。")
    path = spec["rest_path"].replace("{project_id}", project_id or "")
    for name, value in (params or {}).items():
        path = path.replace("{%s}" % name, str(value))
    if "{" in path:
        raise ConfigError("REST 路径缺少必要参数：%s" % path)
    url = "https://aom.%s.myhuaweicloud.com%s" % (region, path)
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
    if args.filter:
        params["filter"] = args.filter
    if args.enterprise_project_id:
        params["enterprise_project_id"] = args.enterprise_project_id
    if args.type:
        params["type"] = args.type
    # category-specific id
    if args.id:
        if "id" in spec["params"]:
            params["id"] = args.id
        else:
            params["id"] = args.id
    if args.prom_id:
        params["prom_id"] = args.prom_id
    if args.prom_type:
        params["prom_type"] = args.prom_type
    # only keep params declared by the category
    params = {k: v for k, v in params.items() if k in spec["params"] and v is not None}
    # Apply per-category defaults for params the backend requires but the caller
    # may omit (e.g. KooCLI `ListPromInstance` requires Enterprise-Project-Id;
    # default it to "0" = default enterprise project) so the CLI path stays
    # viable instead of silently degrading to the SDK.
    for key, value in spec.get("default_params", {}).items():
        params.setdefault(key, value)
    return params


def _try_cli(category, region, params):
    """Attempt the KooCLI path; return (payload, "cli") or (None, None).

    A missing hcloud binary is a ConfigError and degrades to the SDK path
    (returns ``(None, None)``); an empty-but-valid response yields ``[]`` and
    still counts as a successful CLI result.
    """
    try:
        argv = build_cli_command(category, region, params)
        stdout, stderr, returncode = run_hcloud(argv)
    except ConfigError:
        return None, None
    if stdout is not None and returncode == 0 \
            and _USE_ERROR_MARKER not in (stdout + " " + stderr).lower():
        payload = extract_json(stdout)
        return _extract_list_from_payload(category, payload), "cli"
    return None, None


# IAM action / error codes that signal a per-credential read-permission gap
# rather than a genuine API failure: a valid read operation rejected because the
# active credential lacks that specific action. In that case the CLI path (a
# different credential/action surface) is retried before hard-failing.
_PERMISSION_DEGRADE_HINTS = (
    "aom:metric:list", "aom.0403", "aom.0401",
)


def _is_permission_degrade(exc):
    text = str(exc).lower()
    return any(hint in text for hint in _PERMISSION_DEGRADE_HINTS)


def query(category, region, args):
    """Run a query via CLI → SDK → REST, returning (payload, backend)."""
    spec = CATEGORIES[category]
    params = _params_from_args(args, category)
    for required in spec.get("requires", ()):
        if not params.get(required):
            raise ApiError("类别 %s 缺少必填参数 --id（%s）。" % (category, required))

    # 1) CLI (primary; per-category defaults such as ListPromInstance's
    #    Enterprise-Project-Id are filled by _params_from_args so this path
    #    is exercised for natural-language queries).
    result, backend = _try_cli(category, region, params)
    if result is not None:
        return result, backend

    # 2) SDK
    try:
        result = query_via_sdk(category, region, params)
        return result, "sdk"
    except ConfigError as exc:
        sdk_error = exc
    except AuthError as exc:
        # A 403 naming a specific IAM action (e.g. aom:metric:list) is often a
        # credential-scoped gap: retry the read-only CLI path before failing.
        if _is_permission_degrade(exc):
            result, backend = _try_cli(category, region, params)
            if result is not None:
                return result, backend
        raise
    except ApiError:
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
    "id", "alarm_rule_id", "alarm_rule_template_id", "dashboard_id",
    "folder_id", "prom_id", "access_code_id", "status", "prom_status",
    "type", "prom_type", "enable", "alarm_rule_type", "create_time",
    "created", "alarm_create_time", "update_time", "updated",
)


def render_table(rows, name_field=None):
    """Render a list of dict rows as an aligned text table.

    The category's `name_field` (when present) is shown first so the output
    reads as a *name list*.
    """
    rows = [r for r in rows if isinstance(r, dict)]
    if not rows:
        return ""
    columns = []
    if name_field and any(name_field in r for r in rows):
        columns.append(name_field)
    for key in _PREFERRED_KEYS:
        if key not in columns and any(key in r for r in rows):
            columns.append(key)
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


def print_result(category, rows, region, backend, as_json, names_only=False):
    spec = CATEGORIES[category]
    if as_json:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
        return
    if isinstance(rows, list) and not rows:
        print("Region %s 的 %s：无数据。" % (region, spec["label"]))
        return
    if names_only:
        if not isinstance(rows, list):
            rows = [rows]
        name_field = spec.get("name_field")
        printed = 0
        for row in rows:
            if isinstance(row, dict) and name_field and row.get(name_field) is not None:
                print(_cell(row.get(name_field)))
                printed += 1
        if printed == 0:
            print("Region %s 的 %s：无可显示的“名称”字段（%s）。"
                  % (region, spec["label"], name_field))
        return
    if isinstance(rows, list):
        print("Region %s 的 %s（共 %d 条，backend=%s）："
              % (region, spec["label"], len(rows), backend))
        table = render_table(rows, spec.get("name_field"))
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
        print("%-28s %-24s %s %s" % (key, spec["label"],
                                     spec["service"], spec["cli_operation"]))


# --------------------------------------------------------------------------
# Entry point
# --------------------------------------------------------------------------
def build_parser():
    parser = argparse.ArgumentParser(
        description="查询华为云 AOM（应用运维管理）资源名称列表（只读，自然语言可触发）。")
    parser.add_argument("-q", "--query", help="自然语言查询意图，自动路由到某个查询类别")
    parser.add_argument("--category", choices=sorted(CATEGORIES),
                        help="直接指定查询类别（与 --query 二选一）")
    parser.add_argument("-r", "--region", default=DEFAULT_REGION,
                        help="目标 Region（默认 %s）" % DEFAULT_REGION)
    parser.add_argument("--project-id", dest="project_id", default=None,
                        help="项目 ID（REST 回退需要）")
    parser.add_argument("--json", action="store_true", dest="as_json",
                        help="以 JSON 输出完整字段")
    parser.add_argument("--names-only", action="store_true", dest="names_only",
                        help="仅输出资源名称（每行一个）")
    parser.add_argument("--id", "-i", default=None,
                        help="资源 ID（按类别解释：告警模板/服务发现规则等）")
    parser.add_argument("--name", default=None, help="按名称过滤（服务端参数）")
    parser.add_argument("--type", default=None, help="按类型过滤（服务端参数）")
    parser.add_argument("--prom-id", dest="prom_id", default=None,
                        help="Prometheus 实例 ID 过滤")
    parser.add_argument("--prom-type", dest="prom_type", default=None,
                        help="Prometheus 实例类型过滤")
    parser.add_argument("--enterprise-project-id", dest="enterprise_project_id",
                        default=None, help="企业项目 ID 过滤")
    parser.add_argument("--filter", default=None, help="额外过滤表达式（透传）")
    parser.add_argument("--limit", type=int, default=None,
                        help="分页大小（仅部分类别支持）")
    parser.add_argument("--offset", type=int, default=None,
                        help="分页偏移（仅部分类别支持）")
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
    except AomListError as exc:
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

    if args.project_id:
        os.environ["AOM_PROJECT_ID"] = args.project_id

    try:
        guard_operation(category, args.operation)
        rows_or_obj, backend = query(category, args.region, args)
    except AomListError as exc:
        print("[错误] %s" % exc, file=sys.stderr)
        return 1

    print_result(category, rows_or_obj, args.region, backend, args.as_json,
                 args.names_only)
    return 0


if __name__ == "__main__":
    sys.exit(main())