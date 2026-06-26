#!/usr/bin/env python3
"""
n8n Autopilot — Workflow Inspector
Validates structure, detects anti-patterns, and suggests optimizations.

Author: Dr. FIRAS — https://www.linkedin.com/in/doctor-firass/
"""

import sys
import json
import argparse
from collections import defaultdict, deque
from typing import Dict, List, Any, Optional, Set, Tuple


# ---------------------------------------------------------------------------
# Validation Engine
# ---------------------------------------------------------------------------

class Finding:
    """A single validation or diagnostic finding."""
    SEVERITY_ERROR = "error"
    SEVERITY_WARN = "warning"
    SEVERITY_INFO = "info"

    def __init__(self, severity: str, code: str, message: str, node: str = ""):
        self.severity = severity
        self.code = code
        self.message = message
        self.node = node

    def to_dict(self) -> Dict:
        d = {"severity": self.severity, "code": self.code, "message": self.message}
        if self.node:
            d["node"] = self.node
        return d


class InspectionReport:
    """Aggregates findings and computes pass/fail."""

    def __init__(self):
        self.findings: List[Finding] = []

    def add(self, severity: str, code: str, message: str, node: str = ""):
        self.findings.append(Finding(severity, code, message, node))

    def error(self, code: str, msg: str, node: str = ""):
        self.add(Finding.SEVERITY_ERROR, code, msg, node)

    def warn(self, code: str, msg: str, node: str = ""):
        self.add(Finding.SEVERITY_WARN, code, msg, node)

    def info(self, code: str, msg: str, node: str = ""):
        self.add(Finding.SEVERITY_INFO, code, msg, node)

    @property
    def passed(self) -> bool:
        return not any(f.severity == Finding.SEVERITY_ERROR for f in self.findings)

    @property
    def error_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == Finding.SEVERITY_ERROR)

    @property
    def warning_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == Finding.SEVERITY_WARN)

    def to_dict(self) -> Dict:
        return {
            "valid": self.passed,
            "errors": self.error_count,
            "warnings": self.warning_count,
            "findings": [f.to_dict() for f in self.findings],
        }

    def summary_text(self) -> str:
        lines = []
        status = "PASSED" if self.passed else "FAILED"
        lines.append(f"Inspection: {status}  ({self.error_count} errors, {self.warning_count} warnings)")
        lines.append("-" * 60)
        for f in self.findings:
            icon = {"error": "X", "warning": "!", "info": "i"}[f.severity]
            loc = f"[{f.node}] " if f.node else ""
            lines.append(f"  [{icon}] {f.code}: {loc}{f.message}")
        return "\n".join(lines)


def inspect_workflow(wf: Dict) -> InspectionReport:
    """
    Run all structural validation checks on a workflow dict.
    Returns an InspectionReport.
    """
    report = InspectionReport()

    nodes = wf.get("nodes")
    connections = wf.get("connections", {})

    # --- Phase 1: Structure presence ---
    if nodes is None:
        report.error("MISSING_NODES", "Workflow has no 'nodes' array.")
        return report

    if not isinstance(nodes, list) or len(nodes) == 0:
        report.error("EMPTY_NODES", "Workflow 'nodes' array is empty.")
        return report

    # --- Phase 2: Node integrity ---
    node_names: Set[str] = set()
    node_ids: Set[str] = set()
    trigger_count = 0
    trigger_types = {
        "n8n-nodes-base.webhook",
        "n8n-nodes-base.scheduleTrigger",
        "n8n-nodes-base.manualTrigger",
        "n8n-nodes-base.start",
        "n8n-nodes-base.formTrigger",
        "n8n-nodes-base.emailimap",
    }

    for idx, nd in enumerate(nodes):
        name = nd.get("name")
        ntype = nd.get("type", "")

        if not name:
            report.error("NODE_NO_NAME", f"Node at index {idx} has no 'name'.")
            continue
        if name in node_names:
            report.error("DUPLICATE_NAME", f"Duplicate node name: '{name}'.", name)
        node_names.add(name)

        nid = nd.get("id", "")
        if nid in node_ids and nid:
            report.warn("DUPLICATE_ID", f"Duplicate node ID: '{nid}'.", name)
        if nid:
            node_ids.add(nid)

        if not ntype:
            report.error("NODE_NO_TYPE", f"Node '{name}' has no 'type'.", name)

        if ntype in trigger_types or "trigger" in ntype.lower():
            trigger_count += 1

        # Required-parameter checks
        params = nd.get("parameters", {})
        _check_required_params(ntype, name, params, report)

        # Credential hints
        _check_credentials(ntype, name, nd.get("credentials", {}), report)

    if trigger_count == 0 and len(nodes) > 0:
        report.warn("NO_TRIGGER", "Workflow has no trigger node — it can only run manually.")
    elif trigger_count > 1:
        report.warn("MULTI_TRIGGER", f"Workflow has {trigger_count} trigger nodes; n8n may ignore extras.")

    # --- Phase 3: Connection integrity ---
    all_targets: Set[str] = set()
    all_sources: Set[str] = set()

    for src, outputs in connections.items():
        all_sources.add(src)
        if src not in node_names:
            report.error("CONN_BAD_SOURCE", f"Connection from non-existent node: '{src}'.")

        for output_key, output_slots in outputs.items():
            for slot in output_slots:
                for link in slot:
                    tgt = link.get("node", "")
                    all_targets.add(tgt)
                    if tgt not in node_names:
                        report.error("CONN_BAD_TARGET", f"Connection to non-existent node: '{tgt}'.", src)

    # Disconnected nodes
    connected = all_sources | all_targets
    for name in node_names:
        if name not in connected and len(nodes) > 1:
            report.warn("DISCONNECTED", f"Node '{name}' is not connected to any other node.", name)

    # --- Phase 4: Cycle detection ---
    if _has_cycle(node_names, connections):
        report.error("CYCLE_DETECTED", "Workflow graph contains a cycle. n8n may loop infinitely.")

    # --- Phase 5: IF/Switch branch completeness ---
    for nd in nodes:
        ntype = nd.get("type", "")
        name = nd.get("name", "")
        if ntype == "n8n-nodes-base.if":
            outputs = connections.get(name, {}).get("main", [])
            if len(outputs) < 2:
                report.warn("IF_MISSING_BRANCH", f"IF node '{name}' should have 2 output branches.", name)
        elif ntype == "n8n-nodes-base.switch":
            outputs = connections.get(name, {}).get("main", [])
            if len(outputs) < 2:
                report.warn("SWITCH_FEW_BRANCHES", f"Switch node '{name}' has fewer than 2 branches.", name)

    return report


# --- Helpers for inspect_workflow ---

_NEEDS_URL = {"n8n-nodes-base.httpRequest"}
_NEEDS_PATH = {"n8n-nodes-base.webhook"}
_NEEDS_CODE = {"n8n-nodes-base.code"}

_CREDENTIAL_NODES = {
    "n8n-nodes-base.httpRequest",
    "n8n-nodes-base.slack",
    "n8n-nodes-base.gmail",
    "n8n-nodes-base.googleSheets",
    "n8n-nodes-base.postgres",
    "n8n-nodes-base.mysql",
    "n8n-nodes-base.telegram",
    "n8n-nodes-base.stripe",
    "n8n-nodes-base.notion",
    "n8n-nodes-base.airtable",
    "n8n-nodes-base.emailSend",
}


def _check_required_params(ntype: str, name: str, params: Dict, report: InspectionReport):
    if ntype in _NEEDS_URL and not params.get("url"):
        report.error("MISSING_URL", f"HTTP Request node '{name}' has no URL configured.", name)
    if ntype in _NEEDS_PATH and not params.get("path"):
        report.error("MISSING_PATH", f"Webhook node '{name}' has no path configured.", name)
    if ntype in _NEEDS_CODE:
        if not params.get("jsCode") and not params.get("pythonCode"):
            report.error("MISSING_CODE", f"Code node '{name}' has no code.", name)


def _check_credentials(ntype: str, name: str, creds: Dict, report: InspectionReport):
    if ntype in _CREDENTIAL_NODES and not creds:
        auth = creds if creds else None
        # httpRequest with auth=none is fine
        if ntype == "n8n-nodes-base.httpRequest":
            return
        report.info("CREDS_HINT", f"Node '{name}' may need credentials after import.", name)


def _has_cycle(node_names: Set[str], connections: Dict) -> bool:
    """Detect cycles using DFS-based topological sort."""
    adj: Dict[str, List[str]] = defaultdict(list)
    for src, outputs in connections.items():
        for slot_list in outputs.get("main", []):
            for link in slot_list:
                adj[src].append(link.get("node", ""))

    WHITE, GRAY, BLACK = 0, 1, 2
    color = {n: WHITE for n in node_names}

    def dfs(u: str) -> bool:
        color[u] = GRAY
        for v in adj.get(u, []):
            if v not in color:
                continue
            if color[v] == GRAY:
                return True
            if color[v] == WHITE and dfs(v):
                return True
        color[u] = BLACK
        return False

    return any(dfs(n) for n in node_names if color.get(n) == WHITE)


# ---------------------------------------------------------------------------
# Performance Diagnostics
# ---------------------------------------------------------------------------

_EXPENSIVE_KEYWORDS = {"httpRequest", "postgres", "mysql", "mongodb", "googleSheets", "airtable", "stripe"}


def diagnose_performance(wf: Dict, exec_stats: Optional[Dict] = None) -> Dict:
    """
    Analyze a workflow for performance bottlenecks and optimization
    opportunities. Optionally incorporate execution statistics.
    """
    nodes = wf.get("nodes", [])
    connections = wf.get("connections", {})
    settings = wf.get("settings", {})

    result: Dict[str, Any] = {
        "node_count": len(nodes),
        "complexity": _score_complexity(nodes, connections),
        "score": 100,
        "bottlenecks": [],
        "suggestions": [],
    }

    # --- Expensive sequential chains ---
    expensive = [n["name"] for n in nodes if any(k in n.get("type", "") for k in _EXPENSIVE_KEYWORDS)]
    if len(expensive) >= 4:
        result["bottlenecks"].append({
            "id": "SEQUENTIAL_IO",
            "severity": "high",
            "detail": f"{len(expensive)} I/O-heavy nodes detected — consider parallel branching.",
            "nodes": expensive,
        })
        result["score"] -= 15

    # --- Missing error handling ---
    has_error_node = any("error" in n.get("type", "").lower() for n in nodes)
    has_if_guard = any(n.get("type") == "n8n-nodes-base.if" for n in nodes)
    if not has_error_node and not has_if_guard and len(nodes) > 4:
        result["suggestions"].append({
            "id": "ADD_ERROR_HANDLING",
            "priority": "high",
            "detail": "Add an Error Trigger or IF-based guard to handle failures gracefully.",
        })
        result["score"] -= 10

    # --- No execution timeout ---
    if not settings.get("executionTimeout") and len(nodes) > 6:
        result["suggestions"].append({
            "id": "SET_TIMEOUT",
            "priority": "medium",
            "detail": "Set executionTimeout in workflow settings to prevent runaway executions.",
        })
        result["score"] -= 5

    # --- High complexity ---
    if result["complexity"] > 70:
        result["suggestions"].append({
            "id": "SPLIT_WORKFLOW",
            "priority": "medium",
            "detail": f"Complexity score is {result['complexity']}/100 — consider sub-workflows.",
        })
        result["score"] -= 8

    # --- Caching opportunity ---
    http_count = sum(1 for n in nodes if "httpRequest" in n.get("type", ""))
    if http_count >= 3:
        result["suggestions"].append({
            "id": "CACHE_RESPONSES",
            "priority": "medium",
            "detail": f"{http_count} HTTP nodes — cache repeated calls using Code node storage.",
        })

    # --- Batch processing ---
    has_batch = any("splitInBatches" in n.get("type", "") for n in nodes)
    if not has_batch and http_count >= 2:
        result["suggestions"].append({
            "id": "USE_BATCHING",
            "priority": "low",
            "detail": "Use Split In Batches for large dataset processing.",
        })

    # --- Incorporate execution stats ---
    if exec_stats:
        rate = exec_stats.get("success_rate_pct", 100)
        if rate < 60:
            result["bottlenecks"].append({
                "id": "HIGH_FAILURE_RATE",
                "severity": "critical",
                "detail": f"Success rate is only {rate}% — investigate top errors.",
            })
            result["score"] -= 25
        elif rate < 85:
            result["score"] -= 10

    result["score"] = max(0, min(100, result["score"]))
    result["health"] = (
        "excellent" if result["score"] >= 90 else
        "good" if result["score"] >= 70 else
        "fair" if result["score"] >= 50 else
        "poor"
    )
    return result


def _score_complexity(nodes: List[Dict], connections: Dict) -> int:
    """0-100 complexity score based on node count, connections, and logic nodes."""
    score = min(len(nodes) * 5, 50)
    conn_count = sum(
        len(link) for outputs in connections.values()
        for slots in outputs.get("main", []) for link in [slots]
    )
    score += min(conn_count * 3, 30)
    for nd in nodes:
        t = nd.get("type", "")
        if t == "n8n-nodes-base.if":
            score += 5
        elif t == "n8n-nodes-base.switch":
            score += 8
        elif t == "n8n-nodes-base.code":
            score += 3
    return min(score, 100)


def format_diagnosis(diag: Dict, wf_name: str = "Workflow") -> str:
    """Human-readable diagnostic report."""
    lines = [
        "=" * 60,
        f"  Diagnostic Report — {wf_name}",
        "=" * 60,
        f"  Health: {diag['health'].upper()}   Score: {diag['score']}/100",
        f"  Nodes: {diag['node_count']}   Complexity: {diag['complexity']}/100",
        "-" * 60,
    ]
    if diag["bottlenecks"]:
        lines.append("  BOTTLENECKS:")
        for b in diag["bottlenecks"]:
            lines.append(f"    [{b['severity'].upper()}] {b['id']}: {b['detail']}")
    if diag["suggestions"]:
        lines.append("  SUGGESTIONS:")
        for s in diag["suggestions"]:
            lines.append(f"    [{s['priority'].upper()}] {s['id']}: {s['detail']}")
    if not diag["bottlenecks"] and not diag["suggestions"]:
        lines.append("  No issues found. Workflow looks healthy.")
    lines.append("=" * 60)
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _load_workflow(args) -> Tuple[Dict, Optional[str]]:
    """Load workflow from file or n8n instance."""
    if getattr(args, "file", None):
        with open(args.file, "r") as fh:
            return json.load(fh), None
    elif getattr(args, "id", None):
        from n8n_deploy import N8nGateway
        gw = N8nGateway()
        wf = gw.get_workflow(args.id)
        return wf, args.id
    else:
        raise SystemExit("Provide --file or --id")


def main():
    ap = argparse.ArgumentParser(
        prog="workflow_inspector",
        description="n8n Autopilot — Workflow Inspector (by Dr. FIRAS)",
    )
    sub = ap.add_subparsers(dest="command", required=True)

    # check
    p_chk = sub.add_parser("check", help="Validate workflow structure")
    p_chk.add_argument("--file", help="Path to workflow JSON")
    p_chk.add_argument("--id", help="Deployed workflow ID")
    p_chk.add_argument("--json", action="store_true", help="Output raw JSON")

    # diagnose
    p_diag = sub.add_parser("diagnose", help="Full diagnostic report")
    p_diag.add_argument("--file", help="Path to workflow JSON")
    p_diag.add_argument("--id", help="Deployed workflow ID")
    p_diag.add_argument("--days", type=int, default=7)
    p_diag.add_argument("--json", action="store_true")

    # optimize
    p_opt = sub.add_parser("optimize", help="Optimization suggestions")
    p_opt.add_argument("--file", help="Path to workflow JSON")
    p_opt.add_argument("--id", help="Deployed workflow ID")

    args = ap.parse_args()

    try:
        wf, wf_id = _load_workflow(args)

        if args.command == "check":
            report = inspect_workflow(wf)
            if getattr(args, "json", False):
                print(json.dumps(report.to_dict(), indent=2))
            else:
                print(report.summary_text())
            sys.exit(0 if report.passed else 1)

        elif args.command == "diagnose":
            report = inspect_workflow(wf)
            exec_stats = None
            if wf_id:
                from n8n_deploy import N8nGateway
                gw = N8nGateway()
                exec_stats = gw.compute_stats(wf_id, days=args.days)

            diag = diagnose_performance(wf, exec_stats)

            if getattr(args, "json", False):
                combined = {"validation": report.to_dict(), "diagnostics": diag}
                print(json.dumps(combined, indent=2))
            else:
                print(report.summary_text())
                print()
                print(format_diagnosis(diag, wf.get("name", "Workflow")))

        elif args.command == "optimize":
            diag = diagnose_performance(wf)
            if diag["suggestions"]:
                for s in diag["suggestions"]:
                    print(f"  [{s['priority'].upper():6}] {s['id']}: {s['detail']}")
            else:
                print("  No optimization suggestions — workflow looks clean.")

    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
