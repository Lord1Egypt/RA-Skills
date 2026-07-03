"""CCE network failure diagnosis with Kubernetes evidence and Markdown output."""

from __future__ import annotations

import re
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Iterable, List, Optional, Tuple

from . import elb, network
from .cce_k8s import _setup_k8s_client
from .common import (
    IMPORT_ERROR,
    K8S_AVAILABLE,
    K8S_IMPORT_ERROR,
    SDK_AVAILABLE,
    _safe_delete_file,
    get_credentials_with_region,
    k8s_client,
)


DNS_SYMPTOMS = ("dns", "domain", "resolve", "解析", "域名", "nxdomain")
EAST_WEST_SYMPTOMS = ("service", "svc", "集群内", "东西向", "偶现", "抖动", "timeout", "connection refused")
NORTH_SOUTH_SYMPTOMS = ("ingress", "elb", "eip", "external", "公网", "外部", "502", "503", "504", "南北向")
ERROR_LOG_RE = re.compile(
    r"(?i)(error|timeout|timed out|nxdomain|i/o timeout|bad gateway|gateway timeout|"
    r"connection refused|outofmemory|out of memory|pool exhausted)"
)
INGRESS_UPSTREAM_ERROR_RE = re.compile(
    r"(?i)("
    r"\bstatus[=:\s\"']+(?:502|503|504)\b|"
    r"\bHTTP/\d(?:\.\d)?\"?\s+(?:502|503|504)\b|"
    r"\b(?:502|503|504)\s+(?:bad gateway|service unavailable|gateway timeout)\b|"
    r"bad gateway|gateway timeout|upstream timed out|connect\(\) failed|"
    r"no live upstreams|upstream prematurely closed"
    r")"
)
SECRET_PATTERNS = [
    re.compile(r"(?i)(authorization:\s*bearer\s+)[A-Za-z0-9._~+/=-]+"),
    re.compile(r"(?i)((?:password|passwd|token|secret|access[_-]?key|secret[_-]?key)\s*[=:]\s*)\S+"),
    re.compile(r"(?i)(x-auth-token\s*[=:]\s*)\S+"),
]


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


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


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


def _k8s_ts(value: Any) -> Optional[str]:
    return str(value) if value else None


def _mask_secrets(text: str) -> str:
    masked = text or ""
    for pattern in SECRET_PATTERNS:
        masked = pattern.sub(r"\1***", masked)
    return masked


def _md_cell(value: Any, max_len: int = 180) -> str:
    if value is None or value == "":
        return "-"
    text = str(value).replace("\n", " ").replace("|", "\\|").strip()
    if len(text) > max_len:
        return f"{text[: max_len - 3]}..."
    return text


def _obj_meta(obj: Any) -> Any:
    return getattr(obj, "metadata", None)


def _dict_or_empty(value: Any) -> Dict[str, Any]:
    return dict(value or {})


def _selector_to_dict(selector: Any) -> Dict[str, Any]:
    if not selector:
        return {}
    if hasattr(selector, "to_dict"):
        data = selector.to_dict() or {}
    else:
        data = {
            "match_labels": getattr(selector, "match_labels", None),
            "match_expressions": getattr(selector, "match_expressions", None),
        }
    return {
        "match_labels": data.get("match_labels") or data.get("matchLabels") or {},
        "match_expressions": data.get("match_expressions") or data.get("matchExpressions") or [],
    }


def _selector_matches(labels: Dict[str, str], selector: Dict[str, Any]) -> bool:
    if not selector:
        return True
    labels = labels or {}
    for key, value in (selector.get("match_labels") or {}).items():
        if labels.get(key) != value:
            return False
    for expr in selector.get("match_expressions") or []:
        key = expr.get("key")
        operator = expr.get("operator")
        values = expr.get("values") or []
        current = labels.get(key)
        if operator == "In" and current not in values:
            return False
        if operator == "NotIn" and current in values:
            return False
        if operator == "Exists" and key not in labels:
            return False
        if operator == "DoesNotExist" and key in labels:
            return False
    return True


def _condition_status(conditions: Iterable[Dict[str, Any]], condition_type: str) -> Optional[str]:
    for condition in conditions or []:
        if condition.get("type") == condition_type:
            return condition.get("status")
    return None


def _pod_ready(pod: Dict[str, Any]) -> bool:
    if _condition_status(pod.get("conditions") or [], "Ready") == "True":
        return True
    containers = pod.get("containers") or []
    return bool(containers) and all(container.get("ready") for container in containers)


def _pod_to_dict(pod: Any) -> Dict[str, Any]:
    metadata = _obj_meta(pod)
    spec = getattr(pod, "spec", None)
    status = getattr(pod, "status", None)
    containers = []
    for cs in getattr(status, "container_statuses", None) or []:
        state = getattr(cs, "state", None)
        waiting = getattr(state, "waiting", None) if state else None
        terminated = getattr(state, "terminated", None) if state else None
        last_state = getattr(cs, "last_state", None)
        last_terminated = getattr(last_state, "terminated", None) if last_state else None
        containers.append({
            "name": getattr(cs, "name", None),
            "ready": getattr(cs, "ready", None),
            "restart_count": getattr(cs, "restart_count", 0),
            "waiting_reason": getattr(waiting, "reason", None),
            "waiting_message": getattr(waiting, "message", None),
            "terminated_reason": getattr(terminated, "reason", None),
            "last_terminated_reason": getattr(last_terminated, "reason", None),
            "last_exit_code": getattr(last_terminated, "exit_code", None),
        })

    conditions = []
    for condition in getattr(status, "conditions", None) or []:
        conditions.append({
            "type": getattr(condition, "type", None),
            "status": getattr(condition, "status", None),
            "reason": getattr(condition, "reason", None),
            "message": getattr(condition, "message", None),
        })

    dns_config = getattr(spec, "dns_config", None)
    return {
        "name": getattr(metadata, "name", None),
        "namespace": getattr(metadata, "namespace", None),
        "labels": _dict_or_empty(getattr(metadata, "labels", None)),
        "annotations": _dict_or_empty(getattr(metadata, "annotations", None)),
        "phase": getattr(status, "phase", None),
        "reason": getattr(status, "reason", None),
        "message": getattr(status, "message", None),
        "pod_ip": getattr(status, "pod_ip", None),
        "host_ip": getattr(status, "host_ip", None),
        "node": getattr(spec, "node_name", None),
        "created": _k8s_ts(getattr(metadata, "creation_timestamp", None)),
        "dns_policy": getattr(spec, "dns_policy", None),
        "dns_config": {
            "nameservers": list(getattr(dns_config, "nameservers", None) or []),
            "searches": list(getattr(dns_config, "searches", None) or []),
        } if dns_config else None,
        "conditions": conditions,
        "containers": containers,
        "ready": _condition_status(conditions, "Ready") == "True",
    }


def _node_to_dict(node: Any) -> Dict[str, Any]:
    metadata = _obj_meta(node)
    status = getattr(node, "status", None)
    conditions = []
    ready = "Unknown"
    for condition in getattr(status, "conditions", None) or []:
        item = {
            "type": getattr(condition, "type", None),
            "status": getattr(condition, "status", None),
            "reason": getattr(condition, "reason", None),
            "message": getattr(condition, "message", None),
            "last_transition_time": _k8s_ts(getattr(condition, "last_transition_time", None)),
        }
        conditions.append(item)
        if item["type"] == "Ready":
            ready = item["status"]

    internal_ip = None
    for address in getattr(status, "addresses", None) or []:
        if getattr(address, "type", None) == "InternalIP":
            internal_ip = getattr(address, "address", None)
            break

    return {
        "name": getattr(metadata, "name", None),
        "labels": _dict_or_empty(getattr(metadata, "labels", None)),
        "internal_ip": internal_ip,
        "ready": ready,
        "conditions": conditions,
    }


def _service_to_dict(service: Any) -> Dict[str, Any]:
    metadata = _obj_meta(service)
    spec = getattr(service, "spec", None)
    status = getattr(service, "status", None)
    ports = []
    for port in getattr(spec, "ports", None) or []:
        ports.append({
            "name": getattr(port, "name", None),
            "protocol": getattr(port, "protocol", None),
            "port": getattr(port, "port", None),
            "target_port": getattr(port, "target_port", None),
            "node_port": getattr(port, "node_port", None),
        })
    lb_ingress = []
    lb_status = getattr(status, "load_balancer", None)
    for item in getattr(lb_status, "ingress", None) or []:
        lb_ingress.append({"ip": getattr(item, "ip", None), "hostname": getattr(item, "hostname", None)})
    return {
        "name": getattr(metadata, "name", None),
        "namespace": getattr(metadata, "namespace", None),
        "labels": _dict_or_empty(getattr(metadata, "labels", None)),
        "annotations": _dict_or_empty(getattr(metadata, "annotations", None)),
        "type": getattr(spec, "type", None),
        "cluster_ip": getattr(spec, "cluster_ip", None),
        "selector": _dict_or_empty(getattr(spec, "selector", None)),
        "ports": ports,
        "load_balancer_ingress": lb_ingress,
    }


def _ingress_to_dict(ingress: Any) -> Dict[str, Any]:
    metadata = _obj_meta(ingress)
    spec = getattr(ingress, "spec", None)
    status = getattr(ingress, "status", None)
    rules = []
    for rule in getattr(spec, "rules", None) or []:
        paths = []
        http = getattr(rule, "http", None)
        for path in getattr(http, "paths", None) or []:
            backend = getattr(path, "backend", None)
            svc = getattr(backend, "service", None) if backend else None
            port = getattr(svc, "port", None) if svc else None
            paths.append({
                "path": getattr(path, "path", None),
                "path_type": getattr(path, "path_type", None),
                "service_name": getattr(svc, "name", None),
                "service_port": getattr(port, "number", None) or getattr(port, "name", None),
            })
        rules.append({"host": getattr(rule, "host", None), "paths": paths})
    lb_ingress = []
    lb_status = getattr(status, "load_balancer", None)
    for item in getattr(lb_status, "ingress", None) or []:
        lb_ingress.append({"ip": getattr(item, "ip", None), "hostname": getattr(item, "hostname", None)})
    return {
        "name": getattr(metadata, "name", None),
        "namespace": getattr(metadata, "namespace", None),
        "labels": _dict_or_empty(getattr(metadata, "labels", None)),
        "annotations": _dict_or_empty(getattr(metadata, "annotations", None)),
        "ingress_class_name": getattr(spec, "ingress_class_name", None),
        "rules": rules,
        "load_balancer_ingress": lb_ingress,
    }


def _endpoint_slice_to_dict(endpoint_slice: Any) -> Dict[str, Any]:
    metadata = _obj_meta(endpoint_slice)
    endpoints = []
    for endpoint in getattr(endpoint_slice, "endpoints", None) or []:
        conditions = getattr(endpoint, "conditions", None)
        target_ref = getattr(endpoint, "target_ref", None)
        endpoints.append({
            "addresses": list(getattr(endpoint, "addresses", None) or []),
            "ready": getattr(conditions, "ready", None),
            "serving": getattr(conditions, "serving", None),
            "terminating": getattr(conditions, "terminating", None),
            "node_name": getattr(endpoint, "node_name", None),
            "target_ref": {
                "kind": getattr(target_ref, "kind", None),
                "name": getattr(target_ref, "name", None),
                "namespace": getattr(target_ref, "namespace", None),
            } if target_ref else {},
        })
    ports = []
    for port in getattr(endpoint_slice, "ports", None) or []:
        ports.append({
            "name": getattr(port, "name", None),
            "protocol": getattr(port, "protocol", None),
            "port": getattr(port, "port", None),
        })
    return {
        "name": getattr(metadata, "name", None),
        "namespace": getattr(metadata, "namespace", None),
        "labels": _dict_or_empty(getattr(metadata, "labels", None)),
        "service_name": _dict_or_empty(getattr(metadata, "labels", None)).get("kubernetes.io/service-name"),
        "address_type": getattr(endpoint_slice, "address_type", None),
        "ports": ports,
        "endpoints": endpoints,
        "ready_endpoint_count": len([ep for ep in endpoints if ep.get("ready") is not False]),
    }


def _network_policy_to_dict(policy: Any) -> Dict[str, Any]:
    metadata = _obj_meta(policy)
    spec = getattr(policy, "spec", None)
    ingress_rules = []
    for rule in getattr(spec, "ingress", None) or []:
        peers = []
        for peer in getattr(rule, "_from", None) or getattr(rule, "from_", None) or []:
            ip_block = getattr(peer, "ip_block", None)
            peers.append({
                "pod_selector": _selector_to_dict(getattr(peer, "pod_selector", None)),
                "namespace_selector": _selector_to_dict(getattr(peer, "namespace_selector", None)),
                "ip_block": {
                    "cidr": getattr(ip_block, "cidr", None),
                    "except": list(getattr(ip_block, "_except", None) or []),
                } if ip_block else None,
            })
        ports = []
        for port in getattr(rule, "ports", None) or []:
            ports.append({
                "protocol": getattr(port, "protocol", None),
                "port": str(getattr(port, "port", None)) if getattr(port, "port", None) is not None else None,
                "end_port": getattr(port, "end_port", None),
            })
        ingress_rules.append({"from": peers, "ports": ports})
    return {
        "name": getattr(metadata, "name", None),
        "namespace": getattr(metadata, "namespace", None),
        "pod_selector": _selector_to_dict(getattr(spec, "pod_selector", None)),
        "policy_types": list(getattr(spec, "policy_types", None) or []),
        "ingress": ingress_rules,
    }


def _event_to_dict(event: Any) -> Dict[str, Any]:
    involved = getattr(event, "involved_object", None)
    source = getattr(event, "source", None)
    return {
        "name": getattr(_obj_meta(event), "name", None),
        "namespace": getattr(_obj_meta(event), "namespace", None),
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


def _list_events(v1: Any, namespace: str, event_limit: int, hours: int) -> List[Dict[str, Any]]:
    try:
        raw = v1.list_namespaced_event(namespace, limit=event_limit).items
    except Exception:
        return []
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
    events = [_event_to_dict(item) for item in raw]
    filtered = []
    for event in events:
        ts = _event_sort_key(event)
        if ts == datetime.min.replace(tzinfo=timezone.utc) or ts >= cutoff:
            filtered.append(event)
    return sorted(filtered, key=_event_sort_key, reverse=True)[:event_limit]


def _log_excerpt(logs: str, max_lines: int = 80, max_chars: int = 8000) -> str:
    selected = [line for line in (logs or "").splitlines() if ERROR_LOG_RE.search(line)]
    if not selected:
        selected = (logs or "").splitlines()[-min(max_lines, 20):]
    excerpt = "\n".join(selected[-max_lines:])
    return _mask_secrets(excerpt[-max_chars:])


def _read_pod_log_excerpt(v1: Any, pod: Dict[str, Any], tail_lines: int) -> Dict[str, Any]:
    try:
        logs = v1.read_namespaced_pod_log(
            name=pod["name"],
            namespace=pod["namespace"],
            follow=False,
            tail_lines=tail_lines,
        )
        return {"success": True, "excerpt": _log_excerpt(logs, tail_lines)}
    except Exception as exc:
        return {"success": False, "error": str(exc)}


def _safe_call(label: str, fn: Any, *args: Any, **kwargs: Any) -> Dict[str, Any]:
    try:
        result = fn(*args, **kwargs)
        if isinstance(result, dict):
            return result
        return {"success": True, "result": result}
    except Exception as exc:
        return {"success": False, "stage": label, "error": str(exc), "error_type": type(exc).__name__}


def _service_endpoints(snapshot: Dict[str, Any], service_name: str, namespace: str) -> List[Dict[str, Any]]:
    return [
        endpoint_slice
        for endpoint_slice in snapshot.get("endpoint_slices", [])
        if endpoint_slice.get("namespace") == namespace and endpoint_slice.get("service_name") == service_name
    ]


def _ready_endpoint_count(endpoint_slices: List[Dict[str, Any]]) -> int:
    count = 0
    for endpoint_slice in endpoint_slices:
        for endpoint in endpoint_slice.get("endpoints") or []:
            if endpoint.get("ready") is not False:
                count += 1
    return count


def _selected_pods_for_service(snapshot: Dict[str, Any], service: Dict[str, Any]) -> List[Dict[str, Any]]:
    selector = service.get("selector") or {}
    if not selector:
        return []
    return [
        pod
        for pod in snapshot.get("pods", [])
        if pod.get("namespace") == service.get("namespace")
        and all((pod.get("labels") or {}).get(key) == value for key, value in selector.items())
    ]


def _find_service(snapshot: Dict[str, Any], service_name: Optional[str], namespace: str) -> Optional[Dict[str, Any]]:
    if not service_name:
        return None
    for service in snapshot.get("services", []):
        if service.get("namespace") == namespace and service.get("name") == service_name:
            return service
    return None


def _find_pod(snapshot: Dict[str, Any], pod_name: Optional[str], namespace: Optional[str] = None) -> Optional[Dict[str, Any]]:
    if not pod_name:
        return None
    for pod in snapshot.get("pods", []):
        if pod.get("name") == pod_name and (not namespace or pod.get("namespace") == namespace):
            return pod
    return None


def _infer_service_from_ingress(snapshot: Dict[str, Any], ingress_name: Optional[str], domain: Optional[str], namespace: str) -> Tuple[Optional[Dict[str, Any]], Optional[Dict[str, Any]]]:
    ingresses = [
        ing
        for ing in snapshot.get("ingresses", [])
        if ing.get("namespace") == namespace
        and (not ingress_name or ing.get("name") == ingress_name)
    ]
    if domain:
        ingresses = [
            ing for ing in ingresses
            if any(rule.get("host") == domain for rule in ing.get("rules") or [])
        ] or ingresses
    for ingress in ingresses:
        for rule in ingress.get("rules") or []:
            for path in rule.get("paths") or []:
                service = _find_service(snapshot, path.get("service_name"), namespace)
                if service:
                    return ingress, service
        return ingress, None
    return None, None


def _infer_service_from_pod(snapshot: Dict[str, Any], pod: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    if not pod:
        return None
    pod_labels = pod.get("labels") or {}
    for service in snapshot.get("services", []):
        if service.get("namespace") != pod.get("namespace"):
            continue
        selector = service.get("selector") or {}
        if selector and all(pod_labels.get(key) == value for key, value in selector.items()):
            return service
    return None


def _extract_elb_ids(*objects: Optional[Dict[str, Any]]) -> List[str]:
    ids = []
    keys = (
        "kubernetes.io/elb.id",
        "kubernetes.io/elb.ids",
        "elb.id",
        "elb.openstack.org/id",
    )
    for obj in objects:
        if not obj:
            continue
        annotations = obj.get("annotations") or {}
        for key in keys:
            value = annotations.get(key)
            if value:
                ids.extend([item.strip() for item in str(value).split(",") if item.strip()])
    result = []
    for item in ids:
        if item not in result:
            result.append(item)
    return result


def _load_balancer_ips(*objects: Optional[Dict[str, Any]]) -> List[str]:
    ips = []
    for obj in objects:
        if not obj:
            continue
        for item in obj.get("load_balancer_ingress") or []:
            ip = item.get("ip")
            if ip and ip not in ips:
                ips.append(ip)
    return ips


def _symptom_flags(symptom: Optional[str]) -> Dict[str, bool]:
    text = (symptom or "").lower()
    return {
        "dns": any(key in text for key in DNS_SYMPTOMS),
        "east_west": any(key in text for key in EAST_WEST_SYMPTOMS),
        "north_south": any(key in text for key in NORTH_SOUTH_SYMPTOMS),
    }


def _collect_k8s_snapshot(
    region: str,
    cluster_id: str,
    namespace: str,
    access_key: str,
    secret_key: str,
    project_id: Optional[str],
    target_name: Optional[str],
    target_kind: Optional[str],
    service_name: Optional[str],
    ingress_name: Optional[str],
    source_pod: Optional[str],
    destination_pod: Optional[str],
    domain: Optional[str],
    failure_symptom: Optional[str],
    include_logs: bool,
    tail_lines: int,
    event_limit: int,
    hours: int,
) -> Dict[str, Any]:
    _, cert_file, key_file = _setup_k8s_client(region, cluster_id, access_key, secret_key, project_id, "network_failure")
    try:
        v1 = k8s_client.CoreV1Api()
        networking_v1 = k8s_client.NetworkingV1Api()
        discovery_v1 = k8s_client.DiscoveryV1Api()

        pods = [_pod_to_dict(item) for item in v1.list_namespaced_pod(namespace).items]
        kube_system_pods = [_pod_to_dict(item) for item in v1.list_namespaced_pod("kube-system").items]
        pods_by_key = {(pod["namespace"], pod["name"]): pod for pod in [*pods, *kube_system_pods]}
        pods = list(pods_by_key.values())

        services = [_service_to_dict(item) for item in v1.list_namespaced_service(namespace).items]
        kube_system_services = [_service_to_dict(item) for item in v1.list_namespaced_service("kube-system").items]
        endpoint_slices = [_endpoint_slice_to_dict(item) for item in discovery_v1.list_namespaced_endpoint_slice(namespace).items]
        kube_system_endpoint_slices = [
            _endpoint_slice_to_dict(item) for item in discovery_v1.list_namespaced_endpoint_slice("kube-system").items
        ]
        ingresses = [_ingress_to_dict(item) for item in networking_v1.list_namespaced_ingress(namespace).items]
        netpols = [_network_policy_to_dict(item) for item in networking_v1.list_namespaced_network_policy(namespace).items]
        nodes = [_node_to_dict(item) for item in v1.list_node().items]
        namespaces = [
            {
                "name": getattr(_obj_meta(item), "name", None),
                "labels": _dict_or_empty(getattr(_obj_meta(item), "labels", None)),
            }
            for item in v1.list_namespace().items
        ]
        events = [*_list_events(v1, namespace, event_limit, hours), *_list_events(v1, "kube-system", event_limit, hours)]

        coredns_pods = [
            pod for pod in pods
            if pod.get("namespace") == "kube-system"
            and (
                "coredns" in (pod.get("name") or "").lower()
                or (pod.get("labels") or {}).get("k8s-app") == "kube-dns"
                or (pod.get("labels") or {}).get("k8s-app") == "coredns"
            )
        ]
        ingress_controller_pods = [
            pod for pod in pods
            if "ingress" in (pod.get("name") or "").lower()
            or "nginx" in (pod.get("labels") or {}).get("app.kubernetes.io/name", "").lower()
            or "ingress" in (pod.get("labels") or {}).get("app", "").lower()
        ]

        snapshot: Dict[str, Any] = {
            "inputs": {
                "region": region,
                "cluster_id": cluster_id,
                "namespace": namespace,
                "target_kind": target_kind,
                "target_name": target_name,
                "service_name": service_name,
                "ingress_name": ingress_name,
                "source_pod": source_pod,
                "destination_pod": destination_pod,
                "domain": domain,
                "failure_symptom": failure_symptom,
            },
            "collected_at": _now_iso(),
            "nodes": nodes,
            "namespaces": namespaces,
            "pods": pods,
            "services": [*services, *kube_system_services],
            "ingresses": ingresses,
            "endpoint_slices": [*endpoint_slices, *kube_system_endpoint_slices],
            "network_policies": netpols,
            "events": sorted(events, key=_event_sort_key, reverse=True)[:event_limit],
            "system": {
                "coredns_pods": coredns_pods,
                "ingress_controller_pods": ingress_controller_pods,
            },
            "logs": {},
        }

        target_pod = None
        if target_kind and str(target_kind).lower() == "pod":
            target_pod = _find_pod(snapshot, target_name, namespace)
        source = _find_pod(snapshot, source_pod, namespace)
        destination = _find_pod(snapshot, destination_pod, namespace) or target_pod
        target_service = _find_service(snapshot, service_name, namespace)
        target_ingress = None
        if not target_service:
            if target_kind and str(target_kind).lower() in {"service", "svc"}:
                target_service = _find_service(snapshot, target_name, namespace)
            if not target_service:
                target_ingress, target_service = _infer_service_from_ingress(snapshot, ingress_name, domain, namespace)
            if not target_service:
                target_service = _infer_service_from_pod(snapshot, destination)
        if not target_ingress:
            target_ingress, inferred_service = _infer_service_from_ingress(snapshot, ingress_name, domain, namespace)
            if not target_service:
                target_service = inferred_service
        if not destination and target_service:
            selected = _selected_pods_for_service(snapshot, target_service)
            destination = selected[0] if selected else None

        snapshot["target"] = {
            "service": target_service,
            "ingress": target_ingress,
            "source_pod": source,
            "destination_pod": destination,
            "backend_pods": _selected_pods_for_service(snapshot, target_service) if target_service else [],
        }

        if include_logs:
            log_targets = []
            log_targets.extend(coredns_pods[:3])
            log_targets.extend(ingress_controller_pods[:3])
            for pod in [source, destination, *snapshot["target"]["backend_pods"][:3]]:
                if pod and pod not in log_targets:
                    log_targets.append(pod)
            for pod in log_targets[:10]:
                key = f"{pod.get('namespace')}/{pod.get('name')}"
                snapshot["logs"][key] = _read_pod_log_excerpt(v1, pod, tail_lines)

        return snapshot
    finally:
        _safe_delete_file(cert_file)
        _safe_delete_file(key_file)


def _collect_cloud_context(
    region: str,
    service: Optional[Dict[str, Any]],
    ingress: Optional[Dict[str, Any]],
    elb_id: Optional[str],
    access_key: str,
    secret_key: str,
    project_id: Optional[str],
    hours: int,
) -> Dict[str, Any]:
    elb_ids = _extract_elb_ids(service, ingress)
    if elb_id and elb_id not in elb_ids:
        elb_ids.insert(0, elb_id)
    lb_ips = _load_balancer_ips(service, ingress)

    elb_inventory = _safe_call(
        "list_elb",
        elb.list_elb_loadbalancers,
        region,
        ak=access_key,
        sk=secret_key,
        project_id=project_id,
        limit=200,
    )
    if lb_ips and elb_inventory.get("success"):
        for loadbalancer in elb_inventory.get("loadbalancers") or []:
            eip_info = loadbalancer.get("eip_info") or {}
            addresses = {
                loadbalancer.get("vip_address"),
                loadbalancer.get("eip_address"),
                eip_info.get("eip"),
            }
            if any(ip in addresses for ip in lb_ips):
                matched_id = loadbalancer.get("id")
                if matched_id and matched_id not in elb_ids:
                    elb_ids.append(matched_id)

    result: Dict[str, Any] = {
        "elb_ids": elb_ids,
        "load_balancer_ips": lb_ips,
        "elb_inventory": elb_inventory,
        "elbs": {},
        "eips": {},
        "nat": {},
        "security_groups": {},
        "vpc_acls": {},
    }
    for item in elb_ids[:5]:
        backend_status = _safe_call(
            "get_elb_backend_status",
            getattr(elb, "get_elb_backend_status", lambda *a, **kw: {"success": False, "error": "get_elb_backend_status unavailable"}),
            region,
            item,
            ak=access_key,
            sk=secret_key,
            project_id=project_id,
        )
        metrics = _safe_call("get_elb_metrics", elb.get_elb_metrics, region, item, hours=hours, ak=access_key, sk=secret_key, project_id=project_id)
        result["elbs"][item] = {"backend_status": backend_status, "metrics": metrics}

    result["eips"] = _safe_call("list_eip", network.list_eip_addresses, region, ak=access_key, sk=secret_key, project_id=project_id)
    result["nat"] = _safe_call("list_nat", network.list_nat_gateways, region, ak=access_key, sk=secret_key, project_id=project_id)
    result["security_groups"] = _safe_call("list_security_groups", network.list_security_groups, region, ak=access_key, sk=secret_key, project_id=project_id)
    result["vpc_acls"] = _safe_call("list_vpc_acls", network.list_vpc_acls, region, ak=access_key, sk=secret_key, project_id=project_id)
    return result


def _event_text(event: Dict[str, Any]) -> str:
    return " ".join(str(event.get(key) or "") for key in ("reason", "message", "source")).lower()


def _events_for_names(snapshot: Dict[str, Any], names: Iterable[str]) -> List[Dict[str, Any]]:
    name_set = {name for name in names if name}
    selected = []
    for event in snapshot.get("events") or []:
        involved = event.get("involved_object") or {}
        if involved.get("name") in name_set or any(name in _event_text(event) for name in name_set):
            selected.append(event)
    return selected


def _add_finding(
    findings: List[Dict[str, Any]],
    stage: str,
    finding_type: str,
    title: str,
    confidence: float,
    severity: str,
    evidence: List[Dict[str, Any]],
    recommendation: List[str],
    prune: bool = False,
) -> None:
    findings.append({
        "stage": stage,
        "type": finding_type,
        "title": title,
        "confidence": confidence,
        "severity": severity,
        "evidence": evidence[:10],
        "recommendation": recommendation,
        "prune": prune,
    })


def _check_nodes(snapshot: Dict[str, Any], findings: List[Dict[str, Any]]) -> bool:
    stage = "第一阶段：基础设施与节点层诊断"
    target = snapshot.get("target") or {}
    pods = [pod for pod in [target.get("source_pod"), target.get("destination_pod"), *target.get("backend_pods", [])] if pod]
    pod_nodes = {pod.get("node") for pod in pods if pod.get("node")}
    node_by_name = {node.get("name"): node for node in snapshot.get("nodes") or []}
    related_nodes = [node_by_name[name] for name in pod_nodes if name in node_by_name]
    if not related_nodes:
        return False

    for node in related_nodes:
        ready = node.get("ready")
        conditions = {condition.get("type"): condition for condition in node.get("conditions") or []}
        if ready in {"False", "Unknown"}:
            events = _events_for_names(snapshot, [node.get("name")])
            _add_finding(
                findings,
                stage,
                "NodeUnhealthy",
                "目标链路所在节点 NotReady/Unknown，优先判断为节点底座故障引发网络中断",
                0.96,
                "critical",
                [{"node": node.get("name"), "ready": ready, "conditions": node.get("conditions")}, *events[:5]],
                [
                    "先转交 node-failure-diagnoser 对该节点做 Ready/Lease/事件/指标诊断。",
                    "在节点恢复前暂停应用层 Service、Ingress 和 DNS 深挖，避免把底座故障误判为上层配置问题。",
                ],
                prune=True,
            )
            return True
        pressure = [
            name
            for name in ("MemoryPressure", "DiskPressure", "PIDPressure", "NetworkUnavailable")
            if (conditions.get(name) or {}).get("status") == "True"
        ]
        if pressure:
            events = [
                event for event in _events_for_names(snapshot, [node.get("name")])
                if any(key in _event_text(event) for key in ("oom", "kubeletnotready", "pressure", "evict"))
            ]
            _add_finding(
                findings,
                stage,
                "NodePressure",
                "目标链路所在节点存在资源或网络压力，可能导致网络组件/业务 Pod 抖动",
                0.86 if events else 0.72,
                "critical" if events else "warning",
                [{"node": node.get("name"), "pressure": pressure, "conditions": node.get("conditions")}, *events[:5]],
                [
                    "检查节点 CPU/内存/磁盘/网络指标以及 kubelet 事件。",
                    "如果压力与故障窗口重合，优先处理节点资源或 CNI 异常后再复测 Service/Ingress。",
                ],
                prune=bool(events),
            )
            return bool(events)
    return False


def _check_dns(snapshot: Dict[str, Any], findings: List[Dict[str, Any]], flags: Dict[str, bool]) -> None:
    if not flags["dns"]:
        return
    stage = "第二阶段：域名解析层诊断"
    target = snapshot.get("target") or {}
    client = target.get("source_pod") or target.get("destination_pod")
    if client and client.get("dns_policy") == "None" and not client.get("dns_config"):
        _add_finding(
            findings,
            stage,
            "PodDNSConfigMissing",
            "客户端 Pod 设置 dnsPolicy=None 但未配置 dnsConfig",
            0.98,
            "critical",
            [{"pod": f"{client.get('namespace')}/{client.get('name')}", "dns_policy": client.get("dns_policy"), "dns_config": client.get("dns_config")}],
            ["修正 Pod/工作负载 DNS 配置，使用 ClusterFirst 或显式补齐 nameserver/search/options。"],
        )

    kube_dns = _find_service(snapshot, "kube-dns", "kube-system")
    kube_dns_slices = _service_endpoints(snapshot, "kube-dns", "kube-system")
    if kube_dns and _ready_endpoint_count(kube_dns_slices) == 0:
        _add_finding(
            findings,
            stage,
            "KubeDnsNoEndpoint",
            "kube-dns Service 无可用 EndpointSlice 后端",
            0.95,
            "critical",
            [{"service": "kube-system/kube-dns", "endpoint_slices": kube_dns_slices, "coredns_pods": snapshot.get("system", {}).get("coredns_pods", [])}],
            ["检查 CoreDNS Pod 状态、调度节点和 coredns addon 状态；CoreDNS 后端恢复前集群 DNS 会持续失败。"],
        )

    coredns_names = [pod.get("name") for pod in snapshot.get("system", {}).get("coredns_pods", [])]
    coredns_events = _events_for_names(snapshot, coredns_names)
    restart_events = [
        event for event in coredns_events
        if any(key in _event_text(event) for key in ("oomkilled", "liveness probe failed", "unhealthy", "back-off"))
    ]
    if restart_events:
        _add_finding(
            findings,
            stage,
            "CoreDNSRestarting",
            "CoreDNS 近期存在 OOMKilled、探针失败或重启事件，可能造成解析抖动",
            0.88,
            "critical",
            restart_events[:8],
            ["扩展 CoreDNS 副本/资源或排查其所在节点压力，确认重启事件 count 不再增长后复测解析。"],
        )

    for key, log in (snapshot.get("logs") or {}).items():
        if "coredns" not in key.lower() or not log.get("success"):
            continue
        excerpt = log.get("excerpt") or ""
        lower = excerpt.lower()
        if "nxdomain" in lower:
            _add_finding(
                findings,
                stage,
                "CoreDNSNxDomain",
                "CoreDNS 日志出现 NXDOMAIN，优先怀疑服务名拼写或跨命名空间访问格式错误",
                0.82,
                "warning",
                [{"pod": key, "log_excerpt": excerpt[:1200]}],
                ["核对访问域名是否为 service.namespace.svc.cluster.local；跨命名空间访问必须带 namespace。"],
            )
        if "i/o timeout" in lower or "timeout" in lower:
            _add_finding(
                findings,
                stage,
                "CoreDNSUpstreamTimeout",
                "CoreDNS 转发上游 DNS 超时，可能是上游 DNS 或集群外网络故障",
                0.86,
                "critical",
                [{"pod": key, "log_excerpt": excerpt[:1200]}],
                ["检查 CoreDNS Corefile forward/upstream 配置、节点出网、安全组/ACL 和上游 DNS 可达性。"],
            )


def _port_allowed(rule_ports: List[Dict[str, Any]], service: Optional[Dict[str, Any]]) -> bool:
    if not rule_ports:
        return True
    service_ports = service.get("ports") if service else []
    desired = {str(port.get("port")) for port in service_ports or [] if port.get("port") is not None}
    desired.update(str(port.get("target_port")) for port in service_ports or [] if port.get("target_port") is not None)
    for rule_port in rule_ports:
        if rule_port.get("port") is None or str(rule_port.get("port")) in desired:
            return True
    return False


def _peer_allows_source(peer: Dict[str, Any], source: Optional[Dict[str, Any]], namespace_labels: Dict[str, Dict[str, str]]) -> bool:
    if not peer:
        return True
    if peer.get("ip_block"):
        return True
    if not source:
        return False
    pod_selector = peer.get("pod_selector") or {}
    namespace_selector = peer.get("namespace_selector") or {}
    pod_match = _selector_matches(source.get("labels") or {}, pod_selector) if pod_selector else True
    ns_labels = namespace_labels.get(source.get("namespace"), {})
    namespace_match = _selector_matches(ns_labels, namespace_selector) if namespace_selector else True
    return pod_match and namespace_match


def _network_policy_blocks(snapshot: Dict[str, Any], service: Optional[Dict[str, Any]], source: Optional[Dict[str, Any]], destination: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    if not destination:
        return None
    namespace_labels = {item.get("name"): item.get("labels") or {} for item in snapshot.get("namespaces") or []}
    selected = [
        policy for policy in snapshot.get("network_policies") or []
        if policy.get("namespace") == destination.get("namespace")
        and _selector_matches(destination.get("labels") or {}, policy.get("pod_selector") or {})
        and ("Ingress" in (policy.get("policy_types") or ["Ingress"]) or policy.get("ingress"))
    ]
    if not selected:
        return None
    for policy in selected:
        if not policy.get("ingress"):
            continue
        for rule in policy.get("ingress") or []:
            if not _port_allowed(rule.get("ports") or [], service):
                continue
            peers = rule.get("from") or []
            if not peers:
                return None
            if any(_peer_allows_source(peer, source, namespace_labels) for peer in peers):
                return None
    return {"policies": selected, "source_pod": source, "destination_pod": destination}


def _check_east_west(snapshot: Dict[str, Any], findings: List[Dict[str, Any]], flags: Dict[str, bool]) -> None:
    if flags["dns"] and not (flags["east_west"] or flags["north_south"]):
        return
    stage = "第三阶段：东西向路由与策略层诊断"
    target = snapshot.get("target") or {}
    service = target.get("service")
    source = target.get("source_pod")
    destination = target.get("destination_pod") or (target.get("backend_pods") or [None])[0]

    block = _network_policy_blocks(snapshot, service, source, destination)
    if block:
        _add_finding(
            findings,
            stage,
            "NetworkPolicyBlocked",
            "NetworkPolicy 选择了目标 Pod，但未放行源 Pod 标签或目标端口",
            1.0,
            "critical",
            [block],
            [
                "核对目标 Pod 命中的 NetworkPolicy ingress.from 与 ports。",
                "按最小权限补充源 Pod/namespace 标签或服务端口放行规则；变更前先输出策略 diff 和回滚方案。",
            ],
        )

    if service:
        endpoint_slices = _service_endpoints(snapshot, service.get("name"), service.get("namespace"))
        selected_pods = _selected_pods_for_service(snapshot, service)
        if _ready_endpoint_count(endpoint_slices) == 0:
            _add_finding(
                findings,
                stage,
                "ServiceNoReadyEndpoint",
                "Service 无可用 EndpointSlice 后端，流量无法转发到 Pod",
                0.95,
                "critical",
                [{"service": service, "endpoint_slices": endpoint_slices, "selector_matched_pods": selected_pods}],
                [
                    "核对 Service selector 与 Pod labels 是否一致。",
                    "如果 selector 已匹配，继续检查后端 Pod readinessProbe 和容器端口监听状态。",
                ],
            )
        elif not selected_pods and service.get("selector"):
            _add_finding(
                findings,
                stage,
                "ServiceSelectorMismatch",
                "Service selector 未匹配到任何目标 Pod",
                0.92,
                "critical",
                [{"service": service, "selector": service.get("selector")}],
                ["修正 Service selector 或工作负载 labels，确认 EndpointSlice 生成 ready endpoint。"],
            )

    backend_names = [pod.get("name") for pod in target.get("backend_pods") or []]
    backend_events = _events_for_names(snapshot, backend_names)
    readiness_events = [
        event for event in backend_events
        if "readiness probe failed" in _event_text(event) or event.get("reason") == "Unhealthy"
    ]
    if readiness_events:
        _add_finding(
            findings,
            stage,
            "ReadinessFlapping",
            "后端 Pod readinessProbe 在故障窗口内失败，可能导致偶现不通或抖动",
            0.84,
            "warning",
            readiness_events[:8],
            ["检查应用健康检查端点、依赖服务、GC/线程池/连接池耗尽和发布窗口，确认 readiness 失败事件不再增长。"],
        )

    for key, log in (snapshot.get("logs") or {}).items():
        if not log.get("success"):
            continue
        if backend_names and not any(name in key for name in backend_names):
            continue
        excerpt = log.get("excerpt") or ""
        lower = excerpt.lower()
        if "outofmemory" in lower or "out of memory" in lower or "pool exhausted" in lower or "connection pool" in lower:
            _add_finding(
                findings,
                stage,
                "BackendOverloaded",
                "后端应用日志出现 OOM 或连接池耗尽，偶现拒绝服务更可能来自应用自身过载",
                0.82,
                "warning",
                [{"pod": key, "log_excerpt": excerpt[:1200]}],
                ["结合 Pod CPU/内存指标、应用线程池/连接池配置和依赖服务慢请求继续定位。"],
            )


def _elb_has_unhealthy_backend(cloud: Dict[str, Any]) -> List[Dict[str, Any]]:
    unhealthy = []
    for elb_id, data in (cloud.get("elbs") or {}).items():
        status = data.get("backend_status") or {}
        if status.get("success"):
            for member in status.get("members") or []:
                operating = str(member.get("operating_status") or "").upper()
                if operating and operating not in {"ONLINE", "NORMAL", "NO_MONITOR"}:
                    unhealthy.append({"elb_id": elb_id, "member": member})
        metrics = data.get("metrics") or {}
        if metrics.get("success"):
            summary = metrics.get("summary") or {}
            abnormal = summary.get("abnormal_servers")
            if isinstance(abnormal, (int, float)) and abnormal > 0:
                unhealthy.append({"elb_id": elb_id, "metric": "abnormal_servers", "value": abnormal})
    return unhealthy


def _check_north_south(snapshot: Dict[str, Any], findings: List[Dict[str, Any]], flags: Dict[str, bool]) -> None:
    if not flags["north_south"]:
        return
    stage = "第四阶段：南北向边缘接入层诊断"
    target = snapshot.get("target") or {}
    service = target.get("service")
    ingress = target.get("ingress")
    cloud = snapshot.get("cloud") or {}

    lb_empty = False
    lb_obj = ingress or (service if service and service.get("type") == "LoadBalancer" else None)
    if lb_obj is not None:
        lb_empty = not lb_obj.get("load_balancer_ingress")
    if lb_empty:
        related_events = [
            event for event in snapshot.get("events") or []
            if any(key in _event_text(event) for key in ("loadbalancer", "elb", "quota", "permission", "forbidden", "failed"))
        ]
        _add_finding(
            findings,
            stage,
            "LoadBalancerProvisioningFailed",
            "Ingress/LoadBalancer Service 未获得 loadBalancer ingress 地址，云资源可能创建失败",
            0.9 if related_events else 0.76,
            "critical",
            [{"object": lb_obj}, *related_events[:8]],
            ["查看 CCM/CCE 事件中的配额、权限、子网、安全组或 ELB 创建失败信息，先修复云侧创建条件。"],
        )

    unhealthy = _elb_has_unhealthy_backend(cloud)
    backend_ready = bool(target.get("backend_pods")) and all(_pod_ready(pod) for pod in target.get("backend_pods") or [])
    if unhealthy:
        _add_finding(
            findings,
            stage,
            "ELBBackendUnhealthy",
            "ELB 后端健康检查异常；若 K8s Pod Ready，则优先怀疑安全组/NodePort/IPVS/Iptables 链路",
            0.9 if backend_ready else 0.78,
            "critical",
            [{"backend_ready_in_k8s": backend_ready, "unhealthy_backends": unhealthy[:10]}],
            [
                "核对 ELB 后端端口是否为 Service NodePort/容器端口预期值。",
                "检查节点安全组是否放行 ELB 到 NodePort/健康检查端口；如安全组无误，继续排查 kube-proxy/IPVS/Iptables 规则同步。",
            ],
        )

    for key, log in (snapshot.get("logs") or {}).items():
        lower_key = key.lower()
        if "ingress" not in lower_key and "nginx" not in lower_key:
            continue
        if not log.get("success"):
            continue
        excerpt = log.get("excerpt") or ""
        if INGRESS_UPSTREAM_ERROR_RE.search(excerpt):
            _add_finding(
                findings,
                stage,
                "IngressUpstreamError",
                "Ingress Controller 对目标域名/路径返回 502/504，问题位于 Ingress 到后端 Service/Pod 或后端应用响应",
                0.83,
                "critical",
                [{"pod": key, "log_excerpt": excerpt[:1200]}],
                ["核对 Ingress backend Service、EndpointSlice、后端应用响应时间和容器端口；若 Service/Endpoint 正常，重点排查应用超时或进程挂死。"],
            )


def assess_network_snapshot(snapshot: Dict[str, Any]) -> Dict[str, Any]:
    """Assess an already collected network snapshot and return findings plus conclusion data."""
    findings: List[Dict[str, Any]] = []
    flags = _symptom_flags(snapshot.get("inputs", {}).get("failure_symptom"))
    if not any(flags.values()):
        flags = {"dns": False, "east_west": True, "north_south": True}

    pruned = _check_nodes(snapshot, findings)
    if not pruned:
        _check_dns(snapshot, findings, flags)
        _check_east_west(snapshot, findings, flags)
        _check_north_south(snapshot, findings, flags)

    findings.sort(key=lambda item: (item.get("severity") == "critical", item.get("confidence", 0)), reverse=True)
    top_causes = findings[:3]
    if top_causes:
        conclusion = top_causes[0]["title"]
        confidence = "高 (High)" if top_causes[0]["confidence"] >= 0.9 else "中 (Medium)" if top_causes[0]["confidence"] >= 0.75 else "低 (Low)"
    else:
        conclusion = "未发现明确网络链路故障，需补充实时连通性测试或更精确故障窗口"
        confidence = "低 (Low)"

    return {
        "findings": findings,
        "top_causes": top_causes,
        "conclusion": conclusion,
        "confidence": confidence,
        "pipeline_pruned": pruned,
        "symptom_flags": flags,
    }


def _stage_rows(assessment: Dict[str, Any]) -> str:
    stages = [
        "第一阶段：基础设施与节点层诊断",
        "第二阶段：域名解析层诊断",
        "第三阶段：东西向路由与策略层诊断",
        "第四阶段：南北向边缘接入层诊断",
    ]
    rows = ["| 阶段 | 状态 | 命中结论 |", "| :--- | :--- | :--- |"]
    findings = assessment.get("findings") or []
    for stage in stages:
        matched = [item for item in findings if item.get("stage") == stage]
        if matched:
            status = "异常"
            title = matched[0].get("title")
        elif assessment.get("pipeline_pruned") and stage != stages[0]:
            status = "剪枝跳过"
            title = "底座故障已足以解释网络中断"
        else:
            status = "已检查"
            title = "未发现强异常"
        rows.append(f"| {stage} | {status} | {_md_cell(title, 240)} |")
    return "\n".join(rows)


def _evidence_rows(findings: List[Dict[str, Any]]) -> str:
    rows = ["| 阶段 | 严重度 | 类型 | 置信度 | 证据摘要 |", "| :--- | :--- | :--- | :--- | :--- |"]
    if not findings:
        rows.append("| - | - | - | - | 未命中明确异常证据 |")
        return "\n".join(rows)
    for item in findings:
        evidence = item.get("evidence") or []
        summary = evidence[0] if evidence else {}
        rows.append(
            "| {stage} | {severity} | `{typ}` | {confidence:.0%} | {evidence} |".format(
                stage=_md_cell(item.get("stage")),
                severity=_md_cell(item.get("severity")),
                typ=_md_cell(item.get("type")),
                confidence=float(item.get("confidence") or 0),
                evidence=_md_cell(summary, 260),
            )
        )
    return "\n".join(rows)


def _resource_summary(snapshot: Dict[str, Any]) -> str:
    target = snapshot.get("target") or {}
    service = target.get("service") or {}
    ingress = target.get("ingress") or {}
    backend_pods = target.get("backend_pods") or []
    endpoint_slices = _service_endpoints(snapshot, service.get("name"), service.get("namespace")) if service else []
    rows = ["| 对象 | 摘要 |", "| :--- | :--- |"]
    backend_summary = ", ".join(
        f"`{pod.get('name')}` Ready={pod.get('ready')}"
        for pod in backend_pods[:8]
    ) or "-"
    rows.append(f"| Service | `{_md_cell(service.get('namespace'))}/{_md_cell(service.get('name'))}` type=`{_md_cell(service.get('type'))}` selector=`{_md_cell(service.get('selector'))}` |")
    rows.append(f"| EndpointSlice | ready={_ready_endpoint_count(endpoint_slices)} slices={len(endpoint_slices)} |")
    rows.append(f"| Backend Pods | {backend_summary} |")
    rows.append(f"| Ingress | `{_md_cell(ingress.get('namespace'))}/{_md_cell(ingress.get('name'))}` class=`{_md_cell(ingress.get('ingress_class_name'))}` lb=`{_md_cell(ingress.get('load_balancer_ingress'))}` |")
    rows.append(f"| NetworkPolicy | {len(snapshot.get('network_policies') or [])} 个策略位于 namespace `{_md_cell(snapshot.get('inputs', {}).get('namespace'))}` |")
    rows.append(f"| Cloud ELB | ids=`{_md_cell((snapshot.get('cloud') or {}).get('elb_ids'))}` |")
    return "\n".join(rows)


def _topology(snapshot: Dict[str, Any], flags: Dict[str, bool]) -> str:
    target = snapshot.get("target") or {}
    service = target.get("service") or {}
    ingress = target.get("ingress") or {}
    source = target.get("source_pod") or {}
    destination = target.get("destination_pod") or {}
    if flags.get("north_south"):
        chain = [
            "外部客户端",
            "Cloud ELB/EIP",
            f"Ingress {ingress.get('namespace', '-')}/{ingress.get('name', '-')}",
            f"Service {service.get('namespace', '-')}/{service.get('name', '-')}",
            "EndpointSlice",
            f"Pod {destination.get('namespace', '-')}/{destination.get('name', '-')}",
        ]
    elif flags.get("dns"):
        chain = [
            f"Client Pod {source.get('namespace', '-')}/{source.get('name', '-')}",
            "kube-dns Service",
            "CoreDNS Pod",
            "上游 DNS / 集群 Service DNS",
        ]
    else:
        chain = [
            f"Source Pod {source.get('namespace', '-')}/{source.get('name', '-')}",
            "NetworkPolicy",
            f"Service {service.get('namespace', '-')}/{service.get('name', '-')}",
            "EndpointSlice",
            f"Destination Pod {destination.get('namespace', '-')}/{destination.get('name', '-')}",
        ]
    return " -> ".join(chain)


def build_markdown_report(snapshot: Dict[str, Any], assessment: Dict[str, Any]) -> str:
    inputs = snapshot.get("inputs") or {}
    top_causes = assessment.get("top_causes") or []
    findings = assessment.get("findings") or []
    flags = assessment.get("symptom_flags") or {}
    recs = []
    for cause in top_causes:
        for rec in cause.get("recommendation") or []:
            if rec not in recs:
                recs.append(rec)
    if not recs:
        recs = [
            "执行一次从源 Pod 到 Service/Pod IP、Ingress 域名和 ELB VIP 的实时连通性验证，补齐数据面证据。",
            "缩小故障窗口并重新采集 Events、Ingress Controller 日志和后端应用日志。",
        ]

    conclusion_lines = []
    if top_causes:
        for idx, cause in enumerate(top_causes, start=1):
            conclusion_lines.append(f"{idx}. **{cause['title']}** (`{cause['type']}`，置信度 {cause['confidence']:.0%})")
    else:
        conclusion_lines.append("1. 未命中明确根因；当前报告只说明已检查项和证据缺口。")

    return "\n".join([
        "# CCE 网络故障自动化诊断报告",
        "",
        "## 1. 诊断总览",
        "| 评估项 | 详细信息 |",
        "| :--- | :--- |",
        f"| 目标集群 | region=`{_md_cell(inputs.get('region'))}` cluster_id=`{_md_cell(inputs.get('cluster_id'))}` |",
        f"| 目标对象 | namespace=`{_md_cell(inputs.get('namespace'))}` target=`{_md_cell(inputs.get('target_kind'))}/{_md_cell(inputs.get('target_name'))}` service=`{_md_cell(inputs.get('service_name'))}` ingress=`{_md_cell(inputs.get('ingress_name'))}` |",
        f"| 故障现象 | {_md_cell(inputs.get('failure_symptom'))} |",
        f"| 诊断结论 | **{_md_cell(assessment.get('conclusion'), 260)}** |",
        f"| 置信度 | **{_md_cell(assessment.get('confidence'))}** |",
        f"| 数据采集时间 | `{_md_cell(snapshot.get('collected_at'))}` |",
        f"| 剪枝状态 | {'已剪枝，节点/底座故障足以解释问题' if assessment.get('pipeline_pruned') else '未剪枝，已继续检查上层链路'} |",
        "",
        "## 2. 排查过程",
        _stage_rows(assessment),
        "",
        "## 3. 链路拓扑",
        "```text",
        _topology(snapshot, flags),
        "```",
        "",
        "## 4. 关键对象快照",
        _resource_summary(snapshot),
        "",
        "## 5. 证据矩阵",
        _evidence_rows(findings),
        "",
        "## 6. 诊断结论",
        *conclusion_lines,
        "",
        "## 7. 建议动作与验证标准",
        *[f"{idx}. {rec}" for idx, rec in enumerate(recs, start=1)],
        "恢复验证标准：目标 Service 有 ready EndpointSlice；CoreDNS/Ingress Controller 无新增 Warning；ELB 后端为健康；客户端请求成功率恢复并且 502/504/timeout 不再增长。",
        "",
    ])


def diagnose_network_failure(
    region: str,
    cluster_id: str,
    namespace: str = "default",
    target_kind: Optional[str] = None,
    target_name: Optional[str] = None,
    service_name: Optional[str] = None,
    ingress_name: Optional[str] = None,
    source_pod: Optional[str] = None,
    destination_pod: Optional[str] = None,
    domain: Optional[str] = None,
    failure_symptom: Optional[str] = None,
    elb_id: Optional[str] = None,
    include_logs: bool = True,
    include_cloud: bool = True,
    tail_lines: int = 120,
    event_limit: int = 500,
    hours: int = 1,
    ak: Optional[str] = None,
    sk: Optional[str] = None,
    project_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Diagnose Service, DNS, Ingress, NetworkPolicy and ELB failures and return Markdown."""
    access_key, secret_key, proj_id = get_credentials_with_region(region, ak, sk, project_id)
    if not access_key or not secret_key:
        return {"success": False, "error": "Credentials not provided. Set HUAWEI_AK/HUAWEI_SK or pass ak/sk."}
    if not cluster_id:
        return {"success": False, "error": "cluster_id is required"}
    if not K8S_AVAILABLE:
        return {"success": False, "error": f"Kubernetes SDK not installed: {K8S_IMPORT_ERROR}"}
    if not SDK_AVAILABLE:
        return {"success": False, "error": f"Huawei Cloud SDK not installed: {IMPORT_ERROR}"}

    try:
        snapshot = _collect_k8s_snapshot(
            region,
            cluster_id,
            namespace,
            access_key,
            secret_key,
            proj_id,
            target_name,
            target_kind,
            service_name,
            ingress_name,
            source_pod,
            destination_pod,
            domain,
            failure_symptom,
            include_logs,
            tail_lines,
            event_limit,
            hours,
        )
        if include_cloud:
            target = snapshot.get("target") or {}
            snapshot["cloud"] = _collect_cloud_context(
                region,
                target.get("service"),
                target.get("ingress"),
                elb_id,
                access_key,
                secret_key,
                proj_id,
                hours,
            )
        else:
            snapshot["cloud"] = {"elb_ids": []}

        assessment = assess_network_snapshot(snapshot)
        report = build_markdown_report(snapshot, assessment)
        return {
            "success": True,
            "action": "huawei_network_failure_diagnose",
            "region": region,
            "cluster_id": cluster_id,
            "namespace": namespace,
            "snapshot": snapshot,
            "conclusion": assessment["conclusion"],
            "confidence": assessment["confidence"],
            "findings": assessment["findings"],
            "top_causes": assessment["top_causes"],
            "pipeline_pruned": assessment["pipeline_pruned"],
            "report_markdown": report,
        }
    except Exception as exc:
        return {"success": False, "error": str(exc), "error_type": type(exc).__name__}


def diagnose_network_failure_action(params: Dict[str, str]) -> Dict[str, Any]:
    return diagnose_network_failure(
        region=params["region"],
        cluster_id=params["cluster_id"],
        namespace=params.get("namespace", "default"),
        target_kind=params.get("target_kind"),
        target_name=params.get("target_name"),
        service_name=params.get("service_name"),
        ingress_name=params.get("ingress_name"),
        source_pod=params.get("source_pod"),
        destination_pod=params.get("destination_pod"),
        domain=params.get("domain"),
        failure_symptom=params.get("failure_symptom") or params.get("symptom"),
        elb_id=params.get("elb_id"),
        include_logs=_as_bool(params.get("include_logs"), True),
        include_cloud=_as_bool(params.get("include_cloud"), True),
        tail_lines=_to_int(params.get("tail_lines"), 120),
        event_limit=_to_int(params.get("event_limit"), 500),
        hours=_to_int(params.get("hours"), 1),
        ak=params.get("ak"),
        sk=params.get("sk"),
        project_id=params.get("project_id"),
    )
