#!/usr/bin/env python3
"""
pans-case-writer: Case Study 生成器
功能：背景/挑战/方案/成果四段式模板，支持 Markdown/PDF/HTML 导出
"""
import argparse
import os
import sys
import re
from pathlib import Path

# ------------------------------------------------------------------
# 模板
# ------------------------------------------------------------------
CASE_TEMPLATE = """# {customer} 案例研究

## 客户背景
{background}

## 面临挑战
{challenge}

## 解决方案
{solution}

## 成果与价值
{result}
"""

PRESET_TEMPLATES = {
    "default": {
        "name": "标准四段式",
        "sections": ["客户背景", "面临挑战", "解决方案", "成果与价值"],
    },
    "gpu-infra": {
        "name": "GPU算力交付",
        "sections": ["客户背景", "算力需求", "交付方案", "使用成果"],
    },
    "ai-startup": {
        "name": "AI创业公司",
        "sections": ["公司介绍", "核心痛点", "AI能力建设", "业务增长"],
    },
    "enterprise": {
        "name": "企业客户",
        "sections": ["企业概况", "业务挑战", "转型方案", "量化收益"],
    },
}

# ------------------------------------------------------------------
# 工具函数
# ------------------------------------------------------------------
def ask(prompt, default=""):
    val = input(f"{prompt}{' (' + default + ')' if default else ''}: ").strip()
    return val if val else default

def ask_multiline(prompt, default=""):
    print(f"{prompt}（输入空行结束）:")
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    result = "\n".join(lines)
    return result if result else default

def slug(name):
    name = re.sub(r"[^\w\s-]", "", name)
    name = re.sub(r"[\s]+", "-", name)
    return name.lower()

def render_case(data):
    return CASE_TEMPLATE.format(**data)

def save_case(content, output_path):
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"已保存: {output_path}")

def md_to_html(md):
    html = md
    html = re.sub(r"^### (.+)$", r"<h3>\1</h3>", html, flags=re.MULTILINE)
    html = re.sub(r"^## (.+)$", r"<h2>\1</h2>", html, flags=re.MULTILINE)
    html = re.sub(r"^# (.+)$", r"<h1>\1</h1>", html, flags=re.MULTILINE)
    lines = html.split("\n")
    result = []
    in_ul = False
    for line in lines:
        line = line.strip()
        if not line:
            if in_ul:
                result.append("</ul>")
                in_ul = False
            continue
        if line.startswith("<h"):
            if in_ul:
                result.append("</ul>")
                in_ul = False
            result.append(line)
        elif line.startswith("-"):
            if not in_ul:
                result.append("<ul>")
                in_ul = True
            result.append(f"  <li>{line[1:].strip()}</li>")
        else:
            if in_ul:
                result.append("</ul>")
                in_ul = False
            result.append(f"<p>{line}</p>")
    if in_ul:
        result.append("</ul>")
    return "\n".join(result)

def export_html(md_path, html_path):
    with open(md_path, encoding="utf-8") as f:
        md = f.read()
    body = md_to_html(md)
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Case Study</title>
<style>
  body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    max-width: 800px; margin: 60px auto; padding: 0 20px; color: #1a1a1a; line-height: 1.8; }}
  h1 {{ border-bottom: 3px solid #2563eb; padding-bottom: 10px; color: #1e3a8a; }}
  h2 {{ margin-top: 40px; color: #1e40af; border-left: 4px solid #3b82f6; padding-left: 12px; }}
  p  {{ margin: 12px 0; }}
  li {{ margin: 6px 0; }}
</style>
</head>
<body>
{body}
</body>
</html>"""
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"HTML 导出: {html_path}")

def export_pdf(md_path, pdf_path):
    try:
        from weasyprint import HTML as WPHTML
        import markdown
    except ImportError:
        print("缺少依赖，请安装: pip install weasyprint markdown")
        sys.exit(1)
    with open(md_path, encoding="utf-8") as f:
        md = f.read()
    body_html = markdown.markdown(md, extensions=["tables", "fenced_code"])
    html = f"""<!DOCTYPE html>
<html lang="zh-CN"><head>
<meta charset="UTF-8">
<style>
  body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    max-width: 800px; margin: 60px auto; padding: 0 20px; color: #1a1a1a; line-height: 1.8; }}
  h1 {{ border-bottom: 3px solid #2563eb; padding-bottom: 10px; color: #1e3a8a; }}
  h2 {{ margin-top: 40px; color: #1e40af; border-left: 4px solid #3b82f6; padding-left: 12px; }}
</style></head><body>{body_html}</body></html>"""
    WPHTML(string=html).write_pdf(pdf_path)
    print(f"PDF 导出: {pdf_path}")

# ------------------------------------------------------------------
# 命令
# ------------------------------------------------------------------
def cmd_create():
    print("\n>> Case Study 创建向导\n" + "=" * 40)
    customer = ask("客户名称")
    if not customer:
        print("客户名称不能为空")
        sys.exit(1)
    industry = ask("行业领域", "AI/科技")
    background = ask_multiline("客户背景描述")
    challenge = ask_multiline("面临挑战（痛点）")
    solution = ask_multiline("解决方案")
    result = ask_multiline("成果与价值（量化指标）")
    data = {
        "customer": customer,
        "background": background or f"{industry} 行业",
        "challenge": challenge or "待补充",
        "solution": solution or "待补充",
        "result": result or "待补充",
    }
    content = render_case(data)
    filename = f"case-{slug(customer)}.md"
    output_dir = Path.home() / ".qclaw" / "cases"
    output_path = output_dir / filename
    save_case(content, str(output_path))
    print(f"\nCase Study 生成完成！\n文件: {output_path}")

def cmd_export(args):
    md_path = Path(args.export)
    if not md_path.exists():
        print(f"文件不存在: {md_path}")
        sys.exit(1)
    fmt = args.format.lower()
    if fmt == "html":
        export_html(md_path, md_path.with_suffix(".html"))
    elif fmt == "pdf":
        export_pdf(md_path, md_path.with_suffix(".pdf"))
    else:
        print(f"不支持的格式: {fmt}，支持: markdown, html, pdf")
        sys.exit(1)

def cmd_list():
    print("\n可用 Case Study 模板\n" + "=" * 40)
    for key, tmpl in PRESET_TEMPLATES.items():
        sections = " > ".join(tmpl["sections"])
        print(f"\n  [{key}] {tmpl['name']}")
        print(f"     章节: {sections}")
    print()

# ------------------------------------------------------------------
# 主入口
# ------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="pans-case-writer: 自动将客户成功案例包装为 Case Study",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  case.py --create           # 交互式创建
  case.py --export in.md     # 导出（默认 HTML）
  case.py --export in.md -f pdf   # 导出为 PDF
  case.py --list             # 查看可用模板
        """,
    )
    parser.add_argument("--create", action="store_true", help="交互式创建 Case Study")
    parser.add_argument("--export", metavar="FILE", help="导出已生成的 Markdown 文件")
    parser.add_argument("-f", "--format", default="html",
                        choices=["markdown", "html", "pdf"],
                        help="导出格式 (默认: html)")
    parser.add_argument("--list", action="store_true", help="列出可用模板")
    args = parser.parse_args()
    if args.create:
        cmd_create()
    elif args.export:
        cmd_export(args)
    elif args.list:
        cmd_list()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()