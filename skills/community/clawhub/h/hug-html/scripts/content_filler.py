#!/usr/bin/env python3
# content_filler.py — Grid-aware 内容填充器 v2.1.2
# 用法:
#   python content_filler.py fill --template <path> --content <json> --output <path>
#   python content_filler.py auto --template <path> --output <path>
#   python content_filler.py extract --input <html> --output <json>

import argparse
import json
import re
import sys
import traceback
from pathlib import Path

OUTPUT_DIR = DATA_DIR / "output"

SAVED_HTML = {}  # 保存最近处理的 HTML，以便出错时提供上下文

# Style presets
STYLE_PRESETS = {
    "business": {
        "primary": "#1a2a4a",
        "secondary": "#4a5568",
        "bg": "#f0f4f8",
        "font": "'Microsoft YaHei', sans-serif",
        "border_radius": "8px",
        "gradient": "linear-gradient(135deg, #1a2a4a 0%, #4a5568 100%)",
    },
    "academic": {
        "primary": "#333333",
        "secondary": "#666666",
        "bg": "#ffffff",
        "font": "SimSun, serif",
        "border_radius": "4px",
        "gradient": "linear-gradient(135deg, #333 0%, #666 100%)",
    },
    "festive": {
        "primary": "#c0392b",
        "secondary": "#e74c3c",
        "bg": "linear-gradient(135deg, #c0392b 0%, #e74c3c 100%)",
        "font": "SimSun, serif",
        "border_radius": "12px",
        "gradient": "linear-gradient(135deg, #c0392b 0%, #e74c3c 100%)",
    },
    "mourning": {
        "primary": "#333333",
        "secondary": "#666666",
        "bg": "#f5f5f5",
        "font": "SimSun, serif",
        "border_radius": "8px",
        "gradient": "linear-gradient(135deg, #333 0%, #666 100%)",
    },
    "tech": {
        "primary": "#2D3436",
        "secondary": "#636E72",
        "bg": "#f8f9fa",
        "font": "Consolas, 'Courier New', monospace",
        "border_radius": "4px",
        "gradient": "linear-gradient(135deg, #2D3436 0%, #636E72 100%)",
    },
}

def show_error(err_type, message, fix_hint=""):
    """输出中文错误提示 + 修复建议"""
    icon_map = {
        "参数错误": "❌", "文件错误": "📁", "模块错误": "🧩",
        "模板错误": "📋", "路径错误": "🔗", "JSON错误": "📄", "内部错误": "⚙️",
    }
    icon = icon_map.get(err_type, "❌")
    # 兼容 GBK 终端（Windows 下无法显示 emoji 时降级为纯文字）
    lines = [
        f"\n[{err_type}] {message}",
    ]
    if fix_hint:
        lines.append(f"  [修复建议] {fix_hint}")
    msg = "\n".join(lines)
    try:
        print(f"\n{icon} [{err_type}] {message}")
        if fix_hint:
            print(f"  💡 修复建议: {fix_hint}")
    except UnicodeEncodeError:
        print(msg.encode("ascii", errors="replace").decode("ascii"))

def fill_template(template_path, content_data, output_path):
    """Fill template with content data (replaces data-field content)"""
    tpl = Path(template_path)
    if not tpl.exists():
        show_error("文件错误", f"找不到模板文件: {tpl}",
                   "请确认 --template 参数指向一个已存在的 HTML 文件。\n"
                   "  先生成模板: python scripts/template_generator.py --type harmony-app -o data/output/template.html")
        return None

    try:
        html = tpl.read_text(encoding="utf-8")
    except Exception as e:
        show_error("文件错误", f"读取模板文件失败: {e}", "检查文件编码（应为 UTF-8）")
        return None

    filled_count = 0
    for field, value in content_data.items():
        pattern = (
            r'(<[^>]+data-field="' + re.escape(field) + r'"[^>]*>)'
            r'(.*?)'
            r'(</[^>]+>)'
        )
        replacement = r'\1' + str(value) + r'\3'
        new_html, count = re.subn(pattern, replacement, html, count=1, flags=re.DOTALL)
        if count > 0:
            html = new_html
            filled_count += 1
        else:
            print(f"  ⚠️  未找到字段 '{field}'（跳过）")

    try:
        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(html, encoding="utf-8")
    except Exception as e:
        show_error("文件错误", f"写入输出文件失败: {output_path}", f"检查目录权限: {e}")
        return None

    print(f"[OK] 内容填充完成: {output_path}")
    print(f"  共填充了 {filled_count}/{len(content_data)} 个字段")
    return str(output_path)

def auto_fill(template_path, output_path):
    """Auto-fill template with smart sample content based on field names"""
    tpl = Path(template_path)
    if not tpl.exists():
        show_error("文件错误", f"找不到模板文件: {tpl}", "请确认 --template 参数指向一个已存在的 HTML 文件")
        return None

    try:
        html = tpl.read_text(encoding="utf-8")
    except Exception as e:
        show_error("文件错误", f"读取模板文件失败: {e}")
        return None

    fields = re.findall(r'data-field="([^"]+)"', html)
    if not fields:
        show_error("模板错误", f"文件中未找到 data-field 标记字段", "请确认这是一个 hug-html 生成的模板 HTML 文件")
        return None

    samples = {
        r'title|name|header': "主标题文字（可编辑）",
        r'subtitle|sub\b': "副标题或简短描述",
        r'desc|detail|intro': "这里是详细描述内容，可以根据需要修改此文字。",
        r'note|caption|hint': "注释说明文字",
        r'footer': "© 2026 版权所有 | 联系我们",
        r'badge|tag|label': "标签名称",
        r'hint|qr-hint|platform': "平台说明",
        r'feature-text|feature-icon': "特性描述文字 ✨",
        r'qr-label|qr-image': "扫码体验",
        r'device|protocol|arrow': "设备/协议标注",
        r'entity-name|app-name|service-name': "名称",
        r'entity-badge|app-badge|service-badge': "标签",
        r'main-title': "主标题",
        r'main-sub': "副标题",
        r'.*': "可编辑内容",
    }

    content = {}
    for field in fields:
        val = "可编辑内容：" + field
        for pattern, sample in samples.items():
            if re.search(pattern, field, re.IGNORECASE):
                val = sample
                break
        content[field] = val

    for field, value in content.items():
        pattern = (
            r'(<[^>]+data-field="' + re.escape(field) + r'"[^>]*>)'
            r'(.*?)'
            r'(</[^>]+>)'
        )
        replacement = r'\1' + str(value) + r'\3'
        html = re.sub(pattern, replacement, html, count=1, flags=re.DOTALL)

    try:
        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(html, encoding="utf-8")
    except Exception as e:
        show_error("文件错误", f"写入输出文件失败: {output_path}", f"检查目录权限: {e}")
        return None

    print(f"[OK] 自动填充完成: {output_path}")
    print(f"  共填充了 {len(content)} 个字段")
    return str(output_path)

def extract_content(html_path):
    """Extract data-field content from HTML"""
    p = Path(html_path)
    if not p.exists():
        show_error("文件错误", f"找不到文件: {p}")
        return None

    try:
        html = p.read_text(encoding="utf-8")
    except Exception as e:
        show_error("文件错误", f"读取文件失败: {e}")
        return None

    fields = re.findall(r'data-field="([^"]+)"', html)
    content = {}
    for field in fields:
        pattern = (
            r'<[^>]+data-field="' + re.escape(field) + r'"[^>]*>'
            r'(.*?)'
            r'</[^>]+>'
        )
        match = re.search(pattern, html, re.DOTALL)
        if match:
            content[field] = match.group(1).strip()
    return content

def main():
    try:
        _main_impl()
    except SystemExit:
        pass
    except KeyboardInterrupt:
        print("\n⚠️  用户中断操作")
    except Exception as e:
        show_error("内部错误", f"程序发生未预期的错误: {type(e).__name__}",
                   "使用 --help 查看参数说明。如持续报错，可查看 FAQ。")
        traceback.print_exc()

def _main_impl():
    ap = argparse.ArgumentParser(description="Grid-aware HTML 内容填充器 v2", add_help=True)
    sub = ap.add_subparsers(dest="command")

    p_extract = sub.add_parser("extract", help="从 HTML 中提取所有 data-field 内容")
    p_extract.add_argument("--input", required=True, help="输入的 HTML 文件路径")
    p_extract.add_argument("--output", required=True, help="输出的 JSON 文件路径")

    p_auto = sub.add_parser("auto", help="自动填充示例内容")
    p_auto.add_argument("--template", required=True, help="模板 HTML 文件路径")
    p_auto.add_argument("--output", required=True, help="输出文件路径")

    p_fill = sub.add_parser("fill", help="从 JSON 文件填充内容")
    p_fill.add_argument("--template", required=True, help="模板 HTML 文件路径")
    p_fill.add_argument("--content", required=True, help="内容的 JSON 文件路径")
    p_fill.add_argument("--output", required=True, help="输出文件路径")

    p_preset = sub.add_parser("preset", help="应用样式预设")
    p_preset.add_argument("--template", required=True, help="模板 HTML 文件路径")
    p_preset.add_argument("--name", required=True, choices=list(STYLE_PRESETS.keys()), help="样式预设名称")
    p_preset.add_argument("--output", required=True, help="输出文件路径")

    args = ap.parse_args()

    if args.command == "extract":
        content = extract_content(args.input)
        if content is None:
            return
        try:
            out = Path(args.output)
            out.parent.mkdir(parents=True, exist_ok=True)
            with open(out, "w", encoding="utf-8") as f:
                json.dump(content, f, ensure_ascii=False, indent=2)
            print(f"[OK] 内容已提取: {out}")
            print(f"  共提取了 {len(content)} 个字段")
        except Exception as e:
            show_error("文件错误", f"写入输出文件失败: {e}")

    elif args.command == "auto":
        auto_fill(args.template, args.output)

    elif args.command == "fill":
        try:
            with open(args.content, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            show_error("文件错误", f"找不到内容文件: {args.content}")
            return
        except json.JSONDecodeError as e:
            show_error("JSON错误", f"内容文件格式错误: {e}", "请确认 JSON 格式正确")
            return
        fill_template(args.template, data, args.output)

    elif args.command == "preset":
        tpl = Path(args.template)
        if not tpl.exists():
            show_error("文件错误", f"找不到模板文件: {tpl}")
            return
        try:
            html = tpl.read_text(encoding="utf-8")
        except Exception as e:
            show_error("文件错误", f"读取模板文件失败: {e}")
            return
        preset = STYLE_PRESETS[args.name]
        for key, val in preset.items():
            css_var = "--" + key.replace("_", "-") + ":"
            html = html.replace(css_var, css_var + " " + val + ";")
        try:
            out = Path(args.output)
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(html, encoding="utf-8")
            print(f"[OK] 样式预设 '{args.name}' 已应用: {out}")
        except Exception as e:
            show_error("文件错误", f"写入输出文件失败: {e}")

    else:
        ap.print_help()

if __name__ == "__main__":
    main()
