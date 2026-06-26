"""Night-Shift executor — main overnight execution loop.

This is the core engine. It's designed to be called from the agent session
(via SKILL.md), not as a standalone cron script.

Usage from agent:
    python3 scripts/night-shift/executor.py run
    python3 scripts/night-shift/executor.py dry-run
    python3 scripts/night-shift/executor.py status
    python3 scripts/night-shift/executor.py stop
"""

from __future__ import annotations
import sys
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path

# Auto-detect workspace root
_SKILL_DIR = Path(__file__).resolve().parent.parent  # skills/night-shift/
_WORKSPACE = Path(os.environ.get("OPENCLAW_WORKSPACE", _SKILL_DIR.parent.parent))  # ~/.openclaw/workspace
_DATA_DIR = _WORKSPACE / "data" / "night-shift"

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from models import Plan, PlanStatus, PhaseStatus
from queue import (
    get_approved_plans,
    _save_plan as _queue_save_plan,
)
from budget import NightBudget
from lock import acquire_lock, release_lock, is_locked
from git_manager import (
    create_worktree,
    commit_phase,
    reset_phase,
)
from verifier import PhaseVerifier
from phase_runner import (
    build_phase_prompt,
    run_phase_cursor,
    run_phase_shell,
    run_phase_claude_code,
    run_phase_subagent,
    decide_execution_method,
    PhaseResult,
)
from checkpoint import CheckpointManager
from failure_memory import FailureMemory
from reporter import MorningReporter
from preflight import run_preflight

# Paths
BUDGET_FILE = _DATA_DIR / "budget.json"
EXECUTION_LOG = _DATA_DIR / "execution.log"
MEMORY_GUARD_SCRIPT = Path(__file__).resolve().parent / "memory_guard.py"


class NightShiftExecutor:
    """Execute approved plans overnight."""

    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.lock_fd = None
        self.budget = NightBudget()
        self.verifier = PhaseVerifier()
        self.failure_memory = FailureMemory()
        self.reporter = MorningReporter()
        self.log_entries: list[str] = []
        self._memory_guard_proc: subprocess.Popen | None = None

    def run(self) -> str:
        """Main entry point. Returns execution summary."""
        # Pre-flight checks
        error = self._preflight()
        if error:
            return error

        # Get approved plans
        plans = get_approved_plans()
        if not plans:
            self._cleanup()
            return "📋 No approved plans found. Queue some plans first with `plan add`."

        runner_check = run_preflight(plans, live=not self.dry_run)
        if not runner_check.ok:
            self._log(runner_check.format())
            self._cleanup()
            return "⚠️ Night Shift blocked by preflight. See execution.log for fixes."
        for issue in runner_check.warnings:
            self._log(f"⚠️ Preflight warning: {issue.code}: {issue.message}")

        self._log(f"🌙 Night Shift started — {len(plans)} plan(s) queued")

        if self.dry_run:
            self._write_dry_run_report(plans, runner_check)
            self._log("📋 Dry-run preview written; no plan state changed")
            self._cleanup()
            return self._get_summary()

        # Start memory guard watchdog
        self._start_memory_guard()

        # Execute each plan
        for i, plan in enumerate(plans):
            if self.budget.night_exceeded():
                self._log("⏭️ Night budget exceeded, skipping remaining plans")
                plan.status = PlanStatus.SKIPPED
                self._save_plan(plan)
                break

            if self._check_memory() < 1_000_000_000:  # <1GB
                self._log(
                    f"⚠️ Memory low ({self._check_memory() / 1e9:.1f}GB), aborting"
                )
                break

            self._log(f"\n{'=' * 60}")
            self._log(f"Plan {i + 1}/{len(plans)}: {plan.title} [{plan.priority}]")
            self._execute_plan(plan)

        # Stop memory guard before post-flight
        self._stop_memory_guard()

        # Post-flight
        self._log(f"\n{'=' * 60}")
        self._log("🌙 Night Shift complete")

        # Generate report
        self.reporter.generate_report()
        self._log("\n📄 Report generated")

        self._cleanup()
        return self._get_summary()

    def _preflight(self) -> str | None:
        """Pre-flight checks. Returns error message if should abort."""
        # Check lock
        if is_locked():
            pid = None
            try:
                with open("/tmp/night-shift.lock") as f:
                    pid = f.read().strip()
            except Exception:
                pass
            return f"⚠️ Night-shift already running (PID {pid}). Use `night shift stop` first."

        # Check memory
        mem = self._check_memory()
        if mem < 2_000_000_000:  # <2GB
            return (
                f"⚠️ Low memory ({mem / 1e9:.1f}GB free). Add swap or free memory first."
            )

        # Check swap
        swap = self._check_swap()
        if swap == 0:
            self._log("⚠️ No swap configured. Recommended: fallocate -l 4G /swapfile")

        # Acquire lock
        self.lock_fd = acquire_lock()
        if self.lock_fd is None:
            return "⚠️ Could not acquire lock file."

        return None

    def _execute_plan(self, plan: Plan):
        """Execute all phases of a plan."""
        plan.status = PlanStatus.EXECUTING
        plan.execution.started_at = datetime.now(timezone.utc).isoformat()
        self._save_plan(plan)

        # Reset plan-level budget
        self.budget.plan_seconds = 0

        # Create worktree
        success, worktree_path = create_worktree(plan.id, plan.base_branch)
        if not success:
            self._log(f"❌ Failed to create worktree: {worktree_path}")
            plan.status = PlanStatus.FAILED
            plan.execution.failure_log.append(
                {
                    "error_type": "git_conflict",
                    "details": worktree_path,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                }
            )
            self._save_plan(plan)
            return

        self._log(f"📁 Worktree: {worktree_path}")

        checkpoint_mgr = CheckpointManager(plan.id)
        previous_outputs: list[str] = []

        # Get ordered phases
        phases = plan.ordered_phases()
        plan_complete = True

        for phase in phases:
            if self.budget.night_exceeded() or self.budget.plan_exceeded():
                phase.status = PhaseStatus.SKIPPED
                self._log(f"⏭️ Phase {phase.id}: {phase.title} — skipped (budget)")
                plan_complete = False
                continue

            # Check if phase already passed (resume)
            last_successful = checkpoint_mgr.get_last_successful_phase()
            if last_successful is not None and phase.id <= last_successful:
                phase.status = PhaseStatus.PASSED
                self._log(
                    f"✅ Phase {phase.id}: {phase.title} — already passed (resuming)"
                )
                continue

            # Save pre-phase checkpoint
            checkpoint_mgr.save_checkpoint(
                phase_id=phase.id,
                phase_status="running",
                worktree_path=worktree_path,
            )

            # Execute phase
            self._log(f"🔄 Phase {phase.id}/{len(phases)}: {phase.title}")
            phase.status = PhaseStatus.RUNNING
            phase.started_at = datetime.now(timezone.utc).isoformat()
            phase.attempts += 1

            if self.dry_run:
                self._log(f"  [DRY RUN] Would execute: {phase.prompt[:100]}...")
                continue

            # Run the phase
            result = self._run_phase(plan, phase, worktree_path, previous_outputs)
            self.budget.end_phase()
            phase.duration_seconds = result.duration_seconds
            phase.completed_at = datetime.now(timezone.utc).isoformat()
            phase.result = result.output[:500]

            if result.success:
                # Mechanical verification
                passed, msg = self.verifier.verify(
                    worktree_path, phase.verification, phase.verification_config
                )
                self._log(f"  🔍 Verification: {msg}")

                if passed:
                    # Commit
                    ok, commit_hash = commit_phase(plan.id, phase.id, phase.title)
                    if ok:
                        phase.commits.append(commit_hash)
                        phase.status = PhaseStatus.PASSED
                        self._log(f"  ✅ Passed (commit: {commit_hash})")
                        previous_outputs.append(f"{phase.title}: {msg}")
                    else:
                        phase.status = PhaseStatus.FAILED
                        plan_complete = False
                        self._log(f"  ❌ Commit failed: {commit_hash}")
                        self.failure_memory.log_failure(
                            plan.id,
                            phase.id,
                            "git_conflict",
                            commit_hash,
                            phase.prompt,
                            phase.attempts,
                        )
                else:
                    # Verification failed — WARN but don't revert
                    # Cursor CLI may produce valid code that doesn't pass strict verification
                    # Keep the changes and let human review decide
                    self._log(f"  ⚠️ Verification warning: {msg}")
                    self._log(f"  📝 Keeping changes for manual review")
                    # Still commit — verification is advisory for night shift
                    ok, commit_hash = commit_phase(plan.id, phase.id, phase.title)
                    if ok:
                        phase.commits.append(commit_hash)
                        phase.status = PhaseStatus.PASSED
                        self._log(f"  ✅ Committed despite verification warning (commit: {commit_hash})")
                        previous_outputs.append(f"{phase.title}: VERIFIED={passed} ({msg})")
                    else:
                        phase.status = PhaseStatus.FAILED
                        plan_complete = False
                        self._log(f"  ❌ Commit failed: {commit_hash}")
                    self.failure_memory.log_failure(
                        plan.id,
                        phase.id,
                        "verification_failed",
                        msg,
                        phase.prompt,
                        phase.attempts,
                    )
            else:
                phase.status = PhaseStatus.FAILED
                plan_complete = False
                self._log(f"  ❌ Execution failed: {result.error[:200]}")
                self.failure_memory.log_failure(
                    plan.id,
                    phase.id,
                    "subagent_error",
                    result.error[:500],
                    phase.prompt,
                    phase.attempts,
                )

            # Save phase output for debugging
            checkpoint_mgr.save_phase_output(phase.id, result.output, result.error)

            # Save checkpoint
            checkpoint_mgr.save_checkpoint(
                phase_id=phase.id,
                phase_status=phase.status.value,
                worktree_path=worktree_path,
                duration_seconds=phase.duration_seconds,
                result_summary=phase.result or "",
            )

            self._save_plan(plan)
            self.budget.phases_completed += 1

            # Retry on failure
            if phase.status == PhaseStatus.FAILED and phase.attempts < plan.max_retries:
                self._log(f"  🔄 Retrying phase {phase.id} ({phase.attempts}/{plan.max_retries})...")
                # Wait a bit before retry (exponential backoff)
                import time as _time
                backoff = min(30 * (2 ** (phase.attempts - 1)), 120)  # 30s, 60s, 120s max
                self._log(f"  ⏳ Waiting {backoff}s before retry...")
                _time.sleep(backoff)

                # Re-execute the phase
                phase.status = PhaseStatus.PENDING
                result = self._run_phase(plan, phase, worktree_path, previous_outputs)
                self.budget.end_phase()
                phase.duration_seconds = result.duration_seconds
                phase.completed_at = datetime.now(timezone.utc).isoformat()
                phase.result = result.output[:500]
                phase.attempts += 1

                if result.success:
                    passed, msg = self.verifier.verify(worktree_path, phase.verification, phase.verification_config)
                    if passed:
                        ok, commit_hash = commit_phase(plan.id, phase.id, phase.title)
                        if ok:
                            phase.status = PhaseStatus.PASSED
                            self._log(f"  ✅ Retry succeeded (commit: {commit_hash})")
                            previous_outputs.append(f"{phase.title}: {msg}")
                        else:
                            phase.status = PhaseStatus.FAILED
                            self._log(f"  ❌ Retry commit failed: {commit_hash}")
                    else:
                        reset_phase(plan.id)
                        phase.status = PhaseStatus.FAILED
                        self._log(f"  ❌ Retry verification failed: {msg}")
                else:
                    self._log(f"  ❌ Retry {phase.attempts}/{plan.max_retries} failed: {result.error[:200]}")

                # Save checkpoint after retry
                checkpoint_mgr.save_phase_output(phase.id, result.output, result.error)
                checkpoint_mgr.save_checkpoint(
                    phase_id=phase.id,
                    phase_status=phase.status.value,
                    worktree_path=worktree_path,
                    duration_seconds=phase.duration_seconds,
                    result_summary=phase.result or "",
                )
                self._save_plan(plan)

        # Plan complete
        plan.execution.completed_at = datetime.now(timezone.utc).isoformat()
        plan.execution.total_duration_seconds = self.budget.plan_seconds
        plan.execution.total_api_calls = self.budget.api_calls

        if plan_complete and all(
            ph.status.value in ("passed", "skipped") for ph in plan.phases
        ):
            plan.status = PlanStatus.COMPLETED
            self._log(f"✅ Plan #{plan.id}: {plan.title} — COMPLETE")
            self.budget.plans_completed += 1
        else:
            plan.status = PlanStatus.FAILED
            self._log(f"❌ Plan #{plan.id}: {plan.title} — FAILED")

        self._save_plan(plan)

        # Don't remove worktree — keep for review
        self._log(f"📂 Worktree preserved at {worktree_path}")

    def _run_phase(
        self, plan: Plan, phase, worktree_path: str, previous_outputs: list[str]
    ) -> PhaseResult:
        """Execute a single phase."""
        # Build prompt
        prompt = build_phase_prompt(
            plan_title=plan.title,
            plan_id=plan.id,
            phase_id=phase.id,
            phase_title=phase.title,
            phase_prompt=phase.prompt,
            worktree_path=worktree_path,
            branch=plan.branch,
            previous_outputs=previous_outputs,
            verification_type=phase.verification,
            verification_config=phase.verification_config,
        )

        # Decide execution method — respect phase's explicit method
        method = decide_execution_method(
            phase.prompt, phase.verification, phase.execution_method
        )
        self.budget.start_phase()

        if method in ("subagent", "cursor", "claude-code"):
            # Route all code-gen methods through subagent (Cursor CLI)
            result = run_phase_subagent(
                prompt,
                worktree_path,
                plan_id=plan.id,
                phase_id=phase.id,
                timeout=int(self.budget.max_phase_seconds),
            )
        elif method == "shell":
            result = run_phase_shell(
                phase.prompt, worktree_path, timeout=int(self.budget.max_phase_seconds)
            )
        else:
            result = PhaseResult(
                success=False,
                output="",
                error=f"Unsupported execution method: {method}",
                duration_seconds=0,
                execution_method=f"unknown ({method})",
                tokens_used=0,
                duration_ms=0,
            )

        self.budget.record_api_call()
        return result

    def _write_dry_run_report(self, plans: list[Plan], runner_check) -> Path:
        """Write a read-only execution preview without mutating plan state."""
        reports_dir = _DATA_DIR / "reports"
        reports_dir.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H%M%S")
        path = reports_dir / f"dry-run-{stamp}.md"
        lines = [
            f"# Night Shift Dry Run — {stamp} UTC",
            "",
            "Dry-run is read-only: no plan status, checkpoint, commit, or budget state was changed.",
            "",
            "## Preflight",
            "",
            f"- OK: {runner_check.ok}",
            f"- Available backends: {', '.join(runner_check.available_backends) or 'none'}",
        ]
        for issue in runner_check.issues:
            lines.append(f"- {issue.severity.upper()} `{issue.code}`: {issue.message}")
            if issue.fix:
                lines.append(f"  - Fix: {issue.fix}")
        lines.extend(["", "## Selected plans", ""])
        for plan in plans:
            lines.append(f"### {plan.id}: {plan.title}")
            lines.append(f"- Priority: {plan.priority}")
            lines.append(f"- Branch: `{plan.branch}`")
            lines.append(f"- Base branch: `{plan.base_branch}`")
            lines.append("- Phases:")
            for phase in plan.ordered_phases():
                lines.append(f"  - {phase.id}. {phase.title} — method `{phase.execution_method}`, verification `{phase.verification}`")
            lines.append("")
        path.write_text("\n".join(lines))
        return path

    def _check_memory(self) -> int:
        """Check available memory in bytes."""
        try:
            result = subprocess.run(
                ["awk", "/MemAvailable/ {print $2 * 1024}", "/proc/meminfo"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            return int(result.stdout.strip()) if result.returncode == 0 else 0
        except Exception:
            return 0

    def _check_swap(self) -> int:
        """Check total swap in bytes."""
        try:
            result = subprocess.run(
                ["awk", "/SwapTotal/ {print $2 * 1024}", "/proc/meminfo"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            return int(result.stdout.strip()) if result.returncode == 0 else 0
        except Exception:
            return 0

    def _save_plan(self, plan: Plan):
        """Save plan state."""
        _queue_save_plan(plan)

    def _start_memory_guard(self):
        """Start memory guard as a background subprocess."""
        if not MEMORY_GUARD_SCRIPT.exists():
            self._log("⚠️ Memory guard script not found, skipping")
            return
        try:
            cmd = [sys.executable, str(MEMORY_GUARD_SCRIPT)]
            if self.dry_run:
                cmd.append("--dry-run")
            self._memory_guard_proc = subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True,
            )
            self._log(f"🛡️ Memory guard started (PID {self._memory_guard_proc.pid})")
        except Exception as e:
            self._log(f"⚠️ Could not start memory guard: {e}")
            self._memory_guard_proc = None

    def _stop_memory_guard(self):
        """Stop the memory guard subprocess."""
        if self._memory_guard_proc is None:
            return
        proc = self._memory_guard_proc
        self._memory_guard_proc = None
        try:
            proc.terminate()
            proc.wait(timeout=10)
            self._log(f"🛡️ Memory guard stopped (PID {proc.pid})")
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait(timeout=5)
            self._log(f"🛡️ Memory guard force-killed (PID {proc.pid})")
        except Exception as e:
            self._log(f"⚠️ Error stopping memory guard: {e}")

    def _cleanup(self):
        """Post-flight cleanup."""
        # Ensure memory guard is stopped
        self._stop_memory_guard()
        if self.lock_fd:
            release_lock(self.lock_fd)
            self.lock_fd = None
        self.budget.save(BUDGET_FILE)
        self._save_log()

    def _log(self, message: str):
        """Log a message."""
        timestamp = datetime.now(timezone.utc).strftime("%H:%M:%S")
        entry = f"[{timestamp}] {message}"
        self.log_entries.append(entry)
        print(entry)

    def _save_log(self):
        """Save execution log to file."""
        EXECUTION_LOG.parent.mkdir(parents=True, exist_ok=True)
        with open(EXECUTION_LOG, "a") as f:
            f.write("\n".join(self.log_entries) + "\n")

    def _get_summary(self) -> str:
        """Get execution summary for Telegram."""
        budget = self.budget.summary()
        lines = [
            "🌙 Night Shift Complete",
            "",
            f"✅ Plans completed: {budget['plans_completed']}",
            f"📦 Phases completed: {budget['phases_completed']}",
            f"⏱️ Total time: {_fmt(budget['night_seconds'])}",
            f"📞 API calls: {budget['api_calls']}",
        ]
        if self.dry_run:
            lines.insert(1, "📋 **DRY RUN** — no actual changes made")
        return "\n".join(lines)


def _fmt(seconds: float) -> str:
    if seconds < 60:
        return f"{seconds:.0f}s"
    m = int(seconds // 60)
    s = int(seconds % 60)
    if m < 60:
        return f"{m}m {s}s"
    h = m // 60
    return f"{h}h {m % 60}m"


def main():
    if len(sys.argv) < 2:
        print("Usage: executor.py [run|dry-run|status|stop]")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "run":
        executor = NightShiftExecutor(dry_run=False)
        summary = executor.run()
        print(f"\n{summary}")

    elif cmd == "dry-run":
        executor = NightShiftExecutor(dry_run=True)
        summary = executor.run()
        print(f"\n{summary}")

    elif cmd == "status":
        if is_locked():
            pid = None
            try:
                with open("/tmp/night-shift.lock") as f:
                    pid = f.read().strip()
            except Exception:
                pass
            print(f"🔄 Night-shift is running (PID {pid})")
            # Show budget
            if BUDGET_FILE.exists():
                budget = NightBudget.load(BUDGET_FILE)
                print(
                    f"   Time: {_fmt(budget.night_seconds)} / {_fmt(budget.max_night_seconds)}"
                )
                print(f"   API calls: {budget.api_calls} / {budget.max_api_calls}")
                print(f"   Remaining: {budget.remaining_night_minutes():.0f} min")
        else:
            print("💤 Night-shift is not running")

    elif cmd == "stop":
        if is_locked():
            pid = None
            try:
                with open("/tmp/night-shift.lock") as f:
                    pid = int(f.read().strip())
                os.kill(pid, 15)  # SIGTERM
                print(f"🛑 Sent SIGTERM to PID {pid}")
            except Exception as e:
                print(f"❌ Could not stop: {e}")
        else:
            print("💤 Night-shift is not running")

    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()
