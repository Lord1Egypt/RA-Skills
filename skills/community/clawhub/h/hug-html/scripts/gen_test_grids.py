#!/usr/bin/env python3
"""
Generate test grid specs that demonstrate rowspan/colspan merging.
Run: python scripts/gen_test_grids.py
"""

import json
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).parent.parent
TEMPLATES_DIR = DATA_DIR / "templates"
OUTPUT_DIR = DATA_DIR / "output"
MODULES_DIR = DATA_DIR / "modules"

def build_base_modules_json():
    """Extract base module library from grid_builder.py for persistence"""
    # We import dynamically to get the actual data
    sys.path.insert(0, str(SKILL_DIR / "scripts"))
    from grid_builder import BASE_MODULES, COMPOSITE_MODULES

    out = {
        "base": {},
        "composite": {},
    }
    for name, info in BASE_MODULES.items():
        out["base"][name] = {
            "type": info["type"],
            "css": info["css"],
            "desc": info["desc"],
        }
    for name, info in COMPOSITE_MODULES.items():
        out["composite"][name] = {
            "desc": info["desc"],
            "base": info.get("base", []),
            "template_preview": info.get("template", "")[:200],
        }

    return out

def save_modules_json():
    modules = build_base_modules_json()
    MODULES_DIR.mkdir(parents=True, exist_ok=True)
    out = MODULES_DIR / "modules.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(modules, f, ensure_ascii=False, indent=2)
    print(f"[OK] Modules saved: {out}")

def create_3x3_merged_spec():
    """Create a 3×3 grid with rowspan/colspan merging demo"""
    spec = {
        "name": "3×3网格合并演示",
        "desc": "3行3列网格，展示单元格合并效果",
        "card_style": {
            "max_width": "600px",
            "width": "100%",
            "bg": "#ffffff",
            "border_radius": "24px",
            "shadow": "0 10px 30px rgba(0,0,0,0.1)",
            "padding": "20px",
            "border": "1px solid #e8eef5",
        },
        "grid": {"rows": 3, "cols": 3, "gap": "8px"},
        "cells": [
            {"id": "A1", "row": 0, "col": 0,
             "style": {"background":"#6C63FF","color":"white","padding":"24px","border-radius":"12px","text-align":"center","font-weight":"bold","display":"flex","align-items":"center","justify-content":"center"},
             "html": '<div data-field="cell-A1">A1<br><small>标准格</small></div>'},
            {"id": "B1-C1", "row": 0, "col": 1, "colspan": 2, "rowspan": 2,
             "style": {"background":"#00B894","color":"white","padding":"24px","border-radius":"12px","text-align":"center","font-weight":"bold","display":"flex","align-items":"center","justify-content":"center"},
             "html": '<div data-field="cell-B1">B1+C1<br><small>合并2列2行</small></div>'},
            {"id": "A2", "row": 1, "col": 0,
             "style": {"background":"#FF6584","color":"white","padding":"24px","border-radius":"12px","text-align":"center"},
             "html": '<div data-field="cell-A2">A2<br><small>标准格</small></div>'},
            {"id": "A3-B3", "row": 2, "col": 0, "colspan": 2,
             "style": {"background":"#E17055","color":"white","padding":"24px","border-radius":"12px","text-align":"center"},
             "html": '<div data-field="cell-A3">A3+B3<br><small>合并2列</small></div>'},
            {"id": "C3", "row": 2, "col": 2,
             "style": {"background":"#6C63FF","color":"white","padding":"24px","border-radius":"12px","text-align":"center"},
             "html": '<div data-field="cell-C3">C3<br><small>标准格</small></div>'},
        ],
    }
    out = TEMPLATES_DIR / "3x3-merge.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(spec, f, ensure_ascii=False, indent=2)
    print(f"[OK] 3×3 merged spec: {out}")
    return spec

def create_4x2_app_card():
    """Create a 4×2 app card with diverse cell content"""
    spec = {
        "name": "4×2应用推广卡（多样内容）",
        "desc": "4行2列网格，每格不同内容类型",
        "card_style": {
            "max_width": "500px",
            "width": "100%",
            "bg": "rgba(255,255,255,0.9)",
            "backdrop": "blur(20px)",
            "webkit_backdrop": "blur(20px)",
            "border_radius": "32px",
            "shadow": "0 20px 35px -8px rgba(0,0,0,0.12)",
            "padding": "16px",
            "border": "1px solid rgba(255,255,255,0.5)",
        },
        "grid": {"rows": 4, "cols": 2, "gap": "8px"},
        "cells": [
            {"id": "header-title", "row": 0, "col": 0, "colspan": 2,
             "style": {"padding":"16px 0 8px 0"},
             "module": "composite:header-entity"},
            {"id": "feature-col1", "row": 1, "col": 0,
             "style": {"background":"#f8fafd","padding":"16px","border-radius":"16px","border":"1px solid #e8eef5"},
             "module": "composite:text-block"},
            {"id": "feature-col2", "row": 1, "col": 1,
             "style": {"background":"#f8fafd","padding":"16px","border-radius":"16px","border":"1px solid #e8eef5"},
             "module": "composite:text-block"},
            {"id": "qr-section", "row": 2, "col": 0, "colspan": 2,
             "style": {"padding":"8px 0"},
             "module": "composite:qr-card"},
            {"id": "footer", "row": 3, "col": 0, "colspan": 2,
             "module": "composite:footer-caption"},
        ],
    }
    out = TEMPLATES_DIR / "4x2-app-card.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(spec, f, ensure_ascii=False, indent=2)
    print(f"[OK] 4×2 app card: {out}")
    return spec

def create_3x3_mixed_styles():
    """Create a 3×3 grid where each cell has a different style"""
    cell_colors = [
        {"bg": "#6C63FF", "text": "紫色-图文"},
        {"bg": "#00B894", "text": "绿色-纯文字"},
        {"bg": "#E17055", "text": "橙色-多行文字"},
        {"bg": "#FF6584", "text": "粉色-图文组合"},
        {"bg": "#3F51B5", "text": "蓝色-纯图片"},
        {"bg": "#FDCB6E", "text": "黄色-混合内容"},
        {"bg": "#00CEC9", "text": "青色-表单"},
        {"bg": "#2D3436", "text": "深灰-数据"},
        {"bg": "#6C5CE7", "text": "紫色-脚注"},
    ]

    cells = []
    for i in range(3):
        for j in range(3):
            idx = i * 3 + j
            c = cell_colors[idx]
            cells.append({
                "id": f"cell-{i+1}-{j+1}",
                "row": i, "col": j,
                "style": {
                    "background": c["bg"],
                    "color": "white",
                    "padding": "20px",
                    "border-radius": "12px",
                    "text-align": "center",
                    "font-weight": "600",
                    "display": "flex",
                    "align-items": "center",
                    "justify-content": "center",
                },
                "html": f'<div data-field="cell-{i+1}-{j+1}"><div style="font-size:18px;margin-bottom:8px;">{c["text"]}</div><div style="font-size:12px;opacity:0.8;">Row{i+1} Col{j+1}</div></div>',
            })

    spec = {
        "name": "3×3网格·多样式展示",
        "desc": "3行3列，每格不同背景色和内容类型",
        "card_style": {
            "max_width": "700px", "width": "100%",
            "bg": "#f5f7fa", "border_radius": "20px",
            "shadow": "0 10px 30px rgba(0,0,0,0.08)",
            "padding": "16px",
        },
        "grid": {"rows": 3, "cols": 3, "gap": "8px"},
        "cells": cells,
    }

    out = TEMPLATES_DIR / "3x3-mixed-styles.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(spec, f, ensure_ascii=False, indent=2)
    print(f"[OK] 3×3 mixed styles: {out}")
    return spec

if __name__ == "__main__":
    save_modules_json()
    create_3x3_merged_spec()
    create_4x2_app_card()
    create_3x3_mixed_styles()
    print("\n[DONE] All grid specs and modules generated.")
