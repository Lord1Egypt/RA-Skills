#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""List Huawei Cloud FunctionGraph (函数工作流) functions via KooCLI `hcloud functiongraph ListFunctions`.

Read-only query of the FunctionGraph function list for the current account /
project / region. Primary path is KooCLI (`hcloud functiongraph ListFunctions`,
read-only GET `/v2/{project_id}/fgs/functions`, verified in the
`huaweicloudsdkfunctiongraph` v2 `_list_functions_http_info` metadata); when
hcloud is not installed the script falls back to the official SDK
(`huaweicloudsdkfunctiongraph` v2 `list_functions`). Credentials are always read
from the active CLI profile / SDK environment — never passed as literals.

By default the result is **sorted by function name** (func_name) and rendered as
a table showing function name / memory / timeout / handler / runtime / URN, etc.
Three stdout modes are supported: table (default), `--json` (full raw fields)
and `--names-only` (compact name list). `--name` and `--package-name` are
server-side query filters (`func_name` fuzzy search, `package_name` group).

A strict write-intent guard rejects any mutating FunctionGraph intent (create /
delete / update / publish / invoke / import / export / ...) before a single
command is executed — this skill is strictly read-only.

Usage:
    python3 scripts/list_functiongraph.py [--region cn-north-4] [--json | --names-only]
                                          [--name demo] [--package-name app]
                                          [--page-size 400]
                                          [--operation ListFunctions]

Environment overrides (mostly for tests):
    FUNCTIONGRAPH_LIST_HCLOUD_BIN   hcloud executable (default "hcloud")
    FUNCTIONGRAPH_LIST_HCLOUD_ARGS  extra args injected before the FunctionGraph operation
"""

import argparse
import json
import os
import re
import subprocess
import sys

DEFAULT_REGION = "cn-north-4"
DEFAULT_PAGE_SIZE = 400
SERVICE = "functiongraph"
ALLOWED_OPERATION = "ListFunctions"

# SDK fallback credential source — an explicit whitelist of standard Huawei
# Cloud AK/SK environment variable names. Credentials are read one variable at a
# time by exact name (never by iterating the whole environment).
_AK_ENV_NAMES = (
    "HUAWEICLOUD_SDK_AK",
    "HW_ACCESS_KEY",
    "HUAWEI_ACCESS_KEY",
    "HUAWEI_CLOUD_ACCESS_KEY",
    "HUAWEI_AK",
    "HW_AK",
    "HWC_ACCESS_KEY",
)
_SK_ENV_NAMES = (
    "HUAWEICLOUD_SDK_SK",
    "HW_SECRET_KEY",
    "HUAWEI_SECRET_KEY",
    "HUAWEI_CLOUD_SECRET_KEY",
    "HUAWEI_SK",
    "HW_SK",
    "HWC_SECRET_KEY",
)

# Mutating FunctionGraph operations / intents — strictly rejected by the guard.
# Normalized (lower-case, separators stripped) exact operation names first, then
# the generic mutating verbs that any write argument would carry.
WRITE_INTENT_KEYWORDS = (
    "asyncinvokefunction",
    "invokefunction",
    "createfunction",
    "createfunctionversion",
    "createcallbackworkflow",
    "createfunctiontrigger",
    "createfunctionapp",
    "createdependencyversion",
    "createtags",
    "createversionalias",
    "createvpceendpoint",
    "createworkflow",
    "deletefunction",
    "deletefunctiontrigger",
    "deletefunctionapp",
    "deletedependencyversion",
    "updafunctioncode",
    "updatefunctioncode",
    "updatefunctionconfig",
    "updatetrigger",
    "updateversionalias",
    "updateworkflow",
    "publishfunctionversion",
    "importfunction",
    "exportfunction",
    "batchdeletefunctiontriggers",
    "batchdeleteworkflows",
    "creating",
    "deleting",
    "updating",
    "publishing",
    "creatingfunction",
    "invoking",
    "create",
    "delete",
    "update",
    "modify",
    "publish",
    "invoke",
    "import",
    "export",
    "remove",
    "destroy",
)

# Preferred column order for the table view; remaining keys are appended sorted.
PREFERRED_COLUMNS = [
    "func_name",
    "func_urn",
    "memory_size",
    "timeout",
    "handler",
    "runtime",
    "package",
    "code_type",
    "code_size",
    "version",
    "last_modified",
    "description",
]

_FUNCTION_LIST_KEYS = (
    "functions",
    "function_list",
    "items",
    "results",
)

# KooCLI prints usage errors (e.g. "[USE_ERROR]Invalid parameter: xxx") on
# stdout WITH exit code 0 — the marker must be treated as a hard failure even
# when the return code looks successful.
_USE_ERROR_MARKER = "[use_error]"

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
    "does not contain profile",
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


class FunctionGraphListError(Exception):
    """Base error for the FunctionGraph list skill."""


class GuardError(FunctionGraphListError):
    """A write intent was detected and blocked (skill is read-only)."""


class ConfigError(FunctionGraphListError):
    """hcloud missing or credentials (AK/SK) not configured."""


class AuthError(FunctionGraphListError):
    """Authentication/authorization failure (invalid AK/SK or IAM 403)."""


class ApiError(FunctionGraphListError):
    """hcloud / network / unexpected API failure."""


def guard_write_intent(text):
    """Raise GuardError if `text` carries a mutating intent.

    Normalizes separators so `--create-function`, `CreateFunction`, and
    `create_function` all hit the same keyword. Read-only vocabulary
    (list/show/get/describe) never matches.
    """
    low = re.sub(r"[\s_\-]+", "", str(text).lower())
    for keyword in WRITE_INTENT_KEYWORDS:
        if keyword in low:
            raise GuardError(
                "检测到写操作意图（关键词: %s）。本 skill 仅支持只读查询"
                "（FunctionGraph ListFunctions），创建/删除/更新/发布/调用/导入/导出等"
                "变更操作已被守卫拦截。" % keyword
            )
    return False


def guard_operation(operation):
    """Only the read-only ListFunctions operation may be executed."""
    if operation != ALLOWED_OPERATION:
        raise GuardError(
            "不允许的操作 %r：本 skill 仅允许只读操作 %s。" % (operation, ALLOWED_OPERATION)
        )
    return True


def _hcloud_executable():
    return os.environ.get("FUNCTIONGRAPH_LIST_HCLOUD_BIN", "hcloud")


def build_command(region, name=None, package_name=None, maxitems=DEFAULT_PAGE_SIZE,
                  marker=None):
    """Build the hcloud functiongraph ListFunctions argv (without the executable).

    Mirrors the real KooCLI parameter list (`hcloud functiongraph ListFunctions
    --help`): --cli-region / --func_name / --package_name / --maxitems
    / --marker. `marker` is the pagination cursor (`next_marker` from the
    previous page). `--project_id` is a required path parameter but is filled
    automatically by KooCLI from the credential profile, so it is never emitted.
    """
    argv = [
        SERVICE,
        ALLOWED_OPERATION,
        "--cli-region=%s" % region,
        "--maxitems=%d" % maxitems,
    ]
    if name:
        argv.append("--func_name=%s" % name)
    if package_name:
        argv.append("--package_name=%s" % package_name)
    if marker is not None:
        argv.append("--marker=%s" % marker)
    return argv


def run_hcloud(argv):
    """Execute hcloud and return (stdout, stderr, returncode)."""
    cmd = [_hcloud_executable()]
    extra = os.environ.get("FUNCTIONGRAPH_LIST_HCLOUD_ARGS", "").split()
    if extra:
        cmd.extend(extra)
    cmd.extend(argv)
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
    if any(p in low for p in _CREDENTIAL_MISSING_PATTERNS) and not re.search(
            r"\b40[13]\b", blob):
        return ConfigError(
            "缺少 AK/SK 凭证：hcloud 未配置有效凭证。请先运行 hcloud configure 或"
            "设置凭证环境变量（严禁在对话中粘贴 AK/SK），参见"
            " references/cli-installation-guide.md。详情：%s" % blob[:300]
        )
    if _USE_ERROR_MARKER in low:
        return ApiError(
            "hcloud 参数错误（KooCLI 拒绝了该参数组合，退出码 %s）：functiongraph "
            "ListFunctions 真实参数清单可通过 `hcloud functiongraph ListFunctions "
            "--help` 查看。详情：%s" % (returncode, blob[:300])
        )
    if any(p in low for p in _AUTH_PATTERNS):
        return AuthError(
            "无权限访问 FunctionGraph，请检查 IAM 权限（403：AK/SK 无效或未授予"
            " FunctionGraph 只读权限），参见 references/iam-policies.md。详情：%s"
            % blob[:300]
        )
    return ApiError(
        "hcloud 调用失败（退出码 %s）：%s" % (returncode, blob[:300])
    )


def extract_functions(payload):
    """Pull the function list out of a ListFunctions response."""
    if isinstance(payload, list):
        return payload
    for key in _FUNCTION_LIST_KEYS:
        value = payload.get(key)
        if isinstance(value, list):
            return value
    return []


def _next_marker(payload):
    if not isinstance(payload, dict):
        return None
    value = payload.get("next_marker")
    if value is not None and str(value) not in ("", "0", "0.0"):
        return str(value)
    return None


def _count(payload):
    if not isinstance(payload, dict):
        return None
    for key in ("count", "total", "total_count"):
        value = payload.get(key)
        if isinstance(value, int):
            return value
    return None


def list_functions_via_sdk(region, name=None, package_name=None,
                           limit=DEFAULT_PAGE_SIZE, max_pages=100):
    """SDK fallback: query functions through `huaweicloudsdkfunctiongraph` v2.

    Only invoked when hcloud is not installed. Credentials are taken from the
    standard environment variables (HUAWEI_*/HW_*/HWC_* AK/SK markers) — never
    passed as literals here. The official SDK has no env-var auto-discovery on
    `BasicCredentials()`, so AK/SK must be read explicitly. Region resolution
    uses the SDK's own `FunctionGraphRegion` catalog (official endpoints, no
    guessing), falling back to an explicit `Region(id, endpoint)` for custom
    regions. `ListFunctionsRequest` has no server-side sort parameter, so
    sorting by name is applied by the caller via `sort_by_name()`.
    """
    try:
        from huaweicloudsdkcore.auth.credentials import BasicCredentials
        from huaweicloudsdkcore.region.region import Region
        from huaweicloudsdkcore.http.http_config import HttpConfig
        from huaweicloudsdkfunctiongraph.v2 import FunctionGraphClient, ListFunctionsRequest
        from huaweicloudsdkfunctiongraph.v2.region.functiongraph_region import FunctionGraphRegion
    except ImportError as exc:
        raise ConfigError(
            "未找到 hcloud（KooCLI），且 huaweicloudsdkcore/"
            "huaweicloudsdkfunctiongraph 未安装，无法回退到 SDK。请安装 KooCLI "
            "或 pip install huaweicloudsdkcore huaweicloudsdkfunctiongraph。"
            "详情：%s" % exc
        )

    def _env_credential(names):
        """Read the first non-empty value from an explicit env-name whitelist.

        Reads each candidate credential variable by its exact name — it never
        iterates the whole environment, so unrelated variables (e.g. other
        services' tokens) are never touched.
        """
        for name in names:
            value = os.environ.get(name)
            if value:
                return value
        return None

    access_key_id = _env_credential(_AK_ENV_NAMES)
    secret_key_id = _env_credential(_SK_ENV_NAMES)
    if not access_key_id or not secret_key_id:
        raise ConfigError(
            "SDK 回退缺少 AK/SK 凭证：官方 SDK 的 BasicCredentials 不会自动读取"
            "环境变量，且当前环境未检测到 HUAWEI_*/HW_*/HWC_* 形式的 AK/SK 环境变量。"
            "请在会话外设置 HUAWEICLOUD_SDK_AK / HUAWEICLOUD_SDK_SK（严禁在对话中"
            "粘贴 AK/SK），参见 references/cli-installation-guide.md。"
        )
    credentials = BasicCredentials(ak=access_key_id, sk=secret_key_id)  # env-sourced, never literals
    try:
        try:
            region_obj = FunctionGraphRegion.value_of(region)
        except (ValueError, KeyError, AttributeError):
            region_obj = Region(region, "https://functiongraph.%s.myhuaweicloud.com"
                                        % region)
        client = FunctionGraphClient.new_builder() \
            .with_credentials(credentials) \
            .with_region(region_obj) \
            .with_http_config(HttpConfig.get_default_config()) \
            .build()
    except Exception as exc:  # region unknown / config broken
        raise ConfigError(
            "SDK 初始化失败（region=%s）：%s。请检查 huaweicloudsdkfunctiongraph 安装"
            "与区域配置。" % (region, exc)
        )
    functions = []
    marker = None
    for _ in range(max_pages):
        request = ListFunctionsRequest(
            maxitems=limit,
            marker=marker,
            func_name=name,
            package_name=package_name,
        )
        try:
            response = client.list_functions(request)
        except Exception as exc:
            low = str(exc).lower()
            if any(p in low for p in _AUTH_PATTERNS):
                raise AuthError(
                    "无权限访问 FunctionGraph，请检查 IAM 权限（403）。详情：%s"
                    % str(exc)[:300]
                )
            raise ApiError("SDK 调用失败：%s" % str(exc)[:300])
        batch = [fn.to_dict() for fn in (response.functions or [])]
        functions.extend(batch)
        total = getattr(response, "count", None)
        if total is not None and len(functions) >= total:
            break
        if not batch:
            break
        next_marker = getattr(response, "next_marker", None)
        if next_marker is None or str(next_marker) in ("", "0", "0.0"):
            break
        marker = str(next_marker)
    else:
        raise ApiError("翻页超过 %d 页仍未取完，已中止以防死循环。" % max_pages)
    return functions


def sort_by_name(functions):
    """Sort functions by name (func_name) case-insensitively; stable."""
    return sorted(
        functions,
        key=lambda fn: str(fn.get("func_name") or "") if isinstance(fn, dict) else "",
    )


def list_functions(region, name=None, package_name=None,
                   limit=DEFAULT_PAGE_SIZE, max_pages=100):
    """Query all functions (paged); KooCLI first, SDK fallback. Sorted by name.

    `--name` / `--package-name` are forwarded server-side (`func_name` fuzzy
    search, `package_name` group). Pagination uses the `marker` cursor from
    `next_marker` in each page.
    """
    functions = []
    marker = None
    for _page in range(max_pages):
        argv = build_command(region, name=name, package_name=package_name,
                             maxitems=limit, marker=marker)
        try:
            stdout, stderr, returncode = run_hcloud(argv)
        except ConfigError:
            # hcloud binary missing → one-shot SDK fallback (no CLI retry).
            functions = list_functions_via_sdk(
                region, name=name, package_name=package_name,
                limit=limit, max_pages=max_pages,
            )
            break
        if returncode != 0 or _USE_ERROR_MARKER in (stdout + " " + stderr).lower():
            # KooCLI usage errors print [USE_ERROR] on stdout with rc=0.
            raise classify_hcloud_failure(stdout, stderr, returncode)
        payload = extract_json(stdout)
        batch = extract_functions(payload)
        functions.extend(batch)
        next_marker = _next_marker(payload)
        total = _count(payload)
        if total is not None and len(functions) >= total:
            break
        if not batch or not next_marker:
            break
        marker = next_marker
    else:
        raise ApiError("翻页超过 %d 页仍未取完，已中止以防死循环。" % max_pages)
    return sort_by_name(functions)


def _field(fn, *names, default="-"):
    for name in names:
        if name in fn and fn[name] not in (None, ""):
            return fn[name]
    return default


def function_names(functions):
    names = []
    for fn in functions:
        names.append(str(_field(fn, "func_name", "name", default="-")))
    return names


def active_filter_descriptions(name=None, package_name=None):
    """Human-readable description of the filters actually applied."""
    filters = []
    if name:
        filters.append("func_name=%s" % name)
    if package_name:
        filters.append("package_name=%s" % package_name)
    return filters


def _cell(value):
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return str(value)


def render_table(functions):
    """Render full-field table output (union of all returned fields)."""
    rows_data = list(functions)
    if not rows_data:
        return ""
    columns = []
    for key in PREFERRED_COLUMNS:
        if any(key in i for i in rows_data):
            columns.append(key)
    for key in sorted({k for i in rows_data for k in i}):
        if key not in columns:
            columns.append(key)
    if not columns:
        columns = ["func_name", "func_urn"]
    rows = [[_cell(_field(i, col)) for col in columns] for i in rows_data]
    widths = [max(len(col), *(len(row[i]) for row in rows)) for i, col in enumerate(columns)]
    header = "  ".join(col.ljust(widths[i]) for i, col in enumerate(columns))
    separator = "  ".join("-" * w for w in widths)
    lines = [header, separator]
    for row in rows:
        lines.append("  ".join(row[i].ljust(widths[i]) for i in range(len(columns))))
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="查询华为云 FunctionGraph 函数列表（KooCLI hcloud functiongraph "
                    "ListFunctions，只读，按函数名排序）。")
    parser.add_argument("-r", "--region", default=DEFAULT_REGION,
                        help="目标 Region（默认 %s）" % DEFAULT_REGION)
    parser.add_argument("--json", action="store_true", dest="as_json",
                        help="以 JSON 输出完整原始字段")
    parser.add_argument("--names-only", action="store_true", dest="names_only",
                        help="仅输出函数名称清单")
    parser.add_argument("--name", help="按函数名称过滤（func_name，服务端模糊搜索参数）")
    parser.add_argument("--package-name", dest="package_name",
                        help="按分组名称过滤（package_name，服务端参数）")
    parser.add_argument("--page-size", type=int, default=DEFAULT_PAGE_SIZE,
                        dest="page_size",
                        help="分页大小/每页条数（默认 %d，上限 400）" % DEFAULT_PAGE_SIZE)
    parser.add_argument("--operation", default=ALLOWED_OPERATION,
                        help="hcloud FunctionGraph 操作名（仅允许只读 %s）"
                             % ALLOWED_OPERATION)
    args = parser.parse_args(argv)

    raw_argv = argv if argv is not None else sys.argv[1:]
    try:
        # Write-intent guard: scan the raw argv + validate the operation name.
        guard_write_intent(" ".join(raw_argv))
        guard_operation(args.operation)
        if args.name:
            guard_write_intent(args.name)
        if args.package_name:
            guard_write_intent(args.package_name)
        functions = list_functions(
            args.region,
            name=args.name,
            package_name=args.package_name,
            limit=args.page_size,
        )
    except FunctionGraphListError as exc:
        print("[错误] %s" % exc, file=sys.stderr)
        return 1

    if args.as_json:
        print(json.dumps(functions, ensure_ascii=False, indent=2))
    elif args.names_only:
        print("Region %s 的 FunctionGraph 函数名称列表（共 %d 个）："
              % (args.region, len(functions)))
        for name in function_names(functions):
            print("- %s" % name)
    elif not functions:
        filters = active_filter_descriptions(
            name=args.name, package_name=args.package_name)
        suffix = "（过滤条件: %s）" % ", ".join(filters) if filters else ""
        print("当前区域（%s）无函数%s。" % (args.region, suffix))
    else:
        print("Region %s 的 FunctionGraph 函数列表（共 %d 个，按函数名排序）："
              % (args.region, len(functions)))
        print(render_table(functions))

    return 0


if __name__ == "__main__":
    sys.exit(main())