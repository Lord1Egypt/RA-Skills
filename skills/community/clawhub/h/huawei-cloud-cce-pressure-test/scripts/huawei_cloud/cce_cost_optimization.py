"""CCE cost optimization advisor action."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean
from typing import Any, Dict, Iterable, Optional

from . import cce, cce_hpa, cce_metrics


DEFAULT_EXCLUDED_NAMESPACES = ("kube-system",)
LOW_UTILIZATION_THRESHOLD = 30.0
REQUEST_OPTIMIZE_THRESHOLD = 50.0
REQUEST_HIGH_THRESHOLD = 33.0


def _as_list(value: Optional[str | Iterable[str]], default: Iterable[str] = ()) -> list[str]:
    if value is None:
        return [item for item in default if item]
    if isinstance(value, str):
        return [item.strip() for item in value.split(",") if item.strip()]
    return [str(item).strip() for item in value if str(item).strip()]


def _values_from(metric: Dict[str, Any]) -> list[float]:
    values: list[float] = []
    for item in metric.get("time_series", []) or []:
        try:
            value = item[1] if isinstance(item, (list, tuple)) else item.get("value")
            values.append(float(value))
        except (TypeError, ValueError, IndexError, AttributeError):
            continue
    return values


def _stats(metric: Dict[str, Any]) -> Dict[str, Any]:
    values = sorted(_values_from(metric))
    if not values:
        return {"sample_count": 0}
    p95_index = min(len(values) - 1, int(0.95 * (len(values) - 1)))
    return {
        "sample_count": len(values),
        "avg_percent": round(mean(values), 2),
        "p95_percent": round(values[p95_index], 2),
        "min_percent": round(values[0], 2),
        "max_percent": round(values[-1], 2),
    }


def _avg(values: Iterable[Optional[float]]) -> Optional[float]:
    valid = [value for value in values if value is not None]
    if not valid:
        return None
    return round(mean(valid), 2)


def _node_metric_map(response: Dict[str, Any], list_name: str) -> dict[str, Dict[str, Any]]:
    rows: dict[str, Dict[str, Any]] = {}
    for item in response.get("metrics", {}).get(list_name, []) or []:
        ip = item.get("node_ip")
        if not ip and item.get("instance"):
            ip = str(item["instance"]).split(":", 1)[0]
        if not ip:
            continue
        rows[ip] = {
            "ip": ip,
            "node": item.get("node_name") or ip,
            "flavor": item.get("flavor"),
            **_stats(item),
        }
    return rows


def _matcher_clause(
    base_matchers: Iterable[str],
    excluded_namespaces: Iterable[str],
    business_namespaces: Iterable[str],
) -> str:
    matchers = list(base_matchers)
    includes = list(business_namespaces)
    if includes:
        namespace_regex = "|".join(re.escape(namespace) for namespace in includes)
        matchers.append(f'namespace=~"{namespace_regex}"')
    else:
        for namespace in excluded_namespaces:
            matchers.append(f'namespace!="{namespace}"')
    return "{" + ",".join(matchers) + "}"


def _request_ratio_queries(
    top_n: int,
    excluded_namespaces: Iterable[str],
    business_namespaces: Iterable[str],
) -> tuple[str, str]:
    cpu_usage = _matcher_clause(["image!=\"\""], excluded_namespaces, business_namespaces)
    memory_usage = _matcher_clause(["image!=\"\""], excluded_namespaces, business_namespaces)
    cpu_request = _matcher_clause(["resource=\"cpu\""], excluded_namespaces, business_namespaces)
    memory_request = _matcher_clause(["resource=\"memory\""], excluded_namespaces, business_namespaces)

    cpu_query = (
        f"bottomk({top_n}, sum by (pod, namespace) "
        f"(rate(container_cpu_usage_seconds_total{cpu_usage}[5m])) "
        f"/ on (pod, namespace) group_left sum by (pod, namespace) "
        f"(kube_pod_container_resource_requests{cpu_request}) * 100)"
    )
    memory_query = (
        f"bottomk({top_n}, sum by (pod, namespace) "
        f"(container_memory_working_set_bytes{memory_usage}) "
        f"/ on (pod, namespace) group_left sum by (pod, namespace) "
        f"(kube_pod_container_resource_requests{memory_request}) * 100)"
    )
    return cpu_query, memory_query


def _business_pods(
    pods: Dict[str, Any],
    excluded_namespaces: Iterable[str],
    business_namespaces: Iterable[str],
) -> dict[str, Dict[str, Any]]:
    excluded = set(excluded_namespaces)
    includes = set(business_namespaces)
    result: dict[str, Dict[str, Any]] = {}
    for pod in pods.get("pods", []) or []:
        namespace = pod.get("namespace")
        name = pod.get("name")
        if not namespace or not name:
            continue
        if namespace in excluded:
            continue
        if includes and namespace not in includes:
            continue
        result[f"{namespace}/{name}"] = pod
    return result


def _request_map(response: Dict[str, Any], list_name: str) -> dict[str, Dict[str, Any]]:
    result: dict[str, Dict[str, Any]] = {}
    for item in response.get("metrics", {}).get(list_name, []) or []:
        namespace = item.get("namespace")
        pod = item.get("pod")
        if not namespace or not pod:
            continue
        result[f"{namespace}/{pod}"] = _stats(item)
    return result


def _request_priority(short_stats: Optional[Dict[str, Any]], long_stats: Optional[Dict[str, Any]]) -> str:
    short_p95 = None if not short_stats else short_stats.get("p95_percent")
    long_p95 = None if not long_stats else long_stats.get("p95_percent")
    if short_p95 is None and long_p95 is None:
        return "unknown"
    if short_p95 is not None and long_p95 is not None:
        if short_p95 < REQUEST_HIGH_THRESHOLD and long_p95 < REQUEST_HIGH_THRESHOLD:
            return "high"
        if short_p95 < REQUEST_OPTIMIZE_THRESHOLD and long_p95 < REQUEST_OPTIMIZE_THRESHOLD:
            return "optimize"
        return "normal"
    if short_p95 is not None and short_p95 < REQUEST_OPTIMIZE_THRESHOLD:
        return "observe"
    return "normal"


def _oversized_request_rows(
    pods: Dict[str, Any],
    short_response: Dict[str, Any],
    long_response: Dict[str, Any],
    excluded_namespaces: Iterable[str],
    business_namespaces: Iterable[str],
) -> tuple[list[Dict[str, Any]], list[str]]:
    current_pods = _business_pods(pods, excluded_namespaces, business_namespaces)
    short_cpu = _request_map(short_response, "cpu_top_n")
    short_memory = _request_map(short_response, "memory_top_n")
    long_cpu = _request_map(long_response, "cpu_top_n")
    long_memory = _request_map(long_response, "memory_top_n")

    rows: list[Dict[str, Any]] = []
    gaps: list[str] = []
    for pod_key in sorted(current_pods):
        namespace, pod_name = pod_key.split("/", 1)
        pod_rows = [
            ("cpu", short_cpu.get(pod_key), long_cpu.get(pod_key)),
            ("memory", short_memory.get(pod_key), long_memory.get(pod_key)),
        ]
        for resource, short_stats, long_stats in pod_rows:
            priority = _request_priority(short_stats, long_stats)
            if priority == "normal":
                continue
            if priority == "unknown":
                gaps.append(f"request ratio metrics missing for {pod_key} {resource}")
                continue
            rows.append({
                "namespace": namespace,
                "pod": pod_name,
                "resource": resource,
                "short_p95_usage_request_percent": None if not short_stats else short_stats.get("p95_percent"),
                "long_p95_usage_request_percent": None if not long_stats else long_stats.get("p95_percent"),
                "short_avg_usage_request_percent": None if not short_stats else short_stats.get("avg_percent"),
                "long_avg_usage_request_percent": None if not long_stats else long_stats.get("avg_percent"),
                "priority": priority,
                "reason": _request_reason(resource, priority),
            })
    return rows, gaps


def _request_reason(resource: str, priority: str) -> str:
    if priority == "high":
        return f"{resource} usage/request p95 is below 33% in both windows"
    if priority == "optimize":
        return f"{resource} usage/request p95 is below 50% in both windows"
    if priority == "observe":
        return f"{resource} usage/request p95 is low in the short window, but long-window data is missing"
    return "no optimization signal"


def _cluster_utilization(node_rows: list[Dict[str, Any]], short_label: str, long_label: str) -> Dict[str, Any]:
    result = {}
    for label in (short_label, long_label):
        cpu = _avg(row.get(label, {}).get("cpu_avg_percent") for row in node_rows)
        memory = _avg(row.get(label, {}).get("memory_avg_percent") for row in node_rows)
        disk = _avg(row.get(label, {}).get("disk_avg_percent") for row in node_rows)
        result[label] = {
            "cpu_avg_percent": cpu,
            "memory_avg_percent": memory,
            "disk_avg_percent": disk,
            "cpu_below_30_percent": False if cpu is None else cpu < LOW_UTILIZATION_THRESHOLD,
            "memory_below_30_percent": False if memory is None else memory < LOW_UTILIZATION_THRESHOLD,
            "overall_low_utilization": any(
                value is not None and value < LOW_UTILIZATION_THRESHOLD for value in (cpu, memory)
            ),
        }
    return result


def _clearly_below(value: Optional[float], cluster_avg: Optional[float]) -> bool:
    if value is None or cluster_avg is None:
        return False
    return value <= cluster_avg - 20.0 or value <= cluster_avg * 0.6


def _node_rows(
    short_metrics: Dict[str, Any],
    long_metrics: Dict[str, Any],
    k8s_nodes: Dict[str, Any],
    short_label: str,
    long_label: str,
) -> list[Dict[str, Any]]:
    short_cpu = _node_metric_map(short_metrics, "cpu_top_n")
    short_memory = _node_metric_map(short_metrics, "memory_top_n")
    short_disk = _node_metric_map(short_metrics, "disk_top_n")
    long_cpu = _node_metric_map(long_metrics, "cpu_top_n")
    long_memory = _node_metric_map(long_metrics, "memory_top_n")
    long_disk = _node_metric_map(long_metrics, "disk_top_n")

    current_nodes = {}
    for node in k8s_nodes.get("nodes", []) or []:
        ip = node.get("internal_ip") or node.get("name")
        if ip:
            current_nodes[ip] = node

    ips = set(current_nodes) | set(short_cpu) | set(short_memory) | set(long_cpu) | set(long_memory)
    rows = []
    for ip in sorted(ips):
        node = current_nodes.get(ip, {})
        rows.append({
            "node": node.get("name") or short_cpu.get(ip, {}).get("node") or long_cpu.get(ip, {}).get("node") or ip,
            "ip": ip,
            "ready": node.get("ready"),
            "allocatable_cpu": node.get("allocatable_cpu"),
            "allocatable_memory": node.get("allocatable_memory"),
            short_label: {
                "cpu_avg_percent": short_cpu.get(ip, {}).get("avg_percent"),
                "cpu_p95_percent": short_cpu.get(ip, {}).get("p95_percent"),
                "memory_avg_percent": short_memory.get(ip, {}).get("avg_percent"),
                "memory_p95_percent": short_memory.get(ip, {}).get("p95_percent"),
                "disk_avg_percent": short_disk.get(ip, {}).get("avg_percent"),
                "disk_p95_percent": short_disk.get(ip, {}).get("p95_percent"),
            },
            long_label: {
                "cpu_avg_percent": long_cpu.get(ip, {}).get("avg_percent"),
                "cpu_p95_percent": long_cpu.get(ip, {}).get("p95_percent"),
                "memory_avg_percent": long_memory.get(ip, {}).get("avg_percent"),
                "memory_p95_percent": long_memory.get(ip, {}).get("p95_percent"),
                "disk_avg_percent": long_disk.get(ip, {}).get("avg_percent"),
                "disk_p95_percent": long_disk.get(ip, {}).get("p95_percent"),
            },
        })
    return rows


def _low_utilization_nodes(node_rows: list[Dict[str, Any]], cluster_util: Dict[str, Any]) -> list[Dict[str, Any]]:
    result = []
    for row in node_rows:
        flags = []
        for label in cluster_util:
            for resource in ("cpu", "memory"):
                value = row.get(label, {}).get(f"{resource}_avg_percent")
                cluster_avg = cluster_util.get(label, {}).get(f"{resource}_avg_percent")
                if _clearly_below(value, cluster_avg):
                    flags.append({
                        "window": label,
                        "resource": resource,
                        "node_avg_percent": value,
                        "cluster_avg_percent": cluster_avg,
                        "reason": "node average is at least 20 percentage points lower than cluster average, or below 60% of cluster average",
                    })
        if flags:
            result.append({"node": row.get("node"), "ip": row.get("ip"), "signals": flags})
    return result


def _inventory(
    nodes: Dict[str, Any],
    nodepools: Dict[str, Any],
    pods: Dict[str, Any],
    deployments: Dict[str, Any],
    hpas: Dict[str, Any],
) -> Dict[str, Any]:
    pod_status: dict[str, int] = {}
    pod_namespaces: dict[str, int] = {}
    for pod in pods.get("pods", []) or []:
        pod_status[pod.get("status", "unknown")] = pod_status.get(pod.get("status", "unknown"), 0) + 1
        namespace = pod.get("namespace", "unknown")
        pod_namespaces[namespace] = pod_namespaces.get(namespace, 0) + 1
    return {
        "nodes": nodes.get("count", 0),
        "nodepools": nodepools.get("count", 0),
        "pods": pods.get("count", 0),
        "pod_status": pod_status,
        "pod_namespaces": pod_namespaces,
        "deployments": deployments.get("count", 0),
        "hpas": hpas.get("count", 0),
    }


def _nodepool_autoscaling_enabled(nodepools: Dict[str, Any]) -> bool:
    for nodepool in nodepools.get("nodepools", []) or []:
        if nodepool.get("autoscaling_enabled"):
            return True
        for scale_group in nodepool.get("scale_groups", []) or []:
            autoscaling = scale_group.get("autoscaling") or {}
            if autoscaling.get("enable") or autoscaling.get("enabled"):
                return True
    return False


def _select_hpa_target(
    deployments: Dict[str, Any],
    excluded_namespaces: Iterable[str],
    business_namespaces: Iterable[str],
    workload_name: Optional[str],
    namespace: Optional[str],
) -> Optional[Dict[str, str]]:
    excluded = set(excluded_namespaces)
    includes = set(business_namespaces)
    candidates = []
    for deployment in deployments.get("deployments", []) or []:
        dep_namespace = deployment.get("namespace")
        dep_name = deployment.get("name")
        if not dep_namespace or not dep_name:
            continue
        if dep_namespace in excluded:
            continue
        if includes and dep_namespace not in includes:
            continue
        if workload_name and dep_name != workload_name:
            continue
        if namespace and dep_namespace != namespace:
            continue
        candidates.append({"namespace": dep_namespace, "workload_name": dep_name, "workload_type": "deployment"})
    if not candidates:
        return None
    return sorted(candidates, key=lambda item: (item["namespace"] != "default", item["namespace"], item["workload_name"]))[0]


def _elasticity(
    nodepools: Dict[str, Any],
    hpas: Dict[str, Any],
    deployments: Dict[str, Any],
    excluded_namespaces: Iterable[str],
    business_namespaces: Iterable[str],
    hpa_workload_name: Optional[str],
    hpa_namespace: Optional[str],
    hpa_workload_type: str,
    hpa_min_replicas: int,
    hpa_max_replicas: int,
    hpa_target_cpu_utilization: Optional[int],
    hpa_target_memory_utilization: Optional[int],
) -> Dict[str, Any]:
    autoscaling_enabled = _nodepool_autoscaling_enabled(nodepools)
    hpa_count = hpas.get("count")
    hpa_status = "unknown"
    if hpas.get("success"):
        hpa_status = "configured" if hpa_count else "not_configured"

    preview = None
    target = _select_hpa_target(deployments, excluded_namespaces, business_namespaces, hpa_workload_name, hpa_namespace)
    if target and hpa_status == "not_configured":
        generated = cce_hpa.generate_cce_hpa_manifest(
            workload_name=target["workload_name"],
            namespace=target["namespace"],
            min_replicas=hpa_min_replicas,
            max_replicas=hpa_max_replicas,
            workload_type=hpa_workload_type or target["workload_type"],
            target_cpu_utilization=hpa_target_cpu_utilization,
            target_memory_utilization=hpa_target_memory_utilization,
        )
        preview = generated if generated.get("success") else {"error": generated.get("error")}

    return {
        "hpa": {
            "status": hpa_status,
            "count": hpa_count,
            "existing_hpas": hpas.get("hpas", []) if hpas.get("success") else [],
            "preview": preview,
            "recommendations": _hpa_recommendations(hpa_status, preview),
        },
        "node_autoscaler": {
            "status": "configured" if autoscaling_enabled else "not_configured",
            "recommendations": _node_autoscaler_recommendations(autoscaling_enabled, nodepools),
        },
    }


def _hpa_recommendations(status: str, preview: Optional[Dict[str, Any]]) -> list[str]:
    if status == "configured":
        return ["Review existing HPA target utilization, minReplicas, and maxReplicas against request sizing before changing it."]
    if status == "not_configured":
        if preview and preview.get("manifest_yaml"):
            return ["No HPA found. Review the generated HPA preview and apply only after explicit confirmation."]
        return ["No HPA found. Select a business Deployment and generate an HPA preview."]
    return ["HPA status could not be determined. Re-run with Kubernetes API access."]


def _node_autoscaler_recommendations(enabled: bool, nodepools: Dict[str, Any]) -> list[str]:
    if enabled:
        return ["Nodepool autoscaling is enabled. Review min/max bounds, cooldown, and scale-down behavior against observed utilization."]
    node_count = nodepools.get("count", 0)
    if node_count:
        return ["Nodepool autoscaling is not enabled. Consider min/max bounds and scale-down policy for eligible node pools."]
    return ["Nodepool autoscaling status is unknown because nodepools were not collected."]


def _recommendations(
    cluster_utilization: Dict[str, Any],
    low_nodes: list[Dict[str, Any]],
    oversized_requests: list[Dict[str, Any]],
    elasticity: Dict[str, Any],
) -> list[str]:
    recommendations: list[str] = []
    low_windows = [
        label
        for label, data in cluster_utilization.items()
        if data.get("overall_low_utilization")
    ]
    if low_windows:
        recommendations.append(
            f"Cluster average CPU or memory utilization is below {LOW_UTILIZATION_THRESHOLD:.0f}% in {', '.join(low_windows)}."
        )
    if low_nodes:
        recommendations.append(f"{len(low_nodes)} node(s) are clearly below the cluster average and should be reviewed for imbalance.")
    high_requests = [row for row in oversized_requests if row.get("priority") in {"high", "optimize"}]
    if high_requests:
        recommendations.append(f"{len(high_requests)} pod resource request signal(s) look oversized in both windows.")
    if elasticity.get("node_autoscaler", {}).get("status") == "not_configured":
        recommendations.append("Nodepool autoscaling is not configured; prepare a bounded autoscaler policy before reducing baseline capacity.")
    if elasticity.get("hpa", {}).get("status") == "not_configured":
        recommendations.append("No HPA was found for the analyzed scope; use the generated preview as a starting point for business workloads.")
    if not recommendations:
        recommendations.append("No strong cost optimization signal was found with the current data.")
    return recommendations


def _data_gap(name: str, response: Dict[str, Any]) -> Optional[str]:
    if response.get("success"):
        return None
    return f"{name}: {response.get('error', 'collection failed')}"


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _render_report(result: Dict[str, Any]) -> str:
    scope = result["scope"]
    inventory = result["inventory"]
    cluster = result["cluster_utilization"]
    recommendations = "\n".join(f"- {item}" for item in result["recommendations"])
    low_nodes = result["low_utilization"].get("nodes_clearly_below_average", [])
    oversized = result["request_analysis"].get("oversized_requests", [])
    node_lines = []
    for row in result["node_utilization"]:
        short = row[scope["short_window"]]
        long = row[scope["long_window"]]
        node_lines.append(
            f"| {row['node']} | {short.get('cpu_avg_percent')} | {short.get('memory_avg_percent')} | "
            f"{long.get('cpu_avg_percent')} | {long.get('memory_avg_percent')} |"
        )
    node_table = "\n".join(node_lines) or "| NA | NA | NA | NA | NA |"
    request_lines = [
        f"| {row['namespace']}/{row['pod']} | {row['resource']} | "
        f"{row.get('short_p95_usage_request_percent')} | {row.get('long_p95_usage_request_percent')} | {row['priority']} |"
        for row in oversized[:30]
    ]
    request_table = "\n".join(request_lines) or "| NA | NA | NA | NA | NA |"

    return f"""# CCE Cost Optimization Report

Generated at: {result['generated_at']}

## Scope

- Region: {scope['region']}
- Cluster: {scope['cluster_id']}
- Windows: {scope['short_window']}, {scope['long_window']}
- Excluded namespaces: {', '.join(scope['excluded_namespaces']) or 'none'}
- Business namespaces: {', '.join(scope['business_namespaces']) or 'all non-excluded namespaces'}

## Inventory

- Nodes: {inventory.get('nodes')}
- Nodepools: {inventory.get('nodepools')}
- Pods: {inventory.get('pods')}
- Deployments: {inventory.get('deployments')}
- HPAs: {inventory.get('hpas')}

## Cluster Utilization

| Window | CPU avg % | Memory avg % | Disk avg % | Low utilization |
|---|---:|---:|---:|---|
| {scope['short_window']} | {cluster[scope['short_window']].get('cpu_avg_percent')} | {cluster[scope['short_window']].get('memory_avg_percent')} | {cluster[scope['short_window']].get('disk_avg_percent')} | {cluster[scope['short_window']].get('overall_low_utilization')} |
| {scope['long_window']} | {cluster[scope['long_window']].get('cpu_avg_percent')} | {cluster[scope['long_window']].get('memory_avg_percent')} | {cluster[scope['long_window']].get('disk_avg_percent')} | {cluster[scope['long_window']].get('overall_low_utilization')} |

## Node Utilization

| Node | CPU {scope['short_window']} avg % | Memory {scope['short_window']} avg % | CPU {scope['long_window']} avg % | Memory {scope['long_window']} avg % |
|---|---:|---:|---:|---:|
{node_table}

Nodes clearly below average: {len(low_nodes)}

## Oversized Requests

| Pod | Resource | {scope['short_window']} p95 usage/request % | {scope['long_window']} p95 usage/request % | Priority |
|---|---|---:|---:|---|
{request_table}

## Elasticity

- HPA status: {result['elasticity']['hpa']['status']}
- Node autoscaler status: {result['elasticity']['node_autoscaler']['status']}

## Recommendations

{recommendations}
"""


def _write_outputs(
    output_dir: Optional[str],
    result: Dict[str, Any],
    raw_collections: Dict[str, Dict[str, Any]],
    include_raw: bool,
) -> Dict[str, str]:
    if not output_dir:
        return {}
    target_dir = Path(output_dir)
    target_dir.mkdir(parents=True, exist_ok=True)
    summary_path = target_dir / "cost-optimization-summary.json"
    report_path = target_dir / "cost-optimization-report.md"
    _write_json(summary_path, result)
    report_path.write_text(_render_report(result), encoding="utf-8")
    files = {
        "summary": str(summary_path),
        "report": str(report_path),
    }
    if include_raw:
        raw_dir = target_dir / "raw"
        raw_dir.mkdir(parents=True, exist_ok=True)
        for name, payload in raw_collections.items():
            raw_path = raw_dir / f"{name}.response.json"
            _write_json(raw_path, payload)
            files[f"raw_{name}"] = str(raw_path)
    return files


def analyze_cce_cost_optimization(
    region: str,
    cluster_id: str,
    ak: Optional[str] = None,
    sk: Optional[str] = None,
    project_id: Optional[str] = None,
    short_hours: int = 24,
    long_hours: int = 168,
    top_n: int = 50,
    exclude_namespaces: Optional[str | Iterable[str]] = None,
    business_namespaces: Optional[str | Iterable[str]] = None,
    output_dir: Optional[str] = None,
    include_raw: bool = False,
    hpa_workload_name: Optional[str] = None,
    hpa_namespace: Optional[str] = None,
    hpa_workload_type: str = "deployment",
    hpa_min_replicas: int = 1,
    hpa_max_replicas: int = 3,
    hpa_target_cpu_utilization: Optional[int] = 60,
    hpa_target_memory_utilization: Optional[int] = None,
) -> Dict[str, Any]:
    """Collect inventory, metrics, request ratios, and elasticity advice for CCE."""
    excluded = _as_list(exclude_namespaces, DEFAULT_EXCLUDED_NAMESPACES)
    business = _as_list(business_namespaces)
    short_label = f"{short_hours}h"
    long_label = f"{long_hours // 24}d" if long_hours % 24 == 0 else f"{long_hours}h"

    if not region:
        return {"success": False, "error": "region is required"}
    if not cluster_id:
        return {"success": False, "error": "cluster_id is required"}

    cpu_request_query, memory_request_query = _request_ratio_queries(top_n, excluded, business)

    raw = {
        "nodepools": cce.list_cce_node_pools(region, cluster_id, ak, sk, project_id, limit=100),
        "nodes": cce.get_kubernetes_nodes(region, cluster_id, ak, sk, project_id),
        "pods": cce.get_kubernetes_pods(region, cluster_id, ak, sk, project_id),
        "deployments": cce.get_kubernetes_deployments(region, cluster_id, ak, sk, project_id),
        "hpas": cce_hpa.list_cce_hpas(region, cluster_id, ak, sk, project_id, include_system=False),
        "node_metrics_short": cce_metrics.get_cce_node_metrics_topN(
            region, cluster_id, ak, sk, project_id, top_n=top_n, hours=short_hours
        ),
        "node_metrics_long": cce_metrics.get_cce_node_metrics_topN(
            region, cluster_id, ak, sk, project_id, top_n=top_n, hours=long_hours
        ),
        "request_ratio_short": cce_metrics.get_cce_pod_metrics_topN(
            region,
            cluster_id,
            ak,
            sk,
            project_id,
            top_n=top_n,
            hours=short_hours,
            cpu_query=cpu_request_query,
            memory_query=memory_request_query,
        ),
        "request_ratio_long": cce_metrics.get_cce_pod_metrics_topN(
            region,
            cluster_id,
            ak,
            sk,
            project_id,
            top_n=top_n,
            hours=long_hours,
            cpu_query=cpu_request_query,
            memory_query=memory_request_query,
        ),
    }

    data_gaps = [gap for name, response in raw.items() if (gap := _data_gap(name, response))]
    core_failures = [
        name for name in ("nodes", "pods", "nodepools") if not raw[name].get("success")
    ]
    if len(core_failures) == 3:
        return {
            "success": False,
            "error": "core CCE inventory collection failed",
            "failed_collections": core_failures,
            "data_gaps": data_gaps,
        }

    nodes = _node_rows(raw["node_metrics_short"], raw["node_metrics_long"], raw["nodes"], short_label, long_label)
    cluster_util = _cluster_utilization(nodes, short_label, long_label)
    low_nodes = _low_utilization_nodes(nodes, cluster_util)
    oversized_requests, request_gaps = _oversized_request_rows(
        raw["pods"], raw["request_ratio_short"], raw["request_ratio_long"], excluded, business
    )
    elasticity = _elasticity(
        raw["nodepools"],
        raw["hpas"],
        raw["deployments"],
        excluded,
        business,
        hpa_workload_name,
        hpa_namespace,
        hpa_workload_type,
        hpa_min_replicas,
        hpa_max_replicas,
        hpa_target_cpu_utilization,
        hpa_target_memory_utilization,
    )

    result: Dict[str, Any] = {
        "success": True,
        "action": "analyze_cce_cost_optimization",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "scope": {
            "region": region,
            "cluster_id": cluster_id,
            "short_window": short_label,
            "long_window": long_label,
            "short_hours": short_hours,
            "long_hours": long_hours,
            "excluded_namespaces": excluded,
            "business_namespaces": business,
        },
        "inventory": _inventory(raw["nodes"], raw["nodepools"], raw["pods"], raw["deployments"], raw["hpas"]),
        "cluster_utilization": cluster_util,
        "node_utilization": nodes,
        "low_utilization": {
            "threshold_percent": LOW_UTILIZATION_THRESHOLD,
            "cluster_average_below_threshold": {
                label: data.get("overall_low_utilization") for label, data in cluster_util.items()
            },
            "nodes_clearly_below_average": low_nodes,
        },
        "request_analysis": {
            "business_pod_count": len(_business_pods(raw["pods"], excluded, business)),
            "thresholds": {
                "optimize_if_p95_usage_request_below_percent": REQUEST_OPTIMIZE_THRESHOLD,
                "high_if_p95_usage_request_below_percent": REQUEST_HIGH_THRESHOLD,
            },
            "oversized_requests": oversized_requests,
        },
        "elasticity": elasticity,
        "recommendations": _recommendations(cluster_util, low_nodes, oversized_requests, elasticity),
        "data_gaps": data_gaps + request_gaps,
        "promql": {
            "request_cpu": cpu_request_query,
            "request_memory": memory_request_query,
        },
    }
    files = _write_outputs(output_dir, result, raw, include_raw)
    result["files"] = files
    if files.get("summary"):
        _write_json(Path(files["summary"]), result)
    return result
