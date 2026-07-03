"""CCE ops report generator action."""

from __future__ import annotations

import html
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, Optional

from . import cce_auto_inspection, cce_availability_risk, cce_capacity_trend, cce_cost_optimization


DEFAULT_EXCLUDED_NAMESPACES = ("kube-system",)
DEFAULT_GATEWAY_KEYWORDS = ("nginx", "gateway", "ingress", "kong", "apisix", "traefik", "envoy")
REPORT_TYPES = {"weekly", "monthly", "sla", "capacity", "stability"}
DEFAULT_HOURS_BY_REPORT_TYPE = {
    "weekly": 24 * 7,
    "monthly": 24 * 30,
    "sla": 24 * 30,
    "capacity": 24 * 7,
    "stability": 24 * 7,
}


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _as_list(value: Optional[str | Iterable[str]], default: Iterable[str] = ()) -> list[str]:
    if value is None:
        return [item for item in default if item]
    if isinstance(value, str):
        return [item.strip() for item in value.split(",") if item.strip()]
    return [str(item).strip() for item in value if str(item).strip()]


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _read_text(path: Optional[str]) -> Optional[str]:
    if not path:
        return None
    candidate = Path(path)
    if not candidate.exists():
        return None
    try:
        return candidate.read_text(encoding="utf-8")
    except OSError:
        return None


def _extract_oncall(oncall_report_path: Optional[str], oncall_summary: Optional[str]) -> Dict[str, Any]:
    if oncall_summary:
        return {
            "status": "provided",
            "source": "inline",
            "summary": oncall_summary.strip(),
            "details": None,
        }

    if not oncall_report_path:
        return {
            "status": "missing",
            "source": None,
            "summary": "oncall-copilot report not provided",
            "details": None,
        }

    path = Path(oncall_report_path)
    if not path.exists():
        return {
            "status": "missing",
            "source": str(path),
            "summary": "oncall-copilot report path does not exist",
            "details": None,
        }

    try:
        if path.suffix.lower() == ".json":
            payload = json.loads(path.read_text(encoding="utf-8"))
            summary = payload.get("summary") if isinstance(payload, dict) else None
            return {
                "status": "provided",
                "source": str(path),
                "summary": str(summary) if summary else "oncall-copilot JSON loaded",
                "details": payload,
            }
        content = path.read_text(encoding="utf-8")
    except (OSError, json.JSONDecodeError) as exc:
        return {
            "status": "error",
            "source": str(path),
            "summary": f"failed to read oncall-copilot report: {exc}",
            "details": None,
        }

    snippet = content.strip().splitlines()
    return {
        "status": "provided",
        "source": str(path),
        "summary": snippet[0][:200] if snippet else "oncall-copilot report loaded",
        "details": {"preview": "\n".join(snippet[:40])},
    }


def _daily_summary(result: Dict[str, Any]) -> Dict[str, Any]:
    quick = result.get("quick_check", result)
    anomalies = quick.get("anomaly_details", []) if isinstance(quick, dict) else []
    normal_details = quick.get("normal_details", []) if isinstance(quick, dict) else []
    has_anomaly = bool(quick.get("has_anomaly")) if isinstance(quick, dict) else False
    recovery_plan = result.get("recovery_plan", []) if isinstance(result, dict) else []
    return {
        "status": "anomaly" if has_anomaly else "healthy",
        "has_anomaly": has_anomaly,
        "anomaly_count": len(anomalies),
        "anomalies": anomalies[:20],
        "normal_details": normal_details[:20],
        "recovery_plan_count": len(recovery_plan),
        "message": result.get("message"),
    }


def _capacity_summary(result: Dict[str, Any]) -> Dict[str, Any]:
    stats = result.get("capacity_stats", {})
    simulation = result.get("simulation", {})
    elasticity = result.get("elasticity", {})
    return {
        "cpu_avg_percent": stats.get("cpu", {}).get("avg_percent"),
        "memory_avg_percent": stats.get("memory", {}).get("avg_percent"),
        "cpu_p95_percent": stats.get("cpu", {}).get("p95_percent"),
        "memory_p95_percent": stats.get("memory", {}).get("p95_percent"),
        "cpu_trend": stats.get("cpu", {}).get("trend"),
        "memory_trend": stats.get("memory", {}).get("trend"),
        "node_autoscaler_enabled": elasticity.get("node_autoscaler", {}).get("enabled"),
        "hpa_coverage_percent": elasticity.get("hpa", {}).get("coverage_percent"),
        "simulation_status": simulation.get("status"),
        "estimated_reducible_nodes": simulation.get("estimated_reducible_nodes"),
    }


def _availability_summary(result: Dict[str, Any]) -> Dict[str, Any]:
    summary = result.get("summary", {})
    return {
        "risk_level": summary.get("risk_level"),
        "issue_count": summary.get("issue_count"),
        "critical": summary.get("critical"),
        "high": summary.get("high"),
        "medium": summary.get("medium"),
        "low": summary.get("low"),
    }


def _cost_summary(result: Dict[str, Any]) -> Dict[str, Any]:
    low_utilization = result.get("low_utilization", {})
    request_analysis = result.get("request_analysis", {})
    elasticity = result.get("elasticity", {})
    return {
        "cluster_average_below_threshold": low_utilization.get("cluster_average_below_threshold", {}),
        "nodes_clearly_below_average": len(low_utilization.get("nodes_clearly_below_average", []) or []),
        "oversized_requests": len(request_analysis.get("oversized_requests", []) or []),
        "hpa_status": elasticity.get("hpa", {}).get("status"),
        "node_autoscaler_status": elasticity.get("node_autoscaler", {}).get("status"),
    }


def _to_float(value: Any) -> Optional[float]:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _normalize_risk(value: Any, default: str = "low") -> str:
    normalized = str(value or "").strip().lower()
    if normalized in {"critical", "high", "medium", "low", "info"}:
        return normalized
    return default


def _daily_risk(summary: Dict[str, Any]) -> str:
    if summary.get("has_anomaly") or (summary.get("anomaly_count") or 0) > 0:
        return "high"
    return "low"


def _availability_risk(summary: Dict[str, Any]) -> str:
    return _normalize_risk(summary.get("risk_level"), "medium")


def _capacity_risk(summary: Dict[str, Any]) -> str:
    cpu_p95 = _to_float(summary.get("cpu_p95_percent"))
    memory_p95 = _to_float(summary.get("memory_p95_percent"))
    simulation_status = str(summary.get("simulation_status") or "").lower()
    if (cpu_p95 is not None and cpu_p95 >= 80) or (memory_p95 is not None and memory_p95 >= 80):
        return "high"
    if (cpu_p95 is not None and cpu_p95 >= 65) or (memory_p95 is not None and memory_p95 >= 65):
        return "medium"
    if simulation_status in {"insufficient_data", "error"}:
        return "medium"
    return "low"


def _cost_risk(summary: Dict[str, Any]) -> str:
    oversized = int(summary.get("oversized_requests") or 0)
    low_nodes = int(summary.get("nodes_clearly_below_average") or 0)
    low_cluster = any(bool(value) for value in (summary.get("cluster_average_below_threshold") or {}).values())
    if oversized > 0:
        return "high"
    if low_nodes > 0 or low_cluster:
        return "medium"
    return "low"


def _oncall_risk(summary: Dict[str, Any]) -> str:
    status = str(summary.get("status") or "").lower()
    if status in {"missing", "error"}:
        return "medium"
    if status == "provided":
        return "low"
    return "info"


def _risk_upper(value: Any) -> str:
    normalized = _normalize_risk(value, "info")
    icon = {
        "critical": "🔴",
        "high": "🔴",
        "medium": "🟡",
        "low": "🟢",
        "info": "🔵",
    }.get(normalized, "⚪")
    return f"{icon} {normalized.upper()}"


def _md_cell(value: Any) -> str:
    if value is None:
        return "-"
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def _markdown_table(headers: list[str], rows: list[list[Any]]) -> str:
    header = "| " + " | ".join(headers) + " |"
    divider = "| " + " | ".join(["---"] * len(headers)) + " |"
    if not rows:
        rows = [["-"] + [""] * (len(headers) - 1)]
    body = "\n".join("| " + " | ".join(_md_cell(cell) for cell in row) + " |" for row in rows)
    return "\n".join([header, divider, body])


def _html_table(headers: list[str], rows: list[list[Any]]) -> str:
    if not rows:
        rows = [["-"] + [""] * (len(headers) - 1)]
    head = "".join(f"<th>{html.escape(str(item))}</th>" for item in headers)
    body_rows = []
    for row in rows:
        cells = "".join(f"<td>{html.escape('-' if cell is None else str(cell))}</td>" for cell in row)
        body_rows.append(f"<tr>{cells}</tr>")
    body = "".join(body_rows)
    return f"<table class=\"report-table\"><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>"


def _infer_cost_recommendation_risk(text: str) -> str:
    lowered = text.lower()
    if "below 30%" in lowered or "oversized" in lowered:
        return "high"
    if "not configured" in lowered or "not found" in lowered:
        return "medium"
    return "medium"


def _infer_gap_risk(text: str) -> str:
    lowered = text.lower()
    if "request ratio metrics missing" in lowered:
        return "low"
    if (
        "credentials not provided" in lowered
        or "runtime error" in lowered
        or "collection failed" in lowered
        or "request is invalid" in lowered
        or "could not be verified" in lowered
        or "not visible from the kubernetes api" in lowered
    ):
        return "high"
    if "missing" in lowered or "not provided" in lowered:
        return "medium"
    return "medium"


def _collect_data_gap_rows(gaps: list[str]) -> list[Dict[str, str]]:
    rows: list[Dict[str, str]] = []
    for item in gaps:
        raw = str(item)
        if ":" in raw:
            source, message = raw.split(":", 1)
            source = source.strip() or "unknown"
            message = message.strip()
        else:
            source, message = "unknown", raw
        rows.append({
            "source": source,
            "risk_level": _infer_gap_risk(message),
            "message": message,
        })
    if not rows:
        rows.append({
            "source": "report",
            "risk_level": "low",
            "message": "No data gaps detected.",
        })
    return rows[:120]


def _collect_recommendations(
    daily: Dict[str, Any],
    capacity: Dict[str, Any],
    availability: Dict[str, Any],
    cost: Dict[str, Any],
    oncall: Dict[str, Any],
) -> list[Dict[str, str]]:
    recommendations: list[Dict[str, str]] = []
    if daily.get("has_anomaly"):
        recommendations.append({
            "source": "daily-cluster-inspector",
            "risk_level": "high",
            "message": "Daily inspection detected anomalies. Prioritize quick mitigation and verify recovery plan.",
        })
    availability_risk = _normalize_risk(availability.get("summary", {}).get("risk_level"), "medium")
    for item in availability.get("recommendations", [])[:8]:
        recommendations.append({
            "source": "availability-risk-scanner",
            "risk_level": availability_risk,
            "message": str(item),
        })
    for item in cost.get("recommendations", [])[:8]:
        message = str(item)
        recommendations.append({
            "source": "cost-optimization-advisor",
            "risk_level": _infer_cost_recommendation_risk(message),
            "message": message,
        })
    for item in capacity.get("recommendations", [])[:8]:
        suggestion = item.get("suggestion") if isinstance(item, dict) else str(item)
        priority = item.get("priority") if isinstance(item, dict) else "info"
        recommendations.append({
            "source": "capacity-trend-forecaster",
            "risk_level": _normalize_risk(priority, "medium"),
            "message": str(suggestion),
        })
    if oncall.get("status") == "provided":
        recommendations.append({
            "source": "oncall-copilot",
            "risk_level": "low",
            "message": "Include unresolved incidents and action owners in this cycle report.",
        })
    elif oncall.get("status") == "missing":
        recommendations.append({
            "source": "oncall-copilot",
            "risk_level": "medium",
            "message": "Add on-call incident summary to improve SLA and stability context.",
        })
    if not recommendations:
        recommendations.append({
            "source": "report",
            "risk_level": "low",
            "message": "No major risk found in current scope.",
        })
    return recommendations[:40]


def _read_svg(path: Optional[str]) -> str:
    text = _read_text(path)
    if not text:
        return ""
    return text if "<svg" in text else ""


def _report_title(report_type: str) -> str:
    labels = {
        "weekly": "Weekly Operations Report",
        "monthly": "Monthly Operations Report",
        "sla": "SLA Report",
        "capacity": "Capacity Report",
        "stability": "Stability Report",
    }
    return labels.get(report_type, "Operations Report")


def _render_markdown(report: Dict[str, Any]) -> str:
    scope = report["scope"]
    summary = report["summary"]
    daily = summary["daily_cluster_inspector"]
    availability = summary["availability_risk_scanner"]
    cost = summary["cost_optimization_advisor"]
    capacity = summary["capacity_trend_forecaster"]
    oncall = summary["oncall_copilot"]
    daily_risk = _daily_risk(daily)
    availability_risk = _availability_risk(availability)
    cost_risk = _cost_risk(cost)
    capacity_risk = _capacity_risk(capacity)
    oncall_risk = _oncall_risk(oncall)

    scope_table = _markdown_table(
        ["Field", "Value"],
        [
            ["Region", scope["region"]],
            ["Cluster", scope["cluster_id"]],
            ["Report type", report["report"]["type"]],
            ["Window hours", report["report"]["hours"]],
            ["Excluded namespaces", ", ".join(scope["excluded_namespaces"]) or "none"],
            ["Business namespaces", ", ".join(scope["business_namespaces"]) or "all non-excluded namespaces"],
        ],
    )
    executive_table = _markdown_table(
        ["Module", "Signal", "Value", "Risk Level"],
        [
            ["Daily Cluster Inspector", "Status", f"{daily['status']} (anomalies={daily['anomaly_count']})", _risk_upper(daily_risk)],
            ["Availability Risk Scanner", "Risk and issues", f"{availability.get('risk_level')} / {availability.get('issue_count')}", _risk_upper(availability_risk)],
            ["Cost Optimization Advisor", "Cost signals", f"oversized={cost.get('oversized_requests')}, low_nodes={cost.get('nodes_clearly_below_average')}", _risk_upper(cost_risk)],
            ["Capacity Trend Forecaster", "Capacity averages", f"cpu={capacity.get('cpu_avg_percent')}, mem={capacity.get('memory_avg_percent')}", _risk_upper(capacity_risk)],
            ["On-call Context", "Status", f"{oncall.get('status')} / {oncall.get('summary')}", _risk_upper(oncall_risk)],
        ],
    )
    daily_table = _markdown_table(
        ["Metric", "Value", "Risk Level"],
        [
            ["Status", daily["status"], _risk_upper(daily_risk)],
            ["Anomaly count", daily["anomaly_count"], _risk_upper("high" if (daily.get("anomaly_count") or 0) > 0 else "low")],
            ["Recovery plan steps", daily["recovery_plan_count"], _risk_upper("medium" if (daily.get("recovery_plan_count") or 0) > 0 else "low")],
            ["Message", daily.get("message"), _risk_upper(daily_risk)],
        ],
    )
    availability_table = _markdown_table(
        ["Metric", "Value", "Risk Level"],
        [
            ["Risk level", availability.get("risk_level"), _risk_upper(availability_risk)],
            ["Issue count", availability.get("issue_count"), _risk_upper(availability_risk)],
            ["Critical", availability.get("critical"), _risk_upper("critical" if (availability.get("critical") or 0) > 0 else "low")],
            ["High", availability.get("high"), _risk_upper("high" if (availability.get("high") or 0) > 0 else "low")],
            ["Medium", availability.get("medium"), _risk_upper("medium" if (availability.get("medium") or 0) > 0 else "low")],
            ["Low", availability.get("low"), _risk_upper("low")],
        ],
    )
    cluster_below = ", ".join(
        f"{key}={value}" for key, value in (cost.get("cluster_average_below_threshold") or {}).items()
    ) or "none"
    cost_table = _markdown_table(
        ["Metric", "Value", "Risk Level"],
        [
            ["Cluster avg below threshold", cluster_below, _risk_upper("medium" if "True" in cluster_below else "low")],
            ["Nodes clearly below average", cost.get("nodes_clearly_below_average"), _risk_upper("medium" if (cost.get("nodes_clearly_below_average") or 0) > 0 else "low")],
            ["Oversized requests", cost.get("oversized_requests"), _risk_upper("high" if (cost.get("oversized_requests") or 0) > 0 else "low")],
            ["HPA status", cost.get("hpa_status"), _risk_upper("medium" if str(cost.get("hpa_status")) != "configured" else "low")],
            ["Node autoscaler status", cost.get("node_autoscaler_status"), _risk_upper("medium" if str(cost.get("node_autoscaler_status")) != "configured" else "low")],
        ],
    )
    capacity_table = _markdown_table(
        ["Metric", "Value", "Risk Level"],
        [
            ["CPU avg / p95", f"{capacity.get('cpu_avg_percent')} / {capacity.get('cpu_p95_percent')}", _risk_upper(capacity_risk)],
            ["Memory avg / p95", f"{capacity.get('memory_avg_percent')} / {capacity.get('memory_p95_percent')}", _risk_upper(capacity_risk)],
            ["CPU trend", capacity.get("cpu_trend"), _risk_upper(capacity_risk)],
            ["Memory trend", capacity.get("memory_trend"), _risk_upper(capacity_risk)],
            ["Node autoscaler enabled", capacity.get("node_autoscaler_enabled"), _risk_upper("low" if capacity.get("node_autoscaler_enabled") else "medium")],
            ["HPA coverage percent", capacity.get("hpa_coverage_percent"), _risk_upper("medium" if (capacity.get("hpa_coverage_percent") or 0) < 50 else "low")],
            ["Simulation status", capacity.get("simulation_status"), _risk_upper("medium" if str(capacity.get("simulation_status")) == "insufficient_data" else "low")],
            ["Estimated reducible nodes", capacity.get("estimated_reducible_nodes"), _risk_upper("info")],
        ],
    )

    recommendation_rows = report.get("recommendation_rows", [])
    if not recommendation_rows:
        recommendation_rows = [
            {"source": "report", "risk_level": "info", "message": item}
            for item in report.get("recommendations", [])
        ]
    recommendations_table = _markdown_table(
        ["#", "Source", "Risk Level", "Recommendation"],
        [
            [index, row.get("source"), _risk_upper(row.get("risk_level")), row.get("message")]
            for index, row in enumerate(recommendation_rows, start=1)
        ],
    )

    data_gap_rows = report.get("data_gap_rows", [])
    if not data_gap_rows:
        data_gap_rows = _collect_data_gap_rows(report.get("data_gaps", []))
    data_gaps_table = _markdown_table(
        ["#", "Source", "Risk Level", "Gap Detail"],
        [
            [index, row.get("source"), _risk_upper(row.get("risk_level")), row.get("message")]
            for index, row in enumerate(data_gap_rows, start=1)
        ],
    )

    return f"""# {_report_title(report["report"]["type"])}

Generated at: {report["generated_at"]}

## Scope

{scope_table}

## Executive Summary

{executive_table}

## Daily Cluster Inspector

{daily_table}

## Availability Risk Scanner

{availability_table}

## Cost Optimization Advisor

{cost_table}

## Capacity Trend Forecaster

{capacity_table}

## Recommendations

{recommendations_table}

## Data Gaps

{data_gaps_table}
"""


def _render_html(report: Dict[str, Any], trend_svg: str, simulation_svg: str) -> str:
    scope = report["scope"]
    summary = report["summary"]
    daily = summary["daily_cluster_inspector"]
    availability = summary["availability_risk_scanner"]
    cost = summary["cost_optimization_advisor"]
    capacity = summary["capacity_trend_forecaster"]
    oncall = summary["oncall_copilot"]
    daily_risk = _daily_risk(daily)
    availability_risk = _availability_risk(availability)
    cost_risk = _cost_risk(cost)
    capacity_risk = _capacity_risk(capacity)
    oncall_risk = _oncall_risk(oncall)

    scope_table = _html_table(
        ["Field", "Value"],
        [
            ["Region", scope["region"]],
            ["Cluster", scope["cluster_id"]],
            ["Report type", report["report"]["type"]],
            ["Window hours", report["report"]["hours"]],
            ["Excluded namespaces", ", ".join(scope["excluded_namespaces"]) or "none"],
            ["Business namespaces", ", ".join(scope["business_namespaces"]) or "all non-excluded namespaces"],
        ],
    )
    executive_table = _html_table(
        ["Module", "Signal", "Value", "Risk Level"],
        [
            ["Daily Cluster Inspector", "Status", f"{daily['status']} (anomalies={daily['anomaly_count']})", _risk_upper(daily_risk)],
            ["Availability Risk Scanner", "Risk and issues", f"{availability.get('risk_level')} / {availability.get('issue_count')}", _risk_upper(availability_risk)],
            ["Cost Optimization Advisor", "Cost signals", f"oversized={cost.get('oversized_requests')}, low_nodes={cost.get('nodes_clearly_below_average')}", _risk_upper(cost_risk)],
            ["Capacity Trend Forecaster", "Capacity averages", f"cpu={capacity.get('cpu_avg_percent')}, mem={capacity.get('memory_avg_percent')}", _risk_upper(capacity_risk)],
            ["On-call Context", "Status", f"{oncall.get('status')} / {oncall.get('summary')}", _risk_upper(oncall_risk)],
        ],
    )
    daily_table = _html_table(
        ["Metric", "Value", "Risk Level"],
        [
            ["Status", daily["status"], _risk_upper(daily_risk)],
            ["Anomaly count", daily["anomaly_count"], _risk_upper("high" if (daily.get("anomaly_count") or 0) > 0 else "low")],
            ["Recovery plan steps", daily["recovery_plan_count"], _risk_upper("medium" if (daily.get("recovery_plan_count") or 0) > 0 else "low")],
            ["Message", daily.get("message"), _risk_upper(daily_risk)],
        ],
    )
    availability_table = _html_table(
        ["Metric", "Value", "Risk Level"],
        [
            ["Risk level", availability.get("risk_level"), _risk_upper(availability_risk)],
            ["Issue count", availability.get("issue_count"), _risk_upper(availability_risk)],
            ["Critical", availability.get("critical"), _risk_upper("critical" if (availability.get("critical") or 0) > 0 else "low")],
            ["High", availability.get("high"), _risk_upper("high" if (availability.get("high") or 0) > 0 else "low")],
            ["Medium", availability.get("medium"), _risk_upper("medium" if (availability.get("medium") or 0) > 0 else "low")],
            ["Low", availability.get("low"), _risk_upper("low")],
        ],
    )
    cluster_below = ", ".join(
        f"{key}={value}" for key, value in (cost.get("cluster_average_below_threshold") or {}).items()
    ) or "none"
    cost_table = _html_table(
        ["Metric", "Value", "Risk Level"],
        [
            ["Cluster avg below threshold", cluster_below, _risk_upper("medium" if "True" in cluster_below else "low")],
            ["Nodes clearly below average", cost.get("nodes_clearly_below_average"), _risk_upper("medium" if (cost.get("nodes_clearly_below_average") or 0) > 0 else "low")],
            ["Oversized requests", cost.get("oversized_requests"), _risk_upper("high" if (cost.get("oversized_requests") or 0) > 0 else "low")],
            ["HPA status", cost.get("hpa_status"), _risk_upper("medium" if str(cost.get("hpa_status")) != "configured" else "low")],
            ["Node autoscaler status", cost.get("node_autoscaler_status"), _risk_upper("medium" if str(cost.get("node_autoscaler_status")) != "configured" else "low")],
        ],
    )
    capacity_table = _html_table(
        ["Metric", "Value", "Risk Level"],
        [
            ["CPU avg / p95", f"{capacity.get('cpu_avg_percent')} / {capacity.get('cpu_p95_percent')}", _risk_upper(capacity_risk)],
            ["Memory avg / p95", f"{capacity.get('memory_avg_percent')} / {capacity.get('memory_p95_percent')}", _risk_upper(capacity_risk)],
            ["CPU trend", capacity.get("cpu_trend"), _risk_upper(capacity_risk)],
            ["Memory trend", capacity.get("memory_trend"), _risk_upper(capacity_risk)],
            ["Node autoscaler enabled", capacity.get("node_autoscaler_enabled"), _risk_upper("low" if capacity.get("node_autoscaler_enabled") else "medium")],
            ["HPA coverage percent", capacity.get("hpa_coverage_percent"), _risk_upper("medium" if (capacity.get("hpa_coverage_percent") or 0) < 50 else "low")],
            ["Simulation status", capacity.get("simulation_status"), _risk_upper("medium" if str(capacity.get("simulation_status")) == "insufficient_data" else "low")],
            ["Estimated reducible nodes", capacity.get("estimated_reducible_nodes"), _risk_upper("info")],
        ],
    )

    recommendation_rows = report.get("recommendation_rows", [])
    if not recommendation_rows:
        recommendation_rows = [
            {"source": "report", "risk_level": "info", "message": item}
            for item in report.get("recommendations", [])
        ]
    recommendations_table = _html_table(
        ["#", "Source", "Risk Level", "Recommendation"],
        [
            [index, row.get("source"), _risk_upper(row.get("risk_level")), row.get("message")]
            for index, row in enumerate(recommendation_rows, start=1)
        ],
    )

    data_gap_rows = report.get("data_gap_rows", [])
    if not data_gap_rows:
        data_gap_rows = _collect_data_gap_rows(report.get("data_gaps", []))
    data_gaps_table = _html_table(
        ["#", "Source", "Risk Level", "Gap Detail"],
        [
            [index, row.get("source"), _risk_upper(row.get("risk_level")), row.get("message")]
            for index, row in enumerate(data_gap_rows, start=1)
        ],
    )
    trend_block = trend_svg if trend_svg else "<p>No trend chart was generated.</p>"
    simulation_block = simulation_svg if simulation_svg else "<p>No simulation chart was generated.</p>"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{html.escape(_report_title(report["report"]["type"]))}</title>
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; margin: 0; background: #f6f8fb; color: #111827; }}
    .page {{ max-width: 1100px; margin: 0 auto; padding: 20px; }}
    h1 {{ margin: 0 0 8px; font-size: 28px; }}
    h2 {{ margin-top: 24px; font-size: 20px; }}
    .meta {{ color: #4b5563; font-size: 14px; }}
    .report-table {{ width: 100%; border-collapse: collapse; margin-top: 10px; background: #ffffff; }}
    .report-table th, .report-table td {{ border: 1px solid #e5e7eb; padding: 8px 10px; text-align: left; vertical-align: top; font-size: 13px; }}
    .report-table th {{ background: #f3f4f6; }}
    .svg-wrap {{ background: #ffffff; border: 1px solid #e5e7eb; border-radius: 8px; padding: 10px; overflow-x: auto; }}
  </style>
</head>
<body>
  <div class="page">
    <h1>{html.escape(_report_title(report["report"]["type"]))}</h1>
    <div class="meta">Generated at {html.escape(report["generated_at"])} | Region {html.escape(scope["region"])} | Cluster {html.escape(scope["cluster_id"])} | Window {report["report"]["hours"]}h</div>

    <h2>Scope</h2>
    {scope_table}

    <h2>Executive Summary</h2>
    {executive_table}

    <h2>Daily Cluster Inspector</h2>
    {daily_table}

    <h2>Availability Risk Scanner</h2>
    {availability_table}

    <h2>Cost Optimization Advisor</h2>
    {cost_table}

    <h2>Capacity Trend Forecaster</h2>
    {capacity_table}

    <h2>Trend Chart</h2>
    <div class="svg-wrap">{trend_block}</div>

    <h2>Elasticity Simulation</h2>
    <div class="svg-wrap">{simulation_block}</div>

    <h2>Recommendations</h2>
    {recommendations_table}

    <h2>Data Gaps</h2>
    {data_gaps_table}
  </div>
</body>
</html>
"""


def _component_output_dir(root: Optional[str], name: str) -> Optional[str]:
    if not root:
        return None
    path = Path(root) / "sources" / name
    path.mkdir(parents=True, exist_ok=True)
    return str(path)


def _safe_collect(name: str, collector: Any, **kwargs: Any) -> Dict[str, Any]:
    try:
        payload = collector(**kwargs)
    except Exception as exc:  # pragma: no cover - defensive around SDK/environment drift.
        return {
            "success": False,
            "error": f"{type(exc).__name__}: {exc}",
            "data_gaps": [f"{name}: runtime error"],
        }
    if isinstance(payload, dict):
        return payload
    return {
        "success": False,
        "error": f"{name} returned non-dict payload",
        "data_gaps": [f"{name}: invalid payload type"],
    }


def _write_outputs(
    output_dir: Optional[str],
    report: Dict[str, Any],
    trend_svg: str,
    simulation_svg: str,
    raw_payload: Dict[str, Any],
    include_raw: bool,
) -> Dict[str, str]:
    if not output_dir:
        return {}
    target = Path(output_dir)
    target.mkdir(parents=True, exist_ok=True)
    report_type = report["report"]["type"]

    summary_path = target / f"ops-{report_type}-summary.json"
    md_path = target / f"ops-{report_type}-report.md"
    html_path = target / f"ops-{report_type}-report.html"
    trend_path = target / "ops-capacity-trend.svg"
    simulation_path = target / "ops-capacity-simulation.svg"

    _write_json(summary_path, report)
    md_path.write_text(_render_markdown(report), encoding="utf-8")
    html_path.write_text(_render_html(report, trend_svg, simulation_svg), encoding="utf-8")
    if trend_svg:
        trend_path.write_text(trend_svg, encoding="utf-8")
    if simulation_svg:
        simulation_path.write_text(simulation_svg, encoding="utf-8")

    files = {
        "summary": str(summary_path),
        "report": str(md_path),
        "report_html": str(html_path),
    }
    if trend_svg:
        files["trend_chart"] = str(trend_path)
    if simulation_svg:
        files["simulation_chart"] = str(simulation_path)
    if include_raw:
        raw_path = target / f"ops-{report_type}-raw.json"
        _write_json(raw_path, raw_payload)
        files["raw"] = str(raw_path)
    return files


def generate_ops_report(
    region: str,
    cluster_id: str,
    ak: Optional[str] = None,
    sk: Optional[str] = None,
    project_id: Optional[str] = None,
    report_type: str = "weekly",
    hours: Optional[int] = None,
    short_hours: Optional[int] = None,
    long_hours: Optional[int] = None,
    step_seconds: int = 3600,
    top_n: int = 200,
    exclude_namespaces: Optional[str | Iterable[str]] = None,
    business_namespaces: Optional[str | Iterable[str]] = None,
    gateway_keywords: Optional[str | Iterable[str]] = None,
    output_dir: Optional[str] = None,
    include_raw: bool = False,
    oncall_report_path: Optional[str] = None,
    oncall_summary: Optional[str] = None,
) -> Dict[str, Any]:
    """Generate weekly/monthly/SLA/capacity/stability CCE operations reports."""
    if not region:
        return {"success": False, "error": "region is required"}
    if not cluster_id:
        return {"success": False, "error": "cluster_id is required"}

    normalized_type = (report_type or "weekly").strip().lower()
    if normalized_type not in REPORT_TYPES:
        return {
            "success": False,
            "error": f"invalid report_type: {report_type}",
            "allowed_report_types": sorted(REPORT_TYPES),
        }

    effective_hours = int(hours) if hours else DEFAULT_HOURS_BY_REPORT_TYPE[normalized_type]
    effective_hours = max(1, min(24 * 31, effective_hours))
    effective_short = short_hours if short_hours and short_hours > 0 else min(24, effective_hours)
    effective_long = long_hours if long_hours and long_hours > 0 else max(effective_hours, 24 * 7)
    if effective_long < effective_short:
        effective_long = effective_short

    excluded = _as_list(exclude_namespaces, DEFAULT_EXCLUDED_NAMESPACES)
    business = _as_list(business_namespaces)
    gateways = _as_list(gateway_keywords, DEFAULT_GATEWAY_KEYWORDS)

    daily_result = _safe_collect(
        "daily-cluster-inspector",
        cce_auto_inspection.cce_auto_inspection,
        region=region,
        cluster_id=cluster_id,
        ak=ak,
        sk=sk,
        project_id=project_id,
    )
    capacity_result = _safe_collect(
        "capacity-trend-forecaster",
        cce_capacity_trend.analyze_cce_capacity_trend,
        region=region,
        cluster_id=cluster_id,
        ak=ak,
        sk=sk,
        project_id=project_id,
        hours=effective_hours,
        step_seconds=step_seconds,
        top_n=top_n,
        exclude_namespaces=excluded,
        business_namespaces=business,
        output_dir=_component_output_dir(output_dir, "capacity-trend-forecaster"),
        include_raw=include_raw,
    )
    availability_result = _safe_collect(
        "availability-risk-scanner",
        cce_availability_risk.scan_cce_availability_risk,
        region=region,
        cluster_id=cluster_id,
        ak=ak,
        sk=sk,
        project_id=project_id,
        exclude_namespaces=excluded,
        gateway_keywords=gateways,
        metrics_hours=min(effective_hours, 24 * 7),
        output_dir=_component_output_dir(output_dir, "availability-risk-scanner"),
        include_raw=include_raw,
    )
    cost_result = _safe_collect(
        "cost-optimization-advisor",
        cce_cost_optimization.analyze_cce_cost_optimization,
        region=region,
        cluster_id=cluster_id,
        ak=ak,
        sk=sk,
        project_id=project_id,
        short_hours=effective_short,
        long_hours=effective_long,
        top_n=min(top_n, 200),
        exclude_namespaces=excluded,
        business_namespaces=business,
        output_dir=_component_output_dir(output_dir, "cost-optimization-advisor"),
        include_raw=include_raw,
    )
    oncall = _extract_oncall(oncall_report_path, oncall_summary)

    data_gaps: list[str] = []
    for source_name, payload in (
        ("daily-cluster-inspector", daily_result),
        ("capacity-trend-forecaster", capacity_result),
        ("availability-risk-scanner", availability_result),
        ("cost-optimization-advisor", cost_result),
    ):
        if not payload.get("success", True):
            data_gaps.append(f"{source_name}: {payload.get('error', 'collection failed')}")
        for gap in payload.get("data_gaps", []) or []:
            data_gaps.append(f"{source_name}: {gap}")
    if oncall.get("status") in {"missing", "error"}:
        data_gaps.append(f"oncall-copilot: {oncall.get('summary')}")
    data_gap_rows = _collect_data_gap_rows(data_gaps)

    summaries = {
        "daily_cluster_inspector": _daily_summary(daily_result),
        "capacity_trend_forecaster": _capacity_summary(capacity_result),
        "availability_risk_scanner": _availability_summary(availability_result),
        "cost_optimization_advisor": _cost_summary(cost_result),
        "oncall_copilot": {
            "status": oncall.get("status"),
            "source": oncall.get("source"),
            "summary": oncall.get("summary"),
        },
    }
    recommendation_rows = _collect_recommendations(
        daily_result,
        capacity_result,
        availability_result,
        cost_result,
        oncall,
    )
    recommendations = [
        f"[{row.get('source')}][{row.get('risk_level')}] {row.get('message')}"
        for row in recommendation_rows
    ]

    report: Dict[str, Any] = {
        "success": True,
        "action": "generate_ops_report",
        "generated_at": _utc_now(),
        "scope": {
            "region": region,
            "cluster_id": cluster_id,
            "excluded_namespaces": excluded,
            "business_namespaces": business,
            "gateway_keywords": gateways,
        },
        "report": {
            "type": normalized_type,
            "hours": effective_hours,
            "short_hours": effective_short,
            "long_hours": effective_long,
        },
        "summary": summaries,
        "recommendations": recommendations,
        "recommendation_rows": recommendation_rows,
        "data_gaps": data_gaps,
        "data_gap_rows": data_gap_rows,
        "sources": {
            "daily_cluster_inspector": {
                "success": daily_result.get("success", True),
                "message": daily_result.get("message"),
            },
            "capacity_trend_forecaster": {
                "success": capacity_result.get("success", False),
                "files": capacity_result.get("files", {}),
            },
            "availability_risk_scanner": {
                "success": availability_result.get("success", False),
                "files": availability_result.get("files", {}),
            },
            "cost_optimization_advisor": {
                "success": cost_result.get("success", False),
                "files": cost_result.get("files", {}),
            },
            "oncall_copilot": {
                "status": oncall.get("status"),
                "source": oncall.get("source"),
            },
        },
    }
    if include_raw:
        report["source_results"] = {
            "daily_cluster_inspector": daily_result,
            "capacity_trend_forecaster": capacity_result,
            "availability_risk_scanner": availability_result,
            "cost_optimization_advisor": cost_result,
            "oncall_copilot": oncall.get("details"),
        }

    capacity_files = capacity_result.get("files", {}) if isinstance(capacity_result, dict) else {}
    trend_svg = _read_svg(capacity_files.get("trend_chart"))
    simulation_svg = _read_svg(capacity_files.get("simulation_chart"))
    raw_payload = {
        "daily_cluster_inspector": daily_result,
        "capacity_trend_forecaster": capacity_result,
        "availability_risk_scanner": availability_result,
        "cost_optimization_advisor": cost_result,
        "oncall_copilot": oncall,
    }
    report["files"] = _write_outputs(output_dir, report, trend_svg, simulation_svg, raw_payload, include_raw)

    if report["files"].get("summary"):
        _write_json(Path(report["files"]["summary"]), report)
    return report
