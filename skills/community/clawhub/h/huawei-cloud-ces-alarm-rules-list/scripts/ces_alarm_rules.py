#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""盘点华为云 CES（云监控）告警规则列表，并可查询单条规则的详情（只读）。

主路径（KooCLI）：

- ``ListAlarmRules`` —— 告警规则列表
  （``GET /v2/{project_id}/alarms``，实测于 ``huaweicloudsdkces`` v2 的
  ``_list_alarm_rules_http_info`` 与 KooCLI 的 ListAlarmRules 帮助参数清单；
  注意接口路径是 ``/alarms``，不是 ``/alarm-rules``）。
- ``ListAlarmRulePolicies`` —— 单条规则的阈值策略
  （``GET /v2/{project_id}/alarms/{alarm_id}/policies``）。
- ``ListAlarmRuleResources`` —— 单条规则关联的资源
  （``GET /v2/{project_id}/alarms/{alarm_id}/resources``）。
- ``ListAlarms`` —— v1 告警列表，**仅用于补齐告警状态** ``alarm_state``
  （``GET /V1.0/{project_id}/alarms``；v2 ListAlarmRules 的响应不含状态字段）。

hcloud 缺失时回退到官方 SDK ``huaweicloudsdkces``（v2 列表/策略/资源，v1 状态）。

输出形态：
- 默认：仅规则名称列表（每行一条）。
- ``--table``：规则ID / 名称 / 资源类型 / 监控维度 / 指标 / 阈值与比较符 /
  告警级别 / 当前状态 / 是否启用 / 通知方式。
- ``--json``：接口原始结构（不做字段改写）。

只读保证：写意图守卫在解析参数之后、任何命令执行之前拦截
create/update/delete/enable/disable/batch-/add/remove 等意图，退出码 1。

用法：
    python3 scripts/ces_alarm_rules.py [--region cn-north-4]
                                       [--name <子串>]
                                       [--alarm-level 1,2]
                                       [--alarm-state ok,alarm]
                                       [--resource-type SYS.ECS]
                                       [--limit 50] [--offset 0] [--max-pages 100]
                                       [--table | --json]
    python3 scripts/ces_alarm_rules.py --rule-id alxxxxxxxxxxxxxxxxxxxxxx [--json|--table]

环境变量（主要用于离线自测与降级）：
    CES_ALARM_HCLOUD_BIN   hcloud 可执行文件（默认 "hcloud"）
    CES_ALARM_HCLOUD_ARGS  追加到只读参数之后的额外参数（同样受写意图守卫扫描）
    CES_ALARM_SQC_BIN      skill-quality-cli 可执行文件覆盖
    CES_ALARM_PROJECT_ID   SDK 回退所需 project id
"""

import argparse
import importlib
import json
import os
import re
import shutil
import subprocess
import sys

# 交付物保持干净：不生成 __pycache__/*.pyc。
sys.dont_write_bytecode = True

DEFAULT_REGION = "cn-north-4"
DEFAULT_PAGE_SIZE = 50
MAX_PAGE_SIZE = 100
SERVICE = "CES"

# 本 skill 允许构造的只读操作。
OPERATION_LIST = "ListAlarmRules"
OPERATION_POLICIES = "ListAlarmRulePolicies"
OPERATION_RESOURCES = "ListAlarmRuleResources"
OPERATION_STATE = "ListAlarms"
ALLOWED_OPERATIONS = (
    OPERATION_LIST,
    OPERATION_POLICIES,
    OPERATION_RESOURCES,
    OPERATION_STATE,
)

# 官方 REST 路径（实测：huaweicloudsdkces v2/v1 的 *_http_info resource_path）。
REST_PATHS = {
    OPERATION_LIST: "/v2/{project_id}/alarms",
    OPERATION_POLICIES: "/v2/{project_id}/alarms/{alarm_id}/policies",
    OPERATION_RESOURCES: "/v2/{project_id}/alarms/{alarm_id}/resources",
    OPERATION_STATE: "/V1.0/{project_id}/alarms",
}

# 响应中的列表容器键。
CONTAINER_KEYS = {
    OPERATION_LIST: ("alarms",),
    OPERATION_POLICIES: ("policies",),
    OPERATION_RESOURCES: ("resources",),
    OPERATION_STATE: ("metric_alarms",),
}

SKILL_NAME = "huawei-cloud-ces-alarm-rules-list"
SKILL_QUALITY_SKILL_NAME = SKILL_NAME
_QUALITY_OFF_VALUES = ("0", "false", "no", "off")

_FIELD_MISSING = "-"

# 表格列（顺序即验收口径）。
TABLE_COLUMNS = [
    "规则ID",
    "名称",
    "资源类型",
    "监控维度",
    "指标",
    "阈值与比较符",
    "告警级别",
    "当前状态",
    "是否启用",
    "通知方式",
]

# 告警级别：1 紧急 ~ 4 提示。
LEVEL_NAMES = {
    1: "紧急",
    2: "重要",
    3: "次要",
    4: "提示",
}

# 告警状态（v1 alarm_state）→ 中文；数据不足必须独立标注，不得与正常混同。
STATE_NAMES = {
    "ok": "正常",
    "alarm": "告警",
    "insufficient_data": "数据不足",
    "invalid": "无效",
}
_STATE_ALIASES = {
    "ok": "ok",
    "正常": "ok",
    "alarm": "alarm",
    "告警": "alarm",
    "insufficient_data": "insufficient_data",
    "insufficientdata": "insufficient_data",
    "数据不足": "insufficient_data",
    "invalid": "invalid",
    "无效": "invalid",
}
STATE_UNKNOWN = "未知"

# 变更意图关键词（守卫严格拒绝）。
WRITE_INTENT_KEYWORDS = (
    "createalarmrules",
    "createalarm",
    "updatealarmrulepolicies",
    "updatealarm",
    "updatealarmaction",
    "updatealarmnotifications",
    "deletealarm",
    "batchdeletealarmrules",
    "batchenablealarmrules",
    "addalarmruleresources",
    "deletealarmruleresources",
    "createoneclickalarm",
    "batchupdateoneclickalarms",
    "batchupdateoneclickalarmpolicies",
    "create",
    "update",
    "delete",
    "modify",
    "enable",
    "disable",
    "batch",
    "add",
    "remove",
)

# 只读参数取值不做写意图扫描（名称 / 路径 / region 等纯数据）。
_VALUE_STRIPPED_FLAGS = (
    "--region",
    "-r",
    "--name",
    "--rule-id",
    "--alarm-id",
    "--alarm-level",
    "--alarm-state",
    "--resource-type",
    "--limit",
    "--offset",
    "--max-pages",
)

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
_PROJECT_ENV_NAMES = (
    "CES_ALARM_PROJECT_ID",
    "HUAWEICLOUD_SDK_PROJECT_ID",
    "HUAWEI_PROJECT_ID",
    "HW_PROJECT_ID",
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
    "insufficient permission",
    "no permission",
    "ces:alarm",
    "认证失败",
    "权限不足",
)

# KooCLI 用法错误以 [USE_ERROR] 打印在 stdout 上（退出码可能为 0）。
_USE_ERROR_MARKER = "[use_error]"


class AlarmRulesError(Exception):
    """本 skill 的基类异常。"""


class GuardError(AlarmRulesError):
    """检测到写操作意图（本 skill 只读）。"""


class ConfigError(AlarmRulesError):
    """hcloud/SDK 缺失或凭据未配置。"""


class AuthError(AlarmRulesError):
    """认证/鉴权失败（AK/SK 无效或 IAM 403）。"""


class ApiError(AlarmRulesError):
    """hcloud / SDK / 网络 / 响应异常。"""


# ---------------------------------------------------------------------------
# 写意图守卫
# ---------------------------------------------------------------------------

def guard_write_intent(text):
    """文本命中变更意图则抛 GuardError。

    归一化分隔符，使 ``--enable-alarm``、``BatchEnableAlarmRules``、
    ``enable_alarm`` 命中同一个关键词。只读词汇（list/show/count）不会命中。
    """
    low = re.sub(r"[\s_\-]+", "", str(text).lower())
    for keyword in WRITE_INTENT_KEYWORDS:
        if keyword in low:
            raise GuardError(
                "检测到写操作意图（关键词: %s）。本 skill 仅支持 CES 告警规则只读盘点"
                "（ListAlarmRules / ListAlarmRulePolicies / ListAlarmRuleResources），"
                "创建/更新/删除/启用/停用/批量/绑定/解绑等变更操作已被守卫拦截，"
                "未执行任何命令。" % keyword
            )
    return False


def guard_operation(operation):
    """只允许四个只读操作。"""
    if operation not in ALLOWED_OPERATIONS:
        raise GuardError(
            "不允许的操作 %r：本 skill 仅允许只读操作 %s。"
            % (operation, "/".join(ALLOWED_OPERATIONS))
        )
    return True


def guard_text_from_argv(argv):
    """构造守卫要扫描的文本：扫描旗标名，剔除只读取值类旗标的取值。"""
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


# ---------------------------------------------------------------------------
# 参数 → hcloud 命令
# ---------------------------------------------------------------------------

def build_command(operation, region, alarm_id=None, name=None, namespace=None,
                  resource_id=None, enterprise_project_id=None,
                  product_name=None, resource_level=None,
                  limit=DEFAULT_PAGE_SIZE, offset=None, start=None, order=None):
    """构造 hcloud CES 的只读参数（不含可执行文件）。"""
    argv = [SERVICE, operation, "--cli-region=%s" % region]
    if operation == OPERATION_LIST:
        if alarm_id:
            argv.append("--alarm_id=%s" % alarm_id)
        if name:
            argv.append("--name=%s" % name)
        if namespace:
            argv.append("--namespace=%s" % namespace)
        if resource_id:
            argv.append("--resource_id=%s" % resource_id)
        if enterprise_project_id:
            argv.append("--enterprise_project_id=%s" % enterprise_project_id)
        if product_name:
            argv.append("--product_name=%s" % product_name)
        if resource_level:
            argv.append("--resource_level=%s" % resource_level)
        if limit is not None:
            argv.append("--limit=%d" % limit)
        if offset is not None:
            argv.append("--offset=%d" % offset)
    elif operation in (OPERATION_POLICIES, OPERATION_RESOURCES):
        argv.append("--alarm_id=%s" % alarm_id)
        if limit is not None:
            argv.append("--limit=%d" % limit)
        if offset is not None:
            argv.append("--offset=%d" % offset)
    elif operation == OPERATION_STATE:
        if start:
            argv.append("--start=%s" % start)
        if limit is not None:
            argv.append("--limit=%d" % limit)
        if order:
            argv.append("--order=%s" % order)
        if enterprise_project_id:
            argv.append("--enterprise_project_id=%s" % enterprise_project_id)
    return argv


def _hcloud_executable():
    return os.environ.get("CES_ALARM_HCLOUD_BIN") or "hcloud"


def _hcloud_resolvable():
    """hcloud 是否真的能启动（用于决定是否套 skill-quality-cli）。"""
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
    override = os.environ.get("CES_ALARM_SQC_BIN")
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
    extra = os.environ.get("CES_ALARM_HCLOUD_ARGS", "").split()
    if extra:
        cmd.extend(extra)
    return cmd


def build_hcloud_command(argv):
    """构造 hcloud 执行命令，按规范用 skill-quality-cli 包裹。

    遥测 CLI 缺失或 ``SKILL_QUALITY_REPORT=0`` 时降级为裸 hcloud；
    显式 ``CES_ALARM_HCLOUD_BIN``（离线 mock）直接执行。
    """
    hcloud_cmd = _hcloud_argv(argv)
    if os.environ.get("CES_ALARM_HCLOUD_BIN"):
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
    """执行 hcloud（经 skill-quality-cli 包裹），返回 (stdout, stderr, rc)。"""
    extra = os.environ.get("CES_ALARM_HCLOUD_ARGS", "").split()
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


# ---------------------------------------------------------------------------
# 响应解析与错误分类
# ---------------------------------------------------------------------------

def extract_json(stdout):
    """解析 hcloud 输出；容忍前后噪声行。"""
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
        raise ApiError("hcloud 输出无法解析为 JSON：%s" % text[:200])


def _payload_error(payload):
    """响应体是错误信封时返回错误文本（KooCLI 可能 rc=0 打印错误体）。"""
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
        return ("%s %s" % (payload.get("error_code"),
                           payload.get("error_msg"))).strip()
    for key in ("errorCode", "errorMsg", "error_message"):
        if payload.get(key):
            return str(payload[key])
    return None


def classify_hcloud_failure(stdout, stderr, returncode):
    """把失败的 hcloud 调用映射为带明确提示的领域异常。"""
    blob = ((stderr or "") + " " + (stdout or "")).strip()
    low = blob.lower()
    if any(p in low for p in _CREDENTIAL_MISSING_PATTERNS) and not re.search(
            r"\b40[13]\b", blob):
        return ConfigError(
            "缺少 AK/SK 凭据：hcloud 未配置有效凭证。请在会话外完成认证配置"
            "（hcloud configure 或凭证环境变量），严禁在对话中粘贴 AK/SK，"
            "参见 references/cli-installation-guide.md。详情：%s" % blob[:300]
        )
    if _USE_ERROR_MARKER in low:
        return ApiError(
            "hcloud 参数错误（KooCLI 拒绝了该参数组合，退出码 %s）：请用 "
            "`hcloud CES <Operation> --cli-region=<region> --help` 核对真实参数"
            "（ListAlarmRules: alarm_id/name/namespace/resource_id/"
            "enterprise_project_id/product_name/resource_level/limit/offset；"
            "ListAlarms: start/limit/order/enterprise_project_id）。"
            "原文关键行：%s" % (returncode, blob[:300])
        )
    if any(p in low for p in _AUTH_PATTERNS):
        return AuthError(
            "无权限访问 CES 告警规则，请检查 IAM 权限"
            "（403：AK/SK 无效，或缺少 ces:alarms:list / ces:alarms:getPolicies /"
            " ces:alarms:getResources 最小授权），"
            "参见 references/iam-policies.md。详情：%s" % blob[:300]
        )
    return ApiError("hcloud 调用失败（退出码 %s）：%s" % (returncode, blob[:300]))


def extract_items(payload, operation):
    """从响应中取出列表字段。"""
    keys = CONTAINER_KEYS.get(operation, ())
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        for key in keys:
            value = payload.get(key)
            if isinstance(value, list):
                return value
    return []


def _int_or_none(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _sdk_call(fn, request):
    try:
        return fn(request)
    except Exception as exc:
        low = str(exc).lower()
        if any(p in low for p in _AUTH_PATTERNS):
            raise AuthError(
                "无权限访问 CES 告警规则，请检查 IAM 权限（403）。详情：%s"
                % str(exc)[:300]
            )
        raise ApiError("SDK 调用失败：%s" % str(exc)[:300])


def _jsonable(value):
    return json.loads(json.dumps(value, ensure_ascii=False, default=str))


# ---------------------------------------------------------------------------
# SDK 回退
# ---------------------------------------------------------------------------

def _env_value(names):
    for name in names:
        value = os.environ.get(name)
        if value:
            return value
    return None


def _load_sdk():
    """导入 SDK 回退所需的符号（可注入替换以便离线测试）。"""
    try:
        core_credentials = importlib.import_module(
            "huaweicloudsdkcore.auth.credentials")
        core_region = importlib.import_module("huaweicloudsdkcore.region.region")
        core_http = importlib.import_module("huaweicloudsdkcore.http.http_config")
        v1 = importlib.import_module("huaweicloudsdkces.v1")
        v2 = importlib.import_module("huaweicloudsdkces.v2")
        v2_region = importlib.import_module("huaweicloudsdkces.v2.region.ces_region")
        v1_region = importlib.import_module("huaweicloudsdkces.v1.region.ces_region")
    except ImportError as exc:
        raise ConfigError(
            "未找到 hcloud（KooCLI），且 huaweicloudsdkcore/huaweicloudsdkces 未安装，"
            "无法回退到 SDK。请安装 KooCLI 或先运行 `python3 scripts/ensure_env.py`。"
            "详情：%s" % exc
        )
    return {
        "client_v2": v2.CesClient,
        "client_v1": v1.CesClient,
        "region_v2": getattr(v2_region, "CesRegion", None),
        "region_v1": getattr(v1_region, "CesRegion", None),
        "region_class": core_region.Region,
        "credentials": core_credentials.BasicCredentials,
        "http_config": core_http.HttpConfig,
        "requests": {
            OPERATION_LIST: v2.ListAlarmRulesRequest,
            OPERATION_POLICIES: v2.ListAlarmRulePoliciesRequest,
            OPERATION_RESOURCES: v2.ListAlarmRuleResourcesRequest,
            OPERATION_STATE: v1.ListAlarmsRequest,
        },
    }


def query_via_sdk(operation, region, params, loader=None):
    """通过官方 SDK 查询一个只读操作，返回 (payload_dict, items)。

    ``loader`` 可注入，供离线测试使用。
    """
    if loader is None:
        loader = _load_sdk()
    ak = _env_value(_AK_ENV_NAMES)
    sk = _env_value(_SK_ENV_NAMES)
    project_id = _env_value(_PROJECT_ENV_NAMES)
    if not ak or not sk:
        raise ConfigError(
            "SDK 回退缺少 AK/SK 凭证：官方 SDK 的 BasicCredentials 不会自动读取环境"
            "变量，且未检测到白名单中的 AK/SK 环境变量（HUAWEICLOUD_SDK_AK /"
            " HUAWEI_ACCESS_KEY 与 HUAWEICLOUD_SDK_SK / HUAWEI_SECRET_KEY）。"
            "请在会话外设置（严禁在对话中粘贴 AK/SK），参见"
            " references/cli-installation-guide.md。"
        )
    if not project_id:
        raise ConfigError(
            "SDK 回退缺少 project id：CES 是项目级服务，SDK 请求路径需要"
            " /v2/{project_id}/...。请在会话外设置 CES_ALARM_PROJECT_ID（或"
            " HUAWEICLOUD_SDK_PROJECT_ID / HUAWEI_PROJECT_ID），或改用 KooCLI"
            "（hcloud 会自动解析 project id）。"
        )
    credentials = loader["credentials"](ak=ak, sk=sk, project_id=project_id)
    catalog = loader.get("region_v2") if operation != OPERATION_STATE else loader.get("region_v1")
    try:
        try:
            region_obj = catalog.value_of(region)
        except Exception:
            region_obj = loader["region_class"](
                region, "https://ces.%s.myhuaweicloud.com" % region)
        client_class = (loader["client_v2"] if operation != OPERATION_STATE
                        else loader["client_v1"])
        client = client_class.new_builder() \
            .with_credentials(credentials) \
            .with_region(region_obj) \
            .with_http_config(loader["http_config"].get_default_config()) \
            .build()
    except AlarmRulesError:
        raise
    except Exception as exc:
        raise ConfigError("SDK 初始化失败（region=%s）：%s" % (region, exc))

    method = {
        OPERATION_LIST: "list_alarm_rules",
        OPERATION_POLICIES: "list_alarm_rule_policies",
        OPERATION_RESOURCES: "list_alarm_rule_resources",
        OPERATION_STATE: "list_alarms",
    }[operation]
    request = loader["requests"][operation](**params)
    response = _sdk_call(getattr(client, method), request)
    payload = _jsonable(response.to_dict())
    return payload, extract_items(payload, operation)


# ---------------------------------------------------------------------------
# 查询（CLI → SDK 回退）
# ---------------------------------------------------------------------------

def _call_hcloud(operation, region, params, offset=None):
    """执行一次 hcloud 只读调用，返回解析后的 payload。"""
    argv = build_command(operation, region, offset=offset, **params)
    try:
        stdout, stderr, returncode = run_hcloud(argv)
    except ConfigError:
        raise
    if returncode != 0 or _USE_ERROR_MARKER in (stdout + " " + stderr).lower():
        raise classify_hcloud_failure(stdout, stderr, returncode)
    payload = extract_json(stdout)
    err_text = _payload_error(payload)
    if err_text:
        raise classify_hcloud_failure("", err_text, returncode)
    return payload


def _query_page(operation, region, params, offset):
    """查询一页：CLI 优先，hcloud 缺失时回退 SDK。"""
    try:
        payload = _call_hcloud(operation, region, params, offset=offset)
        return payload, extract_items(payload, operation)
    except ConfigError as exc:
        if not _is_missing_hcloud(exc):
            raise
    sdk_params = dict(params)
    if offset is not None:
        sdk_params["offset"] = offset
    payload, items = query_via_sdk(operation, region,
                                   _prune_sdk_params(operation, sdk_params))
    return payload, items


def _is_missing_hcloud(exc):
    text = str(exc)
    return "未找到 hcloud" in text or "无法回退到 SDK" in text


def _prune_sdk_params(operation, params):
    """SDK 请求模型不支持的参数去掉（region 等不进 request）。"""
    allowed = {
        OPERATION_LIST: ("alarm_id", "name", "namespace", "resource_id",
                         "enterprise_project_id", "product_name",
                         "resource_level", "offset", "limit"),
        OPERATION_POLICIES: ("alarm_id", "offset", "limit"),
        OPERATION_RESOURCES: ("alarm_id", "offset", "limit"),
        OPERATION_STATE: ("start", "limit", "order", "enterprise_project_id"),
    }[operation]
    return {k: v for k, v in params.items() if k in allowed and v is not None}


def _collect_alarm_rules(region, name, limit, offset, max_pages):
    items = []
    current = offset
    for _page in range(max(1, max_pages)):
        params = {"name": name, "limit": limit}
        payload, batch = _query_page(OPERATION_LIST, region, params, current)
        items.extend(batch)
        total = _int_or_none((payload or {}).get("count")) if isinstance(payload, dict) else None
        if not batch or len(batch) < limit:
            break
        if total is not None and len(items) >= total:
            break
        current += limit
    else:
        raise ApiError("翻页超过 %d 页仍未取完，已中止以防死循环（可用 --max-pages 调整）。"
                       % max_pages)
    return items


def list_alarm_rules(region, name=None, limit=DEFAULT_PAGE_SIZE, offset=0,
                     max_pages=100):
    """翻页取全量告警规则（ListAlarmRules，offset 翻页）。

    ``--name`` 先按服务端 ``name`` 透传查询；服务端是精确匹配语义，若透传后一条都没有，
    再去掉该参数重取一次并在客户端做模糊过滤——否则 ``--name cpu`` 这类子串查询会被
    服务端静默过滤成空列表。
    """
    items = _collect_alarm_rules(region, name, limit, offset, max_pages)
    if name and not items:
        items = _collect_alarm_rules(region, None, limit, offset, max_pages)
    return items


def fetch_alarm_state_map(region, enterprise_project_id=None,
                          limit=DEFAULT_PAGE_SIZE, max_pages=100):
    """通过 v1 ListAlarms 逐页补齐 alarm_id → alarm_state 映射。

    v2 ListAlarmRules 的响应不含状态字段，状态只能从 v1 列表补齐；
    这是只读操作，且失败时由调用方决定降级还是报错。
    """
    states = {}
    start = None
    for _page in range(max(1, max_pages)):
        params = {
            "limit": limit,
            "order": "asc",
            "enterprise_project_id": enterprise_project_id,
            "start": start,
        }
        try:
            payload = _call_hcloud(OPERATION_STATE, region, params)
            batch = extract_items(payload, OPERATION_STATE)
        except ConfigError as exc:
            if not _is_missing_hcloud(exc):
                raise
            payload, batch = query_via_sdk(
                OPERATION_STATE, region,
                _prune_sdk_params(OPERATION_STATE, params))
        added = 0
        for record in batch:
            alarm_id = record.get("alarm_id") if isinstance(record, dict) else None
            if alarm_id and alarm_id not in states:
                states[alarm_id] = str(record.get("alarm_state") or "")
                added += 1
        if not batch or len(batch) < limit:
            break
        last = batch[-1].get("alarm_id") if isinstance(batch[-1], dict) else None
        # 接口对 start 的边界语义（是否包含该 id）各区域不一致：没有新增就停，防死循环。
        if not last or last == start or added == 0:
            break
        start = last
    else:
        raise ApiError("补齐告警状态时翻页超过 %d 页仍未取完，已中止。" % max_pages)
    return states


# ---------------------------------------------------------------------------
# 归一化 / 过滤 / 渲染
# ---------------------------------------------------------------------------

def _first(record, *keys, default=_FIELD_MISSING):
    for key in keys:
        if isinstance(record, dict) and record.get(key) not in (None, ""):
            return record[key]
    return default


def _as_list(value):
    return value if isinstance(value, list) else []


def level_name(level):
    try:
        return LEVEL_NAMES.get(int(level), str(level))
    except (TypeError, ValueError):
        return _FIELD_MISSING


def state_name(state):
    """告警状态 → 中文；数据不足独立标注。"""
    if not state:
        return STATE_UNKNOWN
    key = str(state).strip().lower()
    return STATE_NAMES.get(_STATE_ALIASES.get(key, key), str(state))


def format_threshold(policy):
    """把一条策略渲染成「比较符 + 阈值 + 连续次数/周期」文本。"""
    if not isinstance(policy, dict):
        return _FIELD_MISSING
    operator = str(policy.get("comparison_operator") or "").strip()
    unit = str(policy.get("unit") or "").strip()
    value = policy.get("value")
    parts = []
    hierarchical = policy.get("hierarchical_value")
    # 实测：分级阈值规则同时返回 value 与 hierarchical_value，此时只展示分级阈值，
    # 避免同一阈值被打印两次。
    has_hierarchical = isinstance(hierarchical, dict) and bool(
        [v for v in hierarchical.values() if v not in (None, "")])
    if value is not None and value != "" and not has_hierarchical:
        parts.append("%s%s%s" % (operator, value, unit))
    if has_hierarchical:
        levels = [
            ("critical", "紧急"),
            ("major", "重要"),
            ("minor", "次要"),
            ("info", "提示"),
        ]
        detail = []
        for key, label in levels:
            level_value = hierarchical.get(key)
            if level_value not in (None, ""):
                detail.append("%s%s%s" % (label, operator, level_value))
        if detail:
            parts.append("分级阈值: " + "/".join(detail))
    if not parts:
        return _FIELD_MISSING
    text = parts[0]
    count = _int_or_none(policy.get("count"))
    period = _int_or_none(policy.get("period"))
    extra = []
    if count and count > 1:
        extra.append("连续 %d 次" % count)
    if period:
        # 实测：v2 policies[].period 的单位是秒（如 300 = 5 分钟）
        extra.append("周期 %d 秒" % period)
    if extra:
        text += "（%s）" % "，".join(extra)
    return text


def _format_dimension(dimension):
    """维度渲染为 name=value；列表视图常只返回 name，此时只显示 name。"""
    name = str(dimension.get("name") or "").strip()
    value = str(dimension.get("value") or "").strip()
    if name and value:
        return "%s=%s" % (name, value)
    return name or _FIELD_MISSING


def _normalize_resource_groups(raw):
    """统一 ListAlarmRuleResources 的资源结构。

    实测：详情接口的 ``resources`` 是**二维**结构
    （``list[list[DimensionResp]]``，每个内层数组是一组维度），而列表接口
    ``ListAlarmRules`` 的 ``resources`` 是 ``[{resource_group_id, resource_group_name,
    dimensions[]}]``。两种形态在这里归一化为「资源组 → 维度列表」。
    """
    groups = []
    for item in _as_list(raw):
        if isinstance(item, dict):
            dims = item.get("dimensions")
            if not isinstance(dims, list):
                dims = [item] if (item.get("name") or item.get("value")) else []
            group = dict(item)
            group["dimensions"] = [d for d in dims if isinstance(d, dict)]
            groups.append(group)
        elif isinstance(item, list):
            groups.append({"dimensions": [d for d in item if isinstance(d, dict)]})
    return groups


def rule_row(rule, state_map=None):
    """把一条 v2 告警规则归一化为表格行（列名即验收口径）。"""
    policies = [p for p in _as_list(rule.get("policies")) if isinstance(p, dict)]
    resources = [r for r in _as_list(rule.get("resources")) if isinstance(r, dict)]

    metrics = []
    for policy in policies:
        metric = str(policy.get("metric_name") or "").strip()
        if metric and metric not in metrics:
            metrics.append(metric)

    dimensions = []
    for policy in policies:
        dim = str(policy.get("dimension_name") or "").strip()
        if dim and dim not in dimensions:
            dimensions.append(dim)
    if not dimensions:
        for resource in resources:
            for dimension in _as_list(resource.get("dimensions")):
                if isinstance(dimension, dict):
                    name = str(dimension.get("name") or "").strip()
                    if name and name not in dimensions:
                        dimensions.append(name)

    levels = []
    for policy in policies:
        name = level_name(policy.get("level"))
        if name != _FIELD_MISSING and name not in levels:
            levels.append(name)

    thresholds = []
    for policy in policies:
        text = format_threshold(policy)
        if text != _FIELD_MISSING and text not in thresholds:
            thresholds.append(text)

    resource_type = _first(rule, "namespace", "product_name")
    if rule.get("resource_level") == "product" and resource_type != _FIELD_MISSING:
        resource_type = "%s（云产品级）" % resource_type

    notifications = rule.get("alarm_notifications")
    if rule.get("notification_enabled") is False:
        notify_text = "未开启通知"
    else:
        types = []
        for item in _as_list(notifications):
            if isinstance(item, dict):
                ntype = str(item.get("type") or "").strip()
                if ntype and ntype not in types:
                    types.append(ntype)
        notify_text = ", ".join(types) if types else _FIELD_MISSING

    alarm_id = _first(rule, "alarm_id")
    state = (state_map or {}).get(alarm_id)

    return {
        "规则ID": alarm_id,
        "名称": _first(rule, "name"),
        "资源类型": resource_type,
        "监控维度": ", ".join(dimensions) if dimensions else _FIELD_MISSING,
        "指标": ", ".join(metrics) if metrics else _FIELD_MISSING,
        "阈值与比较符": "；".join(thresholds) if thresholds else _FIELD_MISSING,
        "告警级别": "/".join(levels) if levels else _FIELD_MISSING,
        "当前状态": state_name(state),
        "是否启用": "启用" if rule.get("enabled") is True else (
            "停用" if rule.get("enabled") is False else _FIELD_MISSING),
        "通知方式": notify_text,
    }


def parse_level_filter(raw_values):
    """解析 --alarm-level：支持 1/2/3/4 与 紧急/重要/次要/提示 的中英文写法。"""
    levels = set()
    for raw in raw_values or []:
        for token in str(raw).replace("，", ",").split(","):
            token = token.strip()
            if not token:
                continue
            if token.isdigit() and int(token) in LEVEL_NAMES:
                levels.add(int(token))
                continue
            matched = False
            for number, name in LEVEL_NAMES.items():
                if token == name:
                    levels.add(number)
                    matched = True
                    break
            if not matched:
                raise ApiError(
                    "--alarm-level 只接受 1~4（1 紧急 / 2 重要 / 3 次要 / 4 提示）"
                    "或其对应中文名，收到：%s" % token)
    return levels


def parse_state_filter(raw_values):
    """解析 --alarm-state：ok / alarm / insufficient_data / invalid 及中文别名。"""
    states = set()
    for raw in raw_values or []:
        for token in str(raw).replace("，", ",").split(","):
            token = token.strip().lower()
            if not token:
                continue
            mapped = _STATE_ALIASES.get(token)
            if not mapped:
                raise ApiError(
                    "--alarm-state 只接受 ok / alarm / insufficient_data / invalid"
                    "（或其中文名 正常 / 告警 / 数据不足 / 无效），收到：%s" % token)
            states.add(mapped)
    return states


def filter_rules(rules, state_map=None, name=None, levels=None, states=None,
                 resource_type=None):
    """客户端过滤（KooCLI 7.3.12 的 ListAlarmRules 没有这三个 query 参数）。"""
    result = []
    needle = (name or "").strip().lower()
    resource_needle = (resource_type or "").strip().lower()
    for rule in rules:
        if not isinstance(rule, dict):
            continue
        if needle:
            rule_name = str(rule.get("name") or "").lower()
            rule_id = str(rule.get("alarm_id") or "").lower()
            if needle not in rule_name and needle not in rule_id:
                continue
        if levels:
            rule_levels = set()
            for policy in _as_list(rule.get("policies")):
                if isinstance(policy, dict):
                    level = _int_or_none(policy.get("level"))
                    if level is not None:
                        rule_levels.add(level)
            if not (rule_levels & levels):
                continue
        if states:
            current = str((state_map or {}).get(rule.get("alarm_id")) or "").lower()
            current = _STATE_ALIASES.get(current, current)
            if current not in states:
                continue
        if resource_needle:
            haystack = []
            for key in ("namespace", "product_name", "type"):
                value = rule.get(key)
                if value:
                    haystack.append(str(value).lower())
            for resource in _as_list(rule.get("resources")):
                if isinstance(resource, dict):
                    if resource.get("resource_group_name"):
                        haystack.append(str(resource["resource_group_name"]).lower())
                    for dimension in _as_list(resource.get("dimensions")):
                        if isinstance(dimension, dict):
                            haystack.append(str(dimension.get("name") or "").lower())
            for policy in _as_list(rule.get("policies")):
                if isinstance(policy, dict) and policy.get("namespace"):
                    haystack.append(str(policy["namespace"]).lower())
            if not any(resource_needle in item for item in haystack):
                continue
        result.append(rule)
    return result


def _cell(value):
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    if value is None or value == "":
        return _FIELD_MISSING
    return str(value)


def render_table(rows, columns):
    """按给定列渲染对齐表格。"""
    rows_data = list(rows)
    if not rows_data:
        return "（无数据）"
    body = [[_cell(row.get(col)) for col in columns] for row in rows_data]
    widths = [max(len(col), *(len(item[i]) for item in body))
              for i, col in enumerate(columns)]
    header = "  ".join(col.ljust(widths[i]) for i, col in enumerate(columns))
    separator = "  ".join("-" * w for w in widths)
    lines = [header, separator]
    for item in body:
        lines.append("  ".join(item[i].ljust(widths[i]) for i in range(len(columns))))
    return "\n".join(lines)


def render_name_list(rules):
    names = [_cell(rule.get("name")) for rule in rules if isinstance(rule, dict)]
    return "\n".join(names) if names else ""


def _notification_lines(rule):
    lines = []
    alarm = _as_list(rule.get("alarm_notifications"))
    if alarm:
        parts = []
        for item in alarm:
            if isinstance(item, dict):
                targets = _as_list(item.get("notification_list"))
                parts.append("%s（%d 个通知对象）"
                             % (item.get("type") or _FIELD_MISSING, len(targets)))
        lines.append("  告警通知：" + ("，".join(parts) if parts else _FIELD_MISSING))
    ok_items = _as_list(rule.get("ok_notifications"))
    if ok_items:
        parts = []
        for item in ok_items:
            if isinstance(item, dict):
                targets = _as_list(item.get("notification_list"))
                parts.append("%s（%d 个通知对象）"
                             % (item.get("type") or _FIELD_MISSING, len(targets)))
        lines.append("  恢复通知：" + ("，".join(parts) if parts else _FIELD_MISSING))
    if not lines:
        lines.append("  通知对象：%s" % (
            "未开启通知" if rule.get("notification_enabled") is False else _FIELD_MISSING))
    return lines


def render_detail(rule, policies, resources, region, state=None):
    """单条规则的可读详情：阈值策略 + 关联资源 + 通知对象。"""
    row = rule_row(rule, {rule.get("alarm_id"): state} if state else None)
    lines = ["告警规则详情（Region %s）：" % region]
    labels = [
        ("规则ID", row["规则ID"]),
        ("名称", row["名称"]),
        ("资源类型", row["资源类型"]),
        ("监控维度", row["监控维度"]),
        ("指标", row["指标"]),
        ("告警级别", row["告警级别"]),
        ("当前状态", row["当前状态"]),
        ("是否启用", row["是否启用"]),
        ("描述", _first(rule, "description")),
    ]
    for label, value in labels:
        lines.append("  %-8s: %s" % (label, value))

    lines.append("")
    lines.append("阈值策略（%d 条）：" % len(policies))
    if policies:
        for index, policy in enumerate(policies, start=1):
            lines.append(
                "  %d. 指标 %s  %s  级别：%s"
                % (index,
                   _first(policy, "metric_name"),
                   format_threshold(policy),
                   level_name(policy.get("level"))))
    else:
        lines.append("  （无策略数据）")

    groups = _normalize_resource_groups(resources)
    lines.append("")
    lines.append("关联资源（%d 组）：" % len(groups))
    if groups:
        for index, group in enumerate(groups, start=1):
            dims = [_format_dimension(d) for d in group["dimensions"]]
            label = (group.get("resource_group_name") or group.get("resource_group_id")
                     or "资源组 %d" % index)
            lines.append("  - %s%s" % (
                label, ("：" + ", ".join(dims)) if dims else ""))
    else:
        lines.append("  （无关联资源数据）")

    lines.append("")
    lines.append("通知对象：")
    lines.extend(_notification_lines(rule))
    return "\n".join(lines)


def render_detail_tables(rule, policies, resources, region, state=None):
    """--table 的单条详情：基本信息 + 策略 + 资源 + 通知 四段表格。"""
    row = rule_row(rule, {rule.get("alarm_id"): state} if state else None)
    base_rows = [{"字段": key, "值": row[key]} for key in TABLE_COLUMNS]
    base_rows.append({"字段": "描述", "值": _cell(_first(rule, "description"))})
    policy_rows = []
    for policy in policies:
        policy_rows.append({
            "指标": _first(policy, "metric_name"),
            "监控维度": _first(policy, "dimension_name"),
            "阈值与比较符": format_threshold(policy),
            "告警级别": level_name(policy.get("level")),
            "连续次数": _first(policy, "count"),
            "周期(分钟)": _first(policy, "period"),
            "抑制周期(秒)": _first(policy, "suppress_duration"),
            "单位": _first(policy, "unit"),
        })
    resource_rows = []
    for resource in _normalize_resource_groups(resources):
        dims = []
        for dimension in _as_list(resource.get("dimensions")):
            if isinstance(dimension, dict):
                dims.append(_format_dimension(dimension))
        resource_rows.append({
            "资源分组ID": _first(resource, "resource_group_id"),
            "资源分组名称": _first(resource, "resource_group_name"),
            "维度": ", ".join(dims) if dims else _FIELD_MISSING,
            "规格": _first(resource, "product_name"),
        })
    notification_rows = []
    for key, label in (("alarm_notifications", "告警通知"),
                       ("ok_notifications", "恢复通知"),
                       ("insufficientdata_actions", "数据不足通知")):
        for item in _as_list(rule.get(key)):
            if isinstance(item, dict):
                notification_rows.append({
                    "通知类型": label,
                    "通道": item.get("type") or _FIELD_MISSING,
                    "通知对象数": len(_as_list(item.get("notification_list"))),
                })
    blocks = [
        "告警规则详情（Region %s）：" % region,
        render_table(base_rows, ["字段", "值"]),
        "",
        "阈值策略（%d 条）：" % len(policies),
        render_table(policy_rows,
                     ["指标", "监控维度", "阈值与比较符", "告警级别",
                      "连续次数", "周期(分钟)", "抑制周期(秒)", "单位"]),
        "",
        "关联资源（%d 组）：" % len(resources),
        render_table(resource_rows, ["资源分组ID", "资源分组名称", "维度", "规格"]),
        "",
        "通知对象：",
        render_table(notification_rows, ["通知类型", "通道", "通知对象数"]),
    ]
    return "\n".join(blocks)


# ---------------------------------------------------------------------------
# 主流程
# ---------------------------------------------------------------------------

def parse_args(argv):
    parser = argparse.ArgumentParser(
        description="盘点华为云 CES 告警规则列表并查看单条规则详情（只读）。")
    parser.add_argument("-r", "--region", default=DEFAULT_REGION,
                        help="目标 Region（默认 %s）" % DEFAULT_REGION)
    parser.add_argument("--rule-id", dest="rule_id", default=None,
                        help="单条告警规则 ID（形如 al 开头 + 22 位），输出该规则详情")
    parser.add_argument("--name", default=None,
                        help="按规则名称过滤：先按服务端 name 参数透传，再做客户端模糊匹配")
    parser.add_argument("--alarm-level", dest="alarm_level", action="append",
                        default=None,
                        help="按告警级别过滤（1 紧急 / 2 重要 / 3 次要 / 4 提示，"
                             "可逗号分隔或重复给出）；客户端过滤")
    parser.add_argument("--alarm-state", dest="alarm_state", action="append",
                        default=None,
                        help="按当前告警状态过滤（ok / alarm / insufficient_data / "
                             "invalid，可逗号分隔）；客户端过滤")
    parser.add_argument("--resource-type", dest="resource_type", default=None,
                        help="按资源类型过滤（namespace / product_name / 维度名，"
                             "子串匹配）；客户端过滤")
    parser.add_argument("--limit", type=int, default=DEFAULT_PAGE_SIZE,
                        help="分页大小（1~100，默认 %d，自动翻页）" % DEFAULT_PAGE_SIZE)
    parser.add_argument("--offset", type=int, default=0,
                        help="起始分页偏移（默认 0）")
    parser.add_argument("--max-pages", dest="max_pages", type=int, default=100,
                        help="自动翻页的最大页数（默认 100，防死循环）")
    parser.add_argument("--table", action="store_true",
                        help="输出全字段表格（规则ID·名称·资源类型·监控维度·指标·"
                             "阈值与比较符·告警级别·当前状态·是否启用·通知方式）")
    parser.add_argument("--json", action="store_true",
                        help="输出接口原始 JSON 结构")
    return parser.parse_args(argv)


def _fetch_detail(region, rule_id):
    """取单条规则本体 + 策略 + 资源。"""
    payload, rules = _query_page(OPERATION_LIST, region,
                                 {"alarm_id": rule_id, "limit": 1}, None)
    policies = []
    resources = []
    if rules:
        rule = rules[0]
        _, policies = _query_page(OPERATION_POLICIES, region,
                                  {"alarm_id": rule_id, "limit": MAX_PAGE_SIZE}, 0)
        _, resources = _query_page(OPERATION_RESOURCES, region,
                                   {"alarm_id": rule_id, "limit": MAX_PAGE_SIZE}, 0)
        return rule, policies, resources, payload
    return None, policies, resources, payload


def main(argv=None):
    raw_argv = argv if argv is not None else sys.argv[1:]

    # 守卫先于 argparse：变更意图要作为守卫违例报出，而不是 argparse 的未知参数错。
    try:
        guard_write_intent(guard_text_from_argv(raw_argv))
    except AlarmRulesError as exc:
        print("[错误] %s" % exc, file=sys.stderr)
        return 1

    args = parse_args(argv)

    try:
        if args.limit is None or not (1 <= args.limit <= MAX_PAGE_SIZE):
            raise ApiError("--limit 必须在 1~100 之间：%s" % args.limit)
        if args.offset is None or args.offset < 0:
            raise ApiError("--offset 必须 >= 0：%s" % args.offset)
        if args.max_pages is None or args.max_pages < 1:
            raise ApiError("--max-pages 必须 >= 1：%s" % args.max_pages)
        guard_operation(OPERATION_LIST)
        levels = parse_level_filter(args.alarm_level)
        states = parse_state_filter(args.alarm_state)

        if args.rule_id:
            rule, policies, resources, _payload = _fetch_detail(args.region,
                                                                args.rule_id)
            if rule is None:
                print("Region %s 未找到告警规则 %s（请核对 --rule-id 与区域）。"
                      % (args.region, args.rule_id))
                return 0
            state = None
            try:
                state = fetch_alarm_state_map(args.region).get(args.rule_id)
            except AlarmRulesError as exc:
                print("[警告] 未能获取告警状态（%s），当前状态标注为「未知」。"
                      % str(exc)[:120], file=sys.stderr)
            if args.json:
                print(json.dumps({"alarm": rule, "policies": policies,
                                  "resources": resources},
                                 ensure_ascii=False, indent=2))
            elif args.table:
                print(render_detail_tables(rule, policies, resources,
                                           args.region, state))
            else:
                print(render_detail(rule, policies, resources, args.region, state))
            return 0

        rules = list_alarm_rules(args.region, name=args.name, limit=args.limit,
                                 offset=args.offset, max_pages=args.max_pages)

        state_map = {}
        need_state = bool(args.table or args.json or states)
        if need_state:
            try:
                state_map = fetch_alarm_state_map(args.region)
            except AlarmRulesError as exc:
                if states:
                    raise ApiError(
                        "无法获取告警状态，--alarm-state 过滤无法执行：%s" % str(exc)[:200])
                print("[警告] 未能获取告警状态（%s），当前状态标注为「未知」。"
                      % str(exc)[:120], file=sys.stderr)

        filtered = filter_rules(rules, state_map=state_map, name=args.name,
                                levels=levels, states=states,
                                resource_type=args.resource_type)

        filters = []
        if args.name:
            filters.append("name~%s" % args.name)
        if levels:
            filters.append("alarm-level=%s" % ",".join(
                str(x) for x in sorted(levels)))
        if states:
            filters.append("alarm-state=%s" % ",".join(sorted(states)))
        if args.resource_type:
            filters.append("resource-type~%s" % args.resource_type)
        filter_suffix = "（过滤条件: %s）" % ", ".join(filters) if filters else ""

        if args.json:
            print(json.dumps(filtered, ensure_ascii=False, indent=2))
            return 0

        if not filtered:
            print("Region %s 无 CES 告警规则%s。" % (args.region, filter_suffix))
            if args.table:
                print(render_table([], TABLE_COLUMNS))
            return 0

        if args.table:
            rows = [rule_row(rule, state_map) for rule in filtered]
            print("CES 告警规则（Region %s，共 %d 条）%s："
                  % (args.region, len(rows), filter_suffix))
            print(render_table(rows, TABLE_COLUMNS))
            return 0

        print("CES 告警规则名称（Region %s，共 %d 条）%s："
              % (args.region, len(filtered), filter_suffix))
        print(render_name_list(filtered))
        return 0
    except AlarmRulesError as exc:
        print("[错误] %s" % exc, file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())