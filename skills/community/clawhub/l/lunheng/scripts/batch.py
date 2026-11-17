#!/usr/bin/env python3
"""
pipeline/batch.py — 批量处理模块
2026-07-19 新增，Phase 2.3

功能：
- 从 CSV/JSON 文件读取多个案情
- 逐个运行 pipeline
- 汇总输出结果
"""

import csv
import json
import sys
import time
from pathlib import Path
from typing import List, Dict

# 添加 scripts 目录到 path
sys.path.insert(0, str(Path(__file__).parent))

from pipeline import run_pipeline
from error_utils import log_error, log_info, log_warning


def load_cases_from_csv(file_path: str, text_column: str = "案情",
                        cause_column: str = "案由") -> List[Dict]:
    """从 CSV 加载案情列表"""
    cases = []
    try:
        with open(file_path, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                text = row.get(text_column, "").strip()
                if not text:
                    log_warning("batch", "load_csv", f"第{i+1}行案情为空，跳过")
                    continue
                cases.append({
                    "id": row.get("id", str(i+1)),
                    "text": text,
                    "cause": row.get(cause_column, ""),
                    "source": f"csv:{file_path}:{i+1}",
                })
    except Exception as e:
        log_error("batch", "load_csv", e, {"file": file_path})
    return cases


def load_cases_from_json(file_path: str) -> List[Dict]:
    """从 JSON 加载案情列表"""
    cases = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            for i, item in enumerate(data):
                text = item.get("text", "").strip()
                if not text:
                    continue
                cases.append({
                    "id": item.get("id", str(i+1)),
                    "text": text,
                    "cause": item.get("cause", ""),
                    "source": f"json:{file_path}:{i+1}",
                })
        elif isinstance(data, dict) and "cases" in data:
            for i, item in enumerate(data["cases"]):
                text = item.get("text", "").strip()
                if not text:
                    continue
                cases.append({
                    "id": item.get("id", str(i+1)),
                    "text": text,
                    "cause": item.get("cause", ""),
                    "source": f"json:{file_path}:{i+1}",
                })
    except Exception as e:
        log_error("batch", "load_json", e, {"file": file_path})
    return cases


def run_batch(cases: List[Dict], output_format: str = "markdown",
              delay: float = 1.0) -> Dict:
    """
    批量运行 pipeline。

    Returns:
        {
            "total": int,
            "success": int,
            "failed": int,
            "results": [{"id": ..., "status": ..., "output": ..., "error": ...}],
            "summary": str,
        }
    """
    results = []
    success = 0
    failed = 0

    print(f"\n{'='*60}", file=sys.stderr)
    print(f"📋 批量处理: {len(cases)} 个案件", file=sys.stderr)
    print(f"{'='*60}\n", file=sys.stderr)

    for i, case in enumerate(cases, 1):
        case_id = case.get("id", str(i))
        print(f"\n[{i}/{len(cases)}] 处理案件 {case_id}...", file=sys.stderr)

        try:
            result = run_pipeline(
                case_text=case["text"],
                cause=case.get("cause", ""),
                output_format=output_format,
            )

            results.append({
                "id": case_id,
                "status": "success",
                "output": result["formatted"],
                "cause": result["elements"].get("cause", ""),
                "warnings": result.get("all_warnings", []),
                "law_check_score": result.get("law_check", {}).get("score"),
                "quality_check_score": result.get("quality_check", {}).get("score"),
            })
            success += 1

        except Exception as e:
            log_error("batch", "run_pipeline", e, {"case_id": case_id})
            results.append({
                "id": case_id,
                "status": "failed",
                "output": "",
                "error": str(e),
            })
            failed += 1

        # 间隔避免 API 限流
        if i < len(cases):
            time.sleep(delay)

    summary = f"完成: {success}/{len(cases)} 成功, {failed} 失败"
    print(f"\n{'='*60}", file=sys.stderr)
    print(f"✅ {summary}", file=sys.stderr)
    print(f"{'='*60}\n", file=sys.stderr)

    return {
        "total": len(cases),
        "success": success,
        "failed": failed,
        "results": results,
        "summary": summary,
    }


def save_batch_results(batch_result: Dict, output_dir: str):
    """保存批量处理结果"""
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    # 保存汇总 JSON
    summary_path = out_path / "batch_summary.json"
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(batch_result, f, ensure_ascii=False, indent=2, default=str)
    log_info("batch", "save", f"汇总已保存: {summary_path}")

    # 保存每个案件的输出
    for r in batch_result["results"]:
        if r["status"] == "success":
            case_path = out_path / f"case_{r['id']}.md"
            with open(case_path, "w", encoding="utf-8") as f:
                f.write(r["output"])

    log_info("batch", "save", f"已保存 {batch_result['success']} 个案件输出到 {out_path}")


# ─── CLI ───────────────────────────────────────────────
def main():
    import argparse

    parser = argparse.ArgumentParser(description="论衡批量处理")
    parser.add_argument("input", help="输入文件路径 (CSV 或 JSON)")
    parser.add_argument("--output-dir", "-o", default="./batch_output",
                        help="输出目录 (默认: ./batch_output)")
    parser.add_argument("--format", choices=["markdown", "text", "html"],
                        default="markdown", help="输出格式")
    parser.add_argument("--text-column", default="案情",
                        help="CSV 中案情列名 (默认: 案情)")
    parser.add_argument("--cause-column", default="案由",
                        help="CSV 中案由列名 (默认: 案由)")
    parser.add_argument("--delay", type=float, default=1.0,
                        help="案件间隔秒数 (默认: 1.0)")
    args = parser.parse_args()

    # 加载案情
    input_path = Path(args.input)
    if input_path.suffix.lower() == ".csv":
        cases = load_cases_from_csv(args.input, args.text_column, args.cause_column)
    elif input_path.suffix.lower() == ".json":
        cases = load_cases_from_json(args.input)
    else:
        print(f"不支持的文件格式: {input_path.suffix}", file=sys.stderr)
        sys.exit(1)

    if not cases:
        print("未找到有效案情", file=sys.stderr)
        sys.exit(1)

    print(f"加载了 {len(cases)} 个案情", file=sys.stderr)

    # 批量处理
    result = run_batch(cases, args.format, args.delay)

    # 保存结果
    save_batch_results(result, args.output_dir)

    print(f"\n📄 结果已保存到: {args.output_dir}", file=sys.stderr)


if __name__ == "__main__":
    main()
