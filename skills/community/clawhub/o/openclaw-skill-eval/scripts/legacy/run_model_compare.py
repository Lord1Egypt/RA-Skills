#!/usr/bin/env python3
"""
Model Comparison — Phase 3.4

Compare Quality + Speed across models for the same skill.

Usage:
    # Quality + Speed (full eval)
    python scripts/run_model_compare.py \
        --evals evals/example-quality.json \
        --skill-path ./SKILL.md \
        --models haiku,sonnet \
        --dimensions quality,speed \
        --n-runs 5 \
        --output-dir workspace/model-compare-1 \
        --workers 6

    # Quality only (fast)
    python scripts/run_model_compare.py \
        --evals evals/example-quality.json \
        --skill-path ./SKILL.md \
        --models haiku,sonnet \
        --dimensions quality \
        --output-dir workspace/model-compare-1

Architecture: ARCHITECTURE.md
Design: PHASE-3-4-DESIGN.md
"""

import argparse
import json
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
    """Resolve model alias to full name."""
    return MODEL_ALIASES.get(alias, alias)


# === Data Classes ===

@dataclass
class QualityMetrics:
    triggered: bool
    quality_score: float  # 0-10
    output_length: int
    
@dataclass
class SpeedMetrics:
    timings_seconds: list
    p50: float
    p90: float
    mean: float
    min_time: float
    max_time: float
    std_dev: float
    stable: bool  # std_dev < 3s

@dataclass
class EvalResult:
    eval_id: int
    eval_name: str
    model: str
    quality: Optional[QualityMetrics]
    speed: Optional[SpeedMetrics]
    transcript: str


# === Core Functions ===

def spawn_eval_single(
    eval_item: dict,
    skill_path: str,
    model: str,
    include_skill: bool = True
) -> tuple[str, float]:
    """
    Spawn a single eval and return (transcript, elapsed_seconds).
    """
    prompt = eval_item.get("prompt", "")
    
    if include_skill:
        task = f"Read {skill_path} for guidance.\n\n{prompt}"
    else:
        task = prompt
    
    start = time.time()
    
    result = invoke("sessions_spawn", {
        "task": task,
        "model": model,
        "sandbox": "inherit",
        "cleanup": "keep",
        "mode": "run",
        "runTimeoutSeconds": 120
    })
    
    elapsed = time.time() - start
    
    # Extract transcript from result
    transcript = ""
    if isinstance(result, dict):
        transcript = result.get("output", "") or result.get("result", "") or str(result)
    else:
        transcript = str(result)
    
    return transcript, elapsed


def run_eval_for_model(
    eval_item: dict,
    skill_path: str,
    model: str,
    dimensions: list[str],
    n_runs: int
) -> EvalResult:
    """
    Run a single eval for a single model, collecting requested dimensions.
    """
    eval_id = eval_item.get("id", 0)
    eval_name = eval_item.get("name", f"eval-{eval_id}")
    full_model = resolve_model(model)
    
    quality = None
    speed = None
    all_transcripts = []
    all_timings = []
    
    # Determine how many runs we need
    runs_needed = n_runs if "speed" in dimensions else 1
    
    for i in range(runs_needed):
        transcript, elapsed = spawn_eval_single(
            eval_item, skill_path, full_model, include_skill=True
        )
        all_transcripts.append(transcript)
        all_timings.append(elapsed)
    
    # Use first transcript for quality analysis
    main_transcript = all_transcripts[0] if all_transcripts else ""
    
    # Quality metrics
    if "quality" in dimensions:
        # Check if triggered (simple heuristic: output > 100 chars and mentions skill-related content)
        triggered = len(main_transcript) > 100
        
        # Quality score (simple heuristic based on output completeness)
        # In production, this would call a grader LLM
        quality_score = estimate_quality_score(main_transcript, eval_item)
        
        quality = QualityMetrics(
            triggered=triggered,
            quality_score=quality_score,
            output_length=len(main_transcript)
        )
    
    # Speed metrics
    if "speed" in dimensions and len(all_timings) >= 2:
        sorted_timings = sorted(all_timings)
        n = len(sorted_timings)
        
        speed = SpeedMetrics(
            timings_seconds=all_timings,
            p50=sorted_timings[n // 2],
            p90=sorted_timings[int(n * 0.9)] if n >= 10 else sorted_timings[-1],
            mean=statistics.mean(all_timings),
            min_time=min(all_timings),
            max_time=max(all_timings),
            std_dev=statistics.stdev(all_timings) if n >= 2 else 0,
            stable=statistics.stdev(all_timings) < 3.0 if n >= 2 else True
        )
    elif "speed" in dimensions:
        # Single run, limited speed info
        speed = SpeedMetrics(
            timings_seconds=all_timings,
            p50=all_timings[0] if all_timings else 0,
            p90=all_timings[0] if all_timings else 0,
            mean=all_timings[0] if all_timings else 0,
            min_time=all_timings[0] if all_timings else 0,
            max_time=all_timings[0] if all_timings else 0,
            std_dev=0,
            stable=True
        )
    
    return EvalResult(
        eval_id=eval_id,
        eval_name=eval_name,
        model=model,
        quality=quality,
        speed=speed,
        transcript=main_transcript
    )


def estimate_quality_score(transcript: str, eval_item: dict) -> float:
    """
    Estimate quality score (0-10) based on heuristics.
    
    In production, this would call a grader LLM.
    For now, use simple heuristics:
    - Length (longer = more complete, up to a point)
    - Contains expected patterns
    """
    score = 5.0  # baseline
    
    # Length bonus
    length = len(transcript)
    if length > 500:
        score += 1.0
    if length > 1000:
        score += 1.0
    if length > 2000:
        score += 0.5
    
    # Check for expected output patterns
    expected = eval_item.get("expected_output", "")
    if expected and expected.lower() in transcript.lower():
        score += 2.0
    
    # Penalty for very short output
    if length < 100:
        score -= 2.0
    
    # Penalty for error indicators
    error_patterns = ["error", "failed", "cannot", "unable to"]
    for pattern in error_patterns:
        if pattern in transcript.lower():
            score -= 0.5
    
    return max(0, min(10, score))


def calculate_model_summary(
    results: list[EvalResult],
    model: str
) -> dict:
    """Calculate summary statistics for a model."""
    model_results = [r for r in results if r.model == model]
    
    summary = {"model": model}
    
    # Quality summary
    quality_scores = [r.quality.quality_score for r in model_results if r.quality]
    if quality_scores:
        summary["avg_quality"] = round(statistics.mean(quality_scores), 2)
        summary["trigger_rate"] = sum(1 for r in model_results if r.quality and r.quality.triggered) / len(model_results)
    
    # Speed summary
    speed_p50s = [r.speed.p50 for r in model_results if r.speed]
    if speed_p50s:
        summary["avg_p50"] = round(statistics.mean(speed_p50s), 2)
        summary["avg_p90"] = round(statistics.mean([r.speed.p90 for r in model_results if r.speed]), 2)
        summary["stability"] = "HIGH" if all(r.speed.stable for r in model_results if r.speed) else "LOW"
    
    return summary


def calculate_model_dependency(summaries: dict) -> dict:
    """
    Calculate model dependency level based on quality delta.
    """
    models = list(summaries.keys())
    if len(models) < 2:
        return {"level": "N/A", "reason": "Need at least 2 models to compare"}
    
    # Compare smallest vs largest model (assuming haiku < sonnet < opus)
    model_order = ["haiku", "sonnet", "opus"]
    sorted_models = sorted(models, key=lambda m: model_order.index(m) if m in model_order else 99)
    
    small = sorted_models[0]
    large = sorted_models[-1]
    
    small_quality = summaries[small].get("avg_quality", 0)
    large_quality = summaries[large].get("avg_quality", 0)
    
    delta = large_quality - small_quality
    
    if delta < 1.0:
        level = "LOW"
        recommendation = f"Skill works well on {small}. Can save cost by using smaller model."
    elif delta < 2.0:
        level = "MEDIUM"
        recommendation = f"Consider using {large} for complex tasks, {small} for simple ones."
    else:
        level = "HIGH"
        recommendation = f"Skill requires {large}+. Consider simplifying SKILL.md instructions."
    
    return {
        "level": level,
        "small_model": small,
        "large_model": large,
        "quality_delta": round(delta, 2),
        "recommendation": recommendation
    }


def generate_markdown_report(
    results: list[EvalResult],
    summaries: dict,
    dependency: dict,
    dimensions: list[str],
    skill_name: str
) -> str:
    """Generate human-readable markdown report."""
    lines = [
        f"# Model Comparison Report: {skill_name}",
        "",
        f"Generated: {datetime.now().isoformat()}",
        f"Dimensions: {', '.join(dimensions)}",
        ""
    ]
    
    models = list(summaries.keys())
    
    # Quality section
    if "quality" in dimensions:
        lines.extend([
            "## Quality Dimension",
            "",
            "| Eval | " + " | ".join(models) + " |",
            "|------|" + "|".join(["------"] * len(models)) + "|"
        ])
        
        # Group by eval
        eval_ids = sorted(set(r.eval_id for r in results))
        for eval_id in eval_ids:
            row = []
            eval_name = ""
            for model in models:
                r = next((x for x in results if x.eval_id == eval_id and x.model == model), None)
                if r and r.quality:
                    eval_name = r.eval_name
                    status = "✅" if r.quality.triggered else "❌"
                    row.append(f"{r.quality.quality_score:.1f} {status}")
                else:
                    row.append("-")
            lines.append(f"| {eval_name} | " + " | ".join(row) + " |")
        
        # Averages
        avg_row = [f"**{summaries[m].get('avg_quality', '-')}**" for m in models]
        lines.append(f"| **Average** | " + " | ".join(avg_row) + " |")
        lines.append("")
    
    # Speed section
    if "speed" in dimensions:
        lines.extend([
            "## Speed Dimension",
            "",
            "| Eval | " + " | ".join([f"{m} p50" for m in models]) + " |",
            "|------|" + "|".join(["------"] * len(models)) + "|"
        ])
        
        eval_ids = sorted(set(r.eval_id for r in results))
        for eval_id in eval_ids:
            row = []
            eval_name = ""
            for model in models:
                r = next((x for x in results if x.eval_id == eval_id and x.model == model), None)
                if r and r.speed:
                    eval_name = r.eval_name
                    stable = "✅" if r.speed.stable else "⚠️"
                    row.append(f"{r.speed.p50:.1f}s {stable}")
                else:
                    row.append("-")
            lines.append(f"| {eval_name} | " + " | ".join(row) + " |")
        
        # Averages
        avg_row = [f"**{summaries[m].get('avg_p50', '-')}s**" for m in models]
        lines.append(f"| **Average** | " + " | ".join(avg_row) + " |")
        lines.append("")
    
    # Model Dependency
    lines.extend([
        f"## Model Dependency: {dependency['level']} {'⚠️' if dependency['level'] == 'HIGH' else ''}",
        "",
        f"Quality delta ({dependency.get('small_model', 'N/A')} vs {dependency.get('large_model', 'N/A')}): {dependency.get('quality_delta', 'N/A')}",
        "",
        f"**Recommendation**: {dependency.get('recommendation', 'N/A')}",
        ""
    ])
    
    # Tradeoff analysis (if both dimensions)
    if "quality" in dimensions and "speed" in dimensions and len(models) >= 2:
        lines.extend([
            "## Tradeoff Analysis",
            "",
            "| Model | Quality | Speed (p50) | Recommendation |",
            "|-------|---------|-------------|----------------|"
        ])
        
        baseline_model = "sonnet" if "sonnet" in models else models[-1]
        baseline_quality = summaries.get(baseline_model, {}).get("avg_quality", 0)
        baseline_speed = summaries.get(baseline_model, {}).get("avg_p50", 0)
        
        for model in models:
            s = summaries[model]
            q = s.get("avg_quality", 0)
            sp = s.get("avg_p50", 0)
            
            if model == baseline_model:
                q_diff = "(baseline)"
                sp_diff = "(baseline)"
                rec = "✅ Recommended"
            else:
                q_pct = ((q - baseline_quality) / baseline_quality * 100) if baseline_quality else 0
                sp_pct = ((sp - baseline_speed) / baseline_speed * 100) if baseline_speed else 0
                q_diff = f"{q_pct:+.0f}%"
                sp_diff = f"{sp_pct:+.0f}%"
                
                if q_pct < -20:
                    rec = "❌ Quality too low"
                elif sp_pct > 30:
                    rec = "⚠️ Too slow"
                else:
                    rec = "✓ Consider"
            
            lines.append(f"| {model} | {q:.1f} ({q_diff}) | {sp:.1f}s ({sp_diff}) | {rec} |")
        
        lines.append("")
    
    return "\n".join(lines)


def run_model_comparison(
    evals_file: str,
    skill_path: str,
    models: list[str],
    dimensions: list[str],
    n_runs: int,
    output_dir: str,
    workers: int
) -> dict:
    """
    Main entry point for model comparison.
    """
    # Load evals
    with open(evals_file, encoding="utf-8") as f:
        evals_data = json.load(f)
    
    skill_name = evals_data.get("skill_name", Path(skill_path).stem)
    evals = evals_data.get("evals", [])
    
    print(f"Running model comparison for {skill_name}")
    print(f"  Models: {', '.join(models)}")
    print(f"  Dimensions: {', '.join(dimensions)}")
    print(f"  Evals: {len(evals)}")
    print(f"  N-runs (speed): {n_runs}")
    print(f"  Workers: {workers}")
    print()
    
    # Create output directory
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    (out_path / "raw").mkdir(exist_ok=True)
    
    # Run all (model, eval) combinations in parallel
    all_results: list[EvalResult] = []
    tasks = []
    
    for model in models:
        for eval_item in evals:
            tasks.append((eval_item, model))
    
    total_tasks = len(tasks)
    completed = 0
    
    print(f"Spawning {total_tasks} eval runs...")
    
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {}
        for eval_item, model in tasks:
            future = executor.submit(
                run_eval_for_model,
                eval_item, skill_path, model, dimensions, n_runs
            )
            futures[future] = (eval_item["id"], model)
        
        for future in as_completed(futures):
            eval_id, model = futures[future]
            completed += 1
            try:
                result = future.result()
                all_results.append(result)
                print(f"  [{completed}/{total_tasks}] {model} eval-{eval_id}: "
                      f"quality={result.quality.quality_score:.1f if result.quality else 'N/A'}, "
                      f"p50={result.speed.p50:.1f}s" if result.speed else "")
                
                # Save transcript
                transcript_file = out_path / "raw" / f"eval-{eval_id}-{model}-transcript.txt"
                transcript_file.write_text(result.transcript, encoding="utf-8")
                
            except Exception as e:
                print(f"  [{completed}/{total_tasks}] {model} eval-{eval_id}: ERROR - {e}")
    
    print()
    
    # Calculate summaries
    summaries = {}
    for model in models:
        summaries[model] = calculate_model_summary(all_results, model)
    
    # Calculate model dependency
    dependency = calculate_model_dependency(summaries)
    
    # Build output structure
    output = {
        "skill_name": skill_name,
        "models_tested": models,
        "dimensions": dimensions,
        "n_runs": n_runs,
        "timestamp": datetime.now().isoformat(),
        "eval_matrix": [
            {
                "eval_id": r.eval_id,
                "eval_name": r.eval_name,
                "model": r.model,
                "quality": asdict(r.quality) if r.quality else None,
                "speed": asdict(r.speed) if r.speed else None
            }
            for r in all_results
        ],
        "summary": summaries,
        "model_dependency": dependency
    }
    
    # Save JSON
    json_file = out_path / "compare_matrix.json"
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved {json_file}")
    
    # Generate and save markdown report
    report = generate_markdown_report(all_results, summaries, dependency, dimensions, skill_name)
    md_file = out_path / "model_comparison_report.md"
    md_file.write_text(report, encoding="utf-8")
    print(f"✅ Saved {md_file}")
    
    # Print summary
    print()
    print("=== Summary ===")
    for model, s in summaries.items():
        q = s.get("avg_quality", "N/A")
        p = s.get("avg_p50", "N/A")
        print(f"  {model}: quality={q}, p50={p}s")
    
    print()
    print(f"Model Dependency: {dependency['level']}")
    print(f"  {dependency.get('recommendation', '')}")
    
    return output


def main():
    parser = argparse.ArgumentParser(
        description="Model Comparison — compare Quality + Speed across models"
    )
    parser.add_argument(
        "--evals",
        required=True,
        help="Path to evals.json"
    )
    parser.add_argument(
        "--skill-path",
        required=True,
        help="Path to SKILL.md"
    )
    parser.add_argument(
        "--models",
        required=True,
        help="Comma-separated model list (e.g., haiku,sonnet,opus)"
    )
    parser.add_argument(
        "--dimensions",
        default="quality,speed",
        help="Comma-separated dimensions (quality,speed). Default: both"
    )
    parser.add_argument(
        "--n-runs",
        type=int,
        default=5,
        help="Number of runs per eval for speed measurement. Default: 5"
    )
    parser.add_argument(
        "--output-dir",
        default="workspace/model-compare",
        help="Output directory"
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=6,
        help="Number of parallel workers. Default: 6"
    )
    
    args = parser.parse_args()
    
    models = [m.strip() for m in args.models.split(",")]
    dimensions = [d.strip() for d in args.dimensions.split(",")]
    
    run_model_comparison(
        evals_file=args.evals,
        skill_path=args.skill_path,
        models=models,
        dimensions=dimensions,
        n_runs=args.n_runs,
        output_dir=args.output_dir,
        workers=args.workers
    )


if __name__ == "__main__":
    main()
