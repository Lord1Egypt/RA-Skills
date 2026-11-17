#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Query the Huawei Cloud CDM (Cloud Data Migration) clusters of the current
account (read-only) and render them as a table / JSON / Markdown / CSV.

The skill exposes the two read-only CDM cluster-management APIs:

- ``ListClusters`` — every CDM cluster in the project
  (``GET /v1.1/{project_id}/clusters``). The official API takes **no** query
  parameters (verified in the ``huaweicloudsdkcdm`` v1
  ``_list_clusters_http_info`` metadata: ``ListClustersRequest.attribute_map``
  is empty), so one call returns the whole list; ``--name`` / ``--status``
  filtering is applied client-side.
- ``ShowClusterDetail`` — the details of one cluster
  (``GET /v1.1/{project_id}/clusters/{cluster_id}``). The KooCLI / SDK
  operation name is ``ShowClusterDetail`` (the API-explorer title “查询集群详
  情”); there is no ``ShowCluster`` operation in either.

KooCLI (``hcloud CDM ListClusters`` / ``hcloud CDM ShowClusterDetail``) is the
primary execution path; when the hcloud binary is absent the script falls back
to the official ``huaweicloudsdkcdm`` v1 SDK (``CdmClient``), which resolves the
project id from ``BasicCredentials`` automatically (querying IAM when needed).

A strict write-intent guard rejects any mutating intent so writes never happen:
the only operations ever constructed are the two read-only ones above. Nothing
is ever written back to the cloud.

Usage:
    python3 scripts/list_cdm_clusters.py [--region cn-north-4]
                                         [--format table|json|markdown|csv]
                                         [--output /path/out.json]
                                         [--cluster-id <uuid>]
                                         [--name <cluster-name>]
                                         [--status 200] [--status 300 ...]
                                         [--summary]
                                         [--max-calls 1]

Environment overrides (mostly for tests):
    CDM_LIST_HCLOUD_BIN    hcloud executable (default "hcloud")
    CDM_LIST_HCLOUD_ARGS   extra args appended AFTER the read-only argv
                           (guard-scanned, read-only)
    CDM_LIST_SQC_BIN       skill-quality-cli executable override
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
DEFAULT_FORMAT = "table"
SERVICE = "CDM"

# Read-only operations this skill is allowed to call.
ALLOWED_OPERATIONS = ("ListClusters", "ShowClusterDetail")
DEFAULT_OPERATION = "ListClusters"
DETAIL_OPERATION = "ShowClusterDetail"

# Official REST paths (verified in the huaweicloudsdkcdm v1 *_http_info
# metadata and the CDM API reference).
REST_PATHS = {
    "ListClusters": "/v1.1/{project_id}/clusters",
    "ShowClusterDetail": "/v1.1/{project_id}/clusters/{cluster_id}",
}

# Cluster status codes (CDM API reference) and their meaning — used to enrich
# the table output and to match human-readable --status values.
CLUSTER_STATUS_MEANINGS = {
    "100": "创建中",
    "200": "正常",
    "300": "失败",
    "303": "创建失败",
    "500": "重启中",
    "800": "冻结",
    "900": "已关机",
    "910": "正在关机",
    "920": "正在开机",
}

# Skill-quality telemetry: every hcloud call on the script execution path is
# reported through skill-quality-cli. When the CLI is unavailable — or
# SKILL_QUALITY_REPORT=0 — the call degrades to bare hcloud.
SKILL_QUALITY_SKILL_NAME = "huawei-cloud-cdm-list"
_QUALITY_OFF_VALUES = ("0", "false", "no", "off")

# Markdown report column order for the cluster list view.
CLUSTER_MD_HEADERS = [
    "集群 ID", "名称", "状态", "状态说明", "版本", "节点数", "规格", "AZ",
    "公网 IP", "创建时间",
]

CLUSTER_MD_DETAIL_HEADERS = [
    "字段", "值",
]

_FIELD_MISSING = "-"

# Mutating CDM operations / intents — strictly rejected by the guard. CDM
# write-side operations (from the KooCLI CLI reference) come first, then the
# generic write vocabulary.
WRITE_INTENT_KEYWORDS = (
    "createcluster",
    "deletecluster",
    "modifycluster",
    "restartcluster",
    "startcluster",
    "stopcluster",
    "createandstartrandomclusterjob",
    "createjob",
    "deletejob",
    "submitjob",
    "canceljob",
    "startjob",
    "stopjob",
    "createlink",
    "deletelink",
    "create",
    "delete",
    "update",
    "modify",
    "restart",
    "reboot",
    "resize",
    "expand",
    "shrink",
    "start",
    "stop",
    "enable",
    "disable",
    "destroy",
    "remove",
    "reset",
    "attach",
    "detach",
)

# Read-only option flags whose *values* are filter/output data (e.g. a cluster
# named "cdm-delete-test", a report path such as "cdm-delete-report.json").
# Their values must NOT be scanned by the write-intent guard.
_VALUE_STRIPPED_FLAGS = (
    "--region",
    "-r",
    "--format",
    "-f",
    "--output",
    "-o",
    "--cluster-id",
    "--cluster_id",
    "--name",
    "--status",
    "--limit",
    "--max-calls",
    "--page-size",
    "--max-pages",
    "--language",
)

# Preferred column order for the table / CSV views; remaining keys are
# appended. Keys are the *normalized* (snake_case) field names.
CLUSTER_PREFERRED_COLUMNS = [
    "id",
    "name",
    "status",
    "status_detail",
    "status_meaning",
    "version",
    "instance_count",
    "instances",
    "flavor_name",
    "az_name",
    "public_endpoint",
    "is_frozen",
    "created",
    "updated",
]

# Raw nested API objects that are already represented by derived flat columns
# (``datastore`` → ``version`` / ``datastore_type``). Dropped from the flat
# table / CSV / detail views so the row does not carry the same data twice;
# ``--format json`` still returns the untouched API record.
CLUSTER_FLAT_EXCLUDED_COLUMNS = ("datastore",)

# AK/SK environment variable names, read *directly* (never by enumerating
# os.environ). The SDK fallback resolves them explicitly; hcloud reads its own
# profile.
_AK_ENV_NAMES = (
    "HUAWEICLOUD_SDK_AK",
    "CLOUD_SDK_AK",
    "HUAWEI_ACCESS_KEY",
    "HW_ACCESS_KEY",
    "HWC_ACCESS_KEY",
    "HUAWEI_AK",
    "HW_AK",
)
_SK_ENV_NAMES = (
    "HUAWEICLOUD_SDK_SK",
    "CLOUD_SDK_SK",
    "HUAWEI_SECRET_KEY",
    "HW_SECRET_KEY",
    "HWC_SECRET_KEY",
    "HUAWEI_SK",
    "HW_SK",
)
_PROJECT_ID_ENV_NAMES = (
    "HUAWEICLOUD_SDK_PROJECT_ID",
    "CLOUD_SDK_PROJECT_ID",
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
    "cdm:cluster:list",
    "cdm:cluster:get",
    "认证失败",
    "权限不足",
    "没有操作权限",
)

# KooCLI prints usage errors (e.g. "[USE_ERROR]Invalid parameter: xxx") on
# stdout WITH exit code 0 — the marker is treated as a hard failure.
_USE_ERROR_MARKER = "[use_error]"


class CdmListError(Exception):
    """Base error for the CDM cluster list skill."""


class GuardError(CdmListError):
    """A write intent was detected and blocked (skill is read-only)."""


class ConfigError(CdmListError):
    """hcloud/SDK missing or credentials (AK/SK) not configured."""


class AuthError(CdmListError):
    """Authentication/authorization failure (invalid AK/SK or IAM 403)."""


class ApiError(CdmListError):
    """hcloud / network / unexpected API failure."""


class ExportError(CdmListError):
    """The export file could not be produced (bad path / write failure)."""


def guard_write_intent(text):
    """Raise GuardError if ``text`` carries a mutating intent.

    Normalizes separators so ``--create-cluster``, ``CreateCluster``, and
    ``create_cluster`` all hit the same keyword. Read-only vocabulary
    (list/show/count) never matches.
    """
    low = re.sub(r"[\s_\-]+", "", str(text).lower())
    for keyword in WRITE_INTENT_KEYWORDS:
        if keyword in low:
            raise GuardError(
                "检测到写操作意图（关键词: %s）。本 skill 仅支持 CDM 只读查询"
                "（ListClusters / ShowClusterDetail），创建/删除/重启/扩容等"
                "变更操作已被守卫拦截。" % keyword
            )
    return False


def guard_operation(operation):
    """Only the two read-only CDM operations may be executed."""
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


def resolve_operation(cluster_id=None, explicit=None):
    """Pick the read-only operation from the user's intent.

    ``--cluster-id`` selects ShowClusterDetail; otherwise the cluster list
    (ListClusters) is used. An explicit ``--operation`` value is honoured (and
    later validated against the allow-list).
    """
    if cluster_id:
        return DETAIL_OPERATION
    if explicit:
        return explicit
    return DEFAULT_OPERATION


def build_command(operation, region, cluster_id=None, language=None):
    """Build the hcloud CDM argv (without the executable).

    Mirrors the real KooCLI parameter list for the two read-only operations.
    ``project_id`` is a required path parameter for CDM; when omitted KooCLI
    resolves it from the active profile. ListClusters takes **no** query
    parameters (the official API has none), so none are added.
    """
    argv = [SERVICE, operation, "--cli-region=%s" % region]
    if language:
        argv.append("--X-Language=%s" % language)
    if operation == "ListClusters":
        pass
    elif operation == DETAIL_OPERATION:
        if not cluster_id:
            raise ApiError(
                "ShowClusterDetail（集群详情）需要提供 --cluster-id。"
                "可先执行默认列表查询获取集群 ID。"
            )
        argv.append("--cluster_id=%s" % cluster_id)
    return argv


def _hcloud_executable():
    return os.environ.get("CDM_LIST_HCLOUD_BIN") or "hcloud"


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
    override = os.environ.get("CDM_LIST_SQC_BIN")
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
    extra = os.environ.get("CDM_LIST_HCLOUD_ARGS", "").split()
    if extra:
        cmd.extend(extra)
    return cmd


def build_hcloud_command(argv):
    """Build the hcloud execution argv, wrapping it with skill-quality-cli.

    Every CLI call is reported as ``skill-quality-cli run --skill-name
    huawei-cloud-cdm-list -- hcloud ...`` (the mandatory wrapping 口径, enforced
    here on the script path). The command degrades to bare hcloud when the
    telemetry CLI is missing or ``SKILL_QUALITY_REPORT=0``; an explicit
    ``CDM_LIST_HCLOUD_BIN`` override (offline mock / verification) is run
    verbatim. When hcloud itself is not resolvable the wrapping is skipped so
    ``run_hcloud`` raises ``FileNotFoundError`` → ``ConfigError`` → SDK fallback.
    """
    hcloud_cmd = _hcloud_argv(argv)
    if os.environ.get("CDM_LIST_HCLOUD_BIN"):
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
    extra = os.environ.get("CDM_LIST_HCLOUD_ARGS", "").split()
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
            "hcloud 参数错误（KooCLI 拒绝了该参数组合，退出码 %s）：CDM 真实参数清单"
            "可通过 `hcloud CDM ListClusters --cli-region=<region> --help` 查看。"
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
            "无权限访问云数据迁移服务（CDM），请检查 IAM 权限"
            "（403：AK/SK 无效或未授予 cdm:cluster:list / cdm:cluster:get 权限），"
            "参见 references/iam-policies.md。详情：%s" % blob[:300]
        )
    return ApiError(
        "hcloud 调用失败（退出码 %s）：%s" % (returncode, blob[:300])
    )


def _payload_error(payload):
    """Return the error text if a response payload is an error envelope.

    KooCLI returns HTTP-level API errors (e.g. 403 permission envelopes) as a
    body on **stdout with exit code 0**. Such an envelope must be surfaced as
    an explicit error, never silently treated as an empty list.
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


def extract_clusters(payload):
    """Pull the cluster list out of a ListClusters response payload.

    Accepts the official camelCase envelope ``{"clusters": [...]}`` (returned
    by hcloud) and plain lists (defensive).
    """
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        value = payload.get("clusters")
        if isinstance(value, list):
            return value
    return []


def _env_value(names):
    for name in names:
        value = os.environ.get(name)
        if value:
            return value
    return None


def _jsonable(value):
    return json.loads(json.dumps(value, ensure_ascii=False, default=str))


def _sdk_credentials():
    """Build BasicCredentials from the whitelisted environment variables."""
    ak = _env_value(_AK_ENV_NAMES)
    sk = _env_value(_SK_ENV_NAMES)
    if not ak or not sk:
        raise ConfigError(
            "SDK 回退缺少 AK/SK 凭证：当前环境未检测到白名单中的 AK/SK 环境变量"
            "（如 HUAWEICLOUD_SDK_AK / CLOUD_SDK_AK 与 HUAWEICLOUD_SDK_SK /"
            " CLOUD_SDK_SK）。请在会话外设置其中之一（严禁在对话中粘贴 AK/SK），"
            "或安装 KooCLI 并配置 profile，参见 references/cli-installation-guide.md。"
        )
    project_id = _env_value(_PROJECT_ID_ENV_NAMES)
    try:
        # project_id may stay None: the SDK queries IAM and resolves it per region.
        from huaweicloudsdkcore.auth.credentials import BasicCredentials
        return BasicCredentials(ak=ak, sk=sk, project_id=project_id)  # env-sourced, never literals
    except ImportError as exc:
        raise ConfigError(
            "未找到 hcloud（KooCLI），且 huaweicloudsdkcore 未安装，无法回退到"
            " SDK。请安装 KooCLI 或先运行 `python3 scripts/ensure_env.py`。详情：%s"
            % exc
        )


def _sdk_client(region):
    """Build the huaweicloudsdkcdm v1 CdmClient for the given region."""
    try:
        from huaweicloudsdkcdm.v1 import CdmClient
        from huaweicloudsdkcdm.v1.region.cdm_region import CdmRegion
    except ImportError as exc:
        raise ConfigError(
            "未找到 hcloud（KooCLI），且 huaweicloudsdkcdm 未安装，无法回退到"
            " SDK。请安装 KooCLI 或先运行 `python3 scripts/ensure_env.py`"
            "（pip install huaweicloudsdkcore huaweicloudsdkcdm）。详情：%s" % exc
        )
    try:
        try:
            region_obj = CdmRegion.value_of(region)
        except (ValueError, KeyError, AttributeError):
            from huaweicloudsdkcore.region.region import Region
            region_obj = Region(region, "https://cdm.%s.myhuaweicloud.com" % region)
        from huaweicloudsdkcore.http.http_config import HttpConfig
        client = CdmClient.new_builder() \
            .with_credentials(_sdk_credentials()) \
            .with_region(region_obj) \
            .with_http_config(HttpConfig.get_default_config()) \
            .build()
    except ConfigError:
        raise
    except Exception as exc:
        raise ConfigError(
            "SDK 初始化失败（region=%s）：%s。请检查 huaweicloudsdkcdm 安装与区域"
            "配置。" % (region, exc)
        )
    return client


def _sdk_call(fn, request):
    try:
        return fn(request)
    except Exception as exc:
        low = str(exc).lower()
        if any(p in low for p in _AUTH_PATTERNS):
            raise AuthError(
                "无权限访问云数据迁移服务（CDM），请检查 IAM 权限"
                "（cdm:cluster:list / cdm:cluster:get，403）。详情：%s"
                % str(exc)[:300]
            )
        raise ApiError("SDK 调用失败：%s" % str(exc)[:300])


def list_clusters_via_sdk(region):
    """SDK fallback: list CDM clusters through ``huaweicloudsdkcdm`` v1."""
    client = _sdk_client(region)
    from huaweicloudsdkcdm.v1 import ListClustersRequest
    response = _sdk_call(client.list_clusters, ListClustersRequest())
    clusters = [_jsonable(c.to_dict()) for c in (response.clusters or [])]
    return clusters


def show_cluster_via_sdk(region, cluster_id):
    """SDK fallback: query one CDM cluster through ``huaweicloudsdkcdm`` v1."""
    client = _sdk_client(region)
    from huaweicloudsdkcdm.v1 import ShowClusterDetailRequest
    request = ShowClusterDetailRequest(cluster_id=cluster_id)
    response = _sdk_call(client.show_cluster_detail, request)
    return _jsonable(response.to_dict())


def list_clusters(region, max_calls=1):
    """Query the CDM cluster list; KooCLI first, SDK fallback on missing hcloud.

    The official ListClusters API takes no query parameters — one call returns
    the whole list, so ``max_calls > 1`` would re-fetch the same page. De-dupe
    by cluster id and stop as soon as a call adds nothing new; ``max_calls`` is
    a defensive ceiling, it never adds parameters to the API call.
    """
    items = []
    seen = set()
    for _call in range(max(1, max_calls)):
        argv = build_command("ListClusters", region)
        try:
            stdout, stderr, returncode = run_hcloud(argv)
        except ConfigError:
            return list_clusters_via_sdk(region)
        if returncode != 0 or _USE_ERROR_MARKER in (stdout + " " + stderr).lower():
            raise classify_hcloud_failure(stdout, stderr, returncode)
        payload = extract_json(stdout)
        err_text = _payload_error(payload)
        if err_text:
            raise classify_hcloud_failure("", err_text, returncode)
        batch = extract_clusters(payload)
        added = 0
        for record in batch:
            key = record.get("id") if isinstance(record, dict) else None
            if key is None:
                items.append(record)
                added += 1
                continue
            key = str(key)
            if key in seen:
                continue
            seen.add(key)
            items.append(record)
            added += 1
        if not added:
            break
    return items


def show_cluster(region, cluster_id):
    """Query one CDM cluster's details; KooCLI first, SDK fallback."""
    argv = build_command(DETAIL_OPERATION, region, cluster_id=cluster_id)
    try:
        stdout, stderr, returncode = run_hcloud(argv)
    except ConfigError:
        return show_cluster_via_sdk(region, cluster_id)
    if returncode != 0 or _USE_ERROR_MARKER in (stdout + " " + stderr).lower():
        raise classify_hcloud_failure(stdout, stderr, returncode)
    payload = extract_json(stdout)
    err_text = _payload_error(payload)
    if err_text:
        raise classify_hcloud_failure("", err_text, returncode)
    return payload if isinstance(payload, dict) else {}


def _camel_to_snake(name):
    text = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", str(name))
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", text).lower()


def _instance_summary(instance):
    """Compact per-instance summary: name(status[, public_ip, traffic_ip])."""
    name = instance.get("name") or instance.get("id") or _FIELD_MISSING
    status = str(instance.get("status") or _FIELD_MISSING)
    ips = [instance.get(k) for k in ("publicIp", "trafficIp", "manageIp",
                                     "private_ip")]
    ip_text = ",".join(str(ip) for ip in ips if ip)
    inside = status if not ip_text else "%s,%s" % (status, ip_text)
    return "%s(%s)" % (name, inside)


def normalize_cluster(record, detail=False):
    """Flatten a CDM cluster record (camelCase API → snake_case table rows).

    Computes the derived ``version`` (``datastore.version``), ``instance_count``
    and ``status_meaning``; flattens ``instances`` into a compact
    ``name(id,status)`` summary for table/CSV while keeping the raw list intact
    for JSON.
    """
    if not isinstance(record, dict):
        return {}
    flat = {}
    for key, value in record.items():
        flat[_camel_to_snake(key)] = value
    datastore = record.get("datastore") or {}
    if isinstance(datastore, dict):
        flat["version"] = datastore.get("version") or _FIELD_MISSING
        flat["datastore_type"] = datastore.get("type") or _FIELD_MISSING
    else:
        flat.setdefault("version", _FIELD_MISSING)
        flat.setdefault("datastore_type", _FIELD_MISSING)
    instances = record.get("instances") or []
    if isinstance(instances, list):
        flat["instance_count"] = len(instances)
        flat["instances"] = "; ".join(
            _instance_summary(i) for i in instances if isinstance(i, dict)
        ) or _FIELD_MISSING
    else:
        flat["instance_count"] = _FIELD_MISSING
        flat["instances"] = _FIELD_MISSING
    status = flat.get("status")
    if status is not None and str(status) in CLUSTER_STATUS_MEANINGS:
        flat["status_meaning"] = CLUSTER_STATUS_MEANINGS[str(status)]
    else:
        flat["status_meaning"] = flat.get("status_detail") or _FIELD_MISSING
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


def _filter_clusters(items, name=None, statuses=None):
    """Client-side cluster filtering (the CDM API has no server-side filters).

    ``name`` matches case-insensitively as a substring; each ``--status`` value
    matches the cluster status code OR the human-readable meaning
    (e.g. ``200`` or ``正常``), case-insensitively.
    """
    wanted_statuses = [str(s).strip().lower() for s in (statuses or []) if str(s).strip()]
    selected = []
    for item in items:
        if name:
            item_name = str(item.get("name") or "")
            if name.lower() not in item_name.lower():
                continue
        if wanted_statuses:
            status = str(item.get("status") or "")
            meaning = CLUSTER_STATUS_MEANINGS.get(status, "")
            status_detail = str(item.get("statusDetail") or "")
            if not any(w == status.lower() or w == meaning.lower()
                       or w == status_detail.lower() for w in wanted_statuses):
                continue
        selected.append(item)
    return selected


def render_table(items, detail=False):
    """Render the aligned table (cluster list view or detail key/value view)."""
    if detail:
        record = items[0] if isinstance(items, list) else items
        return _render_detail_table(record or {})
    rows_data = [normalize_cluster(i) for i in items]
    columns = [c for c in _columns(rows_data, CLUSTER_PREFERRED_COLUMNS)
               if c not in CLUSTER_FLAT_EXCLUDED_COLUMNS]
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


def _render_detail_table(record):
    """Render a single cluster's details as a field/value table."""
    flat = normalize_cluster(record, detail=True)
    preferred = [
        "id", "name", "status", "status_meaning", "status_detail", "version",
        "datastore_type", "instance_count", "instances", "flavor_name",
        "az_name", "public_endpoint", "is_frozen", "created", "updated",
        "vpc_id", "subnet_id", "security_group_id", "namespace", "cluster_mode",
        "config_status", "eps_id",
    ]
    ordered = [k for k in preferred if k in flat and flat[k] is not None]
    for key in sorted(flat):
        if (key not in ordered and flat[key] is not None
                and key not in CLUSTER_FLAT_EXCLUDED_COLUMNS):
            ordered.append(key)
    lines = ["字段        值", "----------  ----------"]
    for key in ordered:
        value = _cell(flat[key])
        lines.append("%s  %s" % (key.ljust(10), value))
    return "\n".join(lines)


def _cluster_md_row(flat):
    """Build one Markdown row from an *already normalized* record.

    Normalization happens exactly once, in ``render_markdown``. Re-normalizing
    here would see ``instances`` as a string and overwrite ``instance_count`` /
    ``instances`` with the missing marker (breaking the 节点数 column).
    """
    return [
        _md_escape(_field(flat, "id")),
        _md_escape(_field(flat, "name")),
        _md_escape(_field(flat, "status")),
        _md_escape(_field(flat, "status_meaning")),
        _md_escape(_field(flat, "version")),
        _md_escape(_field(flat, "instance_count")),
        _md_escape(_field(flat, "flavor_name")),
        _md_escape(_field(flat, "az_name")),
        _md_escape(_field(flat, "public_endpoint")),
        _md_escape(_field(flat, "created")),
    ]


def render_markdown(items, summary=False, region=None, detail_record=None):
    """Render the clusters as a GitHub-flavored Markdown table.

    An empty list still renders a valid (header-only) table.
    """
    if detail_record is not None:
        flat = normalize_cluster(detail_record, detail=True)
        ordered = [k for k in flat if k not in CLUSTER_FLAT_EXCLUDED_COLUMNS]
        lines = [
            "| 字段 | 值 |",
            "| --- | --- |",
        ]
        for key in ordered:
            if flat[key] is None:
                continue
            lines.append("| %s | %s |" % (_md_escape(key), _md_escape(flat[key])))
        return "\n".join(lines)
    rows_data = [normalize_cluster(i) for i in items]
    headers = CLUSTER_MD_HEADERS
    body = [_cluster_md_row(r) for r in rows_data]
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in body:
        lines.append("| " + " | ".join(row) + " |")
    if summary:
        lines.append("")
        lines.append("**汇总**：共 %d 个 CDM 集群（Region %s）。"
                     % (len(items), region or _FIELD_MISSING))
    return "\n".join(lines)


def render_csv(items, detail=False):
    if detail:
        raise ApiError("--format csv 不支持集群详情视图，请使用 table/json/markdown。")
    rows_data = [normalize_cluster(i) for i in items]
    columns = [c for c in _columns(rows_data, CLUSTER_PREFERRED_COLUMNS)
               if c not in CLUSTER_FLAT_EXCLUDED_COLUMNS] or ["(empty)"]
    buffer = io.StringIO()
    writer = csv.writer(buffer, lineterminator="\n")
    writer.writerow(columns)
    for record in rows_data:
        writer.writerow([_cell(_field(record, col)) for col in columns])
    return buffer.getvalue().rstrip("\n")


def render_json(items):
    return json.dumps(items, ensure_ascii=False, indent=2)


def _render(items, fmt, summary=False, region=None, detail_record=None):
    if fmt == "json":
        return render_json(items)
    if fmt == "markdown":
        return render_markdown(items, summary=summary, region=region,
                               detail_record=detail_record)
    if fmt == "csv":
        return render_csv(items, detail=detail_record is not None)
    return render_table(items, detail=detail_record is not None)


def _extension(fmt):
    return "md" if fmt == "markdown" else fmt


def default_output_path(operation, region, fmt):
    prefix = "cdm_clusters" if operation == "ListClusters" else "cdm_cluster_detail"
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return "%s_%s_%s.%s" % (prefix, region, stamp, _extension(fmt))


def export_report(text, output_path):
    """Write the rendered report to ``output_path`` (atomic rename).

    Raises ExportError on an unusable path / write failure; no partial file is
    left behind.
    """
    output_path = os.path.abspath(output_path)
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.isdir(output_dir):
        try:
            os.makedirs(output_dir, exist_ok=True)
        except OSError as exc:
            raise ExportError(
                "无法创建输出目录 %r：%s。请检查 --output 路径。" % (output_dir, exc)
            )
    fd, tmp_path = tempfile.mkstemp(prefix=".cdm_", suffix=".tmp",
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


def active_filter_descriptions(name=None, statuses=None, cluster_id=None):
    filters = []
    if cluster_id:
        filters.append("cluster_id=%s" % cluster_id)
    if name:
        filters.append("name=%s" % name)
    if statuses:
        filters.append("status=%s" % ",".join(str(s) for s in statuses))
    return filters


def parse_args(argv):
    parser = argparse.ArgumentParser(
        description="查询华为云 CDM（云数据迁移）集群列表与详情（只读）。")
    parser.add_argument("-r", "--region", default=DEFAULT_REGION,
                        help="目标 Region（默认 %s）" % DEFAULT_REGION)
    parser.add_argument("-f", "--format", default=DEFAULT_FORMAT,
                        choices=["table", "json", "markdown", "md", "csv"],
                        help="输出格式：table（默认）/ json / markdown（md）/ csv")
    parser.add_argument("-o", "--output", default=None,
                        help="导出文件路径（json/markdown/csv；默认 "
                             "cdm_<view>_<region>_<timestamp>.<ext>）")
    parser.add_argument("--summary", action="store_true",
                        help="markdown 报表末尾追加汇总行")
    parser.add_argument("--cluster-id", dest="cluster_id", default=None,
                        help="集群 ID（指定后走 ShowClusterDetail 查询集群详情）")
    parser.add_argument("--name", default=None,
                        help="按集群名称过滤（客户端模糊匹配，不区分大小写）")
    parser.add_argument("--status", action="append", default=None,
                        help="按集群状态过滤，可重复（状态码 100/200/300/303/500/"
                             "800/900/910/920，或语义值如 正常/创建中/失败/冻结/已关机；"
                             "多值取并集）")
    parser.add_argument("--max-calls", type=int, default=1, dest="max_calls",
                        help="ListClusters 防御性调用上限（官方 API 无分页参数，"
                             "单次调用即全量；默认 1）")
    parser.add_argument("--operation", default=None,
                        help="显式指定只读操作（ListClusters / ShowClusterDetail）")
    return parser.parse_args(argv)


def main(argv=None):
    raw_argv = argv if argv is not None else sys.argv[1:]

    # Write-intent guard runs on the RAW argv BEFORE argparse, so that a
    # mutating flag is reported as a guard violation rather than an argparse
    # "unrecognized argument" error.
    try:
        guard_write_intent(guard_text_from_argv(raw_argv))
    except CdmListError as exc:
        print("[错误] %s" % exc, file=sys.stderr)
        return 1

    args = parse_args(argv)

    detail_record = None
    try:
        operation = resolve_operation(cluster_id=args.cluster_id,
                                      explicit=args.operation)
        guard_operation(operation)
        if args.cluster_id and args.operation and args.operation != DETAIL_OPERATION:
            raise ApiError(
                "同时给出 --cluster-id 与 --operation 时，operation 必须是"
                " ShowClusterDetail。"
            )
        if args.max_calls is None or args.max_calls < 1:
            raise ApiError("--max-calls 必须是正整数：%s" % args.max_calls)
        if args.cluster_id:
            detail_record = show_cluster(args.region, args.cluster_id)
            items = [detail_record]
        else:
            items = list_clusters(args.region, max_calls=args.max_calls)
            items = _filter_clusters(items, name=args.name,
                                     statuses=args.status)
    except CdmListError as exc:
        print("[错误] %s" % exc, file=sys.stderr)
        return 1

    filters = active_filter_descriptions(name=args.name, statuses=args.status,
                                         cluster_id=args.cluster_id)
    filter_suffix = "（过滤条件: %s）" % ", ".join(filters) if filters else ""

    fmt = "markdown" if args.format == "md" else args.format

    if fmt == "table":
        if args.cluster_id:
            if not detail_record:
                print("集群 %s 无详情结果。" % args.cluster_id)
            else:
                print("CDM 集群详情（Region %s，cluster_id=%s）："
                      % (args.region, args.cluster_id))
            print(render_table(items, detail=True))
            return 0
        if not items:
            print("当前区域（%s）无 CDM 集群%s。" % (args.region, filter_suffix))
        else:
            print("Region %s 的 CDM 集群列表（共 %d 个）："
                  % (args.region, len(items)))
        print(render_table(items))
        return 0

    output_path = args.output or default_output_path(operation, args.region, fmt)
    try:
        text = _render(items, fmt, summary=args.summary, region=args.region,
                       detail_record=detail_record)
    except CdmListError as exc:
        print("[错误] %s" % exc, file=sys.stderr)
        return 1
    try:
        written = export_report(text, output_path)
    except ExportError as exc:
        print("[错误] %s" % exc, file=sys.stderr)
        return 1

    if not items:
        print("当前区域（%s）无 CDM 集群%s，已生成空文件（仅表头）：%s"
              % (args.region, filter_suffix, written))
        return 0

    print("已导出 CDM %s（Region %s，共 %d 条，格式 %s）：%s"
          % (operation, args.region, len(items), fmt, written))
    return 0


if __name__ == "__main__":
    sys.exit(main())
