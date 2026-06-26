#!/usr/bin/env python3
"""
导出错题本
支持格式: Markdown, HTML, JSON, PDF(需安装weasyprint)
"""

import json
from datetime import datetime
from pathlib import Path
import os

DATA_DIR = Path(os.environ.get('WORKSPACE', '.')) / 'mistake-data'
OUTPUT_DIR = Path(os.environ.get('WORKSPACE', '.')) / 'mistake-exports'


def load_json(filepath):
    """加载JSON文件"""
    if not filepath.exists():
        return None
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_all_mistakes() -> list:
    """获取所有错题"""
    mistakes = []
    
    if not DATA_DIR.exists():
        return mistakes
    
    for subject_dir in DATA_DIR.iterdir():
        if subject_dir.is_dir() and subject_dir.name not in ['.', '..']:
            for topic_file in subject_dir.glob('*.json'):
                data = load_json(topic_file)
                if data:
                    mistakes.extend(data.get('mistakes', []))
    
    return mistakes


def filter_mistakes(mistakes: list, subject: str = None, 
                    topic: str = None, days: int = None) -> list:
    """筛选错题"""
    filtered = mistakes.copy()
    
    if subject:
        filtered = [m for m in filtered if m.get('subject') == subject]
    
    if topic:
        filtered = [m for m in filtered if m.get('topic') == topic]
    
    if days:
        cutoff = datetime.now() - __import__('datetime').timedelta(days=days)
        filtered = [
            m for m in filtered 
            if datetime.fromisoformat(m.get('created_at', '')) >= cutoff
        ]
    
    return filtered


def export_markdown(mistakes: list, title: str = "我的错题本") -> str:
    """导出为Markdown格式"""
    lines = [
        f"# {title}\n",
        f"导出时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n",
        f"总数: {len(mistakes)}题\n",
        "---\n"
    ]
    
    # 按科目分组
    by_subject = {}
    for m in mistakes:
        subject = m.get('subject', '未分类')
        if subject not in by_subject:
            by_subject[subject] = []
        by_subject[subject].append(m)
    
    for subject, items in sorted(by_subject.items()):
        lines.append(f"\n## {subject}\n")
        
        for i, m in enumerate(items, 1):
            topic = m.get('topic', '未分类')
            difficulty = m.get('difficulty', '中等')
            
            lines.append(f"### {i}. [{topic}] {m.get('question_type', '题目')}\n")
            lines.append(f"**难度**: {difficulty}\n")
            lines.append(f"**题目**: {m.get('question')}\n")
            
            if m.get('options'):
                lines.append("**选项**:")
                for key, val in m['options'].items():
                    lines.append(f"- {key}. {val}")
                lines.append("")
            
            lines.append(f"**错误答案**: {m.get('wrong_answer')}\n")
            lines.append(f"**正确答案**: {m.get('correct_answer')}\n")
            lines.append(f"**错误原因**: {m.get('reason')}\n")
            
            if m.get('notes'):
                lines.append(f"**备注**: {m['notes']}\n")
            
            lines.append("---\n")
    
    return '\n'.join(lines)


def export_html(mistakes: list, title: str = "我的错题本") -> str:
    """导出为HTML格式"""
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }}
        .header {{
            text-align: center;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 10px;
            margin-bottom: 20px;
        }}
        .subject {{
            background: white;
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .subject h2 {{
            color: #667eea;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }}
        .mistake {{
            background: #fafafa;
            padding: 15px;
            margin: 10px 0;
            border-left: 4px solid #764ba2;
            border-radius: 5px;
        }}
        .question {{
            font-size: 1.1em;
            font-weight: bold;
            color: #333;
        }}
        .wrong {{
            color: #e74c3c;
            background: #ffe6e6;
            padding: 5px 10px;
            border-radius: 3px;
        }}
        .correct {{
            color: #27ae60;
            background: #e6ffe6;
            padding: 5px 10px;
            border-radius: 3px;
        }}
        .meta {{
            font-size: 0.9em;
            color: #888;
            margin-top: 10px;
        }}
        .tag {{
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 2px 8px;
            border-radius: 3px;
            font-size: 0.8em;
            margin-right: 5px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>{title}</h1>
        <p>导出时间: {datetime.now().strftime('%Y-%m-%d %H:%M')} | 共 {len(mistakes)} 题</p>
    </div>
"""
    
    # 按科目分组
    by_subject = {}
    for m in mistakes:
        subject = m.get('subject', '未分类')
        if subject not in by_subject:
            by_subject[subject] = []
        by_subject[subject].append(m)
    
    for subject, items in sorted(by_subject.items()):
        html += f'    <div class="subject">\n        <h2>{subject}</h2>\n'
        
        for m in items:
            html += f"""
        <div class="mistake">
            <div class="question">{m.get('question', '')}</div>
            <p><strong>错误答案:</strong> <span class="wrong">{m.get('wrong_answer', '')}</span></p>
            <p><strong>正确答案:</strong> <span class="correct">{m.get('correct_answer', '')}</span></p>
            <p><strong>错误原因:</strong> {m.get('reason', '')}</p>
            <div class="meta">
                <span class="tag">{m.get('topic', '未分类')}</span>
                <span class="tag">{m.get('difficulty', '中等')}</span>
            </div>
        </div>
"""
        
        html += '    </div>\n'
    
    html += '</body>\n</html>'
    
    return html


def export_json(mistakes: list) -> str:
    """导出为JSON格式（备份用）"""
    return json.dumps({
        'exported_at': datetime.now().isoformat(),
        'total': len(mistakes),
        'mistakes': mistakes
    }, ensure_ascii=False, indent=2)


def export_mistakes(
    format: str = 'markdown',
    subject: str = None,
    topic: str = None,
    days: int = None,
    output_file: str = None
) -> str:
    """
    导出错题
    
    Args:
        format: 导出格式 (markdown/html/json)
        subject: 筛选科目
        topic: 筛选知识点
        days: 筛选最近N天
        output_file: 输出文件路径
    
    Returns:
        导出内容或文件路径
    """
    mistakes = get_all_mistakes()
    mistakes = filter_mistakes(mistakes, subject, topic, days)
    
    if not mistakes:
        return "没有找到符合条件的错题"
    
    # 根据格式导出
    format = format.lower()
    
    if format == 'markdown' or format == 'md':
        content = export_markdown(mistakes)
        ext = '.md'
    elif format == 'html':
        content = export_html(mistakes)
        ext = '.html'
    elif format == 'json':
        content = export_json(mistakes)
        ext = '.json'
    else:
        return f"不支持的格式: {format}"
    
    # 保存到文件
    if output_file:
        output_path = Path(output_file)
    else:
        OUTPUT_DIR.mkdir(exist_ok=True, parents=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = OUTPUT_DIR / f"mistakes_{timestamp}{ext}"
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return f"✅ 已导出到: {output_path}"


def main():
    """测试"""
    # 测试各种导出格式
    print(export_mistakes(format='markdown'))
    print()
    print(export_mistakes(format='html'))
    print()
    print(export_mistakes(format='json'))


if __name__ == '__main__':
    main()
