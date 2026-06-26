#!/usr/bin/env python3
"""
生成项目看板
用法: python3 generate_board.py <project-id> --format [markdown|html]
"""

import json
import sys
import argparse
from datetime import datetime
from pathlib import Path

def generate_board(project_id, format_type="markdown"):
    """生成项目看板"""
    
    project_file = Path("projects") / f"{project_id}.json"
    
    if not project_file.exists():
        print(f"❌ 项目不存在: {project_id}")
        return None
    
    with open(project_file, 'r', encoding='utf-8') as f:
        project = json.load(f)
    
    tasks = project.get("tasks", [])
    
    if format_type == "markdown":
        return generate_markdown_board(project, tasks)
    elif format_type == "html":
        return generate_html_board(project, tasks)
    else:
        print(f"❌ 不支持的格式: {format_type}")
        return None

def generate_markdown_board(project, tasks):
    """生成Markdown格式看板"""
    
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    lines = [
        f"# 📊 {project['name']} - 项目看板",
        f"",
        f"*更新时间: {now}*",
        f"",
        f"## 整体进度",
        f""
    ]
    
    # 整体进度
    if tasks:
        overall = sum(t.get("progress", 0) for t in tasks) / len(tasks)
        filled = int(overall / 5)
        bar = "█" * filled + "░" * (20 - filled)
        lines.append(f"**{bar} {overall:.1f}%**")
        lines.append("")
        
        # 按状态统计
        status_counts = {}
        for t in tasks:
            status = t.get("status", "未设置")
            status_counts[status] = status_counts.get(status, 0) + 1
        
        lines.append("| 状态 | 数量 |")
        lines.append("|------|------|")
        for status, count in status_counts.items():
            lines.append(f"| {status} | {count} |")
        lines.append("")
    
    # 看板列
    lines.extend([
        f"---",
        f"",
        f"## 任务看板",
        f""
    ])
    
    columns = {
        "待开始": [],
        "进行中": [],
        "已阻塞": [],
        "已完成": []
    }
    
    for t in tasks:
        status = t.get("status", "待开始")
        if status in columns:
            columns[status].append(t)
    
    # 生成看板表格
    lines.append("| 待开始 ⏳ | 进行中 🔄 | 已阻塞 ⚠️ | 已完成 ✅ |")
    lines.append("|-----------|-----------|-----------|-----------|")
    
    max_rows = max(len(columns[s]) for s in columns)
    
    for i in range(max_rows):
        row = []
        for status in ["待开始", "进行中", "已阻塞", "已完成"]:
            if i < len(columns[status]):
                t = columns[status][i]
                assignee = f"@{t.get('assignee')}" if t.get('assignee') else "未分配"
                progress = f" {t.get('progress', 0)}%" if status == "进行中" else ""
                cell = f"**{t['name']}**<br>{assignee}{progress}"
            else:
                cell = ""
            row.append(cell)
        lines.append(f"| {row[0]} | {row[1]} | {row[2]} | {row[3]} |")
    
    lines.append("")
    
    # 详细任务列表
    lines.extend([
        f"---",
        f"",
        f"## 任务列表",
        f"",
        f"| 任务 | 部门 | 负责人 | 进度 | 截止日期 |",
        f"|------|------|--------|------|----------|"
    ])
    
    for t in tasks:
        dept = t.get('departmentId', 'N/A')[:8]
        assignee = t.get('assignee', '未分配')
        progress = f"{t.get('progress', 0)}%"
        due = t.get('endDate', '未设置')
        status_icon = {"已完成": "✅", "进行中": "🔄", "已阻塞": "⚠️", "待开始": "⏳"}.get(t.get('status'), "⏳")
        lines.append(f"| {status_icon} {t['name']} | {dept}... | {assignee} | {progress} | {due} |")
    
    content = "\n".join(lines)
    
    # 保存文件
    boards_dir = Path("boards")
    boards_dir.mkdir(exist_ok=True)
    
    board_path = boards_dir / f"{project['id']}-board.md"
    with open(board_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ 看板生成成功!")
    print(f"   格式: Markdown")
    print(f"   文件: {board_path}")
    
    return board_path

def generate_html_board(project, tasks):
    """生成HTML格式看板"""
    
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # 计算统计数据
    overall = sum(t.get("progress", 0) for t in tasks) / len(tasks) if tasks else 0
    
    columns = {"待开始": [], "进行中": [], "已阻塞": [], "已完成": []}
    for t in tasks:
        status = t.get("status", "待开始")
        if status in columns:
            columns[status].append(t)
    
    html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{project['name']} - 项目看板</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; margin: 20px; background: #f5f5f5; }}
        .header {{ background: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .header h1 {{ margin: 0 0 10px 0; color: #333; }}
        .progress-bar {{ width: 100%; height: 20px; background: #e0e0e0; border-radius: 10px; overflow: hidden; }}
        .progress-fill {{ height: 100%; background: linear-gradient(90deg, #4CAF50, #8BC34A); transition: width 0.3s; }}
        .board {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; }}
        .column {{ background: white; border-radius: 8px; padding: 15px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .column-header {{ font-weight: bold; padding: 10px; margin: -15px -15px 15px -15px; border-radius: 8px 8px 0 0; color: white; }}
        .todo .column-header {{ background: #9E9E9E; }}
        .progress .column-header {{ background: #2196F3; }}
        .blocked .column-header {{ background: #f44336; }}
        .done .column-header {{ background: #4CAF50; }}
        .task {{ background: #f8f9fa; padding: 10px; margin-bottom: 10px; border-radius: 4px; border-left: 3px solid #ddd; }}
        .task:hover {{ box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
        .task-title {{ font-weight: 500; margin-bottom: 5px; }}
        .task-meta {{ font-size: 12px; color: #666; }}
        .task-progress {{ margin-top: 5px; height: 4px; background: #e0e0e0; border-radius: 2px; }}
        .task-progress-bar {{ height: 100%; background: #4CAF50; border-radius: 2px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 {project['name']}</h1>
        <p>更新时间: {now} | 整体进度: {overall:.1f}%</p>
        <div class="progress-bar">
            <div class="progress-fill" style="width: {overall}%"></div>
        </div>
    </div>
    
    <div class="board">
        <div class="column todo">
            <div class="column-header">⏳ 待开始 ({len(columns['待开始'])})</div>
            {''.join([f"""
            <div class="task">
                <div class="task-title">{t['name']}</div>
                <div class="task-meta">负责人: {t.get('assignee', '未分配')} | 截止: {t.get('endDate', '未设置')}</div>
            </div>
            """ for t in columns['待开始']])}
        </div>
        
        <div class="column progress">
            <div class="column-header">🔄 进行中 ({len(columns['进行中'])})</div>
            {''.join([f"""
            <div class="task">
                <div class="task-title">{t['name']}</div>
                <div class="task-meta">负责人: {t.get('assignee', '未分配')}</div>
                <div class="task-progress">
                    <div class="task-progress-bar" style="width: {t.get('progress', 0)}%"></div>
                </div>
                <div class="task-meta">{t.get('progress', 0)}%</div>
            </div>
            """ for t in columns['进行中']])}
        </div>
        
        <div class="column blocked">
            <div class="column-header">⚠️ 已阻塞 ({len(columns['已阻塞'])})</div>
            {''.join([f"""
            <div class="task">
                <div class="task-title">{t['name']}</div>
                <div class="task-meta">负责人: {t.get('assignee', '未分配')}</div>
                <div class="task-meta" style="color: #f44336;">阻塞: {', '.join(t.get('blockers', []))}</div>
            </div>
            """ for t in columns['已阻塞']])}
        </div>
        
        <div class="column done">
            <div class="column-header">✅ 已完成 ({len(columns['已完成'])})</div>
            {''.join([f"""
            <div class="task">
                <div class="task-title">{t['name']}</div>
                <div class="task-meta">负责人: {t.get('assignee', '未分配')}</div>
            </div>
            """ for t in columns['已完成']])}
        </div>
    </div>
</body>
</html>'''
    
    # 保存文件
    boards_dir = Path("boards")
    boards_dir.mkdir(exist_ok=True)
    
    board_path = boards_dir / f"{project['id']}-board.html"
    with open(board_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ 看板生成成功!")
    print(f"   格式: HTML")
    print(f"   文件: {board_path}")
    
    return board_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="生成项目看板")
    parser.add_argument("project_id", help="项目ID")
    parser.add_argument("--format", "-f", default="markdown",
                        choices=["markdown", "html"],
                        help="输出格式")
    
    args = parser.parse_args()
    
    generate_board(args.project_id, args.format)
