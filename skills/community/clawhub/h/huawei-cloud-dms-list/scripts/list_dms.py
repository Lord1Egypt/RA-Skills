#!/usr/bin/env python3
"""List Huawei Cloud DMS (Distributed Message Service) instances — Kafka and
RabbitMQ — via KooCLI, read-only.

Primary execution path is KooCLI:

    hcloud Kafka    ListInstances         --cli-region=<region> --engine=kafka
    hcloud RabbitMQ ListInstancesDetails  --cli-region=<region> --engine=rabbitmq

Both operations are GET /v2/{project_id}/instances (verified against the
official SDK `_http_info` metadata of huaweicloudsdkkafka v2 `KafkaClient.
list_instances` and huaweicloudsdkrabbitmq v2 `RabbitMQClient.
list_instances_details`). There is no `DMS` KooCLI service name — the engine
name IS the service name.

When the hcloud binary is not installed the script falls back to the official
SDKs (huaweicloudsdkkafka / huaweicloudsdkrabbitmq). Credentials are taken from
the active KooCLI profile or a fixed whitelist of AK/SK environment variable
names — the script never reads, echoes or stores secrets.

Three output modes: default compact instance-name list, `--table` full-field
table (实例ID/名称/引擎/版本/规格/状态/节点数/存储空间/创建时间/VPC/子网/
连接地址, missing values rendered as "-"), and `--json` raw instance array.
A strict write-intent guard rejects any mutating intent before a single command
is executed: this skill is read-only.

Usage:
    python3 scripts/list_dms.py [--region cn-north-4] [--engine all|kafka|rabbitmq]
                                [--names-only | --table | --json]
                                [--name demo] [--name-equal]
                                [--instance-id <id>] [--status RUNNING]
                                [--enterprise-project-id 0]
                                [--limit 50] [--offset 0] [--single-page]
                                [--project-id <id>]

Environment overrides (mostly for tests):
    DMS_LIST_HCLOUD_BIN   hcloud executable (default "hcloud")
    DMS_LIST_HCLOUD_ARGS  extra args injected before the DMS service/operation
"""

import argparse
import json
import os
import re
import subprocess
import sys

DEFAULT_REGION = "cn-north-4"
DEFAULT_LIMIT = 50          # server-side maximum page size for both engines
MAX_LIMIT = 50
DEFAULT_MAX_PAGES = 50
REST_PATH = "/v2/{project_id}/instances"

# KooCLI service name / operation per engine (there is no "DMS" service).
ENGINE_SERVICE = {"kafka": "Kafka", "rabbitmq": "RabbitMQ"}
ENGINE_OPERATION = {"kafka": "ListInstances", "rabbitmq": "ListInstancesDetails"}
ALLOWED_OPERATIONS = ("ListInstances", "ListInstancesDetails")

# Mutating DMS intents — strictly rejected by the guard. Gerund forms such as
# CREATING / DELETING / EXTENDING are legitimate *status* values and therefore
# are deliberately not listed here (the bare verbs still match operation names
# like CreateInstance / DeleteInstance after separator normalization).
WRITE_INTENT_KEYWORDS = (
    "createinstance",
    "deleteinstance",
    "batchdeleteinstance",
    "batchrestartorreset",
    "modifyinstance",
    "updateinstance",
    "resizeinstance",
    "scaleinstance",
    "restartinstance",
    "restartorflush",
    "resetpassword",
    "resetinstancepassword",
    "updateinstanceautotopic",
    "updateinstancesecurity",
    "createconnectortask",
    "deleteconnectortask",
    "create",
    "delete",
    "drop",
    "update",
    "modify",
    "resize",
    "scale",
    "restart",
    "reboot",
    "flush",
    "clear",
    "purge",
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
)

# Table columns: (header, candidate field names, formatter key). Ordered as
# required by the acceptance criteria.
TABLE_COLUMNS = (
    ("实例ID", ("instance_id", "instanceId", "id")),
    ("名称", ("name", "instance_name")),
    ("引擎", ("engine",)),
    ("版本", ("engine_version",)),
    ("规格", ("specification", "spec_code", "resource_spec_code", "product_id")),
    ("状态", ("status",)),
    ("节点数", ("node_num", "broker_num")),
    ("存储空间", ("storage_space", "total_storage_space")),
    ("创建时间", ("created_at", "created")),
    ("VPC", ("vpc_name", "vpc_id")),
    ("子网", ("subnet_name", "subnet_id")),
    ("连接地址", ("connect_address", "kafka_private_connect_address",
                  "public_connect_address", "management_connect_address")),
)

_INSTANCE_LIST_KEYS = ("instances", "instance_list", "instances_detail")

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


class DmsListError(Exception):
    """Base error for the DMS list skill."""


class GuardError(DmsListError):
    """A write intent was detected and blocked (skill is read-only)."""


class ConfigError(DmsListError):
    """hcloud missing / credentials (AK/SK) not configured / SDK unavailable."""


class HcloudMissingError(ConfigError):
    """The hcloud executable is not installed (triggers the SDK fallback)."""


class AuthError(DmsListError):
    """Authentication/authorization failure (invalid AK/SK or IAM 403)."""


class ApiError(DmsListError):
    """hcloud / network / unexpected API failure."""


def guard_write_intent(text):
    """Return False for read-only text; raise GuardError if `text` is mutating.

    Normalizes separators so `--create-instance`, `CreateInstance` and
    `create_instance` all hit the same keyword. Read-only vocabulary
    (list/show/get/describe) never matches.
    """
    low = re.sub(r"[\s_\-]+", "", str(text).lower())
    for keyword in WRITE_INTENT_KEYWORDS:
        if keyword in low:
            raise GuardError(
                "检测到写操作意图（关键词: %s）。本 skill 仅支持只读查询"
                "（Kafka ListInstances / RabbitMQ ListInstancesDetails），"
                "创建/删除/扩缩容/重启/清空等变更操作已被守卫拦截。"
                % keyword
            )
    return False


def guard_operation(engine, operation):
    """Only the read-only list operation of the selected engine may run."""
    allowed = ENGINE_OPERATION.get(engine)
    if allowed is None:
        raise GuardError(
            "不支持的引擎 %r：仅支持 kafka / rabbitmq / all。" % engine
        )
    if operation != allowed:
        raise GuardError(
            "不允许的操作 %r：引擎 %s 仅允许只读操作 %s。"
            % (operation, engine, allowed)
        )
    return True


def build_command(engine, region, name=None, instance_id=None, status=None,
                  exact_match_name=False, enterprise_project_id=None,
                  limit=DEFAULT_LIMIT, offset=0, project_id=None):
    """Build the hcloud argv (without the executable) for one engine page.

    Mirrors the real KooCLI parameter list (`hcloud Kafka ListInstances --help`
    / `hcloud RabbitMQ ListInstancesDetails --help`): --engine (required),
    --project_id (required; resolved from the profile when omitted), --limit
    (1..50), --offset (>=0), --name, --exact_match_name, --instance_id,
    --status, --enterprise_project_id. No parameter outside that list is ever
    emitted, and no mutating flag exists in this function.
    """
    service = ENGINE_SERVICE.get(engine)
    operation = ENGINE_OPERATION.get(engine)
    if service is None or operation is None:
        raise GuardError("不支持的引擎 %r：仅支持 kafka / rabbitmq。" % engine)
    argv = [
        service,
        operation,
        "--cli-region=%s" % region,
        "--engine=%s" % engine,
        "--limit=%d" % limit,
        "--offset=%d" % offset,
    ]
    if project_id:
        argv.append("--project_id=%s" % project_id)
    if name:
        argv.append("--name=%s" % name)
        if exact_match_name:
            argv.append("--exact_match_name=true")
    if instance_id:
        argv.append("--instance_id=%s" % instance_id)
    if status:
        argv.append("--status=%s" % status)
    if enterprise_project_id:
        argv.append("--enterprise_project_id=%s" % enterprise_project_id)
    return argv


def _hcloud_executable():
    return os.environ.get("DMS_LIST_HCLOUD_BIN", "hcloud")


def run_hcloud(argv):
    """Execute hcloud and return (stdout, stderr, returncode)."""
    cmd = [_hcloud_executable()]
    extra = os.environ.get("DMS_LIST_HCLOUD_ARGS", "").split()
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
            "真实参数清单可通过 `hcloud Kafka ListInstances --help` / "
            "`hcloud RabbitMQ ListInstancesDetails --help` 查看。详情：%s"
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
            "无权限访问分布式消息服务（DMS），请检查 IAM 权限"
            "（403：AK/SK 无效或未授予 DMS 只读权限），"
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
        for key in ("instance_num", "total_num", "total_count", "totalCount", "total"):
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


def _sdk_imports(engine):
    """Import the official SDK classes for one engine (no network)."""
    from huaweicloudsdkcore.auth.credentials import BasicCredentials
    from huaweicloudsdkcore.region.region import Region
    from huaweicloudsdkcore.http.http_config import HttpConfig
    if engine == "kafka":
        from huaweicloudsdkkafka.v2 import KafkaClient, ListInstancesRequest
        from huaweicloudsdkkafka.v2.region.kafka_region import KafkaRegion
        return (BasicCredentials, Region, HttpConfig,
                KafkaClient, ListInstancesRequest, KafkaRegion)
    if engine == "rabbitmq":
        from huaweicloudsdkrabbitmq.v2 import (
            RabbitMQClient, ListInstancesDetailsRequest,
        )
        from huaweicloudsdkrabbitmq.v2.region.rabbitmq_region import RabbitMQRegion
        return (BasicCredentials, Region, HttpConfig,
                RabbitMQClient, ListInstancesDetailsRequest, RabbitMQRegion)
    raise ConfigError("SDK 回退不支持引擎 %r。" % engine)


def _sdk_client(engine, region, project_id=None):
    """Build an official SDK client for one engine (credentials from env)."""
    try:
        (BasicCredentials, Region, HttpConfig,
         ClientClass, _RequestClass, RegionClass) = _sdk_imports(engine)
    except ImportError as exc:
        raise ConfigError(
            "未找到 hcloud（KooCLI），且官方 SDK（huaweicloudsdkcore + "
            "huaweicloudsdkkafka / huaweicloudsdkrabbitmq）未安装，"
            "无法回退到 SDK。请安装 KooCLI 或 pip install huaweicloudsdkcore "
            "huaweicloudsdkkafka huaweicloudsdkrabbitmq。详情：%s" % exc
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
            "SDK 回退缺少 project_id：DMS 的 REST 路径为 %s，需要项目 ID。"
            "请通过 --project-id 传入，或设置 HUAWEICLOUD_SDK_PROJECT_ID / "
            "HUAWEI_PROJECT_ID（严禁在对话中粘贴敏感信息）。" % REST_PATH
        )
    credentials = BasicCredentials(ak=ak, sk=sk, project_id=resolved_project_id)  # env-sourced, never literals
    try:
        try:
            region_obj = RegionClass.value_of(region)
        except (ValueError, KeyError, AttributeError):
            region_obj = Region(region, "https://dms.%s.myhuaweicloud.com" % region)
        return ClientClass.new_builder() \
            .with_credentials(credentials) \
            .with_region(region_obj) \
            .with_http_config(HttpConfig.get_default_config()) \
            .build()
    except Exception as exc:  # region unknown / config broken
        raise ConfigError(
            "SDK 初始化失败（engine=%s, region=%s）：%s。请检查官方 SDK 安装与区域配置。"
            % (engine, region, exc)
        )


def list_instances_via_sdk(engine, region, name=None, instance_id=None,
                           status=None, exact_match_name=False,
                           enterprise_project_id=None, limit=DEFAULT_LIMIT,
                           offset=0, project_id=None, max_pages=DEFAULT_MAX_PAGES,
                           allow_truncation=False, client=None):
    """SDK fallback for one engine (only used when hcloud is not installed).

    `KafkaClient.list_instances` / `RabbitMQClient.list_instances_details` are
    the official SDK counterparts of the two KooCLI operations; both hit
    GET /v2/{project_id}/instances. Request parameters are strings in the
    generated SDK models. Paging follows the response `instance_num`.
    """
    try:
        _, _, _, _, RequestClass, _ = _sdk_imports(engine)
    except ImportError as exc:
        raise ConfigError(
            "未找到 hcloud（KooCLI），且官方 SDK 未安装，无法回退到 SDK。"
            "请安装 KooCLI 或 pip install huaweicloudsdkcore "
            "huaweicloudsdkkafka huaweicloudsdkrabbitmq。详情：%s" % exc
        )
    sdk_client = client or _sdk_client(engine, region, project_id=project_id)
    call = (sdk_client.list_instances if engine == "kafka"
            else sdk_client.list_instances_details)
    instances = []
    current_offset = offset
    paged_out = False
    for _ in range(max_pages):
        request = RequestClass(
            engine=engine,
            name=name,
            instance_id=instance_id,
            status=status,
            exact_match_name="true" if exact_match_name and name else None,
            enterprise_project_id=enterprise_project_id,
            limit=str(limit),
            offset=str(current_offset),
        )
        try:
            response = call(request)
        except Exception as exc:
            low = str(exc).lower()
            if any(p in low for p in _AUTH_PATTERNS):
                raise AuthError(
                    "无权限访问分布式消息服务（DMS），请检查 IAM 权限（403）。详情：%s"
                    % str(exc)[:300]
                )
            raise ApiError("SDK 调用失败（engine=%s）：%s" % (engine, str(exc)[:300]))
        batch = list(response.instances or [])
        for item in batch:
            flat = _jsonable(item.to_dict())
            flat.setdefault("engine", engine)
            instances.append(flat)
        total = getattr(response, "instance_num", None)
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


def list_instances(engine, region, name=None, instance_id=None, status=None,
                   exact_match_name=False, enterprise_project_id=None,
                   limit=DEFAULT_LIMIT, offset=0, project_id=None,
                   max_pages=DEFAULT_MAX_PAGES, allow_truncation=False):
    """Query one engine's instances (offset-paged); KooCLI first, SDK fallback."""
    instances = []
    current_offset = offset
    paged_out = False
    for _page in range(max_pages):
        argv = build_command(
            engine, region, name=name, instance_id=instance_id, status=status,
            exact_match_name=exact_match_name,
            enterprise_project_id=enterprise_project_id,
            limit=limit, offset=current_offset, project_id=project_id,
        )
        try:
            stdout, stderr, returncode = run_hcloud(argv)
        except HcloudMissingError:
            # hcloud binary missing → one-shot SDK fallback (no CLI retry).
            return list_instances_via_sdk(
                engine, region, name=name, instance_id=instance_id,
                status=status, exact_match_name=exact_match_name,
                enterprise_project_id=enterprise_project_id,
                limit=limit, offset=offset, project_id=project_id,
                max_pages=max_pages, allow_truncation=allow_truncation,
            )
        if returncode != 0 or _USE_ERROR_MARKER in (stdout + " " + stderr).lower():
            # KooCLI usage errors print [USE_ERROR] on stdout with rc=0.
            raise classify_hcloud_failure(stdout, stderr, returncode)
        payload = extract_json(stdout)
        batch = extract_instances(payload)
        for item in batch:
            if isinstance(item, dict):
                item.setdefault("engine", engine)
        instances.extend(batch)
        if not _has_more(batch, len(instances), limit, payload):
            paged_out = True
            break
        current_offset += len(batch) if batch else limit
    if not paged_out and not allow_truncation:
        raise ApiError("翻页超过 %d 页仍未取完，已中止以防死循环。" % max_pages)
    return instances


def list_all_engines(region, engines, **kwargs):
    """Query the selected engines and concatenate their instances."""
    instances = []
    for engine in engines:
        instances.extend(list_instances(engine, region, **kwargs))
    return instances


def _field(instance, names, default="-"):
    for name in names:
        if isinstance(instance, dict) and instance.get(name) not in (None, ""):
            return instance[name]
    return default


def instance_names(instances):
    names = []
    for instance in instances:
        name = _field(instance, ("name", "instance_name"), default=None)
        if name is None:
            name = _field(instance, ("instance_id", "id"))
        names.append(str(name))
    return names


def _format_cell(header, value):
    if value in (None, ""):
        return "-"
    if header == "存储空间":
        try:
            return "%s GB" % int(value)
        except (TypeError, ValueError):
            return _cell(value)
    if isinstance(value, (list, tuple)):
        return ",".join(str(v) for v in value) or "-"
    return _cell(value)


def _cell(value):
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return str(value)


def render_table(instances):
    """Render the fixed 12-column full-field table (missing values as "-")."""
    headers = [header for header, _names in TABLE_COLUMNS]
    rows = []
    for instance in instances:
        rows.append([_format_cell(header, _field(instance, names))
                     for header, names in TABLE_COLUMNS])
    widths = [max(len(headers[i]), *(len(row[i]) for row in rows))
              for i in range(len(headers))]
    lines = [
        "  ".join(headers[i].ljust(widths[i]) for i in range(len(headers))),
        "  ".join("-" * w for w in widths),
    ]
    for row in rows:
        lines.append("  ".join(row[i].ljust(widths[i]) for i in range(len(headers))))
    return "\n".join(lines)


def _filter_suffix(args):
    filters = []
    if args.name:
        filters.append("name=%s" % args.name)
    if args.instance_id:
        filters.append("instance_id=%s" % args.instance_id)
    if args.status:
        filters.append("status=%s" % args.status)
    if args.enterprise_project_id:
        filters.append("enterprise_project_id=%s" % args.enterprise_project_id)
    return "（过滤条件: %s）" % ", ".join(filters) if filters else ""


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="查询华为云 DMS（分布式消息服务）实例列表 —— "
                    "Kafka / RabbitMQ，只读（KooCLI hcloud Kafka ListInstances / "
                    "hcloud RabbitMQ ListInstancesDetails）。")
    parser.add_argument("-r", "--region", default=DEFAULT_REGION,
                        help="目标 Region（默认 %s）" % DEFAULT_REGION)
    parser.add_argument("--engine", choices=("all", "kafka", "rabbitmq"),
                        default="all",
                        help="消息引擎：kafka / rabbitmq / all（默认 all，两个都查）")
    parser.add_argument("--names-only", action="store_true", dest="names_only",
                        help="仅输出实例名称清单（默认即名称清单模式）")
    parser.add_argument("--json", action="store_true", dest="as_json",
                        help="以 JSON 输出完整原始字段数组")
    parser.add_argument("--table", action="store_true", dest="as_table",
                        help="输出全字段表格（实例ID/名称/引擎/版本/规格/状态/"
                             "节点数/存储空间/创建时间/VPC/子网/连接地址）")
    parser.add_argument("--name",
                        help="按实例名称过滤（服务端查询参数，模糊匹配）")
    parser.add_argument("--name-equal", action="store_true", dest="name_equal",
                        help="按实例名称精确匹配（转发服务端 exact_match_name=true）")
    parser.add_argument("--instance-id", dest="instance_id",
                        help="按实例 ID 过滤（服务端查询参数）")
    parser.add_argument("--status",
                        help="按实例状态过滤（服务端查询参数，如 RUNNING/ERROR）")
    parser.add_argument("--enterprise-project-id", dest="enterprise_project_id",
                        help="按企业项目 ID 过滤（服务端查询参数）")
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
    parser.add_argument("--operation", default=None,
                        help="hcloud 操作名（仅允许只读 ListInstances / "
                             "ListInstancesDetails；缺省按引擎自动选择）")
    args = parser.parse_args(argv)

    try:
        # Write-intent guard: scan the raw argv + validate the operation name.
        guard_write_intent(" ".join(argv if argv is not None else sys.argv[1:]))
        for value in (args.name, args.instance_id, args.status,
                      args.enterprise_project_id):
            if value:
                guard_write_intent(value)
        engines = (["kafka", "rabbitmq"] if args.engine == "all"
                   else [args.engine])
        for engine in engines:
            guard_operation(engine, args.operation or ENGINE_OPERATION[engine])
        if args.limit < 1 or args.limit > MAX_LIMIT:
            raise ApiError("--limit 超出范围（1~%d）：%d" % (MAX_LIMIT, args.limit))
        if args.offset < 0:
            raise ApiError("--offset 不能为负数：%d" % args.offset)
        if args.max_pages < 1:
            raise ApiError("--max-pages 必须 ≥ 1：%d" % args.max_pages)
        instances = list_all_engines(
            args.region,
            engines,
            name=args.name,
            instance_id=args.instance_id,
            status=args.status,
            exact_match_name=args.name_equal,
            enterprise_project_id=args.enterprise_project_id,
            limit=args.limit,
            offset=args.offset,
            project_id=args.project_id,
            max_pages=1 if args.single_page else args.max_pages,
            allow_truncation=args.single_page,
        )
    except DmsListError as exc:
        print("[错误] %s" % exc, file=sys.stderr)
        return 1

    if args.as_json:
        print(json.dumps(instances, ensure_ascii=False, indent=2))
        return 0

    if not instances:
        print("当前区域（%s）无 DMS 实例%s。" % (args.region, _filter_suffix(args)))
        return 0

    if args.as_table:
        print("Region %s 的 DMS 实例列表（共 %d 个，engine=%s）："
              % (args.region, len(instances), args.engine))
        print(render_table(instances))
        return 0

    # Default output mode: the compact instance-name list (--names-only).
    print("Region %s 的 DMS 实例名称列表（共 %d 个）："
          % (args.region, len(instances)))
    for name in instance_names(instances):
        print("- %s" % name)
    return 0


if __name__ == "__main__":
    sys.exit(main())