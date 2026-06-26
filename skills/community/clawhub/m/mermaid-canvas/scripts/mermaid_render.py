#!/usr/bin/env python3
"""
mermaid_render.py — Mermaid Canvas 核心渲染脚本

将 Mermaid 代码渲染为 PNG 图片，使用浏览器 + Mermaid CDN 方案。

依赖：
    - OpenClaw browser 工具
    - feishu_doc_media 工具（可选，用于飞书上传）

用法：
    python mermaid_render.py --code "flowchart LR; A --> B" --output /tmp/output.png
    python mermaid_render.py --code-file diagram.mmd --output /tmp/output.png
    python mermaid_render.py --upload-feishu --doc-id "doc_id" --code "flowchart LR; A --> B"
"""

import argparse
import base64
import os
import tempfile
import time
import uuid
from pathlib import Path

# HTML 模板
HTML_TEMPLATE = '''<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <script src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"></script>
  <style>
    body {{
      margin: 20px;
      background: {background_color};
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }}
    pre.mermaid {{
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: {min_height}px;
      max-width: 100%;
      overflow: visible;
    }}
    .mermaid svg {{
      max-width: 100% !important;
      height: auto !important;
    }}
  </style>
</head>
<body>
  <pre class="mermaid">
{mermaid_code}
  </pre>
  <script>
    mermaid.initialize({{
      startOnLoad: true,
      theme: '{theme}',
      securityLevel: 'loose',
      fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
      flowchart: {{
        htmlLabels: true,
        curve: 'basis'
      }},
      sequence: {{
        actorMargin: 50,
        boxMargin: 10,
        boxTextMargin: 5,
        noteMargin: 10,
        messageMargin: 40
      }}
    }});
    
    // 等待 Mermaid 渲染完成
    async function waitForRender() {{
      return new Promise((resolve) => {{
        setTimeout(() => {{
          // 检查是否有 SVG 生成
          const svg = document.querySelector('.mermaid svg');
          if (svg) {{
            console.log('Mermaid SVG rendered successfully');
            resolve();
          }} else {{
            // 再等一会儿
            setTimeout(resolve, 1000);
          }}
        }}, 500);
      }});
    }}
    
    waitForRender().then(() => {{
      console.log('Ready for screenshot');
    }});
  </script>
</body>
</html>
'''


def escape_mermaid_code(code: str) -> str:
    """转义 Mermaid 代码，处理好缩进"""
    lines = code.strip().split('\n')
    # 保持缩进，但清理多余空白
    result = []
    for line in lines:
        result.append(line.rstrip())
    return '\n'.join(result)


def generate_html(mermaid_code: str, theme: str = "default", background_color: str = "white") -> str:
    """
    生成 Mermaid 渲染用的 HTML
    
    Args:
        mermaid_code: Mermaid 图表代码
        theme: 主题 (default/dark/base/wind)
        background_color: 背景色
    
    Returns:
        HTML 字符串
    """
    # 转义代码
    escaped_code = escape_mermaid_code(mermaid_code)
    
    # 估算最小高度
    line_count = len(escaped_code.split('\n'))
    min_height = max(300, line_count * 30)
    
    html = HTML_TEMPLATE.format(
        mermaid_code=escaped_code,
        theme=theme,
        background_color=background_color,
        min_height=min_height
    )
    
    return html


def save_html_to_temp(html: str) -> str:
    """
    保存 HTML 到临时文件
    
    Args:
        html: HTML 内容
    
    Returns:
        临时文件路径
    """
    # 创建临时目录
    temp_dir = tempfile.gettempdir()
    filename = f"mermaid_render_{uuid.uuid4().hex[:8]}.html"
    filepath = os.path.join(temp_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    
    return filepath


def render_with_mermaid_ink(mermaid_code: str) -> bytes:
    """
    降级方案：使用 mermaid.ink API 渲染
    
    Args:
        mermaid_code: Mermaid 图表代码
    
    Returns:
        PNG 图片数据
    """
    import urllib.request
    
    encoded = base64.urlsafe_b64encode(mermaid_code.encode('utf-8')).decode('ascii')
    url = f"https://mermaid.ink/img/{encoded}"
    
    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            return response.read()
    except Exception as e:
        raise RuntimeError(f"mermaid.ink API 调用失败: {e}")


def render_mermaid_to_png(
    mermaid_code: str,
    output_path: str = "/tmp/mermaid_output.png",
    theme: str = "default",
    background_color: str = "white",
    timeout: int = 30
) -> str:
    """
    将 Mermaid 代码渲染为 PNG 图片
    
    使用 browser 工具 + Mermaid CDN 在本地渲染。
    如果浏览器不可用，降级到 mermaid.ink API。
    
    Args:
        mermaid_code: Mermaid 图表代码
        output_path: 输出图片路径
        theme: Mermaid 主题 (default/dark/base/wind)
        background_color: 背景色
        timeout: 超时时间（秒）
    
    Returns:
        渲染后的图片路径
    """
    # 生成 HTML
    html = generate_html(mermaid_code, theme, background_color)
    
    # 保存到临时文件
    html_path = save_html_to_temp(html)
    
    # 确保输出目录存在
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    
    try:
        # 尝试使用 browser 工具渲染
        # 注意：这里需要通过 OpenClaw 的 browser 工具调用
        # 具体调用方式由调用方处理
        
        # 保存 HTML 路径供 browser 工具使用
        # 返回 HTML 路径，由调用方使用 browser navigate + snapshot
        return html_path
        
    except Exception as e:
        # 降级到 mermaid.ink
        print(f"Browser 渲染失败，降级到 mermaid.ink: {e}")
        png_data = render_with_mermaid_ink(mermaid_code)
        
        with open(output_path, 'wb') as f:
            f.write(png_data)
        
        return output_path


def validate_mermaid_code(mermaid_code: str) -> tuple[bool, str]:
    """
    验证 Mermaid 代码语法
    
    Args:
        mermaid_code: Mermaid 图表代码
    
    Returns:
        (是否有效, 错误信息)
    """
    # 基本检查
    if not mermaid_code or not mermaid_code.strip():
        return False, "Mermaid 代码为空"
    
    code = mermaid_code.strip()
    
    # 检查是否包含图表类型声明
    valid_types = [
        'flowchart', 'graph', 'sequenceDiagram', 'classDiagram',
        'stateDiagram', 'erDiagram', 'gantt', 'pie', 'mindmap',
        'timeline', 'journey', 'architecture', 'gitGraph',
        'quadrantChart', 'xyChart', 'requirementDiagram', 'c4Diagram',
        'radar', 'sankey', 'block', 'ishikawa', 'venn', 'treemap',
        'wardley', 'eventmodeling', 'kanban', 'packet', 'treeView'
    ]
    
    has_valid_type = any(code.startswith(t) or f'\n{t}' in code or f' {t}' in code 
                         for t in valid_types)
    
    if not has_valid_type:
        return False, "未识别图表类型，请确保代码以有效的 Mermaid 关键字开头"
    
    return True, ""


# 以下是命令行接口（供参考，实际使用通过 OpenClaw 工具调用）
def main():
    parser = argparse.ArgumentParser(description='Mermaid Canvas 渲染工具')
    parser.add_argument('--code', type=str, help='Mermaid 代码')
    parser.add_argument('--code-file', type=str, help='Mermaid 代码文件路径')
    parser.add_argument('--output', type=str, default='/tmp/mermaid_output.png', 
                        help='输出图片路径')
    parser.add_argument('--theme', type=str, default='default',
                        choices=['default', 'dark', 'base', 'wind'],
                        help='Mermaid 主题')
    parser.add_argument('--background', type=str, default='white',
                        help='背景色')
    parser.add_argument('--upload-feishu', action='store_true',
                        help='上传到飞书')
    parser.add_argument('--doc-id', type=str,
                        help='飞书文档 ID')
    
    args = parser.parse_args()
    
    # 读取代码
    if args.code_file:
        with open(args.code_file, 'r', encoding='utf-8') as f:
            mermaid_code = f.read()
    elif args.code:
        mermaid_code = args.code
    else:
        print("错误：请提供 --code 或 --code-file")
        return 1
    
    # 验证
    valid, error = validate_mermaid_code(mermaid_code)
    if not valid:
        print(f"错误：{error}")
        return 1
    
    # 渲染
    print(f"开始渲染...")
    html_path = render_mermaid_to_png(
        mermaid_code,
        args.output,
        args.theme,
        args.background
    )
    
    print(f"HTML 已生成：{html_path}")
    print(f"请使用 browser 工具加载此 HTML 并截图")
    
    return 0


if __name__ == '__main__':
    exit(main())
