#!/usr/bin/env python3
"""List Huawei Cloud MRS clusters via KooCLI `hcloud MRS ListClusters` (read-only GET).

Reads nothing but the active KooCLI credential profile. Supports three output
modes (table / --json / --names-only), a --cluster-state filter, and a strict
write-intent guard: any argument that looks like a mutating MRS operation is
rejected before a single command is executed.

Usage:
    python3 scripts/list_mrs.py [--region cn-north-4] [--json | --names-only]
                                 [--cluster-state running] [--cluster-name mrs-01]
                                 [--page-size 10] [--operation ListClusters]

Environment overrides (mostly for tests):
    MRS_LIST_HCLOUD_BIN   hcloud executable (default "hcloud")
    MRS_LIST_HCLOUD_ARGS  extra args injected before the MRS operation
"""

import argparse
import json
import os
import re
import subprocess
import sys

DEFAULT_REGION = "cn-north-4"
DEFAULT_PAGE_SIZE = 10
SERVICE = "MRS"
ALLOWED_OPERATION = "ListClusters"

# Mutating MRS operations / intents — strictly rejected by the guard.
WRITE_INTENT_KEYWORDS = (
    "createcluster",
    "deletecluster",
    "updatecluster",
    "modifycluster",
    "scaleout",
    "scalein",
    "resizcluster",
    "restartcluster",
    "stopcluster",
    "terminatecluster",
    "patchcluster",
    "submitjob",
    "stopjob",
    "killjob",
    "creating",
    "deleting",
    "updating",
    "scaling",
    "terminating",
    "create",
    "delete",
    "update",
    "scale",
    "restart",
    "terminate",
    "destroy",
)

# Preferred column order for the table view; remaining keys are appended sorted.
PREFERRED_COLUMNS = [
    "clusterId",
    "clusterName",
    "clusterState",
    "billingType",
    "version",
    "masterNodeNum",
    "coreNodeNum",
    "taskNodeNum",
    "create",
    "update",
    "datacenter",
    "vpc",
    "subnetId",
    "enterpriseProjectId",
    "tags",
    "errorMessage",
]

_CLUSTER_LIST_KEYS = ("cluster_infos", "clusters", "clusterInfos")

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


class MrsListError(Exception):
    """Base error for the MRS list skill."""


class GuardError(MrsListError):
    """A write intent was detected and blocked (skill is read-only)."""


class ConfigError(MrsListError):
    """hcloud missing or credentials (AK/SK) not configured."""


class AuthError(MrsListError):
    """Authentication/authorization failure (invalid AK/SK or IAM 403)."""


class ApiError(MrsListError):
    """hcloud / network / unexpected API failure."""


def guard_write_intent(text):
    """Return True if `text` carries a mutating intent; raise GuardError.

    Normalizes separators so `--create-cluster`, `CreateCluster`, and
    `create_cluster` all hit the same keyword. Read-only vocabulary
    (list/show/get/describe) never matches.
    """
    low = re.sub(r"[\s_\-]+", "", str(text).lower())
    for keyword in WRITE_INTENT_KEYWORDS:
        if keyword in low:
            raise GuardError(
                "检测到写操作意图（关键词: %s）。本 skill 仅支持只读查询"
                "（MRS ListClusters），创建/删除/扩缩容/重启等变更操作已被守卫拦截。" % keyword
            )
    return False


def guard_operation(operation):
    """Only the read-only ListClusters operation may be executed."""
    if operation != ALLOWED_OPERATION:
        raise GuardError(
            "不允许的操作 %r：本 skill 仅允许只读操作 %s。" % (operation, ALLOWED_OPERATION)
        )
    return True


def build_command(region, cluster_state=None, cluster_name=None,
                  page_size=DEFAULT_PAGE_SIZE, current_page=1):
    """Build the hcloud MRS ListClusters argv (without the executable)."""
    argv = [
        SERVICE,
        ALLOWED_OPERATION,
        "--cli-region=%s" % region,
        "--pageSize=%d" % page_size,
        "--currentPage=%d" % current_page,
    ]
    if cluster_state:
        argv.append("--clusterState=%s" % cluster_state)
    if cluster_name:
        argv.append("--clusterName=%s" % cluster_name)
    return argv


def _hcloud_executable():
    return os.environ.get("MRS_LIST_HCLOUD_BIN", "hcloud")


def run_hcloud(argv):
    """Execute hcloud and return (stdout, stderr, returncode)."""
    cmd = [_hcloud_executable()]
    extra = os.environ.get("MRS_LIST_HCLOUD_ARGS", "").split()
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
    if any(p in low for p in _AUTH_PATTERNS):
        return AuthError(
            "认证/授权失败（AK/SK 无效或 IAM 权限不足，403）：请检查凭证有效性，"
            "并确认已授予 MRS 只读权限（mrs:cluster:list），参见"
            " references/iam-policies.md。详情：%s" % blob[:300]
        )
    return ApiError(
        "hcloud 调用失败（退出码 %s）：%s" % (returncode, blob[:300])
    )


def extract_clusters(payload):
    """Pull the cluster list out of a ListClusters response."""
    if isinstance(payload, list):
        return payload
    for key in _CLUSTER_LIST_KEYS:
        value = payload.get(key)
        if isinstance(value, list):
            return value
    return []


def _has_more(batch, collected, page_size, payload):
    if not batch:
        return False
    if isinstance(payload, dict) and payload.get("isFinished") is True:
        return False
    total = payload.get("total") if isinstance(payload, dict) else None
    if isinstance(total, int) and total >= 0:
        return collected < total
    return len(batch) >= page_size


def list_clusters(region, cluster_state=None, cluster_name=None,
                  page_size=DEFAULT_PAGE_SIZE, max_pages=100):
    """Query all MRS clusters (paged) and return the raw cluster dicts."""
    clusters = []
    current_page = 1
    while current_page <= max_pages:
        argv = build_command(region, cluster_state=cluster_state,
                             cluster_name=cluster_name,
                             page_size=page_size, current_page=current_page)
        stdout, stderr, returncode = run_hcloud(argv)
        if returncode != 0:
            raise classify_hcloud_failure(stdout, stderr, returncode)
        payload = extract_json(stdout)
        batch = extract_clusters(payload)
        clusters.extend(batch)
        if not _has_more(batch, len(clusters), page_size, payload):
            break
        current_page += 1
    else:
        raise ApiError("翻页超过 %d 页仍未取完，已中止以防死循环。" % max_pages)
    return clusters


def _field(cluster, *names, default="-"):
    for name in names:
        if name in cluster and cluster[name] not in (None, ""):
            return cluster[name]
    return default


def cluster_names(clusters):
    names = []
    for cluster in clusters:
        name = _field(cluster, "clusterName", "cluster_name", "name", default=None)
        if name is None:
            name = _field(cluster, "clusterId", "cluster_id", "id")
        names.append(str(name))
    return names


def _cell(value):
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return str(value)


def render_table(clusters):
    """Render full-field table output (union of all returned fields)."""
    columns = []
    for key in PREFERRED_COLUMNS:
        if any(key in c for c in clusters):
            columns.append(key)
    for key in sorted({k for c in clusters for k in c}):
        if key not in columns:
            columns.append(key)
    if not columns:
        columns = ["clusterName", "clusterId"]
    rows = [[_cell(_field(c, col)) for col in columns] for c in clusters]
    widths = [max(len(col), *(len(row[i]) for row in rows)) for i, col in enumerate(columns)]
    header = "  ".join(col.ljust(widths[i]) for i, col in enumerate(columns))
    separator = "  ".join("-" * w for w in widths)
    lines = [header, separator]
    for row in rows:
        lines.append("  ".join(row[i].ljust(widths[i]) for i in range(len(columns))))
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="查询华为云 MRS 集群列表（KooCLI hcloud MRS ListClusters，只读）。")
    parser.add_argument("-r", "--region", default=DEFAULT_REGION,
                        help="目标 Region（默认 %s）" % DEFAULT_REGION)
    parser.add_argument("--json", action="store_true", dest="as_json",
                        help="以 JSON 输出完整原始字段")
    parser.add_argument("--names-only", action="store_true", dest="names_only",
                        help="仅输出集群名称清单")
    parser.add_argument("--cluster-state", dest="cluster_state",
                        help="按集群状态过滤（running/terminated/failed/abnormal 等）")
    parser.add_argument("--cluster-name", dest="cluster_name",
                        help="按集群名称过滤")
    parser.add_argument("--page-size", type=int, default=DEFAULT_PAGE_SIZE,
                        dest="page_size", help="分页大小（默认 %d）" % DEFAULT_PAGE_SIZE)
    parser.add_argument("--operation", default=ALLOWED_OPERATION,
                        help="hcloud MRS 操作名（仅允许只读 %s）" % ALLOWED_OPERATION)
    args = parser.parse_args(argv)

    try:
        # Write-intent guard: scan the raw argv + validate the operation name.
        guard_write_intent(" ".join(argv if argv is not None else sys.argv[1:]))
        guard_operation(args.operation)
        if args.cluster_state:
            guard_write_intent(args.cluster_state)
        clusters = list_clusters(
            args.region,
            cluster_state=args.cluster_state,
            cluster_name=args.cluster_name,
            page_size=args.page_size,
        )
    except MrsListError as exc:
        print("[错误] %s" % exc, file=sys.stderr)
        return 1

    if args.as_json:
        print(json.dumps(clusters, ensure_ascii=False, indent=2))
        return 0

    if args.names_only:
        print("Region %s 的 MRS 集群名称列表（共 %d 个）：" % (args.region, len(clusters)))
        for name in cluster_names(clusters):
            print("- %s" % name)
        return 0

    if not clusters:
        print("Region %s 下暂无 MRS 集群%s。" % (
            args.region,
            "（过滤条件: clusterState=%s）" % args.cluster_state if args.cluster_state else "",
        ))
        return 0

    print("Region %s 的 MRS 集群列表（共 %d 个，完整字段）：" % (args.region, len(clusters)))
    print(render_table(clusters))
    return 0


if __name__ == "__main__":
    sys.exit(main())
