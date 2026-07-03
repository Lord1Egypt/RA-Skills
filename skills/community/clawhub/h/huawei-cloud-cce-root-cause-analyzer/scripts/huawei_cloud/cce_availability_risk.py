"""CCE availability risk scanner."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean
from typing import Any, Dict, Iterable, Optional

from . import cce, cce_hpa, cce_metrics
from .common import (
    IMPORT_ERROR,
    K8S_AVAILABLE,
    K8S_IMPORT_ERROR,
    SDK_AVAILABLE,
    _safe_delete_file,
    get_credentials_with_region,
    k8s_client,
)


SYSTEM_NAMESPACES = {"kube-system"}
DEFAULT_GATEWAY_KEYWORDS = ("nginx", "gateway", "ingress", "proxy", "kong", "apisix", "traefik")
ZONE_LABEL_KEYS = (
    "topology.kubernetes.io/zone",
    "failure-domain.beta.kubernetes.io/zone",
    "topology.cce.io/zone",
)
HOSTNAME_LABEL_KEYS = ("kubernetes.io/hostname",)
NODEPOOL_LABEL_KEY_HINTS = ("nodepool", "node-pool", "node_pool")
CONTROL_PLANE_LABELS = (
    "node-role.kubernetes.io/master",
    "node-role.kubernetes.io/control-plane",
)


def _as_list(value: Optional[str | Iterable[str]], default: Iterable[str] = ()) -> list[str]:
    if value is None:
        return [item for item in default if item]
    if isinstance(value, str):
        return [item.strip() for item in value.split(",") if item.strip()]
    return [str(item).strip() for item in value if str(item).strip()]


def _to_plain(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, list):
        return [_to_plain(item) for item in value]
    if isinstance(value, tuple):
        return [_to_plain(item) for item in value]
    if isinstance(value, dict):
        return {key: _to_plain(item) for key, item in value.items()}
    if hasattr(value, "to_dict"):
        return _to_plain(value.to_dict())
    return str(value)


def _quantity_cpu(value: Optional[str]) -> Optional[float]:
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    try:
        if text.endswith("n"):
            return float(text[:-1]) / 1_000_000_000
        if text.endswith("u"):
            return float(text[:-1]) / 1_000_000
        if text.endswith("m"):
            return float(text[:-1]) / 1000
        return float(text)
    except ValueError:
        return None


def _quantity_memory(value: Optional[str]) -> Optional[float]:
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    suffixes = {
        "Ki": 1024,
        "Mi": 1024**2,
        "Gi": 1024**3,
        "Ti": 1024**4,
        "K": 1000,
        "M": 1000**2,
        "G": 1000**3,
        "T": 1000**4,
    }
    try:
        for suffix, multiplier in suffixes.items():
            if text.endswith(suffix):
                return float(text[: -len(suffix)]) * multiplier
        return float(text)
    except ValueError:
        return None


def _stats(metric: Dict[str, Any]) -> Dict[str, Any]:
    values = []
    for item in metric.get("time_series", []) or []:
        try:
            value = item[1] if isinstance(item, (list, tuple)) else item.get("value")
            values.append(float(value))
        except (TypeError, ValueError, IndexError, AttributeError):
            continue
    values.sort()
    if not values:
        return {"sample_count": 0}
    p95_index = min(len(values) - 1, int(0.95 * (len(values) - 1)))
    return {
        "sample_count": len(values),
        "avg_percent": round(mean(values), 2),
        "p95_percent": round(values[p95_index], 2),
        "max_percent": round(values[-1], 2),
    }


def _metric_map(response: Dict[str, Any], list_name: str) -> dict[str, Dict[str, Any]]:
    result: dict[str, Dict[str, Any]] = {}
    for item in response.get("metrics", {}).get(list_name, []) or []:
        ip = item.get("node_ip") or item.get("node_name")
        if not ip and item.get("instance"):
            ip = str(item["instance"]).split(":", 1)[0]
        if ip:
            result[ip] = _stats(item)
    return result


def _label_value(labels: Dict[str, str], keys: Iterable[str]) -> Optional[str]:
    for key in keys:
        if labels.get(key):
            return labels[key]
    return None


def _nodepool_label(labels: Dict[str, str]) -> Optional[str]:
    for key, value in labels.items():
        normalized = key.lower()
        if any(hint in normalized for hint in NODEPOOL_LABEL_KEY_HINTS):
            return value
    return None


def _node_role(labels: Dict[str, str]) -> str:
    if any(key in labels for key in CONTROL_PLANE_LABELS):
        return "control-plane"
    return "worker"


def _list_items(func, *args, **kwargs):
    result = []
    token = None
    while True:
        call_kwargs = dict(kwargs)
        if token:
            call_kwargs["_continue"] = token
        response = func(*args, **call_kwargs)
        result.extend(getattr(response, "items", []) or [])
        token = getattr(getattr(response, "metadata", None), "_continue", None)
        if not token:
            return result


def _selector_dict(selector: Any) -> Dict[str, Any]:
    data = _to_plain(selector) or {}
    return {
        "match_labels": data.get("match_labels") or data.get("matchLabels") or {},
        "match_expressions": data.get("match_expressions") or data.get("matchExpressions") or [],
    }


def _selector_matches(selector: Dict[str, Any], labels: Dict[str, str]) -> bool:
    for key, value in (selector.get("match_labels") or {}).items():
        if labels.get(key) != value:
            return False
    for expr in selector.get("match_expressions") or []:
        key = expr.get("key")
        operator = expr.get("operator")
        values = expr.get("values") or []
        if operator == "In" and labels.get(key) not in values:
            return False
        if operator == "NotIn" and labels.get(key) in values:
            return False
        if operator == "Exists" and key not in labels:
            return False
        if operator == "DoesNotExist" and key in labels:
            return False
    return True


def _container_info(container: Any) -> Dict[str, Any]:
    resources = _to_plain(getattr(container, "resources", None)) or {}
    return {
        "name": getattr(container, "name", None),
        "image": getattr(container, "image", None),
        "readiness_probe": getattr(container, "readiness_probe", None) is not None,
        "liveness_probe": getattr(container, "liveness_probe", None) is not None,
        "startup_probe": getattr(container, "startup_probe", None) is not None,
        "resources": {
            "requests": resources.get("requests") or {},
            "limits": resources.get("limits") or {},
        },
    }


def _workload_from_obj(obj: Any, kind: str) -> Dict[str, Any]:
    metadata = obj.metadata
    spec = obj.spec
    status = getattr(obj, "status", None)
    pod_spec = spec.template.spec
    template_meta = spec.template.metadata
    containers = [_container_info(container) for container in (pod_spec.containers or [])]
    selector = _selector_dict(getattr(spec, "selector", None))
    desired = getattr(spec, "replicas", None)
    if kind == "DaemonSet":
        desired = getattr(status, "desired_number_scheduled", 0) if status else 0
    if desired is None:
        desired = 1
    return {
        "key": f"{kind}/{metadata.namespace}/{metadata.name}",
        "kind": kind,
        "namespace": metadata.namespace,
        "name": metadata.name,
        "desired_replicas": desired,
        "ready_replicas": getattr(status, "ready_replicas", None) if status else None,
        "available_replicas": getattr(status, "available_replicas", None) if status else None,
        "labels": dict(metadata.labels or {}),
        "selector": selector,
        "template_labels": dict(template_meta.labels or {}),
        "node_selector": dict(pod_spec.node_selector or {}),
        "affinity": _to_plain(getattr(pod_spec, "affinity", None)),
        "topology_spread_constraints": _to_plain(getattr(pod_spec, "topology_spread_constraints", None)) or [],
        "containers": containers,
        "service_names": [],
        "ingress_names": [],
        "pdbs": [],
        "pods": [],
    }


def _pod_owner_key(pod: Any, rs_owner_map: Dict[tuple[str, str], str]) -> Optional[str]:
    namespace = pod.metadata.namespace
    for owner in pod.metadata.owner_references or []:
        if getattr(owner, "controller", False) is False:
            continue
        kind = owner.kind
        name = owner.name
        if kind == "ReplicaSet":
            deployment = rs_owner_map.get((namespace, name))
            return f"Deployment/{namespace}/{deployment}" if deployment else f"ReplicaSet/{namespace}/{name}"
        return f"{kind}/{namespace}/{name}"
    return None


def _pod_info(pod: Any, rs_owner_map: Dict[tuple[str, str], str], node_by_name: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    node_name = getattr(pod.spec, "node_name", None)
    node = node_by_name.get(node_name, {})
    ready = False
    for condition in getattr(pod.status, "conditions", []) or []:
        if condition.type == "Ready":
            ready = condition.status == "True"
            break
    return {
        "name": pod.metadata.name,
        "namespace": pod.metadata.namespace,
        "phase": getattr(pod.status, "phase", None),
        "ready": ready,
        "node": node_name,
        "zone": node.get("zone"),
        "nodepool": node.get("nodepool"),
        "labels": dict(pod.metadata.labels or {}),
        "owner_key": _pod_owner_key(pod, rs_owner_map),
    }


def _node_info(node: Any) -> Dict[str, Any]:
    labels = dict(node.metadata.labels or {})
    ready = "Unknown"
    for condition in node.status.conditions or []:
        if condition.type == "Ready":
            ready = condition.status
            break
    return {
        "name": node.metadata.name,
        "labels": labels,
        "zone": _label_value(labels, ZONE_LABEL_KEYS),
        "nodepool": _nodepool_label(labels),
        "role": _node_role(labels),
        "ready": ready,
        "allocatable_cpu_cores": _quantity_cpu((node.status.allocatable or {}).get("cpu")),
        "allocatable_memory_bytes": _quantity_memory((node.status.allocatable or {}).get("memory")),
    }


def _pdb_info(pdb: Any) -> Dict[str, Any]:
    return {
        "name": pdb.metadata.name,
        "namespace": pdb.metadata.namespace,
        "selector": _selector_dict(pdb.spec.selector if pdb.spec else None),
        "min_available": _to_plain(getattr(pdb.spec, "min_available", None)) if pdb.spec else None,
        "max_unavailable": _to_plain(getattr(pdb.spec, "max_unavailable", None)) if pdb.spec else None,
        "disruptions_allowed": getattr(pdb.status, "disruptions_allowed", None) if pdb.status else None,
    }


def _service_info(service: Any) -> Dict[str, Any]:
    return {
        "name": service.metadata.name,
        "namespace": service.metadata.namespace,
        "type": service.spec.type,
        "selector": dict(service.spec.selector or {}),
        "labels": dict(service.metadata.labels or {}),
        "annotations": dict(service.metadata.annotations or {}),
    }


def _ingress_info(ingress: Any) -> Dict[str, Any]:
    service_names = []
    if ingress.spec.default_backend and ingress.spec.default_backend.service:
        service_names.append(ingress.spec.default_backend.service.name)
    for rule in ingress.spec.rules or []:
        if not rule.http:
            continue
        for path in rule.http.paths or []:
            if path.backend and path.backend.service:
                service_names.append(path.backend.service.name)
    return {
        "name": ingress.metadata.name,
        "namespace": ingress.metadata.namespace,
        "service_names": sorted(set(service_names)),
        "labels": dict(ingress.metadata.labels or {}),
        "annotations": dict(ingress.metadata.annotations or {}),
    }


def _collect_k8s_inventory(
    region: str,
    cluster_id: str,
    ak: Optional[str],
    sk: Optional[str],
    project_id: Optional[str],
    limit: int,
) -> tuple[Dict[str, Any], list[str]]:
    if not K8S_AVAILABLE:
        return {}, [f"Kubernetes SDK not installed: {K8S_IMPORT_ERROR}"]
    if not SDK_AVAILABLE:
        return {}, [f"Huawei Cloud SDK not installed: {IMPORT_ERROR}"]

    access_key, secret_key, proj_id = get_credentials_with_region(region, ak, sk, project_id)
    if not access_key or not secret_key:
        return {}, ["Credentials not provided"]

    cert_file = None
    key_file = None
    data_gaps: list[str] = []
    try:
        cert_file, key_file = cce_hpa._setup_k8s_client(region, cluster_id, access_key, secret_key, proj_id)
        core_v1 = k8s_client.CoreV1Api()
        apps_v1 = k8s_client.AppsV1Api()
        policy_v1 = k8s_client.PolicyV1Api()
        networking_v1 = k8s_client.NetworkingV1Api()

        def safe(name: str, func, *args, **kwargs):
            try:
                return _list_items(func, *args, **kwargs)
            except Exception as exc:
                data_gaps.append(f"{name}: {exc}")
                return []

        nodes_raw = safe("nodes", core_v1.list_node, limit=limit)
        nodes = [_node_info(node) for node in nodes_raw]
        node_by_name = {node["name"]: node for node in nodes}

        replicasets = safe("replicasets", apps_v1.list_replica_set_for_all_namespaces, limit=limit)
        rs_owner_map: dict[tuple[str, str], str] = {}
        for rs in replicasets:
            for owner in rs.metadata.owner_references or []:
                if owner.kind == "Deployment":
                    rs_owner_map[(rs.metadata.namespace, rs.metadata.name)] = owner.name

        pods_raw = safe("pods", core_v1.list_pod_for_all_namespaces, limit=limit)
        pods = [_pod_info(pod, rs_owner_map, node_by_name) for pod in pods_raw]

        deployments = safe("deployments", apps_v1.list_deployment_for_all_namespaces, limit=limit)
        statefulsets = safe("statefulsets", apps_v1.list_stateful_set_for_all_namespaces, limit=limit)
        daemonsets = safe("daemonsets", apps_v1.list_daemon_set_for_all_namespaces, limit=limit)
        workloads = (
            [_workload_from_obj(item, "Deployment") for item in deployments]
            + [_workload_from_obj(item, "StatefulSet") for item in statefulsets]
            + [_workload_from_obj(item, "DaemonSet") for item in daemonsets]
        )

        pdbs = [_pdb_info(item) for item in safe("pdbs", policy_v1.list_pod_disruption_budget_for_all_namespaces, limit=limit)]
        services = [_service_info(item) for item in safe("services", core_v1.list_service_for_all_namespaces, limit=limit)]
        ingresses = [_ingress_info(item) for item in safe("ingresses", networking_v1.list_ingress_for_all_namespaces, limit=limit)]

        return {
            "nodes": nodes,
            "pods": pods,
            "workloads": workloads,
            "pdbs": pdbs,
            "services": services,
            "ingresses": ingresses,
        }, data_gaps
    except Exception as exc:
        return {}, [str(exc)]
    finally:
        _safe_delete_file(cert_file)
        _safe_delete_file(key_file)


def _counter(rows: Iterable[Dict[str, Any]], key: str) -> Dict[str, int]:
    result: dict[str, int] = {}
    for row in rows:
        value = row.get(key) or "unknown"
        result[value] = result.get(value, 0) + 1
    return dict(sorted(result.items()))


def _severity_value(severity: str) -> int:
    return {"critical": 100, "high": 70, "medium": 40, "low": 10}.get(severity, 0)


def _issue(severity: str, category: str, resource: str, message: str, recommendation: str, **extra) -> Dict[str, Any]:
    payload = {
        "severity": severity,
        "category": category,
        "resource": resource,
        "message": message,
        "recommendation": recommendation,
    }
    payload.update(extra)
    return payload


def _is_gateway(workload: Dict[str, Any], services: list[Dict[str, Any]], ingresses: list[Dict[str, Any]], keywords: list[str]) -> bool:
    text_parts = [
        workload["name"],
        workload["namespace"],
        json.dumps(workload.get("labels", {}), sort_keys=True),
        json.dumps(workload.get("template_labels", {}), sort_keys=True),
    ]
    text = " ".join(text_parts).lower()
    if any(keyword.lower() in text for keyword in keywords):
        return True
    for service in services:
        if service["namespace"] != workload["namespace"]:
            continue
        if service.get("type") == "LoadBalancer" and _selector_matches({"match_labels": service.get("selector") or {}}, workload.get("template_labels") or {}):
            return True
    service_names = {
        service["name"]
        for service in services
        if service["namespace"] == workload["namespace"]
        and _selector_matches({"match_labels": service.get("selector") or {}}, workload.get("template_labels") or {})
    }
    return any(
        ingress["namespace"] == workload["namespace"] and service_names.intersection(ingress.get("service_names") or [])
        for ingress in ingresses
    )


def _is_core_plugin(workload: Dict[str, Any]) -> bool:
    text = f"{workload['namespace']}/{workload['name']} {json.dumps(workload.get('labels', {}), sort_keys=True)}".lower()
    return any(keyword in text for keyword in ("coredns", "nginx-ingress", "ingress-nginx"))


def _has_pod_anti_affinity(workload: Dict[str, Any]) -> bool:
    affinity = workload.get("affinity") or {}
    return bool((affinity.get("pod_anti_affinity") or {}).get("required_during_scheduling_ignored_during_execution") or (affinity.get("pod_anti_affinity") or {}).get("preferred_during_scheduling_ignored_during_execution"))


def _has_spread(workload: Dict[str, Any]) -> bool:
    return bool(workload.get("topology_spread_constraints"))


def _restricted_affinity_signals(workload: Dict[str, Any]) -> list[Dict[str, Any]]:
    signals: list[Dict[str, Any]] = []
    for key, value in (workload.get("node_selector") or {}).items():
        lowered = key.lower()
        if key in ZONE_LABEL_KEYS or key in HOSTNAME_LABEL_KEYS or any(hint in lowered for hint in NODEPOOL_LABEL_KEY_HINTS):
            signals.append({"source": "nodeSelector", "key": key, "values": [value]})

    node_affinity = ((workload.get("affinity") or {}).get("node_affinity") or {})
    required = node_affinity.get("required_during_scheduling_ignored_during_execution") or {}
    for term in required.get("node_selector_terms") or []:
        for expr in term.get("match_expressions") or []:
            key = expr.get("key")
            values = expr.get("values") or []
            lowered = (key or "").lower()
            if key in ZONE_LABEL_KEYS or key in HOSTNAME_LABEL_KEYS or any(hint in lowered for hint in NODEPOOL_LABEL_KEY_HINTS):
                signals.append({"source": "requiredNodeAffinity", "key": key, "values": values})
    return signals


def _container_resource_issues(workload: Dict[str, Any], cpu_ratio_threshold: float, memory_ratio_threshold: float) -> list[Dict[str, Any]]:
    issues: list[Dict[str, Any]] = []
    for container in workload.get("containers", []) or []:
        resources = container.get("resources") or {}
        requests = resources.get("requests") or {}
        limits = resources.get("limits") or {}
        resource_name = f"{workload['key']} container/{container.get('name')}"
        if "cpu" not in requests or "memory" not in requests:
            issues.append(_issue(
                "medium",
                "resources",
                resource_name,
                "Container request is missing for CPU or memory.",
                "Set CPU and memory requests based on observed p95 usage before relying on scheduling or autoscaling decisions.",
            ))
        cpu_request = _quantity_cpu(requests.get("cpu"))
        cpu_limit = _quantity_cpu(limits.get("cpu"))
        if cpu_request and cpu_limit and cpu_limit / cpu_request > cpu_ratio_threshold:
            issues.append(_issue(
                "low",
                "resources",
                resource_name,
                f"CPU limit/request ratio is {cpu_limit / cpu_request:.1f}.",
                f"Review CPU limit or request; keep ratio under {cpu_ratio_threshold:.1f} unless burst behavior is intentional.",
            ))
        mem_request = _quantity_memory(requests.get("memory"))
        mem_limit = _quantity_memory(limits.get("memory"))
        if mem_request and mem_limit and mem_limit / mem_request > memory_ratio_threshold:
            issues.append(_issue(
                "medium",
                "resources",
                resource_name,
                f"Memory limit/request ratio is {mem_limit / mem_request:.1f}.",
                f"Review memory limit or request; keep ratio under {memory_ratio_threshold:.1f} to reduce eviction and bin-packing risk.",
            ))
    return issues


def _attach_workload_context(inventory: Dict[str, Any], gateway_keywords: list[str]) -> list[Dict[str, Any]]:
    workloads = [dict(item) for item in inventory.get("workloads", [])]
    workload_by_key = {item["key"]: item for item in workloads}

    for pod in inventory.get("pods", []) or []:
        workload = workload_by_key.get(pod.get("owner_key"))
        if workload:
            workload.setdefault("pods", []).append(pod)

    for pdb in inventory.get("pdbs", []) or []:
        for workload in workloads:
            if pdb["namespace"] == workload["namespace"] and _selector_matches(pdb.get("selector") or {}, workload.get("template_labels") or {}):
                workload.setdefault("pdbs", []).append(pdb)

    for service in inventory.get("services", []) or []:
        for workload in workloads:
            if service["namespace"] == workload["namespace"] and _selector_matches({"match_labels": service.get("selector") or {}}, workload.get("template_labels") or {}):
                workload.setdefault("service_names", []).append(service["name"])

    for ingress in inventory.get("ingresses", []) or []:
        for workload in workloads:
            if ingress["namespace"] == workload["namespace"] and set(workload.get("service_names") or []).intersection(ingress.get("service_names") or []):
                workload.setdefault("ingress_names", []).append(ingress["name"])

    for workload in workloads:
        workload["is_gateway"] = _is_gateway(workload, inventory.get("services", []), inventory.get("ingresses", []), gateway_keywords)
        workload["is_core_plugin"] = _is_core_plugin(workload)
    return workloads


def _cluster_resource_summary(inventory: Dict[str, Any], workloads: list[Dict[str, Any]]) -> Dict[str, Any]:
    alloc_cpu = sum(node.get("allocatable_cpu_cores") or 0 for node in inventory.get("nodes", []))
    alloc_mem = sum(node.get("allocatable_memory_bytes") or 0 for node in inventory.get("nodes", []))
    req_cpu = limit_cpu = req_mem = limit_mem = 0.0
    missing_request_containers = 0
    for workload in workloads:
        desired = workload.get("desired_replicas") or 0
        if workload.get("kind") == "DaemonSet":
            desired = max(1, len(workload.get("pods") or []))
        for container in workload.get("containers", []) or []:
            resources = container.get("resources") or {}
            requests = resources.get("requests") or {}
            limits = resources.get("limits") or {}
            cpu_req = _quantity_cpu(requests.get("cpu"))
            mem_req = _quantity_memory(requests.get("memory"))
            cpu_limit = _quantity_cpu(limits.get("cpu"))
            mem_limit = _quantity_memory(limits.get("memory"))
            if cpu_req is None or mem_req is None:
                missing_request_containers += 1
            req_cpu += (cpu_req or 0) * desired
            req_mem += (mem_req or 0) * desired
            limit_cpu += (cpu_limit or 0) * desired
            limit_mem += (mem_limit or 0) * desired
    return {
        "allocatable_cpu_cores": round(alloc_cpu, 3),
        "request_cpu_cores": round(req_cpu, 3),
        "limit_cpu_cores": round(limit_cpu, 3),
        "cpu_request_allocatable_ratio": None if not alloc_cpu else round(req_cpu / alloc_cpu, 3),
        "cpu_limit_allocatable_ratio": None if not alloc_cpu else round(limit_cpu / alloc_cpu, 3),
        "allocatable_memory_bytes": int(alloc_mem),
        "request_memory_bytes": int(req_mem),
        "limit_memory_bytes": int(limit_mem),
        "memory_request_allocatable_ratio": None if not alloc_mem else round(req_mem / alloc_mem, 3),
        "memory_limit_allocatable_ratio": None if not alloc_mem else round(limit_mem / alloc_mem, 3),
        "missing_request_containers": missing_request_containers,
    }


def _distribution_issues(workload: Dict[str, Any], cluster_zone_count: int) -> list[Dict[str, Any]]:
    pods = [pod for pod in workload.get("pods", []) if pod.get("phase") in {None, "Running"}]
    desired = workload.get("desired_replicas") or 0
    issues: list[Dict[str, Any]] = []
    if workload["kind"] != "DaemonSet" and desired < 2:
        issues.append(_issue(
            "high",
            "single-replica",
            workload["key"],
            "Workload has fewer than 2 desired replicas.",
            "Run at least 2 replicas for availability-sensitive workloads, then add PDB and anti-affinity or topology spread.",
        ))
    if len(pods) >= 2:
        node_counts = _counter(pods, "node")
        zone_counts = {key: value for key, value in _counter(pods, "zone").items() if key != "unknown"}
        if len(node_counts) == 1:
            issues.append(_issue(
                "high",
                "pod-distribution",
                workload["key"],
                "Multiple replicas are concentrated on one node.",
                "Add required/preferred pod anti-affinity or topologySpreadConstraints by hostname.",
                distribution=node_counts,
            ))
        elif max(node_counts.values()) / len(pods) >= 0.7:
            issues.append(_issue(
                "medium",
                "pod-distribution",
                workload["key"],
                "Most replicas are concentrated on one node.",
                "Prefer topology spread by hostname and review node affinity constraints.",
                distribution=node_counts,
            ))
        if cluster_zone_count > 1 and zone_counts:
            if len(zone_counts) == 1:
                issues.append(_issue(
                    "high",
                    "az-distribution",
                    workload["key"],
                    "All visible replicas are concentrated in one AZ.",
                    "Spread replicas across AZs with topologySpreadConstraints or soft pod anti-affinity by zone.",
                    distribution=zone_counts,
                ))
            elif max(zone_counts.values()) / sum(zone_counts.values()) >= 0.7:
                issues.append(_issue(
                    "medium",
                    "az-distribution",
                    workload["key"],
                    "Replica distribution is skewed toward one AZ.",
                    "Review hard node affinity and prefer balanced topology spread by zone.",
                    distribution=zone_counts,
                ))
    return issues


def _workload_issues(workloads: list[Dict[str, Any]], cluster_zone_count: int, cpu_ratio: float, memory_ratio: float) -> list[Dict[str, Any]]:
    issues: list[Dict[str, Any]] = []
    for workload in workloads:
        desired = workload.get("desired_replicas") or 0
        important = workload.get("is_gateway") or workload.get("is_core_plugin") or workload["namespace"] not in SYSTEM_NAMESPACES
        issues.extend(_distribution_issues(workload, cluster_zone_count))

        if workload["kind"] in {"Deployment", "StatefulSet"} and desired >= 2 and important and not workload.get("pdbs"):
            issues.append(_issue(
                "medium",
                "pdb",
                workload["key"],
                "No matching PodDisruptionBudget was found.",
                "Create a PDB such as minAvailable=1 or maxUnavailable=1, adjusted for the desired replica count.",
            ))

        containers = workload.get("containers", []) or []
        if important and containers:
            if not all(container.get("readiness_probe") for container in containers):
                issues.append(_issue(
                    "medium",
                    "health-check",
                    workload["key"],
                    "At least one container is missing readinessProbe.",
                    "Add readinessProbe so Service, Ingress, and rolling updates only route to ready Pods.",
                ))
            if not all(container.get("liveness_probe") for container in containers):
                issues.append(_issue(
                    "low",
                    "health-check",
                    workload["key"],
                    "At least one container is missing livenessProbe.",
                    "Add livenessProbe for self-healing, and tune thresholds to avoid restart loops.",
                ))

        for signal in _restricted_affinity_signals(workload):
            severity = "high" if signal["key"] in HOSTNAME_LABEL_KEYS else "medium"
            issues.append(_issue(
                severity,
                "affinity",
                workload["key"],
                f"Hard scheduling rule restricts placement by {signal['key']}.",
                "Replace hard affinity with soft preferences or topologySpreadConstraints unless the constraint is required.",
                signal=signal,
            ))

        if desired >= 2 and important and not _has_pod_anti_affinity(workload) and not _has_spread(workload):
            category = "core-plugin" if workload.get("is_core_plugin") else "affinity"
            issues.append(_issue(
                "medium",
                category,
                workload["key"],
                "No pod anti-affinity or topology spread constraint was found.",
                "Add anti-affinity or topologySpreadConstraints by hostname and zone for multi-replica workloads.",
            ))

        if workload.get("is_gateway") and desired >= 2:
            if not workload.get("pdbs"):
                issues.append(_issue(
                    "high",
                    "gateway",
                    workload["key"],
                    "Gateway-like workload has multiple replicas but no matching PDB.",
                    "Add a PDB before maintenance operations so gateway capacity is preserved.",
                ))
            if not _has_pod_anti_affinity(workload) and not _has_spread(workload):
                issues.append(_issue(
                    "high",
                    "gateway",
                    workload["key"],
                    "Gateway-like workload lacks anti-affinity/topology spread.",
                    "Spread gateway replicas across nodes and AZs; prefer topologySpreadConstraints for hostname and zone.",
                ))

        issues.extend(_container_resource_issues(workload, cpu_ratio, memory_ratio))
    return issues


def _control_plane_summary(inventory: Dict[str, Any], node_metrics: Dict[str, Any]) -> tuple[Dict[str, Any], list[Dict[str, Any]], list[str]]:
    control_nodes = [node for node in inventory.get("nodes", []) if node.get("role") == "control-plane"]
    issues: list[Dict[str, Any]] = []
    gaps: list[str] = []
    cpu_map = _metric_map(node_metrics, "cpu_top_n") if node_metrics.get("success") else {}
    mem_map = _metric_map(node_metrics, "memory_top_n") if node_metrics.get("success") else {}
    if node_metrics and not node_metrics.get("success"):
        gaps.append(f"master/node metrics: {node_metrics.get('error', 'collection failed')}")

    if not control_nodes:
        gaps.append("Control-plane nodes are not visible from the Kubernetes API; master HA and master CPU/memory utilization could not be verified.")
        return {
            "status": "unknown",
            "visible_master_nodes": 0,
            "zone_distribution": {},
            "metrics": [],
        }, issues, gaps

    zone_distribution = _counter(control_nodes, "zone")
    if len(control_nodes) < 3:
        issues.append(_issue(
            "high",
            "control-plane",
            "cluster/control-plane",
            f"Only {len(control_nodes)} visible control-plane node(s) were found.",
            "Use a high-availability control plane with at least 3 master/control-plane nodes for production clusters.",
        ))
    if len(zone_distribution) < 2 and len(control_nodes) >= 2:
        issues.append(_issue(
            "medium",
            "control-plane",
            "cluster/control-plane",
            "Visible control-plane nodes are not spread across at least 2 AZs.",
            "Distribute control-plane nodes across AZs when the cluster mode supports it.",
        ))

    metrics = []
    for node in control_nodes:
        ip = node["name"]
        cpu = cpu_map.get(ip)
        memory = mem_map.get(ip)
        metrics.append({"node": node["name"], "zone": node.get("zone"), "cpu": cpu, "memory": memory})
        if cpu and cpu.get("avg_percent", 0) >= 70:
            issues.append(_issue("medium", "control-plane", node["name"], "Master CPU average is high.", "Review control-plane load and cluster scale."))
        if memory and memory.get("avg_percent", 0) >= 70:
            issues.append(_issue("medium", "control-plane", node["name"], "Master memory average is high.", "Review control-plane load and cluster scale."))

    return {
        "status": "healthy" if not issues else "risk",
        "visible_master_nodes": len(control_nodes),
        "zone_distribution": zone_distribution,
        "metrics": metrics,
    }, issues, gaps


def _node_distribution_issues(inventory: Dict[str, Any]) -> list[Dict[str, Any]]:
    nodes = inventory.get("nodes", []) or []
    ready_nodes = [node for node in nodes if node.get("ready") == "True"]
    zone_counts = {key: value for key, value in _counter(ready_nodes, "zone").items() if key != "unknown"}
    issues = []
    if len(ready_nodes) >= 2 and len(zone_counts) < 2:
        issues.append(_issue(
            "high",
            "node-az",
            "cluster/nodes",
            "Ready worker nodes are not spread across multiple AZs.",
            "Add or migrate worker nodes into at least two AZs, then verify workload spreading.",
            distribution=zone_counts,
        ))
    elif zone_counts and max(zone_counts.values()) / sum(zone_counts.values()) >= 0.7 and len(zone_counts) > 1:
        issues.append(_issue(
            "medium",
            "node-az",
            "cluster/nodes",
            "Node distribution is skewed toward one AZ.",
            "Balance node pools and autoscaler min/max settings across AZs.",
            distribution=zone_counts,
        ))
    return issues


def _remediation_plan(issues: list[Dict[str, Any]]) -> list[Dict[str, Any]]:
    plan = []
    categories = {issue["category"] for issue in issues}
    if "single-replica" in categories:
        plan.append({"type": "scale", "requires_authorization": True, "description": "Increase critical Deployment/StatefulSet replicas to at least 2 after capacity and statefulness review."})
    if "pdb" in categories or "gateway" in categories:
        plan.append({"type": "pdb", "requires_authorization": True, "description": "Create or tune PodDisruptionBudget for multi-replica business and gateway workloads."})
    if "affinity" in categories or "pod-distribution" in categories or "az-distribution" in categories:
        plan.append({"type": "scheduling", "requires_authorization": True, "description": "Add topologySpreadConstraints or soften hard node/AZ/nodepool affinity."})
    if "health-check" in categories:
        plan.append({"type": "probe", "requires_authorization": True, "description": "Patch workload pod templates with readinessProbe/livenessProbe and validate rollout."})
    if "resources" in categories:
        plan.append({"type": "resources", "requires_authorization": True, "description": "Set missing requests and reduce excessive limit/request ratios based on observed usage."})
    return plan


def _render_report(result: Dict[str, Any]) -> str:
    summary = result["summary"]
    issues = result["issues"][:50]
    issue_rows = "\n".join(
        f"| {issue['severity']} | {issue['category']} | {issue['resource']} | {issue['message']} |"
        for issue in issues
    ) or "| none | none | none | no issue found |"
    recommendations = "\n".join(f"- {item}" for item in result["recommendations"])
    return f"""# CCE Availability Risk Report

Generated at: {result['generated_at']}

## Scope

- Region: {result['scope']['region']}
- Cluster: {result['scope']['cluster_id']}
- Excluded namespaces: {', '.join(result['scope']['excluded_namespaces']) or 'none'}

## Summary

- Risk level: {summary['risk_level']}
- Total issues: {summary['issue_count']}
- Critical: {summary['critical']}
- High: {summary['high']}
- Medium: {summary['medium']}
- Low: {summary['low']}

## Issues

| Severity | Category | Resource | Message |
|---|---|---|---|
{issue_rows}

## Recommendations

{recommendations}
"""


def _write_outputs(output_dir: Optional[str], result: Dict[str, Any], include_raw: bool, inventory: Dict[str, Any]) -> Dict[str, str]:
    if not output_dir:
        return {}
    target = Path(output_dir)
    target.mkdir(parents=True, exist_ok=True)
    summary_path = target / "availability-risk-summary.json"
    report_path = target / "availability-risk-report.md"
    files = {"summary": str(summary_path), "report": str(report_path)}
    summary_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    report_path.write_text(_render_report(result), encoding="utf-8")
    if include_raw:
        raw_path = target / "availability-risk-raw-inventory.json"
        raw_path.write_text(json.dumps(inventory, ensure_ascii=False, indent=2), encoding="utf-8")
        files["raw_inventory"] = str(raw_path)
    return files


def _recommendations(issues: list[Dict[str, Any]], data_gaps: list[str]) -> list[str]:
    recommendations = []
    if data_gaps:
        recommendations.append("Resolve data gaps first so master HA, PDB, and scheduling checks are complete.")
    if any(issue["category"] == "single-replica" for issue in issues):
        recommendations.append("Prioritize critical business and gateway workloads with single replicas.")
    if any(issue["category"] in {"pod-distribution", "az-distribution", "affinity"} for issue in issues):
        recommendations.append("Review hard node/AZ/nodepool affinity and add topology spread for multi-replica workloads.")
    if any(issue["category"] in {"pdb", "gateway"} for issue in issues):
        recommendations.append("Add PDBs before maintenance, upgrade, node drain, or scale-down operations.")
    if any(issue["category"] == "health-check" for issue in issues):
        recommendations.append("Add readiness/liveness probes before changing rollout or gateway policies.")
    if any(issue["category"] == "resources" for issue in issues):
        recommendations.append("Set missing requests and review excessive limit/request ratios to reduce scheduling and eviction risk.")
    if not recommendations:
        recommendations.append("No strong availability risk was found with the collected data.")
    return recommendations


def scan_cce_availability_risk(
    region: str,
    cluster_id: str,
    ak: Optional[str] = None,
    sk: Optional[str] = None,
    project_id: Optional[str] = None,
    exclude_namespaces: Optional[str | Iterable[str]] = None,
    gateway_keywords: Optional[str | Iterable[str]] = None,
    metrics_hours: int = 24,
    limit: int = 500,
    cpu_limit_request_ratio: float = 4.0,
    memory_limit_request_ratio: float = 2.0,
    output_dir: Optional[str] = None,
    include_raw: bool = False,
) -> Dict[str, Any]:
    """Run a read-only availability risk scan for a CCE cluster."""
    if not region:
        return {"success": False, "error": "region is required"}
    if not cluster_id:
        return {"success": False, "error": "cluster_id is required"}

    excluded = set(_as_list(exclude_namespaces, SYSTEM_NAMESPACES))
    keywords = _as_list(gateway_keywords, DEFAULT_GATEWAY_KEYWORDS)
    inventory, data_gaps = _collect_k8s_inventory(region, cluster_id, ak, sk, project_id, limit)
    if not inventory:
        return {"success": False, "error": "Kubernetes inventory collection failed", "data_gaps": data_gaps}

    inventory["workloads"] = [
        workload
        for workload in inventory.get("workloads", [])
        if workload.get("namespace") not in excluded or _is_core_plugin(workload)
    ]
    workloads = _attach_workload_context(inventory, keywords)
    node_metrics = cce_metrics.get_cce_node_metrics_topN(
        region, cluster_id, ak, sk, project_id, top_n=200, hours=metrics_hours
    )
    cluster_info = cce.list_cce_clusters(region, ak, sk, project_id)
    nodepools = cce.list_cce_node_pools(region, cluster_id, ak, sk, project_id, limit=100)
    if not cluster_info.get("success"):
        data_gaps.append(f"cluster_info: {cluster_info.get('error', 'collection failed')}")
    if not nodepools.get("success"):
        data_gaps.append(f"nodepools: {nodepools.get('error', 'collection failed')}")

    control_plane, control_issues, control_gaps = _control_plane_summary(inventory, node_metrics)
    data_gaps.extend(control_gaps)
    cluster_zone_count = len({node.get("zone") for node in inventory.get("nodes", []) if node.get("zone")})
    issues = []
    issues.extend(control_issues)
    issues.extend(_node_distribution_issues(inventory))
    issues.extend(_workload_issues(workloads, cluster_zone_count, cpu_limit_request_ratio, memory_limit_request_ratio))
    issues.sort(key=lambda item: _severity_value(item["severity"]), reverse=True)

    counts = {severity: sum(1 for issue in issues if issue["severity"] == severity) for severity in ("critical", "high", "medium", "low")}
    risk_level = "low"
    if counts["critical"]:
        risk_level = "critical"
    elif counts["high"]:
        risk_level = "high"
    elif counts["medium"]:
        risk_level = "medium"

    result: Dict[str, Any] = {
        "success": True,
        "action": "scan_cce_availability_risk",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "scope": {
            "region": region,
            "cluster_id": cluster_id,
            "excluded_namespaces": sorted(excluded),
            "gateway_keywords": keywords,
            "metrics_hours": metrics_hours,
        },
        "inventory": {
            "nodes": len(inventory.get("nodes", [])),
            "workloads": len(workloads),
            "pods": len(inventory.get("pods", [])),
            "pdbs": len(inventory.get("pdbs", [])),
            "services": len(inventory.get("services", [])),
            "ingresses": len(inventory.get("ingresses", [])),
            "node_zone_distribution": _counter(inventory.get("nodes", []), "zone"),
            "pod_zone_distribution": _counter(inventory.get("pods", []), "zone"),
        },
        "cluster": {
            "clusters": cluster_info.get("clusters", []) if cluster_info.get("success") else [],
            "nodepools": nodepools.get("nodepools", []) if nodepools.get("success") else [],
            "control_plane": control_plane,
            "resources": _cluster_resource_summary(inventory, workloads),
        },
        "workloads": workloads,
        "issues": issues,
        "summary": {
            "risk_level": risk_level,
            "issue_count": len(issues),
            **counts,
        },
        "recommendations": _recommendations(issues, data_gaps),
        "remediation_plan": _remediation_plan(issues),
        "data_gaps": data_gaps,
    }
    files = _write_outputs(output_dir, result, include_raw, inventory)
    result["files"] = files
    if files.get("summary"):
        Path(files["summary"]).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return result
