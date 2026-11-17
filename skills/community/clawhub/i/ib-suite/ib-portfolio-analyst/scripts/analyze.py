"""/ib-analyze entrypoint: read the local lake, run all diagnostics, emit report.

Read-only and offline: it consumes snapshots/bars/executions that ib-gateway
already landed and never contacts IB. Bars/executions can be injected (tests)
or loaded from the lake in production use.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path

# make the sibling ib_analyst package importable when run as a script
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from ib_common.config import load_config
from ib_common.schema import Snapshot, DailyBar, Execution, Dividend
from ib_analyst import (account_health, concentration, pnl_attribution,
                        trade_review, portfolio_risk)
from ib_analyst import dividend_analysis, dividend_report
from ib_analyst import report


def load_latest_snapshot(root: str | Path, account_id: str | None = None) -> Snapshot:
    """Load the newest snapshot JSON under root/snapshots (optionally per account)."""
    base = Path(root) / "snapshots"
    pattern = f"{account_id}/*.json" if account_id else "*/*.json"
    files = sorted(base.glob(pattern))
    if not files:
        raise FileNotFoundError(f"no snapshots found under {base}")
    return Snapshot.model_validate_json(files[-1].read_text(encoding="utf-8"))


def run(cfg_path: str, snapshot_path: str, bars: list | None = None,
        executions: list | None = None, dividends: list | None = None,
        out_dir: str | None = None) -> dict:
    """Run every diagnostic module (incl. dividends) and assemble the report."""
    cfg = load_config(cfg_path)
    th = cfg.thresholds
    snap = Snapshot.model_validate_json(Path(snapshot_path).read_text(encoding="utf-8"))
    bar_rows = [DailyBar(**b) for b in (bars or [])]
    exec_rows = [Execution(**e) for e in (executions or [])]
    div_rows = [Dividend(**d) for d in (dividends or [])]

    findings = []
    findings += account_health.analyze(snap, th)
    findings += concentration.analyze(snap, th)
    findings += pnl_attribution.analyze(snap, th)
    if exec_rows:
        findings += trade_review.analyze(exec_rows, th)
    if bar_rows:
        findings += portfolio_risk.analyze(snap, bar_rows, th)
    if div_rows:
        findings += dividend_analysis.analyze(div_rows, snap, th)

    figures = {
        "concentration": concentration.build_chart(snap),
        "pnl_attribution": pnl_attribution.build_chart(snap),
    }
    if div_rows:
        figures["dividends"] = dividend_report.build_chart(div_rows)

    out = out_dir or "./data/runs/latest"
    return report.build_report(findings, figures, out)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run IB portfolio diagnostics (read-only).")
    parser.add_argument("--config", required=True)
    parser.add_argument("--snapshot", required=True, help="path to a snapshot JSON")
    parser.add_argument("--bars", help="optional path to daily bars JSON")
    parser.add_argument("--executions", help="optional path to executions JSON")
    parser.add_argument("--dividends", help="optional path to dividends JSON")
    parser.add_argument("--out", help="output directory for the report + charts")
    args = parser.parse_args()
    bars = json.loads(Path(args.bars).read_text()) if args.bars else None
    execs = json.loads(Path(args.executions).read_text()) if args.executions else None
    divs = json.loads(Path(args.dividends).read_text()) if args.dividends else None
    print(run(args.config, args.snapshot, bars, execs, divs, args.out))
