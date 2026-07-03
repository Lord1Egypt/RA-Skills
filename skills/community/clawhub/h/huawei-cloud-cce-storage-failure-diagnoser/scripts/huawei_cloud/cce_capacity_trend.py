"""CCE capacity trend forecasting action."""

from __future__ import annotations

import json
import math
import html
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean
from typing import Any, Dict, Iterable, Optional

from . import cce, cce_diagnosis, cce_hpa, cce_metrics


DEFAULT_EXCLUDED_NAMESPACES = ("kube-system",)
MIN_WINDOW_HOURS = 1
MAX_WINDOW_HOURS = 24 * 31
DEFAULT_TARGET_CPU_PERCENT = 60.0
DEFAULT_TARGET_MEMORY_PERCENT = 70.0
DEFAULT_BOTTLENECK_PERCENT = 80.0
DEFAULT_HEADROOM_PERCENT = 15.0


def _as_list(value: Optional[str | Iterable[str]], default: Iterable[str] = ()) -> list[str]:
    if value is None:
        return [item for item in default if item]
    if isinstance(value, str):
        return [item.strip() for item in value.split(",") if item.strip()]
    return [str(item).strip() for item in value if str(item).strip()]


def _clamp_int(value: int, minimum: int, maximum: int) -> int:
    return max(minimum, min(maximum, int(value)))


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _metric_values(metric: Dict[str, Any]) -> list[tuple[int, float]]:
    values: list[tuple[int, float]] = []
    for item in metric.get("time_series", []) or []:
        try:
            timestamp = int(float(item[0] if isinstance(item, (list, tuple)) else item.get("timestamp")))
            value = float(item[1] if isinstance(item, (list, tuple)) else item.get("value"))
            if math.isfinite(value):
                values.append((timestamp, value))
        except (TypeError, ValueError, IndexError, AttributeError):
            continue
    return values


def _average_series(metrics_response: Dict[str, Any], list_name: str) -> list[Dict[str, Any]]:
    by_timestamp: dict[int, list[float]] = {}
    for metric in metrics_response.get("metrics", {}).get(list_name, []) or []:
        for timestamp, value in _metric_values(metric):
            by_timestamp.setdefault(timestamp, []).append(value)
    return [
        {"timestamp": timestamp, "value": round(mean(values), 2), "sample_count": len(values)}
        for timestamp, values in sorted(by_timestamp.items())
        if values
    ]


def _align_capacity_series(
    cpu_series: list[Dict[str, Any]],
    memory_series: list[Dict[str, Any]],
    disk_series: list[Dict[str, Any]],
) -> list[Dict[str, Any]]:
    cpu = {item["timestamp"]: item for item in cpu_series}
    memory = {item["timestamp"]: item for item in memory_series}
    disk = {item["timestamp"]: item for item in disk_series}
    timestamps = sorted(set(cpu) | set(memory) | set(disk))
    aligned: list[Dict[str, Any]] = []
    for timestamp in timestamps:
        aligned.append({
            "timestamp": timestamp,
            "time_utc": datetime.fromtimestamp(timestamp, tz=timezone.utc).replace(microsecond=0).isoformat(),
            "cpu_avg_percent": None if timestamp not in cpu else cpu[timestamp]["value"],
            "memory_avg_percent": None if timestamp not in memory else memory[timestamp]["value"],
            "disk_avg_percent": None if timestamp not in disk else disk[timestamp]["value"],
            "node_samples": max(
                cpu.get(timestamp, {}).get("sample_count", 0),
                memory.get(timestamp, {}).get("sample_count", 0),
                disk.get(timestamp, {}).get("sample_count", 0),
            ),
        })
    return aligned


def _values(series: list[Dict[str, Any]], field: str) -> list[tuple[int, float]]:
    result: list[tuple[int, float]] = []
    for row in series:
        value = row.get(field)
        if value is None:
            continue
        try:
            number = float(value)
        except (TypeError, ValueError):
            continue
        if math.isfinite(number):
            result.append((int(row["timestamp"]), number))
    return result


def _percentile(sorted_values: list[float], percentile: float) -> Optional[float]:
    if not sorted_values:
        return None
    index = min(len(sorted_values) - 1, max(0, int(round((len(sorted_values) - 1) * percentile))))
    return round(sorted_values[index], 2)


def _slope_per_hour(points: list[tuple[int, float]]) -> float:
    if len(points) < 2:
        return 0.0
    first = points[0][0]
    xs = [(timestamp - first) / 3600.0 for timestamp, _ in points]
    ys = [value for _, value in points]
    x_avg = mean(xs)
    y_avg = mean(ys)
    denominator = sum((x - x_avg) ** 2 for x in xs)
    if denominator == 0:
        return 0.0
    return round(sum((x - x_avg) * (y - y_avg) for x, y in zip(xs, ys)) / denominator, 4)


def _series_stats(series: list[Dict[str, Any]], field: str) -> Dict[str, Any]:
    points = _values(series, field)
    raw_values = [value for _, value in points]
    sorted_values = sorted(raw_values)
    if not sorted_values:
        return {"sample_count": 0}
    bucket_size = max(1, len(raw_values) // 4)
    start_avg = mean(raw_values[:bucket_size])
    end_avg = mean(raw_values[-bucket_size:])
    return {
        "sample_count": len(sorted_values),
        "avg_percent": round(mean(sorted_values), 2),
        "min_percent": round(sorted_values[0], 2),
        "max_percent": round(sorted_values[-1], 2),
        "p95_percent": _percentile(sorted_values, 0.95),
        "latest_percent": round(raw_values[-1], 2),
        "trend_delta_percent": round(end_avg - start_avg, 2),
        "slope_percent_per_hour": _slope_per_hour(points),
    }


def _trend_direction(stats: Dict[str, Any]) -> str:
    delta = stats.get("trend_delta_percent")
    slope = stats.get("slope_percent_per_hour")
    if delta is None or slope is None:
        return "unknown"
    if delta >= 5 or slope >= 0.5:
        return "rising"
    if delta <= -5 or slope <= -0.5:
        return "falling"
    return "flat"


def _bottleneck_prediction(stats: Dict[str, Any], threshold_percent: float) -> Dict[str, Any]:
    if not stats.get("sample_count"):
        return {"status": "unknown", "hours_to_threshold": None}
    latest = stats.get("latest_percent")
    slope = stats.get("slope_percent_per_hour", 0)
    p95 = stats.get("p95_percent")
    if latest is None:
        return {"status": "unknown", "hours_to_threshold": None}
    if latest >= threshold_percent or (p95 is not None and p95 >= threshold_percent):
        return {
            "status": "at_or_above_threshold",
            "hours_to_threshold": 0,
            "threshold_percent": threshold_percent,
        }
    if slope <= 0:
        return {
            "status": "not_projected",
            "hours_to_threshold": None,
            "threshold_percent": threshold_percent,
        }
    hours_to_threshold = round((threshold_percent - latest) / slope, 1)
    return {
        "status": "projected",
        "hours_to_threshold": hours_to_threshold,
        "threshold_percent": threshold_percent,
    }


def _capacity_stats(series: list[Dict[str, Any]], bottleneck_percent: float) -> Dict[str, Any]:
    result: Dict[str, Any] = {}
    for resource, field in (
        ("cpu", "cpu_avg_percent"),
        ("memory", "memory_avg_percent"),
        ("disk", "disk_avg_percent"),
    ):
        stats = _series_stats(series, field)
        stats["trend"] = _trend_direction(stats)
        stats["bottleneck_prediction"] = _bottleneck_prediction(stats, bottleneck_percent)
        result[resource] = stats
    return result


def _current_node_count(nodes: Dict[str, Any]) -> int:
    if not nodes.get("success"):
        return 0
    visible_nodes = nodes.get("nodes", []) or []
    ready_nodes = [
        node for node in visible_nodes
        if str(node.get("ready", node.get("status", "True"))).lower() not in {"false", "notready"}
    ]
    return len(ready_nodes) or len(visible_nodes)


def _nodepool_autoscaling(nodepools: Dict[str, Any], current_nodes: int) -> Dict[str, Any]:
    pools: list[Dict[str, Any]] = []
    enabled = False
    min_nodes = 0
    max_nodes = 0
    for pool in nodepools.get("nodepools", []) or []:
        pool_entry = {
            "name": pool.get("name") or pool.get("id") or "unknown",
            "enabled": False,
            "min_node_count": None,
            "max_node_count": None,
            "scale_down_cooldown_time": None,
            "scale_groups": [],
        }
        for group in pool.get("scale_groups", []) or []:
            autoscaling = group.get("autoscaling") or {}
            group_enabled = bool(autoscaling.get("enable") or autoscaling.get("enabled") or pool.get("autoscaling_enabled"))
            group_min = autoscaling.get("min_node_count") or group.get("min_node_count")
            group_max = autoscaling.get("max_node_count") or group.get("max_node_count")
            if group_enabled:
                enabled = True
                pool_entry["enabled"] = True
                if group_min is not None:
                    min_nodes += int(group_min)
                if group_max is not None:
                    max_nodes += int(group_max)
                pool_entry["min_node_count"] = group_min
                pool_entry["max_node_count"] = group_max
                pool_entry["scale_down_cooldown_time"] = autoscaling.get("scale_down_cooldown_time")
            pool_entry["scale_groups"].append({
                "name": group.get("name"),
                "enabled": group_enabled,
                "min_node_count": group_min,
                "max_node_count": group_max,
            })
        pools.append(pool_entry)

    if not enabled:
        min_nodes = current_nodes
        max_nodes = current_nodes
    else:
        if min_nodes <= 0:
            min_nodes = max(1, current_nodes)
        if max_nodes <= 0:
            max_nodes = max(min_nodes, current_nodes)

    return {
        "enabled": enabled,
        "current_nodes": current_nodes,
        "min_nodes": min_nodes,
        "max_nodes": max(max_nodes, min_nodes),
        "nodepools": pools,
    }


def _business_deployments(
    deployments: Dict[str, Any],
    excluded_namespaces: Iterable[str],
    business_namespaces: Iterable[str],
) -> list[Dict[str, Any]]:
    excluded = set(excluded_namespaces)
    included = set(business_namespaces)
    result = []
    for deployment in deployments.get("deployments", []) or []:
        namespace = deployment.get("namespace")
        if not namespace or namespace in excluded:
            continue
        if included and namespace not in included:
            continue
        result.append(deployment)
    return result


def _hpa_target_key(hpa: Dict[str, Any]) -> Optional[str]:
    target = hpa.get("scale_target_ref") or {}
    kind = target.get("kind")
    name = target.get("name")
    namespace = hpa.get("namespace")
    if not namespace or not kind or not name:
        return None
    return f"{str(kind).lower()}/{namespace}/{name}"


def _hpa_targets(hpas: Dict[str, Any]) -> set[str]:
    targets = set()
    for hpa in hpas.get("hpas", []) or []:
        key = _hpa_target_key(hpa)
        if key:
            targets.add(key)
    return targets


def _hpa_metric_targets(hpa: Dict[str, Any]) -> Dict[str, Any]:
    targets: Dict[str, Any] = {}
    for metric in hpa.get("metrics", []) or []:
        resource = metric.get("resource") if isinstance(metric, dict) else None
        if not resource:
            continue
        name = resource.get("name")
        target = resource.get("target") or {}
        if name:
            targets[name] = target.get("average_utilization") or target.get("averageUtilization")
    return targets


def _elasticity_summary(
    nodepools: Dict[str, Any],
    hpas: Dict[str, Any],
    deployments: Dict[str, Any],
    excluded_namespaces: Iterable[str],
    business_namespaces: Iterable[str],
    current_nodes: int,
) -> Dict[str, Any]:
    business = _business_deployments(deployments, excluded_namespaces, business_namespaces)
    hpa_target_keys = _hpa_targets(hpas)
    business_keys = {f"deployment/{item.get('namespace')}/{item.get('name')}" for item in business}
    covered = business_keys.intersection(hpa_target_keys)
    autoscaler = _nodepool_autoscaling(nodepools, current_nodes)
    existing_hpas = hpas.get("hpas", []) if hpas.get("success") else []
    return {
        "node_autoscaler": autoscaler,
        "hpa": {
            "status": "configured" if existing_hpas else "not_configured",
            "count": len(existing_hpas),
            "business_deployments": len(business),
            "covered_business_deployments": len(covered),
            "coverage_percent": round(len(covered) / len(business) * 100, 2) if business else None,
            "existing_hpas": [
                {
                    "namespace": hpa.get("namespace"),
                    "name": hpa.get("name"),
                    "target": hpa.get("scale_target_ref"),
                    "min_replicas": hpa.get("min_replicas"),
                    "max_replicas": hpa.get("max_replicas"),
                    "current_replicas": hpa.get("current_replicas"),
                    "desired_replicas": hpa.get("desired_replicas"),
                    "metric_targets": _hpa_metric_targets(hpa),
                }
                for hpa in existing_hpas
            ],
        },
    }


def _simulate_node_capacity(
    series: list[Dict[str, Any]],
    current_nodes: int,
    min_nodes: int,
    max_nodes: int,
    target_cpu_percent: float,
    target_memory_percent: float,
    headroom_percent: float,
) -> Dict[str, Any]:
    if current_nodes <= 0 or not series:
        return {
            "status": "insufficient_data",
            "series": [],
            "avg_recommended_nodes": None,
            "max_recommended_nodes": None,
        }

    rows: list[Dict[str, Any]] = []
    previous_nodes: Optional[int] = None
    scale_events = 0
    capped_samples = 0
    headroom_multiplier = 1 + max(0.0, headroom_percent) / 100.0

    for row in series:
        cpu = row.get("cpu_avg_percent")
        memory = row.get("memory_avg_percent")
        demand_ratios = []
        if cpu is not None and target_cpu_percent > 0:
            demand_ratios.append(float(cpu) / target_cpu_percent)
        if memory is not None and target_memory_percent > 0:
            demand_ratios.append(float(memory) / target_memory_percent)
        if not demand_ratios:
            continue
        raw_required = current_nodes * max(demand_ratios) * headroom_multiplier
        recommended = max(1, math.ceil(raw_required))
        recommended = max(min_nodes, min(max_nodes, recommended))
        if raw_required > max_nodes:
            capped_samples += 1
        if previous_nodes is not None and recommended != previous_nodes:
            scale_events += 1
        previous_nodes = recommended
        rows.append({
            "timestamp": row["timestamp"],
            "time_utc": row["time_utc"],
            "current_nodes": current_nodes,
            "recommended_nodes": recommended,
            "raw_required_nodes": round(raw_required, 2),
            "cpu_avg_percent": cpu,
            "memory_avg_percent": memory,
        })

    if not rows:
        return {
            "status": "insufficient_data",
            "series": [],
            "avg_recommended_nodes": None,
            "max_recommended_nodes": None,
        }

    recommended_values = [row["recommended_nodes"] for row in rows]
    avg_recommended = round(mean(recommended_values), 2)
    avg_reduction = round(current_nodes - avg_recommended, 2)
    return {
        "status": "ok",
        "target_cpu_percent": target_cpu_percent,
        "target_memory_percent": target_memory_percent,
        "headroom_percent": headroom_percent,
        "min_nodes": min_nodes,
        "max_nodes": max_nodes,
        "current_nodes": current_nodes,
        "avg_recommended_nodes": avg_recommended,
        "max_recommended_nodes": max(recommended_values),
        "min_recommended_nodes": min(recommended_values),
        "avg_node_delta_vs_current": avg_reduction,
        "estimated_reducible_nodes": max(0, math.floor(avg_reduction)),
        "scale_event_count": scale_events,
        "capped_sample_count": capped_samples,
        "capped_sample_percent": round(capped_samples / len(rows) * 100, 2),
        "series": rows,
    }


def _hpa_preview(
    deployments: Dict[str, Any],
    hpas: Dict[str, Any],
    excluded_namespaces: Iterable[str],
    business_namespaces: Iterable[str],
    target_cpu_percent: float,
    target_memory_percent: float,
) -> Optional[Dict[str, Any]]:
    covered = _hpa_targets(hpas)
    for deployment in _business_deployments(deployments, excluded_namespaces, business_namespaces):
        key = f"deployment/{deployment.get('namespace')}/{deployment.get('name')}"
        if key in covered:
            continue
        desired = deployment.get("desired_replicas") or deployment.get("replicas") or 1
        max_replicas = max(int(desired) * 3, int(desired) + 2, 3)
        generated = cce_hpa.generate_cce_hpa_manifest(
            workload_name=deployment["name"],
            namespace=deployment["namespace"],
            min_replicas=max(1, int(desired)),
            max_replicas=max_replicas,
            workload_type="deployment",
            target_cpu_utilization=int(round(target_cpu_percent)),
            target_memory_utilization=int(round(target_memory_percent)),
            behavior={
                "scaleUp": {
                    "stabilizationWindowSeconds": 60,
                    "policies": [{"type": "Percent", "value": 100, "periodSeconds": 60}],
                    "selectPolicy": "Max",
                },
                "scaleDown": {
                    "stabilizationWindowSeconds": 300,
                    "policies": [{"type": "Percent", "value": 50, "periodSeconds": 60}],
                    "selectPolicy": "Max",
                },
            },
        )
        if generated.get("success"):
            return generated
    return None


def _recommendations(
    stats: Dict[str, Any],
    elasticity: Dict[str, Any],
    simulation: Dict[str, Any],
    hpa_preview: Optional[Dict[str, Any]],
) -> list[Dict[str, Any]]:
    recommendations: list[Dict[str, Any]] = []
    cpu = stats.get("cpu", {})
    memory = stats.get("memory", {})
    autoscaler = elasticity.get("node_autoscaler", {})
    hpa = elasticity.get("hpa", {})

    if cpu.get("bottleneck_prediction", {}).get("status") in {"projected", "at_or_above_threshold"}:
        recommendations.append({
            "id": "cpu-bottleneck-watch",
            "priority": "high",
            "area": "capacity",
            "reason": "CPU trend is projected to hit the configured bottleneck threshold or already touched it.",
            "suggestion": "Keep more short-term headroom, lower HPA target CPU if workload HPA exists, and verify node autoscaler max_nodes is enough.",
            "configuration_method": [
                "Review huawei_list_cce_hpas output and adjust target_cpu_utilization in huawei_configure_cce_hpa preview.",
                "Review nodepool autoscaler max_nodes in CCE before increasing traffic.",
            ],
        })

    if memory.get("bottleneck_prediction", {}).get("status") in {"projected", "at_or_above_threshold"}:
        recommendations.append({
            "id": "memory-bottleneck-watch",
            "priority": "high",
            "area": "capacity",
            "reason": "Memory trend is projected to hit the configured bottleneck threshold or already touched it.",
            "suggestion": "Prefer request/right-sizing first, then tune HPA memory target or keep node autoscaler headroom.",
            "configuration_method": [
                "Generate or preview HPA with target_memory_utilization through huawei_configure_cce_hpa.",
                "Do not reduce nodepool min_nodes until memory p95 has stabilized below the target.",
            ],
        })

    low_cpu = cpu.get("p95_percent") is not None and cpu["p95_percent"] < 45
    low_memory = memory.get("p95_percent") is not None and memory["p95_percent"] < 55
    if low_cpu and low_memory and simulation.get("estimated_reducible_nodes", 0) > 0:
        recommendations.append({
            "id": "cost-lower-baseline-capacity",
            "priority": "medium",
            "area": "cost",
            "reason": "Simulation shows the observed demand can run with fewer average nodes while keeping configured headroom.",
            "suggestion": "Lower nodepool min_nodes gradually or shorten scale-down cooldown after a business review.",
            "configuration_method": [
                "Change nodepool autoscaler min/max bounds in CCE after approval.",
                "Use huawei_resize_cce_nodepool only for an explicitly confirmed one-time node count change.",
            ],
        })

    if not autoscaler.get("enabled"):
        recommendations.append({
            "id": "enable-node-autoscaler",
            "priority": "medium",
            "area": "elasticity",
            "reason": "Node autoscaler is not configured, so workload or traffic changes cannot be absorbed by node capacity automatically.",
            "suggestion": "Enable autoscaling for eligible node pools with a conservative min/max bound derived from simulation.",
            "configuration_method": [
                f"Suggested min_nodes={simulation.get('min_recommended_nodes')}, max_nodes={simulation.get('max_recommended_nodes')} based on current simulation.",
                "Apply through CCE nodepool autoscaling configuration or IaC after approval.",
            ],
        })
    elif simulation.get("capped_sample_count", 0) > 0:
        recommendations.append({
            "id": "raise-autoscaler-max",
            "priority": "high",
            "area": "elasticity",
            "reason": "Simulation was capped by current node autoscaler max_nodes in some samples.",
            "suggestion": "Raise max_nodes or add an elastic node pool before traffic grows further.",
            "configuration_method": [
                "Increase nodepool autoscaler max_nodes after capacity and quota review.",
            ],
        })

    coverage = hpa.get("coverage_percent")
    if coverage is not None and coverage < 80:
        item = {
            "id": "increase-hpa-coverage",
            "priority": "medium",
            "area": "workload-elasticity",
            "reason": "Not enough business Deployments are covered by HPA.",
            "suggestion": "Generate HPA previews for stable business Deployments and apply only after request sizing is reviewed.",
            "configuration_method": [
                "Run huawei_generate_cce_hpa_manifest for each selected Deployment.",
                "Run huawei_configure_cce_hpa without confirm=true for preview, then confirm=true only after explicit approval.",
            ],
        }
        if hpa_preview:
            item["preview"] = {
                "hpa_name": hpa_preview.get("hpa_name"),
                "namespace": hpa_preview.get("namespace"),
                "workload_name": hpa_preview.get("workload_name"),
                "manifest_yaml": hpa_preview.get("manifest_yaml"),
            }
        recommendations.append(item)

    if not recommendations:
        recommendations.append({
            "id": "observe-current-capacity",
            "priority": "low",
            "area": "observation",
            "reason": "No strong bottleneck or cost optimization signal was found in the selected window.",
            "suggestion": "Keep periodic records and compare the next cycle before changing elasticity parameters.",
            "configuration_method": ["Schedule this action every 6h, daily, weekly, or monthly as needed."],
        })
    return recommendations


def _read_history(history_dir: Optional[str], limit: int) -> list[Dict[str, Any]]:
    if not history_dir:
        return []
    path = Path(history_dir)
    if not path.exists():
        return []
    records: list[Dict[str, Any]] = []
    for record_path in sorted(path.glob("capacity-trend-*.json"))[-limit:]:
        try:
            records.append(json.loads(record_path.read_text(encoding="utf-8")))
        except (OSError, json.JSONDecodeError):
            continue
    return records


def _history_comparison(current: Dict[str, Any], previous: list[Dict[str, Any]]) -> Dict[str, Any]:
    if not previous:
        return {"available": False, "message": "No previous capacity records found."}
    baseline = previous[-1]
    deltas: Dict[str, Any] = {}
    for resource in ("cpu", "memory", "disk"):
        current_stats = current.get("capacity_stats", {}).get(resource, {})
        previous_stats = baseline.get("capacity_stats", {}).get(resource, {})
        deltas[resource] = {
            "avg_delta_percent": _delta(current_stats.get("avg_percent"), previous_stats.get("avg_percent")),
            "p95_delta_percent": _delta(current_stats.get("p95_percent"), previous_stats.get("p95_percent")),
            "max_delta_percent": _delta(current_stats.get("max_percent"), previous_stats.get("max_percent")),
        }
    return {
        "available": True,
        "compared_record": baseline.get("record_id") or baseline.get("generated_at"),
        "record_count_considered": len(previous),
        "deltas": deltas,
        "previous_action_note": baseline.get("action_note"),
        "previous_recommendation_ids": [
            item.get("id") for item in baseline.get("recommendations", []) if item.get("id")
        ],
    }


def _delta(current: Any, previous: Any) -> Optional[float]:
    if current is None or previous is None:
        return None
    try:
        return round(float(current) - float(previous), 2)
    except (TypeError, ValueError):
        return None


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _chart_points(series: list[Dict[str, Any]], field: str, width: int, height: int, padding: int) -> str:
    points = _values(series, field)
    if not points:
        return ""
    timestamps = [timestamp for timestamp, _ in points]
    values = [value for _, value in points]
    min_ts, max_ts = min(timestamps), max(timestamps)
    max_value = max(max(values), 100.0)
    x_span = max(1, max_ts - min_ts)
    y_span = max(1.0, max_value)
    coords = []
    for timestamp, value in points:
        x = padding + (timestamp - min_ts) / x_span * (width - 2 * padding)
        y = height - padding - value / y_span * (height - 2 * padding)
        coords.append(f"{x:.1f},{y:.1f}")
    return " ".join(coords)


def _render_svg_chart(series: list[Dict[str, Any]], title: str) -> str:
    width = 980
    height = 360
    padding = 48
    cpu_points = _chart_points(series, "cpu_avg_percent", width, height, padding)
    memory_points = _chart_points(series, "memory_avg_percent", width, height, padding)
    disk_points = _chart_points(series, "disk_avg_percent", width, height, padding)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <rect width="100%" height="100%" fill="#ffffff"/>
  <text x="{padding}" y="28" font-family="Arial, sans-serif" font-size="18" fill="#111827">{title}</text>
  <line x1="{padding}" y1="{height-padding}" x2="{width-padding}" y2="{height-padding}" stroke="#d1d5db"/>
  <line x1="{padding}" y1="{padding}" x2="{padding}" y2="{height-padding}" stroke="#d1d5db"/>
  <text x="{padding}" y="{height-14}" font-family="Arial, sans-serif" font-size="12" fill="#6b7280">time</text>
  <text x="8" y="{padding}" font-family="Arial, sans-serif" font-size="12" fill="#6b7280">%</text>
  <polyline points="{cpu_points}" fill="none" stroke="#ef4444" stroke-width="2.5"/>
  <polyline points="{memory_points}" fill="none" stroke="#2563eb" stroke-width="2.5"/>
  <polyline points="{disk_points}" fill="none" stroke="#f59e0b" stroke-width="2.5"/>
  <rect x="{width-230}" y="42" width="180" height="76" rx="6" fill="#f9fafb" stroke="#e5e7eb"/>
  <line x1="{width-212}" y1="64" x2="{width-182}" y2="64" stroke="#ef4444" stroke-width="3"/>
  <text x="{width-172}" y="68" font-family="Arial, sans-serif" font-size="12" fill="#111827">CPU avg</text>
  <line x1="{width-212}" y1="86" x2="{width-182}" y2="86" stroke="#2563eb" stroke-width="3"/>
  <text x="{width-172}" y="90" font-family="Arial, sans-serif" font-size="12" fill="#111827">Memory avg</text>
  <line x1="{width-212}" y1="108" x2="{width-182}" y2="108" stroke="#f59e0b" stroke-width="3"/>
  <text x="{width-172}" y="112" font-family="Arial, sans-serif" font-size="12" fill="#111827">Disk avg</text>
</svg>
"""


def _render_simulation_svg(simulation: Dict[str, Any], title: str) -> str:
    rows = simulation.get("series", []) or []
    width = 980
    height = 320
    padding = 48
    if not rows:
        return _render_svg_chart([], title)
    max_nodes = max(max(row.get("current_nodes", 0), row.get("recommended_nodes", 0)) for row in rows) or 1
    min_ts = min(row["timestamp"] for row in rows)
    max_ts = max(row["timestamp"] for row in rows)
    x_span = max(1, max_ts - min_ts)

    def coords(field: str) -> str:
        points = []
        for row in rows:
            x = padding + (row["timestamp"] - min_ts) / x_span * (width - 2 * padding)
            y = height - padding - float(row.get(field, 0)) / max_nodes * (height - 2 * padding)
            points.append(f"{x:.1f},{y:.1f}")
        return " ".join(points)

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <rect width="100%" height="100%" fill="#ffffff"/>
  <text x="{padding}" y="28" font-family="Arial, sans-serif" font-size="18" fill="#111827">{title}</text>
  <line x1="{padding}" y1="{height-padding}" x2="{width-padding}" y2="{height-padding}" stroke="#d1d5db"/>
  <line x1="{padding}" y1="{padding}" x2="{padding}" y2="{height-padding}" stroke="#d1d5db"/>
  <polyline points="{coords('current_nodes')}" fill="none" stroke="#6b7280" stroke-width="2.5" stroke-dasharray="6 4"/>
  <polyline points="{coords('recommended_nodes')}" fill="none" stroke="#16a34a" stroke-width="2.5"/>
  <rect x="{width-260}" y="42" width="210" height="54" rx="6" fill="#f9fafb" stroke="#e5e7eb"/>
  <line x1="{width-242}" y1="64" x2="{width-212}" y2="64" stroke="#6b7280" stroke-width="3" stroke-dasharray="6 4"/>
  <text x="{width-202}" y="68" font-family="Arial, sans-serif" font-size="12" fill="#111827">Current nodes</text>
  <line x1="{width-242}" y1="86" x2="{width-212}" y2="86" stroke="#16a34a" stroke-width="3"/>
  <text x="{width-202}" y="90" font-family="Arial, sans-serif" font-size="12" fill="#111827">Simulated nodes</text>
</svg>
"""


def _render_report(result: Dict[str, Any]) -> str:
    scope = result["scope"]
    stats = result["capacity_stats"]
    sim = result["simulation"]
    recs = "\n".join(
        f"- [{item['priority']}] {item['id']}: {item['suggestion']}" for item in result["recommendations"]
    )
    gaps = "\n".join(f"- {gap}" for gap in result.get("data_gaps", [])) or "- none"
    history = result.get("history_comparison", {})
    history_text = "No previous records found."
    if history.get("available"):
        delta_lines = []
        for resource, delta in history.get("deltas", {}).items():
            delta_lines.append(
                f"- {resource}: avg {delta.get('avg_delta_percent')}, p95 {delta.get('p95_delta_percent')}, max {delta.get('max_delta_percent')}"
            )
        history_text = "\n".join(delta_lines)

    return f"""# CCE Capacity Trend Forecast Report

Generated at: {result['generated_at']}

## Scope

- Region: {scope['region']}
- Cluster: {scope['cluster_id']}
- Window: {scope['hours']}h
- Step seconds: {scope['step_seconds']}
- Excluded namespaces: {', '.join(scope['excluded_namespaces']) or 'none'}
- Business namespaces: {', '.join(scope['business_namespaces']) or 'all non-excluded namespaces'}

## Capacity Trend

| Resource | Avg % | P95 % | Max % | Latest % | Trend | Slope %/h | Bottleneck |
|---|---:|---:|---:|---:|---|---:|---|
| CPU | {stats['cpu'].get('avg_percent')} | {stats['cpu'].get('p95_percent')} | {stats['cpu'].get('max_percent')} | {stats['cpu'].get('latest_percent')} | {stats['cpu'].get('trend')} | {stats['cpu'].get('slope_percent_per_hour')} | {stats['cpu'].get('bottleneck_prediction', {}).get('status')} |
| Memory | {stats['memory'].get('avg_percent')} | {stats['memory'].get('p95_percent')} | {stats['memory'].get('max_percent')} | {stats['memory'].get('latest_percent')} | {stats['memory'].get('trend')} | {stats['memory'].get('slope_percent_per_hour')} | {stats['memory'].get('bottleneck_prediction', {}).get('status')} |
| Disk | {stats['disk'].get('avg_percent')} | {stats['disk'].get('p95_percent')} | {stats['disk'].get('max_percent')} | {stats['disk'].get('latest_percent')} | {stats['disk'].get('trend')} | {stats['disk'].get('slope_percent_per_hour')} | {stats['disk'].get('bottleneck_prediction', {}).get('status')} |

## Elasticity

- Node autoscaler enabled: {result['elasticity']['node_autoscaler'].get('enabled')}
- Current nodes: {result['elasticity']['node_autoscaler'].get('current_nodes')}
- Autoscaler bounds: {result['elasticity']['node_autoscaler'].get('min_nodes')} - {result['elasticity']['node_autoscaler'].get('max_nodes')}
- HPA count: {result['elasticity']['hpa'].get('count')}
- HPA business coverage: {result['elasticity']['hpa'].get('coverage_percent')}%

## Simulation

- Status: {sim.get('status')}
- Target CPU: {sim.get('target_cpu_percent')}%
- Target memory: {sim.get('target_memory_percent')}%
- Headroom: {sim.get('headroom_percent')}%
- Avg recommended nodes: {sim.get('avg_recommended_nodes')}
- Max recommended nodes: {sim.get('max_recommended_nodes')}
- Estimated reducible nodes: {sim.get('estimated_reducible_nodes')}
- Capped sample percent: {sim.get('capped_sample_percent')}

## Recommendations

{recs}

## History Comparison

{history_text}

## Data Gaps

{gaps}
"""


def _render_html_report(result: Dict[str, Any], trend_svg: str, simulation_svg: str) -> str:
    scope = result["scope"]
    stats = result["capacity_stats"]
    sim = result["simulation"]
    history = result.get("history_comparison", {})
    history_block = "<p>No previous records found.</p>"
    if history.get("available"):
        rows = []
        for resource, delta in (history.get("deltas") or {}).items():
            rows.append(
                f"<tr><td>{html.escape(str(resource))}</td>"
                f"<td>{delta.get('avg_delta_percent')}</td>"
                f"<td>{delta.get('p95_delta_percent')}</td>"
                f"<td>{delta.get('max_delta_percent')}</td></tr>"
            )
        history_block = (
            "<table><thead><tr><th>Resource</th><th>Avg Delta</th><th>P95 Delta</th><th>Max Delta</th></tr></thead>"
            f"<tbody>{''.join(rows)}</tbody></table>"
        )

    recommendations = "".join(
        "<li>"
        f"<strong>{html.escape(str(item.get('priority')))}</strong> "
        f"{html.escape(str(item.get('id')))}: {html.escape(str(item.get('suggestion')))}"
        "</li>"
        for item in result.get("recommendations", [])
    )
    if not recommendations:
        recommendations = "<li>none</li>"

    data_gaps = "".join(
        f"<li>{html.escape(str(gap))}</li>" for gap in result.get("data_gaps", [])
    ) or "<li>none</li>"

    def _row(resource: str) -> str:
        row = stats[resource]
        return (
            "<tr>"
            f"<td>{resource.upper()}</td>"
            f"<td>{row.get('avg_percent')}</td>"
            f"<td>{row.get('p95_percent')}</td>"
            f"<td>{row.get('max_percent')}</td>"
            f"<td>{row.get('latest_percent')}</td>"
            f"<td>{row.get('trend')}</td>"
            f"<td>{row.get('slope_percent_per_hour')}</td>"
            f"<td>{row.get('bottleneck_prediction', {}).get('status')}</td>"
            "</tr>"
        )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>CCE Capacity Trend Report</title>
<style>
body {{
  margin: 0;
  background: #f4f7fb;
  color: #111827;
  font-family: "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif;
}}
.container {{
  max-width: 1160px;
  margin: 20px auto;
  padding: 0 16px 20px;
}}
.panel {{
  background: #ffffff;
  border: 1px solid #dbe5f1;
  border-radius: 10px;
  margin-bottom: 16px;
  padding: 16px 18px;
}}
h1 {{
  margin: 0 0 10px;
  font-size: 24px;
}}
h2 {{
  margin: 0 0 10px;
  font-size: 18px;
}}
p, li {{
  line-height: 1.5;
}}
table {{
  width: 100%;
  border-collapse: collapse;
}}
th, td {{
  border: 1px solid #dbe5f1;
  padding: 8px 10px;
  text-align: left;
  font-size: 14px;
}}
th {{
  background: #f8fafc;
}}
.meta {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 8px;
}}
.svg-wrap {{
  overflow-x: auto;
}}
</style>
</head>
<body>
<div class="container">
  <div class="panel">
    <h1>CCE Capacity Trend Forecast Report</h1>
    <p>Generated at: {html.escape(str(result["generated_at"]))}</p>
    <div class="meta">
      <div><strong>Region:</strong> {html.escape(str(scope["region"]))}</div>
      <div><strong>Cluster:</strong> {html.escape(str(scope["cluster_id"]))}</div>
      <div><strong>Window:</strong> {scope["hours"]}h</div>
      <div><strong>Step:</strong> {scope["step_seconds"]}s</div>
      <div><strong>Excluded namespaces:</strong> {html.escape(", ".join(scope["excluded_namespaces"]) or "none")}</div>
      <div><strong>Business namespaces:</strong> {html.escape(", ".join(scope["business_namespaces"]) or "all non-excluded namespaces")}</div>
    </div>
  </div>
  <div class="panel">
    <h2>Capacity Trend</h2>
    <table>
      <thead>
        <tr>
          <th>Resource</th><th>Avg %</th><th>P95 %</th><th>Max %</th><th>Latest %</th><th>Trend</th><th>Slope %/h</th><th>Bottleneck</th>
        </tr>
      </thead>
      <tbody>
        {_row("cpu")}
        {_row("memory")}
        {_row("disk")}
      </tbody>
    </table>
    <div class="svg-wrap">{trend_svg}</div>
  </div>
  <div class="panel">
    <h2>Elasticity</h2>
    <ul>
      <li>Node autoscaler enabled: {result["elasticity"]["node_autoscaler"].get("enabled")}</li>
      <li>Current nodes: {result["elasticity"]["node_autoscaler"].get("current_nodes")}</li>
      <li>Autoscaler bounds: {result["elasticity"]["node_autoscaler"].get("min_nodes")} - {result["elasticity"]["node_autoscaler"].get("max_nodes")}</li>
      <li>HPA count: {result["elasticity"]["hpa"].get("count")}</li>
      <li>HPA business coverage: {result["elasticity"]["hpa"].get("coverage_percent")}%</li>
    </ul>
  </div>
  <div class="panel">
    <h2>Simulation</h2>
    <ul>
      <li>Status: {sim.get("status")}</li>
      <li>Target CPU: {sim.get("target_cpu_percent")}%</li>
      <li>Target memory: {sim.get("target_memory_percent")}%</li>
      <li>Headroom: {sim.get("headroom_percent")}%</li>
      <li>Avg recommended nodes: {sim.get("avg_recommended_nodes")}</li>
      <li>Max recommended nodes: {sim.get("max_recommended_nodes")}</li>
      <li>Estimated reducible nodes: {sim.get("estimated_reducible_nodes")}</li>
      <li>Capped sample percent: {sim.get("capped_sample_percent")}</li>
    </ul>
    <div class="svg-wrap">{simulation_svg}</div>
  </div>
  <div class="panel">
    <h2>Recommendations</h2>
    <ul>{recommendations}</ul>
  </div>
  <div class="panel">
    <h2>History Comparison</h2>
    {history_block}
  </div>
  <div class="panel">
    <h2>Data Gaps</h2>
    <ul>{data_gaps}</ul>
  </div>
</div>
</body>
</html>
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
    summary_path = target_dir / "capacity-trend-summary.json"
    report_path = target_dir / "capacity-trend-report.md"
    report_html_path = target_dir / "capacity-trend-report.html"
    chart_path = target_dir / "capacity-trend-chart.svg"
    simulation_chart_path = target_dir / "capacity-simulation-chart.svg"
    trend_svg = _render_svg_chart(result["capacity_series"], "CCE capacity trend")
    simulation_svg = _render_simulation_svg(result["simulation"], "CCE capacity simulation")

    _write_json(summary_path, result)
    report_path.write_text(_render_report(result), encoding="utf-8")
    report_html_path.write_text(_render_html_report(result, trend_svg, simulation_svg), encoding="utf-8")
    chart_path.write_text(trend_svg, encoding="utf-8")
    simulation_chart_path.write_text(simulation_svg, encoding="utf-8")

    files = {
        "summary": str(summary_path),
        "report": str(report_path),
        "report_html": str(report_html_path),
        "trend_chart": str(chart_path),
        "simulation_chart": str(simulation_chart_path),
    }
    if include_raw:
        raw_dir = target_dir / "raw"
        raw_dir.mkdir(parents=True, exist_ok=True)
        for name, payload in raw_collections.items():
            raw_path = raw_dir / f"{name}.response.json"
            _write_json(raw_path, payload)
            files[f"raw_{name}"] = str(raw_path)
    return files


def _write_history(history_dir: Optional[str], result: Dict[str, Any]) -> Optional[str]:
    if not history_dir:
        return None
    target_dir = Path(history_dir)
    target_dir.mkdir(parents=True, exist_ok=True)
    generated = result["generated_at"].replace(":", "").replace("-", "")
    record_path = target_dir / f"capacity-trend-{generated}.json"
    record = {
        "record_id": record_path.stem,
        "generated_at": result["generated_at"],
        "scope": result["scope"],
        "capacity_stats": result["capacity_stats"],
        "simulation": {
            key: value for key, value in result["simulation"].items() if key != "series"
        },
        "elasticity": result["elasticity"],
        "recommendations": result["recommendations"],
        "action_note": result.get("action_note"),
        "files": result.get("files", {}),
    }
    _write_json(record_path, record)
    jsonl_path = target_dir / "capacity-trend-history.jsonl"
    with jsonl_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")
    return str(record_path)


def _data_gap(name: str, response: Dict[str, Any]) -> Optional[str]:
    if response.get("success"):
        return None
    return f"{name}: {response.get('error', 'collection failed')}"


def _cluster_name(clusters: Dict[str, Any], cluster_id: str) -> str:
    for cluster in clusters.get("clusters", []) or []:
        if cluster.get("id") == cluster_id:
            return cluster.get("name") or cluster_id
    return cluster_id


def analyze_cce_capacity_trend(
    region: str,
    cluster_id: str,
    ak: Optional[str] = None,
    sk: Optional[str] = None,
    project_id: Optional[str] = None,
    hours: int = 168,
    step_seconds: int = 3600,
    top_n: int = 200,
    exclude_namespaces: Optional[str | Iterable[str]] = None,
    business_namespaces: Optional[str | Iterable[str]] = None,
    output_dir: Optional[str] = None,
    history_dir: Optional[str] = None,
    record_history: bool = True,
    compare_history_count: int = 8,
    include_raw: bool = False,
    target_cpu_percent: float = DEFAULT_TARGET_CPU_PERCENT,
    target_memory_percent: float = DEFAULT_TARGET_MEMORY_PERCENT,
    bottleneck_percent: float = DEFAULT_BOTTLENECK_PERCENT,
    headroom_percent: float = DEFAULT_HEADROOM_PERCENT,
    action_note: Optional[str] = None,
) -> Dict[str, Any]:
    """Analyze periodic CCE capacity trends and forecast bottlenecks."""
    if not region:
        return {"success": False, "error": "region is required"}
    if not cluster_id:
        return {"success": False, "error": "cluster_id is required"}

    hours = _clamp_int(hours, MIN_WINDOW_HOURS, MAX_WINDOW_HOURS)
    step_seconds = _clamp_int(step_seconds, 60, 24 * 3600)
    excluded = _as_list(exclude_namespaces, DEFAULT_EXCLUDED_NAMESPACES)
    business = _as_list(business_namespaces)
    if history_dir is None and output_dir:
        history_dir = str(Path(output_dir) / "history")
    previous_history = _read_history(history_dir, compare_history_count)

    raw: Dict[str, Dict[str, Any]] = {
        "clusters": cce.list_cce_clusters(region, ak, sk, project_id, limit=100),
        "nodes": cce.get_kubernetes_nodes(region, cluster_id, ak, sk, project_id),
        "nodepools": cce.list_cce_node_pools(region, cluster_id, ak, sk, project_id, limit=100),
        "deployments": cce.get_kubernetes_deployments(region, cluster_id, ak, sk, project_id),
        "hpas": cce_hpa.list_cce_hpas(region, cluster_id, ak, sk, project_id, include_system=False),
    }

    current_nodes = _current_node_count(raw["nodes"])
    effective_top_n = max(top_n, current_nodes or top_n)
    raw["node_metrics"] = cce_metrics.get_cce_node_metrics_topN(
        region,
        cluster_id,
        ak,
        sk,
        project_id,
        top_n=effective_top_n,
        hours=hours,
    )

    # Keep AOM discovery visible in raw output because missing AOM explains missing trend data.
    try:
        raw["aom_instance"] = cce_diagnosis.get_aom_instance(region, cluster_id, ak, sk, project_id)
    except Exception as exc:  # pragma: no cover - defensive around SDK/environment drift.
        raw["aom_instance"] = {"success": False, "error": str(exc), "error_type": type(exc).__name__}

    data_gaps = [gap for name, response in raw.items() if (gap := _data_gap(name, response))]
    if not raw["node_metrics"].get("success"):
        return {
            "success": False,
            "error": "node metrics collection failed",
            "data_gaps": data_gaps,
        }

    capacity_series = _align_capacity_series(
        _average_series(raw["node_metrics"], "cpu_top_n"),
        _average_series(raw["node_metrics"], "memory_top_n"),
        _average_series(raw["node_metrics"], "disk_top_n"),
    )
    capacity_stats = _capacity_stats(capacity_series, bottleneck_percent)
    elasticity = _elasticity_summary(raw["nodepools"], raw["hpas"], raw["deployments"], excluded, business, current_nodes)
    autoscaler = elasticity["node_autoscaler"]
    simulation = _simulate_node_capacity(
        capacity_series,
        current_nodes=current_nodes,
        min_nodes=int(autoscaler.get("min_nodes") or current_nodes or 1),
        max_nodes=int(autoscaler.get("max_nodes") or current_nodes or 1),
        target_cpu_percent=float(target_cpu_percent),
        target_memory_percent=float(target_memory_percent),
        headroom_percent=float(headroom_percent),
    )
    hpa_preview = _hpa_preview(
        raw["deployments"],
        raw["hpas"],
        excluded,
        business,
        target_cpu_percent=float(target_cpu_percent),
        target_memory_percent=float(target_memory_percent),
    )

    result: Dict[str, Any] = {
        "success": True,
        "action": "analyze_cce_capacity_trend",
        "generated_at": _utc_now(),
        "cluster_name": _cluster_name(raw["clusters"], cluster_id),
        "scope": {
            "region": region,
            "cluster_id": cluster_id,
            "hours": hours,
            "step_seconds": step_seconds,
            "top_n": effective_top_n,
            "excluded_namespaces": excluded,
            "business_namespaces": business,
        },
        "capacity_series": capacity_series,
        "capacity_stats": capacity_stats,
        "elasticity": elasticity,
        "simulation": simulation,
        "recommendations": _recommendations(capacity_stats, elasticity, simulation, hpa_preview),
        "history_comparison": {},
        "data_gaps": data_gaps,
        "action_note": action_note,
    }
    result["history_comparison"] = _history_comparison(result, previous_history)
    files = _write_outputs(output_dir, result, raw, include_raw)
    result["files"] = files
    history_record = _write_history(history_dir, result) if record_history else None
    if history_record:
        result["files"]["history_record"] = history_record
    if files.get("summary"):
        _write_json(Path(files["summary"]), result)
    return result
