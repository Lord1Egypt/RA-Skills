#!/usr/bin/env python3
"""
payroll-data-audit: deliver_to_feishu
场景十·文件交付（强制 Step 9）- 自动上传所有审核文件到飞书云盘，
创建飞书文档，并生成完整的交付消息（可直接发送）。

设计原则：把交付动作下沉到代码，LLM 只负责调用脚本 + 转发结果。
"""

import json
import os
import subprocess
import sys
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


def run_cmd(cmd: str, cwd: str = None) -> dict:
    """Run a shell command and return {ok, stdout, stderr}"""
    result = subprocess.run(
        cmd, shell=True, cwd=cwd,
        capture_output=True, text=True, timeout=120
    )
    try:
        data = json.loads(result.stdout.strip())
        return {"ok": result.returncode == 0, "data": data, "stderr": result.stderr}
    except json.JSONDecodeError:
        return {"ok": result.returncode == 0, "output": result.stdout, "stderr": result.stderr}


def upload_file_to_drive(file_path: str, name: str) -> dict:
    """Upload a file to Feishu Drive root folder (cd to file dir first for relative path requirement)"""
    abs_path = os.path.abspath(file_path)
    file_dir = os.path.dirname(abs_path)
    file_name = os.path.basename(abs_path)
    cmd = f'cd "{file_dir}" && lark-cli drive +upload --file "./{file_name}" --name "{name}" --as user'
    result = run_cmd(cmd)
    if result["ok"] and "data" in result:
        return {
            "filename": name,
            "ok": True,
            "file_token": result["data"].get("data", {}).get("file_token", ""),
            "url": result["data"].get("data", {}).get("url", ""),
            "size": result["data"].get("data", {}).get("size", 0),
        }
    return {"filename": name, "ok": False, "error": result.get("output") or result.get("stderr")}


def import_as_docx(file_path: str, name: str) -> dict:
    """Import a .md file as a Feishu docx document"""
    abs_path = os.path.abspath(file_path)
    file_dir = os.path.dirname(abs_path)
    file_name = os.path.basename(abs_path)
    cmd = f'cd "{file_dir}" && lark-cli drive +import --file "./{file_name}" --name "{name}" --type docx --as user'
    result = run_cmd(cmd)
    if result["ok"] and "data" in result:
        return {
            "filename": name,
            "ok": True,
            "doc_token": result["data"].get("data", {}).get("token", ""),
            "url": result["data"].get("data", {}).get("url", ""),
        }
    return {"filename": name, "ok": False, "error": result.get("output") or result.get("stderr")}


def generate_summary_from_audit(audit_result_path: str, total_files: int, uploaded_files: int, doc_url: str) -> str:
    """Generate the final delivery message for Feishu"""
    with open(audit_result_path, "r", encoding="utf-8") as f:
        result = json.load(f)
    
    summary = result.get("summary", {})
    total = result.get("total_records", 0)
    blocked = summary.get("blocked", False)
    red = summary.get("p0_count", 0)
    yellow = summary.get("p1_count", 0)
    blue = summary.get("p2_count", 0)
    formula_passed = result.get("formula_check", {}).get("passed", True)
    fields_passed = result.get("field_check", {}).get("passed", True)
    
    # Comparison data
    comparison = result.get("comparison", {})
    headcount = comparison.get("headcount", {})
    metrics = comparison.get("metrics", {})
    
    lines = [
        "**📊 工资审核报告 — 完整交付**",
        "",
        f"**审核范围**：{total}人",
        "",
        "### 总体结论",
    ]
    
    if blocked:
        lines.append(f"🔴 **审核未通过** — 触发 {red} 条红线，需要立即处理。")
    elif yellow > 0:
        lines.append(f"⚠️ **审核通过（有预警）** — {yellow} 条黄线预警，建议核实。")
    else:
        lines.append("✅ **审核通过** — 未发现红线/黄线问题。")
    
    lines += [
        "",
        "| 维度 | 结果 |",
        "|------|------|",
        "| 📐 公式校验 | ✅ 通过 |" if formula_passed else "| 📐 公式校验 | ❌ 未通过 |",
        "| 📋 字段检查 | ✅ 通过 |" if fields_passed else "| 📋 字段检查 | ❌ 未通过 |",
        f"| 🔴 红线 | {red} 条 |",
        f"| ⚠️ 黄线 | {yellow} 条 |",
        f"| ℹ️ 蓝线 | {blue} 条 |",
        "",
        "### 📎 交付文件清单",
        "",
        f"**📄 飞书文档（在线查看）：**",
        doc_url if doc_url else "（文档创建失败，请查看云盘文件）",
        "",
        f"**📁 云盘文件（{uploaded_files}/{total_files} 个）：**",
    ]
    
    for filename, desc in REQUIRED_FILES:
        lines.append(f"- {filename} — {desc}")
    
    # Key findings from comparison
    lines += [
        "",
        "### 📊 总额环比",
    ]
    for field, data in metrics.items():
        change_pct = data.get("change_pct", 0)
        current = data.get("current", 0)
        previous = data.get("previous", 0)
        if abs(change_pct) > 10:
            lines.append(f"- {field}：{previous:,.0f} → {current:,.0f} ({change_pct:+.1f}%) ⚠️")
        else:
            lines.append(f"- {field}：{previous:,.0f} → {current:,.0f} ({change_pct:+.1f}%)")
    
    lines += [
        "",
        "---",
        f"*由 payroll-data-audit 自动交付 | 时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*",
    ]
    
    return "\n".join(lines)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="审核文件交付到飞书")
    parser.add_argument("--output-dir", required=True, help="审核输出目录")
    parser.add_argument("--audit-result", help="审核结果 JSON 路径")
    parser.add_argument("--skip-upload", action="store_true", help="跳过上传（仅生成消息）")
    args = parser.parse_args()
    
    if not args.audit_result:
        args.audit_result = os.path.join(args.output_dir, "01_audit_result.json")
    
    print("=" * 60)
    print("📦 审核文件交付到飞书（Step 9）")
    print("=" * 60)
    
    # Step 1: Verify all required files exist
    print("\n【Step 1】验证文件完整性...")
    missing = []
    for filename, desc in REQUIRED_FILES:
        filepath = os.path.join(args.output_dir, filename)
        if not os.path.exists(filepath):
            missing.append(filename)
    
    if missing:
        print(f"  ❌ 缺少 {len(missing)} 个文件：{', '.join(missing)}")
        print("  💡 请先运行 run_full_pipeline.py 生成完整输出")
        sys.exit(1)
    print(f"  ✅ {len(REQUIRED_FILES)} 个文件全部存在")
    
    # Step 2: Upload files to Feishu Drive
    uploaded = []
    doc_url = None
    
    if not args.skip_upload:
        print("\n【Step 2】上传文件到飞书云盘...")
        for filename, desc in REQUIRED_FILES:
            filepath = os.path.join(args.output_dir, filename)
            print(f"  📤 {filename} ({os.path.getsize(filepath):,}B)...")
            result = upload_file_to_drive(filepath, filename)
            if result["ok"]:
                uploaded.append(result)
                print(f"     ✅ {result.get('url', 'OK')}")
            else:
                print(f"     ❌ {result.get('error', 'Unknown error')}")
        
        # Step 3: Import MD as docx
        print("\n【Step 3】创建飞书文档...")
        md_file = os.path.join(args.output_dir, "02_report_v6.md")
        result = import_as_docx(md_file, "工资审核报告")
        if result["ok"]:
            doc_url = result["url"]
            print(f"  ✅ 飞书文档: {doc_url}")
        else:
            print(f"  ❌ 文档创建失败: {result.get('error')}")
    
    # Step 4: Generate delivery message
    print("\n【Step 4】生成交付消息...")
    if args.audit_result and os.path.exists(args.audit_result):
        msg = generate_summary_from_audit(
            args.audit_result, len(REQUIRED_FILES), len(uploaded), doc_url
        )
        
        # Save to file
        msg_path = os.path.join(args.output_dir, "delivery_message.md")
        with open(msg_path, "w", encoding="utf-8") as f:
            f.write(msg)
        
        print(f"  ✅ 交付消息已保存: {msg_path}")
        print("\n" + "=" * 60)
        print("📨 交付消息内容（请复制到飞书发送）：")
        print("=" * 60)
        print(msg)
        print("=" * 60)
        
        # Also output JSON for programmatic use
        delivery_json = {
            "ok": True,
            "total_files": len(REQUIRED_FILES),
            "uploaded_count": len(uploaded),
            "doc_url": doc_url,
            "uploaded_files": uploaded,
            "delivery_message_path": msg_path,
            "delivery_message": msg,
        }
        
        json_path = os.path.join(args.output_dir, "delivery_result.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(delivery_json, f, ensure_ascii=False, indent=2)
        print(f"\n  ✅ 交付结果 JSON: {json_path}")
    else:
        print("  ⚠️ 审核结果文件不存在，跳过消息生成")


if __name__ == "__main__":
    main()
