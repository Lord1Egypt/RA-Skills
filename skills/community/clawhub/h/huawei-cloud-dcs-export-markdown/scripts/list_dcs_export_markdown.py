#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""List Huawei Cloud DCS (Distributed Cache Service) instances (read-only) and
export a local Markdown report.

Brings the DCS instance-list query paradigm (KooCLI ``hcloud DCS ListInstances``
— official read-only GET ``/v2/{project_id}/instances``) together with a local
Markdown export. When the hcloud binary is absent, the script falls back to the
official ``huaweicloudsdkdcs`` v2 SDK (``DcsClient.list_instances``).

Three output modes are supported:

- ``--format md`` (default): write the instance list into a ``.md`` report
  (headers 名称 / ID / 引擎 / 版本 / 容量 / 规格 / 状态 / 连接地址 / 端口 / 可用区,
  optional summary line) via the bundled ``export_markdown`` module.
- ``--format table``: aligned full-field table on stdout.
- ``--format json``: structured JSON array for downstream tooling.

A strict write-intent guard rejects any mutating DCS intent so writes never
happen: the only operation ever constructed is read-only
``hcloud DCS ListInstances`` (or the SDK ``list_instances`` fallback). No data is
ever written back to the cloud — the Markdown file is produced on the local
filesystem only.

Usage:
    python3 scripts/list_dcs_export_markdown.py [--region cn-north-4]
                                               [--format md|table|json]
                                               [--output /path/out.md]
                                               [--summary] [--status RUNNING]
                                               [--name cache] [--page-size 100]

Environment overrides (mostly for tests):
    DCS_EXPORT_MARKDOWN_HCLOUD_BIN   hcloud executable (default "hcloud")
    DCS_EXPORT_MARKDOWN_HCLOUD_ARGS  extra args appended AFTER the read-only
                                     ``DCS ListInstances`` arguments
                                     (guard-scanned, read-only)
    DCS_EXPORT_MARKDOWN_SQC_BIN      skill-quality-cli executable override
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys

# Keep the shipped skill directory clean: never emit __pycache__/*.pyc when
# this script (or its tests) import the bundled export module.
sys.dont_write_bytecode = True

from export_markdown import (
    ExportError,
    MD_HEADERS,
    default_output_path,
    export_markdown,
)

DEFAULT_REGION = "cn-north-4"
DEFAULT_PAGE_SIZE = 100
DEFAULT_FORMAT = "md"
SERVICE = "DCS"
ALLOWED_OPERATION = "ListInstances"
REST_PATH = "/v2/{project_id}/instances"

# Skill-quality telemetry: every hcloud call on the script execution path is
# reported through skill-quality-cli (the mandatory wrapping口径). When the CLI
# is unavailable — or SKILL_QUALITY_REPORT=0 — the call degrades to bare hcloud.
SKILL_QUALITY_SKILL_NAME = "huawei-cloud-dcs-export-markdown"
_QUALITY_OFF_VALUES = ("0", "false", "no", "off")

# Mutating DCS operations / intents — strictly rejected by the guard.
WRITE_INTENT_KEYWORDS = (
    "createinstance",
    "batchdeleteinstances",
    "deletesingleinstance",
    "deleteinstance",
    "updateinstance",
    "modifyinstance",
    "resizeinstance",
    "restartinstance",
    "restartorflushinstances",
    "flushinstance",
    "restoreinstance",
    "upgradeinstanceminorversion",
    "exchangeinstanceip",
    "rollbackexchangeinstanceip",
    "copyinstance",
    "updateinstancebandwidth",
    "updateinstanceconfig",
    "setinstancepassword",
    "resetinstancepassword",
    "create",
    "delete",
    "update",
    "modify",
    "resize",
    "restart",
    "reboot",
    "flush",
    "clear",
    "restore",
    "upgrade",
    "rollback",
    "backup",
    "freeze",
    "unfreeze",
    "release",
    "stop",
    "start",
    "terminate",
    "destroy",
    "creating",
    "deleting",
    "updating",
    "restarting",
    "resizing",
    "restoring",
    "upgrading",
    "rebooting",
    "flushing",
    "clearing",
)

# Read-only option flags whose *values* are filter/output data (e.g. an
# instance named "restart-me", the DCS status "RUNNING", or a report path such
# as "cache-delete-report.md"). Their values must NOT be scanned by the
# write-intent guard. The `--operation` value is intentionally NOT excluded: it
# is validated by `guard_operation()` and also scanned, as defense in depth.
_VALUE_STRIPPED_FLAGS = (
    "--region",
    "-r",
    "--status",
    "--name",
    "--instance-id",
    "--ip",
    "--tags",
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
    "instance_id",
    "engine",
    "engine_version",
    "capacity",
    "spec_code",
    "status",
    "ip",
    "port",
    "domain_name",
    "az_codes",
    "charging_mode",
    "vpc_name",
    "subnet_id",
    "security_group_id",
    "max_memory",
    "used_memory",
    "tags",
    "enterprise_project_id",
    "created_at",
    "updated_at",
]

_INSTANCE_LIST_KEYS = ("instances", "instance_list", "instances_detail")

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


class DcsExportError(Exception):
    """Base error for the DCS instance-list Markdown export skill."""


class GuardError(DcsExportError):
    """A write intent was detected and blocked (skill is read-only)."""


class ConfigError(DcsExportError):
    """hcloud/SDK missing or credentials (AK/SK) not configured."""


class AuthError(DcsExportError):
    """Authentication/authorization failure (invalid AK/SK or IAM 403)."""


class ApiError(DcsExportError):
    """hcloud / network / unexpected API failure."""


def guard_write_intent(text):
    """Raise GuardError if ``text`` carries a mutating intent.

    Normalizes separators so ``--create-instance``, ``CreateInstance``, and
    ``create_instance`` all hit the same keyword. Read-only vocabulary
    (list/show/get/describe) never matches.
    """
    low = re.sub(r"[\s_\-]+", "", str(text).lower())
    for keyword in WRITE_INTENT_KEYWORDS:
        if keyword in low:
            raise GuardError(
                "检测到写操作意图（关键词: %s）。本 skill 仅支持只读查询"
                "（DCS ListInstances）并仅在本机生成 Markdown 报表，"
                "创建/删除/扩缩容/重启/清空等变更操作已被守卫拦截。"
                % keyword
            )
    return False


def guard_operation(operation):
    """Only the read-only ListInstances operation may be executed."""
    if operation != ALLOWED_OPERATION:
        raise GuardError(
            "不允许的操作 %r：本 skill 仅允许只读操作 %s。"
            % (operation, ALLOWED_OPERATION)
        )
    return True


def guard_text_from_argv(argv):
    """Build the text the write-intent guard should scan.

    Scans flag names and positional tokens, but strips the values of the
    read-only filter flags (``--status`` / ``--name`` / ``--instance-id`` /
    ``--ip`` / ``--tags`` / ``--region`` / ``--page-size`` / ``--project-id``)
    and of the local-output/format flags (``--output`` / ``-o`` / ``--format``
    / ``-f``): those are pure read / file-path data and may legitimately contain
    write-looking words (e.g. the DCS status ``RUNNING``, an instance named
    ``restart-me``, or a report path ``cache-delete-report.md``).

    A *flag* following such an option is never swallowed: a following token
    that starts with ``-`` is still scanned, so a mutating flag cannot hide
    behind a value-stripped option.
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


def build_command(region, name=None, instance_id=None, ip=None, status=None,
                  tags=None, limit=DEFAULT_PAGE_SIZE, offset=0):
    """Build the hcloud DCS ListInstances argv (without the executable).

    Mirrors the real KooCLI parameter list: --cli-region / --name /
    --instance_id / --ip / --status / --tags are real server-side query
    parameters (verified against ``huaweicloudsdkdcs`` v2 ListInstancesRequest);
    paging uses --limit (1..1000) + --offset.
    """
    argv = [
        SERVICE,
        ALLOWED_OPERATION,
        "--cli-region=%s" % region,
        "--limit=%d" % limit,
        "--offset=%d" % offset,
    ]
    if name:
        argv.append("--name=%s" % name)
    if instance_id:
        argv.append("--instance_id=%s" % instance_id)
    if ip:
        argv.append("--ip=%s" % ip)
    if status:
        argv.append("--status=%s" % status)
    if tags:
        argv.append("--tags=%s" % tags)
    return argv


def _hcloud_executable():
    return os.environ.get("DCS_EXPORT_MARKDOWN_HCLOUD_BIN") or "hcloud"


def _quality_report_enabled():
    """Quality telemetry is on unless SKILL_QUALITY_REPORT is a falsy value."""
    value = os.environ.get("SKILL_QUALITY_REPORT")
    if value is None:
        return True
    return value.strip().lower() not in _QUALITY_OFF_VALUES


def _skill_quality_executable():
    """Locate skill-quality-cli: env override → PATH → ~/.local/bin, else None."""
    override = os.environ.get("DCS_EXPORT_MARKDOWN_SQC_BIN")
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

    Extra args (``DCS_EXPORT_MARKDOWN_HCLOUD_ARGS``) are appended *after* the
    read-only argv so they can never rewrite the service/operation.
    """
    cmd = [_hcloud_executable()]
    cmd.extend(argv)
    extra = os.environ.get("DCS_EXPORT_MARKDOWN_HCLOUD_ARGS", "").split()
    if extra:
        cmd.extend(extra)
    return cmd


def build_hcloud_command(argv):
    """Build the hcloud execution argv, wrapping it with skill-quality-cli.

    Every CLI call is reported as ``skill-quality-cli run --skill-name
    huawei-cloud-dcs-export-markdown -- hcloud ...`` (the mandatory wrapping
    口径, enforced here on the script path rather than left to the agent). The
    command degrades to bare hcloud when the telemetry CLI is missing or
    ``SKILL_QUALITY_REPORT=0``; an explicit ``DCS_EXPORT_MARKDOWN_HCLOUD_BIN``
    override (offline mock / verification) is always run verbatim.
    """
    hcloud_cmd = _hcloud_argv(argv)
    if os.environ.get("DCS_EXPORT_MARKDOWN_HCLOUD_BIN"):
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

    Extra args from ``DCS_EXPORT_MARKDOWN_HCLOUD_ARGS`` are appended *after* the
    read-only ``DCS ListInstances`` argv (they can never rewrite the
    service/operation) and are guard-scanned for write intent first.
    """
    extra = os.environ.get("DCS_EXPORT_MARKDOWN_HCLOUD_ARGS", "").split()
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
            "hcloud 参数错误（KooCLI 拒绝了该参数组合，退出码 %s）：DCS ListInstances "
            "真实参数清单可通过 `hcloud DCS ListInstances --help` 查看。"
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
            "无权限访问分布式缓存服务（DCS），请检查 IAM 权限"
            "（403：AK/SK 无效或未授予 DCS 只读权限），"
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


def _payload_total(payload):
    if not isinstance(payload, dict):
        return None
    for key in ("instance_num", "total_num", "total_count", "totalCount", "total"):
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


def list_instances_via_sdk(region, name=None, instance_id=None, ip=None,
                           status=None, tags=None, limit=DEFAULT_PAGE_SIZE,
                           project_id=None, max_pages=100):
    """SDK fallback: query instances through ``huaweicloudsdkdcs`` v2.

    Only invoked when hcloud is not installed. Credentials are taken from the
    explicitly named AK/SK environment variables (never passed as literals).
    Region resolution uses the SDK's own ``DcsRegion`` catalog, falling back to
    an explicit ``Region(id, endpoint)`` for custom regions. Paging follows
    ``instance_num`` + the batch size.
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
            "SDK 回退缺少 project_id：DCS 的 REST 路径为 %s，需要项目 ID。"
            "请通过 --project-id 传入，或设置 HUAWEICLOUD_SDK_PROJECT_ID / "
            "HUAWEI_PROJECT_ID（严禁在对话中粘贴敏感信息）。" % REST_PATH
        )
    try:
        from huaweicloudsdkcore.auth.credentials import BasicCredentials
        from huaweicloudsdkcore.region.region import Region
        from huaweicloudsdkcore.http.http_config import HttpConfig
        from huaweicloudsdkdcs.v2 import DcsClient, ListInstancesRequest
        from huaweicloudsdkdcs.v2.region.dcs_region import DcsRegion
    except ImportError as exc:
        raise ConfigError(
            "未找到 hcloud（KooCLI），且 huaweicloudsdkcore/huaweicloudsdkdcs 未安装，"
            "无法回退到 SDK。请安装 KooCLI 或先运行 "
            "`python3 scripts/ensure_env.py`（pip install huaweicloudsdkcore "
            "huaweicloudsdkdcs）。详情：%s" % exc
        )
    credentials = BasicCredentials(ak=ak, sk=sk, project_id=resolved_project_id)  # env-sourced, never literals
    try:
        try:
            region_obj = DcsRegion.value_of(region)
        except (ValueError, KeyError, AttributeError):
            region_obj = Region(region, "https://dcs.%s.myhuaweicloud.com" % region)
        client = DcsClient.new_builder() \
            .with_credentials(credentials) \
            .with_region(region_obj) \
            .with_http_config(HttpConfig.get_default_config()) \
            .build()
    except Exception as exc:  # region unknown / config broken
        raise ConfigError(
            "SDK 初始化失败（region=%s）：%s。请检查 huaweicloudsdkdcs 安装与区域配置。"
            % (region, exc)
        )
    instances = []
    offset = 0
    for _ in range(max_pages):
        request = ListInstancesRequest(
            limit=limit, offset=offset,
            name=name, instance_id=instance_id,
            ip=ip, status=status, tags=tags,
        )
        try:
            response = client.list_instances(request)
        except Exception as exc:
            low = str(exc).lower()
            if any(p in low for p in _AUTH_PATTERNS):
                raise AuthError(
                    "无权限访问分布式缓存服务（DCS），请检查 IAM 权限（403）。详情：%s"
                    % str(exc)[:300]
                )
            raise ApiError("SDK 调用失败：%s" % str(exc)[:300])
        batch = list(response.instances or [])
        instances.extend(_jsonable(instance.to_dict()) for instance in batch)
        total = getattr(response, "instance_num", None)
        if total is not None and len(instances) >= total:
            break
        if len(batch) < limit:
            break
        offset += len(batch)
    else:
        raise ApiError("翻页超过 %d 页仍未取完，已中止以防死循环。" % max_pages)
    return instances


def list_instances(region, name=None, instance_id=None, ip=None, status=None,
                   tags=None, limit=DEFAULT_PAGE_SIZE, project_id=None,
                   max_pages=100):
    """Query all DCS instances (paged); KooCLI first, SDK fallback."""
    instances = []
    offset = 0
    for _page in range(max_pages):
        argv = build_command(region, name=name, instance_id=instance_id,
                             ip=ip, status=status, tags=tags,
                             limit=limit, offset=offset)
        try:
            stdout, stderr, returncode = run_hcloud(argv)
        except ConfigError:
            # hcloud binary missing → one-shot SDK fallback (no CLI retry).
            instances = list_instances_via_sdk(
                region, name=name, instance_id=instance_id, ip=ip,
                status=status, tags=tags, limit=limit,
                project_id=project_id, max_pages=max_pages,
            )
            break
        if returncode != 0 or _USE_ERROR_MARKER in (stdout + " " + stderr).lower():
            raise classify_hcloud_failure(stdout, stderr, returncode)
        payload = extract_json(stdout)
        batch = extract_instances(payload)
        instances.extend(batch)
        if not _has_more(batch, len(instances), limit, payload):
            break
        offset += len(batch) if batch else limit
    else:
        raise ApiError("翻页超过 %d 页仍未取完，已中止以防死循环。" % max_pages)
    return instances


def normalize_instance(instance):
    """Flatten az_codes / tags lists into table-friendly cells."""
    flat = dict(instance)
    if "instance_id" not in flat and "id" in flat:
        flat["instance_id"] = flat["id"]
    az_codes = flat.get("az_codes")
    if isinstance(az_codes, list):
        flat["az_codes"] = ",".join(str(code) for code in az_codes) or "-"
    tags = flat.get("tags")
    if isinstance(tags, list):
        cells = []
        for tag in tags:
            if isinstance(tag, dict):
                cells.append("%s=%s" % (tag.get("key", ""), tag.get("value", "")))
            else:
                cells.append(str(tag))
        flat["tags"] = ",".join(cells) if cells else "-"
    return flat


def _field(instance, *names, default="-"):
    for name in names:
        if name in instance and instance[name] not in (None, ""):
            return instance[name]
    return default


def active_filter_descriptions(name=None, instance_id=None, ip=None,
                               status=None, tags=None):
    """Human-readable description of the server-side filters actually applied."""
    filters = []
    if name:
        filters.append("name=%s" % name)
    if instance_id:
        filters.append("instance_id=%s" % instance_id)
    if ip:
        filters.append("ip=%s" % ip)
    if status:
        filters.append("status=%s" % status)
    if tags:
        filters.append("tags=%s" % tags)
    return filters


def _cell(value):
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return str(value)


def render_table(instances):
    """Render full-field table output (union of all returned fields)."""
    rows_data = [normalize_instance(instance) for instance in instances]
    columns = []
    for key in PREFERRED_COLUMNS:
        if any(key in i for i in rows_data):
            columns.append(key)
    for key in sorted({k for i in rows_data for k in i}):
        if key not in columns:
            columns.append(key)
    if not columns:
        columns = ["name", "instance_id"]
    rows = [[_cell(_field(i, col)) for col in columns] for i in rows_data]
    widths = [max(len(col), *(len(row[i]) for row in rows)) for i, col in enumerate(columns)]
    header = "  ".join(col.ljust(widths[i]) for i, col in enumerate(columns))
    separator = "  ".join("-" * w for w in widths)
    lines = [header, separator]
    for row in rows:
        lines.append("  ".join(row[i].ljust(widths[i]) for i in range(len(columns))))
    return "\n".join(lines)


def parse_args(argv):
    parser = argparse.ArgumentParser(
        description="查询华为云 DCS（分布式缓存服务）实例列表并导出 Markdown 报表（只读）。")
    parser.add_argument("-r", "--region", default=DEFAULT_REGION,
                        help="目标 Region（默认 %s）" % DEFAULT_REGION)
    parser.add_argument("-f", "--format", default=DEFAULT_FORMAT,
                        choices=["md", "table", "json"],
                        help="输出格式：md（默认）/ table / json")
    parser.add_argument("-o", "--output", default=None,
                        help="Markdown 输出路径（--format md；默认 "
                             "dcs_instances_<region>_<timestamp>.md）")
    parser.add_argument("--summary", action="store_true",
                        help="Markdown 报表末尾追加汇总行（实例数量）")
    parser.add_argument("--name",
                        help="按实例名称过滤（服务端查询参数，模糊匹配）")
    parser.add_argument("--name-equal", action="store_true", dest="name_equal",
                        help="按实例名称精确匹配（本地精确匹配开关）")
    parser.add_argument("--instance-id", dest="instance_id",
                        help="按实例 ID 过滤（服务端查询参数）")
    parser.add_argument("--ip",
                        help="按连接 IP 地址过滤（服务端查询参数）")
    parser.add_argument("--status",
                        help="按实例状态过滤（RUNNING/ERROR 等；服务端查询参数）")
    parser.add_argument("--tags",
                        help="按标签过滤（服务端查询参数，格式 key1=value1,key2=value2）")
    parser.add_argument("--page-size", type=int, default=DEFAULT_PAGE_SIZE,
                        dest="page_size",
                        help="分页大小（默认 %d，范围 1~1000，自动翻页取全量）" % DEFAULT_PAGE_SIZE)
    parser.add_argument("--project-id", dest="project_id",
                        help="项目 ID（可选；SDK 回退在 /v2/{project_id}/instances 路径中需要）")
    parser.add_argument("--operation", default=ALLOWED_OPERATION,
                        help="hcloud DCS 操作名（仅允许只读 %s）" % ALLOWED_OPERATION)
    return parser.parse_args(argv)


def main(argv=None):
    raw_argv = argv if argv is not None else sys.argv[1:]

    # Write-intent guard runs on the RAW argv BEFORE argparse, so that a
    # mutating flag (e.g. `--create-instance`) is reported as a guard violation
    # instead of an argparse "unrecognized argument" error. Filter/output
    # values are read-only data and deliberately not scanned.
    try:
        guard_write_intent(guard_text_from_argv(raw_argv))
    except DcsExportError as exc:
        print("[错误] %s" % exc, file=sys.stderr)
        return 1

    args = parse_args(argv)

    try:
        guard_operation(args.operation)
        if args.page_size is not None:
            if args.page_size < 1 or args.page_size > 1000:
                raise ApiError("--page-size 超出范围（1~1000）：%d" % args.page_size)
        instances = list_instances(
            args.region,
            name=args.name if not args.name_equal else None,
            instance_id=args.instance_id,
            ip=args.ip,
            status=args.status,
            tags=args.tags if not args.name_equal else None,
            limit=args.page_size,
            project_id=args.project_id,
        )
    except DcsExportError as exc:
        print("[错误] %s" % exc, file=sys.stderr)
        return 1

    # --name-equal: exact name matching (server name param is fuzzy by default).
    if args.name_equal:
        if args.name:
            wanted = str(args.name).strip().lower()
            instances = [
                i for i in instances
                if str(i.get("name", "")).strip().lower() == wanted
            ]
        else:
            instances = []

    filters = active_filter_descriptions(name=args.name, instance_id=args.instance_id,
                                         ip=args.ip, status=args.status, tags=args.tags)
    filter_suffix = "（过滤条件: %s）" % ", ".join(filters) if filters else ""
    fmt = args.format

    if fmt == "json":
        print(json.dumps(instances, ensure_ascii=False, indent=2))
        return 0

    if fmt == "table":
        if not instances:
            print("当前区域（%s）无 DCS 实例%s。" % (args.region, filter_suffix))
            return 0
        print("Region %s 的 DCS 实例列表（共 %d 个，完整字段）："
              % (args.region, len(instances)))
        print(render_table(instances))
        return 0

    # fmt == "md": empty instance list → friendly hint, never a broken file.
    if not instances:
        print("当前区域（%s）无 DCS 实例%s，未生成 Markdown 文件。"
              % (args.region, filter_suffix))
        return 0

    output_path = args.output or default_output_path(args.region)
    try:
        written = export_markdown(instances, output_path,
                                  summary=args.summary, region=args.region)
    except ExportError as exc:
        print("[错误] %s" % exc, file=sys.stderr)
        return 1

    print("已生成 DCS 实例列表 Markdown 报表（Region %s，共 %d 个实例）：%s"
          % (args.region, len(instances), written))
    return 0


if __name__ == "__main__":
    sys.exit(main())