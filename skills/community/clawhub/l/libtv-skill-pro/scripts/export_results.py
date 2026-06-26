#!/usr/bin/env python3
"""
结果导出脚本 - 导出会话中的所有结果
"""

import argparse
import json
import sys
import os
import re
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))
from _common import query_session, safe_run


def extract_urls(text: str) -> list:
    """从文本中提取 URL"""
    url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
    return re.findall(url_pattern, text)


def extract_image_urls(text: str) -> list:
    """提取图片 URL"""
    urls = extract_urls(text)
    return [u for u in urls if any(ext in u.lower() for ext in ['.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp'])]


def extract_video_urls(text: str) -> list:
    """提取视频 URL"""
    urls = extract_urls(text)
    return [u for u in urls if any(ext in u.lower() for ext in ['.mp4', '.mov', '.avi', '.webm', '.mkv'])]


def export_session(session_id: str, format_type: str = "json") -> dict:
    """导出会话内容"""
    print(f"[*] 导出会话: {session_id}")
    
    result = query_session(session_id=session_id)
    messages = result.get("messages", [])
    
    if not messages:
        return {"error": "会话为空"}
    
    # 分析消息
    user_messages = [m for m in messages if m.get("role") == "user"]
    assistant_messages = [m for m in messages if m.get("role") == "assistant"]
    
    all_urls = []
    image_urls = []
    video_urls = []
    
    for msg in messages:
        content = msg.get("content", "")
        all_urls.extend(extract_urls(content))
        image_urls.extend(extract_image_urls(content))
        video_urls.extend(extract_video_urls(content))
    
    export_data = {
        "session_id": session_id,
        "export_time": datetime.now().isoformat(),
        "total_messages": len(messages),
        "user_messages": len(user_messages),
        "assistant_messages": len(assistant_messages),
        "urls": {
            "all": list(set(all_urls)),
            "images": list(set(image_urls)),
            "videos": list(set(video_urls)),
        },
        "messages": messages,
    }
    
    return export_data


def format_markdown(data: dict) -> str:
    """格式化为 Markdown"""
    lines = [
        f"# 会话导出报告\n",
        f"**会话 ID**: {data['session_id']}\n",
        f"**导出时间**: {data['export_time']}\n",
        f"**消息总数**: {data['total_messages']}\n",
        "\n## 统计\n",
        f"- 用户消息: {data['user_messages']}",
        f"- 助手消息: {data['assistant_messages']}",
        f"- 总 URL 数: {len(data['urls']['all'])}",
        f"- 图片数: {len(data['urls']['images'])}",
        f"- 视频数: {len(data['urls']['videos'])}",
        "\n## URL 列表\n",
    ]
    
    if data['urls']['images']:
        lines.append("\n### 图片\n")
        for url in data['urls']['images']:
            lines.append(f"- {url}")
    
    if data['urls']['videos']:
        lines.append("\n### 视频\n")
        for url in data['urls']['videos']:
            lines.append(f"- {url}")
    
    lines.append("\n## 消息记录\n")
    for msg in data['messages']:
        role = msg.get("role", "unknown")
        content = msg.get("content", "")
        seq = msg.get("seq", 0)
        lines.append(f"\n### [{seq}] {role.upper()}\n")
        lines.append(f"{content}\n")
    
    return "\n".join(lines)


def format_html(data: dict) -> str:
    """格式化为 HTML"""
    html_parts = [
        "<!DOCTYPE html>",
        "<html>",
        "<head>",
        "<meta charset='utf-8'>",
        f"<title>会话导出 - {data['session_id'][:8]}</title>",
        "<style>",
        "body { font-family: sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; }",
        ".message { margin: 20px 0; padding: 15px; border-radius: 8px; }",
        ".user { background: #e3f2fd; }",
        ".assistant { background: #f3e5f5; }",
        ".meta { color: #666; font-size: 0.9em; margin-bottom: 10px; }",
        ".url-list { background: #f5f5f5; padding: 10px; border-radius: 4px; margin: 10px 0; }",
        "img, video { max-width: 300px; margin: 10px; border-radius: 4px; }",
        "</style>",
        "</head>",
        "<body>",
        f"<h1>会话导出报告</h1>",
        f"<p><strong>会话 ID:</strong> {data['session_id']}</p>",
        f"<p><strong>导出时间:</strong> {data['export_time']}</p>",
        f"<p><strong>消息总数:</strong> {data['total_messages']}</p>",
        "<h2>媒体文件</h2>",
    ]
    
    # 图片
    if data['urls']['images']:
        html_parts.append("<h3>图片</h3><div>")
        for url in data['urls']['images']:
            html_parts.append(f'<img src="{url}" loading="lazy">')
        html_parts.append("</div>")
    
    # 视频
    if data['urls']['videos']:
        html_parts.append("<h3>视频</h3><div>")
        for url in data['urls']['videos']:
            html_parts.append(f'<video src="{url}" controls preload="metadata"></video>')
        html_parts.append("</div>")
    
    # 消息
    html_parts.append("<h2>消息记录</h2>")
    for msg in data['messages']:
        role = msg.get("role", "unknown")
        content = msg.get("content", "")
        seq = msg.get("seq", 0)
        content_html = content.replace("\n", "<br>")
        
        html_parts.append(f'<div class="message {role}">')
        html_parts.append(f'<div class="meta">[{seq}] {role.upper()}</div>')
        html_parts.append(f'<div>{content_html}</div>')
        html_parts.append('</div>')
    
    html_parts.extend(["</body>", "</html>"])
    
    return "\n".join(html_parts)


def main():
    parser = argparse.ArgumentParser(
        description="导出会话结果",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
环境变量:
  LIBTV_ACCESS_KEY  必填，Bearer 鉴权

示例:
  # JSON 格式导出（默认）
  python3 export_results.py <session_id>

  # Markdown 格式
  python3 export_results.py <session_id> --format markdown

  # HTML 格式（包含图片预览）
  python3 export_results.py <session_id> --format html

  # 保存到文件
  python3 export_results.py <session_id> --output report.json

  # 只导出 URL 列表
  python3 export_results.py <session_id> --urls-only
        """,
    )
    parser.add_argument("session_id", help="会话 ID")
    parser.add_argument(
        "--format",
        choices=["json", "markdown", "html"],
        default="json",
        help="输出格式",
    )
    parser.add_argument(
        "--output",
        help="输出文件路径",
    )
    parser.add_argument(
        "--urls-only",
        action="store_true",
        help="只输出 URL 列表",
    )
    
    args = parser.parse_args()
    
    # 导出数据
    data = export_session(args.session_id, args.format)
    
    if "error" in data:
        print(f"错误: {data['error']}", file=sys.stderr)
        sys.exit(1)
    
    # 只输出 URL
    if args.urls_only:
        output = "\n".join(data['urls']['all'])
    else:
        # 根据格式转换
        if args.format == "json":
            output = json.dumps(data, ensure_ascii=False, indent=2)
        elif args.format == "markdown":
            output = format_markdown(data)
        elif args.format == "html":
            output = format_html(data)
    
    # 输出
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"[*] 已导出到: {args.output}")
        
        # 显示统计
        print(f"[*] 统计:")
        print(f"    消息总数: {data['total_messages']}")
        print(f"    URL 总数: {len(data['urls']['all'])}")
        print(f"    图片数: {len(data['urls']['images'])}")
        print(f"    视频数: {len(data['urls']['videos'])}")
    else:
        print(output)


if __name__ == "__main__":
    safe_run(main)
