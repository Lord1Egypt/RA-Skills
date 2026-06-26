#!/usr/bin/env python3
"""
Process Summary - Generate auditable record of the entire pipeline.

Records timeline, decisions, integrity checks, reviewer scores, revision history.
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List
from datetime import datetime


def collect_pipeline_data(work_dir: str) -> Dict:
    """Collect all pipeline outputs from working directory."""
    data = {}
    
    files = {
        "evidence": "research/evidence.json",
        "manuscript_draft": "draft/manuscript.md",
        "manuscript_revised": "revised/manuscript_revised.md",
        "integrity_report_1": "draft/integrity_report.json",
        "integrity_report_2": "revised/integrity_report.json",
        "review_report": "draft/review_report.json",
        "revision_log": "revised/revision_log.json",
        "citations": "draft/citations.json"
    }
    
    for key, filepath in files.items():
        full_path = Path(work_dir) / filepath
        if full_path.exists():
            content = full_path.read_text()
            try:
                data[key] = json.loads(content) if filepath.endswith('.json') else {"content": content, "length": len(content)}
            except:
                data[key] = {"raw": content[:500]}
    
    return data


def generate_summary(work_dir: str, topic: str) -> Dict:
    """Generate comprehensive process summary."""
    print(f"📊 Generating Process Summary for: {topic}")
    
    data = collect_pipeline_data(work_dir)
    
    # Build timeline
    timeline = []
    
    # Stage 1: Research
    if "evidence" in data:
        timeline.append({
            "stage": "Research",
            "timestamp": data["evidence"].get("timestamp", "unknown"),
            "status": "completed",
            "metrics": {
                "total_papers": data["evidence"].get("total_count", 0),
                "grade_A": data["evidence"].get("grade_distribution", {}).get("A", 0),
                "grade_B": data["evidence"].get("grade_distribution", {}).get("B", 0)
            }
        })
    
    # Stage 2: Write
    if "manuscript_draft" in data:
        timeline.append({
            "stage": "Write",
            "timestamp": "unknown",
            "status": "completed",
            "metrics": {
                "word_count": data["manuscript_draft"].get("length", 0)
            }
        })
    
    # Stage 3: Integrity Check (First)
    if "integrity_report_1" in data:
        ir = data["integrity_report_1"]
        timeline.append({
            "stage": "Integrity Check (Round 1)",
            "timestamp": ir.get("timestamp", "unknown"),
            "status": ir.get("overall_pass", False) if ir.get("overall_pass", False) else "failed",
            "metrics": ir.get("citations", {}).get("summary", {})
        })
    
    # Stage 4: Review
    if "review_report" in data:
        rr = data["review_report"]
        synthesis = rr.get("synthesis", {})
        timeline.append({
            "stage": "Review",
            "timestamp": rr.get("timestamp", "unknown"),
            "status": synthesis.get("final_decision", "unknown"),
            "metrics": {
                "final_score": synthesis.get("final_score", 0),
                "editor_score": rr.get("reviews", {}).get("editor", {}).get("score", 0),
                "methodology_score": rr.get("reviews", {}).get("methodology", {}).get("score", 0),
                "domain_score": rr.get("reviews", {}).get("domain", {}).get("score", 0),
                "devil_advocate_score": rr.get("reviews", {}).get("devil_advocate", {}).get("score", 0)
            }
        })
    
    # Stage 5: Revise
    if "revision_log" in data:
        rl = data["revision_log"]
        timeline.append({
            "stage": "Revise",
            "timestamp": rl.get("timestamp", "unknown"),
            "status": "completed",
            "metrics": {
                "revisions_applied": len(rl.get("revisions_applied", []))
            }
        })
    
    # Stage 6: Integrity Check (Final)
    if "integrity_report_2" in data:
        ir = data["integrity_report_2"]
        timeline.append({
            "stage": "Integrity Check (Round 2)",
            "timestamp": ir.get("timestamp", "unknown"),
            "status": ir.get("overall_pass", False) if ir.get("overall_pass", False) else "failed",
            "metrics": ir.get("citations", {}).get("summary", {})
        })
    
    # Calculate overall metrics
    final_score = 0
    final_decision = "unknown"
    integrity_pass = False
    
    if "review_report" in data:
        final_score = data["review_report"].get("synthesis", {}).get("final_score", 0)
        final_decision = data["review_report"].get("synthesis", {}).get("final_decision", "unknown")
    
    if "integrity_report_2" in data:
        integrity_pass = data["integrity_report_2"].get("overall_pass", False)
    elif "integrity_report_1" in data:
        integrity_pass = data["integrity_report_1"].get("overall_pass", False)
    
    # Build summary
    summary = {
        "topic": topic,
        "generated_at": datetime.now().isoformat(),
        "timeline": timeline,
        "overall_metrics": {
            "final_review_score": final_score,
            "final_decision": final_decision,
            "integrity_passed": integrity_pass,
            "total_stages": len(timeline),
            "revision_rounds": 1 if "revision_log" in data else 0
        },
        "quality_gates": {
            "evidence_quality": timeline[0].get("metrics", {}).get("grade_A", 0) >= 2 if timeline else False,
            "integrity_passed": integrity_pass,
            "review_passed": final_decision in ["accept", "minor_revision"]
        },
        "recommendation": generate_recommendation(final_decision, integrity_pass)
    }
    
    # Save summary
    output_file = Path(work_dir) / "summary.json"
    Path(output_file).write_text(json.dumps(summary, indent=2, ensure_ascii=False))
    
    # Generate human-readable report
    report_md = generate_report_md(summary)
    report_file = Path(work_dir) / "summary_report.md"
    Path(report_file).write_text(report_md)
    
    print(f"  ✅ Summary saved to {output_file}")
    print(f"  ✅ Report saved to {report_file}")
    
    return summary


def generate_recommendation(decision: str, integrity: bool) -> str:
    """Generate recommendation based on final status."""
    if decision == "accept" and integrity:
        return "论文已通过所有质量门，可以提交。"
    elif decision == "minor_revision" and integrity:
        return "论文需要小幅修订后可提交。"
    elif decision == "major_revision":
        return "论文需要大幅修订，建议重新审视研究方法。"
    elif decision == "reject":
        return "论文未达到发表标准，建议重新设计研究。"
    elif not integrity:
        return "引用完整性未通过，必须修正引用问题。"
    else:
        return "状态未知，请检查各阶段输出。"


def generate_report_md(summary: Dict) -> str:
    """Generate human-readable Markdown report."""
    
    lines = [
        f"# 学术写作流水线过程报告",
        f"\n**主题**: {summary['topic']}",
        f"\n**生成时间**: {summary['generated_at']}",
        f"\n---",
        f"\n## 流水线时间线",
        ""
    ]
    
    for stage in summary.get("timeline", []):
        lines.append(f"\n### {stage['stage']}")
        lines.append(f"- 时间: {stage['timestamp']}")
        lines.append(f"- 状态: {stage['status']}")
        if stage.get("metrics"):
            lines.append(f"- 指标:")
            for k, v in stage["metrics"].items():
                lines.append(f"  - {k}: {v}")
    
    lines.extend([
        "\n---",
        "\n## 总体评估",
        f"\n- 最终评分: {summary['overall_metrics']['final_review_score']}",
        f"- 最终决定: {summary['overall_metrics']['final_decision']}",
        f"- 完整性通过: {summary['overall_metrics']['integrity_passed']}",
        f"\n### 质量门检查",
        ""
    ])
    
    for gate, passed in summary.get("quality_gates", {}).items():
        status = "✅ 通过" if passed else "❌ 未通过"
        lines.append(f"- {gate}: {status}")
    
    lines.extend([
        "\n---",
        "\n## 建议",
        f"\n{summary['recommendation']}",
        "\n---",
        "\n*此报告由 Academic Writing Pipeline 自动生成*"
    ])
    
    return "\n".join(lines)


def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: python summary.py <work_dir> [--topic <topic>]")
        sys.exit(1)
    
    work_dir = sys.argv[1]
    topic = sys.argv[3] if len(sys.argv) > 3 and sys.argv[2] == "--topic" else "Unknown Topic"
    
    summary = generate_summary(work_dir, topic)
    
    print(f"\n✅ Process Summary generated")
    print(f"   Final decision: {summary['overall_metrics']['final_decision']}")
    print(f"   Integrity passed: {summary['overall_metrics']['integrity_passed']}")
    
    return summary


if __name__ == "__main__":
    main()