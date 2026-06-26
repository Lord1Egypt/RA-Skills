#!/usr/bin/env python3
"""
Latency Profiling — Phase 3.5

Analyze skill execution speed: p50/p90, stability, step-level bottlenecks.

Usage:
    # Basic: total latency distribution (default 5 runs)
    python scripts/run_latency_profile.py \
        --evals evals/example-quality.json \
        --skill-path ./SKILL.md \
        --n-runs 5 \
        --output-dir workspace/latency-1

    # Deep: step-level analysis
    python scripts/run_latency_profile.py \
        --evals evals/example-quality.json \
        --skill-path ./SKILL.md \
        --n-runs 5 \
        --step-level \
        --output-dir workspace/latency-1

    # Multi-model speed comparison (pairs with Phase 3.4)
    python scripts/run_latency_profile.py \
        --evals evals/example-quality.json \
        --skill-path ./SKILL.md \
        --models haiku,sonnet \
        --n-runs 5 \
        --output-dir workspace/latency-1

Architecture: ARCHITECTURE.md
Design: PHASE-3-5-DESIGN.md
"""

import argparse
import json
import re
import statistics
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional

from oc_tools import invoke


# === Model Aliases ===

MODEL_ALIASES = {
    "haiku": "anthropic/claude-haiku-4-5",
    "sonnet": "anthropic/claude-sonnet-4-6",
    "opus": "anthropic/claude-opus-4-5",
}

def resolve_model(alias: str) -> str:
    return MODEL_ALIASES.get(alias, alias)


# === Data Classes ===

@dataclass
class StepTiming:
    step_name: str
    mean_seconds: float
    pct_of_total: float
    is_bottleneck: bool  # pct > 40%


@dataclass
class EvalLatency:
    eval_id: int
    eval_name: str
    model: str
    n_runs: int
    timings_seconds: list
    p50: float
    p90: float
    mean: float
    min_time: float
    max_time: float
    std_dev: float
    stable: bool        # std_dev < 3s
    stability_level: str  # HIGH / MEDIUM / LOW
    steps: Optional[list]  # step-level breakdown if available


# === Core Functions ===

def spawn_single_run(
    eval_item: dict,
    skill_path: str,
    model: str
) -> tuple[str, float]:
    """
    Spawn a single eval run. Returns (transcript, elapsed_seconds).
    """
    prompt = eval_item.get("prompt", "")
    task = f"Read {skill_path} for guidance.\n\n{prompt}"
    full_model = resolve_model(model)

    start = time.time()
    result = invoke("sessions_spawn", {
        "task": task,
        "model": full_model,
        "sandbox": "inherit",
        "cleanup": "keep",
        "mode": "run",
        "runTimeoutSeconds": 120
    })
    elapsed = time.time() - start

    transcript = ""
    if isinstance(result, dict):
        transcript = result.get("output", "") or result.get("result", "") or str(result)
    else:
        transcript = str(result)

    return transcript, elapsed


def parse_step_timings(transcripts: list[str]) -> Optional[list[StepTiming]]:
    """
    Attempt to extract step-level timings from transcripts.

    Looks for patterns like:
    - Tool call names (from sessions_history tool_use blocks)
    - Timestamps in transcript if available

    Returns None if transcript format doesn't support step-level parsing.
    """
    # Collect tool names across all transcripts
    tool_pattern = re.compile(r'\[Tool(?:\s+call)?:\s*([^\]]+)\]', re.IGNORECASE)
    tool_occurrences = {}

    for transcript in transcripts:
        tools_found = tool_pattern.findall(transcript)
        for tool in tools_found:
            tool_clean = tool.strip().split("(")[0].strip()
            tool_occurrences[tool_clean] = tool_occurrences.get(tool_clean, 0) + 1

    if not tool_occurrences:
        return None

    # Can't compute per-step timing without timestamps in transcript
    # Return qualitative step frequency instead
    total_mentions = sum(tool_occurrences.values())
    steps = []
    for tool, count in sorted(tool_occurrences.items(), key=lambda x: -x[1]):
        pct = count / total_mentions
        steps.append(StepTiming(
            step_name=tool,
            mean_seconds=0,       # not available without timestamps
            pct_of_total=round(pct, 2),
            is_bottleneck=pct > 0.4
        ))
    return steps


def run_latency_for_eval(
    eval_item: dict,
    skill_path: str,
    model: str,
    n_runs: int,
    step_level: bool,
    sequential: bool
) -> EvalLatency:
    """
    Run n_runs evaluations for a single eval + model, collect timings.
    """
    eval_id = eval_item.get("id", 0)
    eval_name = eval_item.get("name", f"eval-{eval_id}")

    timings = []
    transcripts = []

    if sequential:
        # Serial runs for more accurate measurements (no interference)
        for i in range(n_runs):
            print(f"    Run {i+1}/{n_runs} (sequential)...")
            transcript, elapsed = spawn_single_run(eval_item, skill_path, model)
            timings.append(elapsed)
            transcripts.append(transcript)
    else:
        # Parallel runs (faster but may have interference)
        with ThreadPoolExecutor(max_workers=min(n_runs, 4)) as executor:
            futures = [
                executor.submit(spawn_single_run, eval_item, skill_path, model)
                for _ in range(n_runs)
            ]
            for future in as_completed(futures):
                transcript, elapsed = future.result()
                timings.append(elapsed)
                transcripts.append(transcript)

    # Compute statistics
    sorted_timings = sorted(timings)
    n = len(sorted_timings)
    std = statistics.stdev(timings) if n >= 2 else 0

    if std < 1.0:
        stability_level = "HIGH"
    elif std < 3.0:
        stability_level = "MEDIUM"
    else:
        stability_level = "LOW"

    # Step-level analysis
    steps = None
    if step_level:
        steps = parse_step_timings(transcripts)

    return EvalLatency(
        eval_id=eval_id,
        eval_name=eval_name,
        model=model,
        n_runs=n_runs,
        timings_seconds=[round(t, 2) for t in timings],
        p50=round(sorted_timings[n // 2], 2),
        p90=round(sorted_timings[int(n * 0.9)] if n >= 10 else sorted_timings[-1], 2),
        mean=round(statistics.mean(timings), 2),
        min_time=round(min(timings), 2),
        max_time=round(max(timings), 2),
        std_dev=round(std, 2),
        stable=std < 3.0,
        stability_level=stability_level,
        steps=steps,
    )


# === Report Generation ===

def generate_markdown_report(
    results: list[EvalLatency],
    models: list[str],
    n_runs: int,
    skill_name: str,
    step_level: bool
) -> str:
    lines = [
        f"# Latency Profile: {skill_name}",
        "",
        f"Generated: {datetime.now().isoformat()}",
        f"Models: {', '.join(models)} | Runs per eval: {n_runs}",
        "",
        "---",
        "",
        "## Summary",
        "",
    ]

    # Summary table
    if len(models) == 1:
        model = models[0]
        lines.extend([
            "| Eval | p50 | p90 | std_dev | Stability |",
            "|------|-----|-----|---------|-----------|",
        ])
        model_results = [r for r in results if r.model == model]
        for r in model_results:
            stable_icon = "✅" if r.stability_level == "HIGH" else ("⚠️" if r.stability_level == "MEDIUM" else "🔴")
            lines.append(
                f"| {r.eval_name} | {r.p50}s | {r.p90}s | {r.std_dev}s | {stable_icon} {r.stability_level} |"
            )
    else:
        # Multi-model: p50 per model
        header = "| Eval | " + " | ".join([f"{m} p50" for m in models]) + " |"
        sep = "|------|" + "|".join(["------"] * len(models)) + "|"
        lines.extend([header, sep])

        eval_ids = sorted(set(r.eval_id for r in results))
        for eval_id in eval_ids:
            row = []
            eval_name = ""
            for model in models:
                r = next((x for x in results if x.eval_id == eval_id and x.model == model), None)
                if r:
                    eval_name = r.eval_name
                    stable_icon = "✅" if r.stable else "⚠️"
                    row.append(f"{r.p50}s {stable_icon}")
                else:
                    row.append("-")
            lines.append(f"| {eval_name} | " + " | ".join(row) + " |")

    lines.append("")

    # Bottleneck analysis
    unstable = [r for r in results if not r.stable]
    if unstable:
        lines.extend([
            "## Bottleneck Analysis",
            "",
        ])
        for r in unstable:
            lines.extend([
                f"### {r.eval_name} ({r.model}) — {r.stability_level} VARIANCE ⚠️",
                "",
                f"p50: {r.p50}s | p90: {r.p90}s | std_dev: {r.std_dev}s",
                "",
                "Recommendation: High variance suggests network/tool non-determinism.",
                "Consider: Add retry logic or timeout in SKILL.md.",
                "",
            ])

    # Step-level if available
    step_results = [r for r in results if r.steps]
    if step_results:
        lines.extend([
            "## Step-Level Analysis",
            "",
            "> Note: Based on tool call frequency, not wall-clock time per step.",
            "",
        ])
        for r in step_results:
            lines.extend([
                f"### {r.eval_name} ({r.model})",
                "",
                "| Step | Frequency | Bottleneck? |",
                "|------|-----------|-------------|",
            ])
            for step in r.steps:
                bottleneck = "⚠️ YES" if step.is_bottleneck else "no"
                lines.append(f"| {step.step_name} | {step.pct_of_total:.0%} | {bottleneck} |")
            lines.append("")

    # Multi-model speedup comparison
    if len(models) >= 2:
        model_order = ["haiku", "sonnet", "opus"]
        sorted_models = sorted(models, key=lambda m: model_order.index(m) if m in model_order else 99)
        baseline = sorted_models[-1]  # slowest (largest model) as baseline
        fast = sorted_models[0]

        baseline_p50s = [r.p50 for r in results if r.model == baseline]
        fast_p50s = [r.p50 for r in results if r.model == fast]

        if baseline_p50s and fast_p50s:
            avg_baseline = statistics.mean(baseline_p50s)
            avg_fast = statistics.mean(fast_p50s)
            speedup = (avg_baseline - avg_fast) / avg_baseline * 100 if avg_baseline > 0 else 0

            lines.extend([
                "## Model Speed Comparison",
                "",
                f"{fast} vs {baseline}: **{speedup:+.0f}%** speed difference",
                f"  {fast} avg p50: {avg_fast:.1f}s",
                f"  {baseline} avg p50: {avg_baseline:.1f}s",
                "",
            ])

    return "\n".join(lines)


# === Main ===

def run_latency_profile(
    evals_file: str,
    skill_path: str,
    models: list[str],
    n_runs: int,
    step_level: bool,
    sequential: bool,
    output_dir: str,
    workers: int
) -> dict:
    """Main entry point for latency profiling."""

    with open(evals_file, encoding="utf-8") as f:
        evals_data = json.load(f)
    skill_name = evals_data.get("skill_name", Path(skill_path).stem)
    evals = evals_data.get("evals", [])

    print(f"Latency profiling: {skill_name}")
    print(f"  Models: {', '.join(models)}")
    print(f"  Evals: {len(evals)}")
    print(f"  Runs per eval: {n_runs}")
    print(f"  Step-level: {step_level}")
    print(f"  Sequential: {sequential}")
    if sequential:
        print(f"  ⚠️  Sequential mode: more accurate but slower")
    print()

    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    all_results: list[EvalLatency] = []

    # Run evaluations
    tasks = [(eval_item, model) for model in models for eval_item in evals]
    total = len(tasks)
    completed = 0

    # Use outer parallelism for (model, eval) pairs
    # Inner parallelism for n_runs within each pair (unless sequential)
    outer_workers = 1 if sequential else min(workers, len(tasks))

    with ThreadPoolExecutor(max_workers=outer_workers) as executor:
        futures = {}
        for eval_item, model in tasks:
            future = executor.submit(
                run_latency_for_eval,
                eval_item, skill_path, model, n_runs, step_level, sequential
            )
            futures[future] = (eval_item["id"], model)

        for future in as_completed(futures):
            eval_id, model = futures[future]
            completed += 1
            try:
                result = future.result()
                all_results.append(result)
                stable_icon = "✅" if result.stable else "⚠️"
                print(
                    f"  [{completed}/{total}] {model} eval-{eval_id}: "
                    f"p50={result.p50}s, p90={result.p90}s, "
                    f"std={result.std_dev}s {stable_icon}"
                )
            except Exception as e:
                print(f"  [{completed}/{total}] {model} eval-{eval_id}: ERROR - {e}")

    print()

    # Build output
    output = {
        "skill_name": skill_name,
        "models": models,
        "n_runs": n_runs,
        "step_level": step_level,
        "sequential": sequential,
        "timestamp": datetime.now().isoformat(),
        "evals": [asdict(r) for r in all_results],
        "summary": {},
    }

    # Compute per-model summaries
    for model in models:
        model_results = [r for r in all_results if r.model == model]
        if model_results:
            output["summary"][model] = {
                "avg_p50": round(statistics.mean(r.p50 for r in model_results), 2),
                "avg_p90": round(statistics.mean(r.p90 for r in model_results), 2),
                "avg_std_dev": round(statistics.mean(r.std_dev for r in model_results), 2),
                "stability": (
                    "HIGH" if all(r.stability_level == "HIGH" for r in model_results)
                    else "LOW" if any(r.stability_level == "LOW" for r in model_results)
                    else "MEDIUM"
                ),
                "unstable_evals": [r.eval_name for r in model_results if not r.stable],
            }

    # Save JSON
    json_file = out_path / "latency_report.json"
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved {json_file}")

    # Generate markdown
    report = generate_markdown_report(all_results, models, n_runs, skill_name, step_level)
    md_file = out_path / "latency_report.md"
    md_file.write_text(report, encoding="utf-8")
    print(f"✅ Saved {md_file}")

    # Print summary
    print()
    print("=== Summary ===")
    for model, s in output["summary"].items():
        print(f"  {model}: p50={s['avg_p50']}s, p90={s['avg_p90']}s, stability={s['stability']}")

    unstable_list = [
        f"{r.eval_name}({r.model})"
        for r in all_results if not r.stable
    ]
    if unstable_list:
        print(f"\n⚠️  Unstable evals: {', '.join(unstable_list)}")
        print("   Consider: add --sequential for accurate measurement, or add retry logic in SKILL.md")

    return output


def main():
    parser = argparse.ArgumentParser(
        description="Latency Profiling — measure skill execution speed"
    )
    parser.add_argument("--evals", required=True, help="Path to evals.json")
    parser.add_argument("--skill-path", required=True, help="Path to SKILL.md")
    parser.add_argument(
        "--models",
        default="sonnet",
        help="Comma-separated model list (e.g., haiku,sonnet). Default: sonnet"
    )
    parser.add_argument(
        "--n-runs",
        type=int,
        default=5,
        help="Number of runs per eval (min 3 for meaningful stats). Default: 5"
    )
    parser.add_argument(
        "--step-level",
        action="store_true",
        help="Attempt step-level analysis from transcripts"
    )
    parser.add_argument(
        "--sequential",
        action="store_true",
        help="Run sequentially for accurate measurement (slower but no interference)"
    )
    parser.add_argument(
        "--output-dir",
        default="workspace/latency",
        help="Output directory"
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=4,
        help="Parallel workers for (model, eval) pairs. Default: 4"
    )

    args = parser.parse_args()

    if args.n_runs < 3:
        print("⚠️  Warning: n-runs < 3 gives unreliable statistics. Recommend at least 5.")

    models = [m.strip() for m in args.models.split(",")]

    run_latency_profile(
        evals_file=args.evals,
        skill_path=args.skill_path,
        models=models,
        n_runs=args.n_runs,
        step_level=args.step_level,
        sequential=args.sequential,
        output_dir=args.output_dir,
        workers=args.workers,
    )


if __name__ == "__main__":
    main()
