"""Node failure diagnosis with Kubernetes evidence and Markdown reporting."""

from __future__ import annotations

from collections import Counter, defaultdict
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional

from . import cce_metrics
from .cce import _k8s_container_status, _k8s_owner_references, _k8s_pod_conditions
from .cce_k8s import _setup_k8s_client
from .common import (
    IMPORT_ERROR,
    K8S_AVAILABLE,
    K8S_IMPORT_ERROR,
    SDK_AVAILABLE,
    _safe_delete_file,
    get_credentials,
    k8s_client,
)


LEASE_NAMESPACE = "kube-node-lease"
DEFAULT_LEASE_TIMEOUT_SECONDS = 40
CORE_DAEMON_KEYWORDS = (
    "kube-proxy",
    "coredns",
    "everest-csi",
    "cce-pause",
    "cilium",
    "eni",
    "canal",
    "flannel",
    "calico",
    "network",
)
CNI_ERROR_PATTERNS = (
    "failedcreatepodsandbox",
    "network plugin",
    "cni",
    "pod sandbox",
    "setup network",
    "timeout waiting for dhcp",
    "failed to create pod sandbox",
    "failed to setup network",
)
DISK_PATTERNS = ("diskpressure", "imagefs", "nodefs", "ephemeral-storage", "no space left")
MEMORY_PATTERNS = ("memorypressure", "systemoom", "oomkilled", "out of memory")
KUBELET_PATTERNS = ("kubeletsetupfailed", "containerruntimenotready", "runtime not ready", "pleg")


def _as_bool(value: Any, default: bool = True) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() not in {"0", "false", "no", "off"}


def _to_int(value: Any, default: int) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _k8s_ts(value: Any) -> Optional[str]:
    return str(value) if value else None


def _parse_dt(value: Any) -> Optional[datetime]:
    if not value:
        return None
    if isinstance(value, datetime):
        parsed = value
    else:
        text = str(value).strip()
        if text.endswith("Z"):
            text = f"{text[:-1]}+00:00"
        try:
            parsed = datetime.fromisoformat(text)
        except ValueError:
            return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _md_cell(value: Any, max_len: int = 180) -> str:
    if value is None or value == "":
        return "-"
    text = str(value).replace("\n", " ").replace("|", "\\|").strip()
    if len(text) > max_len:
        return f"{text[: max_len - 3]}..."
    return text


def _condition_to_dict(condition: Any) -> Dict[str, Any]:
    return {
        "type": getattr(condition, "type", None),
        "status": getattr(condition, "status", None),
        "reason": getattr(condition, "reason", None),
        "message": getattr(condition, "message", None),
        "last_heartbeat_time": _k8s_ts(getattr(condition, "last_heartbeat_time", None)),
        "last_transition_time": _k8s_ts(getattr(condition, "last_transition_time", None)),
    }


def _node_to_dict(node: Any) -> Dict[str, Any]:
    addresses = []
    internal_ip = None
    hostname = None
    for address in getattr(getattr(node, "status", None), "addresses", None) or []:
        item = {"type": getattr(address, "type", None), "address": getattr(address, "address", None)}
        addresses.append(item)
        if item["type"] == "InternalIP":
            internal_ip = item["address"]
        elif item["type"] == "Hostname":
            hostname = item["address"]

    conditions = [_condition_to_dict(cond) for cond in getattr(getattr(node, "status", None), "conditions", None) or []]
    condition_map = {cond.get("type"): cond for cond in conditions}
    ready = condition_map.get("Ready", {}).get("status", "Unknown")

    taints = []
    for taint in getattr(getattr(node, "spec", None), "taints", None) or []:
        taints.append({
            "key": getattr(taint, "key", None),
            "value": getattr(taint, "value", None),
            "effect": getattr(taint, "effect", None),
        })

    return {
        "name": getattr(getattr(node, "metadata", None), "name", None),
        "uid": getattr(getattr(node, "metadata", None), "uid", None),
        "created": _k8s_ts(getattr(getattr(node, "metadata", None), "creation_timestamp", None)),
        "labels": getattr(getattr(node, "metadata", None), "labels", None) or {},
        "addresses": addresses,
        "internal_ip": internal_ip,
        "hostname": hostname,
        "ready": ready,
        "conditions": conditions,
        "capacity": dict(getattr(getattr(node, "status", None), "capacity", None) or {}),
        "allocatable": dict(getattr(getattr(node, "status", None), "allocatable", None) or {}),
        "taints": taints,
    }


def _pod_to_dict(pod: Any) -> Dict[str, Any]:
    spec_containers = {c.name: c for c in (getattr(getattr(pod, "spec", None), "containers", None) or [])}
    init_spec_containers = {
        c.name: c for c in (getattr(getattr(pod, "spec", None), "init_containers", None) or [])
    }
    container_statuses = getattr(getattr(pod, "status", None), "container_statuses", None) or []
    init_statuses = getattr(getattr(pod, "status", None), "init_container_statuses", None) or []

    return {
        "name": getattr(getattr(pod, "metadata", None), "name", None),
        "namespace": getattr(getattr(pod, "metadata", None), "namespace", None),
        "phase": getattr(getattr(pod, "status", None), "phase", None),
        "status": getattr(getattr(pod, "status", None), "phase", None),
        "reason": getattr(getattr(pod, "status", None), "reason", None),
        "message": getattr(getattr(pod, "status", None), "message", None),
        "node": getattr(getattr(pod, "spec", None), "node_name", None),
        "pod_ip": getattr(getattr(pod, "status", None), "pod_ip", None),
        "host_ip": getattr(getattr(pod, "status", None), "host_ip", None),
        "created": _k8s_ts(getattr(getattr(pod, "metadata", None), "creation_timestamp", None)),
        "labels": getattr(getattr(pod, "metadata", None), "labels", None) or {},
        "owner_references": _k8s_owner_references(getattr(getattr(pod, "metadata", None), "owner_references", None)),
        "conditions": _k8s_pod_conditions(getattr(getattr(pod, "status", None), "conditions", None)),
        "containers": [_k8s_container_status(cs, spec_containers) for cs in container_statuses],
        "init_containers": [_k8s_container_status(cs, init_spec_containers) for cs in init_statuses],
    }


def _event_to_dict(event: Any) -> Dict[str, Any]:
    involved = getattr(event, "involved_object", None)
    source = getattr(event, "source", None)
    return {
        "name": getattr(getattr(event, "metadata", None), "name", None),
        "namespace": getattr(getattr(event, "metadata", None), "namespace", None),
        "type": getattr(event, "type", None),
        "reason": getattr(event, "reason", None),
        "message": getattr(event, "message", None),
        "source": getattr(source, "component", None) or getattr(event, "reporting_component", None),
        "first_timestamp": _k8s_ts(getattr(event, "first_timestamp", None)),
        "last_timestamp": _k8s_ts(getattr(event, "last_timestamp", None)),
        "event_time": _k8s_ts(getattr(event, "event_time", None)),
        "count": getattr(event, "count", None) or 1,
        "involved_object": {
            "kind": getattr(involved, "kind", None),
            "name": getattr(involved, "name", None),
            "namespace": getattr(involved, "namespace", None),
        } if involved else {},
    }


def _event_sort_key(event: Dict[str, Any]) -> datetime:
    return (
        _parse_dt(event.get("last_timestamp"))
        or _parse_dt(event.get("event_time"))
        or _parse_dt(event.get("first_timestamp"))
        or datetime.min.replace(tzinfo=timezone.utc)
    )


def _read_target_node(v1: Any, node_name: Optional[str], node_ip: Optional[str]) -> Optional[Any]:
    if node_name:
        try:
            return v1.read_node(node_name)
        except Exception:
            pass

    nodes = v1.list_node().items
    for node in nodes:
        info = _node_to_dict(node)
        names = {info.get("name"), info.get("hostname"), info.get("internal_ip")}
        if node_name in names or node_ip in names:
            return node
        for address in info.get("addresses", []):
            if node_ip and address.get("address") == node_ip:
                return node
    if not node_name and not node_ip and len(nodes) == 1:
        return nodes[0]
    return None


def _read_node_lease(coordination_v1: Any, node_name: str, timeout_seconds: int) -> Dict[str, Any]:
    now = datetime.now(timezone.utc)
    try:
        lease = coordination_v1.read_namespaced_lease(node_name, LEASE_NAMESPACE)
        spec = getattr(lease, "spec", None)
        renew_time = getattr(spec, "renew_time", None)
        renew_dt = _parse_dt(renew_time)
        delay = None
        if renew_dt:
            delay = max(0, int((now - renew_dt).total_seconds()))
        return {
            "found": True,
            "name": node_name,
            "namespace": LEASE_NAMESPACE,
            "holder_identity": getattr(spec, "holder_identity", None),
            "lease_duration_seconds": getattr(spec, "lease_duration_seconds", None),
            "renew_time": _k8s_ts(renew_time),
            "renew_delay_seconds": delay,
            "stale": delay is None or delay > timeout_seconds,
            "threshold_seconds": timeout_seconds,
        }
    except Exception as exc:
        return {
            "found": False,
            "name": node_name,
            "namespace": LEASE_NAMESPACE,
            "renew_delay_seconds": None,
            "stale": True,
            "threshold_seconds": timeout_seconds,
            "error": str(exc),
        }


def _list_pods_on_node(v1: Any, node_name: str) -> List[Dict[str, Any]]:
    pods = v1.list_pod_for_all_namespaces(field_selector=f"spec.nodeName={node_name}")
    return [_pod_to_dict(pod) for pod in pods.items]


def _list_related_events(v1: Any, node_name: str, pods: Iterable[Dict[str, Any]], limit: int) -> Dict[str, List[Dict[str, Any]]]:
    pod_keys = {(pod.get("namespace"), pod.get("name")) for pod in pods if pod.get("name")}
    events = v1.list_event_for_all_namespaces(limit=limit)
    all_events = [_event_to_dict(event) for event in events.items]
    all_events.sort(key=_event_sort_key, reverse=True)

    node_events = []
    pod_events = []
    for event in all_events:
        involved = event.get("involved_object") or {}
        if involved.get("kind") == "Node" and involved.get("name") == node_name:
            node_events.append(event)
        if involved.get("kind") == "Pod" and (involved.get("namespace"), involved.get("name")) in pod_keys:
            pod_events.append(event)

    return {"node_events": node_events, "pod_events": pod_events, "all_events": all_events}


def _condition_map(node: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    return {condition.get("type"): condition for condition in node.get("conditions", [])}


def _contains_any(text: str, patterns: Iterable[str]) -> bool:
    lower = text.lower()
    return any(pattern in lower for pattern in patterns)


def _pod_container_findings(pod: Dict[str, Any]) -> List[Dict[str, Any]]:
    findings = []
    for container in [*pod.get("init_containers", []), *pod.get("containers", [])]:
        state = container.get("state_detail") or {}
        last_state = container.get("last_state_detail") or {}
        if state.get("type") == "waiting":
            findings.append({
                "signal": "Waiting",
                "container": container.get("name"),
                "reason": state.get("reason"),
                "message": state.get("message"),
                "restart_count": container.get("restart_count", 0),
            })
        if last_state.get("type") == "terminated":
            findings.append({
                "signal": "LastTerminated",
                "container": container.get("name"),
                "reason": last_state.get("reason"),
                "message": last_state.get("message"),
                "exit_code": last_state.get("exit_code"),
                "restart_count": container.get("restart_count", 0),
            })
    return findings


def _pod_is_core_daemon(pod: Dict[str, Any]) -> bool:
    if pod.get("namespace") != "kube-system":
        return False
    text = " ".join([
        str(pod.get("name") or ""),
        " ".join(str(value) for value in (pod.get("labels") or {}).values()),
    ]).lower()
    return any(keyword in text for keyword in CORE_DAEMON_KEYWORDS)


def _summarize_pods(pods: List[Dict[str, Any]], pod_events: List[Dict[str, Any]]) -> Dict[str, Any]:
    phase_counts = Counter(pod.get("phase") or "Unknown" for pod in pods)
    evicted = []
    oom_killed = []
    creating = []
    unknown = []
    core_daemon_issues = []
    symptomatic = []

    cni_pods = set()
    unhealthy_pods = set()
    for event in pod_events:
        involved = event.get("involved_object") or {}
        key = (involved.get("namespace"), involved.get("name"))
        reason_msg = f"{event.get('reason') or ''} {event.get('message') or ''}"
        if _contains_any(reason_msg, CNI_ERROR_PATTERNS):
            cni_pods.add(key)
        if str(event.get("reason") or "").lower() == "unhealthy":
            unhealthy_pods.add(key)

    for pod in pods:
        key = (pod.get("namespace"), pod.get("name"))
        message = pod.get("message") or ""
        reason = pod.get("reason") or ""
        signals = []

        if pod.get("phase") == "Unknown" or reason == "NodeLost":
            unknown.append(pod)
            signals.append("Unknown/NodeLost")

        if pod.get("phase") == "Failed" and reason == "Evicted":
            evicted.append(pod)
            signals.append("Evicted")

        for finding in _pod_container_findings(pod):
            if finding.get("signal") == "LastTerminated" and finding.get("reason") == "OOMKilled":
                oom_killed.append({**pod, "container_finding": finding})
                signals.append("OOMKilled")
            if finding.get("signal") == "Waiting" and finding.get("reason") == "ContainerCreating":
                creating.append({**pod, "container_finding": finding})
                signals.append("ContainerCreating")

        restart_total = sum(_to_int(container.get("restart_count"), 0) for container in pod.get("containers", []))
        if _pod_is_core_daemon(pod) and (restart_total >= 3 or key in unhealthy_pods or pod.get("phase") not in {"Running", "Succeeded"}):
            core_daemon_issues.append({**pod, "restart_total": restart_total})
            signals.append(f"CoreDaemon restart={restart_total}")

        if key in cni_pods:
            signals.append("CNI/Sandbox event")

        if signals:
            symptomatic.append({
                "namespace": pod.get("namespace"),
                "name": pod.get("name"),
                "phase": pod.get("phase"),
                "reason": reason,
                "message": message,
                "signals": sorted(set(signals)),
            })

    observed = []
    for pod in pods:
        restart_total = sum(_to_int(container.get("restart_count"), 0) for container in pod.get("containers", []))
        observed.append({
            "namespace": pod.get("namespace"),
            "name": pod.get("name"),
            "phase": pod.get("phase"),
            "reason": pod.get("reason"),
            "restart_total": restart_total,
            "core_daemon": _pod_is_core_daemon(pod),
        })

    return {
        "total": len(pods),
        "phase_counts": dict(phase_counts),
        "evicted": evicted,
        "oom_killed": oom_killed,
        "container_creating": creating,
        "unknown": unknown,
        "core_daemon_issues": core_daemon_issues,
        "cni_event_pods": sorted(f"{ns}/{name}" for ns, name in cni_pods if name),
        "symptomatic": symptomatic,
        "observed": observed,
    }


def _evidence_item(category: str, signal: str, detail: str, source: str, severity: str = "warning", time: Any = None) -> Dict[str, Any]:
    return {
        "category": category,
        "signal": signal,
        "detail": detail,
        "source": source,
        "severity": severity,
        "time": time,
    }


def _score_evidence(node: Dict[str, Any], lease: Dict[str, Any], node_events: List[Dict[str, Any]], pod_events: List[Dict[str, Any]], pod_summary: Dict[str, Any]) -> Dict[str, Any]:
    scores: Dict[str, int] = defaultdict(int)
    evidence: List[Dict[str, Any]] = []
    seen_evidence = set()

    def add(category: str, points: int, signal: str, detail: str, source: str, severity: str = "warning", time: Any = None) -> None:
        key = (category, signal, detail, source, time)
        if key in seen_evidence:
            return
        seen_evidence.add(key)
        scores[category] += points
        evidence.append(_evidence_item(category, signal, detail, source, severity, time))

    conditions = _condition_map(node)
    ready = conditions.get("Ready", {}).get("status", node.get("ready", "Unknown"))
    ready_condition = conditions.get("Ready", {})
    lease_stale = bool(lease.get("stale"))
    lease_delay = lease.get("renew_delay_seconds")

    if ready != "True":
        add("NotReady", 3, f"Ready={ready}", ready_condition.get("reason") or "Ready condition abnormal", "v1.Node", "critical")

    if ready == "Unknown" and lease_stale:
        add(
            "ControlPlaneDisconnected",
            8,
            "ReadyUnknown+LeaseStale",
            f"Ready=Unknown 且 kube-node-lease 续约延迟 {lease_delay if lease_delay is not None else 'unknown'} 秒",
            "Ready+Lease",
            "critical",
        )
        add("Kubelet", 2, "Kubelet/CRI candidate", "Lease 停止续约，kubelet 进程退出、卡死或 CRI 阻塞均可能导致该现象", "Ready+Lease", "warning")
        add("Network", 2, "Network partition candidate", "Ready=Unknown 且 Lease 停止续约，节点到控制面网络分区仍需排查", "Ready+Lease", "warning")
    elif ready == "False" and not lease_stale:
        add("Kubelet", 2, "Kubelet reports unhealthy", "Lease 正常续约，但 Ready=False，说明 kubelet 存活并主动上报异常", "Ready+Lease", "warning")

    for cond_name, category in [
        ("MemoryPressure", "MemoryPressure"),
        ("DiskPressure", "DiskPressure"),
        ("PIDPressure", "Kubelet"),
        ("NetworkUnavailable", "Network"),
    ]:
        cond = conditions.get(cond_name)
        if cond and cond.get("status") == "True":
            add(category, 4, f"{cond_name}=True", cond.get("message") or cond.get("reason") or cond_name, "v1.Node", "critical")

    for event in [*node_events, *pod_events]:
        reason = str(event.get("reason") or "")
        message = str(event.get("message") or "")
        combined = f"{reason} {message}"
        source = f"Event/{event.get('source') or '-'}"
        time = event.get("last_timestamp") or event.get("event_time") or event.get("first_timestamp")

        if reason == "SystemOOM" or _contains_any(combined, ("system oom",)):
            add("MemoryPressure", 6, "SystemOOM", message or "System OOM event", source, "critical", time)
        if reason == "EvictionThresholdMet":
            if _contains_any(combined, DISK_PATTERNS):
                add("DiskPressure", 6, "EvictionThresholdMet", message, source, "critical", time)
            elif _contains_any(combined, MEMORY_PATTERNS):
                add("MemoryPressure", 5, "EvictionThresholdMet", message, source, "critical", time)
            else:
                add("Kubelet", 2, "EvictionThresholdMet", message, source, "warning", time)
        if reason in {"KubeletSetupFailed", "ContainerRuntimeNotReady"} or _contains_any(combined, KUBELET_PATTERNS):
            add("Kubelet", 6, reason or "runtime/kubelet error", message, source, "critical", time)
        if reason == "NodeNotReady":
            add("NotReady", 3, "NodeNotReady", message, source, "critical", time)
        if reason == "FailedCreatePodSandBox" and _contains_any(combined, CNI_ERROR_PATTERNS):
            add("Network", 6, "FailedCreatePodSandBox/CNI", message, source, "critical", time)
        elif _contains_any(combined, CNI_ERROR_PATTERNS):
            add("Network", 3, reason or "CNI/network event", message, source, "warning", time)

    for pod in pod_summary.get("evicted", []):
        msg = f"{pod.get('reason') or ''} {pod.get('message') or ''}"
        if _contains_any(msg, DISK_PATTERNS):
            add("DiskPressure", 4, "Pod Evicted by DiskPressure", f"{pod.get('namespace')}/{pod.get('name')}: {pod.get('message')}", "Pod status", "critical")
        elif _contains_any(msg, MEMORY_PATTERNS):
            add("MemoryPressure", 4, "Pod Evicted by MemoryPressure", f"{pod.get('namespace')}/{pod.get('name')}: {pod.get('message')}", "Pod status", "critical")
        else:
            add("Kubelet", 1, "Pod Evicted", f"{pod.get('namespace')}/{pod.get('name')}: {pod.get('message')}", "Pod status")

    for pod in pod_summary.get("oom_killed", []):
        finding = pod.get("container_finding", {})
        exit_code = finding.get("exit_code")
        points = 5 if exit_code == 137 else 4
        add("MemoryPressure", points, "OOMKilled", f"{pod.get('namespace')}/{pod.get('name')} container={finding.get('container')} exit_code={exit_code}", "Container lastState", "critical")

    if pod_summary.get("container_creating") and pod_summary.get("cni_event_pods"):
        add("Network", 5, "ContainerCreating + CNI event", f"{len(pod_summary['container_creating'])} 个 Pod 卡在 ContainerCreating，{len(pod_summary['cni_event_pods'])} 个 Pod 有 CNI/Sandbox 事件", "Pod status + Event", "critical")

    if pod_summary.get("unknown"):
        points = 5 if len(pod_summary["unknown"]) >= max(2, pod_summary.get("total", 0) // 2) else 3
        add("Kubelet", points, "Pod Unknown/NodeLost", f"{len(pod_summary['unknown'])} 个 Pod 处于 Unknown/NodeLost", "Pod status", "critical")

    if pod_summary.get("core_daemon_issues"):
        add("Kubelet", 4, "Core daemon unhealthy", f"{len(pod_summary['core_daemon_issues'])} 个 kube-system 核心 DaemonSet Pod 异常或重启偏高", "kube-system Pods", "critical")

    return {"scores": dict(scores), "evidence": evidence}


def _liveness_triage(node: Dict[str, Any], lease: Dict[str, Any]) -> Dict[str, Any]:
    ready = (_condition_map(node).get("Ready") or {}).get("status", node.get("ready", "Unknown"))
    stale = bool(lease.get("stale"))
    delay = lease.get("renew_delay_seconds")
    threshold = lease.get("threshold_seconds", DEFAULT_LEASE_TIMEOUT_SECONDS)

    if ready == "Unknown" and stale:
        case = "A"
        conclusion = "控制面与节点失联"
        inference = "Ready=Unknown 且 Lease 续约超过阈值，优先怀疑节点网络异常或 kubelet/CRI 僵死。"
    elif ready == "False" and not stale:
        case = "B"
        conclusion = "kubelet 存活但主动报告节点不健康"
        inference = "Lease 正常更新，控制面仍能收到 kubelet 心跳；继续沿节点条件、事件和 Pod 症状下钻。"
    elif ready == "True":
        case = "C"
        conclusion = "控制面基础通信正常"
        inference = "Ready=True，直接排查资源压力、CNI 局部异常和工作负载侧症状。"
    else:
        case = "D"
        conclusion = "控制面状态不一致或证据不足"
        inference = "Ready 与 Lease 组合不满足标准分流，需要结合事件和节点本地日志确认。"

    return {
        "case": case,
        "ready": ready,
        "lease_stale": stale,
        "lease_delay_seconds": delay,
        "lease_threshold_seconds": threshold,
        "conclusion": conclusion,
        "inference": inference,
    }


def _confidence(best_score: int, evidence_count: int) -> str:
    if best_score >= 8 or evidence_count >= 4:
        return "高 (High)"
    if best_score >= 4 or evidence_count >= 2:
        return "中 (Medium)"
    return "低 (Low)"


def _conclusion(root_category: str, liveness: Dict[str, Any]) -> str:
    if root_category == "ControlPlaneDisconnected":
        return "控制面与节点失联（网络链路或 Kubelet/CRI 心跳中断，需节点侧验证）"
    if root_category == "MemoryPressure":
        if liveness.get("case") == "A":
            return "内存压力（MemoryPressure）引发的 Kubelet 间歇性失联"
        return "内存压力（MemoryPressure）导致节点或 Pod 异常"
    if root_category == "DiskPressure":
        return "磁盘压力（DiskPressure / nodefs / imagefs）导致节点不健康或 Pod 驱逐"
    if root_category == "Network":
        return "节点网络异常或 CNI 异常导致控制面/Pod 沙箱通信失败"
    if root_category == "Kubelet":
        return "Kubelet 或容器运行时（CRI）异常"
    if root_category == "NotReady":
        return "节点 NotReady，根因仍需结合节点本地日志确认"
    return "未发现明确节点级故障"


def _build_health_items(node: Dict[str, Any], lease: Dict[str, Any], liveness: Dict[str, Any], scores: Dict[str, int]) -> List[Dict[str, str]]:
    conditions = _condition_map(node)

    def item(name: str, status: str, detail: str) -> Dict[str, str]:
        return {"item": name, "status": status, "detail": detail}

    def pressure_status(condition_value: str, score: int) -> str:
        if condition_value == "True" or score > 0:
            return "异常"
        if condition_value == "Unknown" and liveness.get("case") == "A":
            return "不可判定"
        return "正常"

    ready = conditions.get("Ready", {}).get("status", node.get("ready", "Unknown"))
    memory = conditions.get("MemoryPressure", {}).get("status", "False")
    disk = conditions.get("DiskPressure", {}).get("status", "False")
    network = conditions.get("NetworkUnavailable", {}).get("status", "False")
    lease_delay = lease.get("renew_delay_seconds")
    lease_detail = f"Lease delay={lease_delay if lease_delay is not None else 'unknown'}s, threshold={lease.get('threshold_seconds')}s"
    taints = node.get("taints") or []
    taint_detail = ", ".join(
        f"{taint.get('key')}:{taint.get('effect')}" for taint in taints if taint.get("key")
    ) or "-"

    network_status = "异常" if network == "True" or scores.get("Network", 0) >= 4 else "候选" if liveness.get("case") == "A" and scores.get("Network", 0) > 0 else "正常"

    return [
        item("NotReady", "异常" if ready != "True" else "正常", f"Ready={ready}; {conditions.get('Ready', {}).get('reason') or '-'}"),
        item("内存压力", pressure_status(memory, scores.get("MemoryPressure", 0)), f"MemoryPressure={memory}; evidence_score={scores.get('MemoryPressure', 0)}"),
        item("磁盘压力", pressure_status(disk, scores.get("DiskPressure", 0)), f"DiskPressure={disk}; evidence_score={scores.get('DiskPressure', 0)}"),
        item("网络状态", network_status, f"NetworkUnavailable={network}; evidence_score={scores.get('Network', 0)}"),
        item("Kubelet状态", "异常" if bool(lease.get("stale")) or scores.get("Kubelet", 0) >= 4 else "正常", f"{lease_detail}; liveness_case={liveness.get('case')}"),
        item("节点调度污点", "异常" if taints else "正常", taint_detail),
    ]


def _top_root_category(scores: Dict[str, int], liveness: Dict[str, Any]) -> str:
    if liveness.get("case") == "A":
        specific_candidates = {key: scores.get(key, 0) for key in ("MemoryPressure", "DiskPressure", "Network", "Kubelet")}
        category, score = max(specific_candidates.items(), key=lambda item: item[1])
        if score >= 6:
            return category
        if scores.get("ControlPlaneDisconnected", 0) > 0:
            return "ControlPlaneDisconnected"

    root_candidates = {key: scores.get(key, 0) for key in ("ControlPlaneDisconnected", "MemoryPressure", "DiskPressure", "Network", "Kubelet")}
    category, score = max(root_candidates.items(), key=lambda item: item[1])
    if score > 0:
        return category
    if scores.get("NotReady", 0) > 0:
        return "NotReady"
    return "Healthy"


def assess_node_failure_context(
    node: Dict[str, Any],
    lease: Dict[str, Any],
    node_events: List[Dict[str, Any]],
    pods: List[Dict[str, Any]],
    pod_events: List[Dict[str, Any]],
    metrics: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Assess already-collected node evidence and return conclusion data."""
    pod_summary = _summarize_pods(pods, pod_events)
    liveness = _liveness_triage(node, lease)
    scored = _score_evidence(node, lease, node_events, pod_events, pod_summary)
    scores = scored["scores"]
    evidence = scored["evidence"]
    root_category = _top_root_category(scores, liveness)
    best_score = scores.get(root_category, 0)
    category_evidence_count = len([item for item in evidence if item.get("category") == root_category])
    confidence = _confidence(best_score, category_evidence_count)

    return {
        "liveness": liveness,
        "pod_summary": pod_summary,
        "scores": scores,
        "evidence": evidence,
        "root_category": root_category,
        "conclusion": _conclusion(root_category, liveness),
        "confidence": confidence,
        "health_items": _build_health_items(node, lease, liveness, scores),
        "metrics": metrics or {},
    }


def _format_event_rows(events: List[Dict[str, Any]], limit: int = 12) -> str:
    rows = ["| 发生时间 | 级别 | 来源组件 | Reason | Message |", "| :--- | :--- | :--- | :--- | :--- |"]
    seen = set()
    for event in events:
        key = (
            event.get("last_timestamp") or event.get("event_time") or event.get("first_timestamp"),
            event.get("type"),
            event.get("source"),
            event.get("reason"),
            event.get("message"),
        )
        if key in seen:
            continue
        seen.add(key)
        rows.append(
            "| {time} | {type} | {source} | `{reason}` | {message} |".format(
                time=_md_cell(event.get("last_timestamp") or event.get("event_time") or event.get("first_timestamp")),
                type=_md_cell(event.get("type")),
                source=_md_cell(event.get("source")),
                reason=_md_cell(event.get("reason")),
                message=_md_cell(event.get("message"), 240),
            )
        )
        if len(rows) - 2 >= limit:
            break
    if len(rows) == 2:
        rows.append("| - | - | - | - | 未发现相关事件 |")
    return "\n".join(rows)


def _format_pod_rows(pod_summary: Dict[str, Any], limit: int = 12) -> str:
    rows = ["| Pod | 命名空间 | 状态 | Reason/重启 | 症状信号 |", "| :--- | :--- | :--- | :--- | :--- |"]
    symptomatic = pod_summary.get("symptomatic", [])
    if symptomatic:
        pods = symptomatic[:limit]
    else:
        pods = pod_summary.get("observed", [])[:limit]

    for pod in pods:
        signals = pod.get("signals")
        if signals:
            signal_text = ", ".join(signals)
        else:
            signal_text = "未发现明显异常"
        reason = pod.get("reason")
        if reason is None and "restart_total" in pod:
            reason = f"restart={pod.get('restart_total', 0)}"
        rows.append(
            "| `{name}` | `{namespace}` | {phase} | `{reason}` | {signals} |".format(
                name=_md_cell(pod.get("name")),
                namespace=_md_cell(pod.get("namespace")),
                phase=_md_cell(pod.get("phase")),
                reason=_md_cell(reason),
                signals=_md_cell(signal_text),
            )
        )
    if len(rows) == 2:
        rows.append("| - | - | - | - | 未发现节点上 Pod |")
    return "\n".join(rows)


def _format_metric_rows(metrics: Dict[str, Any]) -> str:
    rows = ["| 指标 | 最新值 | 状态 | 说明 |", "| :--- | :--- | :--- | :--- |"]
    labels = {
        "cpu": "CPU 使用率",
        "memory": "内存使用率",
        "disk": "磁盘使用率",
    }
    for key, label in labels.items():
        metric = metrics.get(key)
        if not metric:
            rows.append(f"| {label} | - | 未采集 | 指标缺失或监控查询无数据 |")
            continue
        value_key = f"{key}_usage_percent"
        value = metric.get(value_key)
        rows.append(
            "| {label} | {value} | {status} | {points} 个采样点 |".format(
                label=label,
                value=f"{round(value, 2)}%" if isinstance(value, (int, float)) else _md_cell(value),
                status=_md_cell(metric.get("status")),
                points=len(metric.get("time_series", []) or []),
            )
        )
    return "\n".join(rows)


def _format_evidence_rows(evidence: List[Dict[str, Any]], limit: int = 12) -> str:
    rows = ["| 类别 | 严重级别 | 信号 | 来源 | 证据摘要 |", "| :--- | :--- | :--- | :--- | :--- |"]
    for item in evidence[:limit]:
        rows.append(
            "| {category} | {severity} | `{signal}` | {source} | {detail} |".format(
                category=_md_cell(item.get("category")),
                severity=_md_cell(item.get("severity")),
                signal=_md_cell(item.get("signal")),
                source=_md_cell(item.get("source")),
                detail=_md_cell(item.get("detail"), 220),
            )
        )
    if len(rows) == 2:
        rows.append("| - | - | - | - | 暂无强匹配证据 |")
    return "\n".join(rows)


def _runbook(root_category: str, liveness: Dict[str, Any]) -> List[str]:
    steps = []
    if liveness.get("ready") != "True":
        steps.append("先执行节点隔离预览：建议由 `auto-remediation-runner` 生成 `cordon` 预览，确认影响 Pod 后再执行。")
    if root_category == "ControlPlaneDisconnected":
        steps.extend([
            "同时排查两条候选链路：节点到 apiserver 的网络连通性，以及节点本地 kubelet/CRI 进程状态。",
            "登录节点检查 `systemctl status kubelet containerd` 与 `journalctl -u kubelet`，并核对故障时刻前后是否有进程退出、PLEG 卡顿或证书/鉴权错误。",
            "从节点侧验证 apiserver、DNS、路由、安全组和网络 ACL；若节点不可登录，优先检查 ECS 实例状态和 VPC 链路。",
        ])
    elif root_category == "MemoryPressure":
        steps.extend([
            "核对 OOMKilled Pod 的 `requests/limits`、JVM/进程堆内参数与最近发布变更，优先降低热点工作负载内存占用。",
            "若 kubelet 已失联，SSH 到节点检查 `systemctl status kubelet`、`containerd`/`docker` 与 `journalctl -u kubelet` 中的 OOM 记录。",
        ])
    elif root_category == "DiskPressure":
        steps.extend([
            "检查 `nodefs`、`imagefs`、容器日志目录和 inode 使用率，优先清理无用镜像、异常日志和临时文件。",
            "确认被 Evicted 的 Pod 是否可重新调度，必要时扩容节点磁盘或迁移高写入工作负载。",
        ])
    elif root_category == "Network":
        steps.extend([
            "检查节点到控制面、API Server、DNS/DHCP、容器网络插件的连通性，并复核安全组与网络 ACL。",
            "排查 CNI DaemonSet 日志和 `FailedCreatePodSandBox` 对应 Pod 事件，确认是否存在 IPAM/DHCP 超时或插件进程异常。",
        ])
    elif root_category == "Kubelet":
        steps.extend([
            "检查 kubelet 与 CRI 运行时进程、PLEG 健康、镜像服务和容器运行时 socket。",
            "如需重启 kubelet/运行时或 drain 节点，先列出节点上 Pod、PDB 与有状态服务影响面，再由恢复 skill 走确认流程。",
        ])
    else:
        steps.append("继续采集节点本地 kubelet、CRI、内核和 CNI 日志，补齐控制面证据无法覆盖的部分。")
    steps.append("恢复验证：`Ready=True`、Lease 延迟低于阈值、异常 Event 不再增长、节点上业务 Pod 状态恢复。")
    return steps


def build_markdown_report(
    node: Dict[str, Any],
    lease: Dict[str, Any],
    node_events: List[Dict[str, Any]],
    pod_events: List[Dict[str, Any]],
    assessment: Dict[str, Any],
) -> str:
    pod_summary = assessment["pod_summary"]
    liveness = assessment["liveness"]
    evidence = assessment["evidence"]
    node_ip = node.get("internal_ip") or "-"
    phase_counts = ", ".join(f"{key}={value}" for key, value in sorted(pod_summary.get("phase_counts", {}).items())) or "-"
    blast_radius = f"影响/观察到 {pod_summary.get('total', 0)} 个 Pod；异常症状 {len(pod_summary.get('symptomatic', []))} 个；状态分布：{phase_counts}"

    health_lines = []
    for item in assessment["health_items"]:
        health_lines.append(f"* **[{item['item']}]** {item['status']}。{item['detail']}")

    runbook_lines = [f"{idx}. {step}" for idx, step in enumerate(_runbook(assessment["root_category"], liveness), start=1)]
    related_events = sorted([*node_events, *pod_events], key=_event_sort_key, reverse=True)
    taints = node.get("taints") or []
    taint_text = ", ".join(
        f"{taint.get('key')}:{taint.get('effect')}" for taint in taints if taint.get("key")
    ) or "-"
    metrics = assessment.get("metrics", {})

    return "\n".join([
        "# Kubernetes 节点自动化诊断报告",
        "",
        "## 1. 诊断总览",
        "| 评估项 | 详细信息 |",
        "| :--- | :--- |",
        f"| **目标节点** | `{_md_cell(node.get('name'))}` (IP: `{_md_cell(node_ip)}`) |",
        f"| **诊断结论** | **{_md_cell(assessment['conclusion'])}** |",
        f"| **置信度评级** | **{_md_cell(assessment['confidence'])}**；主类得分 `{assessment['scores'].get(assessment['root_category'], 0)}` |",
        f"| **爆炸半径** | {blast_radius} |",
        f"| **节点污点** | `{_md_cell(taint_text, 240)}` |",
        "",
        f"> 高危提示：控制面分流为 **情况 {liveness['case']} - {liveness['conclusion']}**。{liveness['inference']}",
        "",
        "## 2. 节点状态健康度",
        *health_lines,
        "",
        "## 3. 关键排查",
        "",
        "### 3.1 控制面存活状态分流",
        "| 信号 | 当前值 | 判断 |",
        "| :--- | :--- | :--- |",
        f"| Ready 条件 | `{_md_cell(liveness.get('ready'))}` | {liveness['conclusion']} |",
        f"| Lease 续约 | `delay={_md_cell(liveness.get('lease_delay_seconds'))}s / threshold={_md_cell(liveness.get('lease_threshold_seconds'))}s` | {'超时' if liveness.get('lease_stale') else '正常'} |",
        f"| Lease renewTime | `{_md_cell(lease.get('renew_time'))}` | namespace=`{LEASE_NAMESPACE}` |",
        "",
        "### 3.2 关键事件时序",
        _format_event_rows(related_events),
        "",
        "### 3.3 节点负载异常观测",
        _format_pod_rows(pod_summary),
        "",
        "### 3.4 指标快照",
        _format_metric_rows(metrics),
        "",
        "### 3.5 证据矩阵",
        _format_evidence_rows(evidence),
        "",
        "## 4. 诊断结论",
        f"综合 Ready/Lease、节点事件、节点上 Pod 症状与指标快照，当前判断为：**{assessment['conclusion']}**。",
        "",
        "## 5. 运维处置建议",
        *runbook_lines,
        "",
    ])


def diagnose_node_failure(
    region: str,
    cluster_id: str,
    node_name: Optional[str] = None,
    node_ip: Optional[str] = None,
    ak: Optional[str] = None,
    sk: Optional[str] = None,
    project_id: Optional[str] = None,
    lease_timeout_seconds: int = DEFAULT_LEASE_TIMEOUT_SECONDS,
    event_limit: int = 500,
    hours: int = 1,
    include_metrics: bool = True,
) -> Dict[str, Any]:
    """Diagnose a CCE node and return structured evidence plus Markdown report."""
    access_key, secret_key, proj_id = get_credentials(ak, sk, project_id)
    if not access_key or not secret_key:
        return {"success": False, "error": "Credentials not provided. Set HUAWEI_AK/HUAWEI_SK or pass ak/sk."}
    if not cluster_id:
        return {"success": False, "error": "cluster_id is required"}
    if not (node_name or node_ip):
        return {"success": False, "error": "node_name or node_ip is required"}
    if not K8S_AVAILABLE:
        return {"success": False, "error": f"Kubernetes SDK not installed: {K8S_IMPORT_ERROR}"}
    if not SDK_AVAILABLE:
        return {"success": False, "error": f"Huawei Cloud SDK not installed: {IMPORT_ERROR}"}

    cert_file = None
    key_file = None
    try:
        _, cert_file, key_file = _setup_k8s_client(region, cluster_id, access_key, secret_key, proj_id, "node_failure")
        v1 = k8s_client.CoreV1Api()
        coordination_v1 = k8s_client.CoordinationV1Api()

        node_obj = _read_target_node(v1, node_name, node_ip)
        if not node_obj:
            return {
                "success": False,
                "error": f"Cannot find node by node_name={node_name!r} or node_ip={node_ip!r}",
            }

        node = _node_to_dict(node_obj)
        lease = _read_node_lease(coordination_v1, node["name"], lease_timeout_seconds)
        pods = _list_pods_on_node(v1, node["name"])
        events = _list_related_events(v1, node["name"], pods, event_limit)

        metrics: Dict[str, Any] = {}
        metric_error = None
        if include_metrics and (node.get("internal_ip") or node_ip):
            metrics_result = cce_metrics.get_cce_node_metrics(
                region,
                cluster_id,
                node.get("internal_ip") or node_ip,
                access_key,
                secret_key,
                proj_id,
                hours,
            )
            if metrics_result.get("success"):
                metrics = metrics_result.get("metrics", metrics_result)
            else:
                metric_error = metrics_result.get("error")

        assessment = assess_node_failure_context(
            node,
            lease,
            events["node_events"],
            pods,
            events["pod_events"],
            metrics,
        )
        report = build_markdown_report(node, lease, events["node_events"], events["pod_events"], assessment)

        return {
            "success": True,
            "action": "huawei_node_failure_diagnose",
            "region": region,
            "cluster_id": cluster_id,
            "node": node,
            "lease": lease,
            "liveness": assessment["liveness"],
            "conclusion": assessment["conclusion"],
            "confidence": assessment["confidence"],
            "root_category": assessment["root_category"],
            "scores": assessment["scores"],
            "evidence": assessment["evidence"],
            "health_items": assessment["health_items"],
            "pod_summary": assessment["pod_summary"],
            "node_events": events["node_events"],
            "pod_events": events["pod_events"],
            "metrics": metrics,
            "metric_error": metric_error,
            "report_markdown": report,
        }
    except Exception as exc:
        return {"success": False, "error": str(exc), "error_type": type(exc).__name__}
    finally:
        _safe_delete_file(cert_file)
        _safe_delete_file(key_file)


def diagnose_node_failure_action(params: Dict[str, str]) -> Dict[str, Any]:
    return diagnose_node_failure(
        region=params["region"],
        cluster_id=params["cluster_id"],
        node_name=params.get("node_name"),
        node_ip=params.get("node_ip"),
        ak=params.get("ak"),
        sk=params.get("sk"),
        project_id=params.get("project_id"),
        lease_timeout_seconds=_to_int(params.get("lease_timeout_seconds"), DEFAULT_LEASE_TIMEOUT_SECONDS),
        event_limit=_to_int(params.get("event_limit"), 500),
        hours=_to_int(params.get("hours"), 1),
        include_metrics=_as_bool(params.get("include_metrics"), True),
    )
