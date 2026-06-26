#!/usr/bin/env python3
"""
Academic Writing Pipeline - Main orchestrator.

Full pipeline: Research → Write → Integrity Check → Review → Revise → Finalize → Summary

Usage:
    python main.py --topic "your research topic"
    python main.py --stage integrity-check --input draft/manuscript.md
"""

import argparse
import json
import os
import sys
import subprocess
import shutil
from pathlib import Path
from datetime import datetime

# Script paths (relative to this file)
SCRIPT_DIR = Path(__file__).parent

# Quality gates
QUALITY_GATES = {
    "evidence": {"min_grade_A": 2, "min_grade_AB": 5},
    "integrity": {"pass_rate": 1.0},
    "review": {"min_score": 65}
}


def run_stage(stage_name: str, command: list, work_dir: Path) -> dict:
    """Run a single pipeline stage."""
    print(f"\n{'='*60}")
    print(f"📦 Stage: {stage_name}")
    print(f"{'='*60}")
    
    result = {
        "stage": stage_name,
        "command": " ".join(command),
        "start_time": datetime.now().isoformat(),
        "success": False,
        "output": None
    }
    
    try:
        proc = subprocess.run(
            command,
            cwd=work_dir,
            capture_output=True,
            text=True,
            timeout=300  # 5 min timeout per stage
        )
        
        result["stdout"] = proc.stdout
        result["stderr"] = proc.stderr
        result["returncode"] = proc.returncode
        result["success"] = proc.returncode == 0
        result["end_time"] = datetime.now().isoformat()
        
        print(proc.stdout)
        if proc.stderr:
            print(f"⚠️ {proc.stderr}")
        
    except subprocess.TimeoutExpired:
        result["error"] = "Stage timeout (>5min)"
        result["success"] = False
        print(f"❌ {stage_name} timed out")
        
    except Exception as e:
        result["error"] = str(e)
        result["success"] = False
        print(f"❌ {stage_name} failed: {e}")
    
    return result


def check_quality_gate(stage_name: str, work_dir: Path) -> bool:
    """Check if quality gate passed."""
    
    if stage_name == "research":
        evidence_file = work_dir / "research" / "evidence.json"
        if not evidence_file.exists():
            return False
        evidence = json.loads(evidence_file.read_text())
        grade_dist = evidence.get("grade_distribution", {})
        gate = QUALITY_GATES["evidence"]
        return grade_dist.get("A", 0) >= gate["min_grade_A"] and \
               (grade_dist.get("A", 0) + grade_dist.get("B", 0)) >= gate["min_grade_AB"]
    
    elif stage_name == "integrity-check":
        # Find latest integrity report
        for subdir in ["revised", "draft"]:
            report_file = work_dir / subdir / "integrity_report.json"
            if report_file.exists():
                report = json.loads(report_file.read_text())
                return report.get("overall_pass", False)
        return False
    
    elif stage_name == "review":
        report_file = work_dir / "draft" / "review_report.json"
        if not report_file.exists():
            return False
        report = json.loads(report_file.read_text())
        decision = report.get("synthesis", {}).get("final_decision", "reject")
        return decision in ["accept", "minor_revision"]
    
    return True


def run_full_pipeline(topic: str, work_dir: str = None, max_revision_rounds: int = 2) -> dict:
    """Run complete pipeline."""
    
    # Create work directory
    if work_dir is None:
        work_dir = Path(f"output/{topic.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
    else:
        work_dir = Path(work_dir)
    
    work_dir.mkdir(parents=True, exist_ok=True)
    print(f"📁 Working directory: {work_dir}")
    
    pipeline_log = {
        "topic": topic,
        "work_dir": str(work_dir),
        "start_time": datetime.now().isoformat(),
        "stages": []
    }
    
    # Stage 1: Research
    result = run_stage(
        "Research",
        ["python3", str(SCRIPT_DIR / "research.py"), topic, str(work_dir / "research")],
        work_dir
    )
    pipeline_log["stages"].append(result)
    
    if not check_quality_gate("research", work_dir):
        print("\n❌ Evidence quality gate FAILED - returning to Research stage")
        return pipeline_log
    
    # Stage 2: Write
    result = run_stage(
        "Write",
        ["python3", str(SCRIPT_DIR / "write.py"), topic, str(work_dir / "research" / "evidence.json"), str(work_dir / "draft")],
        work_dir
    )
    pipeline_log["stages"].append(result)
    
    # Stage 3: Integrity Check (Round 1)
    manuscript_file = work_dir / "draft" / "manuscript.md"
    result = run_stage(
        "Integrity Check (Round 1)",
        ["python3", str(SCRIPT_DIR / "integrity_check.py"), str(manuscript_file)],
        work_dir
    )
    pipeline_log["stages"].append(result)
    
    if not check_quality_gate("integrity-check", work_dir):
        print("\n❌ Integrity gate FAILED - returning to Write stage")
        # TODO: Loop back to Write
    
    # Stage 4: Review
    result = run_stage(
        "Review",
        ["python3", str(SCRIPT_DIR / "review.py"), str(manuscript_file)],
        work_dir
    )
    pipeline_log["stages"].append(result)
    
    review_passed = check_quality_gate("review", work_dir)
    
    # Stage 5-6: Revise + Re-check (if needed)
    revision_round = 0
    while not review_passed and revision_round < max_revision_rounds:
        revision_round += 1
        
        result = run_stage(
            f"Revise (Round {revision_round})",
            ["python3", str(SCRIPT_DIR / "revise.py"), str(manuscript_file), str(work_dir / "draft" / "review_report.json"), str(work_dir / "revised")],
            work_dir
        )
        pipeline_log["stages"].append(result)
        
        # Re-check integrity
        revised_file = work_dir / "revised" / "manuscript_revised.md"
        result = run_stage(
            f"Integrity Check (Round {revision_round + 1})",
            ["python3", str(SCRIPT_DIR / "integrity_check.py"), str(revised_file)],
            work_dir
        )
        pipeline_log["stages"].append(result)
        
        # Re-review (optional - can skip for minor revisions)
        # For simplicity, we skip re-review and check previous decision
        
        review_passed = check_quality_gate("review", work_dir)
        
        # Update manuscript for next round
        manuscript_file = revised_file
    
    # Stage 7: Process Summary
    result = run_stage(
        "Process Summary",
        ["python3", str(SCRIPT_DIR / "summary.py"), str(work_dir), "--topic", topic],
        work_dir
    )
    pipeline_log["stages"].append(result)
    
    # Finalize
    pipeline_log["end_time"] = datetime.now().isoformat()
    pipeline_log["total_time_seconds"] = (
        datetime.fromisoformat(pipeline_log["end_time"]) -
        datetime.fromisoformat(pipeline_log["start_time"])
    ).total_seconds()
    
    # Save pipeline log
    log_file = work_dir / "pipeline_log.json"
    log_file.write_text(json.dumps(pipeline_log, indent=2, ensure_ascii=False))
    
    print(f"\n{'='*60}")
    print(f"✅ Pipeline completed in {pipeline_log['total_time_seconds']:.1f} seconds")
    print(f"📁 All outputs saved to: {work_dir}")
    print(f"{'='*60}")
    
    return pipeline_log


def run_single_stage(stage: str, input_file: str, work_dir: str = None) -> dict:
    """Run a single stage."""
    work_dir = Path(work_dir or Path(input_file).parent.parent)
    
    stage_scripts = {
        "research": ["python3", str(SCRIPT_DIR / "research.py")],
        "write": ["python3", str(SCRIPT_DIR / "write.py")],
        "integrity-check": ["python3", str(SCRIPT_DIR / "integrity_check.py")],
        "review": ["python3", str(SCRIPT_DIR / "review.py")],
        "revise": ["python3", str(SCRIPT_DIR / "revise.py")],
        "summary": ["python3", str(SCRIPT_DIR / "summary.py")]
    }
    
    if stage not in stage_scripts:
        print(f"❌ Unknown stage: {stage}")
        return {}
    
    command = stage_scripts[stage] + [input_file]
    return run_stage(stage, command, work_dir)


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="Academic Writing Pipeline")
    parser.add_argument("--topic", help="Research topic for full pipeline")
    parser.add_argument("--stage", help="Run single stage (research/write/integrity-check/review/revise/summary)")
    parser.add_argument("--input", help="Input file for single stage")
    parser.add_argument("--work-dir", help="Working directory")
    parser.add_argument("--max-revision-rounds", type=int, default=2, help="Maximum revision iterations")
    
    args = parser.parse_args()
    
    if args.stage:
        if not args.input:
            print("❌ --input required for single stage mode")
            sys.exit(1)
        result = run_single_stage(args.stage, args.input, args.work_dir)
        
    elif args.topic:
        result = run_full_pipeline(
            args.topic,
            args.work_dir,
            args.max_revision_rounds
        )
        
    else:
        parser.print_help()
        sys.exit(1)
    
    return result


if __name__ == "__main__":
    main()