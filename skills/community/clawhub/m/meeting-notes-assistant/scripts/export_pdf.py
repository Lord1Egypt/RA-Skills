#!/usr/bin/env python3
"""
导出 PDF 会议纪要
适合快速分享，无需复杂排版
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime


def normalize_title(meeting_info):
    return meeting_info.get("title") or meeting_info.get("theme") or "会议纪要"


def normalize_item(item):
    if isinstance(item, dict):
        return {
            "task": str(item.get("task") or item.get("content") or "").strip(),
            "owner": str(item.get("owner") or item.get("assignee") or "").strip(),
            "due": str(item.get("due") or item.get("deadline") or "").strip(),
        }
    return {"task": str(item).strip(), "owner": "", "due": ""}


def normalize_todos(notes):
    return [normalize_item(todo) for todo in notes.get("todos", [])]


def normalize_action_items(notes):
    return [normalize_item(item) for item in notes.get("action_items", [])]


def find_cjk_font() -> str | None:
    candidates = [
        Path(r"C:\Windows\Fonts\simhei.ttf"),
        Path(r"C:\Windows\Fonts\msyh.ttc"),
        Path(r"C:\Windows\Fonts\simsun.ttc"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return str(candidate)
    return None


def notes_to_html(notes):
    """
    将结构化纪要转换为 HTML（用于 PDF 生成）
    """
    meeting_info = notes.get("meeting_info", {})
    title_text = normalize_title(meeting_info)
    topics = notes.get("topics", [])
    todos = normalize_todos(notes)
    keywords = notes.get("keywords", [])
    action_items = normalize_action_items(notes)
    
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>会议纪要 - {title_text}</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Microsoft YaHei", sans-serif; margin: 40px; line-height: 1.6; }}
        h1 {{ color: #333; border-bottom: 2px solid #4A90D9; padding-bottom: 10px; }}
        h2 {{ color: #555; margin-top: 30px; }}
        .meta {{ color: #666; margin-bottom: 20px; }}
        .meta-item {{ margin: 5px 0; }}
        .topic {{ background: #f8f9fa; padding: 15px; margin: 10px 0; border-radius: 5px; }}
        .topic-title {{ font-weight: bold; color: #333; }}
        .topic-conclusion {{ color: #4A90D9; margin-top: 5px; }}
        .todo-item {{ padding: 8px 0; border-bottom: 1px solid #eee; }}
        .todo-owner {{ color: #e67e22; font-weight: bold; }}
        .keyword {{ display: inline-block; background: #e8f4fd; padding: 3px 10px; margin: 3px; border-radius: 15px; font-size: 14px; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 15px; }}
        th, td {{ border: 1px solid #ddd; padding: 10px; text-align: left; }}
        th {{ background: #4A90D9; color: white; }}
        tr:nth-child(even) {{ background: #f9f9f9; }}
        .footer {{ margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd; color: #999; font-size: 12px; }}
    </style>
</head>
<body>
    <h1>📋 {title_text}</h1>
    
    <div class="meta">
        <div class="meta-item">📅 时间：{meeting_info.get("time", "未指定")}</div>
        <div class="meta-item">👥 参会人：{meeting_info.get("attendees", "未指定")}</div>
    </div>
"""
    
    # 议题与结论
    if topics:
        html += "<h2>📝 议题与结论</h2>\n"
        for topic in topics:
            html += f"""    <div class="topic">
        <div class="topic-title">▪ {topic.get("title", "")}</div>
        <div class="topic-conclusion">{topic.get("conclusion", "")}</div>
    </div>
"""
    
    # 待办事项
    if todos:
        html += "<h2>✅ 待办事项</h2>\n"
        for todo in todos:
            owner = todo.get("owner", "")
            due = todo.get("due", "")
            task = todo.get("task", str(todo))
            html += f"""    <div class="todo-item">
        ☐ {task} <span class="todo-owner">{f"(@{owner})" if owner else ""} {f"[{due}]" if due else ""}</span>
    </div>
"""
    
    # Action Items
    if action_items:
        html += """<h2>🎯 Action Items</h2>
    <table>
        <tr><th>任务</th><th>负责人</th><th>截止时间</th></tr>
"""
        for item in action_items:
            html += f"""        <tr>
            <td>{item.get("task", "")}</td>
            <td>{item.get("owner", "-")}</td>
            <td>{item.get("due", "-")}</td>
        </tr>
"""
        html += "    </table>\n"
    
    # 关键词
    if keywords:
        html += "<h2>🏷️ 关键词</h2>\n"
        for kw in keywords:
            html += f'    <span class="keyword">{kw}</span>\n'
    
    # 页脚
    html += f"""
    <div class="footer">
        <p>生成时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
        <p>会议纪要智能助手</p>
    </div>
</body>
</html>"""
    
    return html


def export_with_weasyprint(html_content, pdf_path):
    from weasyprint import HTML

    HTML(string=html_content).write_pdf(pdf_path)
    print(f"PDF 已导出: {pdf_path}")
    return str(pdf_path)


def export_with_reportlab(notes, pdf_path):
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.utils import simpleSplit
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.pdfgen import canvas

    meeting_info = notes.get("meeting_info", {})
    title_text = normalize_title(meeting_info)
    topics = notes.get("topics", [])
    todos = normalize_todos(notes)
    keywords = notes.get("keywords", [])
    action_items = normalize_action_items(notes)
    font_path = find_cjk_font()
    if not font_path:
        raise RuntimeError("No CJK font found for reportlab")

    pdfmetrics.registerFont(TTFont("CJK", font_path))
    page_width, page_height = A4
    left_margin = 48
    right_margin = 48
    top_margin = 56
    bottom_margin = 48
    content_width = page_width - left_margin - right_margin
    pdf = canvas.Canvas(str(pdf_path), pagesize=A4)
    pdf.setTitle(title_text)
    y = page_height - top_margin

    def ensure_space(line_height: int = 18):
        nonlocal y
        if y < bottom_margin + line_height:
            pdf.showPage()
            pdf.setFont("CJK", 11)
            y = page_height - top_margin

    def draw_lines(text: str, font_size: int = 11, leading: int = 18):
        nonlocal y
        lines = simpleSplit(text, "CJK", font_size, content_width) or [""]
        pdf.setFont("CJK", font_size)
        for line in lines:
            ensure_space(leading)
            pdf.drawString(left_margin, y, line)
            y -= leading

    draw_lines(title_text, font_size=16, leading=22)
    y -= 4
    draw_lines(f"时间：{meeting_info.get('time', '未指定')}")
    draw_lines(f"参会人：{meeting_info.get('attendees', '未指定')}")

    if topics:
        y -= 4
        draw_lines("议题与结论", font_size=13, leading=20)
        for topic in topics:
            draw_lines(f"- {topic.get('title', '')}")
            if topic.get("conclusion"):
                draw_lines(f"  结论：{topic.get('conclusion', '')}")

    if todos:
        y -= 4
        draw_lines("待办事项", font_size=13, leading=20)
        for todo in todos:
            suffix = []
            if todo.get("owner"):
                suffix.append(f"负责人：{todo['owner']}")
            if todo.get("due"):
                suffix.append(f"截止：{todo['due']}")
            extra = f"（{'；'.join(suffix)}）" if suffix else ""
            draw_lines(f"- {todo.get('task', '')}{extra}")

    if action_items:
        y -= 4
        draw_lines("Action Items", font_size=13, leading=20)
        for item in action_items:
            suffix = []
            if item.get("owner"):
                suffix.append(f"负责人：{item['owner']}")
            if item.get("due"):
                suffix.append(f"截止：{item['due']}")
            extra = f"（{'；'.join(suffix)}）" if suffix else ""
            draw_lines(f"- {item.get('task', '')}{extra}")

    if keywords:
        y -= 4
        draw_lines("关键词", font_size=13, leading=20)
        draw_lines("、".join(keywords))

    pdf.save()
    print(f"PDF 已导出: {pdf_path}")
    return str(pdf_path)


def export_with_fpdf2(notes, pdf_path):
    from fpdf import FPDF

    meeting_info = notes.get("meeting_info", {})
    title_text = normalize_title(meeting_info)
    topics = notes.get("topics", [])
    todos = normalize_todos(notes)
    keywords = notes.get("keywords", [])
    action_items = normalize_action_items(notes)
    font_path = find_cjk_font()
    if not font_path:
        raise RuntimeError("No CJK font found for fpdf2")

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.add_font("CJK", style="", fname=font_path)
    pdf.set_font("CJK", size=16)
    pdf.multi_cell(0, 10, title_text, align="C")

    pdf.ln(2)
    pdf.set_font("CJK", size=11)
    pdf.multi_cell(0, 8, f"时间：{meeting_info.get('time', '未指定')}")
    pdf.multi_cell(0, 8, f"参会人：{meeting_info.get('attendees', '未指定')}")

    if topics:
        pdf.ln(2)
        pdf.set_font("CJK", size=13)
        pdf.cell(0, 8, "议题与结论", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("CJK", size=11)
        for topic in topics:
            pdf.multi_cell(0, 8, f"- {topic.get('title', '')}")
            if topic.get("conclusion"):
                pdf.multi_cell(0, 8, f"  结论：{topic.get('conclusion', '')}")

    if todos:
        pdf.ln(2)
        pdf.set_font("CJK", size=13)
        pdf.cell(0, 8, "待办事项", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("CJK", size=11)
        for todo in todos:
            suffix = []
            if todo.get("owner"):
                suffix.append(f"负责人：{todo['owner']}")
            if todo.get("due"):
                suffix.append(f"截止：{todo['due']}")
            extra = f"（{'；'.join(suffix)}）" if suffix else ""
            pdf.multi_cell(0, 8, f"- {todo.get('task', '')}{extra}")

    if action_items:
        pdf.ln(2)
        pdf.set_font("CJK", size=13)
        pdf.cell(0, 8, "Action Items", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("CJK", size=11)
        for item in action_items:
            suffix = []
            if item.get("owner"):
                suffix.append(f"负责人：{item['owner']}")
            if item.get("due"):
                suffix.append(f"截止：{item['due']}")
            extra = f"（{'；'.join(suffix)}）" if suffix else ""
            pdf.multi_cell(0, 8, f"- {item.get('task', '')}{extra}")

    if keywords:
        pdf.ln(2)
        pdf.set_font("CJK", size=13)
        pdf.cell(0, 8, "关键词", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("CJK", size=11)
        pdf.multi_cell(0, 8, "、".join(keywords))

    pdf.output(str(pdf_path))
    print(f"PDF 已导出: {pdf_path}")
    return str(pdf_path)


def export_as_html(html_content, pdf_path):
    html_path = pdf_path.with_suffix(".html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"警告：未安装可用 PDF 引擎，已导出 HTML: {html_path}")
    print("提示：安装以下任一库以支持 PDF 导出：")
    if sys.platform == "win32":
        print("   - pip install reportlab")
        print("   - pip install fpdf2")
    else:
        print("   - pip install weasyprint")
        print("   - pip install reportlab")
        print("   - pip install fpdf2")
    return str(html_path)


def preferred_pdf_engines():
    if sys.platform == "win32":
        return ["reportlab", "fpdf2", "html"]
    return ["weasyprint", "reportlab", "fpdf2", "html"]


def export_pdf(notes_json_path, output_path):
    """
    导出 PDF

    Args:
        notes_json_path: 会议纪要 JSON 文件路径
        output_path: 输出 PDF 路径
    """
    with open(notes_json_path, "r", encoding="utf-8") as f:
        notes = json.load(f)

    html_content = notes_to_html(notes)
    pdf_path = Path(output_path)

    for engine in preferred_pdf_engines():
        if engine == "weasyprint":
            try:
                return export_with_weasyprint(html_content, pdf_path)
            except Exception as e:
                print(f"提示：weasyprint 不可用，将尝试其他 PDF 引擎。原因: {e}")
        elif engine == "reportlab":
            try:
                return export_with_reportlab(notes, pdf_path)
            except Exception as e:
                print(f"提示：reportlab 导出失败，将尝试其他 PDF 引擎。原因: {e}")
        elif engine == "fpdf2":
            try:
                return export_with_fpdf2(notes, pdf_path)
            except ImportError:
                print("提示：fpdf2 未安装，将尝试其他 PDF 引擎。")
            except Exception as e:
                print(f"提示：fpdf2 导出失败，将尝试其他 PDF 引擎。原因: {e}")
        elif engine == "html":
            return export_as_html(html_content, pdf_path)

    return export_as_html(html_content, pdf_path)


def main():
    parser = argparse.ArgumentParser(description="导出 PDF 会议纪要")
    parser.add_argument("notes_json", help="会议纪要 JSON 文件路径")
    parser.add_argument("--output", "-o", required=True, help="输出 PDF 路径")
    
    args = parser.parse_args()
    
    # 检查文件存在
    if not Path(args.notes_json).exists():
        print(f"错误：文件不存在: {args.notes_json}")
        sys.exit(1)
    
    # 导出
    export_pdf(args.notes_json, args.output)


if __name__ == "__main__":
    main()