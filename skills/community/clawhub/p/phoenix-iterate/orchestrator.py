"""
Strategy Iteration Orchestrator
================================
AI-driven strategy iteration engine. Provides tools for the AI to:
1. Get decision context (briefing)
2. Scan code for violations
3. Record iteration results
4. Run diagnostics
5. Check system status

Configuration is loaded from a config.json file or passed as a dict.
No hardcoded strategies, blueprints, or project-specific references.

Usage:
    python orchestrator.py briefing [--code path/to/strategy.py] [--config config.json]
    python orchestrator.py status [--config config.json]
    python orchestrator.py scan --code path/to/strategy.py [--config config.json]
    python orchestrator.py diagnose --orders path/to/orders.csv [--result path/to/result.json]
    python orchestrator.py record --name MyStrategy --blueprint baseline --dimension sizing \\
        --hypothesis "..." --status completed [--sharpe 1.5] [--drawdown 0.35]
    python orchestrator.py list [--config config.json]
"""
import os
import re
import json
from datetime import datetime
from typing import Optional, Dict, Any, List


# ---------------------------------------------------------------------------
# Default configuration -- overridden by config.json or constructor args
# ---------------------------------------------------------------------------
DEFAULT_CONFIG: Dict[str, Any] = {
    "project_root": ".",
    "strategies_dir": "./strategies",
    "results_dir": "./results",
    "memory_dir": "./memory",
    "backtest_cash": 10000,
    "target_sharpe": 2.0,
    "target_max_drawdown": 0.40,
    "target_min_profit": 3.0,
    "backtest_windows": {
        "smoke_test": {
            "start": "2024-01-01",
            "end": "2024-03-31",
            "max_dd": 0.50,
            "expected_time": "15-20 min",
            "purpose": "Eliminate obvious bugs and catastrophic flaws",
        },
        "stress_test": {
            "start": "2024-02-01",
            "end": "2024-06-30",
            "max_dd": 0.45,
            "expected_time": "25-30 min",
            "purpose": "Test survival in worst market conditions",
        },
        "medium": {
            "start": "2024-01-01",
            "end": "2025-06-30",
            "max_dd": 0.42,
            "expected_time": "45-60 min",
            "purpose": "Validate across bull/bear transitions",
        },
        "full": {
            "start": "2023-01-01",
            "end": "2026-01-31",
            "max_dd": 0.40,
            "expected_time": "2-3 hours",
            "purpose": "Final acceptance benchmark",
        },
    },
    "blueprints": {},
    "mutation_dimensions": {},
    "banned_patterns": [],
}


# ---------------------------------------------------------------------------
# Lightweight constitutional memory (no external dependency)
# ---------------------------------------------------------------------------
class _ConstitutionalMemory:
    """
    Minimal, self-contained constitutional memory system.

    Stores lessons (JSON) and banned code patterns on disk.  Provides a
    code scanner and a context exporter -- just enough for the orchestrator
    to work without any external packages.
    """

    def __init__(self, memory_dir: str, initial_bans: List[str] = None):
        self.memory_dir = memory_dir
        os.makedirs(self.memory_dir, exist_ok=True)

        self.lessons_file = os.path.join(self.memory_dir, "lessons.json")
        self.bans_file = os.path.join(self.memory_dir, "bans.json")

        self.lessons: List[Dict] = []
        self.bans: List[str] = list(initial_bans or [])

        self._load()

    # -- persistence --------------------------------------------------------

    def _load(self):
        if os.path.exists(self.lessons_file):
            with open(self.lessons_file) as f:
                self.lessons = json.load(f)
        if os.path.exists(self.bans_file):
            with open(self.bans_file) as f:
                extra = json.load(f)
                self.bans = list(set(self.bans + extra))

    def _save(self):
        with open(self.lessons_file, "w") as f:
            json.dump(self.lessons, f, indent=2, ensure_ascii=False)
        with open(self.bans_file, "w") as f:
            json.dump(self.bans, f, indent=2)

    # -- mutations ----------------------------------------------------------

    def add_lesson(
        self,
        strategy_name: str,
        category: str,
        description: str,
        evidence: str = "",
        severity: str = "high",
        new_ban: str = None,
    ):
        lesson = {
            "id": len(self.lessons) + 1,
            "timestamp": datetime.now().isoformat(),
            "strategy": strategy_name,
            "category": category,
            "description": description,
            "evidence": evidence,
            "severity": severity,
        }
        self.lessons.append(lesson)
        if new_ban and new_ban not in self.bans:
            self.bans.append(new_ban)
        self._save()

    # -- code scanner -------------------------------------------------------

    def scan_code(self, code: str) -> List[Dict]:
        """
        Scan strategy source code for banned patterns.

        Performs case-insensitive matching while skipping comment lines
        and string literals.

        Returns a list of violation dicts:
            [{"pattern": "...", "line": 42, "content": "..."}]
        """
        violations: List[Dict] = []
        in_multiline_string = False

        for lineno, line in enumerate(code.split("\n"), 1):
            stripped = line.strip()

            # Track multi-line strings (triple quotes)
            triple_count = stripped.count('"""') + stripped.count("'''")
            if triple_count % 2 == 1:
                in_multiline_string = not in_multiline_string
            if in_multiline_string:
                continue

            # Skip pure comment lines
            if stripped.startswith("#"):
                continue

            code_part = self._strip_strings_and_comments(line)

            for ban in self.bans:
                if ban.lower() in code_part.lower():
                    violations.append(
                        {"pattern": ban, "line": lineno, "content": stripped}
                    )
        return violations

    @staticmethod
    def _strip_strings_and_comments(line: str) -> str:
        """Remove inline string literals and comments, keeping only code."""
        result = re.sub(r'"(?:[^"\\]|\\.)*"', '""', line)
        result = re.sub(r"'(?:[^'\\]|\\.)*'", "''", result)
        hash_idx = result.find("#")
        if hash_idx >= 0:
            result = result[:hash_idx]
        return result

    # -- context export -----------------------------------------------------

    def get_context(self, max_lessons: int = 30) -> str:
        """Return a human-readable summary suitable for an LLM system prompt."""
        lines: List[str] = []
        lines.append("=== CONSTITUTIONAL MEMORY ===")

        if not self.lessons:
            lines.append("(No lessons recorded yet.)\n")
        else:
            severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
            sorted_lessons = sorted(
                self.lessons[-max_lessons:],
                key=lambda x: severity_order.get(x.get("severity", "medium"), 2),
            )
            for lesson in sorted_lessons:
                sev = lesson.get("severity", "medium")
                tag = (
                    "CRITICAL"
                    if sev == "critical"
                    else "WARNING"
                    if sev == "high"
                    else "INFO"
                )
                lines.append(
                    f"[{tag}] [{lesson['strategy']}] {lesson['category']}: "
                    f"{lesson['description']}"
                )
                if lesson.get("evidence"):
                    lines.append(f"   Evidence: {lesson['evidence']}")

        if self.bans:
            lines.append(f"\n=== BANNED CODE PATTERNS ({len(self.bans)}) ===")
            for ban in self.bans:
                lines.append(f"  BANNED: `{ban}`")

        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main orchestrator
# ---------------------------------------------------------------------------
class StrategyOrchestrator:
    """
    Strategy iteration orchestrator.

    The AI calls this class's tool methods to execute the iteration loop:

        briefing() -> scan_strategy() -> record_iteration() -> diagnose()

    Initialise with a config dict, a path to a config.json file, or
    nothing at all (uses DEFAULT_CONFIG).
    """

    def __init__(
        self,
        config: dict = None,
        config_file: str = None,
        verbose: bool = True,
    ):
        # -- resolve config -------------------------------------------------
        if config_file and os.path.exists(config_file):
            with open(config_file) as f:
                self.config: Dict[str, Any] = {**DEFAULT_CONFIG, **json.load(f)}
        elif config:
            self.config = {**DEFAULT_CONFIG, **config}
        else:
            self.config = dict(DEFAULT_CONFIG)

        self.verbose = verbose

        # -- resolve paths --------------------------------------------------
        self.project_root = os.path.abspath(self.config["project_root"])
        self.strategies_dir = self._resolve(self.config["strategies_dir"])
        self.results_dir = self._resolve(self.config["results_dir"])
        self.memory_dir = self._resolve(self.config["memory_dir"])

        # -- constitutional memory ------------------------------------------
        self.memory = _ConstitutionalMemory(
            self.memory_dir,
            initial_bans=self.config.get("banned_patterns", []),
        )

        # -- run log --------------------------------------------------------
        self.run_log = self._load_run_log()

    # -- helpers ------------------------------------------------------------

    def _resolve(self, path: str) -> str:
        """Resolve a path relative to project_root if not absolute."""
        if os.path.isabs(path):
            return path
        return os.path.abspath(os.path.join(self.project_root, path))

    def _log(self, msg: str):
        if self.verbose:
            ts = datetime.now().strftime("%H:%M:%S")
            print(f"[{ts}] {msg}")

    def _run_log_path(self) -> str:
        return os.path.join(self.memory_dir, "run_log.json")

    def _load_run_log(self) -> List[Dict]:
        path = self._run_log_path()
        if os.path.exists(path):
            with open(path) as f:
                return json.load(f)
        return []

    def _save_run_log(self):
        os.makedirs(os.path.dirname(self._run_log_path()), exist_ok=True)
        with open(self._run_log_path(), "w") as f:
            json.dump(self.run_log, f, indent=2, default=str, ensure_ascii=False)

    @staticmethod
    def _parse_float(s: str) -> float:
        try:
            return float(str(s).replace(",", "").replace("$", "").replace("%", ""))
        except (ValueError, TypeError):
            return 0.0

    # ================================================================
    # Tool 1: Briefing (decision context)
    # ================================================================
    def briefing(self, include_code: str = None) -> str:
        """
        Prepare full decision context for the AI before starting an iteration.

        Returns a structured text block covering:
        - Constitutional memory (all recorded lessons)
        - Available strategy blueprints with historical stats
        - Mutation dimensions (what can be changed and why)
        - Recent iteration history
        - Resource constraints and progressive validation windows
        - Optionally, the source code of an existing strategy

        Args:
            include_code: Optional path to a strategy source file to include.
        """
        sections: List[str] = []

        # --- Section 1: Constitutional memory ---
        sections.append(self.memory.get_context())

        # --- Section 2: Available blueprints ---
        blueprints = self.config.get("blueprints", {})
        if blueprints:
            sections.append("\n=== AVAILABLE STRATEGY BLUEPRINTS ===")
            for bp_name, bp in blueprints.items():
                sections.append(f"\n  Blueprint: {bp_name}")
                if "description" in bp:
                    sections.append(f"    Description: {bp['description']}")
                if "key_stats" in bp:
                    stats_str = ", ".join(
                        f"{k}={v}" for k, v in bp["key_stats"].items()
                    )
                    sections.append(f"    Key stats: {stats_str}")
                # Print any extra top-level keys as parameters
                skip = {"description", "key_stats"}
                extras = {k: v for k, v in bp.items() if k not in skip}
                if extras:
                    sections.append(f"    Parameters: {json.dumps(extras)}")
        else:
            sections.append("\n=== AVAILABLE STRATEGY BLUEPRINTS ===")
            sections.append("  (No blueprints configured. Add them to config.json.)")

        # --- Section 3: Mutation dimensions ---
        dimensions = self.config.get("mutation_dimensions", {})
        if dimensions:
            sections.append("\n=== MUTATION DIMENSIONS ===")
            for dim_name, dim_info in dimensions.items():
                sections.append(f"\n  Dimension: {dim_name}")
                if "description" in dim_info:
                    sections.append(f"    Description: {dim_info['description']}")
                if "options" in dim_info:
                    sections.append(
                        f"    Options: {', '.join(dim_info['options'])}"
                    )
                if "tunable_params" in dim_info:
                    for p in dim_info["tunable_params"]:
                        sections.append(
                            f"    Parameter: {p[0]} "
                            f"(range {p[1]}~{p[2]}, step {p[3]})"
                        )
                if "lesson" in dim_info:
                    sections.append(f"    Lesson: {dim_info['lesson']}")
        else:
            sections.append("\n=== MUTATION DIMENSIONS ===")
            sections.append(
                "  (No mutation dimensions configured. Add them to config.json.)"
            )

        # --- Section 4: Iteration history ---
        if self.run_log:
            sections.append(
                f"\n=== ITERATION HISTORY ({len(self.run_log)} total) ==="
            )
            for r in self.run_log[-10:]:
                name = r.get("strategy_name", "?")
                status = r.get("status", "?")
                sharpe = r.get("sharpe", "?")
                dd = r.get("drawdown", "?")
                profit = r.get("net_profit", "?")
                sections.append(
                    f"  {name}: {status} | Sharpe={sharpe} | DD={dd} | Profit={profit}"
                )
        else:
            sections.append("\n=== ITERATION HISTORY ===")
            sections.append("  (No iterations recorded yet.)")

        # --- Section 5: Resource constraints & progressive validation ---
        sections.append("\n=== RESOURCE CONSTRAINTS ===")
        sections.append("  - Only 1 backtest can run at a time (serial execution)")
        sections.append(
            f"  - Initial capital: ${self.config['backtest_cash']:,}"
        )

        windows = self.config.get("backtest_windows", {})
        if windows:
            sections.append(
                "\n=== PROGRESSIVE VALIDATION (fail fast, promote slowly) ==="
            )
            stage_labels = {
                "smoke_test": "Stage 1",
                "stress_test": "Stage 2",
                "medium": "Stage 3",
                "full": "Stage 4",
            }
            for stage_name, window in windows.items():
                label = stage_labels.get(stage_name, stage_name)
                sections.append(
                    f"  [{label}] {stage_name}: "
                    f"{window['start']} ~ {window['end']} "
                    f"({window.get('expected_time', '?')}) "
                    f"DD threshold <= {window['max_dd']:.0%}"
                )
                if "purpose" in window:
                    sections.append(f"     Purpose: {window['purpose']}")
            ordered = list(windows.keys())
            sections.append(f"  Pipeline: {' -> '.join(ordered)}")
            sections.append(
                "  Rule: only promote to next stage after passing current stage"
            )

        # --- Section 6: Target constraints ---
        sections.append("\n=== TARGET CONSTRAINTS (acceptance criteria) ===")
        sections.append(f"  Sharpe >= {self.config['target_sharpe']}")
        sections.append(
            f"  Max drawdown <= {self.config['target_max_drawdown']:.0%}"
        )
        sections.append(
            f"  Min net profit >= {self.config['target_min_profit']:.0%}"
        )

        # --- Section 7: Current code (optional) ---
        if include_code and os.path.exists(include_code):
            with open(include_code) as f:
                code = f.read()
            sections.append(f"\n=== CURRENT CODE ({include_code}) ===")
            sections.append(code[:5000])  # cap length for LLM context

        return "\n".join(sections)

    # ================================================================
    # Tool 2: Code violation scan
    # ================================================================
    def scan_strategy(self, code: str) -> Dict:
        """
        Scan strategy source code against constitutional memory bans.

        If no memory system is available (no banned patterns), returns clean.

        Returns:
            {"clean": True/False, "violations": [...]}
        """
        violations = self.memory.scan_code(code)
        if violations:
            self._log(
                f"VIOLATION: Code has {len(violations)} banned pattern(s):"
            )
            for v in violations:
                self._log(
                    f"  Line {v['line']}: `{v['content']}` "
                    f"(matches banned pattern: {v['pattern']})"
                )
        else:
            self._log("CLEAN: Code passed constitutional scan.")
        return {"clean": len(violations) == 0, "violations": violations}

    # ================================================================
    # Tool 3: Record iteration result
    # ================================================================
    def record_iteration(
        self,
        strategy_name: str,
        blueprint_used: str,
        mutation_dimension: str,
        hypothesis: str,
        backtest_window: str = "smoke_test",
        backtest_id: str = None,
        status: str = "submitted",
        sharpe: float = None,
        drawdown: float = None,
        net_profit: float = None,
        diagnosis_summary: str = None,
        notes: str = None,
    ) -> Dict:
        """
        Record the result of a single iteration.

        The AI calls this after a backtest completes to persist the
        outcome into the run log and, where appropriate, add lessons
        to constitutional memory.
        """
        windows = self.config.get("backtest_windows", {})
        window_info = windows.get(backtest_window, {})

        record: Dict[str, Any] = {
            "timestamp": datetime.now().isoformat(),
            "strategy_name": strategy_name,
            "blueprint_used": blueprint_used,
            "mutation_dimension": mutation_dimension,
            "hypothesis": hypothesis,
            "backtest_window": backtest_window,
            "backtest_period": (
                f"{window_info.get('start', '?')} ~ {window_info.get('end', '?')}"
            ),
            "backtest_id": backtest_id,
            "status": status,
            "sharpe": sharpe,
            "drawdown": drawdown,
            "net_profit": net_profit,
            "diagnosis_summary": diagnosis_summary,
            "notes": notes,
        }

        self.run_log.append(record)
        self._save_run_log()
        self._log(f"RECORDED: {strategy_name} -> {status}")

        # Auto-add lessons for notable outcomes
        target_sharpe = self.config.get("target_sharpe", 2.0)

        if status == "early_stop" and drawdown is not None:
            self.memory.add_lesson(
                strategy_name,
                "drawdown",
                f"Drawdown {drawdown:.1%} triggered early stop.",
                evidence=(
                    f"DD: {drawdown:.1%}, Blueprint: {blueprint_used}, "
                    f"Mutation: {mutation_dimension}"
                ),
                severity="high" if drawdown < 0.60 else "critical",
            )

        if status == "completed" and sharpe is not None and sharpe >= target_sharpe:
            dd_str = f"{drawdown:.1%}" if drawdown is not None else "N/A"
            np_str = f"{net_profit:.0%}" if net_profit is not None else "N/A"
            self.memory.add_lesson(
                strategy_name,
                "success",
                f"Target met! Sharpe={sharpe:.2f}, DD={dd_str}, Profit={np_str}",
                evidence=(
                    f"Blueprint: {blueprint_used}, "
                    f"Mutation: {mutation_dimension}"
                ),
                severity="low",
            )

        return record

    # ================================================================
    # Tool 4: Diagnose backtest results
    # ================================================================
    def diagnose(self, orders_csv: str, result_json: str = None) -> str:
        """
        Run forensic diagnosis on backtest output files.

        Tries to import pandas for rich analysis.  If pandas is not
        available, falls back to a basic line-count summary.

        Args:
            orders_csv:  Path to the orders CSV file.
            result_json: Optional path to the result JSON file.

        Returns:
            A human-readable diagnosis report string.
        """
        if not os.path.exists(orders_csv):
            return f"ERROR: Orders file not found: {orders_csv}"

        report_lines: List[str] = []
        report_lines.append("=== BACKTEST DIAGNOSIS ===")
        report_lines.append(f"Orders file: {orders_csv}")
        if result_json:
            report_lines.append(f"Result file: {result_json}")

        # -- Result JSON summary -------------------------------------------
        stats: Dict[str, Any] = {}
        if result_json and os.path.exists(result_json):
            with open(result_json) as f:
                data = json.load(f)
            result_obj = data.get("backtest", data)
            stats = result_obj.get("statistics", result_obj.get("Statistics", {}))
            if stats:
                report_lines.append("\n--- Summary Statistics ---")
                for k, v in stats.items():
                    report_lines.append(f"  {k}: {v}")

        # -- Orders analysis (requires pandas) -----------------------------
        try:
            import pandas as pd

            df = pd.read_csv(orders_csv)
            report_lines.append(f"\n--- Order Analysis ---")
            report_lines.append(f"Total rows: {len(df)}")

            if "status" in df.columns:
                filled = df[df["status"] == "Filled"]
                report_lines.append(
                    f"Filled orders: {len(filled)} / {len(df)}"
                )
            else:
                filled = df

            if "fillPrice" in df.columns:
                df["fillPrice"] = pd.to_numeric(df["fillPrice"], errors="coerce")
            if "quantity" in df.columns:
                df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")

            # Underlying extraction
            if "symbol" in df.columns:
                df["underlying"] = df["symbol"].apply(
                    lambda s: str(s).split()[0].strip()
                )
                unique_symbols = df["underlying"].nunique()
                report_lines.append(f"Unique underlyings traded: {unique_symbols}")

                # Per-underlying summary
                report_lines.append("\n--- Per-Underlying Breakdown ---")
                for sym, grp in df.groupby("underlying"):
                    buys = grp[grp.get("direction", grp.get("quantity", 0)) > 0] if "direction" in grp.columns else grp[grp["quantity"] > 0] if "quantity" in grp.columns else grp
                    report_lines.append(
                        f"  {sym}: {len(grp)} orders"
                    )

            # Time range
            time_col = None
            for candidate in ("time", "Time", "timestamp", "Timestamp", "date"):
                if candidate in df.columns:
                    time_col = candidate
                    break
            if time_col:
                report_lines.append(
                    f"\nTime range: {df[time_col].iloc[0]} .. {df[time_col].iloc[-1]}"
                )

        except ImportError:
            # Fallback: basic line count without pandas
            with open(orders_csv) as f:
                lines = f.readlines()
            report_lines.append(f"\nTotal CSV lines (including header): {len(lines)}")
            report_lines.append(
                "(Install pandas for richer diagnosis: pip install pandas)"
            )

        self._log(f"DIAGNOSIS COMPLETE: {orders_csv}")
        return "\n".join(report_lines)

    # ================================================================
    # Tool 5: Status digest
    # ================================================================
    def status_digest(self) -> str:
        """
        Return a concise status summary of the iteration system.

        Covers lesson count, ban count, iteration history, and
        any active backtest state file if present.
        """
        lines: List[str] = []
        lines.append("=== Strategy Orchestrator Status ===")
        lines.append(f"Constitutional lessons: {len(self.memory.lessons)}")
        lines.append(f"Banned patterns:       {len(self.memory.bans)}")
        lines.append(f"Total iterations:      {len(self.run_log)}")

        if self.run_log:
            lines.append("\nRecent iterations:")
            for r in self.run_log[-5:]:
                name = r.get("strategy_name", "?")
                status = r.get("status", "?")
                mut = r.get("mutation_dimension", "?")
                window = r.get("backtest_window", "?")
                lines.append(f"  {name} | {status} | dim={mut} | window={window}")

        # Check for a state.json file (from a backtest poller, if any)
        state_file = os.path.join(self.project_root, "state.json")
        if os.path.exists(state_file):
            with open(state_file) as f:
                state = json.load(f)
            backtests = state.get("backtests", [])
            active = [
                b for b in backtests if b.get("status") in ("pending", "running")
            ]
            completed = [b for b in backtests if b.get("status") == "completed"]
            stopped = [b for b in backtests if b.get("status") == "early_stop"]
            lines.append(
                f"\nPoller: {'running' if state.get('poller_running') else 'not running'}"
            )
            lines.append(f"Active backtests:    {len(active)}")
            lines.append(f"Completed backtests: {len(completed)}")
            lines.append(f"Early-stopped:       {len(stopped)}")

        return "\n".join(lines)

    # ================================================================
    # Tool 6: List available base strategies
    # ================================================================
    def list_base_strategies(self) -> List[Dict]:
        """
        List all strategy directories under the configured strategies_dir.

        Looks for directories containing a main.py (or any .py file).
        """
        strategies: List[Dict] = []
        if not os.path.isdir(self.strategies_dir):
            return strategies

        for name in sorted(os.listdir(self.strategies_dir)):
            dir_path = os.path.join(self.strategies_dir, name)
            if not os.path.isdir(dir_path):
                continue

            # Prefer main.py; fall back to first .py file found
            main_py = os.path.join(dir_path, "main.py")
            if os.path.exists(main_py):
                entry = main_py
            else:
                py_files = [
                    f for f in os.listdir(dir_path) if f.endswith(".py")
                ]
                if not py_files:
                    continue
                entry = os.path.join(dir_path, py_files[0])

            strategies.append(
                {
                    "name": name,
                    "path": entry,
                    "size_bytes": os.path.getsize(entry),
                }
            )
        return strategies


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------
def main():
    import argparse

    # Parent parser with the shared --config option so it works on every
    # subcommand (e.g.  ``orchestrator.py briefing --config config.json``).
    parent = argparse.ArgumentParser(add_help=False)
    parent.add_argument(
        "--config",
        type=str,
        default=None,
        help="Path to config.json (optional, uses defaults if omitted)",
    )

    parser = argparse.ArgumentParser(
        description="Strategy Iteration Orchestrator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        parents=[parent],
        epilog="""
Examples:
  # Get full decision context before starting an iteration
  python orchestrator.py briefing --config config.json

  # Get system status
  python orchestrator.py status --config config.json

  # Scan strategy code for banned patterns
  python orchestrator.py scan --code strategies/my_strategy/main.py

  # Diagnose backtest results
  python orchestrator.py diagnose --orders results/smoke/orders.csv --result results/smoke/result.json

  # Record an iteration result
  python orchestrator.py record --name MyStrat_v2 --blueprint baseline --dimension position_sizing \\
    --hypothesis "Reduce max trade to 2%" --status completed --sharpe 1.5 --drawdown 0.35

  # List available base strategies
  python orchestrator.py list --config config.json
        """,
    )

    subparsers = parser.add_subparsers(dest="command")

    # -- briefing -----------------------------------------------------------
    bp = subparsers.add_parser(
        "briefing", help="Get full decision context", parents=[parent]
    )
    bp.add_argument("--code", type=str, help="Path to strategy source to include")

    # -- status -------------------------------------------------------------
    subparsers.add_parser("status", help="Show system status digest", parents=[parent])

    # -- scan ---------------------------------------------------------------
    sp = subparsers.add_parser(
        "scan", help="Scan code for banned patterns", parents=[parent]
    )
    sp.add_argument("--code", type=str, required=True, help="Path to strategy source")

    # -- diagnose -----------------------------------------------------------
    dp = subparsers.add_parser(
        "diagnose", help="Diagnose backtest results", parents=[parent]
    )
    dp.add_argument("--orders", type=str, required=True, help="Path to orders CSV")
    dp.add_argument("--result", type=str, help="Path to result JSON (optional)")

    # -- record -------------------------------------------------------------
    rp = subparsers.add_parser(
        "record", help="Record an iteration result", parents=[parent]
    )
    rp.add_argument("--name", required=True, help="Strategy name")
    rp.add_argument("--blueprint", required=True, help="Blueprint used")
    rp.add_argument("--dimension", required=True, help="Mutation dimension")
    rp.add_argument("--hypothesis", required=True, help="Hypothesis description")
    rp.add_argument(
        "--window",
        default="smoke_test",
        help="Backtest window name (default: smoke_test)",
    )
    rp.add_argument("--backtest-id", help="Backtest ID")
    rp.add_argument("--status", default="submitted", help="Outcome status")
    rp.add_argument("--sharpe", type=float, help="Sharpe ratio")
    rp.add_argument("--drawdown", type=float, help="Max drawdown (0.0 - 1.0)")
    rp.add_argument("--net-profit", type=float, help="Net profit ratio")
    rp.add_argument("--notes", help="Free-text notes")

    # -- list ---------------------------------------------------------------
    subparsers.add_parser(
        "list", help="List available base strategies", parents=[parent]
    )

    args = parser.parse_args()

    # Build orchestrator
    orch = StrategyOrchestrator(config_file=args.config)

    if args.command == "briefing":
        code_path = None
        if hasattr(args, "code") and args.code:
            code_path = (
                os.path.abspath(args.code)
                if not os.path.isabs(args.code)
                else args.code
            )
        print(orch.briefing(include_code=code_path))

    elif args.command == "status":
        print(orch.status_digest())

    elif args.command == "scan":
        code_path = (
            os.path.abspath(args.code)
            if not os.path.isabs(args.code)
            else args.code
        )
        with open(code_path) as f:
            code = f.read()
        result = orch.scan_strategy(code)
        if result["clean"]:
            print("CLEAN: No violations found.")
        else:
            print(f"VIOLATIONS: {len(result['violations'])} banned pattern(s) found.")
            for v in result["violations"]:
                print(f"  Line {v['line']}: {v['content']}  (pattern: {v['pattern']})")

    elif args.command == "diagnose":
        orders = (
            os.path.abspath(args.orders)
            if not os.path.isabs(args.orders)
            else args.orders
        )
        result_path = None
        if args.result:
            result_path = (
                os.path.abspath(args.result)
                if not os.path.isabs(args.result)
                else args.result
            )
        print(orch.diagnose(orders, result_path))

    elif args.command == "record":
        record = orch.record_iteration(
            strategy_name=args.name,
            blueprint_used=args.blueprint,
            mutation_dimension=args.dimension,
            hypothesis=args.hypothesis,
            backtest_window=args.window,
            backtest_id=args.backtest_id,
            status=args.status,
            sharpe=args.sharpe,
            drawdown=args.drawdown,
            net_profit=args.net_profit,
            notes=args.notes,
        )
        print(json.dumps(record, indent=2, default=str))

    elif args.command == "list":
        strategies = orch.list_base_strategies()
        if strategies:
            print(f"Available strategies ({len(strategies)}):")
            for s in strategies:
                print(f"  {s['name']:40s} {s['size_bytes']:>8,} bytes  {s['path']}")
        else:
            print(
                f"No strategies found in {orch.strategies_dir}. "
                "Create a subdirectory with a main.py file."
            )

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
