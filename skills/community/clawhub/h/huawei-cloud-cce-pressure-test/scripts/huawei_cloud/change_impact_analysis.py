"""Change impact analysis for CCE incidents.

The analyzer is read-only. It correlates CCE audit logs, Kubernetes events,
AOM alarms, and current topology snapshots to identify changes that are likely
to explain a recent incident.
"""

from __future__ import annotations

import json
import re
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

from . import aom, cce, network

try:
    from . import cce_app_logs, cce_events_lts
    LTS_HELPERS_AVAILABLE = True
except ImportError as exc:  # pragma: no cover - depends on optional SDK install
    cce_app_logs = None  # type: ignore[assignment]
    cce_events_lts = None  # type: ignore[assignment]
    LTS_HELPERS_AVAILABLE = False
    LTS_HELPERS_IMPORT_ERROR = str(exc)


CHANGE_VERBS = {"create", "update", "patch", "delete", "replace"}
WORKLOAD_RESOURCES = {"deployments", "statefulsets", "daemonsets", "replicasets", "cronjobs", "jobs"}
CONFIG_RESOURCES = {"configmaps", "secrets"}
NETWORK_RESOURCES = {
    "services",
    "ingresses",
    "gatewayclasses",
    "gateways",
    "httproutes",
    "tcproutes",
    "udproutes",
    "grpcroutes",
    "endpointslices",
}
SECURITY_RESOURCES = {
    "networkpolicies",
    "roles",
    "clusterroles",
    "rolebindings",
    "clusterrolebindings",
    "serviceaccounts",
    "podsecuritypolicies",
}
NODE_RESOURCES = {"nodes", "nodepools", "machines"}
NOISE_RESOURCES = {
    "events",
    "leases",
    "endpoints",
    "controllerrevisions",
    "tokenreviews",
    "subjectaccessreviews",
    "selfsubjectaccessreviews",
    "selfsubjectrulesreviews",
    "localsubjectaccessreviews",
    "pods/status",
    "pods/binding",
    "nodes/status",
    "serviceaccounts/token",
}
SYSTEM_CONTROLLER_MARKERS = (
    "horizontal-pod-autoscaler",
    "hpa-controller",
    "deployment-controller",
    "replicaset-controller",
    "statefulset-controller",
    "daemon-set-controller",
    "daemonset-controller",
    "endpoint-controller",
    "endpointslice-controller",
    "node-controller",
    "kube-controller-manager",
    "kube-scheduler",
    "kubelet",
)
CCE_MANAGED_RBAC_PREFIXES = (
    "system:cce:",
    "cce:",
)
CCE_PLATFORM_ACTOR_MARKERS = (
    "system:masters",
    "cceaddon",
    "cce-controller",
    "packageversion",
)
GLOBAL_CONFIG_NAMES = {
    "coredns",
    "kube-dns",
    "kube-proxy",
    "node-local-dns",
    "node-local-dns-config",
    "everest-csi-driver",
    "cceaddon-coredns",
}
HIGH_SIGNAL_FIELDS = {
    "image",
    "replicas",
    "containers",
    "initContainers",
    "env",
    "envFrom",
    "resources",
    "readinessProbe",
    "livenessProbe",
    "startupProbe",
    "ports",
    "selector",
    "rules",
    "tls",
    "backend",
    "backends",
    "data",
    "stringData",
    "taints",
    "tolerations",
    "affinity",
    "nodeSelector",
    "serviceAccountName",
    "policyTypes",
    "ingress",
    "egress",
    "roleRef",
    "subjects",
    "upstream",
    "Corefile",
}
SEMANTIC_DROP_KEYS = {
    "uid",
    "resourceVersion",
    "generation",
    "managedFields",
    "creationTimestamp",
    "deletionTimestamp",
    "selfLink",
    "annotations.kubectl.kubernetes.io/last-applied-configuration",
}


def _to_bool(value: Any, default: bool = True) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() not in {"0", "false", "no", "off"}


def _to_int(value: Any, default: int) -> int:
    try:
        return int(value) if value not in (None, "") else default
    except (TypeError, ValueError):
        return default


def _md_cell(value: Any, max_len: int = 180) -> str:
    if value is None or value == "":
        return "-"
    text = str(value).replace("\n", " ").replace("|", "\\|").strip()
    if len(text) > max_len:
        return f"{text[: max_len - 3]}..."
    return text


def _json_text(value: Any, max_len: int = 4000) -> str:
    try:
        text = json.dumps(value, ensure_ascii=False, sort_keys=True)
    except TypeError:
        text = str(value)
    if len(text) > max_len:
        return text[: max_len - 3] + "..."
    return text


def _parse_time(value: Any) -> Optional[datetime]:
    if not value:
        return None
    if isinstance(value, datetime):
        parsed = value
    else:
        text = str(value).strip()
        if not text:
            return None
        if text.endswith("Z"):
            text = text[:-1] + "+00:00"
        text = text.replace("T", " ")
        for fmt in ("%Y-%m-%d %H:%M:%S%z", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"):
            try:
                parsed = datetime.strptime(text.split(".")[0], fmt)
                break
            except ValueError:
                parsed = None  # type: ignore[assignment]
        if parsed is None:
            try:
                parsed = datetime.fromisoformat(text)
            except ValueError:
                return None
    if parsed.tzinfo:
        return parsed.astimezone(timezone.utc).replace(tzinfo=None)
    return parsed


def _format_time(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def _analysis_window(params: Dict[str, str]) -> Tuple[str, str, int]:
    hours = _to_int(params.get("hours"), 1)
    end_dt = _parse_time(params.get("end_time")) or datetime.now()
    start_dt = _parse_time(params.get("start_time")) or end_dt - timedelta(hours=hours)
    return _format_time(start_dt), _format_time(end_dt), max(1, int((end_dt - start_dt).total_seconds() // 3600) or hours)


def _nested_get(data: Dict[str, Any], path: Iterable[str]) -> Any:
    current: Any = data
    for part in path:
        if not isinstance(current, dict):
            return None
        current = current.get(part)
    return current


def _normalize_resource(resource: Any, subresource: Any = None) -> str:
    base = (str(resource or "").strip().lower()).strip("/")
    sub = str(subresource or "").strip().lower()
    if base and sub in {"status", "token"}:
        return f"{base}/{sub}"
    return base


def _event_time(event: Dict[str, Any]) -> Optional[datetime]:
    return (
        _parse_time(event.get("time"))
        or _parse_time(event.get("last_timestamp"))
        or _parse_time(event.get("event_time"))
        or _parse_time(event.get("first_timestamp"))
        or _parse_time(event.get("timestamp"))
    )


def _flatten_keys(value: Any, prefix: str = "", result: Optional[set[str]] = None) -> set[str]:
    if result is None:
        result = set()
    if isinstance(value, dict):
        for key, item in value.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            if key not in SEMANTIC_DROP_KEYS and path not in SEMANTIC_DROP_KEYS:
                result.add(str(key))
                result.add(path)
                _flatten_keys(item, path, result)
    elif isinstance(value, list):
        for item in value[:20]:
            _flatten_keys(item, prefix, result)
    return result


def _semantic_fields(event: Dict[str, Any]) -> List[str]:
    raw = event.get("raw") if isinstance(event.get("raw"), dict) else {}
    request_object = raw.get("requestObject") if isinstance(raw, dict) else None
    patch = raw.get("patch") if isinstance(raw, dict) else None
    keys = set()
    if request_object:
        keys.update(_flatten_keys(request_object))
    if patch:
        keys.update(_flatten_keys(patch))

    content = str(event.get("content") or "")
    for field in HIGH_SIGNAL_FIELDS:
        if field in keys or re.search(rf'"?{re.escape(field)}"?\s*[:=]', content):
            keys.add(field)
    return sorted(keys.intersection(HIGH_SIGNAL_FIELDS), key=str.lower)


def _is_controller_noise(event: Dict[str, Any], semantic_fields: List[str]) -> bool:
    resource = _normalize_resource(event.get("resource"), event.get("subresource"))
    verb = str(event.get("verb") or "").lower()
    actor = f"{event.get('user') or ''} {event.get('user_agent') or ''}".lower()
    name = str(event.get("name") or "").lower()
    if resource.endswith("/status"):
        return True
    if resource in NOISE_RESOURCES:
        return True
    if resource in {"clusterroles", "clusterrolebindings", "roles", "rolebindings"}:
        cce_managed = name.startswith(CCE_MANAGED_RBAC_PREFIXES)
        platform_actor = any(marker in actor for marker in CCE_PLATFORM_ACTOR_MARKERS)
        if cce_managed and platform_actor:
            return True
    if resource == "secrets" and "token" in str(event.get("name") or "").lower():
        return True
    if resource in {"replicasets", "pods"} and any(marker in actor for marker in SYSTEM_CONTROLLER_MARKERS):
        return True
    if resource in WORKLOAD_RESOURCES and any(marker in actor for marker in SYSTEM_CONTROLLER_MARKERS):
        return True
    if resource in WORKLOAD_RESOURCES and verb in {"update", "patch"}:
        hpa_like = any(marker in actor for marker in ("horizontal-pod-autoscaler", "hpa"))
        only_replicas = semantic_fields and set(semantic_fields).issubset({"replicas"})
        if hpa_like and (only_replicas or "replicas" in semantic_fields):
            return True
    return False


def _scope_match(event: Dict[str, Any], namespace: Optional[str], target_name: Optional[str]) -> str:
    namespace_match = namespace and event.get("namespace") == namespace
    name_match = target_name and target_name in str(event.get("name") or "")
    if namespace_match and name_match:
        return "target-object"
    if name_match:
        return "target-name"
    if namespace_match:
        return "target-namespace"
    return "cluster-context"


def classify_audit_event(
    event: Dict[str, Any],
    namespace: Optional[str] = None,
    target_name: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    """Convert one parsed audit event into a normalized core-change candidate."""
    verb = str(event.get("verb") or "").lower()
    resource = _normalize_resource(event.get("resource"), event.get("subresource"))
    if verb not in CHANGE_VERBS:
        return None

    semantic_fields = _semantic_fields(event)
    if _is_controller_noise(event, semantic_fields):
        return None

    ns = event.get("namespace")
    name = event.get("name")
    api_group = event.get("api_group")
    object_key = f"{ns}/{name}" if ns else str(name or "-")
    category = "other"
    title = "其他 Kubernetes 变更"
    blast_radius = "局部对象"
    base_score = 35
    reasons: List[str] = []

    if resource in WORKLOAD_RESOURCES:
        category = "workload_release"
        title = "应用发布或工作负载规格变更"
        blast_radius = "单个工作负载及其直接上下游"
        base_score = 45
        if semantic_fields:
            reasons.append(f"审计记录包含语义字段: {', '.join(semantic_fields[:8])}")
        else:
            reasons.append("工作负载对象发生写操作，但审计日志未暴露具体字段")
    elif resource in CONFIG_RESOURCES:
        category = "config_change"
        title = "配置或密钥变更"
        blast_radius = "命名空间内依赖该配置的工作负载"
        base_score = 55
        if (ns == "kube-system" and str(name).lower() in GLOBAL_CONFIG_NAMES) or str(name).lower() in GLOBAL_CONFIG_NAMES:
            category = "global_config_change"
            title = "集群基础配置变更"
            blast_radius = "全集群"
            base_score = 90
            reasons.append("命中 CoreDNS/Kube-Proxy/核心插件等全局配置名称")
        if semantic_fields:
            reasons.append(f"配置写操作包含字段: {', '.join(semantic_fields[:8])}")
    elif resource in NETWORK_RESOURCES:
        category = "network_route_change"
        title = "网络与路由变更"
        blast_radius = "入口流量或 Service 后端链路"
        base_score = 60
        if resource in {"ingresses", "gateways", "httproutes"}:
            base_score += 8
            reasons.append("入口或 Gateway 路由变更可能影响外部访问链路")
        if semantic_fields:
            reasons.append(f"网络对象字段变化: {', '.join(semantic_fields[:8])}")
    elif resource in SECURITY_RESOURCES:
        category = "security_policy_change"
        title = "安全策略或权限边界变更"
        blast_radius = "跨服务或跨命名空间安全边界"
        base_score = 75
        if resource in {"clusterroles", "clusterrolebindings"}:
            base_score += 10
            blast_radius = "集群级权限边界"
        reasons.append("安全类资源写操作需要重点关联 403、连接超时、鉴权失败")
    elif resource in NODE_RESOURCES:
        category = "node_infra_change"
        title = "节点或基础设施变更"
        blast_radius = "节点上的 Pod 与调度路径"
        base_score = 70
        if "taints" in semantic_fields or "unschedulable" in str(event.get("content") or "").lower():
            base_score += 10
            reasons.append("节点污点或调度状态变化可能导致 Pending/驱逐")

    if not reasons:
        reasons.append(f"{resource} 发生 {verb} 写操作")

    return {
        "time": event.get("time"),
        "timestamp": _event_time(event),
        "verb": verb,
        "resource": resource,
        "api_group": api_group,
        "namespace": ns,
        "name": name,
        "object_key": object_key,
        "category": category,
        "title": title,
        "actor": event.get("user"),
        "user_agent": event.get("user_agent"),
        "status_code": event.get("status_code"),
        "semantic_fields": semantic_fields,
        "blast_radius": blast_radius,
        "base_score": min(base_score, 100),
        "scope_match": _scope_match(event, namespace, target_name),
        "evidence": [
            {
                "source": "audit",
                "time": event.get("time"),
                "summary": f"{verb} {resource} {object_key}",
                "actor": event.get("user"),
                "status_code": event.get("status_code"),
                "request_uri": event.get("request_uri"),
            }
        ],
        "risk_reasons": reasons,
        "raw_event_excerpt": event.get("content"),
    }


def categorize_changes(
    audit_events: Iterable[Dict[str, Any]],
    namespace: Optional[str] = None,
    target_name: Optional[str] = None,
) -> List[Dict[str, Any]]:
    changes = []
    for event in audit_events:
        change = classify_audit_event(event, namespace=namespace, target_name=target_name)
        if change:
            changes.append(change)
    changes.sort(key=lambda item: item.get("timestamp") or datetime.min)
    return changes


def _event_text(event: Dict[str, Any]) -> str:
    involved = event.get("involved_object") or event.get("involvedObject") or {}
    if isinstance(involved, dict):
        involved_text = " ".join(str(v) for v in involved.values() if v)
    else:
        involved_text = str(involved)
    return " ".join(
        str(event.get(key) or "")
        for key in ("reason", "message", "type", "namespace", "name")
    ) + " " + involved_text


def correlate_observations(
    changes: List[Dict[str, Any]],
    k8s_events: Iterable[Dict[str, Any]],
    alarms: Iterable[Dict[str, Any]],
    incident_time: Optional[datetime],
    correlation_window_minutes: int,
) -> None:
    window = timedelta(minutes=max(1, correlation_window_minutes))
    parsed_events = [(event, _event_time(event), _event_text(event).lower()) for event in k8s_events]
    parsed_alarms = [(alarm, _event_time(alarm), _json_text(alarm, 1200).lower()) for alarm in alarms]

    for change in changes:
        change_time = change.get("timestamp")
        if incident_time and change_time:
            delta = abs((incident_time - change_time).total_seconds()) / 60
            if delta <= correlation_window_minutes:
                change.setdefault("risk_reasons", []).append(f"距离故障时间约 {int(delta)} 分钟")
                change["time_proximity_score"] = max(0, 15 - int(delta / 2))
        matched = []
        terms = [str(change.get("name") or "").lower(), str(change.get("namespace") or "").lower(), change.get("resource")]
        terms = [term for term in terms if term and term != "none"]
        for event, event_time, text in parsed_events:
            if change_time and event_time and event_time < change_time:
                continue
            if change_time and event_time and event_time - change_time > window:
                continue
            if terms and any(term in text for term in terms):
                matched.append(
                    {
                        "source": "k8s_event",
                        "time": event.get("last_timestamp") or event.get("event_time") or event.get("first_timestamp"),
                        "summary": f"{event.get('reason') or '-'}: {event.get('message') or '-'}",
                    }
                )
        alarm_matches = []
        for alarm, alarm_time, text in parsed_alarms:
            if change_time and alarm_time and alarm_time < change_time:
                continue
            if change_time and alarm_time and alarm_time - change_time > window:
                continue
            if terms and any(term in text for term in terms):
                alarm_matches.append(
                    {
                        "source": "aom_alarm",
                        "time": alarm.get("time") or alarm.get("starts_at") or alarm.get("last_alarm_time"),
                        "summary": alarm.get("alarm_name") or alarm.get("name") or alarm.get("event_name") or _json_text(alarm, 160),
                    }
                )
        if matched:
            change.setdefault("evidence", []).extend(matched[:5])
            change.setdefault("risk_reasons", []).append(f"变更后 {correlation_window_minutes} 分钟内出现相关 Kubernetes 事件")
            change["event_correlation_score"] = min(10, len(matched) * 3)
        if alarm_matches:
            change.setdefault("evidence", []).extend(alarm_matches[:5])
            change.setdefault("risk_reasons", []).append(f"变更后 {correlation_window_minutes} 分钟内出现相关 AOM 告警")
            change["alarm_correlation_score"] = min(12, len(alarm_matches) * 4)


def _labels_match(selector: Dict[str, Any], labels: Dict[str, Any]) -> bool:
    if not selector:
        return False
    labels = labels or {}
    return all(str(labels.get(key)) == str(value) for key, value in selector.items())


def assemble_blast_radius(changes: List[Dict[str, Any]], snapshots: Dict[str, Any]) -> None:
    pods = snapshots.get("pods") or []
    services = snapshots.get("services") or []
    ingresses = snapshots.get("ingresses") or []
    nodes = snapshots.get("nodes") or []

    for change in changes:
        resource = change.get("resource")
        namespace = change.get("namespace")
        name = change.get("name")
        impacted: Dict[str, Any] = {"pods": [], "services": [], "ingresses": [], "nodes": []}

        if resource == "services":
            service = next((svc for svc in services if svc.get("namespace") == namespace and svc.get("name") == name), None)
            if service:
                selector = service.get("selector") or {}
                impacted["services"].append(f"{namespace}/{name}")
                impacted["pods"] = [
                    f"{pod.get('namespace')}/{pod.get('name')}"
                    for pod in pods
                    if pod.get("namespace") == namespace and _labels_match(selector, pod.get("labels") or {})
                ][:20]
                impacted["ingresses"] = _ingresses_for_service(ingresses, namespace, name)[:20]
        elif resource == "ingresses":
            ingress = next((item for item in ingresses if item.get("namespace") == namespace and item.get("name") == name), None)
            if ingress:
                impacted["ingresses"].append(f"{namespace}/{name}")
                impacted["services"] = _services_for_ingress(ingress)[:20]
        elif resource == "nodes":
            impacted["nodes"].append(str(name))
            impacted["pods"] = [
                f"{pod.get('namespace')}/{pod.get('name')}"
                for pod in pods
                if pod.get("node") == name or pod.get("host_ip") == name or pod.get("node_name") == name
            ][:30]
        elif resource in WORKLOAD_RESOURCES:
            impacted["pods"] = [
                f"{pod.get('namespace')}/{pod.get('name')}"
                for pod in pods
                if pod.get("namespace") == namespace and str(name or "") in str(pod.get("name") or "")
            ][:20]
            impacted["services"] = [
                f"{svc.get('namespace')}/{svc.get('name')}"
                for svc in services
                if svc.get("namespace") == namespace and _service_selects_any_pod(svc, pods, namespace, name)
            ][:20]
        elif resource in CONFIG_RESOURCES:
            if change.get("category") == "global_config_change":
                impacted["nodes"] = [node.get("name") or node.get("internal_ip") for node in nodes[:50]]
                impacted["services"] = ["kube-system/kube-dns", "cluster DNS path"]
            else:
                impacted["pods"] = [
                    f"{pod.get('namespace')}/{pod.get('name')}"
                    for pod in pods
                    if pod.get("namespace") == namespace
                ][:20]

        impacted = {key: [item for item in value if item] for key, value in impacted.items()}
        change["impacted_entities"] = impacted
        entity_count = sum(len(value) for value in impacted.values())
        if entity_count >= 20:
            change["blast_radius_score"] = 12
            change.setdefault("risk_reasons", []).append(f"当前拓扑显示至少 {entity_count} 个实体可能受影响")
        elif entity_count >= 5:
            change["blast_radius_score"] = 7
            change.setdefault("risk_reasons", []).append(f"当前拓扑显示 {entity_count} 个实体可能受影响")
        elif entity_count > 0:
            change["blast_radius_score"] = 3


def _ingresses_for_service(ingresses: List[Dict[str, Any]], namespace: Optional[str], service_name: Optional[str]) -> List[str]:
    result = []
    for ingress in ingresses:
        if ingress.get("namespace") != namespace:
            continue
        for svc_key in _services_for_ingress(ingress):
            if svc_key == f"{namespace}/{service_name}":
                result.append(f"{namespace}/{ingress.get('name')}")
                break
    return result


def _services_for_ingress(ingress: Dict[str, Any]) -> List[str]:
    namespace = ingress.get("namespace")
    result = []
    for rule in ingress.get("rules") or []:
        for path in rule.get("paths") or []:
            backend = path.get("backend") or {}
            service_name = backend.get("service_name") or path.get("service_name")
            if service_name:
                result.append(f"{namespace}/{service_name}")
    if ingress.get("default_backend", {}).get("service_name"):
        result.append(f"{namespace}/{ingress['default_backend']['service_name']}")
    return sorted(set(result))


def _service_selects_any_pod(
    service: Dict[str, Any],
    pods: List[Dict[str, Any]],
    namespace: Optional[str],
    workload_name: Optional[str],
) -> bool:
    selector = service.get("selector") or {}
    if not selector:
        return False
    for pod in pods:
        if pod.get("namespace") != namespace or str(workload_name or "") not in str(pod.get("name") or ""):
            continue
        if _labels_match(selector, pod.get("labels") or {}):
            return True
    return False


def score_changes(changes: List[Dict[str, Any]]) -> None:
    for change in changes:
        score = int(change.get("base_score") or 0)
        score += int(change.get("time_proximity_score") or 0)
        score += int(change.get("event_correlation_score") or 0)
        score += int(change.get("alarm_correlation_score") or 0)
        score += int(change.get("blast_radius_score") or 0)
        if change.get("scope_match") == "target-object":
            score += 8
        elif change.get("scope_match") == "target-namespace":
            score += 4
        change["risk_score"] = min(score, 100)
        if score >= 85:
            change["risk_level"] = "Critical"
            change["confidence"] = "high" if len(change.get("evidence", [])) >= 2 else "medium"
        elif score >= 70:
            change["risk_level"] = "High"
            change["confidence"] = "medium"
        elif score >= 50:
            change["risk_level"] = "Medium"
            change["confidence"] = "medium"
        else:
            change["risk_level"] = "Low"
            change["confidence"] = "low"


def _public_change(change: Dict[str, Any]) -> Dict[str, Any]:
    result = dict(change)
    timestamp = result.get("timestamp")
    if isinstance(timestamp, datetime):
        result["timestamp"] = _format_time(timestamp)
    return result


def _safe_capture(label: str, collector: Callable[[], Dict[str, Any]]) -> Dict[str, Any]:
    try:
        result = collector()
        if not isinstance(result, dict):
            return {"success": True, "result": result}
        return result
    except Exception as exc:  # pragma: no cover - defensive cloud boundary
        return {"success": False, "stage": label, "error": str(exc), "error_type": type(exc).__name__}


def _collect_snapshots(params: Dict[str, str]) -> Dict[str, Any]:
    region = params["region"]
    cluster_id = params["cluster_id"]
    namespace = params.get("namespace")
    ak = params.get("ak")
    sk = params.get("sk")
    project_id = params.get("project_id")
    limit = _to_int(params.get("snapshot_limit"), 200)

    raw: Dict[str, Dict[str, Any]] = {}
    raw["pods"] = _safe_capture(
        "pods",
        lambda: cce.get_kubernetes_pods(region, cluster_id, ak, sk, project_id, namespace),
    )
    raw["services"] = _safe_capture(
        "services",
        lambda: cce.get_kubernetes_services(region, cluster_id, ak, sk, project_id, namespace),
    )
    raw["ingresses"] = _safe_capture(
        "ingresses",
        lambda: cce.get_kubernetes_ingresses(region, cluster_id, ak, sk, project_id, namespace),
    )
    raw["nodes"] = _safe_capture(
        "nodes",
        lambda: cce.get_kubernetes_nodes(region, cluster_id, ak, sk, project_id),
    )
    raw["configmaps"] = _safe_capture(
        "configmaps",
        lambda: cce.list_cce_configmaps(region, cluster_id, namespace, limit, 0, False, ak, sk, project_id),
    )
    raw["secrets"] = _safe_capture(
        "secrets",
        lambda: cce.list_cce_secrets(region, cluster_id, namespace, limit, False, ak, sk, project_id),
    )
    raw["nodepools"] = _safe_capture(
        "nodepools",
        lambda: cce.list_cce_node_pools(region, cluster_id, ak, sk, project_id, limit, 0),
    )
    raw["security_groups"] = _safe_capture(
        "security_groups",
        lambda: network.list_security_groups(region, params.get("vpc_id"), ak, sk, project_id, limit, 0),
    )
    raw["vpc_acls"] = _safe_capture(
        "vpc_acls",
        lambda: network.list_vpc_acls(region, params.get("vpc_id"), ak, sk, project_id),
    )

    return {
        "raw": raw,
        "pods": raw["pods"].get("pods", []) if raw["pods"].get("success") else [],
        "services": raw["services"].get("services", []) if raw["services"].get("success") else [],
        "ingresses": raw["ingresses"].get("ingresses", []) if raw["ingresses"].get("success") else [],
        "nodes": raw["nodes"].get("nodes", []) if raw["nodes"].get("success") else [],
        "configmaps": raw["configmaps"].get("configmaps", []) if raw["configmaps"].get("success") else [],
        "secrets": raw["secrets"].get("secrets", []) if raw["secrets"].get("success") else [],
        "nodepools": raw["nodepools"].get("nodepools", []) if raw["nodepools"].get("success") else [],
        "security_groups": raw["security_groups"].get("security_groups", []) if raw["security_groups"].get("success") else [],
        "vpc_acls": raw["vpc_acls"].get("acls", []) if raw["vpc_acls"].get("success") else [],
    }


def collect_shadow_captures(params: Dict[str, str], start_time: str, end_time: str, hours: int) -> Dict[str, Any]:
    captures: Dict[str, Any] = {"audit": {}, "k8s_events_lts": {}, "aom": {}, "snapshots": {}}
    if _to_bool(params.get("include_audit"), True):
        if not LTS_HELPERS_AVAILABLE or cce_app_logs is None:
            captures["audit"] = {
                "success": False,
                "error": f"LTS helpers unavailable: {globals().get('LTS_HELPERS_IMPORT_ERROR', 'unknown')}",
            }
        else:
            audit_params = {
                "region": params["region"],
                "cluster_id": params["cluster_id"],
                "start_time": start_time,
                "end_time": end_time,
                "limit": str(_to_int(params.get("audit_page_limit"), 500)),
                "max_pages": str(_to_int(params.get("audit_max_pages"), 5)),
                "sample_limit": str(_to_int(params.get("audit_sample_limit"), 500)),
                "auto_paginate": "true",
            }
            for key in (
                "ak",
                "sk",
                "project_id",
                "log_group_id",
                "log_stream_id",
                "log_group_name",
                "log_stream_name",
                "audit_stream_keywords",
            ):
                if params.get(key):
                    audit_params[key] = params[key]
            captures["audit"] = _safe_capture(
                "audit",
                lambda: cce_app_logs.query_cce_audit_logs_action(audit_params),  # type: ignore[union-attr]
            )

    if _to_bool(params.get("include_k8s_events"), True):
        if not LTS_HELPERS_AVAILABLE or cce_events_lts is None:
            captures["k8s_events_lts"] = {
                "success": False,
                "error": f"LTS helpers unavailable: {globals().get('LTS_HELPERS_IMPORT_ERROR', 'unknown')}",
            }
        else:
            event_params = {
                "region": params["region"],
                "cluster_id": params["cluster_id"],
                "start_time": start_time,
                "end_time": end_time,
                "limit": str(_to_int(params.get("event_limit"), 500)),
            }
            for key in ("ak", "sk", "project_id", "event_keywords", "keywords"):
                if params.get(key):
                    event_params["keywords" if key == "event_keywords" else key] = params[key]
            captures["k8s_events_lts"] = _safe_capture(
                "k8s_events_lts",
                lambda: cce_events_lts.query_k8s_events_from_lts_action(event_params),  # type: ignore[union-attr]
            )

    if _to_bool(params.get("include_aom"), True):
        captures["aom"] = _safe_capture(
            "aom",
            lambda: aom.analyze_aom_alarms(
                region=params["region"],
                ak=params.get("ak"),
                sk=params.get("sk"),
                project_id=params.get("project_id"),
                cluster_id=params.get("cluster_id"),
                cluster_name=params.get("cluster_name"),
                hours=hours,
                chronic_threshold=_to_int(params.get("chronic_threshold"), 5),
                sudden_window_minutes=_to_int(params.get("sudden_window_minutes"), 10),
            ),
        )

    if _to_bool(params.get("include_snapshots"), True):
        captures["snapshots"] = _collect_snapshots(params)
    return captures


def _alarms_from_capture(aom_capture: Dict[str, Any]) -> List[Dict[str, Any]]:
    if not aom_capture.get("success"):
        return []
    alarms: List[Dict[str, Any]] = []
    for key in ("sudden_alarms", "focus_alarms", "chronic_alarms", "alarms", "items"):
        value = aom_capture.get(key)
        if isinstance(value, list):
            alarms.extend([item for item in value if isinstance(item, dict)])
    summary = aom_capture.get("summary")
    if isinstance(summary, dict):
        for value in summary.values():
            if isinstance(value, list):
                alarms.extend([item for item in value if isinstance(item, dict)])
    return alarms


def _capture_status_rows(captures: Dict[str, Any]) -> List[Tuple[str, str, str]]:
    rows = []
    audit = captures.get("audit") or {}
    rows.append(("CCE 审计日志", "成功" if audit.get("success") else "失败/未启用", audit.get("error") or f"匹配 {audit.get('summary', {}).get('matched_events', 0)} 条"))
    events = captures.get("k8s_events_lts") or {}
    rows.append(("K8s 历史事件", "成功" if events.get("success") else "失败/未启用", events.get("error") or f"获取 {events.get('event_count', 0)} 条"))
    aom_capture = captures.get("aom") or {}
    rows.append(("AOM 告警", "成功" if aom_capture.get("success") else "失败/未启用", aom_capture.get("error") or "active + history 关联分析"))
    snapshots = captures.get("snapshots") or {}
    raw = snapshots.get("raw") or {}
    success_count = len([item for item in raw.values() if isinstance(item, dict) and item.get("success")])
    rows.append(("当前资源快照", "成功" if success_count else "失败/未采集", f"{success_count}/{len(raw)} 类资源可用" if raw else "未请求"))
    return rows


def _timeline_table(changes: List[Dict[str, Any]]) -> str:
    if not changes:
        return "未在采集窗口中识别到核心变更。"
    lines = [
        "| 时间 | 风险 | 类别 | 操作 | 对象 | 执行者 | 核心语义 |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for change in changes:
        lines.append(
            "| {time} | {risk} | {category} | {verb} | {object_key} | {actor} | {fields} |".format(
                time=_md_cell(change.get("time")),
                risk=_md_cell(f"{change.get('risk_level')}({change.get('risk_score')})"),
                category=_md_cell(change.get("title")),
                verb=_md_cell(change.get("verb")),
                object_key=_md_cell(change.get("object_key")),
                actor=_md_cell(change.get("actor")),
                fields=_md_cell(", ".join(change.get("semantic_fields") or []) or "写操作"),
            )
        )
    return "\n".join(lines)


def _top_risks(changes: List[Dict[str, Any]], top_n: int) -> str:
    if not changes:
        return "- 暂未发现可解释当前故障的核心变更。"
    lines = []
    for index, change in enumerate(sorted(changes, key=lambda item: item.get("risk_score", 0), reverse=True)[:top_n], start=1):
        reasons = "；".join(change.get("risk_reasons") or []) or "缺少进一步证据"
        evidence_count = len(change.get("evidence") or [])
        lines.append(
            f"{index}. **{change.get('risk_level')} {change.get('object_key')}**：{change.get('title')}，"
            f"评分 {change.get('risk_score')}/100，置信度 {change.get('confidence')}。"
            f"依据：{reasons}。证据数：{evidence_count}。"
        )
    return "\n".join(lines)


def _blast_radius_section(changes: List[Dict[str, Any]], top_n: int) -> str:
    lines = []
    for change in sorted(changes, key=lambda item: item.get("risk_score", 0), reverse=True)[:top_n]:
        impacted = change.get("impacted_entities") or {}
        pieces = []
        for key in ("pods", "services", "ingresses", "nodes"):
            values = impacted.get(key) or []
            if values:
                pieces.append(f"{key}: {', '.join(str(item) for item in values[:8])}")
        if not pieces:
            pieces.append(change.get("blast_radius") or "影响面需要结合当前拓扑继续确认")
        lines.append(f"- **{change.get('object_key')}**：{'；'.join(pieces)}")
    return "\n".join(lines) if lines else "- 无可建模的变更影响面。"


def _evidence_matrix(changes: List[Dict[str, Any]], top_n: int) -> str:
    lines = [
        "| 变更对象 | 来源 | 时间 | 证据摘要 |",
        "| --- | --- | --- | --- |",
    ]
    has_row = False
    for change in sorted(changes, key=lambda item: item.get("risk_score", 0), reverse=True)[:top_n]:
        for evidence in change.get("evidence") or []:
            has_row = True
            lines.append(
                f"| {_md_cell(change.get('object_key'))} | {_md_cell(evidence.get('source'))} | "
                f"{_md_cell(evidence.get('time'))} | {_md_cell(evidence.get('summary'), 260)} |"
            )
    return "\n".join(lines) if has_row else "证据不足：未能从审计、事件或告警中获得可展示证据。"


def _reusable_capabilities_section() -> str:
    return "\n".join(
        [
            "- 已复用 `huawei_query_cce_audit_logs` 获取 Kubernetes 审计变更影子。",
            "- 已复用 `huawei_query_k8s_events_from_lts` 获取历史 Kubernetes 事件。",
            "- 已复用 `huawei_analyze_aom_alarms` 做 active + history 告警关联。",
            "- 已复用 CCE 资源查询：Pod、Service、Ingress、Node、ConfigMap、Secret、NodePool。",
            "- 已复用 VPC 只读查询：Security Group、VPC ACL 当前快照。",
        ]
    )


def _gap_section(captures: Dict[str, Any]) -> str:
    gaps = []
    if not (captures.get("audit") or {}).get("success"):
        gaps.append("审计日志不可用时，只能基于当前资源快照和事件推断，无法可靠还原变更执行人和变更时间。")
    if not (captures.get("k8s_events_lts") or {}).get("success"):
        gaps.append("Kubernetes 事件未进入 LTS 时，历史事件窗口不完整，只能查实时 Events。")
    gaps.extend(
        [
            "当前仓库尚无 CTS/云审计原子能力，无法直接还原 CCE 集群升级、节点池扩缩容、ELB/安全组/ACL 的历史变更人和时间。",
            "审计日志若未记录 requestObject/patch，只能识别对象级写操作，无法完成严格的 before/after YAML diff。",
            "Gateway API、RBAC、NetworkPolicy 的当前拓扑查询可继续补独立原子工具，提升影响面建模精度。",
        ]
    )
    return "\n".join(f"- {gap}" for gap in gaps)


def build_markdown_report(
    trace_id: str,
    params: Dict[str, str],
    start_time: str,
    end_time: str,
    captures: Dict[str, Any],
    changes: List[Dict[str, Any]],
    top_n: int,
) -> str:
    status_lines = [
        "| 数据源 | 状态 | 说明 |",
        "| --- | --- | --- |",
        *[f"| {_md_cell(source)} | {_md_cell(status)} | {_md_cell(note, 260)} |" for source, status, note in _capture_status_rows(captures)],
    ]
    highest = sorted(changes, key=lambda item: item.get("risk_score", 0), reverse=True)[:1]
    conclusion = (
        f"最高疑似诱因是 `{highest[0].get('object_key')}` 的 {highest[0].get('title')}，"
        f"风险等级 {highest[0].get('risk_level')}，评分 {highest[0].get('risk_score')}/100。"
        if highest
        else "本窗口内没有识别到足以解释故障的核心变更，建议扩大时间窗口或补齐审计/CTS 数据。"
    )
    target = params.get("target_name") or params.get("workload_name") or params.get("app_name") or "未指定"

    return "\n".join(
        [
            "# CCE 变更影响分析报告",
            "",
            "## 1. 分析摘要",
            "",
            f"- Analysis-Trace-ID: `{trace_id}`",
            f"- 集群: `{params.get('cluster_id')}`",
            f"- 区域: `{params.get('region')}`",
            f"- 范围: `{params.get('namespace') or '全集群'}`",
            f"- 目标对象: `{target}`",
            f"- 分析窗口: `{start_time}` 至 `{end_time}`",
            f"- 识别核心变更: `{len(changes)}` 条",
            f"- 初步结论: {conclusion}",
            "",
            "## 2. 排查过程",
            "",
            "1. 范围定义与数据总线：初始化 Trace ID，并并行收集应用配置、网络路由、安全策略、基础设施四类变更影子。",
            "2. 核心识别与噪声消除：剥离 HPA/控制器写入、Token/Lease/Status 等常规噪声，保留镜像、配置、路由、权限、污点等核心语义字段。",
            "3. 爆炸半径与风险推演：将核心变更映射到当前 Pod、Service、Ingress、Node 拓扑，模拟可能的传播路径。",
            "4. 风险综合与评级报告：按变更敏感度、拓扑波及范围、安全边界跨度、故障时间邻近度、事件/告警相关性评分。",
            "",
            "## 3. 数据源与采集状态",
            "",
            "\n".join(status_lines),
            "",
            "## 4. 核心变更时间线",
            "",
            _timeline_table(changes),
            "",
            "## 5. 最高风险预警",
            "",
            _top_risks(changes, top_n),
            "",
            "## 6. 爆炸半径与传播路径",
            "",
            _blast_radius_section(changes, top_n),
            "",
            "## 7. 证据矩阵",
            "",
            _evidence_matrix(changes, top_n),
            "",
            "## 8. 结论与验证建议",
            "",
            f"- 结论: {conclusion}",
            "- 验证建议: 对 Top 风险对象回看发布单/配置审计，执行只读连通性、日志、事件和指标复核；需要回滚或修复时转交恢复流程并先生成预览。",
            "- 置信度说明: 高置信度需要同时满足审计变更、故障时间邻近、事件或告警响应、拓扑影响面可解释四类证据。",
            "",
            "## 9. 已复用能力",
            "",
            _reusable_capabilities_section(),
            "",
            "## 10. 能力缺口与补强建议",
            "",
            _gap_section(captures),
            "",
        ]
    )


def analyze_change_impact(params: Dict[str, str]) -> Dict[str, Any]:
    missing = [key for key in ("region", "cluster_id") if not params.get(key)]
    if missing:
        return {"success": False, "error": f"{', '.join(missing)} is required"}

    start_time, end_time, hours = _analysis_window(params)
    trace_id = params.get("analysis_trace_id") or f"CIA-{datetime.now().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:8]}"
    top_n = _to_int(params.get("top_n"), 3)
    target_name = params.get("target_name") or params.get("workload_name") or params.get("app_name")
    incident_time = _parse_time(params.get("fault_time") or params.get("incident_time"))
    correlation_window = _to_int(params.get("correlation_window_minutes"), 30)

    captures = collect_shadow_captures(params, start_time, end_time, hours)
    audit_events = (captures.get("audit") or {}).get("events") or []
    changes = categorize_changes(audit_events, namespace=params.get("namespace"), target_name=target_name)

    k8s_events = (captures.get("k8s_events_lts") or {}).get("events") or []
    alarms = _alarms_from_capture(captures.get("aom") or {})
    correlate_observations(changes, k8s_events, alarms, incident_time, correlation_window)

    snapshots = captures.get("snapshots") or {}
    if snapshots:
        assemble_blast_radius(changes, snapshots)
    score_changes(changes)
    changes.sort(key=lambda item: (item.get("risk_score", 0), item.get("timestamp") or datetime.min), reverse=True)

    report_markdown = build_markdown_report(trace_id, params, start_time, end_time, captures, changes, top_n)
    public_changes = [_public_change(change) for change in changes]
    output_file = params.get("output_file")
    if output_file:
        Path(output_file).write_text(report_markdown, encoding="utf-8")

    return {
        "success": True,
        "analysis_trace_id": trace_id,
        "analysis_window": {"start_time": start_time, "end_time": end_time, "hours": hours},
        "scope": {
            "region": params.get("region"),
            "cluster_id": params.get("cluster_id"),
            "namespace": params.get("namespace"),
            "target_name": target_name,
        },
        "summary": {
            "core_change_count": len(changes),
            "top_risk_count": min(top_n, len(changes)),
            "data_sources": {source: status for source, status, _ in _capture_status_rows(captures)},
        },
        "top_changes": public_changes[:top_n],
        "changes": public_changes,
        "report_markdown": report_markdown,
        "report_file": output_file,
        "capture_metadata": {
            "audit": {
                "success": (captures.get("audit") or {}).get("success"),
                "summary": (captures.get("audit") or {}).get("summary"),
                "stream_match_type": (captures.get("audit") or {}).get("stream_match_type"),
            },
            "k8s_events_lts": {
                "success": (captures.get("k8s_events_lts") or {}).get("success"),
                "event_count": (captures.get("k8s_events_lts") or {}).get("event_count"),
            },
            "aom": {
                "success": (captures.get("aom") or {}).get("success"),
            },
        },
    }


def analyze_change_impact_action(params: Dict[str, str]) -> Dict[str, Any]:
    return analyze_change_impact(params)
