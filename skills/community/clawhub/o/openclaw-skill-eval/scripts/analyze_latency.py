#!/usr/bin/env python3
"""
Latency Analyzer (v2 — pure data processing, no OpenClaw API calls)

Takes pre-saved timing files and computes p50/p90/std_dev stats.
Mo runs the spawning and records timings; this script only analyzes data.

Usage:
    python3 scripts/analyze_latency.py \
        --evals evals/weather/quality.json \
        --timings-dir workspace/weather/iter-1/raw/timings/ \
        --models haiku,sonnet \
        --output-dir workspace/weather/iter-1/latency/

Timing file format:
    raw/timings/eval-{id}-{model}-run-{n}.json
    {"eval_id": 1, "model": "sonnet", "run": 1, "elapsed_seconds": 12.3}
"""

import argparse
import json
import statistics
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, asdict


@dataclass
class EvalLatency:
    eval_id: int
    eval_name: str
    model: str
    n_runs: int
    timings: list
    p50: float
    p90: float
    mean: float
    min_time: float
    max_time: float
    std_dev: float
    stable: bool
    stability_level: str


def load_timings(timings_dir: Path, eval_id: int, model: str) -> list[float]:
    """Load all run timings for a (eval, model) pair."""
    timings = []
    pattern = f"eval-{eval_id}-{model}-run-*.json"
    for f in sorted(timings_dir.glob(pattern)):
        data = json.loads(f.read_text())
        elapsed = data.get("elapsed_seconds")
        if elapsed is not None:
            timings.append(float(elapsed))
    return timings


def compute_latency(eval_id: int, name: str, model: str, timings: list) -> EvalLatency:
    n = len(timings)
    if n == 0:
        return EvalLatency(eval_id, name, model, 0, [], 0, 0, 0, 0, 0, 0, True, "N/A")

    sorted_t = sorted(timings)
    std = statistics.stdev(timings) if n >= 2 else 0

    stability = "HIGH" if std < 1.0 else "MEDIUM" if std < 3.0 else "LOW"

    return EvalLatency(
        eval_id=eval_id,
        eval_name=name,
        model=model,
        n_runs=n,
        timings=[round(t, 2) for t in timings],
        p50=round(sorted_t[n // 2], 2),
        p90=round(sorted_t[int(n * 0.9)] if n >= 10 else sorted_t[-1], 2),
        mean=round(statistics.mean(timings), 2),
        min_time=round(min(timings), 2),
        max_time=round(max(timings), 2),
        std_dev=round(std, 2),
        stable=std < 3.0,
        stability_level=stability,
    )


def generate_report(results: list[EvalLatency], models: list[str], skill_name: str) -> str:
    lines = [
        f"# Latency Profile: {skill_name}",
        f"Generated: {datetime.now().isoformat()}",
        f"Models: {', '.join(models)}",
        ""
    ]

    if len(models) == 1:
        lines += [
            "| Eval | p50 | p90 | std_dev | Stability |",
            "|------|-----|-----|---------|-----------|"
        ]
        for r in results:
            icon = "✅" if r.stability_level == "HIGH" else "⚠️" if r.stability_level == "MEDIUM" else "🔴"
            lines.append(f"| {r.eval_name} | {r.p50}s | {r.p90}s | {r.std_dev}s | {icon} {r.stability_level} |")
    else:
        lines += [
            "| Eval | " + " | ".join([f"{m} p50" for m in models]) + " |",
            "|------|" + "|".join(["------"] * len(models)) + "|"
        ]
        eval_ids = sorted(set(r.eval_id for r in results))
        for eid in eval_ids:
            row = []
            name = ""
            for model in models:
                r = next((x for x in results if x.eval_id == eid and x.model == model), None)
                if r:
                    name = r.eval_name
                    icon = "✅" if r.stable else "⚠️"
                    row.append(f"{r.p50}s {icon}")
                else:
                    row.append("-")
            lines.append(f"| {name} | " + " | ".join(row) + " |")

    lines.append("")

    unstable = [r for r in results if not r.stable]
    if unstable:
        lines += ["## Unstable Evals", ""]
        for r in unstable:
            lines.append(f"- {r.eval_name} ({r.model}): std_dev={r.std_dev}s — consider retry logic")
        lines.append("")

    return "\n".join(lines)


def analyze_latency(
    evals_file: str,
    timings_dir: str,
    models: list[str],
    output_dir: str,
) -> dict:
    with open(evals_file, encoding="utf-8") as f:
        evals_data = json.load(f)

    skill_name = evals_data.get("skill_name", "unknown")
    evals = evals_data.get("evals", [])
    t_dir = Path(timings_dir)
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    all_results = []

    for eval_item in evals:
        eval_id = eval_item.get("id")
        name = eval_item.get("name", f"eval-{eval_id}")

        for model in models:
            timings = load_timings(t_dir, eval_id, model)
            if not timings:
                print(f"  ⚠️  No timing data for eval-{eval_id} model={model}")
                continue

            result = compute_latency(eval_id, name, model, timings)
            all_results.append(result)

            icon = "✅" if result.stable else "⚠️"
            print(f"  [{eval_id}] {model}: p50={result.p50}s p90={result.p90}s "
                  f"std={result.std_dev}s {icon}")

    if not all_results:
        print("❌ No results")
        return {}

    # Summaries per model
    summaries = {}
    for model in models:
        mr = [r for r in all_results if r.model == model]
        if mr:
            summaries[model] = {
                "avg_p50": round(statistics.mean(r.p50 for r in mr), 2),
                "avg_p90": round(statistics.mean(r.p90 for r in mr), 2),
                "stability": (
                    "HIGH" if all(r.stability_level == "HIGH" for r in mr)
                    else "LOW" if any(r.stability_level == "LOW" for r in mr)
                    else "MEDIUM"
                ),
                "unstable_evals": [r.eval_name for r in mr if not r.stable],
            }

    output = {
        "skill_name": skill_name,
        "timestamp": datetime.now().isoformat(),
        "models": models,
        "results": [asdict(r) for r in all_results],
        "summary": summaries,
    }

    json_file = out_dir / "latency_report.json"
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    report = generate_report(all_results, models, skill_name)
    md_file = out_dir / "latency_report.md"
    md_file.write_text(report, encoding="utf-8")

    print()
    print("=== Summary ===")
    for model, s in summaries.items():
        print(f"  {model}: avg_p50={s['avg_p50']}s stability={s['stability']}")
    print(f"✅ Saved to {output_dir}")

    return output


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--evals", required=True)
    parser.add_argument("--timings-dir", required=True)
    parser.add_argument("--models", default="sonnet")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show detailed output per eval (default: summary only)"
    )
    args = parser.parse_args()

    analyze_latency(
        evals_file=args.evals,
        timings_dir=args.timings_dir,
        models=[m.strip() for m in args.models.split(",")],
        output_dir=args.output_dir,
    )


if __name__ == "__main__":
    main()
