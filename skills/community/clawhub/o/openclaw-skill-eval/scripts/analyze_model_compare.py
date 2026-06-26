#!/usr/bin/env python3
"""
Model Comparison Analyzer (v2 — pure data processing, no OpenClaw API calls)

Takes pre-fetched transcripts across models and computes Quality + Speed matrix.
Mo runs the spawning and history fetching; this script only analyzes data.

Usage:
    python3 scripts/analyze_model_compare.py \
        --evals evals/weather/quality.json \
        --data-dir workspace/weather/iter-1/raw/model-compare/ \
        --models haiku,sonnet \
        --output-dir workspace/weather/iter-1/model-compare/

Data directory structure:
    raw/model-compare/
    ├── eval-{id}-{model}-run-{n}-transcript.txt
    ├── eval-{id}-{model}-run-{n}-timing.json   # {"elapsed_seconds": 12.3}
    └── ...
"""

import argparse
import json
import re
import statistics
from dataclasses import dataclass, asdict
from pathlib import Path
from datetime import datetime
from typing import Optional


@dataclass
class QualityMetrics:
    quality_score: float
    assertions_passed: int
    assertions_total: int
    output_length: int


@dataclass
class SpeedMetrics:
    timings: list
    p50: float
    p90: float
    mean: float
    std_dev: float
    stable: bool
    stability_level: str


@dataclass
class EvalModelResult:
    eval_id: int
    eval_name: str
    model: str
    quality: Optional[QualityMetrics]
    speed: Optional[SpeedMetrics]


def load_transcripts_for_model(
    data_dir: Path, eval_id: int, model: str
) -> tuple[list[str], list[float]]:
    """Load all run transcripts and timings for a (eval, model) pair."""
    transcripts = []
    timings = []

    # Find all run files
    pattern = f"eval-{eval_id}-{model}-run-*-transcript.txt"
    for f in sorted(data_dir.glob(pattern)):
        transcripts.append(f.read_text(encoding="utf-8"))
        # Load corresponding timing file
        timing_file = f.with_name(f.name.replace("-transcript.txt", "-timing.json"))
        if timing_file.exists():
            timing_data = json.loads(timing_file.read_text())
            timings.append(timing_data.get("elapsed_seconds", 0))

    return transcripts, timings


def score_assertions(transcript: str, assertions: list) -> tuple[int, int]:
    """Return (passed, total)."""
    if not assertions:
        return 0, 0

    transcript_lower = transcript.lower()
    passed = 0
    for assertion in assertions:
        key_terms = [t for t in assertion.lower().split()
                     if len(t) > 3 and t not in ("that", "this", "with", "from", "uses")]
        if any(term in transcript_lower for term in key_terms):
            passed += 1

    return passed, len(assertions)


def estimate_quality(transcript: str, assertions: list) -> QualityMetrics:
    """Estimate quality score from transcript + assertions."""
    if not transcript:
        return QualityMetrics(0.0, 0, len(assertions), 0)

    passed, total = score_assertions(transcript, assertions)
    pass_rate = passed / total if total > 0 else 0

    score = 5.0 + pass_rate * 3.0
    length = len(transcript)
    if length > 200: score += 0.5
    if length > 500: score += 0.5
    if length > 1000: score += 0.5
    if length < 50: score -= 3.0
    for pattern in [r'\berror\b', r'\bfailed\b']:
        if re.search(pattern, transcript, re.IGNORECASE):
            score -= 0.5

    return QualityMetrics(
        quality_score=round(max(0, min(10, score)), 1),
        assertions_passed=passed,
        assertions_total=total,
        output_length=length
    )


def compute_speed(timings: list) -> Optional[SpeedMetrics]:
    """Compute speed stats from timing list."""
    if not timings:
        return None

    n = len(timings)
    sorted_t = sorted(timings)
    std = statistics.stdev(timings) if n >= 2 else 0

    if std < 1.0:
        stability = "HIGH"
    elif std < 3.0:
        stability = "MEDIUM"
    else:
        stability = "LOW"

    return SpeedMetrics(
        timings=[round(t, 2) for t in timings],
        p50=round(sorted_t[n // 2], 2),
        p90=round(sorted_t[int(n * 0.9)] if n >= 10 else sorted_t[-1], 2),
        mean=round(statistics.mean(timings), 2),
        std_dev=round(std, 2),
        stable=std < 3.0,
        stability_level=stability
    )


def generate_report(
    results: list[EvalModelResult],
    models: list[str],
    dimensions: list[str],
    skill_name: str
) -> str:
    lines = [
        f"# Model Comparison Report: {skill_name}",
        f"Generated: {datetime.now().isoformat()}",
        f"Models: {', '.join(models)} | Dimensions: {', '.join(dimensions)}",
        ""
    ]

    if "quality" in dimensions:
        lines += [
            "## Quality",
            "",
            "| Eval | " + " | ".join(models) + " |",
            "|------|" + "|".join(["------"] * len(models)) + "|"
        ]
        eval_ids = sorted(set(r.eval_id for r in results))
        for eid in eval_ids:
            row = []
            name = ""
            for model in models:
                r = next((x for x in results if x.eval_id == eid and x.model == model), None)
                if r and r.quality:
                    name = r.eval_name
                    row.append(f"{r.quality.quality_score}")
                else:
                    row.append("-")
            lines.append(f"| {name} | " + " | ".join(row) + " |")
        lines.append("")

    if "speed" in dimensions:
        lines += [
            "## Speed (p50)",
            "",
            "| Eval | " + " | ".join(models) + " |",
            "|------|" + "|".join(["------"] * len(models)) + "|"
        ]
        for eid in sorted(set(r.eval_id for r in results)):
            row = []
            name = ""
            for model in models:
                r = next((x for x in results if x.eval_id == eid and x.model == model), None)
                if r and r.speed:
                    name = r.eval_name
                    icon = "✅" if r.speed.stable else "⚠️"
                    row.append(f"{r.speed.p50}s {icon}")
                else:
                    row.append("-")
            lines.append(f"| {name} | " + " | ".join(row) + " |")
        lines.append("")

    return "\n".join(lines)


def analyze_model_compare(
    evals_file: str,
    data_dir: str,
    models: list[str],
    dimensions: list[str],
    output_dir: str,
) -> dict:
    with open(evals_file, encoding="utf-8") as f:
        evals_data = json.load(f)

    skill_name = evals_data.get("skill_name", "unknown")
    evals = evals_data.get("evals", [])
    d_dir = Path(data_dir)
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    all_results = []

    for eval_item in evals:
        eval_id = eval_item.get("id")
        name = eval_item.get("name", f"eval-{eval_id}")
        assertions = eval_item.get("assertions", [])

        for model in models:
            transcripts, timings = load_transcripts_for_model(d_dir, eval_id, model)

            if not transcripts and not timings:
                print(f"  ⚠️  No data for eval-{eval_id} model={model}")
                continue

            quality = None
            speed = None

            if "quality" in dimensions and transcripts:
                # Use first transcript for quality
                quality = estimate_quality(transcripts[0], assertions)

            if "speed" in dimensions and timings:
                speed = compute_speed(timings)

            result = EvalModelResult(
                eval_id=eval_id,
                eval_name=name,
                model=model,
                quality=quality,
                speed=speed
            )
            all_results.append(result)

            q_str = f"q={quality.quality_score}" if quality else ""
            s_str = f"p50={speed.p50}s" if speed else ""
            print(f"  [{eval_id}] {model}: {q_str} {s_str}")

    # Build output
    summaries = {}
    for model in models:
        model_results = [r for r in all_results if r.model == model]
        if not model_results:
            continue
        q_scores = [r.quality.quality_score for r in model_results if r.quality]
        p50s = [r.speed.p50 for r in model_results if r.speed]
        summaries[model] = {
            "avg_quality": round(statistics.mean(q_scores), 2) if q_scores else None,
            "avg_p50": round(statistics.mean(p50s), 2) if p50s else None,
        }

    # Model dependency
    model_order = ["haiku", "sonnet", "opus"]
    sorted_models = sorted(models, key=lambda m: model_order.index(m) if m in model_order else 99)
    dependency = {}
    if len(sorted_models) >= 2:
        small, large = sorted_models[0], sorted_models[-1]
        sq = summaries.get(small, {}).get("avg_quality") or 0
        lq = summaries.get(large, {}).get("avg_quality") or 0
        delta = lq - sq
        dependency = {
            "level": "HIGH" if delta > 2.0 else "MEDIUM" if delta > 1.0 else "LOW",
            "quality_delta": round(delta, 2),
            "recommendation": (
                f"Skill requires {large}+ (delta={delta:.1f})" if delta > 2.0
                else f"Both {small} and {large} acceptable"
            )
        }

    output = {
        "skill_name": skill_name,
        "timestamp": datetime.now().isoformat(),
        "models": models,
        "dimensions": dimensions,
        "results": [asdict(r) for r in all_results],
        "summary": summaries,
        "model_dependency": dependency,
    }

    json_file = out_dir / "compare_matrix.json"
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    report = generate_report(all_results, models, dimensions, skill_name)
    md_file = out_dir / "model_comparison_report.md"
    md_file.write_text(report, encoding="utf-8")

    print()
    print("=== Summary ===")
    for model, s in summaries.items():
        print(f"  {model}: quality={s.get('avg_quality')} p50={s.get('avg_p50')}s")
    if dependency:
        print(f"  Model dependency: {dependency['level']} (delta={dependency.get('quality_delta')})")
    print(f"✅ Saved to {output_dir}")

    return output


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--evals", required=True)
    parser.add_argument("--data-dir", required=True, help="Directory with transcripts + timings")
    parser.add_argument("--models", required=True, help="e.g. haiku,sonnet")
    parser.add_argument("--dimensions", default="quality,speed")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show detailed output per eval (default: summary only)"
    )
    args = parser.parse_args()

    analyze_model_compare(
        evals_file=args.evals,
        data_dir=args.data_dir,
        models=[m.strip() for m in args.models.split(",")],
        dimensions=[d.strip() for d in args.dimensions.split(",")],
        output_dir=args.output_dir,
    )


if __name__ == "__main__":
    main()
