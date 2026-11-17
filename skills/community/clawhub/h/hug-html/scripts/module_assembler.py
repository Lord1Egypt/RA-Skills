#!/usr/bin/env python3
"""
from _paths import DATA_DIR
module_assembler.py — 组件式模块组装引擎 v3.0.0

原子组件(6种) + 组合引擎 + 3级约束(fill/fit/clip) + 8方向位置

用法:
  python module_assembler.py --list-components    # 列出所有组件类型
  python module_assembler.py --spec <spec> -o <out>  # 从组件Spec生成
"""

import json
import re
import sys
from pathlib import Path
from typing import Optional

# R-12 审计锚点
DEFAULT_DATA_DIR_RAW = "skills/.standardization/hug-html/data/"
SKILL_DIR = Path(__file__).parent.parent

# ══════════════════════════════════════════════════════
# 约束模式
# ══════════════════════════════════════════════════════

CONSTRAINT_MODES = {
    "fill": "stretch to fill container, ignore aspect ratio",
    "fit": "maintain aspect ratio, fit within container (contain)",
    "clip": "no scaling, center in container, overflow hidden",
}

# ══════════════════════════════════════════════════════
# 位置系统：8方向 + 占比 + 宽高比
# ══════════════════════════════════════════════════════

POSITION_DIRECTIONS = {
    "left", "right", "top", "bottom",
    "center", "top-left", "top-right",
    "bottom-left", "bottom-right",
}

# ══════════════════════════════════════════════════════
# 组件类型定义
# ══════════════════════════════════════════════════════

COMPONENT_TYPES = {
    "text": {
        "desc": "纯文本，支持 title/body/caption 变体",
        "fields": ["content", "variant", "style"],
        "variant_options": {
            "title": {"font_size": "18px", "font_weight": "700", "color": "#1a1a2e"},
            "body": {"font_size": "14px", "font_weight": "400", "color": "#4a4a6a"},
            "caption": {"font_size": "12px", "font_weight": "300", "color": "#8888aa"},
        },
    },
    "image": {
        "desc": "图片，支持 fit/cover/原始三种填充模式",
        "fields": ["src", "alt", "constraint", "aspect", "style"],
    },
    "icon": {
        "desc": "图标（SVG内联/FontAwesome）",
        "fields": ["name", "family", "size", "color", "style"],
    },
    "qrcode": {
        "desc": "二维码（通过API生成或占位）",
        "fields": ["content", "size", "label", "style"],
    },
    "table": {
        "desc": "数据表格",
        "fields": ["headers", "rows", "style"],
    },
    "divider": {
        "desc": "分割线",
        "fields": ["height", "color", "style_type", "style"],
    },
    "spacer": {
        "desc": "空白占位，用于控制间距",
        "fields": ["width", "height", "style"],
    },
    "group": {
        "desc": "组件组合容器，递归包含子组件",
        "fields": ["direction", "align", "cross_align", "children", "style"],
    },
}

# ══════════════════════════════════════════════════════
# 约束CSS生成
# ══════════════════════════════════════════════════════

def _constraint_css(constraint: str, aspect: Optional[str] = None) -> str:
    """根据约束模式生成CSS"""
    css = ""
    if constraint == "fill":
        css += "width:100%;height:100%;"
    elif constraint == "fit":
        css += "max-width:100%;max-height:100%;width:auto;height:auto;"
        if aspect:
            css += f"aspect-ratio:{aspect};"
        css += "object-fit:contain;"
    elif constraint == "clip":
        css += "position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);"
        css += "max-width:none;max-height:none;overflow:hidden;"
    return css


def _container_css(direction: str, align: str, cross_align: str) -> str:
    """生成flex容器CSS"""
    css = "display:flex;"
    css += "flex-direction:column;" if direction == "column" else "flex-direction:row;"
    align_map = {
        "left": "flex-start", "right": "flex-end", "center": "center",
        "top": "flex-start", "bottom": "flex-end", "stretch": "stretch",
    }
    css += f"align-items:{align_map.get(cross_align, 'stretch')};"
    if direction == "row":
        css += f"justify-content:{align_map.get(align, 'flex-start')};"
    else:
        css += f"justify-content:{align_map.get(align, 'flex-start')};"
    return css


# ══════════════════════════════════════════════════════
# 组件HTML生成
# ══════════════════════════════════════════════════════

def _gen_text(comp: dict, cell_style: dict) -> str:
    """生成文本组件HTML"""
    variant = comp.get("variant", "body")
    variants = COMPONENT_TYPES["text"]["variant_options"]
    vstyle = variants.get(variant, variants["body"])
    content = comp.get("content", "")
    user_style = comp.get("style", {})
    merged = {**vstyle, **user_style}
    css = f"font-size:{merged['font_size']};font-weight:{merged['font_weight']};"
    css += f"color:{merged['color']};margin:0;"
    return f'<p class="component-text" style="{css}">{_esc(content)}</p>'


def _gen_image(comp: dict, cell_style: dict) -> str:
    """生成图片组件HTML"""
    src = comp.get("src", "")
    alt = comp.get("alt", "")
    constraint = comp.get("constraint", "fit")
    aspect = comp.get("aspect")
    user_style = comp.get("style", {})
    css = _constraint_css(constraint, aspect)
    for k, v in user_style.items():
        css += f"{k}:{v};"
    return f'<img class="component-image" src="{_esc(src)}" alt="{_esc(alt)}" style="{css}" loading="lazy">'


def _gen_icon(comp: dict, cell_style: dict) -> str:
    """生成图标组件HTML"""
    name = comp.get("name", "star")
    family = comp.get("family", "fa")
    size = comp.get("size", "24px")
    color = comp.get("color", "#1a1a2e")
    # FontAwesome 图标
    if family == "fa":
        return f'<i class="component-icon fa fa-{name}" style="font-size:{size};color:{color};"></i>'
    # SVG内联图标（用简单占位，实际可扩展）
    svg_size = size.replace("px", "")
    return f'''<svg class="component-icon" width="{svg_size}" height="{svg_size}" viewBox="0 0 24 24" fill="{color}">
  <path d="M12 2L15.09 8.26L22 9.27L17 14.14L18.18 21.02L12 17.77L5.82 21.02L7 14.14L2 9.27L8.91 8.26L12 2Z"/>
</svg>'''


def _gen_qrcode(comp: dict, cell_style: dict) -> str:
    """生成二维码组件HTML"""
    content = comp.get("content", "")
    size = comp.get("size", "120px")
    label = comp.get("label", "")
    # 使用QR码API生成
    qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size={size}x{size}&data={_esc(content)}"
    html = f'<img class="component-qrcode" src="{qr_url}" alt="QR" style="width:{size};height:{size};display:block;">'
    if label:
        html += f'<p class="component-qrlabel" style="text-align:center;font-size:12px;color:#888;margin:4px 0 0 0;">{_esc(label)}</p>'
    return html


def _gen_table(comp: dict, cell_style: dict) -> str:
    """生成表格组件HTML"""
    headers = comp.get("headers", [])
    rows = comp.get("rows", [])
    user_style = comp.get("style", {})
    css = "width:100%;border-collapse:collapse;font-size:13px;"
    for k, v in user_style.items():
        css += f"{k}:{v};"
    html = f'<table class="component-table" style="{css}"><thead><tr>'
    for h in headers:
        html += f'<th style="padding:8px;border-bottom:2px solid #eee;text-align:left;">{_esc(h)}</th>'
    html += '</tr></thead><tbody>'
    for row in rows:
        html += '<tr>'
        for cell in row:
            html += f'<td style="padding:8px;border-bottom:1px solid #f0f0f0;">{_esc(str(cell))}</td>'
        html += '</tr>'
    html += '</tbody></table>'
    return html


def _gen_divider(comp: dict, cell_style: dict) -> str:
    """生成分割线组件HTML"""
    height = comp.get("height", "1px")
    color = comp.get("color", "#e0e0e0")
    style_type = comp.get("style_type", "solid")
    return f'<hr class="component-divider" style="border:none;border-top:{height} {style_type} {color};margin:8px 0;width:100%;">'


def _gen_spacer(comp: dict, cell_style: dict) -> str:
    """生成空白占位HTML"""
    w = comp.get("width", "100%")
    h = comp.get("height", "auto")
    return f'<div class="component-spacer" style="width:{w};height:{h};flex-shrink:0;"></div>'


def _gen_group(comp: dict, cell_style: dict) -> str:
    """生成组件组合容器HTML（递归）"""
    direction = comp.get("direction", "row")
    align = comp.get("align", "left")
    cross_align = comp.get("cross_align", "stretch")
    children = comp.get("children", [])
    user_style = comp.get("style", {})
    # 计算子组件的flex比例
    ratios = comp.get("ratios", None)  # [1, 2] 表示1/3和2/3
    css = _container_css(direction, align, cross_align)
    for k, v in user_style.items():
        css += f"{k}:{v};"
    if css:
        css = css.rstrip(";")
    html = f'<div class="component-group" style="{css}">'
    for i, child in enumerate(children):
        child_html = _render_component(child, cell_style)
        # 应用比例
        if ratios and i < len(ratios):
            total = sum(ratios)
            pct = f"{ratios[i] / total * 100:.2f}%"
            child_html = child_html.replace(
                'class="',
                f'style="flex:0 0 {pct};max-width:{pct};" class="'
            ) if direction == "row" else child_html.replace(
                'class="',
                f'style="flex:0 0 {pct};" class="'
            )
        html += child_html
    html += '</div>'
    return html


# ══════════════════════════════════════════════════════
# 组件分发器
# ══════════════════════════════════════════════════════

_COMP_GENERATORS = {
    "text": _gen_text,
    "image": _gen_image,
    "icon": _gen_icon,
    "qrcode": _gen_qrcode,
    "table": _gen_table,
    "divider": _gen_divider,
    "spacer": _gen_spacer,
    "group": _gen_group,
}


def _render_component(comp: dict, cell_style: dict) -> str:
    """渲染单个组件（递归）"""
    comp_type = comp.get("type", "text")
    gen = _COMP_GENERATORS.get(comp_type)
    if not gen:
        return f'<!-- unknown component type: {comp_type} -->'
    return gen(comp, cell_style)


# ══════════════════════════════════════════════════════
# 单元格内容生成（主入口）
# ══════════════════════════════════════════════════════

def render_cell_content(cell: dict, cell_index: int) -> str:
    """根据cell定义生成HTML内容，支持新旧两种格式"""
    cell_padding = cell.get("padding", "12px")
    cell_style = {"padding": cell_padding}

    # ---- 旧格式兼容：composite module ----
    if "module" in cell and "components" not in cell:
        module_name = cell["module"]
        # 尝试调用 grid_builder 的旧模块渲染
        try:
            sys.path.insert(0, str(Path(__file__).parent))
            from grid_builder import _render_composite_module
            return _render_composite_module(module_name, cell.get("style", {}))
        except Exception:
            return f'<!-- 旧模块 {module_name} 渲染失败，请迁移到组件格式 -->'

    # ---- 新格式：components ----
    components = cell.get("components", [])
    if not components:
        return ""

    # 如果只有一个组件，直接渲染（不加group包装）
    if len(components) == 1:
        comp = components[0]
        if comp.get("type") == "group":
            return _gen_group(comp, cell_style)
        return _render_component(comp, cell_style)

    # 多个组件：自动用group包装
    direction = cell.get("direction", "row")
    align = cell.get("align", "center")
    cross_align = cell.get("cross_align", "stretch")
    ratios = cell.get("ratios", None)
    group = {
        "type": "group",
        "direction": direction,
        "align": align,
        "cross_align": cross_align,
        "ratios": ratios,
        "children": components,
    }
    return _gen_group(group, cell_style)


# ══════════════════════════════════════════════════════
# 约束模式css辅助（供grid_builder调用）
# ══════════════════════════════════════════════════════

def cell_constraint_css(cell: dict) -> str:
    """生成cell级别的约束CSS"""
    constraint = cell.get("constraint", "fill")
    if constraint == "fill":
        return "width:100%;height:100%;overflow:hidden;"
    elif constraint == "fit":
        return "width:100%;height:100%;overflow:hidden;display:flex;align-items:center;justify-content:center;"
    elif constraint == "clip":
        return "width:100%;height:100%;overflow:hidden;position:relative;"
    return ""


# ══════════════════════════════════════════════════════
# 辅助函数
# ══════════════════════════════════════════════════════

def _esc(s: str) -> str:
    """HTML转义"""
    s = str(s)
    s = s.replace("&", "&amp;")
    s = s.replace("<", "&lt;")
    s = s.replace(">", "&gt;")
    s = s.replace('"', "&quot;")
    s = s.replace("'", "&#39;")
    return s


def list_components() -> str:
    """列出所有组件类型"""
    lines = [f"\n=== 组件类型 ({len(COMPONENT_TYPES)} 种) ===\n"]
    for name, info in COMPONENT_TYPES.items():
        lines.append(f"  {name}: {info['desc']}")
        if "fields" in info:
            lines.append(f"    字段: {', '.join(info['fields'])}")
    lines.append(f"\n约束模式: {json.dumps(CONSTRAINT_MODES, ensure_ascii=False, indent=2)}")
    lines.append(f"\n8方向位置: {', '.join(sorted(POSITION_DIRECTIONS))}")
    return "\n".join(lines)


def export_interfaces() -> dict:
    """导出完整的组件系统接口定义"""
    return {
        "component_types": {k: {"desc": v["desc"], "fields": v["fields"]}
                           for k, v in COMPONENT_TYPES.items()},
        "constraint_modes": CONSTRAINT_MODES,
        "position_directions": sorted(POSITION_DIRECTIONS),
        "text_variants": COMPONENT_TYPES["text"]["variant_options"],
        "example_cell": {
            "row": 0, "col": 0, "rowspan": 1, "colspan": 1,
            "constraint": "fit",
            "direction": "row",
            "ratios": [2, 3],
            "padding": "12px",
            "components": [
                {"type": "image", "src": "https://...", "constraint": "fit", "aspect": "1:1"},
                {"type": "group", "direction": "column",
                 "children": [
                     {"type": "text", "variant": "title", "content": "标题"},
                     {"type": "text", "variant": "body", "content": "正文"},
                 ]}
            ]
        }
    }


# ══════════════════════════════════════════════════════
# CLI入口
# ══════════════════════════════════════════════════════

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Component-based module assembly engine v3.0")
    parser.add_argument("--list-components", action="store_true", help="列出所有组件类型")
    parser.add_argument("--export-interfaces", metavar="FILE", help="导出接口定义JSON")
    parser.add_argument("--spec", metavar="FILE", help="组件Spec文件路径")
    parser.add_argument("-o", "--output", metavar="FILE", help="输出HTML路径")
    parser.add_argument("--demo", action="store_true", help="生成演示HTML")
    args = parser.parse_args()

    if args.list_components:
        print(list_components())
        sys.exit(0)

    if args.export_interfaces:
        data = export_interfaces()
        with open(args.export_interfaces, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"[OK] 接口定义已导出: {args.export_interfaces}")
        sys.exit(0)

    if args.spec and args.output:
        with open(args.spec, "r", encoding="utf-8") as f:
            spec = json.load(f)
        cells_html = []
        for i, cell in enumerate(spec.get("grid", {}).get("cells", [])):
            cells_html.append(render_cell_content(cell, i))
        with open(args.output, "w", encoding="utf-8") as f:
            f.write("\n".join(cells_html))
        print(f"[OK] 已生成: {args.output}")
        sys.exit(0)

    if args.demo:
        # 生成一个3x3的演示页面
        demo_spec = {
            "name": "组件系统演示",
            "card_style": {
                "max_width": "600px",
                "bg": "rgba(255,255,255,0.9)",
                "border_radius": "24px",
                "padding": "20px",
            },
            "grid": {
                "rows": 3, "cols": 3, "gap": "12px",
                "cells": [
                    {"id": "c1", "row": 0, "col": 0, "rowspan": 1, "colspan": 2,
                     "constraint": "fill", "direction": "row", "ratios": [1, 2],
                     "components": [
                         {"type": "image", "src": "https://picsum.photos/100/100", "constraint": "fit", "aspect": "1/1"},
                         {"type": "group", "direction": "column",
                          "children": [
                              {"type": "text", "variant": "title", "content": "图文卡片标题"},
                              {"type": "text", "variant": "body", "content": "这里是正文描述，展示图文左右组合的效果。"},
                          ]}
                     ]},
                    {"id": "c2", "row": 0, "col": 2,
                     "components": [
                         {"type": "icon", "name": "star", "size": "32px", "color": "#ffd700"},
                         {"type": "text", "variant": "caption", "content": "收藏"},
                     ]},
                    {"id": "c3", "row": 1, "col": 0, "colspan": 3,
                     "components": [{"type": "divider"}]},
                    {"id": "c4", "row": 2, "col": 0, "colspan": 3,
                     "direction": "row", "ratios": [1, 1, 1],
                     "components": [
                         {"type": "text", "variant": "body", "content": "左列文字"},
                         {"type": "text", "variant": "body", "content": "中列文字"},
                         {"type": "text", "variant": "body", "content": "右列文字"},
                     ]},
                ]
            }
        }
        html = f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
* {{margin:0;padding:0;box-sizing:border-box;}}
body {{min-height:100vh;display:flex;align-items:center;justify-content:center;
  background:linear-gradient(135deg,#667eea,#764ba2);font-family:'Segoe UI',sans-serif;padding:20px;}}
.card {{max-width:{demo_spec['card_style']['max_width']};width:100%;
  background:{demo_spec['card_style']['bg']};
  border-radius:{demo_spec['card_style']['border_radius']};
  padding:{demo_spec['card_style']['padding']};
  box-shadow:0 20px 60px rgba(0,0,0,0.15);}}
.grid {{display:grid;
  grid-template-columns:repeat({demo_spec['grid']['cols']},1fr);
  gap:{demo_spec['grid']['gap']};}}
.cell {{overflow:hidden;}}
</style></head><body><div class="card"><div class="grid">
"""
        for cell in demo_spec["grid"]["cells"]:
            row, col = cell["row"], cell["col"]
            rs = cell.get("rowspan", 1)
            cs = cell.get("colspan", 1)
            constraint_css = cell_constraint_css(cell)
            content = render_cell_content(cell, cell.get("id", ""))
            html += f'<div class="cell" style="grid-row:{row+1}/span{rs};grid-column:{col+1}/span{cs};{constraint_css}">{content}</div>'
        html += "</div></div></body></html>"

        out = str(DATA_DIR / "output" / "component-demo.html")
        Path(out).parent.mkdir(parents=True, exist_ok=True)
        with open(out, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"[OK] 演示页面已生成: {out}")
        sys.exit(0)

    parser.print_help()
