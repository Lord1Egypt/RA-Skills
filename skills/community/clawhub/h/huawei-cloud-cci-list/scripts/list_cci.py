#!/usr/bin/env python3
"""List Huawei Cloud CCI (Cloud Container Instance) resources via KooCLI (read-only).

Routes to one of five read-only CCI list operations selected with `--resource`
and `--namespace`:

    namespace     hcloud CCI ListCoreV1Namespace              GET /api/v1/namespaces
    pod           hcloud CCI ListCoreV1PodForAllNamespaces    GET /api/v1/pods
                  hcloud CCI ListCoreV1NamespacedPod          GET /api/v1/namespaces/{namespace}/pods
    deployment    hcloud CCI ListAppsV1DeploymentForAllNamespaces
                                                              GET /apis/apps/v1/deployments
                  hcloud CCI ListAppsV1NamespacedDeployment   GET /apis/apps/v1/namespaces/{namespace}/deployments

Primary (and only) execution path is KooCLI: the CCI OpenAPI is Kubernetes-style
and CCI ships no public Python SDK package (`huaweicloudsdkcci` is not published
on PyPI), so there is no SDK fallback. Credentials are only ever taken from the
active KooCLI profile / standard environment variables; the script never reads,
echoes, or stores secrets itself.

Supports three output modes (full-field table / --json / --names-only), a
client-side --name filter, server-side Kubernetes label/field selectors,
automatic continue-token paging, and a strict write-intent guard: any mutating
intent is rejected before a single command is executed.

Usage:
    python3 scripts/list_cci.py [--resource namespace|pod|deployment]
                                [--region cn-north-4] [--namespace NS]
                                [--name NAME] [--label-selector k=v]
                                [--field-selector k=v] [--json | --names-only]
                                [--page-size 100] [--operation ListCoreV1Namespace]

Environment overrides (mostly for tests):
    CCI_LIST_HCLOUD_BIN    hcloud executable (default "hcloud")
    CCI_LIST_HCLOUD_ARGS   extra args injected before the CCI operation
"""

import argparse
import json
import os
import re
import subprocess
import sys

DEFAULT_REGION = "cn-north-4"
DEFAULT_PAGE_SIZE = 100
MAX_PAGES = 100
SERVICE = "CCI"

# --- KooCLI routing table ---------------------------------------------------
# Service code and operation names are taken verbatim from the CCI OpenAPI
# operation ids published in the Huawei Cloud API reference / API Explorer CLI
# examples (operation id -> PascalCase: listCoreV1Namespace -> ListCoreV1Namespace).
# See references/verification-method.md.
RESOURCES = {
    "namespace": {
        "label": "CCI 命名空间（Namespace）",
        "operation": "ListCoreV1Namespace",
        "scoped_operation": None,
        "rest": "GET /api/v1/namespaces",
        "scoped_rest": None,
        "needs_namespace": False,
        "kind": "Namespace",
    },
    "pod": {
        "label": "CCI Pod（实例）",
        "operation": "ListCoreV1PodForAllNamespaces",
        "scoped_operation": "ListCoreV1NamespacedPod",
        "rest": "GET /api/v1/pods",
        "scoped_rest": "GET /api/v1/namespaces/{namespace}/pods",
        "needs_namespace": False,
        "kind": "Pod",
    },
    "deployment": {
        "label": "CCI 无状态负载（Deployment）",
        "operation": "ListAppsV1DeploymentForAllNamespaces",
        "scoped_operation": "ListAppsV1NamespacedDeployment",
        "rest": "GET /apis/apps/v1/deployments",
        "scoped_rest": "GET /apis/apps/v1/namespaces/{namespace}/deployments",
        "needs_namespace": False,
        "kind": "Deployment",
    },
}

ALLOWED_OPERATIONS = frozenset(
    op
    for spec in RESOURCES.values()
    for op in (spec["operation"], spec["scoped_operation"])
    if op
)
EXPECTED_OPS_BY_RESOURCE = {
    name: frozenset(op for op in (spec["operation"], spec["scoped_operation"]) if op)
    for name, spec in RESOURCES.items()
}

# Mutating CCI intents — strictly rejected by the guard.
# NOTE: read-only vocabulary (list / read / get / describe / show) and words that
# appear inside our own read-only operations/resource names must never be listed
# here (e.g. "connect" is a mutating pod exec operation and IS listed).
WRITE_INTENT_KEYWORDS = (
    "createcorev1namespace",
    "deletecorev1namespace",
    "patchcorev1namespace",
    "replacecorev1namespace",
    "createcorev1namespacedpod",
    "deletecorev1namespacedpod",
    "deletecorev1collectionnamespacedpod",
    "patchcorev1namespacedpod",
    "replacecorev1namespacedpod",
    "connectcorev1getnamespacedpodexec",
    "connectcorev1postnamespacedpodexec",
    "createappsv1namespaceddeployment",
    "deleteappsv1namespaceddeployment",
    "deleteappsv1collectionnamespaceddeployment",
    "patchappsv1namespaceddeployment",
    "replaceappsv1namespaceddeployment",
    "create",
    "delete",
    "deletecollection",
    "update",
    "modify",
    "patch",
    "replace",
    "apply",
    "connect",
    "exec",
    "attach",
    "scale",
    "resize",
    "restart",
    "rollout",
    "rollback",
    "upgrade",
    "kill",
    "evict",
    "drain",
    "cordon",
    "uncordon",
    "taint",
    "annotate",
    "label",
    "stop",
    "start",
    "terminate",
    "destroy",
    "remove",
    "archive",
)

# Flags whose values are pure read data (filters/selectors) and must NOT be
# scanned by the write-intent guard, otherwise legitimate filters such as
# `--name restart-me` or `--namespace create-test` would be rejected.
_VALUE_STRIPPED_FLAGS = (
    "--region",
    "-r",
    "--resource",
    "--namespace",
    "-n",
    "--name",
    "--label-selector",
    "--field-selector",
    "--page-size",
)

# Preferred column order for the table view; remaining keys are appended sorted.
PREFERRED_COLUMNS = [
    "name",
    "namespace",
    "status",
    "replicas",
    "ready_replicas",
    "pod_ip",
    "node_name",
    "creation_timestamp",
    "uid",
    "resource_version",
    "images",
    "labels",
]

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
    "profile",
)

_AUTH_PATTERNS = (
    "401",
    "403",
    "unauthorized",
    "forbidden",
    "认证失败",
    "权限不足",
    "permission denied",
)

# KooCLI prints usage errors (e.g. "[USE_ERROR]Invalid parameter: xxx") on
# stdout WITH exit code 0 — the marker must be treated as a hard failure even
# when the return code looks successful.
_USE_ERROR_MARKER = "[use_error]"


class CciListError(Exception):
    """Base error for the CCI list skill."""


class GuardError(CciListError):
    """A write intent was detected and blocked (skill is read-only)."""


class ConfigError(CciListError):
    """hcloud missing or credentials (AK/SK) not configured."""


class AuthError(CciListError):
    """Authentication/authorization failure (invalid AK/SK or IAM 403)."""


class ApiError(CciListError):
    """hcloud / network / unexpected API failure."""


def guard_write_intent(text):
    """Raise GuardError if `text` carries a mutating intent.

    Normalizes separators so `--create-namespace`, `CreateCoreV1Namespace` and
    `create_namespace` all hit the same keyword. Read-only vocabulary
    (list / read / get / describe) never matches.
    """
    low = re.sub(r"[\s_\-:]+", "", str(text).lower())
    for keyword in WRITE_INTENT_KEYWORDS:
        if keyword in low:
            raise GuardError(
                "检测到写操作意图（关键词: %s）。本 skill 仅支持只读列表查询（CCI "
                "ListCoreV1Namespace / ListCoreV1Pod(ForAllNamespaces) / "
                "ListCoreV1NamespacedPod / ListAppsV1Deployment(ForAllNamespaces) / "
                "ListAppsV1NamespacedDeployment），创建/删除/更新/Pod exec 等变更操作已被守卫拦截。"
                % keyword
            )
    return False


def guard_operation(operation, resource=None):
    """Only a read-only CCI list operation may be executed."""
    if operation not in ALLOWED_OPERATIONS:
        raise GuardError(
            "不允许的 CCI 操作 %r：本 skill 仅允许只读 List 操作（%s）。"
            % (operation, ", ".join(sorted(ALLOWED_OPERATIONS)))
        )
    if resource and operation not in EXPECTED_OPS_BY_RESOURCE[resource]:
        raise GuardError(
            "操作 %r 与资源 %s 不匹配（允许：%s）。"
            % (operation, resource,
               ", ".join(sorted(EXPECTED_OPS_BY_RESOURCE[resource])))
        )
    return True


def guard_text_from_argv(argv):
    """Build the text the write-intent guard should scan.

    Scans flag names and positional tokens, but strips the values of the
    read-only selector/filter flags so legit read data is never rejected.
    """
    tokens = list(argv if argv is not None else sys.argv[1:])
    kept = []
    skip_next = False
    for tok in tokens:
        if skip_next:
            skip_next = False
            continue
        key = tok.split("=", 1)[0]
        if tok in _VALUE_STRIPPED_FLAGS:
            skip_next = True
            continue
        if tok.startswith("-") and "=" in tok and key in _VALUE_STRIPPED_FLAGS:
            continue
        kept.append(tok)
    return " ".join(kept)


def build_command(resource, region, namespace=None,
                  limit=DEFAULT_PAGE_SIZE, continue_token=None):
    """Build the hcloud argv (without executable) for the selected resource.

    Kubernetes list query parameters are forwarded verbatim (KooCLI uses the
    API's own parameter names): `--limit` + `--continue` for paging, optional
    `--namespace` for the namespaced variants.
    """
    spec = RESOURCES[resource]
    if namespace and spec["scoped_operation"]:
        operation = spec["scoped_operation"]
    else:
        operation = spec["operation"]
    argv = [
        SERVICE,
        operation,
        "--cli-region=%s" % region,
    ]
    if namespace and spec["scoped_operation"]:
        argv.append("--namespace=%s" % namespace)
    if limit:
        argv.append("--limit=%d" % limit)
    if continue_token:
        argv.append("--continue=%s" % continue_token)
    return argv


def _hcloud_executable():
    return os.environ.get("CCI_LIST_HCLOUD_BIN", "hcloud")


def run_hcloud(argv):
    """Execute hcloud and return (stdout, stderr, returncode)."""
    cmd = [_hcloud_executable()]
    extra = os.environ.get("CCI_LIST_HCLOUD_ARGS", "").split()
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
            "未找到 hcloud（KooCLI）。CCI 采用类 Kubernetes OpenAPI，暂无官方 Python SDK"
            "（huaweicloudsdkcci 未发布），无 SDK 回退路径。请先安装 KooCLI 并完成认证配置，"
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
        pass
    obj_at, arr_at = text.find("{"), text.find("[")
    if arr_at >= 0 and (obj_at < 0 or arr_at < obj_at):
        candidates = [("[", "]"), ("{", "}")]
    else:
        candidates = [("{", "}"), ("[", "]")]
    for open_ch, close_ch in candidates:
        start, end = text.find(open_ch), text.rfind(close_ch)
        if start >= 0 and end > start:
            try:
                return json.loads(text[start:end + 1])
            except json.JSONDecodeError:
                continue
    raise ApiError("hcloud 输出无法解析为 JSON：%s" % text[:200])


def classify_hcloud_failure(stdout, stderr, returncode, service=SERVICE,
                            operation=None):
    """Map a failed hcloud invocation to a domain error with explicit hints."""
    blob = (stderr + " " + stdout).strip()
    low = blob.lower()
    hint = "`hcloud %s %s --help`" % (service, operation or "<Operation>")
    if _USE_ERROR_MARKER in low:
        return ApiError(
            "hcloud 参数错误（KooCLI 拒绝了该参数组合，退出码 %s）：真实参数清单可通过 "
            "%s 查看。详情：%s" % (returncode, hint, blob[:300])
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
            "无权限访问云容器实例（CCI），请检查 IAM 权限（403：AK/SK 无效或未授予 CCI "
            "只读权限），参见 references/iam-policies.md。详情：%s" % blob[:300]
        )
    return ApiError("hcloud 调用失败（退出码 %s）：%s" % (returncode, blob[:300]))


def extract_items(payload):
    """Pull the item list out of a Kubernetes-style list response."""
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        items = payload.get("items")
        if isinstance(items, list):
            return items
    return []


def next_continue_token(payload):
    """Return the Kubernetes `metadata.continue` token (or None)."""
    if not isinstance(payload, dict):
        return None
    meta = payload.get("metadata")
    if isinstance(meta, dict):
        token = meta.get("continue")
        if isinstance(token, str) and token:
            return token
    return None


def _field(item, *names, **kwargs):
    default = kwargs.get("default", "-")
    for name in names:
        if name in item and item[name] not in (None, ""):
            return item[name]
    return default


def _meta(item):
    meta = item.get("metadata") if isinstance(item, dict) else None
    return meta if isinstance(meta, dict) else {}


def _status(item):
    status = item.get("status") if isinstance(item, dict) else None
    return status if isinstance(status, dict) else {}


def _spec(item):
    spec = item.get("spec") if isinstance(item, dict) else None
    return spec if isinstance(spec, dict) else {}


def filter_by_name(items, name):
    """Client-side name filter (case-insensitive substring match).

    Kubernetes list calls expose no name query parameter, so the name filter is
    applied locally after the full list is fetched.
    """
    if not name:
        return list(items)
    wanted = str(name).strip().lower()
    out = []
    for item in items:
        value = _meta(item).get("name")
        if value is not None and wanted in str(value).lower():
            out.append(item)
    return out


def collect(resource, region, namespace=None, name=None, label_selector=None,
            field_selector=None, limit=DEFAULT_PAGE_SIZE, max_pages=MAX_PAGES):
    """Query all pages of one CCI resource (KooCLI only; no SDK fallback)."""
    spec = RESOURCES[resource]
    operation = (spec["scoped_operation"] if (namespace and spec["scoped_operation"])
                 else spec["operation"])
    items = []
    continue_token = None
    for _page in range(max_pages):
        argv = build_command(resource, region, namespace=namespace,
                             limit=limit, continue_token=continue_token)
        if label_selector:
            argv.append("--labelSelector=%s" % label_selector)
        if field_selector:
            argv.append("--fieldSelector=%s" % field_selector)
        stdout, stderr, returncode = run_hcloud(argv)
        if returncode != 0 or _USE_ERROR_MARKER in (stdout + " " + stderr).lower():
            raise classify_hcloud_failure(stdout, stderr, returncode,
                                          spec["operation"], operation)
        payload = extract_json(stdout)
        batch = extract_items(payload)
        items.extend(batch)
        continue_token = next_continue_token(payload)
        if not continue_token or not batch:
            break
    else:
        raise ApiError("翻页超过 %d 页仍未取完，已中止以防死循环。" % max_pages)
    if name:
        items = filter_by_name(items, name)
    return items


def normalize_item(item, resource):
    """Flatten a Kubernetes object into table-friendly key fields."""
    meta = _meta(item)
    status = _status(item)
    spec = _spec(item)
    flat = {
        "name": meta.get("name"),
        "namespace": meta.get("namespace", "-"),
        "uid": meta.get("uid"),
        "creation_timestamp": meta.get("creationTimestamp"),
        "resource_version": meta.get("resourceVersion"),
    }
    if resource == "namespace":
        flat["status"] = status.get("phase")
    elif resource == "pod":
        flat["status"] = status.get("phase")
        flat["pod_ip"] = status.get("podIP")
        flat["node_name"] = spec.get("nodeName")
        images = []
        for container in spec.get("containers") or []:
            if isinstance(container, dict) and container.get("image"):
                images.append(str(container.get("image")))
        flat["images"] = ",".join(images) if images else "-"
    elif resource == "deployment":
        replicas = spec.get("replicas")
        ready = status.get("readyReplicas")
        flat["replicas"] = replicas if replicas is not None else "-"
        flat["ready_replicas"] = ready if ready is not None else 0
        flat["status"] = "%s/%s" % (ready if ready is not None else 0,
                                    replicas if replicas is not None else "-")
    labels = meta.get("labels")
    if isinstance(labels, dict) and labels:
        flat["labels"] = ",".join("%s=%s" % (k, v) for k, v in sorted(labels.items()))
    return flat


def _cell(value):
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return str(value)


def render_table(items, resource):
    """Render the key-field table (union of normalized columns)."""
    rows_data = [normalize_item(item, resource) for item in items]
    columns = []
    for key in PREFERRED_COLUMNS:
        if any(key in i for i in rows_data):
            columns.append(key)
    for key in sorted({k for i in rows_data for k in i}):
        if key not in columns:
            columns.append(key)
    if not columns:
        columns = ["name", "namespace"]
    rows = [[_cell(_field(i, col)) for col in columns] for i in rows_data]
    widths = [max(len(col), *(len(row[i]) for row in rows))
              for i, col in enumerate(columns)]
    header = "  ".join(col.ljust(widths[i]) for i, col in enumerate(columns))
    separator = "  ".join("-" * w for w in widths)
    lines = [header, separator]
    for row in rows:
        lines.append("  ".join(row[i].ljust(widths[i])
                               for i in range(len(columns))))
    return "\n".join(lines)


def item_summary_lines(items, resource):
    """Compact `namespace/name` (or `name`) lines for the --names-only mode."""
    lines = []
    for item in items:
        name = _meta(item).get("name", "-")
        namespace = _meta(item).get("namespace")
        if resource == "namespace" or not namespace:
            lines.append(str(name))
        else:
            lines.append("%s/%s" % (namespace, name))
    return lines


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="查询华为云云容器实例（CCI）资源列表"
                    "（KooCLI 只读 List，默认 namespace）。")
    parser.add_argument("--resource", default="namespace",
                        choices=sorted(RESOURCES.keys()),
                        help="要列出的 CCI 资源（默认 namespace）")
    parser.add_argument("-r", "--region", default=DEFAULT_REGION,
                        help="目标 Region（默认 %s）" % DEFAULT_REGION)
    parser.add_argument("-n", "--namespace", dest="namespace",
                        help="命名空间（pod/deployment 指定时查询该命名空间；"
                             "省略则跨命名空间查询全部）")
    parser.add_argument("--name", help="按名称过滤（本地过滤，大小写不敏感子串）")
    parser.add_argument("--label-selector", dest="label_selector",
                        help="Kubernetes 标签选择器（服务端查询参数，如 app=web）")
    parser.add_argument("--field-selector", dest="field_selector",
                        help="Kubernetes 字段选择器（服务端查询参数，如 status.phase=Running）")
    parser.add_argument("--json", action="store_true", dest="as_json",
                        help="以 JSON 输出完整原始对象")
    parser.add_argument("--names-only", action="store_true", dest="names_only",
                        help="仅输出名称清单（pod/deployment 为 namespace/name）")
    parser.add_argument("--page-size", type=int, default=DEFAULT_PAGE_SIZE,
                        dest="page_size", help="分页大小（默认 %d，自动翻页取全量）" % DEFAULT_PAGE_SIZE)
    parser.add_argument("--operation", default=None,
                        help="hcloud CCI 操作名（仅允许当前资源的只读 List 操作）")

    # Guard runs on the RAW argv before argparse so a mutating flag is reported
    # as a guard violation rather than an argparse error.
    try:
        guard_write_intent(guard_text_from_argv(argv))
    except CciListError as exc:
        print("[错误] %s" % exc, file=sys.stderr)
        return 1

    args = parser.parse_args(argv)
    spec = RESOURCES[args.resource]

    try:
        guard_operation(args.operation or spec["operation"], args.resource)
        if args.page_size is not None and (
                args.page_size < 1 or args.page_size > 1000):
            raise ApiError("--page-size 超出范围（1~1000）：%d" % args.page_size)
        items = collect(
            args.resource,
            args.region,
            namespace=args.namespace,
            name=args.name,
            label_selector=args.label_selector,
            field_selector=args.field_selector,
            limit=args.page_size,
        )
    except CciListError as exc:
        print("[错误] %s" % exc, file=sys.stderr)
        return 1

    if args.as_json:
        print(json.dumps(items, ensure_ascii=False, indent=2))
        return 0

    scope = args.region
    if args.namespace and spec["scoped_operation"]:
        scope += "，namespace=%s" % args.namespace

    if args.names_only:
        if not items:
            print(_empty_message(args, spec))
            return 0
        print("%s（region=%s，共 %d 个）：" % (spec["label"], scope, len(items)))
        for line in item_summary_lines(items, args.resource):
            print("- %s" % line)
        return 0

    if not items:
        print(_empty_message(args, spec))
        return 0

    print("%s（region=%s，共 %d 个，关键字段）："
          % (spec["label"], scope, len(items)))
    print(render_table(items, args.resource))
    return 0


def _empty_message(args, spec):
    filters = []
    if args.namespace:
        filters.append("namespace=%s" % args.namespace)
    if args.name:
        filters.append("name=%s" % args.name)
    if args.label_selector:
        filters.append("labelSelector=%s" % args.label_selector)
    if args.field_selector:
        filters.append("fieldSelector=%s" % args.field_selector)
    suffix = "（过滤条件: %s）" % ", ".join(filters) if filters else ""
    return "当前区域（%s）无 CCI 资源（resource=%s）%s。" % (
        args.region, args.resource, suffix)


if __name__ == "__main__":
    sys.exit(main())