#!/usr/bin/env python3
"""
生成项目报告
用法: python3 generate_report.py <project-id> --type [weekly|monthly|milestone]
"""

import json
import sys
import argparse
from datetime import datetime, timedelta
from pathlib import Path

def generate_report(project_id, report_type="weekly"):
    """生成项目报告"""
    
    project_file = Path("projects") / f"{project_id}.json"
    
    if not project_file.exists():
        print(f"❌ 项目不存在: {project_id}")
        return None
    
    with open(project_file, 'r', encoding='utf-8') as f:
        project = json.load(f)
    
    now = datetime.now()
    report_date = now.strftime("%Y-%m-%d")
    
    # 报告标题
    type_names = {
        "weekly": "周报",
        "monthly": "月报",
        "milestone": "里程碑报告",
        "status": "状态报告"
    }
    report_title = f"{project['name']} - {type_names.get(report_type, '项目报告')}"
    
    # 计算统计数据
    tasks = project.get("tasks", [])
    total_tasks = len(tasks)
    completed_tasks = len([t for t in tasks if t.get("status") == "已完成"])
    in_progress_tasks = len([t for t in tasks if t.get("status") == "进行中"])
    blocked_tasks = len([t for t in tasks if t.get("status") == "已阻塞"])
    
    overall_progress = sum(t.get("progress", 0) for t in tasks) / total_tasks if total_tasks > 0 else 0
    
    # 生成报告内容
    report_lines = [
        f"# {report_title}",
        f"",
        f"**报告日期**: {report_date}",
        f"**项目状态**: {project.get('status', 'N/A')}",
        f"**整体进度**: {overall_progress:.1f}%",
        f"",
        f"---",
        f"",
        f"## 📊 执行摘要",
        f"",
        f"| 指标 | 数值 |",
        f"|------|------|",
        f"| 总任务数 | {total_tasks} |",
        f"| 已完成 | {completed_tasks} |",
        f"| 进行中 | {in_progress_tasks} |",
        f"| 已阻塞 | {blocked_tasks} |",
        f"| 完成率 | {completed_tasks/total_tasks*100:.1f}% |" if total_tasks > 0 else "| 完成率 | N/A |",
        f"",
        f"---",
        f"",
        f"## 🎯 里程碑进展",
        f""
    ]
    
    milestones = project.get("milestones", [])
    if milestones:
        for ms in milestones:
            status_icon = "✅" if ms.get("status") == "已完成" else "🔄" if ms.get("status") == "进行中" else "⏳"
            report_lines.append(f"- {status_icon} **{ms['name']}** - {ms.get('status', 'N/A')} (计划: {ms.get('date', '未设置')})")
    else:
        report_lines.append("暂无里程碑")
    
    report_lines.extend([
        f"",
        f"---",
        f"",
        f"## 📋 任务详情",
        f""
    ])
    
    # 按状态分组任务
    if tasks:
        status_order = ["进行中", "已阻塞", "待开始", "已完成"]
        for status in status_order:
            status_tasks = [t for t in tasks if t.get("status") == status]
            if status_tasks:
                report_lines.append(f"### {status} ({len(status_tasks)}个)")
                report_lines.append("")
                for t in status_tasks:
                    assignee = f" @{t.get('assignee')}" if t.get('assignee') else ""
                    progress_bar = "█" * (t.get("progress", 0) // 10) + "░" * (10 - t.get("progress", 0) // 10)
                    report_lines.append(f"- **{t['name']}**{assignee} - {progress_bar} {t.get('progress', 0)}%")
                    if t.get("blockers"):
                        report_lines.append(f"  ⚠️ 阻塞: {', '.join(t['blockers'])}")
                report_lines.append("")
    else:
        report_lines.append("暂无任务")
    
    # KPI部分
    report_lines.extend([
        f"---",
        f"",
        f"## 📈 KPI指标",
        f""
    ])
    
    kpis = project.get("kpis", [])
    if kpis:
        report_lines.append("| 指标 | 目标 | 当前 | 状态 |")
        report_lines.append("|------|------|------|------|")
        for kpi in kpis:
            report_lines.append(f"| {kpi['name']} | {kpi.get('target', 'N/A')} | {kpi.get('current', 'N/A')} | {kpi.get('status', 'N/A')} |")
    else:
        report_lines.append("暂无KPI指标")
    
    # 风险与问题
    report_lines.extend([
        f"",
        f"---",
        f"",
        f"## ⚠️ 风险与问题",
        f""
    ])
    
    blocked = [t for t in tasks if t.get("status") == "已阻塞"]
    if blocked:
        report_lines.append("### 当前阻塞项")
        report_lines.append("")
        for t in blocked:
            report_lines.append(f"- **{t['name']}**: {', '.join(t.get('blockers', ['未说明']))}")
    else:
        report_lines.append("暂无阻塞问题")
    
    # 下周/下阶段计划
    report_lines.extend([
        f"",
        f"---",
        f"",
        f"## 📝 下阶段计划",
        f"",
        "_（请在此处补充下阶段计划）_",
        f"",
        f"---",
        f"",
        f"*报告生成时间: {now.strftime("%Y-%m-%d %H:%M:%S")}*"
    ])
    
    report_content = "\n".join(report_lines)
    
    # 保存报告
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)
    
    report_filename = f"{project_id}-{report_date}-{report_type}.md"
    report_path = reports_dir / report_filename
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    # 更新项目报告记录
    project["reports"].append({
        "type": report_type,
        "date": report_date,
        "file": str(report_path)
    })
    
    with open(project_file, 'w', encoding='utf-8') as f:
        json.dump(project, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 报告生成成功!")
    print(f"   类型: {type_names.get(report_type, report_type)}")
    print(f"   文件: {report_path}")
    
    return report_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="生成项目报告")
    parser.add_argument("project_id", help="项目ID")
    parser.add_argument("--type", "-t", default="weekly",
                        choices=["weekly", "monthly", "milestone", "status"],
                        help="报告类型")
    
    args = parser.parse_args()
    
    generate_report(args.project_id, args.type)
