#!/usr/bin/env python3
"""Print module telemetry and dataflow break-candidate report."""

import argparse
import os

from mg_events.telemetry import build_report


def main(argv=None):
    parser = argparse.ArgumentParser(description="memory-guardian dataflow report")
    parser.add_argument("--workspace", required=True, help="Workspace path")
    args = parser.parse_args(argv)

    report = build_report(args.workspace)
    print("MEMORY GUARDIAN — Dataflow Report")
    print(f"Generated: {report['generated_at']}")

    modules = report["modules"]
    if not modules:
        print("No telemetry recorded yet.")
        return 0

    for name in sorted(modules):
        stats = modules[name]
        flag = " BREAK" if stats.get("pipeline_break_candidate") else ""
        print(
            f"{name}: hits={stats['hits']} misses={stats['misses']} "
            f"input={stats['input_total']} output={stats['output_total']}{flag}"
        )

    if report["break_candidates"]:
        print("Pipeline break candidates: " + ", ".join(report["break_candidates"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
