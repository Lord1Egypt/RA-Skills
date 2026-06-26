#!/usr/bin/env python3
"""
马尔代夫选岛报告 Markdown → PDF 导出工具

使用方法：
    python export-pdf.py <input.md> [output.pdf]

如果不指定 output.pdf，默认输出到同目录下同名 .pdf 文件。

依赖：
    pip install markdown weasyprint
"""

import sys
import os

def check_dependencies():
    """检查并提示安装缺失的依赖"""
    missing = []
    try:
        import markdown
    except ImportError:
        missing.append("markdown")
    try:
        import weasyprint
    except ImportError:
        missing.append("weasyprint")

    if missing:
        print(f"缺少依赖: {', '.join(missing)}", file=sys.stderr)
        print(f"请执行: pip install {' '.join(missing)}", file=sys.stderr)
        sys.exit(1)


def convert_markdown_to_pdf(input_path, output_path):
    """将 Markdown 文件转换为 PDF"""
    import markdown
    import weasyprint

    with open(input_path, "r", encoding="utf-8") as f:
        markdown_content = f.read()

    html_body = markdown.markdown(
        markdown_content,
        extensions=["tables", "fenced_code", "toc"]
    )

    full_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<style>
    body {{
        font-family: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
        max-width: 800px;
        margin: 0 auto;
        padding: 40px;
        color: #333;
        line-height: 1.8;
    }}
    h1 {{
        color: #1a73e8;
        border-bottom: 2px solid #1a73e8;
        padding-bottom: 10px;
    }}
    h2 {{
        color: #2c3e50;
        margin-top: 30px;
    }}
    h3 {{
        color: #34495e;
    }}
    table {{
        border-collapse: collapse;
        width: 100%;
        margin: 15px 0;
    }}
    th, td {{
        border: 1px solid #ddd;
        padding: 10px 12px;
        text-align: left;
    }}
    th {{
        background-color: #f5f7fa;
        font-weight: bold;
    }}
    tr:nth-child(even) {{
        background-color: #fafafa;
    }}
    blockquote {{
        border-left: 4px solid #1a73e8;
        margin: 15px 0;
        padding: 10px 20px;
        background-color: #f8f9fa;
        color: #555;
    }}
    img {{
        max-width: 100%;
        border-radius: 8px;
        margin: 10px 0;
    }}
    a {{
        color: #1a73e8;
        text-decoration: none;
    }}
    hr {{
        border: none;
        border-top: 1px solid #eee;
        margin: 25px 0;
    }}
    code {{
        background-color: #f5f5f5;
        padding: 2px 6px;
        border-radius: 3px;
        font-size: 0.9em;
    }}
</style>
</head>
<body>
{html_body}
</body>
</html>"""

    weasyprint.HTML(string=full_html).write_pdf(output_path)
    print(f"✅ PDF 已导出: {output_path}")


def main():
    if len(sys.argv) < 2:
        print("用法: python export-pdf.py <input.md> [output.pdf]", file=sys.stderr)
        sys.exit(1)

    input_path = sys.argv[1]
    if not os.path.exists(input_path):
        print(f"文件不存在: {input_path}", file=sys.stderr)
        sys.exit(1)

    if len(sys.argv) >= 3:
        output_path = sys.argv[2]
    else:
        output_path = os.path.splitext(input_path)[0] + ".pdf"

    check_dependencies()
    convert_markdown_to_pdf(input_path, output_path)


if __name__ == "__main__":
    main()
