"""
Progressive Validator — Multi-Stage Backtest Validation Framework
=================================================================
Fail fast with short backtest windows before committing to expensive
full-period runs. Each stage has increasing duration and stricter thresholds.

Usage:
    validator = ProgressiveValidator(config_file="config.json")
    validator.run_stage("smoke_test", "path/to/strategy.py", "MyStrategy_v1")
    # If passed, run next stage:
    validator.run_stage("stress_test", "path/to/strategy.py", "MyStrategy_v1")
"""
import argparse
import json
import os
import sys
import time
from datetime import datetime
from typing import Dict, List, Optional


DEFAULT_STAGES = {
    "smoke_test": {
        "start": "2024-01-01",
        "end": "2024-03-31",
        "max_dd": 0.50,
        "expected_time": "15-20 min",
        "purpose": "Eliminate obvious bugs and catastrophic flaws",
        "order": 1,
    },
    "stress_test": {
        "start": "2024-02-01",
        "end": "2024-06-30",
        "max_dd": 0.45,
        "expected_time": "25-30 min",
        "purpose": "Test survival in worst market conditions",
        "order": 2,
    },
    "medium": {
        "start": "2024-01-01",
        "end": "2025-06-30",
        "max_dd": 0.42,
        "expected_time": "45-60 min",
        "purpose": "Validate across bull/bear transitions",
        "order": 3,
    },
    "full": {
        "start": "2023-01-01",
        "end": "2026-01-31",
        "max_dd": 0.40,
        "expected_time": "2-3 hours",
        "purpose": "Final acceptance benchmark",
        "order": 4,
    },
}

SKIP_RULES = """
=== Progressive Validation Skip Rules ===

1. NEVER skip the smoke_test stage.
   - It catches fatal bugs in minutes, not hours.

2. You MAY skip stress_test only if:
   - The strategy has already been validated on the same date range
     in a prior iteration with zero code changes.

3. You MAY skip medium only if:
   - Both smoke_test AND stress_test passed with Sharpe >= 2.5
     and drawdown < 30%.

4. The full stage can NEVER be skipped.
   - It is the final acceptance gate.

5. If any code change is made (even a single parameter tweak),
   restart from smoke_test.

6. Results older than 30 days should be considered stale.
   Re-run from the earliest stale stage.
"""


class ProgressiveValidator:
    """Multi-stage backtest validation pipeline."""

    def __init__(
        self,
        config: Optional[dict] = None,
        config_file: Optional[str] = None,
        results_file: str = "validation_results.json",
    ):
        if config_file and os.path.exists(config_file):
            with open(config_file) as f:
                loaded = json.load(f)
            self.stages = loaded.get("stages", DEFAULT_STAGES)
            self.acceptance_criteria = loaded.get(
                "acceptance_criteria",
                {"min_sharpe": 2.0, "max_drawdown": 0.40, "min_profit": 3.0},
            )
        elif config:
            self.stages = config.get("stages", DEFAULT_STAGES)
            self.acceptance_criteria = config.get("acceptance_criteria", {})
        else:
            self.stages = dict(DEFAULT_STAGES)
            self.acceptance_criteria = {
                "min_sharpe": 2.0,
                "max_drawdown": 0.40,
                "min_profit": 3.0,
            }

        self.results_file = results_file
        self.results: Dict = self._load_results()

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def _load_results(self) -> dict:
        """Load previous validation results from disk."""
        if os.path.exists(self.results_file):
            with open(self.results_file) as f:
                return json.load(f)
        return {}

    def _save_results(self):
        """Persist validation results to disk."""
        with open(self.results_file, "w") as f:
            json.dump(self.results, f, indent=2, default=str)

    # ------------------------------------------------------------------
    # Stage ordering helpers
    # ------------------------------------------------------------------

    def get_stage_order(self) -> List[str]:
        """Return stage names sorted by their configured order."""
        return sorted(
            self.stages.keys(), key=lambda s: self.stages[s].get("order", 99)
        )

    def get_next_stage(self, strategy_name: str) -> Optional[str]:
        """Determine the next stage a strategy should run."""
        history = self.results.get(strategy_name, {})
        for stage in self.get_stage_order():
            if stage not in history or history[stage].get("status") != "passed":
                return stage
        return None  # All stages passed

    # ------------------------------------------------------------------
    # Display helpers
    # ------------------------------------------------------------------

    def show_pipeline(self):
        """Print the full validation pipeline to stdout."""
        ordered = self.get_stage_order()
        print("\n=== Progressive Validation Pipeline ===\n")
        for i, stage_name in enumerate(ordered, 1):
            stage = self.stages[stage_name]
            print(f"  Stage {i}: {stage_name}")
            print(f"    Period:  {stage['start']} ~ {stage['end']}")
            print(f"    Time:    ~{stage['expected_time']}")
            print(f"    Max DD:  {stage['max_dd'] * 100:.0f}%")
            print(f"    Purpose: {stage['purpose']}")
            if i < len(ordered):
                print("         |")
                print("         v  (pass to advance)")

        ac = self.acceptance_criteria
        print(
            f"\n  Final acceptance: "
            f"Sharpe >= {ac.get('min_sharpe', 'N/A')}, "
            f"DD <= {ac.get('max_drawdown', 'N/A')}, "
            f"Profit >= {ac.get('min_profit', 'N/A')}"
        )
        print()

    def show_status(self, strategy_name: str):
        """Print the current validation status for a given strategy."""
        history = self.results.get(strategy_name, {})
        ordered = self.get_stage_order()

        print(f"\n=== Validation Status: {strategy_name} ===\n")
        for stage_name in ordered:
            result = history.get(stage_name, {})
            status = result.get("status", "pending")
            icon = {
                "passed": "[PASS]",
                "failed": "[FAIL]",
                "pending": "[----]",
            }.get(status, "[????]")

            detail = ""
            if status == "passed":
                dd = result.get("drawdown", "?")
                sh = result.get("sharpe", "?")
                detail = f" (DD: {dd}, Sharpe: {sh})"
            elif status == "failed":
                detail = f" (Reason: {result.get('reason', '?')})"

            print(f"  {icon} {stage_name}{detail}")

        next_stage = self.get_next_stage(strategy_name)
        if next_stage:
            print(f"\n  Next: {next_stage}")
        else:
            print("\n  All stages PASSED!")
        print()

    # ------------------------------------------------------------------
    # Recording
    # ------------------------------------------------------------------

    def record_result(
        self,
        strategy_name: str,
        stage_name: str,
        status: str,
        sharpe: Optional[float] = None,
        drawdown: Optional[float] = None,
        profit: Optional[float] = None,
        reason: Optional[str] = None,
    ):
        """Record the outcome of a validation stage."""
        if strategy_name not in self.results:
            self.results[strategy_name] = {}

        self.results[strategy_name][stage_name] = {
            "status": status,
            "sharpe": sharpe,
            "drawdown": drawdown,
            "profit": profit,
            "reason": reason,
            "timestamp": datetime.now().isoformat(),
        }
        self._save_results()
        print(f"Recorded: {strategy_name} / {stage_name} -> {status}")

    # ------------------------------------------------------------------
    # Command suggestion
    # ------------------------------------------------------------------

    def suggest_command(
        self,
        strategy_name: str,
        strategy_file: str,
        cli_path: str = "../backtest-poller/cli.py",
    ) -> Optional[str]:
        """Generate the backtest submission command for the next validation stage.

        Submission is handled by the backtest-poller skill. ``cli_path`` should
        point to that skill's cli.py (default assumes skills are sibling directories).
        """
        next_stage = self.get_next_stage(strategy_name)
        if not next_stage:
            return None

        stage = self.stages[next_stage]
        return (
            f"python3 {cli_path} submit "
            f"--main-file {strategy_file} "
            f"--name {strategy_name}_{next_stage}"
        )


# ======================================================================
# CLI
# ======================================================================


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="validator",
        description="Progressive Validator — multi-stage backtest validation",
    )
    parser.add_argument(
        "--config",
        default=None,
        help="Path to JSON config file (default: use built-in stages)",
    )
    parser.add_argument(
        "--results",
        default="validation_results.json",
        help="Path to results JSON file (default: validation_results.json)",
    )

    sub = parser.add_subparsers(dest="command", help="Available commands")

    # pipeline
    sub.add_parser("pipeline", help="Display the full validation pipeline")

    # status
    p_status = sub.add_parser("status", help="Show validation status for a strategy")
    p_status.add_argument("strategy_name", help="Name of the strategy")

    # next
    p_next = sub.add_parser("next", help="Show the next command to run")
    p_next.add_argument("strategy_name", help="Name of the strategy")
    p_next.add_argument("strategy_file", help="Path to the strategy source file")

    # record
    p_record = sub.add_parser("record", help="Record a stage result")
    p_record.add_argument("strategy_name", help="Name of the strategy")
    p_record.add_argument("stage", help="Stage name (e.g. smoke_test)")
    p_record.add_argument(
        "--status",
        required=True,
        choices=["passed", "failed"],
        help="Result status",
    )
    p_record.add_argument("--sharpe", type=float, default=None, help="Sharpe ratio")
    p_record.add_argument("--drawdown", type=float, default=None, help="Max drawdown (0-1)")
    p_record.add_argument("--profit", type=float, default=None, help="Profit factor")
    p_record.add_argument("--reason", default=None, help="Failure reason (if failed)")

    # skip-rules
    sub.add_parser("skip-rules", help="Display the skip rules")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    validator = ProgressiveValidator(
        config_file=args.config, results_file=args.results
    )

    if args.command == "pipeline":
        validator.show_pipeline()

    elif args.command == "status":
        validator.show_status(args.strategy_name)

    elif args.command == "next":
        cmd = validator.suggest_command(args.strategy_name, args.strategy_file)
        if cmd:
            next_stage = validator.get_next_stage(args.strategy_name)
            stage = validator.stages[next_stage]
            print(f"\nNext stage: {next_stage}")
            print(f"  Period:  {stage['start']} ~ {stage['end']}")
            print(f"  Time:    ~{stage['expected_time']}")
            print(f"  Purpose: {stage['purpose']}")
            print(f"\nSuggested command:\n  {cmd}\n")
        else:
            print(f"\n{args.strategy_name}: all stages already passed.\n")

    elif args.command == "record":
        validator.record_result(
            strategy_name=args.strategy_name,
            stage_name=args.stage,
            status=args.status,
            sharpe=args.sharpe,
            drawdown=args.drawdown,
            profit=args.profit,
            reason=args.reason,
        )

    elif args.command == "skip-rules":
        print(SKIP_RULES)


if __name__ == "__main__":
    main()
