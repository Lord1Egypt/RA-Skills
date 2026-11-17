#!/usr/bin/env python3
"""Execution State Recovery System — checkpoint retry, partial resume, rollback.

Provides fault-tolerance for the state machine:
  1. checkpoint retry: re-attempt a failed state transition with backoff
  2. partial state resume: resume ACTIVE_TESTING from where it left off
     (skip already-probed endpoints), not from the beginning of the state
  3. failure rollback: on catastrophic failure, roll back to the previous
     state and re-attempt with a degraded strategy

Works in conjunction with state.py (StateSerializer) which handles the
atomic checkpoint writes. This module adds the RECOVERY LOGIC on top.

Usage (CLI):
  python state_recovery.py --checkpoint runs/run-001.json --mode check
  python state_recovery.py --checkpoint runs/run-001.json --mode resume
  python state_recovery.py --checkpoint runs/run-001.json --mode rollback
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from dataclasses import dataclass, field

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils import load_json, dump_json, utc_now_iso
from state import STATES, next_state, StateSerializer

# ---- Retry configuration ----------------------------------------------------
MAX_CHECKPOINT_RETRIES = 3
RETRY_BACKOFF_MS = [500, 1000, 2000]  # exponential backoff schedule

# States that support partial resume (can skip already-done work)
PARTIAL_RESUME_STATES = {"ACTIVE_TESTING", "VALIDATION"}

# States that can be rolled back to (must be "safe" — no side effects to undo)
ROLLBACK_SAFE_STATES = {"INIT", "SCOPE_CHECK", "PRE_FLIGHT", "RECONNAISSANCE"}


@dataclass
class RecoveryPlan:
    """The recovery strategy for a failed or interrupted state transition."""

    action: str  # "resume" | "retry" | "rollback" | "abort"
    target_state: str
    reason: str
    partial_results: dict = field(default_factory=dict)
    retry_schedule: list = field(default_factory=list)
    rollback_to: str | None = None
    skipped_items: list = field(default_factory=list)
    degraded_strategy: str | None = None


def validate_checkpoint(checkpoint: dict) -> tuple[bool, str]:
    """Verify a checkpoint is structurally valid and can be resumed.

    Implements formal_algorithms.md §6.1: CanResume(c).
    """
    if not isinstance(checkpoint, dict):
        return False, "checkpoint is not a dict"

    current = checkpoint.get("current", "")
    if current not in STATES:
        return False, f"invalid state '{current}'"
    if current == "DONE":
        return False, "run already completed"

    history = checkpoint.get("history", [])
    if not history:
        return False, "history is empty"

    context = checkpoint.get("context_snapshot", {})
    if not context.get("scope"):
        return False, "context_snapshot missing scope"
    if not context.get("targets"):
        return False, "context_snapshot missing targets"

    ts = checkpoint.get("checkpointed_at", "")
    if not ts:
        return False, "checkpointed_at is missing"

    return True, current


def build_partial_resume_plan(checkpoint: dict) -> RecoveryPlan:
    """Build a partial resume plan for ACTIVE_TESTING / VALIDATION.

    Implements formal_algorithms.md §6.2: ResumePlan(c).
    Skips already-probed targets/endpoints to avoid redundant work.
    """
    current = checkpoint.get("current", "")
    partial = checkpoint.get("partial_results", {})

    if current in PARTIAL_RESUME_STATES and partial:
        probed = set(partial.get("probed_targets", []))
        probed_endpoints = set(partial.get("probed_endpoints", []))
        validated_findings = partial.get("validated_findings", [])
        candidate_count = partial.get("candidate_count", 0)

        plan = RecoveryPlan(
            action="resume",
            target_state=current,
            reason=f"partial resume at {current}: {len(probed)} targets already probed, "
                   f"{len(validated_findings)} findings validated, "
                   f"{candidate_count - len(validated_findings)} remaining",
            partial_results=partial,
            skipped_items=sorted(probed_endpoints),
        )
        return plan
    else:
        # No partial results — restart the state from scratch
        return RecoveryPlan(
            action="resume",
            target_state=current,
            reason=f"no partial results for {current}; restarting state from beginning",
            degraded_strategy="full_restart",
        )


def build_retry_plan(checkpoint: dict, failure_reason: str, attempt: int = 1) -> RecoveryPlan:
    """Build a retry plan for a failed state transition.

    Implements checkpoint retry with exponential backoff.
    """
    current = checkpoint.get("current", "")

    if attempt < MAX_CHECKPOINT_RETRIES:
        schedule = []
        for i in range(MAX_CHECKPOINT_RETRIES - attempt + 1):
            delay = RETRY_BACKOFF_MS[min(i, len(RETRY_BACKOFF_MS) - 1)]
            schedule.append({"attempt": attempt + i, "delay_ms": delay})

        return RecoveryPlan(
            action="retry",
            target_state=current,
            reason=f"state transition failed at {current}: {failure_reason}; "
                   f"retrying with backoff (attempt {attempt}/{MAX_CHECKPOINT_RETRIES})",
            retry_schedule=schedule,
            degraded_strategy="retry_same_strategy" if attempt == 1 else "retry_reduced_tier",
        )
    else:
        # Exhausted retries → rollback
        return build_rollback_plan(checkpoint, f"retries exhausted at {current}: {failure_reason}")


def build_rollback_plan(checkpoint: dict, failure_reason: str) -> RecoveryPlan:
    """Build a rollback plan to revert to the previous safe state.

    Implements formal_algorithms.md §6.3: Rollback(c, S).
    """
    current = checkpoint.get("current", "")
    history = checkpoint.get("history", [])

    # Find the previous state
    idx = STATES.index(current) if current in STATES else -1
    prev_state = STATES[idx - 1] if idx > 0 else None

    if prev_state and prev_state in ROLLBACK_SAFE_STATES:
        return RecoveryPlan(
            action="rollback",
            target_state=prev_state,
            reason=f"catastrophic failure at {current}: {failure_reason}; "
                   f"rolling back to {prev_state}",
            rollback_to=prev_state,
            degraded_strategy="rollback_and_retry_reduced",
        )
    else:
        return RecoveryPlan(
            action="abort",
            target_state="ABORT",
            reason=f"cannot rollback from {current}: no safe previous state; aborting run. "
                   f"Failure: {failure_reason}",
        )


def execute_rollback(checkpoint: dict, rollback_to: str) -> dict:
    """Execute a rollback: restore context, append rollback event, set state.

    Returns an updated checkpoint dict. The caller is responsible for
    persisting it via StateSerializer.checkpoint().
    """
    out = json.loads(json.dumps(checkpoint))  # deep copy
    out["current"] = rollback_to
    out["history"].append({
        "ts": utc_now_iso(),
        "state": rollback_to,
        "msg": f"ROLLBACK from {checkpoint.get('current', '?')} to {rollback_to}",
        "event_type": "rollback",
        "reason": checkpoint.get("_last_failure_reason", "unknown"),
    })
    # Clear partial results since we're going back to a pre-failure state
    out["partial_results"] = {}
    out["_rollback_count"] = out.get("_rollback_count", 0) + 1
    return out


def save_partial_progress(checkpoint: dict, state: str, probed_targets: list,
                          probed_endpoints: list, validated_findings: list,
                          candidate_count: int) -> dict:
    """Save partial progress for a resumable state.

    Called by the agent DURING ACTIVE_TESTING/VALIDATION to checkpoint
    progress so a crash/resume doesn't lose work.
    """
    out = json.loads(json.dumps(checkpoint))
    out["current"] = state
    out["partial_results"] = {
        "probed_targets": probed_targets,
        "probed_endpoints": probed_endpoints,
        "validated_findings": validated_findings,
        "candidate_count": candidate_count,
        "saved_at": utc_now_iso(),
    }
    return out


def recover(checkpoint: dict, failure_reason: str | None = None, attempt: int = 1) -> dict:
    """Main entry point: determine the recovery strategy for a checkpoint.

    If failure_reason is provided → retry/rollback path.
    If failure_reason is None → resume path (partial or full restart).
    """
    valid, current = validate_checkpoint(checkpoint)
    if not valid:
        return {
            "action": "abort",
            "target_state": "ABORT",
            "reason": f"checkpoint invalid: {current}",
        }

    if failure_reason:
        plan = build_retry_plan(checkpoint, failure_reason, attempt)
        if plan.action == "retry" and attempt >= MAX_CHECKPOINT_RETRIES:
            plan = build_rollback_plan(checkpoint, failure_reason)
    else:
        plan = build_partial_resume_plan(checkpoint)

    return {
        "action": plan.action,
        "target_state": plan.target_state,
        "reason": plan.reason,
        "partial_results": plan.partial_results,
        "retry_schedule": plan.retry_schedule,
        "rollback_to": plan.rollback_to,
        "skipped_items": plan.skipped_items,
        "degraded_strategy": plan.degraded_strategy,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Execution state recovery system")
    ap.add_argument("--checkpoint", required=True, help="Checkpoint JSON (path or '-')")
    ap.add_argument("--mode", required=True, choices=["check", "resume", "rollback", "retry"],
                    help="Recovery mode")
    ap.add_argument("--failure-reason", help="Failure reason (for retry/rollback mode)")
    ap.add_argument("--attempt", type=int, default=1, help="Current retry attempt number")
    args = ap.parse_args()

    checkpoint = load_json(args.checkpoint)

    if args.mode == "check":
        valid, msg = validate_checkpoint(checkpoint)
        print(dump_json({"valid": valid, "current_state": msg if valid else None,
                         "reason": None if valid else msg}))
        return 0 if valid else 1

    elif args.mode == "resume":
        plan = recover(checkpoint)
        print(dump_json(plan))
        return 0 if plan["action"] != "abort" else 1

    elif args.mode == "retry":
        plan = recover(checkpoint, args.failure_reason or "unspecified", args.attempt)
        print(dump_json(plan))
        return 0 if plan["action"] != "abort" else 1

    elif args.mode == "rollback":
        plan = build_rollback_plan(checkpoint, args.failure_reason or "manual rollback")
        if plan.action == "rollback":
            rolled_back = execute_rollback(checkpoint, plan.rollback_to)
            print(dump_json({
                "plan": {"action": plan.action, "target_state": plan.target_state,
                         "reason": plan.reason, "rollback_to": plan.rollback_to},
                "rolled_back_checkpoint": rolled_back,
            }))
            return 0
        else:
            print(dump_json({"plan": {"action": plan.action, "reason": plan.reason}}))
            return 1

    return 2


if __name__ == "__main__":
    sys.exit(main())
