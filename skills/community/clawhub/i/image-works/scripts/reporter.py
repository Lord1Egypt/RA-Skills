"""
Processing report generator for image-works.
Generates a comprehensive report of batch processing results.
"""
import os
import logging
from typing import Dict, List
from datetime import datetime

logger = logging.getLogger(__name__)


def generate_report(results: list, operations: list) -> Dict:
    """
    Generate a comprehensive processing report.
    
    Args:
        results: List of per-file processing results.
        operations: List of operations applied.
        
    Returns:
        Report dict with summary, stats, and details.
    """
    successful = [r for r in results if r.get("status") == "success"]
    failed = [r for r in results if r.get("status") == "failed"]
    skipped = [r for r in results if r.get("status") == "skipped"]
    
    total_input = sum(r.get("input_size", 0) for r in successful)
    total_output = sum(r.get("output_size", 0) for r in successful)
    
    # Compute sizes in human-readable format
    input_human = _format_size(total_input)
    output_human = _format_size(total_output)
    saved_human = _format_size(total_input - total_output)
    
    saved_percent = ((total_input - total_output) / total_input * 100) if total_input > 0 else 0
    
    avg_ratio = 0
    if successful:
        ratios = [r.get("compression_ratio", 0) for r in successful if r.get("compression_ratio")]
        avg_ratio = sum(ratios) / len(ratios) if ratios else 0
    
    # Operation names
    op_names = []
    for op in operations:
        op_type = op.get("type", "unknown")
        details = []
        if "quality" in op:
            details.append(f"q={op['quality']}")
        if "format" in op:
            details.append(f"→{op['format']}")
        if "width" in op:
            details.append(f"{op.get('width', '')}×{op.get('height', '')}")
        if op.get("text"):
            details.append("wm:" + op["text"][:10])
        detail_str = f" ({', '.join(details)})" if details else ""
        op_names.append(f"{op_type}{detail_str}")
    
    report = {
        "meta": {
            "total_input_files": len(results),
            "processed_successfully": len(successful),
            "failed": len(failed),
            "skipped": len(skipped),
            "operations_applied": op_names,
            "timestamp": datetime.now().isoformat(),
        },
        "summary": {
            "total_input_size": total_input,
            "total_output_size": total_output,
            "total_input_size_human": input_human,
            "total_output_size_human": output_human,
            "space_saved_human": saved_human,
            "space_saved_percent": round(saved_percent, 1),
            "avg_compression_ratio": round(avg_ratio, 4),
        },
        "details": [],
        "failed_files": [],
    }
    
    for r in results:
        detail = {
            "input_path": r.get("input_path", ""),
            "output_path": r.get("output_path", ""),
            "input_size": r.get("input_size", 0),
            "output_size": r.get("output_size", 0),
            "input_size_human": _format_size(r.get("input_size", 0)),
            "output_size_human": _format_size(r.get("output_size", 0)),
            "input_dimensions": r.get("input_dimensions", "unknown"),
            "output_dimensions": r.get("output_dimensions", "unknown"),
            "format": r.get("format", ""),
            "status": r.get("status", "unknown"),
            "compression_ratio": r.get("compression_ratio", 0),
        }
        
        if r.get("status") == "failed":
            report["failed_files"].append({
                "path": r.get("input_path", ""),
                "reason": r.get("error", "Unknown error"),
            })
        else:
            report["details"].append(detail)
    
    return report


def format_report_text(report: Dict) -> str:
    """Format the report as a readable text summary."""
    meta = report.get("meta", {})
    summary = report.get("summary", {})
    
    lines = [
        "📊 Processing Report",
        "=" * 40,
        f"✅ Success: {meta.get('processed_successfully', 0)}/{meta.get('total_input_files', 0)}",
        f"❌ Failed: {meta.get('failed', 0)}",
        f"⏭  Skipped: {meta.get('skipped', 0)}",
        "",
        f"📦 Total input:  {summary.get('total_input_size_human', 'N/A')}",
        f"📦 Total output: {summary.get('total_output_size_human', 'N/A')}",
        f"💾 Saved: {summary.get('space_saved_human', 'N/A')} ({summary.get('space_saved_percent', 0)}%)",
        "",
        f"🔧 Operations: {', '.join(meta.get('operations_applied', ['N/A']))}",
    ]
    
    if report.get("failed_files"):
        lines.extend([
            "",
            "❌ Failed Files:",
            "-" * 30,
        ])
        for f in report["failed_files"]:
            lines.append(f"  • {f['path']}: {f['reason']}")
    
    return "\n".join(lines)


def _format_size(size_bytes: int) -> str:
    """Format file size in human-readable format."""
    if size_bytes == 0:
        return "0 B"
    for unit in ("B", "KB", "MB", "GB"):
        if abs(size_bytes) < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"
