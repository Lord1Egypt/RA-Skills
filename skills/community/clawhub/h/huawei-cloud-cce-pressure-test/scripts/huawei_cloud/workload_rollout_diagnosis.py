"""Workload rollout diagnosis helpers for CCE clusters."""

from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional, Tuple

from .common import (
    IMPORT_ERROR,
    K8S_AVAILABLE,
    K8S_IMPORT_ERROR,
    SDK_AVAILABLE,
    _safe_delete_file,
    get_credentials,
    k8s_client,
)
from . import cce_k8s, pod_diagnosis


SUPPORTED_KINDS = {
    "deployment": "Deployment",
    "deploy": "Deployment",
    "statefulset": "StatefulSet",
    "sts": "StatefulSet",
    "daemonset": "DaemonSet",
    "ds": "DaemonSet",
}

ADMISSION_KEYWORDS = (
    "admission",
    "denied",
    "forbidden",
    "resourcequota",
    "quota",
    "limitrange",
    "limit range",
    "webhook",
    "podsecurity",
    "securitycontextconstraints",
)


def _to_int(value: Any, default: int = 0) -> int:
    try:
        return int(value) if value is not None else default
    except (TypeError, ValueError):
        return default


def _kind(kind: str) -> Optional[str]:
    return SUPPORTED_KINDS.get((kind or "").strip().lower())


def _ts(value: Any) -> Optional[str]:
    if value is None:
        return None
    if hasattr(value, "isoformat"):
        return value.isoformat()
    return str(value)


def _parse_ts(value: Any) -> datetime:
    if value is None:
        return datetime.min.replace(tzinfo=timezone.utc)
    if isinstance(value, datetime):
        return value if value.tzinfo else value.replace(tzinfo=timezone.utc)
    text = str(value)
    if not text:
        return datetime.min.replace(tzinfo=timezone.utc)
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(text)
        return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)
    except ValueError:
        return datetime.min.replace(tzinfo=timezone.utc)


def _plain_mapping(value: Any) -> Dict[str, Any]:
    if not value:
        return {}
    if isinstance(value, dict):
        return {str(k): v for k, v in value.items()}
    try:
        return {str(k): v for k, v in dict(value).items()}
    except Exception:
        return {}


def _stringify(value: Any) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, (str, int, float, bool)):
        return str(value)
    return str(value)


def _string_map(value: Any) -> Dict[str, str]:
    return {key: _stringify(item) or "" for key, item in _plain_mapping(value).items()}


def _owner_references(owner_refs: Any) -> List[Dict[str, Any]]:
    result = []
    for ref in owner_refs or []:
        result.append({
            "api_version": getattr(ref, "api_version", None),
            "kind": getattr(ref, "kind", None),
            "name": getattr(ref, "name", None),
            "uid": getattr(ref, "uid", None),
            "controller": getattr(ref, "controller", None),
            "block_owner_deletion": getattr(ref, "block_owner_deletion", None),
        })
    return result


def _conditions(conditions: Any) -> List[Dict[str, Any]]:
    result = []
    for condition in conditions or []:
        result.append({
            "type": getattr(condition, "type", None),
            "status": getattr(condition, "status", None),
            "reason": getattr(condition, "reason", None),
            "message": getattr(condition, "message", None),
            "last_transition_time": _ts(getattr(condition, "last_transition_time", None)),
            "last_update_time": _ts(getattr(condition, "last_update_time", None)),
        })
    return result


def _resource_requirements(spec: Any) -> Dict[str, Dict[str, str]]:
    resources = getattr(spec, "resources", None)
    if not resources:
        return {"requests": {}, "limits": {}}
    return {
        "requests": _string_map(getattr(resources, "requests", None)),
        "limits": _string_map(getattr(resources, "limits", None)),
    }


def _container_state(state: Any) -> Dict[str, Any]:
    if not state:
        return {}
    waiting = getattr(state, "waiting", None)
    running = getattr(state, "running", None)
    terminated = getattr(state, "terminated", None)
    if waiting:
        return {
            "type": "waiting",
            "reason": getattr(waiting, "reason", None),
            "message": getattr(waiting, "message", None),
        }
    if running:
        return {
            "type": "running",
            "started_at": _ts(getattr(running, "started_at", None)),
        }
    if terminated:
        return {
            "type": "terminated",
            "reason": getattr(terminated, "reason", None),
            "message": getattr(terminated, "message", None),
            "exit_code": getattr(terminated, "exit_code", None),
            "signal": getattr(terminated, "signal", None),
            "started_at": _ts(getattr(terminated, "started_at", None)),
            "finished_at": _ts(getattr(terminated, "finished_at", None)),
        }
    return {}


def _container_status(cs: Any, spec_by_name: Dict[str, Any]) -> Dict[str, Any]:
    spec = spec_by_name.get(getattr(cs, "name", ""))
    return {
        "name": getattr(cs, "name", None),
        "image": getattr(cs, "image", None) or getattr(spec, "image", None),
        "image_id": getattr(cs, "image_id", None),
        "container_id": getattr(cs, "container_id", None),
        "ready": getattr(cs, "ready", None),
        "started": getattr(cs, "started", None),
        "restart_count": getattr(cs, "restart_count", 0),
        "state": str(getattr(cs, "state", None)) if getattr(cs, "state", None) else None,
        "state_detail": _container_state(getattr(cs, "state", None)),
        "last_state": str(getattr(cs, "last_state", None)) if getattr(cs, "last_state", None) else None,
        "last_state_detail": _container_state(getattr(cs, "last_state", None)),
        "resources": _resource_requirements(spec),
    }


def _selector_from_match_labels(match_labels: Dict[str, Any]) -> Optional[str]:
    labels = {str(k): str(v) for k, v in (match_labels or {}).items() if k and v is not None}
    if not labels:
        return None
    return ",".join(f"{key}={labels[key]}" for key in sorted(labels))


def _selector_info(selector: Any) -> Dict[str, Any]:
    if not selector:
        return {"match_labels": {}, "match_expressions": [], "label_selector": None}
    match_labels = _plain_mapping(getattr(selector, "match_labels", None))
    expressions = []
    for expr in getattr(selector, "match_expressions", None) or []:
        expressions.append({
            "key": getattr(expr, "key", None),
            "operator": getattr(expr, "operator", None),
            "values": list(getattr(expr, "values", None) or []),
        })
    return {
        "match_labels": match_labels,
        "match_expressions": expressions,
        "label_selector": _selector_from_match_labels(match_labels),
    }


def _strategy_info(strategy: Any) -> Dict[str, Any]:
    if not strategy:
        return {}
    rolling = getattr(strategy, "rolling_update", None)
    result = {"type": getattr(strategy, "type", None)}
    if rolling:
        result["rolling_update"] = {
            "max_surge": _stringify(getattr(rolling, "max_surge", None)),
            "max_unavailable": _stringify(getattr(rolling, "max_unavailable", None)),
            "partition": getattr(rolling, "partition", None),
        }
    return result


def _metadata(obj: Any) -> Dict[str, Any]:
    metadata = getattr(obj, "metadata", None)
    return {
        "name": getattr(metadata, "name", None),
        "namespace": getattr(metadata, "namespace", None),
        "uid": getattr(metadata, "uid", None),
        "resource_version": getattr(metadata, "resource_version", None),
        "generation": getattr(metadata, "generation", None),
        "created": _ts(getattr(metadata, "creation_timestamp", None)),
        "labels": _plain_mapping(getattr(metadata, "labels", None)),
        "annotations": _plain_mapping(getattr(metadata, "annotations", None)),
        "owner_references": _owner_references(getattr(metadata, "owner_references", None)),
    }


def _serialize_workload(obj: Any, kind: str) -> Dict[str, Any]:
    spec = getattr(obj, "spec", None)
    status = getattr(obj, "status", None)
    meta = _metadata(obj)
    selector = _selector_info(getattr(spec, "selector", None))
    common = {
        "kind": kind,
        "api_version": "apps/v1",
        "name": meta["name"],
        "namespace": meta["namespace"],
        "uid": meta["uid"],
        "resource_version": meta["resource_version"],
        "generation": meta["generation"],
        "created": meta["created"],
        "labels": meta["labels"],
        "annotations": meta["annotations"],
        "selector": selector,
        "conditions": _conditions(getattr(status, "conditions", None)),
        "observed_generation": getattr(status, "observed_generation", None),
    }

    if kind == "Deployment":
        common.update({
            "desired_replicas": getattr(spec, "replicas", None),
            "strategy": _strategy_info(getattr(spec, "strategy", None)),
            "min_ready_seconds": getattr(spec, "min_ready_seconds", None),
            "progress_deadline_seconds": getattr(spec, "progress_deadline_seconds", None),
            "status_replicas": getattr(status, "replicas", None),
            "updated_replicas": getattr(status, "updated_replicas", None),
            "ready_replicas": getattr(status, "ready_replicas", None),
            "available_replicas": getattr(status, "available_replicas", None),
            "unavailable_replicas": getattr(status, "unavailable_replicas", None),
        })
    elif kind == "StatefulSet":
        common.update({
            "desired_replicas": getattr(spec, "replicas", None),
            "strategy": _strategy_info(getattr(spec, "update_strategy", None)),
            "pod_management_policy": getattr(spec, "pod_management_policy", None),
            "service_name": getattr(spec, "service_name", None),
            "status_replicas": getattr(status, "replicas", None),
            "current_replicas": getattr(status, "current_replicas", None),
            "updated_replicas": getattr(status, "updated_replicas", None),
            "ready_replicas": getattr(status, "ready_replicas", None),
            "available_replicas": getattr(status, "available_replicas", None),
            "current_revision": getattr(status, "current_revision", None),
            "update_revision": getattr(status, "update_revision", None),
        })
    else:
        desired = getattr(status, "desired_number_scheduled", None)
        common.update({
            "desired_replicas": desired,
            "strategy": _strategy_info(getattr(spec, "update_strategy", None)),
            "status_replicas": getattr(status, "current_number_scheduled", None),
            "current_replicas": getattr(status, "current_number_scheduled", None),
            "updated_replicas": getattr(status, "updated_number_scheduled", None),
            "ready_replicas": getattr(status, "number_ready", None),
            "available_replicas": getattr(status, "number_available", None),
            "unavailable_replicas": getattr(status, "number_unavailable", None),
            "misscheduled_replicas": getattr(status, "number_misscheduled", None),
        })
    return common


def _serialize_rs(rs: Any) -> Dict[str, Any]:
    metadata = _metadata(rs)
    spec = getattr(rs, "spec", None)
    status = getattr(rs, "status", None)
    annotations = metadata["annotations"]
    revision = _to_int(annotations.get("deployment.kubernetes.io/revision"), -1)
    return {
        "kind": "ReplicaSet",
        "api_version": "apps/v1",
        "name": metadata["name"],
        "namespace": metadata["namespace"],
        "uid": metadata["uid"],
        "resource_version": metadata["resource_version"],
        "created": metadata["created"],
        "labels": metadata["labels"],
        "annotations": annotations,
        "owner_references": metadata["owner_references"],
        "revision": revision if revision >= 0 else None,
        "selector": _selector_info(getattr(spec, "selector", None)),
        "desired_replicas": getattr(spec, "replicas", None),
        "status_replicas": getattr(status, "replicas", None),
        "ready_replicas": getattr(status, "ready_replicas", None),
        "available_replicas": getattr(status, "available_replicas", None),
        "fully_labeled_replicas": getattr(status, "fully_labeled_replicas", None),
        "observed_generation": getattr(status, "observed_generation", None),
        "conditions": _conditions(getattr(status, "conditions", None)),
    }


def _serialize_pod(pod: Any) -> Dict[str, Any]:
    metadata = _metadata(pod)
    spec = getattr(pod, "spec", None)
    status = getattr(pod, "status", None)
    spec_containers = {c.name: c for c in (getattr(spec, "containers", None) or [])}
    init_spec_containers = {c.name: c for c in (getattr(spec, "init_containers", None) or [])}
    return {
        "kind": "Pod",
        "api_version": "v1",
        "name": metadata["name"],
        "namespace": metadata["namespace"],
        "uid": metadata["uid"],
        "resource_version": metadata["resource_version"],
        "created": metadata["created"],
        "labels": metadata["labels"],
        "annotations": metadata["annotations"],
        "owner_references": metadata["owner_references"],
        "status": getattr(status, "phase", None),
        "phase": getattr(status, "phase", None),
        "reason": getattr(status, "reason", None),
        "message": getattr(status, "message", None),
        "node": getattr(spec, "node_name", None),
        "ip": getattr(status, "pod_ip", None),
        "host_ip": getattr(status, "host_ip", None),
        "qos_class": getattr(status, "qos_class", None),
        "conditions": _conditions(getattr(status, "conditions", None)),
        "restart_policy": getattr(spec, "restart_policy", None),
        "service_account": getattr(spec, "service_account_name", None),
        "image_pull_secrets": [
            item.name for item in (getattr(spec, "image_pull_secrets", None) or []) if getattr(item, "name", None)
        ],
        "containers": [
            _container_status(cs, spec_containers)
            for cs in (getattr(status, "container_statuses", None) or [])
        ],
        "init_containers": [
            _container_status(cs, init_spec_containers)
            for cs in (getattr(status, "init_container_statuses", None) or [])
        ],
    }


def _serialize_event(event: Any) -> Dict[str, Any]:
    metadata = getattr(event, "metadata", None)
    involved = getattr(event, "involved_object", None)
    event_time = (
        getattr(event, "event_time", None)
        or getattr(event, "last_timestamp", None)
        or getattr(event, "first_timestamp", None)
        or getattr(metadata, "creation_timestamp", None)
    )
    return {
        "name": getattr(metadata, "name", None),
        "namespace": getattr(metadata, "namespace", None),
        "uid": getattr(metadata, "uid", None),
        "resource_version": getattr(metadata, "resource_version", None),
        "type": getattr(event, "type", None),
        "reason": getattr(event, "reason", None),
        "message": getattr(event, "message", None),
        "first_timestamp": _ts(getattr(event, "first_timestamp", None)),
        "last_timestamp": _ts(getattr(event, "last_timestamp", None)),
        "event_time": _ts(event_time),
        "count": getattr(event, "count", None) or 1,
        "involved_object": {
            "api_version": getattr(involved, "api_version", None),
            "kind": getattr(involved, "kind", None),
            "name": getattr(involved, "name", None),
            "namespace": getattr(involved, "namespace", None),
            "uid": getattr(involved, "uid", None),
            "resource_version": getattr(involved, "resource_version", None),
            "field_path": getattr(involved, "field_path", None),
        } if involved else None,
    }


def _read_workload(apps_v1: Any, namespace: str, kind: str, name: str) -> Any:
    if kind == "Deployment":
        return apps_v1.read_namespaced_deployment(name, namespace)
    if kind == "StatefulSet":
        return apps_v1.read_namespaced_stateful_set(name, namespace)
    return apps_v1.read_namespaced_daemon_set(name, namespace)


def _list_replicasets(apps_v1: Any, namespace: str, selector: Optional[str], workload_uid: Optional[str]) -> List[Dict[str, Any]]:
    rs_list = apps_v1.list_namespaced_replica_set(namespace, label_selector=selector)
    serialized = [_serialize_rs(rs) for rs in rs_list.items]
    if not workload_uid:
        return serialized
    return [
        rs for rs in serialized
        if any(ref.get("uid") == workload_uid and ref.get("kind") == "Deployment" for ref in rs.get("owner_references") or [])
    ]


def _list_pods(core_v1: Any, namespace: str, selector: Optional[str]) -> List[Dict[str, Any]]:
    pods = core_v1.list_namespaced_pod(namespace, label_selector=selector)
    return [_serialize_pod(pod) for pod in pods.items]


def _list_events(core_v1: Any, namespace: str, limit: int) -> List[Dict[str, Any]]:
    events: List[Dict[str, Any]] = []
    continue_token = None
    total = 0
    max_events = max(1, limit)
    field_selector = f"involvedObject.namespace={namespace}"
    while total < max_events:
        page_size = min(500, max_events - total)
        page = core_v1.list_namespaced_event(
            namespace,
            field_selector=field_selector,
            limit=page_size,
            _continue=continue_token,
        )
        if not page.items:
            break
        events.extend(_serialize_event(event) for event in page.items)
        total += len(page.items)
        continue_token = getattr(page.metadata, "_continue", None) or getattr(page.metadata, "continue_", None)
        if not continue_token:
            break
    return events


def _filter_events_by_uid(events: List[Dict[str, Any]], uids: Iterable[Optional[str]]) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    uid_set = {uid for uid in uids if uid}
    missing_uid_count = 0
    filtered = []
    for event in events:
        involved = event.get("involved_object") or {}
        involved_uid = involved.get("uid")
        if not involved_uid:
            missing_uid_count += 1
            continue
        if involved_uid in uid_set:
            filtered.append(event)
    filtered.sort(key=lambda item: _parse_ts(item.get("event_time")), reverse=True)
    return filtered, {
        "uid_count": len(uid_set),
        "before_count": len(events),
        "after_count": len(filtered),
        "events_without_involved_uid": missing_uid_count,
    }


def _owner_matches(refs: List[Dict[str, Any]], kind: str, name: Optional[str] = None, uid: Optional[str] = None) -> bool:
    for ref in refs or []:
        if ref.get("kind") != kind:
            continue
        if uid and ref.get("uid") == uid:
            return True
        if name and ref.get("name") == name:
            return True
    return False


def _pick_new_rs(replicasets: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    candidates = [rs for rs in replicasets if rs.get("revision") is not None]
    if not candidates:
        return None
    return max(candidates, key=lambda rs: (_to_int(rs.get("revision"), -1), _parse_ts(rs.get("created"))))


def _condition(items: List[Dict[str, Any]], condition_type: str) -> Dict[str, Any]:
    for item in items or []:
        if item.get("type") == condition_type:
            return item
    return {}


def _is_pod_ready(pod: Dict[str, Any]) -> bool:
    return (_condition(pod.get("conditions") or [], "Ready").get("status") == "True")


def _all_containers(pod: Dict[str, Any]) -> List[Dict[str, Any]]:
    return list(pod.get("init_containers") or []) + list(pod.get("containers") or [])


def _pod_has_abnormal_signal(pod: Dict[str, Any]) -> bool:
    if pod.get("phase") not in {"Running", "Succeeded"}:
        return True
    if not _is_pod_ready(pod):
        return True
    for container in _all_containers(pod):
        state = container.get("state_detail") or {}
        if state.get("type") == "waiting":
            return True
        if container.get("ready") is False:
            return True
        if _to_int(container.get("restart_count"), 0) >= 3:
            return True
    return False


def _event_text(event: Dict[str, Any]) -> str:
    return f"{event.get('reason') or ''} {event.get('message') or ''}".lower()


def _events_for_object(events: List[Dict[str, Any]], uid: Optional[str] = None, kind: Optional[str] = None, name: Optional[str] = None) -> List[Dict[str, Any]]:
    result = []
    for event in events:
        involved = event.get("involved_object") or {}
        if uid and involved.get("uid") == uid:
            result.append(event)
            continue
        if kind and name and involved.get("kind") == kind and involved.get("name") == name:
            result.append(event)
    return result


def _add_cause(
    causes: List[Dict[str, Any]],
    cause_type: str,
    title: str,
    confidence: float,
    evidence: List[Dict[str, Any]],
    recommendation: List[str],
) -> None:
    for cause in causes:
        if cause.get("type") == cause_type:
            cause["confidence"] = max(cause.get("confidence", 0), confidence)
            cause["evidence"].extend(evidence)
            for item in recommendation:
                if item not in cause["recommendation"]:
                    cause["recommendation"].append(item)
            cause["evidence"] = cause["evidence"][:10]
            cause["recommendation"] = cause["recommendation"][:6]
            return
    causes.append({
        "type": cause_type,
        "title": title,
        "confidence": confidence,
        "evidence": evidence[:10],
        "recommendation": recommendation[:6],
    })


def _status_layer(layer: str, expected: Optional[int], actual: Optional[int]) -> Dict[str, Any]:
    status = "unknown"
    if expected is not None and actual is not None:
        status = "pass" if actual >= expected else "fail"
    return {"layer": layer, "expected": expected, "actual": actual, "status": status}


def _new_rs_desired_layer(workload: Dict[str, Any], expected: Optional[int], actual: Optional[int]) -> Dict[str, Any]:
    layer = _status_layer("new_rs_desired", expected, actual)
    if layer["status"] != "fail":
        return layer
    ready = workload.get("ready_replicas")
    available = workload.get("available_replicas")
    updated = workload.get("updated_replicas")
    if expected is not None and (
        (ready is not None and _to_int(ready) >= _to_int(expected))
        or (available is not None and _to_int(available) >= _to_int(expected))
    ):
        layer["status"] = "held"
        layer["reason"] = "rolling_update_capacity_guard"
        layer["message"] = "新版本 Pod 未就绪时，Deployment 暂缓继续扩 NewRS 以保持旧版本可用副本。"
    elif updated is not None and actual is not None and _to_int(updated) == _to_int(actual):
        layer["status"] = "waiting"
        layer["reason"] = "waiting_for_new_pods"
    return layer


def _deployment_version(context: Dict[str, Any]) -> Dict[str, Any]:
    replicasets = context.get("replicasets") or []
    new_rs = _pick_new_rs(replicasets)
    old_rs = [rs for rs in replicasets if not new_rs or rs.get("uid") != new_rs.get("uid")]
    new_pods = []
    if new_rs:
        new_pods = [
            pod for pod in context.get("pods") or []
            if _owner_matches(pod.get("owner_references") or [], "ReplicaSet", new_rs.get("name"), new_rs.get("uid"))
        ]
    return {
        "strategy": "DeploymentReplicaSet",
        "new_rs": new_rs,
        "old_rs": old_rs,
        "new_pods": new_pods,
    }


def _workload_expected(workload: Dict[str, Any]) -> Optional[int]:
    desired = workload.get("desired_replicas")
    if desired is None and workload.get("kind") == "DaemonSet":
        desired = workload.get("current_replicas")
    return desired


def _build_funnel(context: Dict[str, Any], version: Dict[str, Any]) -> List[Dict[str, Any]]:
    workload = context.get("workload") or {}
    expected = _workload_expected(workload)
    funnel = [
        _status_layer("workload_current", expected, workload.get("status_replicas") or workload.get("current_replicas")),
        _status_layer("workload_updated", expected, workload.get("updated_replicas")),
        _status_layer("workload_ready", expected, workload.get("ready_replicas")),
        _status_layer("workload_available", expected, workload.get("available_replicas")),
    ]
    if workload.get("kind") == "Deployment":
        new_rs = version.get("new_rs") or {}
        new_pods = version.get("new_pods") or []
        new_expected = new_rs.get("desired_replicas")
        funnel.insert(1, _new_rs_desired_layer(workload, expected, new_expected))
        funnel.insert(2, _status_layer("new_rs_created", new_expected, new_rs.get("status_replicas")))
        funnel.insert(3, _status_layer("new_pods_ready", new_expected, sum(1 for pod in new_pods if _is_pod_ready(pod))))
    return funnel


def _progress_deadline_exceeded(workload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    condition = _condition(workload.get("conditions") or [], "Progressing")
    if condition.get("status") == "False" and condition.get("reason") == "ProgressDeadlineExceeded":
        return condition
    return None


def _diagnose_abnormal_pods(
    context: Dict[str, Any],
    pods: List[Dict[str, Any]],
    include_logs: bool,
    include_metrics: bool,
    region: str,
    cluster_id: str,
    ak: Optional[str],
    sk: Optional[str],
    project_id: Optional[str],
    tail_lines: int,
    hours: int,
    max_pods: int,
) -> List[Dict[str, Any]]:
    abnormal = [pod for pod in pods if _pod_has_abnormal_signal(pod)][:max_pods]
    pod_diags = [pod_diagnosis._diagnose_pod(pod, context.get("events") or []) for pod in abnormal]
    if include_logs:
        log_budget = 5
        for diag in pod_diags:
            if log_budget <= 0:
                break
            if not diag.get("issues"):
                continue
            if any(issue.get("type") == "ImagePullBackOff" for issue in diag.get("issues") or []):
                continue
            diag["logs"] = pod_diagnosis._fetch_pod_logs(
                region, cluster_id, diag, ak, sk, project_id, tail_lines,
            )
            log_budget -= 1
    if include_metrics:
        for diag in pod_diags:
            try:
                diag["metrics"] = pod_diagnosis._fetch_pod_metrics(
                    region, cluster_id, diag, ak, sk, project_id, hours,
                )
            except Exception as exc:
                diag["metrics"] = {"success": False, "error": str(exc), "error_type": type(exc).__name__}
    return pod_diags


def _add_pod_causes(causes: List[Dict[str, Any]], pod_diags: List[Dict[str, Any]], events: List[Dict[str, Any]]) -> None:
    issue_counts = Counter(
        issue.get("type")
        for diag in pod_diags
        for issue in (diag.get("issues") or [])
    )
    affected = [
        f"{diag.get('pod', {}).get('namespace')}/{diag.get('pod', {}).get('name')}"
        for diag in pod_diags
    ]
    probe_pods = []
    for diag in pod_diags:
        pod = diag.get("pod") or {}
        pod_events = _events_for_object(events, name=pod.get("name"), kind="Pod")
        if any(event.get("reason") == "Unhealthy" for event in pod_events):
            probe_pods.append(f"{pod.get('namespace')}/{pod.get('name')}")

    if probe_pods:
        _add_cause(
            causes,
            "ProbeFailure",
            "新版本 Pod 运行中但探针失败或未就绪",
            0.88,
            [{"affected_pods": sorted(set(probe_pods))}],
            [
                "区分 startupProbe、livenessProbe、readinessProbe 失败类型，核对路径、端口、初始延迟和阈值。",
                "查看 Pod current/previous 日志，确认应用是否已监听健康检查端口。",
            ],
        )
    command_errors = _command_error_evidence(pod_diags)
    if command_errors:
        _add_cause(
            causes,
            "ContainerCommandNotFound",
            "新版本容器启动命令或入口文件不存在",
            0.94,
            command_errors,
            [
                "检查 Deployment command/args、镜像 ENTRYPOINT/CMD，以及容器内是否存在目标可执行文件。",
                "确认镜像 tag 是否为预期版本，必要时进入同镜像调试或回滚到上一稳定版本。",
            ],
        )
    mapping = {
        "PendingScheduling": ("SchedulingBlocked", "新版本 Pod 调度条件不满足"),
        "PendingStorage": ("StorageMountBlocked", "新版本 Pod 存储挂载或绑定异常"),
        "ImagePullBackOff": ("ImagePullBlocked", "新版本 Pod 镜像拉取失败"),
        "CrashLoopBackOff": ("CrashLoopOrAppExit", "新版本容器反复启动失败"),
        "FrequentRestart": ("CrashLoopOrAppExit", "新版本容器频繁重启"),
        "OOMKilled": ("OOMKilled", "新版本容器被 OOM Killer 终止"),
        "Evicted": ("Evicted", "新版本 Pod 被节点驱逐"),
        "PodNotReady": ("PodNotReady", "新版本 Pod 未就绪"),
    }
    for issue_type, count in issue_counts.items():
        mapped = mapping.get(issue_type)
        if not mapped:
            continue
        cause_type, title = mapped
        _add_cause(
            causes,
            cause_type,
            title,
            0.84 if count > 0 else 0.6,
            [{"issue_type": issue_type, "affected_count": count, "affected_pods": affected[:10]}],
            [
                "复用 pod-failure-diagnoser 的事件、容器状态和日志证据继续下钻。",
            ],
        )


def _command_error_evidence(pod_diags: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    evidence = []
    needles = (
        "executable file not found",
        "no such file or directory",
        "not found in $path",
        "permission denied",
    )
    for diag in pod_diags:
        pod = diag.get("pod") or {}
        for issue in diag.get("issues") or []:
            if issue.get("type") not in {"CrashLoopBackOff", "FrequentRestart"}:
                continue
            for item in issue.get("evidence") or []:
                termination = item.get("last_termination") if isinstance(item, dict) else None
                message = (termination or {}).get("message") or item.get("message")
                if not message:
                    continue
                lowered = str(message).lower()
                if "exec:" in lowered and any(needle in lowered for needle in needles):
                    evidence.append({
                        "pod": f"{pod.get('namespace')}/{pod.get('name')}",
                        "container": item.get("container") or issue.get("container"),
                        "reason": (termination or {}).get("reason"),
                        "exit_code": (termination or {}).get("exit_code"),
                        "message": message,
                    })
    return evidence[:5]


def analyze_rollout_context(
    context: Dict[str, Any],
    include_pod_diagnosis: bool = True,
    include_logs: bool = True,
    include_metrics: bool = False,
    region: Optional[str] = None,
    cluster_id: Optional[str] = None,
    ak: Optional[str] = None,
    sk: Optional[str] = None,
    project_id: Optional[str] = None,
    tail_lines: int = 80,
    hours: int = 1,
    max_pods: int = 20,
) -> Dict[str, Any]:
    workload = context.get("workload") or {}
    kind = workload.get("kind")
    events = context.get("events") or []
    causes: List[Dict[str, Any]] = []
    warnings: List[Dict[str, Any]] = []
    version: Dict[str, Any]
    target_pods: List[Dict[str, Any]]

    generation = workload.get("generation")
    observed = workload.get("observed_generation")
    generation_check = {
        "generation": generation,
        "observed_generation": observed,
        "observed": None,
    }
    if generation is not None and observed is not None:
        generation_check["observed"] = _to_int(observed, 0) >= _to_int(generation, 0)
        if not generation_check["observed"]:
            _add_cause(
                causes,
                "ControlPlaneNotObserved",
                "工作负载控制面尚未观察到最新 spec generation",
                0.95,
                [{"generation": generation, "observed_generation": observed}],
                [
                    "检查 kube-apiserver/controller-manager 限流、控制面压力和相关 AOM 告警。",
                    "等待控制面观察到最新 generation 后再判断 ReplicaSet/Pod 侧问题。",
                ],
            )
    else:
        warnings.append({"stage": "generation_check", "message": "generation or observedGeneration is missing"})

    if kind == "Deployment":
        version = _deployment_version(context)
        target_pods = version.get("new_pods") or []
    else:
        version = {
            "strategy": f"{kind}Controller",
            "current_revision": workload.get("current_revision"),
            "update_revision": workload.get("update_revision"),
        }
        target_pods = list(context.get("pods") or [])

    funnel = _build_funnel(context, version)

    if not causes and kind == "Deployment":
        new_rs = version.get("new_rs")
        if not new_rs:
            _add_cause(
                causes,
                "ReplicaSetCreateBlocked",
                "Deployment 未找到可归属的新 ReplicaSet",
                0.78,
                [{"replicaset_count": len(context.get("replicasets") or [])}],
                ["检查 Deployment 事件和控制器状态，确认 ReplicaSet 是否被准入或控制面问题阻断。"],
            )
        else:
            new_rs_events = _events_for_object(events, new_rs.get("uid"), "ReplicaSet", new_rs.get("name"))
            failed_create_events = [
                event for event in new_rs_events
                if event.get("type") == "Warning" and event.get("reason") == "FailedCreate"
            ]
            new_desired = _to_int(new_rs.get("desired_replicas"), 0)
            new_actual = _to_int(new_rs.get("status_replicas"), 0)
            if new_desired > 0 and (new_actual == 0 or not target_pods):
                if failed_create_events:
                    text = " ".join(_event_text(event) for event in failed_create_events)
                    cause_type = "QuotaOrAdmissionRejected" if any(keyword in text for keyword in ADMISSION_KEYWORDS) else "ReplicaSetCreateBlocked"
                    _add_cause(
                        causes,
                        cause_type,
                        "新版本 ReplicaSet 无法创建 Pod",
                        0.92,
                        failed_create_events[:5],
                        [
                            "根据 FailedCreate 事件检查 ResourceQuota、LimitRange、准入 webhook、PodSecurity 或镜像策略。",
                            "如果事件指向配额，先确认 namespace quota 和 requests/limits 是否满足。",
                        ],
                    )
                else:
                    _add_cause(
                        causes,
                        "ReplicaSetCreateBlocked",
                        "新版本 ReplicaSet 期望副本大于 0，但未派生出 Pod",
                        0.82,
                        [{"new_rs": new_rs}],
                        ["检查 ReplicaSet Warning 事件、控制器状态和命名空间配额。"],
                    )

    timeout_condition = _progress_deadline_exceeded(workload)
    if timeout_condition:
        _add_cause(
            causes,
            "RolloutTimeout",
            "Deployment 滚动升级超过 progressDeadlineSeconds",
            0.9,
            [timeout_condition],
            ["优先处理导致 NewRS Pod 不 Ready 的具体原因，再重新观察 rollout。"],
        )

    pod_diags: List[Dict[str, Any]] = []
    if include_pod_diagnosis and target_pods:
        pod_diags = _diagnose_abnormal_pods(
            context,
            target_pods,
            include_logs,
            include_metrics,
            region or context.get("region"),
            cluster_id or context.get("cluster_id"),
            ak,
            sk,
            project_id,
            tail_lines,
            hours,
            max_pods,
        )
        _add_pod_causes(causes, pod_diags, events)

    expected = _workload_expected(workload)
    ready = workload.get("ready_replicas")
    available = workload.get("available_replicas")
    updated = workload.get("updated_replicas")
    if not causes and expected is not None:
        if updated is not None and _to_int(updated) < _to_int(expected):
            _add_cause(
                causes,
                "RolloutBlocked",
                "工作负载 updatedReplicas 未达预期",
                0.68,
                [{"expected": expected, "updated_replicas": updated}],
                ["继续查看新版本 Pod 事件、调度和探针状态，确认卡住层级。"],
            )
        elif ready is not None and _to_int(ready) < _to_int(expected):
            _add_cause(
                causes,
                "ReplicasUnavailable",
                "工作负载 readyReplicas 未达预期",
                0.66,
                [{"expected": expected, "ready_replicas": ready}],
                ["按 Pod 状态机继续下钻 Pending、Waiting、Running but NotReady。"],
            )
        elif available is not None and _to_int(available) < _to_int(expected):
            _add_cause(
                causes,
                "MinReadySecondsWaiting",
                "Pod Ready 后尚未满足 available 条件",
                0.55,
                [{"expected": expected, "available_replicas": available, "min_ready_seconds": workload.get("min_ready_seconds")}],
                ["确认 minReadySeconds 和 Pod Ready 时间，若仍在窗口内可继续观察。"],
            )

    if not causes:
        _add_cause(
            causes,
            "HealthyOrConverging",
            "工作负载发布状态未发现明确异常",
            0.7,
            [{"funnel": funnel}],
            ["如果业务仍不可用，转向 network-failure-diagnoser 或 root-cause-analyzer 检查访问链路和依赖。"],
        )

    causes.sort(key=lambda cause: cause.get("confidence", 0), reverse=True)
    for index, cause in enumerate(causes[:3], start=1):
        cause["rank"] = index

    top_cause = causes[0]
    status_map = {
        "ControlPlaneNotObserved": "control_plane_not_observed",
        "ReplicaSetCreateBlocked": "new_version_not_created",
        "QuotaOrAdmissionRejected": "new_version_not_created",
        "ContainerCommandNotFound": "rollout_blocked",
        "RolloutTimeout": "rollout_blocked",
        "RolloutBlocked": "rollout_blocked",
        "ReplicasUnavailable": "replicas_unavailable",
        "ProbeFailure": "probe_failure",
        "HealthyOrConverging": "healthy",
    }
    summary_status = status_map.get(top_cause["type"], "rollout_blocked")
    headline = _summary_headline(top_cause, workload, expected, ready, available, updated)

    return {
        "summary": {
            "status": summary_status,
            "headline": headline,
            "expected_replicas": expected,
            "ready_replicas": ready,
            "available_replicas": available,
            "top_cause": top_cause["type"],
        },
        "generation_check": generation_check,
        "version": {key: value for key, value in version.items() if key != "new_pods"},
        "funnel": funnel,
        "pod_diagnosis": {
            "diagnosed_pods": len(pod_diags),
            "pods": pod_diags,
        },
        "top_causes": causes[:3],
        "handoff": _handoff_for_causes(causes[:3]),
        "warnings": warnings,
    }


def _summary_headline(
    top_cause: Dict[str, Any],
    workload: Dict[str, Any],
    expected: Optional[int],
    ready: Optional[int],
    available: Optional[int],
    updated: Optional[int],
) -> str:
    headline = top_cause["title"]
    if top_cause.get("type") == "HealthyOrConverging":
        return headline
    if workload.get("kind") == "Deployment" and expected is not None:
        old_version_available = (
            (ready is not None and _to_int(ready) >= _to_int(expected))
            or (available is not None and _to_int(available) >= _to_int(expected))
        )
        rollout_incomplete = updated is not None and _to_int(updated) < _to_int(expected)
        if old_version_available and rollout_incomplete:
            return f"{headline}，Deployment rollout 卡住；旧版本副本仍保持可用"
    return headline


def _handoff_for_causes(causes: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    handoff = []
    mapping = {
        "SchedulingBlocked": ("node-failure-diagnoser", "调度失败可能与节点资源、污点或亲和性有关"),
        "StorageMountBlocked": ("pod-failure-diagnoser", "存储挂载需继续查看 Pod/PVC/PV 事件"),
        "ImagePullBlocked": ("pod-failure-diagnoser", "镜像拉取失败需查看镜像地址、SWR 权限和节点网络"),
        "ContainerCommandNotFound": ("pod-failure-diagnoser", "容器启动命令不存在，需核对 command/args 和镜像入口"),
        "CrashLoopOrAppExit": ("pod-failure-diagnoser", "容器启动失败需继续查看 previous/current logs"),
        "OOMKilled": ("pod-failure-diagnoser", "OOM 需结合 Pod 指标和日志判断资源或泄漏问题"),
        "ProbeFailure": ("pod-failure-diagnoser", "探针失败需结合 Pod 日志和健康检查配置"),
        "ReplicasUnavailable": ("root-cause-analyzer", "副本不满足但当前证据不足，需要跨域收敛"),
        "ControlPlaneNotObserved": ("root-cause-analyzer", "控制面未响应需结合告警和集群组件压力分析"),
        "QuotaOrAdmissionRejected": ("auto-remediation-runner", "如需调整配额或资源规格，先生成恢复预案"),
    }
    seen = set()
    for cause in causes:
        item = mapping.get(cause.get("type"))
        if not item or item[0] in seen:
            continue
        handoff.append({"skill": item[0], "reason": item[1]})
        seen.add(item[0])
    return handoff


def _diagnostic_event_timeline(events: List[Dict[str, Any]], limit: int = 20) -> List[Dict[str, Any]]:
    important_reasons = {
        "BackOff",
        "BackOffStart",
        "ErrImagePull",
        "Failed",
        "FailedCreate",
        "FailedMount",
        "FailedScheduling",
        "FailedStart",
        "Unhealthy",
    }
    selected = [
        event for event in events
        if event.get("type") == "Warning" or event.get("reason") in important_reasons
    ]
    return (selected or events)[:limit]


def get_workload_rollout_context(
    region: str,
    cluster_id: str,
    namespace: str,
    kind: str,
    name: str,
    event_limit: int = 500,
    label_selector: Optional[str] = None,
    ak: Optional[str] = None,
    sk: Optional[str] = None,
    project_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Collect Workload, ReplicaSet, Pod, and UID-filtered Event context for rollout diagnosis."""
    canonical_kind = _kind(kind)
    if not canonical_kind:
        return {"success": False, "error": "kind must be Deployment, StatefulSet, or DaemonSet"}

    access_key, secret_key, proj_id = get_credentials(ak, sk, project_id)
    if not access_key or not secret_key:
        return {"success": False, "error": "Credentials not provided. Set HUAWEI_AK and HUAWEI_SK environment variables or pass as parameters."}
    if not cluster_id:
        return {"success": False, "error": "cluster_id is required"}
    if not namespace:
        return {"success": False, "error": "namespace is required"}
    if not name:
        return {"success": False, "error": "name is required"}
    if not K8S_AVAILABLE:
        return {"success": False, "error": f"Kubernetes SDK not installed: {K8S_IMPORT_ERROR}"}
    if not SDK_AVAILABLE:
        return {"success": False, "error": f"Huawei Cloud SDK not installed: {IMPORT_ERROR}"}

    cert_file = None
    key_file = None
    warnings: List[Dict[str, Any]] = []
    try:
        _, cert_file, key_file = cce_k8s._setup_k8s_client(region, cluster_id, access_key, secret_key, proj_id, "rollout")
        apps_v1 = k8s_client.AppsV1Api()
        core_v1 = k8s_client.CoreV1Api()

        workload_obj = _read_workload(apps_v1, namespace, canonical_kind, name)
        workload = _serialize_workload(workload_obj, canonical_kind)

        selector = label_selector or (workload.get("selector") or {}).get("label_selector")
        if label_selector:
            selector_source = "override"
        else:
            selector_source = "matchLabels"
        if not selector:
            warnings.append({"stage": "selector", "message": "workload selector.matchLabels is empty; related pods may be incomplete"})

        pods = _list_pods(core_v1, namespace, selector)
        replicasets: List[Dict[str, Any]] = []
        if canonical_kind == "Deployment":
            replicasets = _list_replicasets(apps_v1, namespace, selector, workload.get("uid"))

        raw_events = _list_events(core_v1, namespace, event_limit)
        uid_set = [workload.get("uid")]
        uid_set.extend(rs.get("uid") for rs in replicasets)
        uid_set.extend(pod.get("uid") for pod in pods)
        events, event_filter = _filter_events_by_uid(raw_events, uid_set)
        if event_filter["events_without_involved_uid"]:
            warnings.append({
                "stage": "event_filter",
                "message": "some events were skipped because involvedObject.uid was missing",
                "count": event_filter["events_without_involved_uid"],
            })

        return {
            "success": True,
            "action": "get_workload_rollout_context",
            "region": region,
            "cluster_id": cluster_id,
            "target": {
                "namespace": namespace,
                "kind": canonical_kind,
                "name": name,
            },
            "selector": {
                "value": selector,
                "source": selector_source,
            },
            "workload": workload,
            "replicasets": replicasets,
            "pods": pods,
            "events": events,
            "event_filter": event_filter,
            "warnings": warnings,
        }
    except Exception as exc:
        return {
            "success": False,
            "error": str(exc),
            "error_type": type(exc).__name__,
            "stage": "get_workload_rollout_context",
        }
    finally:
        _safe_delete_file(cert_file)
        _safe_delete_file(key_file)


def workload_rollout_diagnose(
    region: str,
    cluster_id: str,
    namespace: str,
    kind: str,
    name: str,
    include_pod_diagnosis: bool = True,
    include_logs: bool = True,
    include_metrics: bool = False,
    tail_lines: int = 80,
    hours: int = 1,
    max_pods: int = 20,
    event_limit: int = 500,
    label_selector: Optional[str] = None,
    ak: Optional[str] = None,
    sk: Optional[str] = None,
    project_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Diagnose CCE workload rollout and replica availability failures."""
    context = get_workload_rollout_context(
        region=region,
        cluster_id=cluster_id,
        namespace=namespace,
        kind=kind,
        name=name,
        event_limit=event_limit,
        label_selector=label_selector,
        ak=ak,
        sk=sk,
        project_id=project_id,
    )
    if not context.get("success"):
        return context

    analysis = analyze_rollout_context(
        context,
        include_pod_diagnosis=include_pod_diagnosis,
        include_logs=include_logs,
        include_metrics=include_metrics,
        region=region,
        cluster_id=cluster_id,
        ak=ak,
        sk=sk,
        project_id=project_id,
        tail_lines=tail_lines,
        hours=hours,
        max_pods=max_pods,
    )

    return {
        "success": True,
        "action": "workload_rollout_diagnose",
        "region": region,
        "cluster_id": cluster_id,
        "target": context.get("target"),
        "selector": context.get("selector"),
        "summary": analysis["summary"],
        "generation_check": analysis["generation_check"],
        "workload": context.get("workload"),
        "version": analysis["version"],
        "funnel": analysis["funnel"],
        "events": {
            "filtered_count": len(context.get("events") or []),
            "timeline": _diagnostic_event_timeline(context.get("events") or []),
            "filter": context.get("event_filter"),
        },
        "pod_diagnosis": analysis["pod_diagnosis"],
        "top_causes": analysis["top_causes"],
        "handoff": analysis["handoff"],
        "warnings": (context.get("warnings") or []) + analysis["warnings"],
    }
