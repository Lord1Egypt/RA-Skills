#!/usr/bin/env python3
"""Execution Trace — deterministic decision recording and replay.

v2.2 NEW: Provides fixed decision trace (every decision produces an immutable
trace entry) and replayable execution (same input → same output, no randomness).

This module records every decision the agent makes (scope check, probe
continuation, severity upgrade, scope expansion, confidence scoring) into
a structured, machine-readable trace. The trace can be replayed to verify
determinism and audit decision paths.

Usage (CLI):
  python execution_trace.py --record --state ACTIVE_TESTING --decision continue --result '{"decision":"continue",...}'
  python execution_trace.py --replay trace.json
  python execution_trace.py --verify trace1.json trace2.json
  python execution_trace.py --diff trace1.json trace2.json
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
from dataclasses import dataclass, field, asdict
from typing import Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils import load_json, dump_json


# =============================================================================
# Data Models
# =============================================================================

@dataclass
class TraceEntry:
    """A single immutable decision trace entry."""
    index: int
    timestamp: str
    state: str
    decision_type: str              # "scope_check" | "probe_continue" | "severity_upgrade" | "scope_expand" | "confidence" | "state_transition"
    input_hash: str                 # SHA256 of normalized input
    result: dict                    # The decision result (DecisionResult or similar)
    rule_path: str = ""             # Which rule chain was followed
    deterministic: bool = True      # Always True in v2.2


@dataclass
class ExecutionTrace:
    """Full execution trace for a single run."""
    run_id: str
    skill_version: str = "2.2.0"
    started_at: str = ""
    completed_at: str = ""
    entries: list = field(default_factory=list)
    summary: dict = field(default_factory=dict)
    verification: dict = field(default_factory=dict)


# =============================================================================
# Trace Recording
# =============================================================================

def create_trace(run_id: str) -> ExecutionTrace:
    """Create a new execution trace for a run."""
    return ExecutionTrace(
        run_id=run_id,
        started_at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    )


def record_decision(trace: ExecutionTrace, state: str, decision_type: str,
                    input_data: dict, result: dict) -> TraceEntry:
    """Record a single decision into the trace.

    Args:
        trace: The execution trace to append to
        state: Current state machine state (e.g., "ACTIVE_TESTING")
        decision_type: Type of decision (scope_check, probe_continue, etc.)
        input_data: Normalized input that drove the decision
        result: The decision result (must contain 'decision', 'score', 'reasoning')

    Returns:
        The TraceEntry that was appended
    """
    input_hash = _hash_input(input_data)
    entry = TraceEntry(
        index=len(trace.entries),
        timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        state=state,
        decision_type=decision_type,
        input_hash=input_hash,
        result={
            "decision": result.get("decision", ""),
            "score": result.get("score", 0),
            "threshold": result.get("threshold", 0),
            "reasoning": result.get("reasoning", ""),
            "factors": result.get("factors", {}),
        },
        rule_path=result.get("rule_path", ""),
        deterministic=result.get("deterministic", True),
    )
    trace.entries.append(entry)
    return entry


def finalize_trace(trace: ExecutionTrace) -> ExecutionTrace:
    """Finalize a trace — compute summary and close."""
    trace.completed_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    decisions_by_type = {}
    for e in trace.entries:
        decisions_by_type.setdefault(e.decision_type, []).append(e.result["decision"])

    trace.summary = {
        "total_decisions": len(trace.entries),
        "states_visited": sorted(set(e.state for e in trace.entries)),
        "decisions_by_type": {k: len(v) for k, v in decisions_by_type.items()},
        "all_deterministic": all(e.deterministic for e in trace.entries),
    }
    return trace


# =============================================================================
# Trace Replay (Determinism Verification)
# =============================================================================

def replay_trace(trace: ExecutionTrace) -> dict:
    """Analyze a trace for determinism and decision path audit.

    Returns a verification report with:
    - total entries
    - unique rule paths used
    - state coverage
    - determinism status
    """
    rule_paths = {}
    for e in trace.entries:
        rp = e.rule_path or "no_rule_path"
        rule_paths.setdefault(rp, []).append(e.index)

    return {
        "run_id": trace.run_id,
        "skill_version": trace.skill_version,
        "total_entries": len(trace.entries),
        "deterministic": all(e.deterministic for e in trace.entries),
        "rule_paths_used": {rp: len(idxs) for rp, idxs in rule_paths.items()},
        "states_covered": sorted(set(e.state for e in trace.entries)),
        "decision_types": sorted(set(e.decision_type for e in trace.entries)),
        "duration": trace.completed_at,
    }


def verify_determinism(trace_a: ExecutionTrace, trace_b: ExecutionTrace) -> dict:
    """Compare two traces from the same input to verify determinism.

    Returns a comparison report showing whether both runs produced
    identical decisions at each step.
    """
    if len(trace_a.entries) != len(trace_b.entries):
        return {
            "match": False,
            "reason": f"Entry count mismatch: {len(trace_a.entries)} vs {len(trace_b.entries)}",
            "divergences": [],
        }

    divergences = []
    for i, (ea, eb) in enumerate(zip(trace_a.entries, trace_b.entries)):
        if ea.decision_type != eb.decision_type:
            divergences.append({
                "index": i,
                "field": "decision_type",
                "a": ea.decision_type,
                "b": eb.decision_type,
            })
        if ea.result["decision"] != eb.result["decision"]:
            divergences.append({
                "index": i,
                "field": "decision",
                "a": ea.result["decision"],
                "b": eb.result["decision"],
            })
        if abs(ea.result["score"] - eb.result["score"]) > 0.001:
            divergences.append({
                "index": i,
                "field": "score",
                "a": ea.result["score"],
                "b": eb.result["score"],
            })

    return {
        "match": len(divergences) == 0,
        "total_compared": len(trace_a.entries),
        "divergence_count": len(divergences),
        "divergences": divergences,
    }


def diff_traces(trace_a: ExecutionTrace, trace_b: ExecutionTrace) -> dict:
    """Produce a human-readable diff of two execution traces.

    Useful for debugging when determinism verification fails.
    """
    result = verify_determinism(trace_a, trace_b)
    result["summary"] = (
        f"{'IDENTICAL' if result['match'] else 'DIVERGENT'}: "
        f"{result['total_compared']} entries compared, "
        f"{result['divergence_count']} divergences found"
    )
    result["trace_a_run_id"] = trace_a.run_id
    result["trace_b_run_id"] = trace_b.run_id
    return result


# =============================================================================
# Helpers
# =============================================================================

def _hash_input(data: dict) -> str:
    """Produce a deterministic SHA256 hash of normalized input."""
    normalized = json.dumps(data, sort_keys=True, ensure_ascii=False, default=str)
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()[:16]


def load_trace(path: str) -> ExecutionTrace:
    """Load a trace from a JSON file and reconstruct the ExecutionTrace object."""
    raw = load_json(path)
    trace = ExecutionTrace(
        run_id=raw.get("run_id", ""),
        skill_version=raw.get("skill_version", "2.2.0"),
        started_at=raw.get("started_at", ""),
        completed_at=raw.get("completed_at", ""),
        summary=raw.get("summary", {}),
        verification=raw.get("verification", {}),
    )
    for e_raw in raw.get("entries", []):
        trace.entries.append(TraceEntry(
            index=e_raw.get("index", 0),
            timestamp=e_raw.get("timestamp", ""),
            state=e_raw.get("state", ""),
            decision_type=e_raw.get("decision_type", ""),
            input_hash=e_raw.get("input_hash", ""),
            result=e_raw.get("result", {}),
            rule_path=e_raw.get("rule_path", ""),
            deterministic=e_raw.get("deterministic", True),
        ))
    return trace


def trace_to_dict(trace: ExecutionTrace) -> dict:
    """Serialize an ExecutionTrace to a JSON-serializable dict."""
    return {
        "run_id": trace.run_id,
        "skill_version": trace.skill_version,
        "started_at": trace.started_at,
        "completed_at": trace.completed_at,
        "entries": [asdict(e) for e in trace.entries],
        "summary": trace.summary,
        "verification": trace.verification,
    }


# =============================================================================
# CLI
# =============================================================================

def main() -> int:
    ap = argparse.ArgumentParser(
        description="Execution Trace — deterministic decision recording and replay (v2.2)"
    )
    sub = ap.add_subparsers(dest="command", required=True)

    # -- record
    rec = sub.add_parser("record", help="Record a single decision into a trace")
    rec.add_argument("--trace", required=True, help="Path to trace file (will create if not exists)")
    rec.add_argument("--run-id", help="Run ID (required for new trace)")
    rec.add_argument("--state", required=True, help="State machine state")
    rec.add_argument("--decision-type", required=True, help="Decision type")
    rec.add_argument("--input", required=True, help="Input JSON for the decision")
    rec.add_argument("--result", required=True, help="Decision result JSON")

    # -- finalize
    fin = sub.add_parser("finalize", help="Finalize a trace (compute summary)")
    fin.add_argument("--trace", required=True, help="Path to trace file")

    # -- replay
    rep = sub.add_parser("replay", help="Replay and analyze a trace")
    rep.add_argument("--trace", required=True, help="Path to trace file")

    # -- verify
    ver = sub.add_parser("verify", help="Verify determinism between two traces")
    ver.add_argument("--trace-a", required=True, help="First trace file")
    ver.add_argument("--trace-b", required=True, help="Second trace file")

    # -- diff
    dif = sub.add_parser("diff", help="Diff two traces")
    dif.add_argument("--trace-a", required=True, help="First trace file")
    dif.add_argument("--trace-b", required=True, help="Second trace file")

    args = ap.parse_args()

    if args.command == "record":
        # Load or create trace
        if os.path.exists(args.trace):
            trace = load_trace(args.trace)
        else:
            if not args.run_id:
                print("Error: --run-id required for new trace", file=sys.stderr)
                return 2
            trace = create_trace(args.run_id)

        input_data = load_json(args.input)
        result_data = load_json(args.result)
        record_decision(trace, args.state, args.decision_type, input_data, result_data)
        with open(args.trace, "w", encoding="utf-8") as f:
            f.write(dump_json(trace_to_dict(trace)))
        print(dump_json({"recorded": True, "entry_index": len(trace.entries) - 1}))
        return 0

    elif args.command == "finalize":
        trace = load_trace(args.trace)
        finalize_trace(trace)
        with open(args.trace, "w", encoding="utf-8") as f:
            f.write(dump_json(trace_to_dict(trace)))
        print(dump_json(trace.summary))
        return 0

    elif args.command == "replay":
        trace = load_trace(args.trace)
        report = replay_trace(trace)
        print(dump_json(report))
        return 0

    elif args.command == "verify":
        trace_a = load_trace(args.trace_a)
        trace_b = load_trace(args.trace_b)
        result = verify_determinism(trace_a, trace_b)
        print(dump_json(result))
        return 0 if result["match"] else 1

    elif args.command == "diff":
        trace_a = load_trace(args.trace_a)
        trace_b = load_trace(args.trace_b)
        result = diff_traces(trace_a, trace_b)
        print(dump_json(result))
        return 0 if result["match"] else 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
