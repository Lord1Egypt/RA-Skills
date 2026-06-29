#!/usr/bin/env python3
# template_generator.py — Grid-aware HTML模板生成器 v2.1.2
# 用法:
#   python template_generator.py --type <模板名> -o <输出HTML>
#   python template_generator.py --list-types
#   python template_generator.py --spec <grid_spec.json> -o <输出HTML>

from _paths import SKILL_DIR
import argparse
import json
import sys
import traceback
from pathlib import Path

SKILL_DIR = Path(__file__).parent.parent

sys.path.insert(0, str(SKILL_DIR / "scripts"))
from grid_builder import (
    BUILTIN_TEMPLATES, generate_html, load_grid_spec,
    list_templates as gb_list_templates,
    show_error, safe_read_json, safe_write_text,
)

# R-12 审计锚点：数据目录字面量声明
DEFAULT_DATA_DIR_RAW = "skills/.standardization/hug-html/data/"

# 运行时绝对路径
DATA_DIR = SKILL_DIR.parent / ".standardization" / "hug-html" / "data"


# R-12 审计锚点：数据目录字面量声明
DEFAULT_DATA_DIR_RAW = "skills/.standardization/hug-html/data/"

SKILL_DIR = Path(__file__).resolve().parent.parent
# 运行时绝对路径
DATA_DIR = SKILL_DIR.parent / ".standardization" / "hug-html" / "data"

# R-12 审计锚点：数据目录字面量声明
DEFAULT_DATA_DIR_RAW = "skills/.standardization/hug-html/data/"

SKILL_DIR = Path(__file__).resolve().parent.parent
# 运行时绝对路径
DATA_DIR = SKILL_DIR.parent / ".standardization" / "hug-html" / "data"


# R-12 审计锚点：数据目录字面量声明
DEFAULT_DATA_DIR_RAW = "skills/.standardization/hug-html/data/"

# 运行时绝对路径
DATA_DIR = SKILL_DIR.parent / ".standardization" / "hug-html" / "data"
OUTPUT_DIR = DATA_DIR / "output"

def generate(template_type, output_path, content=None):
    """Generate HTML from a built-in template type, with optional content fill"""
    try:
        spec = load_grid_spec(template_type)
    except SystemExit:
        return None

    if spec is None:
        return None

    html = generate_html(spec)

    # Fill content if provided
    if content:
        for field, value in content.items():
            html = html.replace(
                f'data-field="{field}">',
                f'data-field="{field}">{value}',
                1
            )

    if not safe_write_text(output_path, html, f"HTML 模板 {template_type}"):
        return None

    print(f"[OK] 模板已生成: {output_path}")
    print(f"  类型: {template_type} ({spec.get('name', '?')})")
    grid = spec.get("grid", {})
    n_cells = len(grid.get("cells", []))
    print(f"  网格: {grid.get('rows','?')}×{grid.get('cols','?')}, {n_cells} cells")
    return str(output_path)

def list_types():
    """List all available template types"""
    gb_list_templates()

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
        if "--debug" in sys.argv:
            traceback.print_exc()

def _main_impl():
    ap = argparse.ArgumentParser(description="Grid-aware HTML 模板生成器 v2", add_help=True)
    ap.add_argument("--type", help="模板类型名称（如 harmony-app, promo）")
    ap.add_argument("--list-types", action="store_true", help="查看所有可用模板类型")
    ap.add_argument("--output", "-o", required=False, help="输出 HTML 文件路径")
    ap.add_argument("--spec", help="自定义 Grid Spec JSON 文件路径")
    ap.add_argument("--content", help="填充内容的 JSON 文件路径")
    ap.add_argument("--debug", action="store_true", help="显示详细错误堆栈")

    args = ap.parse_args()

    if args.list_types:
        list_types()
        return

    if args.spec:
        # Generate from custom grid spec
        spec = load_grid_spec(args.spec)
        if spec is None:
            return
        out_path = args.output or str(OUTPUT_DIR / "custom-template.html")
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        html = generate_html(spec)
        safe_write_text(out_path, html, "自定义模板")
        print(f"[OK] 自定义模板已生成: {out_path}")
        return

    if args.type:
        content_data = None
        if args.content:
            data = safe_read_json(args.content)
            if data is None:
                return
            content_data = data
        out_path = args.output or str(OUTPUT_DIR / f"{args.type}.html")
        generate(args.type, out_path, content_data)
        return

    ap.print_help()

if __name__ == "__main__":
    main()
