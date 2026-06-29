"""CCE autoscaling diagnosis for HPA and Cluster Autoscaler paths."""

from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, Optional

from . import cce, cce_hpa, cce_metrics


WORKLOAD_KEYWORDS = (
    "pod",
    "pods",
    "workload",
    "deployment",
    "statefulset",
    "replica",
    "replicas",
    "副本",
    "实例",
    "工作负载",
)
NODE_KEYWORDS = (
    "node",
    "nodes",
    "ecs",
    "vm",
    "server",
    "节点",
    "虚拟机",
    "服务器",
    "主机",
)
SCALE_DOWN_KEYWORDS = ("缩容", "scale down", "scaledown", "减少", "回收", "删除节点")
SCALE_UP_KEYWORDS = ("扩容", "scale up", "scaleup", "增加", "新增", "拉起")
CA_ADDON_KEYWORDS = ("autoscaler", "cluster-autoscaler", "autoscaling", "弹性引擎", "elastic")
METRIC_ADDON_KEYWORDS = ("metrics-server", "prometheus", "aom", "monitor", "metric")
SAFE_TO_EVICT_KEY = "cluster-autoscaler.kubernetes.io/safe-to-evict"

CA_POD_NAME_KEYWORDS = ("autoscaler", "cce-elastic", "elastic-engine", "cluster-autoscaling")

CA_LOG_PATTERNS: list[tuple[re.Pattern, str, str, str]] = [
    # (regex, issue_code, title, severity)
    # --- scale-up blockers ---
    (re.compile(r"(?i)no\s*expansion\s*options"), "CA_LOG_NO_EXPANSION_OPTIONS", "CA 日志显示无可扩容选项", "critical"),
    (re.compile(r"(?i)max\s*(imum)?\s*node\s*group\s*size"), "CA_LOG_MAX_NODE_GROUP_SIZE", "CA 日志显示节点组已达最大尺寸", "critical"),
    (re.compile(r"(?i)(scale\s*up|expand).*plan\s*(is\s*)?empty"), "CA_LOG_SCALE_UP_PLAN_EMPTY", "CA 日志显示扩容最终计划为空", "critical"),
    (re.compile(r"(?i)skipping\s*node\s*group"), "CA_LOG_SKIPPING_NODE_GROUP", "CA 日志显示跳过了节点组", "high"),
    (re.compile(r"(?i)(pod|pods).*(can\s*\'?t\s*be\s*scheduled|is\s*unschedulable)"), "CA_LOG_UNSCHEDULABLE_POD", "CA 日志检测到不可调度 Pod", "info"),
    (re.compile(r"(?i)estimated.*\d+.*pending"), "CA_LOG_ESTIMATED_PENDING", "CA 日志估算到 Pending Pod 数量", "info"),
    # --- scale-down blockers ---
    (re.compile(r"(?i)not\s*suitable\s*for\s*removal"), "CA_LOG_NODE_NOT_SUITABLE", "CA 日志判定节点不适合缩容", "high"),
    (re.compile(r"(?i)scale\s*down.*(no|0)\s*candidate"), "CA_LOG_NO_SCALE_DOWN_CANDIDATES", "CA 日志缩容无候选节点", "info"),
    (re.compile(r"(?i)(not\s*safe\s*to\s*evict|safe\s*to\s*evict.*(false|protection))"), "CA_LOG_SAFE_TO_EVICT_BLOCK", "CA 日志因 safe-to-evict/pdb 阻止驱逐", "high"),
    (re.compile(r"(?i)node.*is\s*(unremovable|cannot\s*be\s*removed)"), "CA_LOG_NODE_UNREMOVABLE", "CA 日志节点不可移除", "medium"),
    # --- cloud resource errors ---
    (re.compile(r"(?i)(quota\s*exceeded?|insufficient\s*quota|quota.*limit)"), "CA_LOG_QUOTA_EXCEEDED", "CA 日志显示云资源配额超限", "critical"),
    (re.compile(r"(?i)(subnet.*(exhaust|insufficient|full|no\s*ip)|insufficient\s*ip|ip\s*(exhaust|deplete))"), "CA_LOG_SUBNET_IP_EXHAUSTED", "CA 日志显示子网 IP 耗竭", "critical"),
    (re.compile(r"(?i)(insufficient\s*(cpu|memory|resource))"), "CA_LOG_INSUFFICIENT_RESOURCE", "CA 日志显示资源不足以调度", "high"),
    # --- permission / IAM errors ---
    (re.compile(r"(?i)(iam|agency|委托|permission.*(denied?|missing|forbidden)|unauthorized|403|401)"), "CA_LOG_IAM_PERMISSION_ERROR", "CA 日志显示 IAM/权限异常", "critical"),
    # --- connectivity / API errors ---
    (re.compile(r"(?i)(failed\s*to\s*refresh|cannot\s*connect|connection\s*refused|time\s*out|api.*error)"), "CA_LOG_API_CONNECTIVITY_ERROR", "CA 日志显示云 API 连接异常", "high"),
    # --- generic health ---
    (re.compile(r"(?i)(error|exception|panic|fatal)"), "CA_LOG_GENERIC_ERROR", "CA 日志含错误/异常/panic 信号", "medium"),
]


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    return str(value)


def _lower_blob(*values: Any) -> str:
    return " ".join(_text(value).lower() for value in values if value is not None)


def _as_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    return str(value).strip().lower() in {"true", "1", "yes", "y", "on", "enable", "enabled"}


def _as_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _dict(value: Any) -> Dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _dig(data: Dict[str, Any], *keys: str) -> Any:
    current: Any = data
    for key in keys:
        if not isinstance(current, dict):
            return None
        if key in current:
            current = current[key]
            continue
        alt = _camel_to_snake(key)
        if alt in current:
            current = current[alt]
            continue
        alt = _snake_to_camel(key)
        if alt in current:
            current = current[alt]
            continue
        return None
    return current


def _camel_to_snake(value: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", value).lower()


def _snake_to_camel(value: str) -> str:
    parts = value.split("_")
    return parts[0] + "".join(part[:1].upper() + part[1:] for part in parts[1:])


def classify_intent(question: str = "", target: Optional[str] = None) -> str:
    explicit = (target or "").strip().upper()
    if explicit in {"WORKLOAD", "POD", "HPA"}:
        return "WORKLOAD"
    if explicit in {"NODE", "CA", "CLUSTER_AUTOSCALER"}:
        return "NODE"
    text = question.lower()
    has_workload = any(keyword.lower() in text for keyword in WORKLOAD_KEYWORDS)
    has_node = any(keyword.lower() in text for keyword in NODE_KEYWORDS)
    if has_workload and not has_node:
        return "WORKLOAD"
    if has_node and not has_workload:
        return "NODE"
    return "UNKNOWN"


def classify_scale_direction(question: str = "", scale_direction: Optional[str] = None) -> str:
    explicit = (scale_direction or "").strip().lower().replace("_", "-")
    if explicit in {"up", "scale-up", "expand", "扩容"}:
        return "scale_up"
    if explicit in {"down", "scale-down", "shrink", "缩容"}:
        return "scale_down"
    text = question.lower()
    if any(keyword in text for keyword in SCALE_DOWN_KEYWORDS):
        return "scale_down"
    if any(keyword in text for keyword in SCALE_UP_KEYWORDS):
        return "scale_up"
    return "unknown"


def _collection_gap(name: str, response: Dict[str, Any]) -> Optional[str]:
    if response.get("success", True):
        return None
    error = response.get("error") or response.get("error_type") or "collection failed"
    return f"{name}: {error}"


def _version_tuple(version: Any) -> tuple[int, ...]:
    numbers = re.findall(r"\d+", _text(version))
    return tuple(int(item) for item in numbers[:4])


def _addon_discovery(addons: Dict[str, Any]) -> Dict[str, Any]:
    ca_matches = []
    metric_matches = []
    for addon in _list(addons.get("addons")):
        blob = _lower_blob(
            addon.get("name"),
            addon.get("template_name"),
            addon.get("description"),
            addon.get("version"),
        )
        if any(keyword in blob for keyword in CA_ADDON_KEYWORDS):
            ca_matches.append(addon)
        if any(keyword in blob for keyword in METRIC_ADDON_KEYWORDS):
            metric_matches.append(addon)

    low_version = []
    abnormal = []
    for addon in ca_matches:
        version = _version_tuple(addon.get("version"))
        if version and version < (1, 13, 8):
            low_version.append(addon)
        status = _text(addon.get("status")).lower()
        if status in {"abnormal", "failed", "error", "deleting", "install_failed", "upgrade_failed", "rollback_failed"}:
            abnormal.append(addon)

    return {
        "ca_addon_installed": bool(ca_matches),
        "ca_addons": ca_matches,
        "ca_addon_low_version": low_version,
        "ca_addon_abnormal": abnormal,
        "metric_addons": metric_matches,
        "metric_addon_detected": bool(metric_matches),
    }


def _group_current_count(group: Dict[str, Any], statuses: Iterable[Dict[str, Any]]) -> Optional[int]:
    group_name = group.get("name")
    for status in statuses:
        if group_name and status.get("name") == group_name and status.get("current_node_count") is not None:
            return _as_int(status.get("current_node_count"))
    for key in ("current_node_count", "initial_node_count"):
        if group.get(key) is not None:
            return _as_int(group.get(key))
    return None


def _nodepool_discovery(nodepools: Dict[str, Any]) -> Dict[str, Any]:
    enabled = False
    max_reached = []
    pools = []
    for pool in _list(nodepools.get("nodepools")):
        statuses = _list(pool.get("scale_group_statuses"))
        pool_entry = {
            "name": pool.get("name") or pool.get("id"),
            "id": pool.get("id"),
            "enabled": False,
            "groups": [],
        }
        for group in _list(pool.get("scale_groups")):
            autoscaling = _dict(group.get("autoscaling"))
            group_enabled = (
                _as_bool(autoscaling.get("enable"))
                or _as_bool(autoscaling.get("enabled"))
                or _as_bool(pool.get("autoscaling_enabled"))
            )
            current = _group_current_count(_dict(group), statuses)
            min_nodes = group.get("min_node_count") or autoscaling.get("min_node_count")
            max_nodes = group.get("max_node_count") or autoscaling.get("max_node_count")
            group_entry = {
                "name": group.get("name") or "default",
                "enabled": group_enabled,
                "current_node_count": current,
                "min_node_count": min_nodes,
                "max_node_count": max_nodes,
                "flavor": group.get("flavor"),
                "availability_zone": group.get("availability_zone"),
            }
            if group_enabled:
                enabled = True
                pool_entry["enabled"] = True
                if max_nodes is not None and current is not None and current >= _as_int(max_nodes):
                    max_reached.append({
                        "nodepool": pool_entry["name"],
                        "scale_group": group_entry["name"],
                        "current_node_count": current,
                        "max_node_count": _as_int(max_nodes),
                    })
            pool_entry["groups"].append(group_entry)
        pools.append(pool_entry)

    return {
        "nodepool_autoscaling_enabled": enabled,
        "nodepool_count": nodepools.get("count"),
        "nodepools": pools,
        "max_reached": max_reached,
    }


def _target_ref(hpa: Dict[str, Any]) -> Dict[str, Any]:
    ref = _dict(hpa.get("scale_target_ref"))
    return {
        "kind": ref.get("kind") or ref.get("Kind"),
        "name": ref.get("name") or ref.get("Name"),
        "api_version": ref.get("api_version") or ref.get("apiVersion"),
    }


def _kind_matches(left: Optional[str], right: Optional[str]) -> bool:
    if not left or not right:
        return True
    return left.strip().lower() == right.strip().lower()


def _select_hpas(
    hpas: Dict[str, Any],
    namespace: Optional[str],
    workload_name: Optional[str],
    workload_type: Optional[str],
) -> list[Dict[str, Any]]:
    items = _list(hpas.get("hpas"))
    selected = []
    for hpa in items:
        ref = _target_ref(hpa)
        if namespace and hpa.get("namespace") != namespace:
            continue
        if workload_name and ref.get("name") != workload_name:
            continue
        if workload_type and not _kind_matches(ref.get("kind"), workload_type):
            continue
        selected.append(hpa)
    return selected


def _workload_rows(deployments: Dict[str, Any], statefulsets: Dict[str, Any]) -> list[Dict[str, Any]]:
    rows: list[Dict[str, Any]] = []
    for dep in _list(deployments.get("deployments")):
        item = dict(dep)
        item["kind"] = "Deployment"
        rows.append(item)
    for sts in _list(statefulsets.get("statefulsets")):
        item = dict(sts)
        item["kind"] = "StatefulSet"
        item["replicas"] = item.get("current_replicas")
        rows.append(item)
    return rows


def _find_workload(
    workloads: Iterable[Dict[str, Any]],
    namespace: Optional[str],
    name: Optional[str],
    kind: Optional[str],
) -> Optional[Dict[str, Any]]:
    if not name:
        return None
    for workload in workloads:
        if namespace and workload.get("namespace") != namespace:
            continue
        if workload.get("name") != name:
            continue
        if kind and not _kind_matches(workload.get("kind"), kind):
            continue
        return workload
    return None


def _pod_owner_blob(pod: Dict[str, Any]) -> str:
    owners = []
    for owner in _list(pod.get("owner_references")):
        owners.append(f"{owner.get('kind')}:{owner.get('name')}")
    return " ".join(owners)


def _pod_matches_workload(pod: Dict[str, Any], namespace: str, name: str, kind: str) -> bool:
    if pod.get("namespace") != namespace:
        return False
    owners = _list(pod.get("owner_references"))
    for owner in owners:
        if owner.get("kind") == kind and owner.get("name") == name:
            return True
        if kind == "Deployment" and owner.get("kind") == "ReplicaSet" and _text(owner.get("name")).startswith(f"{name}-"):
            return True
    pod_name = _text(pod.get("name"))
    if kind == "StatefulSet":
        return pod_name.startswith(f"{name}-")
    if kind == "Deployment":
        return pod_name.startswith(f"{name}-")
    return False


def _pods_for_hpa(hpa: Dict[str, Any], pods: Dict[str, Any]) -> list[Dict[str, Any]]:
    ref = _target_ref(hpa)
    namespace = hpa.get("namespace")
    name = ref.get("name")
    kind = ref.get("kind") or "Deployment"
    if not namespace or not name:
        return []
    return [pod for pod in _list(pods.get("pods")) if _pod_matches_workload(pod, namespace, name, kind)]


def _requested_resource_metrics(hpa: Dict[str, Any]) -> list[str]:
    result = []
    for metric in _list(hpa.get("metrics")):
        resource = _dict(metric.get("resource"))
        name = resource.get("name")
        target_type = _dig(resource, "target", "type")
        if name in {"cpu", "memory"} and _text(target_type).lower() == "utilization":
            result.append(name)
    return sorted(set(result))


def _missing_requests(pods: Iterable[Dict[str, Any]], required_metrics: Iterable[str]) -> list[Dict[str, Any]]:
    metrics = set(required_metrics)
    if not metrics:
        return []
    missing = []
    for pod in pods:
        for container in _list(pod.get("containers")) + _list(pod.get("init_containers")):
            requests = _dict(_dict(container.get("resources")).get("requests"))
            absent = sorted(metric for metric in metrics if not requests.get(metric))
            if absent:
                missing.append({
                    "namespace": pod.get("namespace"),
                    "pod": pod.get("name"),
                    "container": container.get("name"),
                    "missing_requests": absent,
                })
    return missing


def _event_text(event: Dict[str, Any]) -> str:
    return _lower_blob(
        event.get("type"),
        event.get("reason"),
        event.get("message"),
        event.get("name"),
        _dict(event.get("involved_object")).get("kind"),
        _dict(event.get("involved_object")).get("name"),
    )


def _events_for_hpa(events: Dict[str, Any], hpa: Dict[str, Any]) -> list[Dict[str, Any]]:
    namespace = hpa.get("namespace")
    name = hpa.get("name")
    selected = []
    for event in _list(events.get("events")):
        involved = _dict(event.get("involved_object"))
        if namespace and event.get("namespace") not in {namespace, None}:
            continue
        if involved.get("kind") == "HorizontalPodAutoscaler" and involved.get("name") == name:
            selected.append(event)
            continue
        if name and name.lower() in _event_text(event):
            selected.append(event)
    return selected


def _events_for_pending_pods(events: Dict[str, Any], pending_pods: Iterable[Dict[str, Any]]) -> list[Dict[str, Any]]:
    pod_keys = {(pod.get("namespace"), pod.get("name")) for pod in pending_pods}
    selected = []
    for event in _list(events.get("events")):
        involved = _dict(event.get("involved_object"))
        if event.get("reason") != "FailedScheduling":
            continue
        key = (involved.get("namespace") or event.get("namespace"), involved.get("name"))
        if not pod_keys or key in pod_keys:
            selected.append(event)
    return selected


def _metric_entries(hpa: Dict[str, Any]) -> list[Dict[str, Any]]:
    spec_by_name: dict[str, Dict[str, Any]] = {}
    for metric in _list(hpa.get("metrics")):
        resource = _dict(metric.get("resource"))
        name = resource.get("name")
        if name:
            spec_by_name[name] = resource

    entries = []
    for metric in _list(hpa.get("current_metrics")):
        resource = _dict(metric.get("resource"))
        name = resource.get("name")
        if not name:
            continue
        current = _dict(resource.get("current"))
        spec = _dict(spec_by_name.get(name))
        target = _dict(spec.get("target"))
        current_util = current.get("average_utilization") or current.get("averageUtilization")
        target_util = target.get("average_utilization") or target.get("averageUtilization")
        ratio = None
        if current_util is not None and target_util:
            ratio = float(current_util) / float(target_util)
        entries.append({
            "resource": name,
            "current_average_utilization": current_util,
            "target_average_utilization": target_util,
            "ratio": ratio,
            "current_average_value": current.get("average_value") or current.get("averageValue"),
            "target_average_value": target.get("average_value") or target.get("averageValue"),
        })
    return entries


def _condition_map(hpa: Dict[str, Any]) -> dict[str, Dict[str, Any]]:
    return {item.get("type"): item for item in _list(hpa.get("conditions")) if item.get("type")}


def _add_issue(
    issues: list[Dict[str, Any]],
    code: str,
    title: str,
    severity: str,
    layer: str,
    evidence: str,
    recommendation: str,
) -> None:
    issues.append({
        "code": code,
        "title": title,
        "severity": severity,
        "layer": layer,
        "evidence": evidence,
        "recommendation": recommendation,
    })


def _analyze_hpa_path(
    raw: Dict[str, Dict[str, Any]],
    selected_hpas: list[Dict[str, Any]],
    workloads: list[Dict[str, Any]],
    namespace: Optional[str],
    workload_name: Optional[str],
    workload_type: Optional[str],
    tolerance: float,
) -> Dict[str, Any]:
    issues: list[Dict[str, Any]] = []
    evidence: list[Dict[str, Any]] = []
    hpas = raw["hpas"]
    pods = raw["pods"]
    events = raw["events"]
    addons = _addon_discovery(raw["addons"])

    if not selected_hpas:
        scope = f"{namespace or '*'} / {workload_name or '*'}"
        code = "HPA_NOT_CONFIGURED_FOR_WORKLOAD" if workload_name else "HPA_NOT_CONFIGURED"
        _add_issue(
            issues,
            code,
            "未发现匹配的 HPA",
            "critical",
            "HPA",
            f"HPA 查询成功但匹配范围 {scope} 下没有 HPA；集群 HPA 总数={hpas.get('count', 0)}。",
            "为目标 Deployment/StatefulSet 创建 HPA，或确认客户实际使用的是 CronHPA/CustomedHPA/AHPA 等其他策略。",
        )
        return {"issues": issues, "evidence": evidence, "hpa_scaled": False}

    hpa_scaled = False
    for hpa in selected_hpas:
        ref = _target_ref(hpa)
        kind = ref.get("kind") or workload_type or "Deployment"
        target_name = ref.get("name")
        target = _find_workload(workloads, hpa.get("namespace"), target_name, kind)
        hpa_pods = _pods_for_hpa(hpa, pods)
        hpa_events = _events_for_hpa(events, hpa)
        conditions = _condition_map(hpa)
        metric_entries = _metric_entries(hpa)
        current_replicas = _as_int(hpa.get("current_replicas"))
        desired_replicas = _as_int(hpa.get("desired_replicas"))
        max_replicas = _as_int(hpa.get("max_replicas"))
        min_replicas = _as_int(hpa.get("min_replicas"))
        target_desired = _as_int(target.get("desired_replicas")) if target else None
        target_ready = _as_int(target.get("ready_replicas")) if target else None

        evidence.append({
            "layer": "HPA",
            "source": "HorizontalPodAutoscaler/status",
            "summary": (
                f"{hpa.get('namespace')}/{hpa.get('name')} -> {kind}/{target_name}, "
                f"min={min_replicas}, max={max_replicas}, current={current_replicas}, desired={desired_replicas}"
            ),
        })

        if target is None:
            _add_issue(
                issues,
                "HPA_TARGET_NOT_FOUND",
                "HPA 指向的目标工作负载不存在或未采集到",
                "critical",
                "HPA",
                f"HPA {hpa.get('namespace')}/{hpa.get('name')} scaleTargetRef={kind}/{target_name}，但目标清单中未找到。",
                "核对 HPA 的 scaleTargetRef.kind/name/apiVersion 与实际 Deployment/StatefulSet 是否一致。",
            )

        if max_replicas and desired_replicas >= max_replicas and current_replicas >= max_replicas:
            _add_issue(
                issues,
                "HPA_MAX_REPLICAS_REACHED",
                "HPA 已达到 maxReplicas",
                "critical",
                "HPA",
                f"HPA desiredReplicas/currentReplicas 均达到 maxReplicas={max_replicas}。",
                "评估业务容量后提高 maxReplicas，或降低单 Pod 资源压力。",
            )

        for condition_name, condition in conditions.items():
            reason = _text(condition.get("reason"))
            message = _text(condition.get("message"))
            blob = _lower_blob(reason, message)
            if condition_name == "ScalingActive" and str(condition.get("status")) == "False":
                if any(token in blob for token in ("failedgetresource", "failedcomputemetrics", "unable to get metric", "missing request")):
                    _add_issue(
                        issues,
                        "HPA_METRICS_MISSING",
                        "HPA 无法获得扩缩容指标",
                        "critical",
                        "HPA",
                        f"ScalingActive=False, reason={reason}, message={message}",
                        "检查 metrics-server/AOM/Prometheus 指标链路和目标 Pod 的 CPU/Memory requests。",
                    )
                else:
                    _add_issue(
                        issues,
                        "HPA_SCALING_INACTIVE",
                        "HPA ScalingActive=False",
                        "high",
                        "HPA",
                        f"reason={reason}, message={message}",
                        "继续查看 HPA Event 与 scaleTargetRef，确认指标、权限或目标对象是否异常。",
                    )
            if condition_name == "AbleToScale" and str(condition.get("status")) == "False":
                _add_issue(
                    issues,
                    "HPA_SCALE_API_BLOCKED",
                    "HPA 无法访问或更新 scale 子资源",
                    "critical",
                    "HPA",
                    f"AbleToScale=False, reason={reason}, message={message}",
                    "核对目标工作负载是否支持 scale 子资源，以及 HPA 控制器与 API 访问是否正常。",
                )
            if condition_name == "ScalingLimited" and str(condition.get("status")) == "True":
                if "too many" in blob or "max" in blob:
                    _add_issue(
                        issues,
                        "HPA_SCALING_LIMITED_BY_MAX",
                        "HPA 扩容被上限限制",
                        "high",
                        "HPA",
                        f"ScalingLimited=True, reason={reason}, message={message}",
                        "检查 maxReplicas 与业务预期峰值是否匹配。",
                    )

        for event in hpa_events:
            blob = _event_text(event)
            if "missing request" in blob or "missing request for" in blob:
                _add_issue(
                    issues,
                    "HPA_REQUEST_MISSING_EVENT",
                    "HPA Event 显示容器缺少 request",
                    "critical",
                    "HPA",
                    f"{event.get('reason')}: {event.get('message')}",
                    "给被 HPA 采样的容器补齐 CPU/Memory requests；CPU/内存利用率型 HPA 依赖 request 作为分母。",
                )
            elif any(token in blob for token in ("failedgetresource", "failedcomputemetrics", "unable to get metric", "no metrics")):
                _add_issue(
                    issues,
                    "HPA_METRIC_EVENT",
                    "HPA Event 显示指标获取失败",
                    "critical",
                    "HPA",
                    f"{event.get('reason')}: {event.get('message')}",
                    "检查 metrics.k8s.io/custom.metrics.k8s.io/external.metrics.k8s.io 及 AOM/Prometheus 数据流。",
                )
            elif any(token in blob for token in ("failedgetscale", "not found", "selector")):
                _add_issue(
                    issues,
                    "HPA_TARGET_OR_SELECTOR_EVENT",
                    "HPA Event 指向目标对象或选择器异常",
                    "high",
                    "HPA",
                    f"{event.get('reason')}: {event.get('message')}",
                    "核对 HPA scaleTargetRef、工作负载 selector 和 Pod template labels。",
                )
            elif any(token in blob for token in ("backoff", "stabiliz", "cooldown")):
                _add_issue(
                    issues,
                    "HPA_COOLDOWN_OR_STABILIZATION",
                    "HPA 处于冷却或稳定窗口",
                    "medium",
                    "HPA",
                    f"{event.get('reason')}: {event.get('message')}",
                    "等待稳定窗口结束，或审视 autoscaling/v2 behavior 的 scaleUp/scaleDown 策略。",
                )

        required_metrics = _requested_resource_metrics(hpa)
        missing = _missing_requests(hpa_pods, required_metrics)
        if missing:
            sample = ", ".join(f"{item['namespace']}/{item['pod']}:{item['container']} missing {','.join(item['missing_requests'])}" for item in missing[:5])
            _add_issue(
                issues,
                "HPA_CONTAINER_REQUEST_MISSING",
                "被 HPA 采样的容器缺少资源 request",
                "critical",
                "HPA",
                sample,
                "为所有目标 Pod 容器设置 HPA 指标对应的 resources.requests。",
            )

        if target and not hpa_pods and current_replicas > 0:
            _add_issue(
                issues,
                "HPA_TARGET_PODS_NOT_MATCHED",
                "未能按工作负载归属匹配到目标 Pod",
                "medium",
                "HPA",
                f"目标 {kind}/{target_name} 存在，但通过 owner/name 前缀未匹配到 Pod；可能是 selector/labels 异常或采集字段不足。",
                "核对工作负载 selector 与 Pod template labels，必要时通过 kubectl describe hpa/deployment 复核。",
            )

        if metric_entries:
            high_entries = [entry for entry in metric_entries if entry.get("ratio") is not None and entry["ratio"] > 1 + tolerance]
            in_tolerance = [entry for entry in metric_entries if entry.get("ratio") is not None and 1 < entry["ratio"] <= 1 + tolerance]
            below_target = [entry for entry in metric_entries if entry.get("ratio") is not None and entry["ratio"] <= 1]
            if below_target and desired_replicas <= current_replicas:
                detail = "; ".join(
                    f"{entry['resource']} current={entry['current_average_utilization']} target={entry['target_average_utilization']}"
                    for entry in below_target
                )
                _add_issue(
                    issues,
                    "HPA_THRESHOLD_NOT_EXCEEDED",
                    "当前指标未超过扩容阈值",
                    "info",
                    "HPA",
                    detail,
                    "这属于正常不扩容；如仍需更敏捷扩容，可评估降低 target utilization 或引入预测/定时策略。",
                )
            if in_tolerance and desired_replicas <= current_replicas:
                detail = "; ".join(f"{entry['resource']} ratio={entry['ratio']:.2f}" for entry in in_tolerance)
                _add_issue(
                    issues,
                    "HPA_WITHIN_TOLERANCE",
                    "指标落在 HPA 忍受度范围内",
                    "info",
                    "HPA",
                    f"{detail}; tolerance={tolerance:.2f}",
                    "HPA 默认存在忍受度，比例变化太小会保持副本数不变。",
                )
            if high_entries and desired_replicas <= current_replicas:
                detail = "; ".join(f"{entry['resource']} ratio={entry['ratio']:.2f}" for entry in high_entries)
                _add_issue(
                    issues,
                    "HPA_EXPECTED_SCALE_BUT_DESIRED_UNCHANGED",
                    "指标超过阈值但 desiredReplicas 未增长",
                    "high",
                    "HPA",
                    detail,
                    "检查 HPA 控制器事件、冷却窗口、maxReplicas 与指标时间延迟。",
                )

        if target_desired is not None and target_ready is not None and target_desired > target_ready:
            pending_for_hpa = [pod for pod in hpa_pods if pod.get("status") == "Pending" or pod.get("phase") == "Pending"]
            if pending_for_hpa or target_desired >= desired_replicas > target_ready:
                hpa_scaled = True

    if not addons["metric_addon_detected"]:
        _add_issue(
            issues,
            "METRICS_ADDON_NOT_DETECTED",
            "未在插件清单中识别到 metrics-server/AOM/Prometheus 组件",
            "medium",
            "Metrics",
            "CCE addon 列表未命中 metrics-server/prometheus/AOM/monitor 关键字。",
            "如果 HPA 依赖 CPU/内存或自定义指标，确认指标插件和 AOM/Prometheus 实例可用。",
        )

    return {"issues": issues, "evidence": evidence, "hpa_scaled": hpa_scaled}


def _pending_pods_for_scope(
    raw: Dict[str, Dict[str, Any]],
    namespace: Optional[str],
    selected_hpas: list[Dict[str, Any]],
) -> list[Dict[str, Any]]:
    pods = _list(raw["pods"].get("pods"))
    pending = [pod for pod in pods if pod.get("phase") == "Pending" or pod.get("status") == "Pending"]
    if selected_hpas:
        scoped = []
        for hpa in selected_hpas:
            hpa_pod_keys = {(pod.get("namespace"), pod.get("name")) for pod in _pods_for_hpa(hpa, raw["pods"])}
            scoped.extend([pod for pod in pending if (pod.get("namespace"), pod.get("name")) in hpa_pod_keys])
        return scoped
    if namespace:
        return [pod for pod in pending if pod.get("namespace") == namespace]
    return pending


def _find_ca_pod(pods: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """从 pod 列表中定位 cluster-autoscaler Pod（优先 kube-system 名字空间）。"""
    pod_list = _list(pods.get("pods"))
    for pod in pod_list:
        name = _text(pod.get("name")).lower()
        ns = _text(pod.get("namespace"))
        if ns == "kube-system" and any(kw in name for kw in CA_POD_NAME_KEYWORDS):
            return pod
    for pod in pod_list:
        ns = _text(pod.get("namespace"))
        if ns != "kube-system":
            continue
        owners = _pod_owner_blob(pod).lower()
        if any(kw in owners for kw in ("autoscaler", "cce-elastic", "elastic-engine")):
            return pod
    return None


def _pod_container_health(pod: Dict[str, Any]) -> Dict[str, Any]:
    """提取 Pod 中容器的健康状态摘要。"""
    phase = pod.get("phase") or pod.get("status") or "Unknown"
    containers = []
    unhealthy = []
    for c in _list(pod.get("containers")):
        state = {}
        if isinstance(c, dict):
            state = _dict(c.get("state"))
        ready = c.get("ready") if isinstance(c, dict) else None
        name = c.get("name") if isinstance(c, dict) else "?"
        containers.append({"name": name, "ready": ready, "state": state})
        waiting = _dict(state.get("waiting"))
        reason = waiting.get("reason", "")
        if reason in {"CrashLoopBackOff", "Error", "ImagePullBackOff", "ErrImagePull", "CreateContainerConfigError"}:
            unhealthy.append({"container": name, "reason": reason, "message": waiting.get("message", "")})
        terminated = _dict(state.get("terminated"))
        exit_code = terminated.get("exit_code") or terminated.get("exitCode")
        if exit_code is not None and exit_code != 0:
            unhealthy.append({
                "container": name,
                "reason": f"ExitCode:{exit_code}",
                "message": terminated.get("message") or terminated.get("reason", ""),
            })
    return {"phase": phase, "containers": containers, "unhealthy": unhealthy}


def _fetch_ca_pod_logs(
    region: str,
    cluster_id: str,
    ak: Optional[str] = None,
    sk: Optional[str] = None,
    project_id: Optional[str] = None,
    tail_lines: int = 200,
) -> Dict[str, Any]:
    """独立查询 kube-system 下的 CA Pod 并拉取日志（含健康状态 + previous 重试）。"""
    kube_pods = cce.get_kubernetes_pods(region, cluster_id, ak, sk, project_id, namespace="kube-system")
    ca_pod = _find_ca_pod(kube_pods)
    if not ca_pod:
        return {"success": True, "ca_pod_found": False, "log_lines": "", "error": "CA Pod 未在 kube-system 中识别到"}

    pod_name = ca_pod.get("name")
    pod_ns = ca_pod.get("namespace") or "kube-system"
    health = _pod_container_health(ca_pod)
    container = None
    containers = _list(ca_pod.get("containers"))
    if containers:
        container = containers[0].get("name") if isinstance(containers[0], dict) else None

    # 拉取当前容器日志
    log_result = cce.get_pod_logs(
        region=region,
        cluster_id=cluster_id,
        pod_name=pod_name,
        ak=ak,
        sk=sk,
        project_id=project_id,
        namespace=pod_ns,
        container=container,
        tail_lines=tail_lines,
    )
    logs = ""
    log_source = "current"
    if log_result.get("success"):
        logs = log_result.get("logs") or ""

    # 当前日志为空时（容器可能尚未成功启动），重试拉取上一个崩溃容器的日志
    if not logs:
        prev_result = cce.get_pod_logs(
            region=region,
            cluster_id=cluster_id,
            pod_name=pod_name,
            ak=ak,
            sk=sk,
            project_id=project_id,
            namespace=pod_ns,
            container=container,
            previous=True,
            tail_lines=tail_lines,
        )
        if prev_result.get("success"):
            prev_logs = prev_result.get("logs") or ""
            if prev_logs:
                logs = prev_logs
                log_source = "previous"

    return {
        "success": True,
        "ca_pod_found": True,
        "ca_pod_name": pod_name,
        "ca_pod_namespace": pod_ns,
        "ca_container": container,
        "ca_pod_phase": health["phase"],
        "ca_pod_unhealthy": health["unhealthy"],
        "log_lines": logs,
        "log_source": log_source,
        "tail_lines": tail_lines,
    }


def _analyze_ca_log_content(
    ca_log_result: Dict[str, Any],
    direction: str,
) -> Dict[str, Any]:
    """解析 CA Pod 日志内容，提取诊断信号。"""
    findings: list[Dict[str, Any]] = []
    log_text = ca_log_result.get("log_lines", "")
    if not log_text or not ca_log_result.get("ca_pod_found"):
        return {"findings": findings, "log_snippet": ""}

    lines = log_text.split("\n")
    for pattern, code, title, severity in CA_LOG_PATTERNS:
        matched_lines: list[str] = []
        for line_num, line in enumerate(lines, 1):
            if pattern.search(line):
                matched_lines.append(f"L{line_num}: {line.strip()[:200]}")
                if len(matched_lines) >= 3:
                    break
        if matched_lines:
            # 缩容场景下 scale-up 类 blocker 不够相关，调整严重级别
            effective_severity = severity
            if direction == "scale_down" and code in {
                "CA_LOG_NO_EXPANSION_OPTIONS",
                "CA_LOG_MAX_NODE_GROUP_SIZE",
                "CA_LOG_SCALE_UP_PLAN_EMPTY",
                "CA_LOG_SKIPPING_NODE_GROUP",
            }:
                effective_severity = "info"
            elif direction == "scale_up" and code in {
                "CA_LOG_NO_SCALE_DOWN_CANDIDATES",
                "CA_LOG_NODE_NOT_SUITABLE",
            }:
                effective_severity = "info"
            findings.append({
                "code": code,
                "title": title,
                "severity": effective_severity,
                "layer": "CA-Log",
                "evidence": " | ".join(matched_lines),
                "recommendation": _ca_log_recommendation(code),
            })

    # 截取包含最多信号的片段（取首条命中的前后各 5 行）
    snippet_lines: list[str] = []
    if findings:
        first_line = None
        for pattern, _, _, _ in CA_LOG_PATTERNS:
            for i, line in enumerate(lines):
                if pattern.search(line):
                    first_line = i
                    break
            if first_line is not None:
                break
        if first_line is not None:
            start = max(0, first_line - 5)
            end = min(len(lines), first_line + 10)
            snippet_lines = lines[start:end]
    log_snippet = "\n".join(snippet_lines[:15]) if snippet_lines else "\n".join(lines[-15:])

    return {"findings": findings, "log_snippet": log_snippet}


def _ca_log_recommendation(code: str) -> str:
    recommendations: dict[str, str] = {
        "CA_LOG_NO_EXPANSION_OPTIONS": "CA 无可用扩容选项；检查节点池规格、AZ、子网、配额是否满足待调度 Pod 需求。",
        "CA_LOG_MAX_NODE_GROUP_SIZE": "节点组已达 max_nodes，提升 max_nodes 或扩展新的可调度节点池。",
        "CA_LOG_SCALE_UP_PLAN_EMPTY": "CA 扩容最终计划为空，通常是所有节点组被跳过或节点池不满足调度要求。",
        "CA_LOG_SKIPPING_NODE_GROUP": "确认 CA 跳过该节点组的原因（规格不匹配/AZ 不匹配/已达上限/资源不足）。",
        "CA_LOG_UNSCHEDULABLE_POD": "CA 确认检测到不可调度 Pod，继续检查是否触发扩容和为什么没有扩容。",
        "CA_LOG_ESTIMATED_PENDING": "CA 已识别 Pending Pod 数量，检查是否命中扩容计划。",
        "CA_LOG_NODE_NOT_SUITABLE": "检查节点上的 PDB、safe-to-evict、系统 Pod 和资源使用率是否阻止缩容。",
        "CA_LOG_NO_SCALE_DOWN_CANDIDATES": "当前集群没有满足缩容条件的节点，可能是资源利用率仍高于阈值或保护策略拦截。",
        "CA_LOG_SAFE_TO_EVICT_BLOCK": "Pod 设置了 safe-to-evict=false 或被 PDB 保护，修改 annotation 或 PDB 后 CA 方可驱逐。",
        "CA_LOG_NODE_UNREMOVABLE": "节点上有阻止缩容的 Pod 或条件，逐一排查 kube-system 非 DaemonSet Pod 或裸 Pod。",
        "CA_LOG_QUOTA_EXCEEDED": "云资源配额不足（ECS/EVS/EIP），需要申请提升配额或释放闲置资源。",
        "CA_LOG_SUBNET_IP_EXHAUSTED": "VPC 子网可用 IP 不足，扩容子网或切换到有剩余 IP 的子网。",
        "CA_LOG_INSUFFICIENT_RESOURCE": "集群内 CPU/内存资源总量已不足以调度 Pending Pod。",
        "CA_LOG_IAM_PERMISSION_ERROR": "CCE 委托或 IAM 权限存在问题，确认弹性引擎所需权限未被收窄或删除。",
        "CA_LOG_API_CONNECTIVITY_ERROR": "CA 无法连接云 API 或控制面，检查网络/安全组/API 端点可达性。",
        "CA_LOG_GENERIC_ERROR": "CA 日志含通用异常信号，建议扩大 tail_lines 或从 LTS 拉取更多日志进一步排查。",
    }
    return recommendations.get(code, "检视 CA 日志中匹配行的上下文，必要时拉取更多日志或开启 CA 调试级别。")


def _analyze_ca_path(
    raw: Dict[str, Dict[str, Any]],
    selected_hpas: list[Dict[str, Any]],
    namespace: Optional[str],
    direction: str,
) -> Dict[str, Any]:
    issues: list[Dict[str, Any]] = []
    evidence: list[Dict[str, Any]] = []
    addon_info = _addon_discovery(raw["addons"])
    nodepool_info = _nodepool_discovery(raw["nodepools"])
    pending = _pending_pods_for_scope(raw, namespace, selected_hpas)
    scheduling_events = _events_for_pending_pods(raw["events"], pending)

    # —— CA Pod 日志分析 ——
    ca_log_result = raw.get("ca_pod_logs", {})
    ca_log_analysis = _analyze_ca_log_content(ca_log_result, direction)
    ca_log_findings = ca_log_analysis.get("findings", [])
    ca_log_snippet = ca_log_analysis.get("log_snippet", "")
    if ca_log_result.get("ca_pod_found"):
        evidence.append({
            "layer": "CA-Log",
            "source": f"Pod/{ca_log_result.get('ca_pod_name', '?')} logs (tail={ca_log_result.get('tail_lines', '?')})",
            "summary": (
                f"CA Pod={ca_log_result.get('ca_pod_name')}/{ca_log_result.get('ca_pod_namespace')}, "
                f"container={ca_log_result.get('ca_container')}, "
                f"log_signals={len(ca_log_findings)}, snippet=\"{ca_log_snippet[:200]}\""
            ),
        })
        # 将高置信度的 CA 日志信号合并到 issues
        for finding in ca_log_findings:
            _add_issue(
                issues,
                finding["code"],
                finding["title"],
                finding["severity"],
                finding["layer"],
                finding["evidence"],
                finding["recommendation"],
            )
    elif not ca_log_result.get("success", True):
        evidence.append({
            "layer": "CA-Log",
            "source": "CA Pod 日志采集",
            "summary": f"CA 日志采集失败: {ca_log_result.get('error', '未知错误')}",
        })

    evidence.append({
        "layer": "CA",
        "source": "CCE addons/nodepools",
        "summary": (
            f"ca_addon_installed={addon_info['ca_addon_installed']}, "
            f"nodepool_autoscaling_enabled={nodepool_info['nodepool_autoscaling_enabled']}, "
            f"pending_pods={len(pending)}"
        ),
    })

    # —— CA 插件状态异常检查 ——
    if addon_info["ca_addon_abnormal"]:
        abnormal_details = []
        for addon in addon_info["ca_addon_abnormal"]:
            status = addon.get("status", "?")
            name = addon.get("name", "?")
            version = addon.get("version", "?")
            abnormal_details.append(f"{name} v{version} status={status}")
        _add_issue(
            issues,
            "CA_ADDON_STATUS_ABNORMAL",
            "CA 弹性引擎插件状态异常",
            "critical",
            "CA",
            "; ".join(abnormal_details),
            "CA 插件处于非正常状态（abnormal/failed/error），无法执行扩缩容决策。优先恢复插件到正常状态：检查插件配置（尤其是容器资源 limit）、查看插件 Pod 日志和 Events，必要时升级或重建插件。",
        )

    # —— CA Pod 健康检查 ——
    ca_pod_phase = ca_log_result.get("ca_pod_phase", "")
    ca_pod_unhealthy = ca_log_result.get("ca_pod_unhealthy", [])
    if ca_log_result.get("ca_pod_found") and ca_pod_unhealthy:
        unhealthy_detail = "; ".join(
            f"{u['container']}: {u['reason']}" + (f" ({u['message'][:120]})" if u.get("message") else "")
            for u in ca_pod_unhealthy
        )
        ca_pod_is_crashing = any(
            u.get("reason") in {"CrashLoopBackOff", "Error"} or "OOM" in u.get("message", "") or "ExitCode:137" in u.get("reason", "")
            for u in ca_pod_unhealthy
        )
        severity = "critical" if ca_pod_is_crashing else "high"
        _add_issue(
            issues,
            "CA_POD_UNHEALTHY",
            f"CA 组件 Pod 健康状态异常 (phase={ca_pod_phase})",
            severity,
            "CA",
            f"Pod={ca_log_result.get('ca_pod_name')}/{ca_log_result.get('ca_pod_namespace')}, phase={ca_pod_phase}, unhealthy: {unhealthy_detail}",
            "CA Pod 处于不健康状态时无法执行扩缩容。检查容器日志中的 crash 原因、确认容器 resources.limits.memory 是否过低、查看 OOMKilled/ExitCode:137 等事件。提高 memory limit 后等待 Pod 自动恢复。",
        )
        # 补一条 evidence 记录日志来源（previous vs current）
        log_source = ca_log_result.get("log_source", "")
        if log_source == "previous":
            evidence.append({
                "layer": "CA-Log",
                "source": "CA Pod 崩溃前日志",
                "summary": f"CA Pod 当前容器未产出日志，已回退拉取 previous 容器日志 (tail={ca_log_result.get('tail_lines', '?')})",
            })

    if not addon_info["ca_addon_installed"]:
        _add_issue(
            issues,
            "CA_ADDON_NOT_INSTALLED",
            "未识别到 CCE 集群弹性引擎/Cluster Autoscaler 插件",
            "critical",
            "CA",
            "CCE addon 列表未命中 autoscaler/cluster-autoscaler 关键字。",
            "安装或恢复 CCE 集群弹性引擎插件；CCE 文档要求使用节点伸缩前安装该插件。",
        )

    if addon_info["ca_addon_low_version"]:
        versions = ", ".join(f"{item.get('name')}={item.get('version')}" for item in addon_info["ca_addon_low_version"])
        _add_issue(
            issues,
            "CA_ADDON_VERSION_LOW",
            "CCE 弹性引擎版本低于 1.13.8",
            "critical",
            "CA",
            versions,
            "升级 CCE 集群弹性引擎到 1.13.8 或以上后再验证节点伸缩。",
        )

    if not nodepool_info["nodepool_autoscaling_enabled"]:
        _add_issue(
            issues,
            "NODEPOOL_AUTOSCALING_DISABLED",
            "节点池未开启弹性伸缩",
            "critical",
            "CA",
            "nodepool/scale_group autoscaling enable 均未识别为 true。",
            "为承载业务的节点池配置 min/max 节点数和伸缩策略。",
        )

    for item in nodepool_info["max_reached"]:
        _add_issue(
            issues,
            "NODEPOOL_MAX_NODES_REACHED",
            "节点池已达到 max_nodes",
            "critical",
            "CA",
            f"{item['nodepool']}/{item['scale_group']} current={item['current_node_count']} max={item['max_node_count']}",
            "提升节点池 max_nodes，或扩展新的可调度节点池/规格。",
        )

    if direction != "scale_down":
        if not pending:
            _add_issue(
                issues,
                "CA_NO_PENDING_POD_TRIGGER",
                "未发现 Pending Pod 触发信号",
                "info",
                "CA",
                "当前范围内没有 Pending Pod；CA 扩容核心触发信号缺失。",
                "先确认 HPA 是否已增加副本并产生因资源不足无法调度的 Pod；没有 Pending 时节点不扩容通常是正常行为。",
            )
        else:
            sample = ", ".join(f"{pod.get('namespace')}/{pod.get('name')}" for pod in pending[:10])
            evidence.append({
                "layer": "CA",
                "source": "Pod/status",
                "summary": f"Pending Pod 样例: {sample}",
            })

        insufficient_events = []
        constraint_events = []
        subnet_events = []
        quota_events = []
        permission_events = []
        for event in scheduling_events:
            blob = _event_text(event)
            if any(token in blob for token in ("insufficient cpu", "insufficient memory", "insufficient pods", "insufficient ephemeral", "insufficient nvidia", "didn't have enough resource")):
                insufficient_events.append(event)
            if any(token in blob for token in ("taint", "toleration", "node affinity", "node selector", "matchnode", "affinity", "anti-affinity")):
                constraint_events.append(event)
            if any(token in blob for token in ("subnet", "available ip", "ip address", "insufficient ip", "no available ip")):
                subnet_events.append(event)
            if any(token in blob for token in ("quota", "exceeded", "insufficient quota")):
                quota_events.append(event)
            if any(token in blob for token in ("forbidden", "iam", "permission", "agency", "委托", "权限")):
                permission_events.append(event)

        if insufficient_events:
            sample = "; ".join(f"{event.get('reason')}: {event.get('message')}" for event in insufficient_events[:3])
            _add_issue(
                issues,
                "PENDING_INSUFFICIENT_RESOURCES",
                "存在资源不足导致的 Pending Pod",
                "high",
                "Scheduler",
                sample,
                "这是 CA 扩容的核心输入；若节点仍未增加，继续检查 CA 插件、节点池上限、配额和权限。",
            )
        if constraint_events:
            sample = "; ".join(f"{event.get('reason')}: {event.get('message')}" for event in constraint_events[:3])
            _add_issue(
                issues,
                "PENDING_SCHEDULING_CONSTRAINT_CONFLICT",
                "亲和性、污点或选择器约束阻断调度",
                "high",
                "Scheduler",
                sample,
                "调整 nodeSelector/nodeAffinity/tolerations/topology 约束，或确保开启伸缩的节点池满足这些标签和污点条件。",
            )
        if subnet_events:
            sample = "; ".join(f"{event.get('message')}" for event in subnet_events[:3])
            _add_issue(
                issues,
                "SUBNET_IP_EXHAUSTION_SUSPECTED",
                "事件中出现子网或 IP 不足信号",
                "high",
                "CloudResource",
                sample,
                "检查节点池使用的 VPC 子网剩余 IP，扩容子网或切换到有可用 IP 的子网。",
            )
        if quota_events:
            sample = "; ".join(f"{event.get('message')}" for event in quota_events[:3])
            _add_issue(
                issues,
                "ECS_QUOTA_SUSPECTED",
                "事件中出现配额不足信号",
                "high",
                "CloudResource",
                sample,
                "检查 ECS、磁盘、弹性 IP 或相关资源配额；必要时申请提升配额。",
            )
        if permission_events:
            sample = "; ".join(f"{event.get('message')}" for event in permission_events[:3])
            _add_issue(
                issues,
                "IAM_AGENCY_PERMISSION_SUSPECTED",
                "事件中出现 IAM/委托/权限异常信号",
                "high",
                "CloudResource",
                sample,
                "检查 CCE 委托与节点弹性引擎所需权限是否被删除或收窄。",
            )

    if direction in {"scale_down", "unknown"}:
        pods = _list(raw["pods"].get("pods"))
        safe_to_evict = [
            pod for pod in pods
            if SAFE_TO_EVICT_KEY in _list(pod.get("annotation_keys"))
        ]
        kube_system_non_ds = [
            pod for pod in pods
            if pod.get("namespace") == "kube-system" and "DaemonSet:" not in _pod_owner_blob(pod)
        ]
        standalone = [
            pod for pod in pods
            if not _list(pod.get("owner_references")) and pod.get("namespace") != "kube-system"
        ]
        if safe_to_evict:
            sample = ", ".join(f"{pod.get('namespace')}/{pod.get('name')}" for pod in safe_to_evict[:5])
            _add_issue(
                issues,
                "SCALE_DOWN_SAFE_TO_EVICT_PROTECTION",
                "Pod 设置了 safe-to-evict 保护",
                "medium",
                "CA",
                sample,
                "缩容场景需核对该 annotation 值是否为 false；当前工具能识别 key，建议补充读取 annotation value 的原子能力。",
            )
        if kube_system_non_ds:
            sample = ", ".join(f"{pod.get('namespace')}/{pod.get('name')}" for pod in kube_system_non_ds[:5])
            _add_issue(
                issues,
                "SCALE_DOWN_KUBE_SYSTEM_POD_PROTECTION",
                "kube-system 非 DaemonSet Pod 可能阻止节点缩容",
                "medium",
                "CA",
                sample,
                "确认这些系统 Pod 是否可迁移或由控制器管理；CA 默认会保护部分系统 Pod。",
            )
        if standalone:
            sample = ", ".join(f"{pod.get('namespace')}/{pod.get('name')}" for pod in standalone[:5])
            _add_issue(
                issues,
                "SCALE_DOWN_STANDALONE_POD_PROTECTION",
                "非控制器管理 Pod 可能阻止节点缩容",
                "medium",
                "CA",
                sample,
                "将裸 Pod 迁移为 Deployment/StatefulSet/Job 等控制器管理对象，或人工确认缩容影响。",
            )

    return {"issues": issues, "evidence": evidence, "pending_pods": pending, "nodepool_info": nodepool_info, "addon_info": addon_info, "ca_log_findings": ca_log_findings}


def _route(target: str, has_hpa: bool, has_ca: bool) -> str:
    if not has_hpa and not has_ca:
        return "BLOCKED"
    if target == "WORKLOAD":
        return "A"
    if target == "NODE":
        return "B"
    if has_hpa and not has_ca:
        return "A"
    if not has_hpa and has_ca:
        return "B"
    return "C"


def _issue_rank(issue: Dict[str, Any]) -> int:
    return {"critical": 0, "high": 1, "medium": 2, "info": 3}.get(issue.get("severity"), 4)


def _confidence(issues: list[Dict[str, Any]], data_gaps: list[str]) -> str:
    critical = [issue for issue in issues if issue.get("severity") == "critical"]
    high = [issue for issue in issues if issue.get("severity") == "high"]
    if critical:
        return "高 (High)"
    if high:
        return "中 (Medium)"
    if data_gaps:
        return "低 (Low)"
    return "中 (Medium)"


def _conclusion(route: str, issues: list[Dict[str, Any]]) -> str:
    blockers = [issue for issue in sorted(issues, key=_issue_rank) if issue.get("severity") in {"critical", "high"}]
    if not blockers:
        if route == "BLOCKED":
            return "集群未发现 HPA 或 CCE 弹性引擎能力，无法形成自动弹性闭环。"
        return "未发现明确阻断项；当前证据更像是扩缩容条件未触发或采集信息不足。"
    top = blockers[0]
    return f"{top['title']}：{top['evidence']}"


def _md_table(headers: list[str], rows: list[list[Any]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(_text(value).replace("\n", " ") for value in row) + " |")
    return "\n".join(lines)


def build_markdown_report(result: Dict[str, Any]) -> str:
    discovery = result["discovery"]
    intent = result["intent"]
    issues = sorted(result.get("issues", []), key=_issue_rank)
    evidence = result.get("evidence", [])
    data_gaps = result.get("data_gaps", [])
    route_name = {
        "A": "路径 A：工作负载弹性诊断",
        "B": "路径 B：节点弹性诊断",
        "C": "路径 C：双层级联诊断",
        "BLOCKED": "直接阻断",
    }.get(result.get("route"), result.get("route"))

    lines = [
        "# CCE 弹性伸缩自动化诊断报告",
        "",
        "## 1. 诊断总览",
        _md_table(
            ["项目", "结果"],
            [
                ["生成时间", result.get("generated_at")],
                ["区域/集群", f"{result.get('region')} / {result.get('cluster_id')}"],
                ["语义意图", intent.get("target")],
                ["伸缩方向", intent.get("scale_direction")],
                ["诊断路径", route_name],
                ["结论", result.get("conclusion")],
                ["置信度", result.get("confidence")],
            ],
        ),
        "",
        "## 2. 能力发现与路由",
        _md_table(
            ["能力", "发现结果", "证据"],
            [
                ["HPA", "存在" if discovery.get("has_hpa") else "未发现", f"匹配 HPA={discovery.get('selected_hpa_count')}，集群 HPA={discovery.get('hpa_count')}"],
                ["CCE 弹性引擎/CA", "存在" if discovery.get("has_ca") else "未发现", f"插件={discovery.get('ca_addon_installed')}，节点池伸缩={discovery.get('nodepool_autoscaling_enabled')}"],
                ["指标链路", "有候选插件" if discovery.get("metric_addon_detected") else "未识别", discovery.get("metric_addons") or "-"],
            ],
        ),
        "",
        "## 3. 排查过程",
    ]

    for step in result.get("process", []):
        lines.append(f"- {step}")

    lines.extend(["", "## 4. 关键证据"])
    if evidence:
        lines.append(_md_table(["层级", "来源", "证据"], [[item.get("layer"), item.get("source"), item.get("summary")] for item in evidence]))
    else:
        lines.append("未采集到可展示的关键证据。")

    lines.extend(["", "## 5. 问题与根因收敛"])
    if issues:
        lines.append(_md_table(
            ["级别", "层级", "问题", "证据", "建议"],
            [[item.get("severity"), item.get("layer"), item.get("title"), item.get("evidence"), item.get("recommendation")] for item in issues],
        ))
    else:
        lines.append("未发现明确阻断项。")

    lines.extend(["", "## 6. 下一步建议"])
    recommendations = []
    seen = set()
    for issue in issues:
        recommendation = issue.get("recommendation")
        if recommendation and recommendation not in seen:
            seen.add(recommendation)
            recommendations.append(recommendation)
    if not recommendations:
        recommendations = [
            "扩大事件和指标时间窗口，确认是否存在短暂触发后恢复的情况。",
            "若用户期望立即扩容，核对 HPA 目标值、min/maxReplicas 和节点池 max_nodes 是否符合业务峰值。",
        ]
    for recommendation in recommendations[:8]:
        lines.append(f"- {recommendation}")

    lines.extend(["", "## 7. 数据缺口"])
    if data_gaps:
        for gap in data_gaps:
            lines.append(f"- {gap}")
    else:
        lines.append("无核心采集失败。")

    return "\n".join(lines) + "\n"


def collect_autoscaling_context(
    region: str,
    cluster_id: str,
    namespace: Optional[str] = None,
    include_metrics: bool = True,
    include_ca_logs: bool = True,
    hours: int = 1,
    event_limit: int = 500,
    top_n: int = 20,
    ca_log_tail_lines: int = 200,
    ak: Optional[str] = None,
    sk: Optional[str] = None,
    project_id: Optional[str] = None,
) -> Dict[str, Dict[str, Any]]:
    raw: Dict[str, Dict[str, Any]] = {
        "hpas": cce_hpa.list_cce_hpas(region, cluster_id, ak, sk, project_id, namespace=namespace, include_system=True),
        "addons": cce.list_cce_addons(region, cluster_id, ak, sk, project_id),
        "nodepools": cce.list_cce_node_pools(region, cluster_id, ak, sk, project_id, limit=100),
        "pods": cce.get_kubernetes_pods(region, cluster_id, ak, sk, project_id, namespace=namespace),
        "events": cce.get_kubernetes_events(region, cluster_id, ak, sk, project_id, namespace=namespace, limit=event_limit),
        "deployments": cce.get_kubernetes_deployments(region, cluster_id, ak, sk, project_id, namespace=namespace),
        "statefulsets": cce.list_cce_statefulsets(region, cluster_id, namespace, 100, False, ak, sk, project_id),
    }
    if include_metrics:
        raw["pod_metrics_topn"] = cce_metrics.get_cce_pod_metrics_topN(region, cluster_id, ak, sk, project_id, top_n=top_n, hours=hours)
        raw["node_metrics_topn"] = cce_metrics.get_cce_node_metrics_topN(region, cluster_id, ak, sk, project_id, top_n=top_n, hours=hours)
    if include_ca_logs:
        raw["ca_pod_logs"] = _fetch_ca_pod_logs(region, cluster_id, ak, sk, project_id, tail_lines=ca_log_tail_lines)
    return raw


def assess_autoscaling_context(
    raw: Dict[str, Dict[str, Any]],
    region: str,
    cluster_id: str,
    question: str = "",
    target: Optional[str] = None,
    scale_direction: Optional[str] = None,
    namespace: Optional[str] = None,
    workload_name: Optional[str] = None,
    workload_type: Optional[str] = None,
    tolerance: float = 0.1,
) -> Dict[str, Any]:
    target_intent = classify_intent(question, target)
    direction = classify_scale_direction(question, scale_direction)
    addon_info = _addon_discovery(raw.get("addons", {}))
    nodepool_info = _nodepool_discovery(raw.get("nodepools", {}))
    ca_log_result = raw.get("ca_pod_logs", {})
    hpas = raw.get("hpas", {})
    selected_hpas = _select_hpas(hpas, namespace, workload_name, workload_type)
    has_hpa = bool(hpas.get("count", 0))
    has_ca = bool(addon_info["ca_addon_installed"] or nodepool_info["nodepool_autoscaling_enabled"])
    route = _route(target_intent, has_hpa, has_ca)
    workloads = _workload_rows(raw.get("deployments", {}), raw.get("statefulsets", {}))
    data_gaps = [
        gap for name, response in raw.items()
        if (gap := _collection_gap(name, response))
    ]

    process = [
        f"Gateway：基于问题文本判定 Target={target_intent}，ScaleDirection={direction}。",
        f"Discovery：HPA 总数={hpas.get('count', 0)}，匹配 HPA={len(selected_hpas)}；CA 插件={addon_info['ca_addon_installed']}，节点池伸缩={nodepool_info['nodepool_autoscaling_enabled']}。",
        f"Route：进入 {route}。",
    ]

    all_issues: list[Dict[str, Any]] = []
    all_evidence: list[Dict[str, Any]] = []

    if route == "BLOCKED":
        _add_issue(
            all_issues,
            "AUTOSCALING_CAPABILITY_ABSENT",
            "集群未配置 HPA 或 CCE 节点弹性能力",
            "critical",
            "Gateway",
            "Discovery 同时显示 Has_HPA=False 且 Has_CA=False。",
            "先配置工作负载 HPA 或安装并配置 CCE 集群弹性引擎/节点池弹性伸缩。",
        )
    else:
        hpa_result: Dict[str, Any] = {"issues": [], "evidence": [], "hpa_scaled": False}
        ca_result: Dict[str, Any] = {"issues": [], "evidence": []}

        if route in {"A", "C"}:
            process.append("路径 A：检查 HPA 是否形成 指标 -> 决策 -> 修改 replicas 的闭环。")
            hpa_result = _analyze_hpa_path(raw, selected_hpas, workloads, namespace, workload_name, workload_type, tolerance)
            all_issues.extend(hpa_result["issues"])
            all_evidence.extend(hpa_result["evidence"])

        if route == "B":
            process.append("路径 B：检查 CA 组件 Pod 日志、Pending Pod 触发信号、CA 插件、节点池上限、调度约束和云资源条件。")
            ca_result = _analyze_ca_path(raw, selected_hpas, namespace, direction)
            ca_log_count = len(ca_result.get("ca_log_findings", []))
            if ca_log_count:
                process.append(f"路径 B-CA 日志：在 CA Pod 日志中发现 {ca_log_count} 个诊断信号，优先作为根因证据。")
            all_issues.extend(ca_result["issues"])
            all_evidence.extend(ca_result["evidence"])

        if route == "C":
            pending = _pending_pods_for_scope(raw, namespace, selected_hpas)
            hpa_blockers = [issue for issue in hpa_result["issues"] if issue.get("severity") in {"critical", "high"} and issue.get("layer") == "HPA"]
            if hpa_blockers and not hpa_result.get("hpa_scaled"):
                process.append("路径 C 时序判断：HPA 未完成扩容闭环，降级收敛到路径 A。")
            elif hpa_result.get("hpa_scaled") or pending:
                process.append("路径 C 时序判断：HPA 已提高目标副本或出现新增 Pending Pod，继续进入路径 B 检查 CA。")
                ca_result = _analyze_ca_path(raw, selected_hpas, namespace, direction)
                all_issues.extend(ca_result["issues"])
                all_evidence.extend(ca_result["evidence"])
            else:
                process.append("路径 C 时序判断：未观察到 HPA 扩容后的 Pending 链路，保留 HPA 条件未触发/证据不足结论。")

    discovery = {
        "has_hpa": has_hpa,
        "hpa_count": hpas.get("count", 0),
        "selected_hpa_count": len(selected_hpas),
        "has_ca": has_ca,
        "ca_addon_installed": addon_info["ca_addon_installed"],
        "ca_addons": addon_info["ca_addons"],
        "ca_addon_low_version": addon_info["ca_addon_low_version"],
        "ca_addon_abnormal": [{"name": a.get("name"), "version": a.get("version"), "status": a.get("status")} for a in addon_info["ca_addon_abnormal"]],
        "nodepool_autoscaling_enabled": nodepool_info["nodepool_autoscaling_enabled"],
        "nodepool_max_reached": nodepool_info["max_reached"],
        "metric_addon_detected": addon_info["metric_addon_detected"],
        "metric_addons": [item.get("name") or item.get("template_name") for item in addon_info["metric_addons"]],
        "ca_pod_phase": ca_log_result.get("ca_pod_phase", ""),
        "ca_pod_unhealthy": ca_log_result.get("ca_pod_unhealthy", []),
    }
    result: Dict[str, Any] = {
        "success": True,
        "action": "huawei_autoscaling_diagnose",
        "generated_at": _now(),
        "region": region,
        "cluster_id": cluster_id,
        "intent": {"target": target_intent, "scale_direction": direction, "question": question},
        "scope": {"namespace": namespace, "workload_name": workload_name, "workload_type": workload_type},
        "route": route,
        "discovery": discovery,
        "process": process,
        "issues": sorted(all_issues, key=_issue_rank),
        "evidence": all_evidence,
        "data_gaps": data_gaps,
    }
    result["confidence"] = _confidence(result["issues"], data_gaps)
    result["conclusion"] = _conclusion(route, result["issues"])
    result["report_markdown"] = build_markdown_report(result)
    return result


def diagnose_cce_autoscaling(
    region: str,
    cluster_id: str,
    question: str = "",
    target: Optional[str] = None,
    scale_direction: Optional[str] = None,
    namespace: Optional[str] = None,
    workload_name: Optional[str] = None,
    workload_type: Optional[str] = None,
    include_metrics: bool = True,
    include_ca_logs: bool = True,
    include_raw: bool = False,
    hours: int = 1,
    event_limit: int = 500,
    top_n: int = 20,
    ca_log_tail_lines: int = 200,
    tolerance: float = 0.1,
    output_file: Optional[str] = None,
    ak: Optional[str] = None,
    sk: Optional[str] = None,
    project_id: Optional[str] = None,
) -> Dict[str, Any]:
    raw = collect_autoscaling_context(
        region=region,
        cluster_id=cluster_id,
        namespace=namespace,
        include_metrics=include_metrics,
        include_ca_logs=include_ca_logs,
        hours=hours,
        event_limit=event_limit,
        top_n=top_n,
        ca_log_tail_lines=ca_log_tail_lines,
        ak=ak,
        sk=sk,
        project_id=project_id,
    )
    result = assess_autoscaling_context(
        raw=raw,
        region=region,
        cluster_id=cluster_id,
        question=question,
        target=target,
        scale_direction=scale_direction,
        namespace=namespace,
        workload_name=workload_name,
        workload_type=workload_type,
        tolerance=tolerance,
    )
    if include_raw:
        result["raw"] = raw
    if output_file:
        path = Path(output_file)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(result["report_markdown"], encoding="utf-8")
        result["output_file"] = str(path)
    return result
