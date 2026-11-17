#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Huawei Cloud Auto Scaling (AS) inventory helper — strictly read-only.

Inventories the AS scaling groups of one region (name / ID / status / desired and
current instance numbers / min-max / VPC / subnet / associated ELB) and the
instances inside a scaling group (life-cycle state / health status / join
time). Aimed at troubleshooting "scale-out did not take effect", "instance
counts do not match", and "scaling group stuck in an abnormal state".

Executed operations (both read-only):

    ListScalingGroups    GET /autoscaling-api/v1/{project_id}/scaling_group
    ListScalingInstances GET /autoscaling-api/v1/{project_id}/scaling_group_instance/{scaling_group_id}/list

Backends:

- primary:  KooCLI subprocess ``hcloud AS ListScalingGroups`` /
  ``hcloud AS ListScalingInstances --scaling_group_id=<id>``
- fallback: official ``huaweicloudsdkas`` v1 SDK (``AsClient``)

Output modes:

- default:  compact list (scaling group: 名称 | 组ID | 状态)
- ``--table``: group view (11 columns) or, with ``--group-id``, instance view
  (6 columns). Abnormal groups (desired != current or status != INSERVICE) and
  abnormal instances (life-cycle != INSERVICE or health != NORMAL) are placed
  in a separate highlighted section at the top.
- ``--json``: the raw merged response body

Filtering: ``--name`` (exact; ``--fuzzy`` for substring), ``--group-id``
(drill down to instances), ``--status`` (client-side, supports the
``abnormal`` alias), ``--region`` (default cn-north-4).

Every mutating intent (create / update / delete / enable / disable /
batch-add / batch-remove / policy-execute / ...) is rejected with exit code 1
before any command runs — this skill never writes to AS.

Credentials are never hardcoded and never read by this script: the KooCLI
profile / environment is used by ``hcloud``; the SDK path reads AK/SK from
environment variables only.

Usage:
    python3 scripts/list_as_groups.py --region cn-north-4
    python3 scripts/list_as_groups.py --table
    python3 scripts/list_as_groups.py --json
    python3 scripts/list_as_groups.py --name web --fuzzy
    python3 scripts/list_as_groups.py --status abnormal
    python3 scripts/list_as_groups.py --group-id <group-id> --table
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
from datetime import date, datetime
from types import SimpleNamespace

SKILL_NAME = "huawei-cloud-as-group-list"
DEFAULT_REGION = os.environ.get("HUAWEICLOUD_SDK_REGION", "cn-north-4")
DEFAULT_LIMIT = 100
MAX_LIMIT = 100
DEFAULT_MAX_PAGES = 50
DEFAULT_TIMEOUT = 60

HCLOUD_BIN_ENV = ("HUAWEI_CLOUD_AS_GROUP_LIST_HCLOUD_BIN", "AS_HCLOUD_BIN")

READONLY_OPERATIONS = ("ListScalingGroups", "ListScalingInstances")
ALLOWED_ACTIONS = ("list", "ls", "query", "describe", "show", "inspect")

WRITE_INTENT_TOKENS = (
    "create", "delete", "update", "enable", "disable", "pause", "resume",
    "batch-add", "batch_add", "batch-remove", "batch_remove",
    "policy-execute", "policy_execute", "execute-policy", "execute_policy",
    "remove-instance", "remove_instance", "add-instance", "add_instance",
    "attach", "detach", "reboot", "modify", "scale-out", "scale_out",
    "scale-in", "scale_in",
)

GROUP_STATUSES = ("INSERVICE", "PAUSED", "ERROR", "DELETING", "FREEZED")
INSTANCE_LIFECYCLES = (
    "INSERVICE", "PENDING", "PENDING_WAIT", "REMOVING", "REMOVING_WAIT",
    "STANDBY", "ENTERING_STANDBY",
)
INSTANCE_HEALTH = ("INITIALIZING", "NORMAL", "ERROR")
ABNORMAL_ALIASES = (
    "abnormal", "anomaly", "drift", "mismatch", "inconsistent", "desync",
    "异常",
)
NOT_INSERVICE_ALIASES = (
    "not-inservice", "non-inservice", "not_inservice", "notinservice",
    "非inservice",
)

GROUP_KEY = "scaling_groups"
INSTANCE_KEY = "scaling_group_instances"


class AsError(Exception):
    """Classified failure with a user-actionable message."""

    def __init__(self, kind, message, detail=""):
        Exception.__init__(self, message)
        self.kind = kind
        self.message = message
        self.detail = detail


# ---------------------------------------------------------------------------
# Write-intent guard
# ---------------------------------------------------------------------------

def _flag_value(argv, index):
    token = argv[index]
    if token.startswith("--") and "=" in token:
        return token.split("=", 1)[1]
    if index + 1 < len(argv) and not argv[index + 1].startswith("--"):
        return argv[index + 1]
    return None


def guard_write_intent(argv):
    """Reject mutating intent on the raw argv before argparse / any cloud call.

    Returns an error message when a write intent is detected, else None. The
    value of ``--name`` is deliberately scanned as well: an AS group called
    ``create-me`` would make the requested read ambiguous, and the acceptance
    criteria require such input to be rejected.
    """
    action = None
    operation = None
    values = []
    index = 0
    while index < len(argv):
        token = argv[index]
        if token.startswith("--"):
            name = token.split("=", 1)[0]
            lowered_name = name.lower()
            value = _flag_value(argv, index)
            if lowered_name == "--action":
                action = value
            elif lowered_name == "--operation":
                operation = value
            for write_token in WRITE_INTENT_TOKENS:
                if write_token in lowered_name:
                    return (
                        "此技能为只读查询（AS 伸缩组/实例盘点），检测到写操作参数: {0}。"
                        "仅支持查询动作，写操作已被守卫拦截。".format(name)
                    )
            if lowered_name in ("--name", "--group-id", "--status") and value:
                values.append((name, value))
        else:
            values.append(("参数", token))
        index += 1

    if action is not None:
        lowered_action = str(action).strip().lower()
        if lowered_action not in ALLOWED_ACTIONS:
            return (
                "此技能为只读查询（AS 伸缩组/实例盘点），拒绝执行非查询动作: {0}。"
                "支持的动作仅限 list（默认）。".format(action)
            )
    if operation is not None and operation not in READONLY_OPERATIONS:
        return (
            "此技能只允许调用只读接口 ListScalingGroups / ListScalingInstances，"
            "拒绝执行: {0}。".format(operation)
        )

    for field, value in values:
        lowered_value = str(value).lower()
        for write_token in WRITE_INTENT_TOKENS:
            if write_token in lowered_value:
                return (
                    "此技能为只读查询（AS 伸缩组/实例盘点），不支持执行写操作。"
                    "在 {0} 中检测到疑似写操作意图: {1}".format(field, write_token)
                )
    return None


# ---------------------------------------------------------------------------
# KooCLI backend
# ---------------------------------------------------------------------------

def hcloud_binary():
    """Return the hcloud binary path or None (env override wins for tests)."""
    for name in HCLOUD_BIN_ENV:
        override = os.environ.get(name)
        if override:
            return override
    return shutil.which("hcloud")


def _jsonable(value):
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if isinstance(value, dict):
        return {key: _jsonable(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_jsonable(item) for item in value]
    return value


def parse_hcloud_json(body):
    """Extract the first JSON object from hcloud stdout.

    hcloud may append diagnostic text after the JSON body (for example the
    "Failed to get terminal width" line), so a plain json.loads is not enough.
    """
    text = (body or "").strip()
    if not text:
        return None
    start = text.find("{")
    if start < 0:
        return None
    try:
        value, _ = json.JSONDecoder().raw_decode(text[start:])
    except ValueError:
        return None
    return value


def classify_cli_error(detail, returncode=None):
    """Map a hcloud / API failure message onto an actionable AsError."""
    text = detail or ""
    lowered = text.lower()
    if "[use_error]" in lowered:
        return AsError(
            "use_error",
            "KooCLI 参数/用法错误（[USE_ERROR]），请检查 --region / --limit / "
            "--group-id 取值（limit 需在 1~100 之间）。",
            text,
        )
    if ("as.0031" in lowered or "not authorized" in lowered
            or "accessdenied" in lowered or "access denied" in lowered
            or "no identity-based policy" in lowered
            or "permission" in lowered or "403" in text):
        return AsError(
            "forbidden",
            "无权限访问 AS 伸缩组/实例（403），请检查 IAM 权限："
            "查询伸缩组需 as:scalingGroup:list（别名 as:groups:list），"
            "查询组内实例需 as:scalingGroup:listInstances（别名 as:instances:list）。",
            text,
        )
    if ("not found" in lowered or "does not exist" in lowered
            or "not exist" in lowered or "as.0049" in lowered
            or "伸缩组不存在" in text or "404" in text):
        return AsError(
            "not_found",
            "伸缩组不存在或不属于当前区域（请确认 --group-id 与 --region）。"
            "可先不带 --group-id 列出全部伸缩组，再选择有效 ID。",
            text,
        )
    if ("credential" in lowered or "ak/sk" in lowered or "ak, sk" in lowered
            or "no valid authentication" in lowered):
        return AsError(
            "credentials",
            "缺少或无效的华为云凭据（AK/SK）。请在终端离线配置 KooCLI profile，"
            "或设置 HUAWEICLOUD_SDK_AK / HUAWEICLOUD_SDK_SK 环境变量后重试。",
            text,
        )
    return AsError(
        "cli_error",
        "hcloud 调用失败（exit={0}）。".format(returncode),
        text,
    )


def _raise_error_body(error_body):
    detail = json.dumps(error_body, ensure_ascii=False)
    code = str(error_body.get("code") or error_body.get("error_code") or "")
    message = error_body.get("message") or error_body.get("error_msg") or detail
    exc = classify_cli_error(detail + "\n" + str(message))
    # Preserve the original API code in the detail for troubleshooting.
    if code:
        exc.detail = "{0}\n{1}".format(code, detail)
    raise exc


def run_hcloud(args, timeout=DEFAULT_TIMEOUT):
    """Run hcloud and return the parsed JSON body."""
    binary = hcloud_binary()
    if not binary:
        raise AsError(
            "cli_missing",
            "未找到 hcloud（KooCLI），无法查询 AS 伸缩组列表。",
            "安装后可重试（见 references/cli-installation-guide.md），"
            "或改用 --backend sdk 走 SDK 回退。",
        )
    command = [binary] + list(args)
    try:
        proc = subprocess.run(command, capture_output=True, text=True,
                              timeout=timeout)
    except subprocess.TimeoutExpired:
        raise AsError(
            "timeout",
            "调用 hcloud 超时（{0} 秒），请检查网络或稍后重试。".format(timeout),
        )
    except OSError as exc:
        raise AsError("cli_error", "无法执行 hcloud: {0}".format(exc))

    body = (proc.stdout or "").strip()
    data = parse_hcloud_json(body)

    if isinstance(data, dict) and isinstance(data.get("error"), dict):
        _raise_error_body(data["error"])
    if (isinstance(data, dict) and data.get("error_msg")
            and not data.get(GROUP_KEY) and not data.get(INSTANCE_KEY)):
        _raise_error_body(data)
    stderr = (proc.stderr or "").strip()
    if proc.returncode != 0:
        raise classify_cli_error(stderr or body, proc.returncode)
    if not isinstance(data, dict):
        detail = stderr or body
        if detail:
            raise classify_cli_error(detail, proc.returncode)
        raise AsError(
            "bad_output",
            "hcloud 返回了非 JSON 输出，无法解析 AS 响应。",
            body[:300],
        )
    return data


def build_group_args(region, limit, start_number, name=None):
    args = [
        "AS", "ListScalingGroups",
        "--cli-region=" + region,
        "--limit=" + str(limit),
        "--start_number=" + str(start_number),
    ]
    if name:
        args.append("--scaling_group_name=" + str(name))
    return args


def build_instance_args(region, limit, start_number, group_id):
    return [
        "AS", "ListScalingInstances",
        "--cli-region=" + region,
        "--scaling_group_id=" + str(group_id),
        "--limit=" + str(limit),
        "--start_number=" + str(start_number),
    ]


# ---------------------------------------------------------------------------
# SDK backend (fallback)
# ---------------------------------------------------------------------------

def env_credentials():
    ak = (os.environ.get("HUAWEICLOUD_SDK_AK")
          or os.environ.get("HUAWEI_ACCESS_KEY")
          or os.environ.get("HUAWEI_AK"))
    sk = (os.environ.get("HUAWEICLOUD_SDK_SK")
          or os.environ.get("HUAWEI_SECRET_KEY")
          or os.environ.get("HUAWEI_SK"))
    if not ak or not sk:
        raise AsError(
            "credentials",
            "缺少华为云凭据（AK/SK）。请在终端离线配置 KooCLI profile 或导出 "
            "HUAWEICLOUD_SDK_AK / HUAWEICLOUD_SDK_SK 环境变量后重试。",
        )
    return ak, sk


def sdk_client(region):
    """Build an AS SDK client (lazy import keeps the CLI path dependency-free)."""
    try:
        from huaweicloudsdkcore.auth.credentials import BasicCredentials
        from huaweicloudsdkas.v1 import AsClient
        from huaweicloudsdkas.v1.region.as_region import AsRegion
    except ImportError as exc:
        raise AsError(
            "sdk_missing",
            "未安装华为云 AS SDK（huaweicloudsdkas），无法走 SDK 回退。",
            "pip install huaweicloudsdkcore huaweicloudsdkas；"
            "或安装 KooCLI 走 CLI 主路径。原始错误: {0}".format(exc),
        )
    ak, sk = env_credentials()
    credentials = BasicCredentials(ak, sk)
    token = os.environ.get("HUAWEICLOUD_SDK_SECURITY_TOKEN")
    if token:
        credentials = credentials.with_security_token(token)
    builder = AsClient.new_builder().with_credentials(credentials)
    try:
        return builder.with_region(AsRegion.value_of(region)).build()
    except Exception:
        from huaweicloudsdkcore.region.region import Region
        endpoint = "https://as.{0}.myhuaweicloud.com".format(region)
        return builder.with_region(Region(id=region, endpoint=endpoint)).build()


def _sdk_request(name, **fields):
    """Build an SDK request model, or a plain attribute holder."""
    try:
        module = __import__("huaweicloudsdkas.v1", fromlist=[name])
        request = getattr(module, name)()
    except Exception:
        request = SimpleNamespace()
    for key, value in fields.items():
        if value is not None:
            setattr(request, key, value)
    return request


def _response_to_dict(response):
    if hasattr(response, "to_dict"):
        try:
            data = response.to_dict()
            if isinstance(data, dict):
                return _jsonable(data)
        except Exception:
            pass
    data = {}
    for attr in (GROUP_KEY, INSTANCE_KEY, "total_number", "start_number", "limit"):
        value = getattr(response, attr, None)
        if value is None:
            continue
        if isinstance(value, list) and value and hasattr(value[0], "to_dict"):
            data[attr] = [_jsonable(item.to_dict()) for item in value]
        else:
            data[attr] = _jsonable(value)
    return data


def sdk_page(region, limit, start_number, name=None, group_id=None):
    """One AS list page through the SDK, returned as a plain dict."""
    if group_id:
        request = _sdk_request(
            "ListScalingInstancesRequest", scaling_group_id=str(group_id),
            start_number=int(start_number), limit=int(limit))
        response = sdk_client(region).list_scaling_instances(request)
    else:
        request = _sdk_request(
            "ListScalingGroupsRequest", scaling_group_name=name,
            start_number=int(start_number), limit=int(limit))
        response = sdk_client(region).list_scaling_groups(request)
    return _response_to_dict(response)


# ---------------------------------------------------------------------------
# Pagination
# ---------------------------------------------------------------------------

def _items(body, key):
    items = body.get(key) if isinstance(body, dict) else None
    return items if isinstance(items, list) else []


def _total_number(body):
    if not isinstance(body, dict):
        return None
    for key in ("total_number", "total"):
        value = body.get(key)
        if value in (None, ""):
            continue
        try:
            return int(value)
        except (TypeError, ValueError):
            continue
    return None


def _start_number(body, fallback):
    if isinstance(body, dict):
        value = body.get("start_number")
        if value not in (None, ""):
            try:
                return int(value)
            except (TypeError, ValueError):
                pass
    return fallback


def _paginate(fetch_page, key, limit, max_pages):
    """Fetch pages until total_number / accumulated count / short page says stop."""
    pages = []
    received = 0
    total = None
    start = 0
    for _ in range(max_pages):
        body = fetch_page(start)
        if not isinstance(body, dict):
            body = {}
        pages.append(body)
        page_total = _total_number(body)
        if page_total is not None:
            total = page_total
        count = len(_items(body, key))
        received += count
        if count == 0:
            break
        if total is not None and received >= total:
            break
        if count < limit:
            break
        start = _start_number(body, start) + count
    return pages


def fetch_pages_hcloud(region, limit, max_pages, timeout=DEFAULT_TIMEOUT,
                       name=None, group_id=None):
    key = INSTANCE_KEY if group_id else GROUP_KEY

    def fetch(start):
        if group_id:
            args = build_instance_args(region, limit, start, group_id)
        else:
            args = build_group_args(region, limit, start, name)
        return run_hcloud(args, timeout)

    return _paginate(fetch, key, limit, max_pages)


def fetch_pages_sdk(region, limit, max_pages, name=None, group_id=None):
    key = INSTANCE_KEY if group_id else GROUP_KEY

    def fetch(start):
        return sdk_page(region, limit, start, name=name, group_id=group_id)

    return _paginate(fetch, key, limit, max_pages)


# ---------------------------------------------------------------------------
# Normalization / filtering
# ---------------------------------------------------------------------------

def _as_int(value):
    if value in (None, ""):
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _text(value):
    if value in (None, ""):
        return ""
    return str(value)


def _subnet_ids(item):
    result = []
    for network in item.get("networks") or []:
        if isinstance(network, dict):
            network_id = network.get("id")
        else:
            network_id = network
        if network_id:
            result.append(str(network_id))
    return result


def _elb_ids(item):
    result = []
    classic = _text(item.get("lb_listener_id"))
    if classic:
        result.extend(part.strip() for part in classic.split(",") if part.strip())
    for listener in item.get("lbaas_listeners") or []:
        if isinstance(listener, dict):
            listener_id = listener.get("listener_id") or listener.get("pool_id")
        else:
            listener_id = listener
        if listener_id:
            result.append(str(listener_id))
    unique = []
    for value in result:
        if value not in unique:
            unique.append(value)
    return unique


def normalize_groups(pages, region):
    groups = []
    seen = set()
    for body in pages:
        for item in _items(body, GROUP_KEY):
            if not isinstance(item, dict):
                continue
            group_id = _text(item.get("scaling_group_id"))
            if group_id and group_id in seen:
                continue
            if group_id:
                seen.add(group_id)
            groups.append({
                "group_id": group_id,
                "name": _text(item.get("scaling_group_name")),
                "status": _text(item.get("scaling_group_status")),
                "desire": _as_int(item.get("desire_instance_number")),
                "current": _as_int(item.get("current_instance_number")),
                "min": _as_int(item.get("min_instance_number")),
                "max": _as_int(item.get("max_instance_number")),
                "vpc_id": _text(item.get("vpc_id")),
                "subnet_ids": _subnet_ids(item),
                "elb_ids": _elb_ids(item),
                "create_time": _text(item.get("create_time")),
                "detail": _text(item.get("detail")),
                "is_scaling": item.get("is_scaling"),
                "activity_type": _text(item.get("activity_type")),
                "region": region,
            })
    return groups


def normalize_instances(pages, region, group_id=None):
    instances = []
    seen = set()
    for body in pages:
        for item in _items(body, INSTANCE_KEY):
            if not isinstance(item, dict):
                continue
            instance_id = _text(item.get("instance_id"))
            if instance_id and instance_id in seen:
                continue
            if instance_id:
                seen.add(instance_id)
            instances.append({
                "instance_id": instance_id,
                "instance_name": _text(item.get("instance_name")),
                "group_id": _text(item.get("scaling_group_id")) or _text(group_id),
                "group_name": _text(item.get("scaling_group_name")),
                "life_cycle_state": _text(item.get("life_cycle_state")),
                "health_status": _text(item.get("health_status")),
                "config_name": _text(item.get("scaling_configuration_name")),
                "config_id": _text(item.get("scaling_configuration_id")),
                "create_time": _text(item.get("create_time")),
                "protect_from_scaling_down": item.get("protect_from_scaling_down"),
                "region": region,
            })
    return instances


def group_is_abnormal(group):
    if _text(group.get("status")).upper() != "INSERVICE":
        return True
    desire = group.get("desire")
    current = group.get("current")
    if desire is not None and current is not None and desire != current:
        return True
    return False


def instance_is_abnormal(instance):
    if _text(instance.get("life_cycle_state")).upper() != "INSERVICE":
        return True
    health = _text(instance.get("health_status")).upper()
    if health and health != "NORMAL":
        return True
    return False


def _status_key(status):
    return str(status).strip().lower()


def filter_groups(groups, name=None, fuzzy=False, status=None):
    selected = groups
    if name:
        needle = str(name).strip().lower()
        if fuzzy:
            selected = [g for g in selected
                        if needle in _text(g.get("name")).lower()]
        else:
            selected = [g for g in selected
                        if _text(g.get("name")).lower() == needle]
    if status:
        key = _status_key(status)
        if key in ABNORMAL_ALIASES:
            selected = [g for g in selected if group_is_abnormal(g)]
        elif key in NOT_INSERVICE_ALIASES:
            selected = [g for g in selected
                        if _text(g.get("status")).upper() != "INSERVICE"]
        else:
            selected = [g for g in selected
                        if _text(g.get("status")).upper() == key.upper()]
    return selected


def filter_instances(instances, status=None):
    if not status:
        return instances
    key = _status_key(status)
    if key in ABNORMAL_ALIASES:
        return [item for item in instances if instance_is_abnormal(item)]
    if key in NOT_INSERVICE_ALIASES:
        return [item for item in instances
                if _text(item.get("life_cycle_state")).upper() != "INSERVICE"]
    upper = key.upper()
    return [item for item in instances
            if upper in (_text(item.get("life_cycle_state")).upper(),
                         _text(item.get("health_status")).upper())]


def valid_status(status, instance_mode=False):
    key = _status_key(status)
    if key in ABNORMAL_ALIASES or key in NOT_INSERVICE_ALIASES:
        return True
    allowed = set(GROUP_STATUSES) | set(INSTANCE_LIFECYCLES) | set(INSTANCE_HEALTH)
    return key.upper() in allowed


# ---------------------------------------------------------------------------
# Presentation
# ---------------------------------------------------------------------------

def _cell_int(value):
    return "-" if value is None else str(value)


def _min_max(min_value, max_value):
    if min_value is None and max_value is None:
        return "-"
    return "{0}-{1}".format(_cell_int(min_value), _cell_int(max_value))


def render_table(header, rows):
    widths = [len(header[i]) for i in range(len(header))]
    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(str(cell)))
    lines = [" | ".join(header[i].ljust(widths[i]) for i in range(len(header)))]
    lines.append("-+-".join("-" * width for width in widths))
    for row in rows:
        lines.append(" | ".join(str(row[i]).ljust(widths[i])
                                for i in range(len(header))))
    return "\n".join(lines)


def group_row(group, marked=False):
    group_id = group.get("group_id") or "-"
    if marked:
        group_id = "⚠ " + group_id
    return [
        group_id,
        group.get("name") or "-",
        group.get("status") or "-",
        _cell_int(group.get("desire")),
        _cell_int(group.get("current")),
        _min_max(group.get("min"), group.get("max")),
        group.get("vpc_id") or "-",
        ",".join(group.get("subnet_ids") or []) or "-",
        ",".join(group.get("elb_ids") or []) or "-",
        group.get("create_time") or "-",
        group.get("region") or "-",
    ]


GROUP_TABLE_HEADER = [
    "组ID", "名称", "状态", "期望实例数", "当前实例数", "最小-最大",
    "VPC", "子网", "关联ELB", "创建时间", "region",
]


def render_group_table(groups):
    abnormal = [group for group in groups if group_is_abnormal(group)]
    normal = [group for group in groups if not group_is_abnormal(group)]
    lines = ["异常伸缩组（期望实例数≠当前实例数 或 状态非 INSERVICE）："]
    if abnormal:
        lines.append(render_table(GROUP_TABLE_HEADER,
                                  [group_row(group, True) for group in abnormal]))
    else:
        lines.append("无")
    lines.append("")
    lines.append("正常伸缩组：")
    if normal:
        lines.append(render_table(GROUP_TABLE_HEADER,
                                  [group_row(group, False) for group in normal]))
    else:
        lines.append("无")
    return "\n".join(lines)


def instance_row(instance, marked=False):
    instance_id = instance.get("instance_id") or "-"
    if marked:
        instance_id = "⚠ " + instance_id
    return [
        instance_id,
        instance.get("instance_name") or "-",
        instance.get("group_name") or instance.get("group_id") or "-",
        instance.get("life_cycle_state") or "-",
        instance.get("health_status") or "-",
        instance.get("create_time") or "-",
    ]


INSTANCE_TABLE_HEADER = [
    "实例ID", "实例名", "所属伸缩组", "生命周期状态", "健康状态", "加入时间",
]


def render_instance_table(instances):
    abnormal = [item for item in instances if instance_is_abnormal(item)]
    normal = [item for item in instances if not instance_is_abnormal(item)]
    lines = ["异常实例（生命周期非 INSERVICE 或 健康状态非 NORMAL）："]
    if abnormal:
        lines.append(render_table(
            INSTANCE_TABLE_HEADER,
            [instance_row(item, True) for item in abnormal]))
    else:
        lines.append("无")
    lines.append("")
    lines.append("正常实例：")
    if normal:
        lines.append(render_table(
            INSTANCE_TABLE_HEADER,
            [instance_row(item, False) for item in normal]))
    else:
        lines.append("无")
    return "\n".join(lines)


def merge_pages(pages, group_id_mode, region):
    key = INSTANCE_KEY if group_id_mode else GROUP_KEY
    merged = {
        key: [],
        "total_number": 0,
        "start_number": 0,
        "limit": 0,
        "region": region,
    }
    total = None
    for body in pages:
        merged[key].extend(_items(body, key))
        page_total = _total_number(body)
        if page_total is not None:
            total = page_total
        limit = _as_int(body.get("limit"))
        if limit is not None:
            merged["limit"] = limit
    merged["total_number"] = total if total is not None else len(merged[key])
    return _jsonable(merged)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser():
    parser = argparse.ArgumentParser(
        prog="list_as_groups.py",
        description="查询华为云 AS 伸缩组及组内实例列表（严格只读）",
    )
    parser.add_argument("--region", "-r", default=DEFAULT_REGION,
                        help="区域，默认 {0}".format(DEFAULT_REGION))
    parser.add_argument("--name", default=None,
                        help="按伸缩组名称过滤（默认精确匹配；配合 --fuzzy 变模糊）")
    parser.add_argument("--fuzzy", action="store_true",
                        help="--name 使用模糊（子串）匹配")
    parser.add_argument("--group-id", dest="group_id", default=None,
                        help="下钻查询指定伸缩组内的实例")
    parser.add_argument("--status", default=None,
                        help="客户端状态过滤：INSERVICE/PAUSED/ERROR/DELETING/"
                             "FREEZED、实例生命周期/健康状态，或 abnormal（仅异常）")
    parser.add_argument("--limit", type=int, default=DEFAULT_LIMIT,
                        help="每页数量 1~100，默认 {0}".format(DEFAULT_LIMIT))
    parser.add_argument("--max-pages", type=int, default=DEFAULT_MAX_PAGES,
                        help="最大分页数，默认 {0}".format(DEFAULT_MAX_PAGES))
    parser.add_argument("--table", action="store_true",
                        help="输出完整表格（组视图 11 列；--group-id 时为实例视图 6 列）")
    parser.add_argument("--json", action="store_true", help="输出原始响应 JSON")
    parser.add_argument("--backend", choices=("auto", "cli", "sdk"), default="auto",
                        help="后端: auto=CLI 优先、失败回退 SDK（默认）")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT,
                        help="单次调用超时秒数，默认 {0}".format(DEFAULT_TIMEOUT))
    parser.add_argument("--action", default="list",
                        help="动作，仅支持 list（默认）；其它值会被只读守卫拒绝")
    parser.add_argument("--operation", default=None,
                        help="hcloud 操作，仅允许 ListScalingGroups / ListScalingInstances")
    return parser


def _fetch(args):
    backend = args.backend
    pages = []
    used = None
    try:
        if backend in ("auto", "cli"):
            if hcloud_binary():
                try:
                    pages = fetch_pages_hcloud(
                        args.region, args.limit, args.max_pages, args.timeout,
                        name=args.name, group_id=args.group_id)
                    used = "cli"
                except AsError as exc:
                    if backend == "cli" or exc.kind in (
                            "forbidden", "credentials", "not_found", "use_error"):
                        raise
                    print("hcloud 调用失败，回退 SDK：{0}".format(exc.message),
                          file=sys.stderr)
            elif backend == "cli":
                raise AsError(
                    "cli_missing",
                    "未找到 hcloud（KooCLI），无法查询 AS 伸缩组列表。",
                    "安装 KooCLI 后重试（见 references/cli-installation-guide.md）。",
                )
        if used is None and backend in ("auto", "sdk"):
            pages = fetch_pages_sdk(
                args.region, args.limit, args.max_pages,
                name=args.name, group_id=args.group_id)
            used = "sdk"
    except AsError as exc:
        print(exc.message, file=sys.stderr)
        if exc.detail:
            print("详情: {0}".format(str(exc.detail)[:300]), file=sys.stderr)
        return None, None
    return pages, used


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)

    guard_message = guard_write_intent(argv)
    if guard_message:
        print(guard_message, file=sys.stderr)
        return 1

    parser = build_parser()
    args = parser.parse_args(argv)

    if args.limit < 1 or args.limit > MAX_LIMIT:
        print("--limit 取值须在 1~{0} 之间，当前为 {1}。".format(
            MAX_LIMIT, args.limit), file=sys.stderr)
        return 1
    if args.max_pages < 1:
        print("--max-pages 须大于 0。", file=sys.stderr)
        return 1
    if args.timeout < 1:
        print("--timeout 须大于 0。", file=sys.stderr)
        return 1
    if args.fuzzy and not args.name:
        print("提示: --fuzzy 仅在配合 --name 时生效。", file=sys.stderr)
    if args.status is not None and not valid_status(
            args.status, instance_mode=bool(args.group_id)):
        print("--status 取值无效: {0}。可选状态: INSERVICE/PAUSED/ERROR/"
              "DELETING/FREEZED、实例生命周期/健康状态，或 abnormal（仅异常）。".format(
                  args.status), file=sys.stderr)
        return 1

    pages, used_backend = _fetch(args)
    if used_backend is None:
        return 1

    group_id_mode = bool(args.group_id)

    if args.json:
        print(json.dumps(merge_pages(pages, group_id_mode, args.region),
                         ensure_ascii=False, indent=2))
        return 0

    if group_id_mode:
        instances = normalize_instances(pages, args.region, args.group_id)
        selected = filter_instances(instances, status=args.status)
        if not selected:
            if args.status:
                print("未找到匹配的实例（伸缩组: {0}，区域: {1}）。".format(
                    args.group_id, args.region))
                print("可去掉 --status 后重试，或确认实例生命周期/健康状态。")
            else:
                print("伸缩组 {0} 内无实例（区域: {1}）。".format(
                    args.group_id, args.region))
                print("确认伸缩组 ID 是否属于当前区域；扩容未生效时可检查"
                      "期望实例数与伸缩策略。")
            return 0

        abnormal_count = len([item for item in selected
                              if instance_is_abnormal(item)])
        if args.table:
            print(render_instance_table(selected))
        else:
            header = ["实例ID", "实例名", "生命周期状态", "健康状态"]
            rows = [[inst["instance_id"] or "", inst["instance_name"] or "",
                     inst["life_cycle_state"] or "-", inst["health_status"] or "-"]
                    for inst in selected]
            print(render_table(header, rows))
        print("\n共 {0} 个实例（伸缩组: {1}，区域: {2}，后端: {3}，异常: {4}）".format(
            len(selected), args.group_id, args.region, used_backend,
            abnormal_count))
        return 0

    groups = normalize_groups(pages, args.region)
    selected = filter_groups(groups, name=args.name, fuzzy=args.fuzzy,
                             status=args.status)
    if not selected:
        if args.name or args.status:
            print("未找到匹配的伸缩组（区域: {0}）。".format(args.region))
            print("可去掉过滤条件后重试，或确认伸缩组是否创建在其他区域。")
        else:
            print("当前区域无伸缩组（区域: {0}）。".format(args.region))
            print("可更换 --region（如 cn-north-1 / cn-east-3）后重试；"
                  "该账号也可能尚未创建伸缩组。")
        return 0

    abnormal_count = len([group for group in selected
                          if group_is_abnormal(group)])
    if args.table:
        print(render_group_table(selected))
    else:
        header = ["名称", "组ID", "状态"]
        rows = [[group["name"] or "", group["group_id"] or "",
                 group["status"] or "-"] for group in selected]
        print(render_table(header, rows))
    print("\n共 {0} 个伸缩组（区域: {1}，后端: {2}，异常: {3}）".format(
        len(selected), args.region, used_backend, abnormal_count))
    return 0


if __name__ == "__main__":
    sys.exit(main())