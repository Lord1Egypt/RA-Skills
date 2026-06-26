#!/usr/bin/env python3
"""
payroll-data-audit: deliver_audit_files
场景十·文件交付（强制 Step 9）- 将审核输出文件打包并生成飞书交付消息。

使用方式（LLM 层调用）：
1. 流水线执行完毕后，运行此脚本获取待交付文件清单
2. 使用 message 工具发送文件到飞书
3. 附审核结论摘要

交付文件清单（11个必发文件）：
1. 00_data_scan.json      - 数据扫描确认
2. 01_audit_result.json    - 审核结果
3. 02_report_v6.html       - 表格化审核报告（推荐）
4. 02_report_v6.md         - Markdown 版审核报告
5. 02a_data_index.json     - 数据支撑索引
6. 03_kanban_v6.html       - 动态交互看板（推荐）
7. 03_kanban.md            - Markdown 版审核清单
8. 04_sampling_verify.json - 抽样校验结果
9. 05_issue_report.md      - 问题清单
10. 06_master_report.html   - 总审核报告
11. audit_summary.md        - 审核结论摘要（自动生成）

注意：本脚本不直接发送文件（那是 LLM 的消息工具职责），
      只负责生成文件清单和审核结论摘要。
"""

import json
import os
from pathlib import Path
from datetime import datetime


REQUIRED_FILES = [
    ("00_data_scan.json", "数据扫描确认"),
    ("01_audit_result.json", "审核结果"),
    ("02_report_v6.html", "表格化审核报告（推荐）"),
    ("02_report_v6.md", "Markdown 审核报告"),
    ("02a_data_index.json", "数据支撑索引"),
    ("03_kanban_v6.html", "动态交互看板（推荐）"),
    ("03_kanban.md", "Markdown 审核清单"),
    ("04_sampling_verify.json", "抽样校验结果"),
    ("05_issue_report.md", "问题清单"),
    ("06_master_report.html", "总审核报告"),
    ("audit_summary.md", "审核结论摘要（自动生成）"),
]


def generate_summary(audit_result_path: str) -> str:
    """从审核结果生成简洁的审核结论摘要"""
    if not os.path.exists(audit_result_path):
        return "# 审核结论摘要\n\n审核结果文件不存在，无法生成摘要。\n"
    
    with open(audit_result_path, "r", encoding="utf-8") as f:
        result = json.load(f)
    
    summary = result.get("summary", {})
    total = result.get("total_records", 0)
    status = summary.get("status", "N/A")
    blocked = summary.get("blocked", False)
    
    red = summary.get("p0_count", 0)
    yellow = summary.get("p1_count", 0)
    blue = summary.get("p2_count", 0)
    
    # 公式校验
    formula = result.get("formula_check", {})
    formula_passed = formula.get("passed", True)
    
    # 字段检查
    fields = result.get("field_check", {})
    fields_passed = fields.get("passed", True)
    
    lines = [
        "# 审核结论摘要",
        "",
        f"**审核时间**: {result.get('audit_time', 'N/A')}",
        f"**审核版本**: {result.get('version', 'N/A')}",
        f"**审核范围**: {total} 条记录",
        "",
        "## 总体结论",
        "",
    ]
    
    if blocked:
        lines.append(f"🔴 **审核未通过** - 触发 {red} 条红线，需要立即处理。")
    elif yellow > 0:
        lines.append(f"⚠️  **审核通过（有预警）** - {yellow} 条黄线预警，建议核实。")
    else:
        lines.append("✅ **审核通过** - 未发现红线/黄线问题。")
    
    lines += [
        "",
        "## 审核维度",
        "",
        "| 维度 | 结果 |",
        "|------|------|",
        f"| 🔴 红线 | {red} 条触发 |" if red > 0 else "| 🔴 红线 | 0 条触发 ✅ |",
        f"| ⚠️  黄线 | {yellow} 条触发 |" if yellow > 0 else "| ⚠️  黄线 | 0 条触发 ✅ |",
        f"| ℹ️  蓝线 | {blue} 条提示 |" if blue > 0 else "| ℹ️  蓝线 | 0 条提示 |",
        f"| 📐 公式校验 | 通过 ✅ |" if formula_passed else "| 📐 公式校验 | **未通过** ❌ |",
        f"| 📋 字段检查 | 通过 ✅ |" if fields_passed else "| 📋 字段检查 | **未通过** ❌ |",
        "",
        "## 详细报告",
        "",
        "请查阅以下文件获取完整信息：",
        "- `06_master_report.html` - 总审核报告（一份看全）",
        "- `03_kanban_v6.html` - 动态交互看板（筛选/排序/导出）",
        "- `05_issue_report.md` - 问题清单（逐项跟进）",
        "",
    ]
    
    return "\n".join(lines)


def list_deliverable_files(output_dir: str) -> list:
    """列出 output_dir 中所有可交付的文件，返回 (file_path, description, exists) 列表"""
    results = []
    for filename, desc in REQUIRED_FILES:
        filepath = os.path.join(output_dir, filename)
        exists = os.path.exists(filepath)
        size = os.path.getsize(filepath) if exists else 0
        results.append({
            "filename": filename,
            "description": desc,
            "path": filepath,
            "exists": exists,
            "size": size,
        })
    return results


def main():
    import argparse
    parser = argparse.ArgumentParser(description="审核文件交付清单生成器")
    parser.add_argument("--output-dir", required=True, help="审核输出目录")
    parser.add_argument("--audit-result", help="审核结果 JSON 路径（用于生成摘要）")
    parser.add_argument("--format", choices=["json", "markdown"], default="markdown",
                        help="输出格式（默认 markdown）")
    args = parser.parse_args()
    
    files = list_deliverable_files(args.output_dir)
    
    # 生成审核摘要
    summary_path = os.path.join(args.output_dir, "audit_summary.md")
    if args.audit_result:
        summary_content = generate_summary(args.audit_result)
        with open(summary_path, "w", encoding="utf-8") as f:
            f.write(summary_content)
        # 标记审计摘要已生成
        for f_item in files:
            if f_item["filename"] == "audit_summary.md":
                f_item["exists"] = True
                f_item["size"] = len(summary_content)
    
    if args.format == "json":
        print(json.dumps(files, ensure_ascii=False, indent=2))
    else:
        print("📦 审核文件交付清单")
        print("=" * 50)
        exists_count = 0
        for f_item in files:
            status = "✅" if f_item["exists"] else "❌"
            size_str = f"{f_item['size']:,}B" if f_item["exists"] else "N/A"
            print(f"  {status} {f_item['filename']:<30s} {f_item['description']:<30s} {size_str}")
            if f_item["exists"]:
                exists_count += 1
        print("=" * 50)
        print(f"可交付: {exists_count}/{len(files)} 个文件")


if __name__ == "__main__":
    main()
