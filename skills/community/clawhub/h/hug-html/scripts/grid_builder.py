#!/usr/bin/env python3
"""
grid_builder.py — Grid-based HTML模块化引擎 v1.0.0

两层级模块体系:
  - Base (base): CSS原语 (字体/颜色/渐变/圆角/图片裁切/间距)
  - Composite (composite): 复合模块 (图文组合/多行文字/二维码卡片等)

Grid spec 定义布局 → cells 分配模块 → 输出带 CSS Grid 的自包含 HTML

用法:
  python grid_builder.py --spec <grid_spec.json> --output <out.html>
  python grid_builder.py --list-modules
  python grid_builder.py --list-templates
  python grid_builder.py --demo --template harmony-app --output demo.html
"""

import argparse
import json
import re
import sys
import traceback
from copy import deepcopy
from pathlib import Path

SKILL_DIR = Path(__file__).parent.parent
SCRIPTS_DIR = SKILL_DIR / "scripts"
BUILTIN_TEMPLATES_DIR = SCRIPTS_DIR / "templates"   # 内置文件型模板（跟随技能）
OUTPUT_DIR = DATA_DIR / "output"
USER_TEMPLATES_DIR = DATA_DIR / "user-templates"

# ══════════════════════════════════════════════════════
# 中文错误处理工具
# ══════════════════════════════════════════════════════

def show_error(err_type, message, fix_hint=""):
    """输出中文错误提示 + 修复建议。不抛异常，不输出英文 Traceback。"""
    icon_map = {
        "参数错误": "❌",
        "文件错误": "📁",
        "模块错误": "🧩",
        "模板错误": "📋",
        "路径错误": "🔗",
        "JSON错误": "📄",
        "内部错误": "⚙️",
    }
    icon = icon_map.get(err_type, "❌")
    # 兼容 GBK 终端（Windows 下无法显示 emoji 时降级为纯文字）
    lines = [
        f"\n[{err_type}] {message}",
    ]
    if fix_hint:
        lines.append(f"  [修复建议] {fix_hint}")
    lines.append("  [提示] 如仍有问题，可查看 FAQ (references/faq.md) 或使用 --help 查看参数说明")
    msg = "\n".join(lines)
    try:
        print(f"\n{icon} [{err_type}] {message}")
        if fix_hint:
            print(f"  💡 修复建议: {fix_hint}")
        print("  ℹ️  如仍有问题，可查看 FAQ (references/faq.md) 或使用 --help 查看参数说明")
    except UnicodeEncodeError:
        # Fallback for GBK terminals (Windows)
        print(msg.encode("ascii", errors="replace").decode("ascii"))

def safe_read_json(path):
    """安全读取 JSON 文件，失败输出中文错误"""
    p = Path(path)
    if not p.exists():
        show_error("文件错误", f"找不到文件: {p}", f"请检查路径是否正确。可使用绝对路径，如: {Path.cwd() / p}")
        return None
    try:
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        show_error("JSON错误", f"文件 {p} 格式错误: {e}", "请确认 JSON 格式正确，可使用 jsonlint.com 校验")
        return None
    except Exception as e:
        show_error("文件错误", f"读取文件 {p} 失败: {e}", "检查文件权限和编码（应为 UTF-8）")
        return None

def safe_write_text(path, text, desc="文件"):
    """安全写入文本文件"""
    p = Path(path)
    try:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
    except Exception as e:
        show_error("文件错误", f"写入 {desc} 失败: {p}", f"检查目录权限或路径是否有效: {e}")
        return False
    return True

# ══════════════════════════════════════════════════════
# 第一层: Base Modules (CSS 原语)
# ══════════════════════════════════════════════════════

BASE_MODULES = {
    # ── 字体大小 ──
    "font-size-xxl": {"type": "css", "css": {"font-size": "36px", "font-weight": "700", "line-height": "1.2"}, "desc": "超大标题 36px Bold"},
    "font-size-xl":  {"type": "css", "css": {"font-size": "28px", "font-weight": "600", "line-height": "1.2"}, "desc": "大标题 28px Semibold"},
    "font-size-lg":  {"type": "css", "css": {"font-size": "18px", "font-weight": "600", "line-height": "1.3"}, "desc": "中标题 18px Semibold"},
    "font-size-md":  {"type": "css", "css": {"font-size": "15px", "font-weight": "400", "line-height": "1.5"}, "desc": "正文 15px Regular"},
    "font-size-sm":  {"type": "css", "css": {"font-size": "13px", "font-weight": "500", "line-height": "1.4"}, "desc": "小字 13px Medium"},
    "font-size-xs":  {"type": "css", "css": {"font-size": "11px", "font-weight": "500", "line-height": "1.3"}, "desc": "极小 11px Medium"},
    "font-size-xxs": {"type": "css", "css": {"font-size": "9px", "font-weight": "400", "line-height": "1.3"}, "desc": "注释 9px Regular"},

    # ── 字体颜色 ──
    "color-dark":    {"type": "css", "css": {"color": "#1a2a3a"}, "desc": "深色文字"},
    "color-mid":     {"type": "css", "css": {"color": "#4f606f"}, "desc": "中灰色文字"},
    "color-light":   {"type": "css", "css": {"color": "#8b9aab"}, "desc": "浅灰色文字"},
    "color-white":   {"type": "css", "css": {"color": "#ffffff"}, "desc": "白色文字"},
    "color-primary": {"type": "css", "css": {"color": "#2c7da0"}, "desc": "主色调文字"},
    "color-gradient-text": {"type": "css", "css": {
        "background": "linear-gradient(145deg, #2d3f55 0%, #13212e 100%)",
        "-webkit-background-clip": "text",
        "background-clip": "text",
        "color": "transparent",
    }, "desc": "渐变文字"},

    # ── 背景 ──
    "bg-white":       {"type": "css", "css": {"background": "#ffffff"}, "desc": "白色背景"},
    "bg-transparent": {"type": "css", "css": {"background": "transparent"}, "desc": "透明背景"},
    "bg-light-blue":  {"type": "css", "css": {"background": "rgba(240, 246, 255, 0.6)"}, "desc": "浅蓝半透明背景"},
    "bg-light-gray":  {"type": "css", "css": {"background": "#f8f9fa"}, "desc": "浅灰色背景"},
    "bg-glass":       {"type": "css", "css": {"background": "rgba(255,255,255,0.82)", "backdrop-filter": "blur(25px)", "-webkit-backdrop-filter": "blur(25px)"}, "desc": "毛玻璃效果"},
    "bg-dark":        {"type": "css", "css": {"background": "#1a2a3a"}, "desc": "深色背景"},
    "bg-gradient-purple": {"type": "css", "css": {"background": "linear-gradient(135deg, #6C63FF 0%, #FF6584 100%)"}, "desc": "粉紫渐变"},
    "bg-gradient-blue":   {"type": "css", "css": {"background": "linear-gradient(135deg, #00B894 0%, #00CEC9 100%)"}, "desc": "蓝绿渐变"},
    "bg-gradient-dark":   {"type": "css", "css": {"background": "linear-gradient(135deg, #2D3436 0%, #636E72 100%)"}, "desc": "深灰渐变"},
    "bg-gradient-gold":   {"type": "css", "css": {"background": "linear-gradient(135deg, #c0392b 0%, #e74c3c 100%)"}, "desc": "红金渐变"},

    # ── 圆角 ──
    "radius-sm":  {"type": "css", "css": {"border-radius": "8px"}, "desc": "小圆角 8px"},
    "radius-md":  {"type": "css", "css": {"border-radius": "16px"}, "desc": "中圆角 16px"},
    "radius-lg":  {"type": "css", "css": {"border-radius": "24px"}, "desc": "大圆角 24px"},
    "radius-xl":  {"type": "css", "css": {"border-radius": "36px"}, "desc": "超大圆角 36px"},
    "radius-full": {"type": "css", "css": {"border-radius": "50%"}, "desc": "圆形 50%"},
    "radius-pill": {"type": "css", "css": {"border-radius": "40px"}, "desc": "胶囊圆角 40px"},

    # ── 边距 ──
    "pad-xs":  {"type": "css", "css": {"padding": "8px"}, "desc": "小间距 8px"},
    "pad-sm":  {"type": "css", "css": {"padding": "12px 16px"}, "desc": "中间距 12x16"},
    "pad-md":  {"type": "css", "css": {"padding": "16px 20px"}, "desc": "中上间距 16x20"},
    "pad-lg":  {"type": "css", "css": {"padding": "24px 20px 28px"}, "desc": "大间距 24x20x28"},
    "pad-xl":  {"type": "css", "css": {"padding": "40px 24px"}, "desc": "超大间距 40x24"},

    # ── 阴影 ──
    "shadow-sm":  {"type": "css", "css": {"box-shadow": "0 2px 8px rgba(0,0,0,0.06)"}, "desc": "小阴影"},
    "shadow-md":  {"type": "css", "css": {"box-shadow": "0 10px 20px -8px rgba(0,20,30,0.15)"}, "desc": "中阴影"},
    "shadow-lg":  {"type": "css", "css": {"box-shadow": "0 20px 35px -12px rgba(0,0,0,0.12)"}, "desc": "大阴影"},
    "shadow-glass": {"type": "css", "css": {"box-shadow": "0 20px 35px -8px rgba(0,0,0,0.15), 0 4px 12px rgba(0,0,0,0.05), inset 0 1px 1px rgba(255,255,255,0.7)"}, "desc": "毛玻璃阴影"},

    # ── 边框 ──
    "border-glass": {"type": "css", "css": {"border": "1px solid rgba(255,255,255,0.4)"}, "desc": "毛玻璃边框"},
    "border-light": {"type": "css", "css": {"border": "1px solid rgba(210,225,245,0.8)"}, "desc": "浅色边框"},
    "border-bottom": {"type": "css", "css": {"border-bottom": "1px solid #d0deed"}, "desc": "底部边框线"},
    "divider-gradient": {"type": "css", "css": {"height": "1px", "background": "linear-gradient(90deg, transparent, #b3c6d9, transparent)"}, "desc": "渐变分割线"},
    "divider-solid": {"type": "css", "css": {"height": "1px", "background": "#e0e8f0"}, "desc": "实色分割线"},

    # ── 图片样式 ──
    "img-circle": {"type": "css", "css": {"border-radius": "50%", "object-fit": "cover"}, "desc": "圆形图片裁剪"},
    "img-cover":  {"type": "css", "css": {"width": "100%", "height": "200px", "object-fit": "cover", "border-radius": "8px"}, "desc": "封面填充"},
    "img-contain":{"type": "css", "css": {"width": "100%", "height": "auto", "border-radius": "8px"}, "desc": "含展示(不变形)"},
    "img-logo":   {"type": "css", "css": {"width": "80px", "height": "auto", "position": "absolute", "top": "12px", "left": "12px"}, "desc": "Logo定位"},

    # ── flex / 布局原语 ──
    "flex-center":     {"type": "css", "css": {"display": "flex", "align-items": "center", "justify-content": "center"}, "desc": "Flex居中"},
    "flex-between":    {"type": "css", "css": {"display": "flex", "align-items": "center", "justify-content": "space-between"}, "desc": "Flex两端对齐"},
    "flex-col":        {"type": "css", "css": {"display": "flex", "flex-direction": "column"}, "desc": "Flex纵向排列"},
    "text-center":     {"type": "css", "css": {"text-align": "center"}, "desc": "文字居中"},
    "text-left":       {"type": "css", "css": {"text-align": "left"}, "desc": "文字左对齐"},
    "gap-xs":          {"type": "css", "css": {"gap": "8px"}, "desc": "小间隙 8px"},
    "gap-sm":          {"type": "css", "css": {"gap": "12px"}, "desc": "中间隙 12px"},
    "gap-md":          {"type": "css", "css": {"gap": "16px"}, "desc": "大间隙 16px"},
    "gap-lg":          {"type": "css", "css": {"gap": "24px"}, "desc": "超大间隙 24px"},

    # ── 透明度 ──
    "opacity-100": {"type": "css", "css": {"opacity": "1"}, "desc": "不透明"},
    "opacity-90":  {"type": "css", "css": {"opacity": "0.9"}, "desc": "90%透明"},
    "opacity-70":  {"type": "css", "css": {"opacity": "0.7"}, "desc": "70%透明"},
    "opacity-50":  {"type": "css", "css": {"opacity": "0.5"}, "desc": "50%透明"},

    # ── 动画 ──
    "anim-fade":  {"type": "css", "css": {"animation": "gridFadeIn 0.6s ease-out"}, "desc": "淡入动画"},
    "anim-slide": {"type": "css", "css": {"animation": "gridSlideIn 0.5s ease-out"}, "desc": "滑入动画"},
    "hover-scale":{"type": "css", "css": {"transition": "transform 0.3s"}, "desc": "悬停放大"},
}

# ══════════════════════════════════════════════════════
# 第二层: Composite Modules (复合模块)
# 每个复合模块引用 base modules + 定义 HTML 模板
# ══════════════════════════════════════════════════════

COMPOSITE_MODULES = {
    # ── 头部 ──
    "header-entity": {
        "desc": "应用头部（圆形图标 + 名称 + 标签）",
        "base": ["flex-center", "gap-xs", "pad-xs"],
        "template": (
            '<div class="grid-header-entity">'
              '<div class="ghe-icon">'
                '<img class="ghe-icon-img editable-img" data-field="app-icon" src="data:image/svg+xml,%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 width=%2748%27 height=%2748%27%3E%3Crect fill=%27%236C63FF%27 width=%2748%27 height=%2748%27 rx=%2716%27/%3E%3Ctext x=%2724%27 y=%2728%27 text-anchor=%27middle%27 fill=%27white%27 font-size=%2720%27 font-weight=%27bold%27%3EA%3C/text%3E%3C/svg%3E" alt="应用图标">'
              '</div>'
              '<div class="ghe-text">'
                '<div class="ghe-name" data-field="entity-name">应用名称</div>'
                '<div class="ghe-badge" data-field="entity-badge">标签描述</div>'
              '</div>'
            '</div>'
        ),
        "css": """
.grid-header-entity { display:flex; align-items:center; gap:8px; justify-content:center; }
.ghe-icon { width:48px; height:48px; border-radius:16px; display:flex; align-items:center; justify-content:center; flex-shrink:0; }
.ghe-icon-img { width:100%; height:100%; border-radius:16px; object-fit:cover; cursor:pointer; }
.ghe-text { display:flex; flex-direction:column; }
.ghe-name { font-size:18px; font-weight:600; color:#1a2a3a; line-height:1.2; }
.ghe-badge { font-size:11px; color:#5e707f; background:rgba(210,225,240,0.6); padding:2px 8px; border-radius:30px; margin-top:2px; border:0.3px solid rgba(0,90,150,0.1); text-align:center; }
"""
    },

    "header-dual": {
        "desc": "双实体头部（左应用 + 右元服务）",
        "base": ["flex-between", "gap-sm", "pad-xs"],
        "template": (
            '<div class="grid-dual-header">'
              '<div class="gdh-entity gdh-left">'
                '<div class="gdh-icon"><img class="gdh-icon-img editable-img" data-field="app-icon" src="data:image/svg+xml,%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 width=%2748%27 height=%2748%27%3E%3Crect fill=%27%236C63FF%27 width=%2748%27 height=%2748%27 rx=%2716%27/%3E%3Ctext x=%2724%27 y=%2728%27 text-anchor=%27middle%27 fill=%27white%27 font-size=%2720%27 font-weight=%27bold%27%3EA%3C/text%3E%3C/svg%3E" alt="应用图标"></div>'
                '<div class="gdh-text">'
                  '<div class="gdh-name" data-field="app-name">应用名称</div>'
                  '<div class="gdh-badge" data-field="app-badge">应用市场</div>'
                '</div>'
              '</div>'
              '<div class="gdh-entity gdh-right">'
                '<div class="gdh-text" style="text-align:right;align-items:flex-end;">'
                  '<div class="gdh-name" data-field="service-name">元服务</div>'
                  '<div class="gdh-badge" data-field="service-badge">即用·免安装</div>'
                '</div>'
                '<div class="gdh-icon"><img class="gdh-icon-img editable-img" data-field="service-icon" src="data:image/svg+xml,%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 width=%2748%27 height=%2748%27%3E%3Crect fill=%27%23FF6584%27 width=%2748%27 height=%2748%27 rx=%2716%27/%3E%3Ctext x=%2724%27 y=%2728%27 text-anchor=%27middle%27 fill=%27white%27 font-size=%2720%27 font-weight=%27bold%27%3ES%3C/text%3E%3C/svg%3E" alt="元服务图标"></div>'
              '</div>'
            '</div>'
        ),
        "css": """
.grid-dual-header { display:flex; justify-content:space-between; align-items:center; gap:12px; margin-bottom:20px; }
.gdh-entity { display:flex; align-items:center; gap:8px; flex:1; }
.gdh-left { justify-content:flex-start; }
.gdh-right { justify-content:flex-end; }
.gdh-icon { width:48px; height:48px; border-radius:16px; display:flex; align-items:center; justify-content:center; flex-shrink:0; }
.gdh-icon-img { width:100%; height:100%; border-radius:16px; object-fit:cover; cursor:pointer; }
.gdh-text { display:flex; flex-direction:column; min-width:0; }
.gdh-right .gdh-text { align-items:flex-end; text-align:right; }
.gdh-name { font-size:18px; font-weight:600; color:#1a2a3a; line-height:1.2; white-space:nowrap; }
.gdh-badge { font-size:11px; color:#5e707f; background:rgba(210,225,240,0.6); padding:2px 8px; border-radius:30px; margin-top:2px; border:0.3px solid rgba(0,90,150,0.1); }
"""
    },

    # ── 主标题区 ──
    "main-title": {
        "desc": "主标题（渐变文字 + 副标题 + 底部边线）",
        "base": ["text-center", "gap-xs", "pad-sm"],
        "template": (
            '<div class="grid-main-title">'
              '<div class="gmt-title" data-field="main-title">主标题文字</div>'
              '<div class="gmt-sub" data-field="main-sub">副标题描述</div>'
            '</div>'
        ),
        "css": """
.grid-main-title { text-align:center; margin:6px 0 14px 0; }
.gmt-title { font-size:28px; font-weight:600; background:linear-gradient(145deg,#2d3f55 0%,#13212e 100%); -webkit-background-clip:text; background-clip:text; color:transparent; letter-spacing:0.5px; line-height:1.2; }
.gmt-sub { font-size:15px; font-weight:380; color:#4f606f; border-bottom:1px solid #d0deed; padding-bottom:12px; margin:0 10px 8px 10px; }
"""
    },

    # ── 二维码卡片 ──
    "qr-card": {
        "desc": "单张二维码卡片",
        "base": [],
        "template": (
            '<div class="grid-qr-section">'
              '<div class="gqs-item">'
                '<div class="gqs-qr-wrapper">'
                  '<img class="gqs-qr-img editable-img" src="data:image/svg+xml,%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 width=%27110%27 height=%27110%27%3E%3Crect fill=%27%23f2f5fa%27 width=%27110%27 height=%27110%27/%3E%3Cpath d=%27M30 30L80 30L80 80L30 80Z%27 fill=%27none%27 stroke=%27%233f5e7a%27 stroke-width=%274%27 stroke-dasharray=%278 6%27/%3E%3Ctext x=%2720%27 y=%2760%27 font-size=%2712%27 fill=%27%233f5e7a%27%3E二维码%3C/text%3E%3C/svg%3E" data-field="qr-image" alt="QR码占位">'
                '</div>'
                '<span class="gqs-label" data-field="qr-label">扫码体验</span>'
                '<span class="gqs-hint" data-field="qr-hint">平台说明</span>'
              '</div>'
            '</div>'
        ),
        "css": """
.grid-qr-section { display:flex; gap:16px; margin:10px 0 16px 0; justify-content:center; }
.gqs-item { background:white; border-radius:24px; padding:16px 12px 12px; box-shadow:0 10px 20px -8px rgba(0,20,30,0.15); border:1px solid rgba(210,225,245,0.8); display:flex; flex-direction:column; align-items:center; max-width:160px; }
.gqs-qr-wrapper { width:110px; height:110px; background:#fff; border-radius:16px; padding:6px; box-shadow:0 2px 8px rgba(0,0,0,0.03); display:flex; align-items:center; justify-content:center; }
.gqs-qr-img { width:100%; height:100%; object-fit:contain; display:block; border-radius:12px; }
.gqs-label { margin-top:8px; font-size:12px; font-weight:500; color:#2e4a62; background:#ecf3fa; padding:3px 12px; border-radius:40px; border:0.3px solid #bdd0e6; white-space:nowrap; }
.gqs-hint { font-size:9px; color:#7e92a5; margin-top:2px; }
"""
    },

    "qr-dual": {
        "desc": "双二维码（应用 + 元服务并排）",
        "base": [],
        "template": (
            '<div class="grid-qr-dual">'
              '<div class="gqd-item">'
                '<div class="gqd-qr-wrapper">'
                  '<img class="gqd-qr-img editable-img" src="data:image/svg+xml,%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 width=%27110%27 height=%27110%27%3E%3Crect fill=%27%23f2f5fa%27 width=%27110%27 height=%27110%27/%3E%3Cpath d=%27M30 30L80 30L80 80L30 80Z%27 fill=%27none%27 stroke=%27%233f5e7a%27 stroke-width=%274%27 stroke-dasharray=%278 6%27/%3E%3Ctext x=%2720%27 y=%2760%27 font-size=%2712%27 fill=%27%233f5e7a%27%3E应用码%3C/text%3E%3C/svg%3E" data-field="qr-image-left" alt="QR码左">'
                '</div>'
                '<span class="gqd-label" data-field="qr-label-left">安装应用</span>'
                '<span class="gqd-hint" data-field="qr-hint-left">华为应用市场</span>'
              '</div>'
              '<div class="gqd-item">'
                '<div class="gqd-qr-wrapper">'
                  '<img class="gqd-qr-img editable-img" src="data:image/svg+xml,%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 width=%27110%27 height=%27110%27%3E%3Crect fill=%27%23f2f5fa%27 width=%27110%27 height=%27110%27/%3E%3Cpath d=%27M30 30L80 30L80 80L30 80Z%27 fill=%27none%27 stroke=%27%233f5e7a%27 stroke-width=%274%27 stroke-dasharray=%278 6%27/%3E%3Ctext x=%2720%27 y=%2760%27 font-size=%2712%27 fill=%27%233f5e7a%27%3E元服务码%3C/text%3E%3C/svg%3E" data-field="qr-image-right" alt="QR码右">'
                '</div>'
                '<span class="gqd-label" data-field="qr-label-right">体验元服务</span>'
                '<span class="gqd-hint" data-field="qr-hint-right">即扫即用</span>'
              '</div>'
            '</div>'
        ),
        "css": """
.grid-qr-dual { display:flex; gap:16px; margin:10px 0 16px 0; justify-content:center; }
.gqd-item { background:white; border-radius:24px; padding:16px 12px 12px; box-shadow:0 10px 20px -8px rgba(0,20,30,0.15); border:1px solid rgba(210,225,245,0.8); flex:1; display:flex; flex-direction:column; align-items:center; max-width:160px; }
.gqd-qr-wrapper { width:110px; height:110px; background:#fff; border-radius:16px; padding:6px; box-shadow:0 2px 8px rgba(0,0,0,0.03); display:flex; align-items:center; justify-content:center; }
.gqd-qr-img { width:100%; height:100%; object-fit:contain; display:block; border-radius:12px; }
.gqd-label { margin-top:8px; font-size:12px; font-weight:500; color:#2e4a62; background:#ecf3fa; padding:3px 12px; border-radius:40px; border:0.3px solid #bdd0e6; white-space:nowrap; }
.gqd-hint { font-size:9px; color:#7e92a5; margin-top:2px; }
"""
    },

    # ── 特性面板 ──
    "feature-panel": {
        "desc": "特性面板（多行图标+文字描述）",
        "base": [],
        "template": (
            '<div class="grid-feature-panel">'
              '<div class="gfp-row" data-row="0">'
                '<span class="gfp-icon" data-field="feature-icon-0">✨⭐</span>'
                '<span class="gfp-text" data-field="feature-text-0">特性描述一</span>'
              '</div>'
              '<div class="gfp-row" data-row="1">'
                '<span class="gfp-icon" data-field="feature-icon-1">🎯📊</span>'
                '<span class="gfp-text" data-field="feature-text-1">特性描述二</span>'
              '</div>'
            '</div>'
        ),
        "css": """
.grid-feature-panel { background:rgba(240,246,255,0.6); border-radius:40px; padding:12px 16px; backdrop-filter:blur(8px); border:0.6px solid rgba(190,210,235,0.9); display:flex; flex-direction:column; gap:12px; }
.gfp-row { display:flex; align-items:center; gap:12px; color:#1e3a5f; justify-content:center; }
.gfp-icon { font-size:18px; color:#3a5f7a; min-width:60px; text-align:center; }
.gfp-text { font-size:13px; font-weight:500; }
"""
    },

    # ── 通信面板 (设备标签 + 箭头) ──
    "comms-panel": {
        "desc": "双端通信/对比面板（标签 + 连接线 + 协议标注）",
        "base": [],
        "template": (
            '<div class="grid-comms-panel">'
              '<div class="gcp-row" data-row="0">'
                '<span class="gcp-device"><span class="gcp-dev-icon">📱</span> <span data-field="device-a">端A</span></span>'
                '<span class="gcp-arrow">⟷ <span class="gcp-protocol" data-field="protocol-a">协议/连接</span> ⟷</span>'
                '<span class="gcp-device"><span class="gcp-dev-icon">📱</span> <span data-field="device-b">端B</span></span>'
              '</div>'
              '<div class="gcp-row" data-row="1">'
                '<span class="gcp-device"><span class="gcp-dev-icon">⭐</span> <span data-field="device-c">端C</span></span>'
                '<span class="gcp-arrow">⟶ <span class="gcp-protocol" data-field="protocol-b">协议/连接</span> ⟶</span>'
                '<span class="gcp-device"><span class="gcp-dev-icon">📱</span> <span data-field="device-d">端D</span></span>'
              '</div>'
            '</div>'
        ),
        "css": """
.grid-comms-panel { background:rgba(240,246,255,0.6); border-radius:40px; padding:12px 16px; backdrop-filter:blur(8px); border:0.6px solid rgba(190,210,235,0.9); display:flex; flex-direction:column; gap:10px; }
.gcp-row { display:flex; align-items:center; justify-content:space-around; flex-wrap:wrap; gap:8px; }
.gcp-device { display:flex; align-items:center; gap:4px; background:white; padding:4px 12px; border-radius:30px; font-size:13px; color:#1e3a5f; box-shadow:0 2px 4px rgba(0,0,0,0.02); border:0.5px solid #ccddef; }
.gcp-dev-icon { font-size:16px; }
.gcp-arrow { display:flex; align-items:center; gap:4px; color:#6e8bb0; font-size:14px; }
.gcp-protocol { background:#d9e9ff; border-radius:30px; padding:2px 8px; font-size:10px; font-weight:600; color:#1e5c8b; border:0.5px solid #a0c0e0; }
"""
    },

    # ── 脚注 ──
    "footer-caption": {
        "desc": "底部说明行（分隔线 + 标签组）",
        "base": [],
        "template": (
            '<div class="grid-footer">'
              '<div class="gf-divider"></div>'
              '<div class="gf-caption">'
                '<span data-field="footer-tag-1">标签一</span>'
                '<span data-field="footer-tag-2">标签二</span>'
                '<span data-field="footer-tag-3">标签三</span>'
              '</div>'
            '</div>'
        ),
        "css": """
.grid-footer { margin-top:4px; }
.gf-divider { margin:14px 0 6px 0; height:1px; background:linear-gradient(90deg,transparent,#b3c6d9,transparent); }
.gf-caption { text-align:center; font-size:10px; color:#8b9aab; display:flex; justify-content:center; gap:10px; }
.gf-caption span { background:rgba(210,225,240,0.5); padding:2px 10px; border-radius:30px; }
"""
    },

    "small-note": {
        "desc": "极小注释文字行",
        "base": [],
        "template": (
            '<div class="grid-small-note" data-field="note-text">注释说明文字</div>'
        ),
        "css": """
.grid-small-note { font-size:9px; color:#7f93a8; text-align:center; margin-top:4px; }
"""
    },

    # ── 纯文本块 ──
    "text-block": {
        "desc": "纯文本块（标题 + 正文）",
        "base": [],
        "template": (
            '<div class="grid-text-block">'
              '<h3 class="gtb-title" data-field="tb-title">标题</h3>'
              '<p class="gtb-body" data-field="tb-body">正文内容，可以包含多行文字描述。</p>'
              '<p class="gtb-body" data-field="tb-body-2">第二段正文。</p>'
            '</div>'
        ),
        "css": """
.grid-text-block { padding:16px; }
.gtb-title { font-size:18px; font-weight:600; color:#1a2a3a; margin:0 0 8px 0; }
.gtb-body { font-size:14px; line-height:1.6; color:#4f606f; margin:0 0 8px 0; }
"""
    },

    # ── 图文组合（左文右图） ──
    "text-img-right": {
        "desc": "左文右图组合",
        "base": [],
        "template": (
            '<div class="grid-text-img">'
              '<div class="gti-text">'
                '<h3 class="gti-title" data-field="ti-title">标题</h3>'
                '<p class="gti-desc" data-field="ti-desc">描述文字</p>'
              '</div>'
              '<div class="gti-image">'
                '<img class="gti-img editable-img" src="data:image/svg+xml,%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 width=%27300%27 height=%27200%27%3E%3Crect fill=%27%23e0e8f0%27 width=%27300%27 height=%27200%27 rx=%2712%27/%3E%3Ctext x=%27150%27 y=%27110%27 text-anchor=%27middle%27 fill=%27%238b9aab%27 font-size=%2716%27%3E点击/拖入图片%3C/text%3E%3C/svg%3E" data-field="ti-image" alt="图文区图片" style="width:100%;border-radius:12px;">'
              '</div>'
            '</div>'
        ),
        "css": """
.grid-text-img { display:grid; grid-template-columns:1fr 1fr; gap:20px; align-items:center; padding:16px; }
.gti-text { display:flex; flex-direction:column; gap:8px; }
.gti-title { font-size:18px; font-weight:600; color:#1a2a3a; margin:0; }
.gti-desc { font-size:14px; color:#4f606f; margin:0; line-height:1.6; }
.gti-image { display:flex; align-items:center; justify-content:center; }
.gti-img { width:100%; border-radius:12px; cursor:pointer; }
"""
    },

    # ── 参数面板（表单区） ──
    "param-panel": {
        "desc": "参数设置面板（带标题的信息区）",
        "base": [],
        "template": (
            '<div class="grid-param-panel">'
              '<div class="gpp-title" data-field="param-title">📆 参数控制</div>'
              '<div class="gpp-body">'
                '<div class="gpp-row"><label>参数1：</label><span class="gpp-value" data-field="param-1">值1</span></div>'
                '<div class="gpp-row"><label>参数2：</label><span class="gpp-value" data-field="param-2">值2</span></div>'
              '</div>'
            '</div>'
        ),
        "css": """
.grid-param-panel { background:#f8fafd; padding:20px 24px; border-radius:24px; border:1px solid #dce5ef; }
.gpp-title { font-weight:700; font-size:1.05rem; color:#1f5068; border-bottom:2px solid #cbdde9; padding-bottom:6px; margin-bottom:12px; }
.gpp-body { display:flex; flex-direction:column; gap:10px; }
.gpp-row { display:flex; align-items:center; gap:16px; }
.gpp-row label { font-weight:600; min-width:80px; }
.gpp-value { color:#4a627a; }
"""
    },

    # ── 数据表格 ──
    "data-table": {
        "desc": "数据表格（含表头 + 可编辑行）",
        "base": [],
        "template": (
            '<div class="grid-data-table">'
              '<table class="gdt-table">'
                '<thead><tr><th data-field="th-1">列1</th><th data-field="th-2">列2</th><th>操作</th></tr></thead>'
                '<tbody>'
                  '<tr><td data-field="td-row0-col0">值1</td><td data-field="td-row0-col1">值2</td><td><button class="gdt-del">🗑️</button></td></tr>'
                '</tbody>'
              '</table>'
              '<button class="gdt-add">+ 添加</button>'
            '</div>'
        ),
        "css": """
.grid-data-table { width:100%; }
.gdt-table { width:100%; border-collapse:collapse; background:white; border-radius:16px; overflow:hidden; font-size:0.85rem; }
.gdt-table th { background:#eef3fc; font-weight:600; padding:8px 6px; border-bottom:1px solid #e2e8f0; text-align:left; }
.gdt-table td { padding:8px 6px; border-bottom:1px solid #e2e8f0; }
.gdt-del { background:none; border:none; cursor:pointer; font-size:1.1rem; color:#b91c1c; padding:0 5px; }
.gdt-add { margin-top:12px; background:#eef2ff; border:1px dashed #5f8ab6; padding:6px 14px; border-radius:40px; font-size:0.8rem; cursor:pointer; }
"""
    },

    # ── 统计卡片 ──
    "stat-card": {
        "desc": "数据统计卡片（大数字 + 图例）",
        "base": [],
        "template": (
            '<div class="grid-stat-card">'
              '<div class="gsc-main">'
                '<div class="gsc-label" data-field="stat-label">总工日</div>'
                '<div class="gsc-value" data-field="stat-value">365</div>'
              '</div>'
              '<div class="gsc-legend">'
                '<span class="badge badge-work">🟢 工作日</span>'
                '<span class="badge badge-holiday">🟠 节假日</span>'
              '</div>'
            '</div>'
        ),
        "css": """
.grid-stat-card { background:#eef3fa; border-radius:20px; padding:14px 22px; display:flex; justify-content:space-between; align-items:baseline; flex-wrap:wrap; gap:12px; }
.gsc-main { display:flex; flex-direction:column; gap:4px; }
.gsc-label { font-size:14px; color:#4a627a; }
.gsc-value { font-size:2rem; font-weight:800; color:#1f6392; }
.gsc-legend { display:flex; gap:18px; font-size:0.75rem; flex-wrap:wrap; }
.badge { display:inline-block; font-size:0.7rem; border-radius:30px; padding:2px 8px; }
.badge-work { background:#e1f7dc; color:#2c6e2c; }
.badge-holiday { background:#ffdec2; color:#bc5100; }
.badge-rest { background:#ffe6e5; color:#b13e3e; }
.badge-comp { background:#d9effa; color:#00668c; }
"""
    },
}

# ══════════════════════════════════════════════════════
# 样式预设 (Style Presets)
# ══════════════════════════════════════════════════════

STYLE_PRESETS = {
    "business": {
        "name": "商务风格",
        "card_style": {
            "max_width": "1200px", "width": "100%",
            "bg": "#f0f4f8", "border_radius": "8px",
            "shadow": "0 4px 12px rgba(0,0,0,0.08)",
            "padding": "24px",
            "border": "1px solid #d0d8e0",
        },
        "font": "'Microsoft YaHei', sans-serif",
        "primary": "#1a2a4a", "secondary": "#4a5568",
    },
    "academic": {
        "name": "科研风格",
        "card_style": {
            "max_width": "960px", "width": "100%",
            "bg": "#ffffff", "border_radius": "4px",
            "shadow": "0 2px 8px rgba(0,0,0,0.06)",
            "padding": "28px",
            "border": "1px solid #cccccc",
        },
        "font": "SimSun, serif",
        "primary": "#333333", "secondary": "#666666",
    },
    "festive": {
        "name": "喜庆风格（红金配色）",
        "card_style": {
            "max_width": "600px", "width": "100%",
            "bg": "linear-gradient(135deg, #c0392b 0%, #e74c3c 100%)",
            "border_radius": "16px",
            "shadow": "0 8px 24px rgba(192,57,43,0.3)",
            "padding": "32px",
            "border": "none",
        },
        "font": "SimSun, serif",
        "primary": "#FFD700", "secondary": "#FFA500",
    },
    "mourning": {
        "name": "丧事风格（素雅黑白灰）",
        "card_style": {
            "max_width": "600px", "width": "100%",
            "bg": "#f5f5f5", "border_radius": "8px",
            "shadow": "0 2px 8px rgba(0,0,0,0.04)",
            "padding": "28px",
            "border": "1px solid #dddddd",
        },
        "font": "SimSun, serif",
        "primary": "#333333", "secondary": "#666666",
    },
    "tech": {
        "name": "技术风格（代码样式）",
        "card_style": {
            "max_width": "1200px", "width": "100%",
            "bg": "#f8f9fa", "border_radius": "4px",
            "shadow": "0 2px 8px rgba(0,0,0,0.06)",
            "padding": "24px",
            "border": "1px solid #d0d8e0",
        },
        "font": "Consolas, 'Courier New', monospace",
        "primary": "#2D3436", "secondary": "#636E72",
    },
}

# ══════════════════════════════════════════════════════
# Grid Spec 默认包装器
# ══════════════════════════════════════════════════════

DEFAULT_CARD_STYLE = {
    "max_width": "400px",
    "width": "100%",
    "bg": "rgba(255,255,255,0.82)",
    "backdrop": "blur(25px)",
    "webkit_backdrop": "blur(25px)",
    "border_radius": "36px",
    "shadow": "0 20px 35px -8px rgba(0,0,0,0.15), 0 4px 12px rgba(0,0,0,0.05), inset 0 1px 1px rgba(255,255,255,0.7)",
    "padding": "24px 20px 28px 20px",
    "border": "1px solid rgba(255,255,255,0.4)",
}

def css_dict_to_str(css_dict):
    """Convert dict of CSS properties to inline style string"""
    return "; ".join(f"{k}: {v}" for k, v in css_dict.items())

def merge_css_dicts(*dicts):
    """Merge multiple CSS dicts; later dicts override earlier ones"""
    result = {}
    for d in dicts:
        if d:
            result.update(d)
    return result

def resolve_base_modules(base_names):
    """Resolve base module names to combined CSS dict"""
    css = {}
    for name in base_names:
        if name in BASE_MODULES:
            mod = BASE_MODULES[name]
            if mod["type"] == "css":
                css.update(mod["css"])
        else:
            print(f"  [WARN] Unknown base module: {name}")
    return css

def composite_inline_css(composite_name, cell_config=None):
    """Get inline CSS from composite module's base modules and cell overrides"""
    mod = COMPOSITE_MODULES.get(composite_name, {})
    base_names = mod.get("base", [])
    cell_base = (cell_config or {}).get("base", [])
    css = resolve_base_modules(base_names + cell_base)
    # Cell-level style overrides
    cell_style = (cell_config or {}).get("style", {})
    css.update(cell_style)
    return css

# ══════════════════════════════════════════════════════
# 内置模板定义
# ══════════════════════════════════════════════════════

BUILTIN_TEMPLATES = {
    "harmony-app": {
        "name": "App推广卡片（毛玻璃风格）",
        "desc": "通用APP推广模板：头部图标 → 主标题 → 二维码 → 特性 → 脚注",
        "card_style": DEFAULT_CARD_STYLE,
        "grid": {"rows": 6, "cols": 1, "gap": "0",
            "cells": [
                {"id": "header", "row": 0, "col": 0, "module": "composite:header-entity"},
                {"id": "title",  "row": 1, "col": 0, "module": "composite:main-title"},
                {"id": "qr",     "row": 2, "col": 0, "module": "composite:qr-card"},
                {"id": "features","row": 3, "col": 0, "module": "composite:feature-panel"},
                {"id": "footer", "row": 4, "col": 0, "module": "composite:footer-caption"},
                {"id": "note",   "row": 5, "col": 0, "module": "composite:small-note"},
            ],
        },
    },
    "harmony-dual": {
        "name": "双端推广卡片（应用+元服务/双实体）",
        "desc": "通用双实体推广模板：左应用右服务 → 主标题 → 双二维码 → 通信/对比面板 → 脚注",
        "card_style": DEFAULT_CARD_STYLE,
        "grid": {"rows": 6, "cols": 1, "gap": "0",
            "cells": [
                {"id": "dual-header", "row": 0, "col": 0, "module": "composite:header-dual"},
                {"id": "title",       "row": 1, "col": 0, "module": "composite:main-title"},
                {"id": "qr-dual",     "row": 2, "col": 0, "module": "composite:qr-dual"},
                {"id": "comms",       "row": 3, "col": 0, "module": "composite:comms-panel"},
                {"id": "footer",      "row": 4, "col": 0, "module": "composite:footer-caption"},
                {"id": "note",        "row": 5, "col": 0, "module": "composite:small-note"},
            ],
        },
    },
    "calendar-dashboard": {
        "name": "动态周历·假日区间管理仪表板（完整交互版）",
        "desc": "完全交互式：年份控制、周末规则、假日区间CRUD、补班管理、周历视图、总工日统计",
        "source": "智能周历系统（用户模板泛化）",
        "file": "scripts/templates/calendar-dashboard-interactive.json",
        "card_style": {
            "max_width": "1600px",
            "width": "100%",
            "bg": "#eef2f7",
            "border_radius": "28px",
            "shadow": "0 20px 35px -12px rgba(0,0,0,0.12)",
            "padding": "24px 28px 36px",
        },
        "grid": {"rows": 5, "cols": 3, "gap": "16px",
            "cells": [{"id":"header","row":0,"col":0,"colspan":3,"html":"<div>📅 动态周历</div>"}]*3 + [{"id":"stat","row":2,"col":0,"colspan":3,"html":"<div>🏆 总工日</div>"}],
        },
    },
    "promo": {
        "name": "活动宣传面板",
        "desc": "渐变头部 + 卡片网格（原promo模板）",
        "card_style": {
            "max_width": "1200px", "width": "100%",
            "bg": "#ffffff", "border_radius": "12px",
            "shadow": "0 4px 20px rgba(0,0,0,0.08)",
            "padding": "20px",
        },
        "grid": {"rows": 3, "cols": 3, "gap": "20px",
            "cells": [
                {"id": "header", "row": 0, "col": 0, "colspan": 3,
                 "module": "composite:text-block",
                 "style": {"text-align":"center","background":"linear-gradient(135deg,#6C63FF 0%,#3F51B5 100%)","color":"white","padding":"40px 20px","border-radius":"12px 12px 0 0","margin":"-20px -20px 0 -20px"}},
                {"id": "card1", "row": 1, "col": 0,
                 "style": {"background":"#f8f9fa","padding":"24px","border-radius":"10px","border-top":"3px solid #6C63FF"}},
                {"id": "card2", "row": 1, "col": 1,
                 "style": {"background":"#f8f9fa","padding":"24px","border-radius":"10px","border-top":"3px solid #6C63FF"}},
                {"id": "card3", "row": 1, "col": 2,
                 "style": {"background":"#f8f9fa","padding":"24px","border-radius":"10px","border-top":"3px solid #6C63FF"}},
                {"id": "footer", "row": 2, "col": 0, "colspan": 3,
                 "style": {"text-align":"center","padding":"20px","border-top":"1px solid #eee","color":"#999","font-size":"0.9em"}},
            ],
        },
    },
}

# ══════════════════════════════════════════════════════
# HTML 生成逻辑
# ══════════════════════════════════════════════════════

def get_cells(spec):
    """Get cells list from spec, supporting both top-level and grid.cells locations"""
    cells = spec.get("cells", [])
    if not cells:
        cells = spec.get("grid", {}).get("cells", [])
    return cells

def collect_all_css(template_spec):
    """Collect all CSS from composite modules used in this template"""
    styles = []
    cells = get_cells(template_spec)
    grid_def = template_spec.get("grid", {})

    # Apply style_preset if specified
    preset_name = template_spec.get("style_preset", "")
    if preset_name and preset_name in STYLE_PRESETS:
        preset = STYLE_PRESETS[preset_name]
        card_style = template_spec.get("card_style", {})
        # Merge preset card_style (preset values are defaults, spec values override)
        merged = {**preset["card_style"], **card_style}
        template_spec["card_style"] = merged
        # Add preset font family to body
        preset_font = preset.get("font", "")
        if preset_font:
            template_spec["_preset_font"] = preset_font
    else:
        template_spec["_preset_font"] = ""

    # Global grid CSS
    rows = grid_def.get("rows", 1)
    cols = grid_def.get("cols", 1)
    gap = grid_def.get("gap", "0")

    # Body background: use card bg if solid color, else default light
    card = template_spec.get("card_style", DEFAULT_CARD_STYLE)
    card_bg = card.get("bg", "#f5f7fa")
    body_bg = card_bg if card_bg.startswith("#") else ("#000" if "backdrop" in card else "#eef2f7")
    preset_font = template_spec.get("_preset_font", "system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif")
    styles.append(f"body {{ margin:0; padding:0; background:{body_bg}; display:flex; align-items:center; justify-content:center; min-height:100vh; font-family:{preset_font}; }}")

    # Card style (skip backdrop-filter/border unless explicitly set — avoids clipping)
    card_css_parts = [
        f"max-width: {card.get('max_width','400px')};",
        f"width: {card.get('width','100%')};",
        f"background: {card.get('bg','rgba(255,255,255,0.82)')};",
        f"border-radius: {card.get('border_radius','36px')};",
        f"box-shadow: {card.get('shadow','0 20px 35px -8px rgba(0,0,0,0.15)')};",
        f"padding: {card.get('padding','24px 20px 28px 20px')};",
        "margin: 0 auto;",
        "overflow: hidden;",
        "transition: transform 0.2s ease;",
    ]
    if "backdrop" in card:
        card_css_parts.append(f"backdrop-filter: {card['backdrop']};")
    if "webkit_backdrop" in card:
        card_css_parts.append(f"-webkit-backdrop-filter: {card['webkit_backdrop']};")
    if "border" in card:
        card_css_parts.append(f"border: {card['border']};")
    else:
        card_css_parts.append("border: none;")

    card_css = ".grid-card {\n  " + "\n  ".join(card_css_parts) + "\n}\n.grid-card:hover { transform:scale(1.01); }\n"

    # Grid container
    container_css = f"""
.grid-container {{
  display: grid;
  grid-template-columns: repeat({cols}, 1fr);
  grid-template-rows: auto;
  gap: {gap};
}}
"""
    styles.append(card_css)
    styles.append(container_css)

    # Cell positions
    for cell in cells:
        r = cell.get("row", 0) + 1
        c = cell.get("col", 0) + 1
        rs = cell.get("rowspan", 1)
        cs = cell.get("colspan", 1)
        cell_id = cell.get("id", f"cell-{r}-{c}")

        pos_css = f"#cell-{cell_id} {{ grid-row: {r} / span {rs}; grid-column: {c} / span {cs}; }}"

        # Cell-level style: if cell has a "style" dict, use it directly (avoids duplicate properties)
        cell_style = cell.get("style", {})
        if cell_style:
            pos_css += f"\n#cell-{cell_id} {{ {css_dict_to_str(cell_style)} }}"
        else:
            cell_bg = cell.get("bg", "transparent")
            cell_pad = cell.get("padding", "4px")
            pos_css += f"\n#cell-{cell_id} {{ background:{cell_bg}; padding:{cell_pad}; }}"

        styles.append(pos_css)

    # Composite module CSS
    seen_modules = set()
    for cell in cells:
        module_name = cell.get("module", "")
        if module_name.startswith("composite:"):
            mname = module_name.split(":", 1)[1]
            if mname in COMPOSITE_MODULES and mname not in seen_modules:
                mod_css = COMPOSITE_MODULES[mname].get("css", "")
                if mod_css:
                    styles.append(mod_css)
                    seen_modules.add(mname)

    # Animation keyframes
    styles.append("""
@keyframes gridFadeIn { from { opacity:0; transform:translateY(20px); } to { opacity:1; transform:translateY(0); } }
@keyframes gridSlideIn { from { opacity:0; transform:translateX(-30px); } to { opacity:1; transform:translateX(0); } }
* { margin:0; padding:0; box-sizing:border-box; }
.edit-text { border:1px dashed transparent; padding:2px 4px; min-height:1em; outline:none; }
.edit-text:hover { border-color:#aaa; background:rgba(108,99,255,0.05); }
.edit-text:focus { border-color:#6C63FF; background:white; }
""")

    return "\n".join(styles)

def build_cell_html(template_spec):
    """Build HTML for each cell in the grid (支持组件式和旧模块格式)"""
    cells = get_cells(template_spec)
    parts = []

    # 导入组件引擎
    try:
        from module_assembler import render_cell_content, cell_constraint_css
        _HAVE_COMPONENT_ENGINE = True
    except Exception:
        _HAVE_COMPONENT_ENGINE = False

    for cell in cells:
        cell_id = cell.get("id", "cell-x")
        module_name = cell.get("module", "")
        raw_html = cell.get("html", "")
        components = cell.get("components", None)

        # 优先级1：组件式 → 使用 module_assembler
        if components and _HAVE_COMPONENT_ENGINE:
            content = render_cell_content(cell, cell_id)
        # 优先级2：旧格式 raw HTML
        elif raw_html:
            content = raw_html
        # 优先级3：旧格式 composite module
        elif module_name.startswith("composite:"):
            mname = module_name.split(":", 1)[1]
            mod = COMPOSITE_MODULES.get(mname, {})
            content = mod.get("template", f"<div data-field='{cell_id}'>[{mname}]</div>")
        else:
            content = f'<div data-field="{cell_id}" class="edit-text">[{cell_id}]</div>'

        # 约束CSS
        constraint_css = ""
        if _HAVE_COMPONENT_ENGINE and cell.get("constraint"):
            constraint_css = cell_constraint_css(cell)
        elif _HAVE_COMPONENT_ENGINE and components:
            constraint_css = cell_constraint_css(cell)

        cell_html = f'<div id="cell-{cell_id}" class="grid-cell" style="{constraint_css}">{content}</div>'
        parts.append(cell_html)

    return "\n".join(parts)

def generate_html(template_spec):
    """Generate complete HTML from template spec"""
    # Pre-generation grid validation
    grid = template_spec.get("grid", {})
    rows = grid.get("rows", 0)
    cols = grid.get("cols", 0)
    if rows < 1 or cols < 1:
        print("[ERROR] Grid spec 缺少有效的 rows/cols")
        return "<html><body><p>Grid 规格错误</p></body></html>"

    all_css = collect_all_css(template_spec)
    body = build_cell_html(template_spec)
    custom_scripts = template_spec.get("scripts", "")
    if custom_scripts.strip():
        custom_scripts = "\n<script>\n" + custom_scripts + "\n</script>\n"

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{template_spec.get('name','Grid HTML')}</title>
<style>
{all_css}
</style>
</head>
<body>
<div class="grid-card">
<div class="grid-container">
{body}
</div>
</div>

<!-- Editor toolbar -->
<div id="editor-bar" style="display:none;position:fixed;top:0;left:0;right:0;background:#1e1e2e;color:white;padding:6px 14px;z-index:9999;font-size:13px;gap:8px;align-items:center;flex-wrap:wrap;box-shadow:0 2px 12px rgba(0,0,0,0.3);">
  <span style="color:#6C63FF;font-weight:bold;font-size:12px;">🛠️</span>

  <button onclick="execCmd('bold')" title="粗体" style="background:#333;color:#fff;border:1px solid #666;padding:3px 8px;border-radius:4px;cursor:pointer;font-weight:bold;font-size:12px;">B</button>
  <button onclick="execCmd('italic')" title="斜体" style="background:#333;color:#fff;border:1px solid #666;padding:3px 8px;border-radius:4px;cursor:pointer;font-style:italic;font-size:12px;">I</button>
  <button onclick="execCmd('underline')" title="下划线" style="background:#333;color:#fff;border:1px solid #666;padding:3px 8px;border-radius:4px;cursor:pointer;text-decoration:underline;font-size:12px;">U</button>

  <select id="editor-font-family" onchange="applyFontFamily()" title="字体" style="background:#333;color:#fff;border:1px solid #666;padding:2px 4px;border-radius:4px;font-size:11px;max-width:110px;">
    <option value="">字体</option>
    <option value="system-ui, -apple-system, sans-serif">系统默认</option>
    <option value="'Microsoft YaHei', sans-serif">微软雅黑</option>
    <option value="'PingFang SC', sans-serif">苹方</option>
    <option value="SimSun, serif">宋体</option>
    <option value="SimHei, sans-serif">黑体</option>
    <option value="'Noto Sans SC', sans-serif">Noto Sans</option>
    <option value="Consolas, monospace">Consolas 等宽</option>
    <option value="'Courier New', monospace">Courier</option>
  </select>

  <select id="editor-font-weight" onchange="applyFontWeight()" title="字重" style="background:#333;color:#fff;border:1px solid #666;padding:2px 4px;border-radius:4px;font-size:11px;width:60px;">
    <option value="">字重</option>
    <option value="100">100 细</option>
    <option value="300">300 轻</option>
    <option value="400">400 常规</option>
    <option value="500">500 中</option>
    <option value="600">600 半粗</option>
    <option value="700">700 粗</option>
    <option value="900">900 超粗</option>
  </select>

  <select id="editor-font-size" onchange="applyFontSize()" title="字号" style="background:#333;color:#fff;border:1px solid #666;padding:2px 4px;border-radius:4px;font-size:11px;width:55px;">
    <option value="">字号</option>
    <option value="9">9px</option>
    <option value="11">11px</option>
    <option value="12">12px</option>
    <option value="13">13px</option>
    <option value="14">14px</option>
    <option value="15">15px</option>
    <option value="16">16px</option>
    <option value="18">18px</option>
    <option value="20">20px</option>
    <option value="24">24px</option>
    <option value="28">28px</option>
    <option value="32">32px</option>
    <option value="36">36px</option>
    <option value="48">48px</option>
  </select>

  <label title="字色" style="color:#ccc;font-size:11px;display:inline-flex;align-items:center;gap:2px;">🎨<input type="color" id="editor-font-color" value="#333333" onchange="applyFontColor()" style="width:22px;height:22px;border:none;cursor:pointer;padding:0;"></label>

  <div style="flex:1;"></div>
  <button onclick="previewHTML()" style="background:#3F51B5;color:#fff;border:none;padding:4px 10px;border-radius:4px;cursor:pointer;font-size:11px;">👁️ 预览</button>
  <button onclick="exportHTML()" style="background:#00B894;color:#fff;border:none;padding:4px 12px;border-radius:4px;cursor:pointer;font-weight:bold;font-size:11px;">✅ 生成</button>
  <button onclick="closeEditor()" style="background:#E17055;color:#fff;border:none;padding:3px 8px;border-radius:4px;cursor:pointer;font-size:11px;">❌</button>
</div>

<script>
let editMode = false;
function enableEditor() {{
  editMode = true;
  document.getElementById('editor-bar').style.display = 'flex';
  document.querySelectorAll('[data-field]').forEach(el => {{
    el.setAttribute('contenteditable', 'true');
    el.classList.add('edit-text');
  }});
  // Mark images as clickable
  document.querySelectorAll('img.editable-img').forEach(img => {{
    img.style.outline = '2px dashed #FF6584';
    img.style.outlineOffset = '2px';
    img.style.cursor = 'pointer';
  }});
}}
function closeEditor() {{
  editMode = false;
  document.getElementById('editor-bar').style.display = 'none';
  document.querySelectorAll('[data-field]').forEach(el => {{
    el.removeAttribute('contenteditable');
    el.classList.remove('edit-text');
  }});
  document.querySelectorAll('img.editable-img').forEach(img => {{
    img.style.outline = '';
    img.style.cursor = '';
  }});
}}
function execCmd(cmd) {{ document.execCommand(cmd); }}
function previewHTML() {{
  const clone = document.querySelector('.grid-card').cloneNode(true);
  clone.querySelectorAll('[contenteditable]').forEach(el => el.removeAttribute('contenteditable'));
  clone.querySelectorAll('.edit-text').forEach(el => {{ el.style.border = ''; el.style.background = ''; }});
  const w = window.open('', '_blank');
  w.document.write('<!DOCTYPE html>\\n' + clone.outerHTML);
  w.document.close();
}}
// Get the currently focused editable element
function getActiveEditorElement() {{
  const sel = window.getSelection();
  if (sel && sel.rangeCount > 0) {{
    let node = sel.getRangeAt(0).startContainer;
    while (node && node.nodeType === 3) node = node.parentNode;
    return node ? node.closest('[data-field]') || node.closest('[contenteditable]') : null;
  }}
  return null;
}}
function applyFontFamily() {{
  const el = getActiveEditorElement();
  if (!el) return;
  el.style.fontFamily = document.getElementById('editor-font-family').value;
}}
function applyFontWeight() {{
  const el = getActiveEditorElement();
  if (!el) return;
  el.style.fontWeight = document.getElementById('editor-font-weight').value;
}}
function applyFontSize() {{
  const el = getActiveEditorElement();
  if (!el) return;
  el.style.fontSize = document.getElementById('editor-font-size').value;
}}
function applyFontColor() {{
  const el = getActiveEditorElement();
  if (!el) return;
  el.style.color = document.getElementById('editor-font-color').value;
}}
function replaceImage(imgEl) {{
  const url = prompt('输入图片URL（或留空用占位图）：', imgEl.src || '');
  if (url === null) return;
  if (url.trim() === '') {{
    imgEl.src = 'data:image/svg+xml,%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 width=%27200%27 height=%27200%27%3E%3Crect fill=%27%23ddd%27 width=%27200%27 height=%27200%27/%3E%3Ctext x=%2750%25%27 y=%2750%25%27 text-anchor=%27middle%27 fill=%27%23999%27 font-size=%2716%27%3E点击换图%3C/text%3E%3C/svg%3E';
  }} else {{
    imgEl.src = url;
  }}
}}
// Make images clickable
document.addEventListener('click', function(e) {{
  const target = e.target.closest('img.editable-img');
  if (target && editMode) {{
    e.preventDefault();
    e.stopPropagation();
    replaceImage(target);
  }}
}});
// Drag & drop image onto editable-img elements
document.addEventListener('dragover', function(e) {{
  const target = e.target.closest('img.editable-img');
  if (target && editMode) {{
    e.preventDefault();
    e.dataTransfer.dropEffect = 'copy';
    target.style.outline = '3px solid #00B894';
  }}
}});
document.addEventListener('dragleave', function(e) {{
  const target = e.target.closest('img.editable-img');
  if (target) {{
    target.style.outline = '2px dashed #FF6584';
  }}
}});
document.addEventListener('drop', function(e) {{
  e.preventDefault();
  const target = e.target.closest('img.editable-img');
  if (!target || !editMode) return;
  const file = e.dataTransfer.files[0];
  if (!file || !file.type.startsWith('image/')) {{
    alert('请拖入图片文件');
    return;
  }}
  // Read file as data URL
  const reader = new FileReader();
  reader.onload = function(ev) {{
    target.src = ev.target.result;
    target.style.outline = '2px dashed #FF6584';
    console.log('[Editor] 图片已通过拖放替换');
  }};
  reader.readAsDataURL(file);
}});
function exportHTML() {{
  // Generate clean HTML by cloning and stripping editing UI
  const clone = document.querySelector('.grid-card').cloneNode(true);
  clone.querySelectorAll('[contenteditable]').forEach(el => el.removeAttribute('contenteditable'));
  clone.querySelectorAll('.edit-text').forEach(el => {{
    el.style.border = '';
    el.style.background = '';
  }});
  const cleanHtml = '<!DOCTYPE html>\\n' + clone.outerHTML;
  const blob = new Blob([cleanHtml], {{type:'text/html'}});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'final.html';
  a.click();
  alert('✅ 最终HTML已生成！');
  closeEditor();
}}
document.addEventListener('keydown', e => {{
  if (e.ctrlKey && e.key === 'e') {{ e.preventDefault(); editMode ? closeEditor() : enableEditor(); }}
}});
console.log('💡 提示：按 Ctrl+E 进入/退出编辑模式 | 点击图片输入链接 | 拖拽图片文件到图片上替换');
</script>

<!-- Custom scripts from spec -->
{custom_scripts}
</body>
</html>"""
    # Post-generation audit (pass silent for initial generation)
    audit_passed = print_audit_report(html, template_spec, silent=True)
    if not audit_passed:
        print("[WARN] 审计发现严重问题，请检查生成的 HTML")
    print_generation_guide(template_spec)
    return html

def print_generation_guide(spec=None):
    """强制输出的生成说明 — 每次生成后必须调用"""
    name = spec.get("name", "") if spec else ""
    grid = spec.get("grid", {}) if spec else {}
    n_cells = len(grid.get("cells", []))
    rs = grid.get("rows", "?")
    cs = grid.get("cols", "?")
    style_preset = spec.get("style_preset", "") if spec else ""

    lines = []
    lines.append("=" * 58)
    if name:
        lines.append(f"  [OK] 生成完成: {name}")
    else:
        lines.append("  [OK] HTML 生成完成")
    lines.append("=" * 58)
    lines.append("")
    lines.append("  [编辑] 浏览器打开 HTML 后按 Ctrl+E 进入编辑模式:")
    lines.append("     文字 -> 点击直接编辑     图片 -> 点击输入URL / 拖放文件替换")
    lines.append("     字体 -> 选字体家族/字重   字号/字色 -> 调字号/选颜色")
    lines.append("     完成 -> Ctrl+S 或点 [生成] 按钮")
    lines.append("")
    lines.append("  [创作模式]")
    lines.append("     骨架创作  -> 定 NxM 网格 -> 选模块放入格子 -> 填充内容")
    lines.append("     自由创作  -> AI 参考模块库直接写 HTML -> 填充内容")
    lines.append("")
    lines.append("  [审计] 两种模式均自动执行 -- 保证:")
    lines.append("     1. HTML 结构完整 (DOCTYPE/标签平衡/闭合)")
    lines.append("     2. 网格定义正确 (无越界/无重叠)")
    lines.append("     3. 编辑功能可用 (data-field 标记/svg占位图)")
    lines.append("     4. 渲染无风险 (backdrop-filter 裁剪/背景色异常)")
    lines.append("     5. 与技能要求一致 (模块引用有效/CSS平衡)")
    lines.append("")
    lines.append("  [可用资源] (命令行)")
    lines.append("     --list-templates     查看预置方案模板")
    lines.append("     --list-modules       查看模块列表")
    lines.append("     --list-presets       查看样式预设")
    lines.append("     --save-as <名>       固化当前方案为用户模板")
    lines.append("     --export-interfaces  导出接口定义供 AI 参考")
    lines.append("")
    if style_preset:
        lines.append(f"  [当前样式] {style_preset}")
    lines.append(f"  [当前网格] {rs}x{cs}, {n_cells} 格")
    lines.append("=" * 58)

    msg = "\n" + "\n".join(lines) + "\n"
    try:
        print(msg)
    except UnicodeEncodeError:
        # Fallback for terminals without full Unicode support
        print(msg.encode("ascii", errors="replace").decode("ascii"))

# ══════════════════════════════════════════════════════
# 主入口
# ══════════════════════════════════════════════════════

def list_modules():
    """Print all available modules (base + composite)"""
    print("=== Base Modules (CSS Primitives) ===")
    for name, info in BASE_MODULES.items():
        cat = "css"
        desc = info.get("desc", "")
        print(f"  base:{name} — {desc} [{cat}]")

    print("\n=== Composite Modules (可复用组件) ===")
    for name, info in COMPOSITE_MODULES.items():
        bases = info.get("base", [])
        base_str = ", ".join(bases) if bases else "—"
        print(f"  composite:{name} — {info['desc']}")
        print(f"    引用 base: {base_str}")

def list_templates():
    """Print all built-in templates"""
    print("=== 内置模板 (Grid Spec) ===")
    for name, spec in BUILTIN_TEMPLATES.items():
        grid = spec.get("grid", {})
        cells = grid.get("cells", [])

        # For file-based templates, try to load the actual file for accurate info
        file_name = spec.get("file", "")
        if file_name:
            file_path = SKILL_DIR / file_name
            if file_path.exists():
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        file_spec = json.load(f)
                    file_grid = file_spec.get("grid", {})
                    file_cells = file_grid.get("cells", [])
                    grid = file_grid
                    cells = file_cells
                except Exception:
                    pass

        source = spec.get("source", "")
        src_info = f"  [来源: {source}]" if source else ""
        has_js = spec.get("file", "").endswith(".json") and cells
        js_tag = " [交互JS]" if has_js else ""
        print(f"  {name}: {spec['name']} ({grid.get('rows','?')}×{grid.get('cols','?')}, {len(cells)} cells){src_info}{js_tag}")
        print(f"    {spec['desc']}")

    # Also list user templates
    list_user_templates()

def load_grid_spec(spec_path_or_name):
    """Load grid spec from file or built-in template name"""
    p = Path(spec_path_or_name)
    if p.exists():
        spec = safe_read_json(p)
        if spec is None:
            sys.exit(1)
        return spec

    # Check built-in templates
    if spec_path_or_name in BUILTIN_TEMPLATES:
        entry = BUILTIN_TEMPLATES[spec_path_or_name]
        # Support file-based built-in templates (e.g., the interactive calendar)
        if "file" in entry:
            file_path = SKILL_DIR / entry["file"]
            if file_path.exists():
                spec = safe_read_json(file_path)
                if spec is None:
                    show_error("模板错误", f"内置模板 '{spec_path_or_name}' 引用的文件损坏: {file_path}")
                    sys.exit(1)
                # Merge card_style and other metadata from the entry
                for key in ["name", "desc", "source", "card_style"]:
                    if key in entry and key not in spec:
                        spec[key] = entry[key]
                return spec
            else:
                show_error("文件错误", f"内置模板 '{spec_path_or_name}' 引用的文件不存在: {file_path}",
                           "这可能是技能安装不完整。尝试重新安装 hug-html 技能。")
                # Fallback: use built-in entry without external file
                return entry

        return entry

    # Check user templates directory
    user_file = USER_TEMPLATES_DIR / f"{spec_path_or_name}.json"
    if user_file.exists():
        spec = safe_read_json(user_file)
        if spec:
            return spec
        show_error("模板错误", f"用户模板 '{spec_path_or_name}' 解析失败",
                   f"请检查文件格式: {user_file}")

    # Not found anywhere — print helpful message and exit
    msg_lines = [
        "",
        "[模板/文件错误] 找不到模板或 Spec 文件: " + spec_path_or_name,
        "  可用内置模板:",
    ]
    for t in BUILTIN_TEMPLATES:
        msg_lines.append(f"    {t}")
    user_files = sorted(USER_TEMPLATES_DIR.glob("*.json"))
    if user_files:
        msg_lines.append("  用户自定义模板:")
        for f in user_files:
            msg_lines.append(f"    {f.stem}")
    msg_lines.append("  [提示] 使用 --list-templates 查看所有模板, 使用 --list-modules 查看模块")
    try:
        print(f"\n❌ 找不到模板或 Spec 文件: {spec_path_or_name}")
        print("  可用内置模板:")
        for t in BUILTIN_TEMPLATES:
            print(f"    {t}")
        user_files = sorted(USER_TEMPLATES_DIR.glob("*.json"))
        if user_files:
            print("  用户自定义模板:")
            for f in user_files:
                print(f"    {f.stem}")
        print("  💡 提示: 使用 --list-templates 查看所有模板, 使用 --list-modules 查看模块")
    except UnicodeEncodeError:
        print("\n".join(msg_lines))
    sys.exit(1)

def save_template(template_spec, name):
    """Save template spec to scripts/templates/ directory (built-in)"""
    BUILTIN_TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)
    out = BUILTIN_TEMPLATES_DIR / f"{name}.json"
    try:
        content = json.dumps(template_spec, ensure_ascii=False, indent=2)
        if safe_write_text(out, content, f"模板 {name}"):
            print(f"[OK] 模板已保存: {out}")
            return str(out)
    except Exception as e:
        show_error("文件错误", f"保存模板失败: {e}")
    return ""

def save_user_template(template_spec, name, description=""):
    """Save a grid spec as a user-defined template (方案模板)"""
    USER_TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)
    spec = dict(template_spec)
    spec["_type"] = "user_template"
    spec["_version"] = 1
    if description:
        spec["desc"] = description
    if "name" not in spec or not spec.get("name"):
        spec["name"] = name
    out = USER_TEMPLATES_DIR / f"{name}.json"
    # Version check - don't overwrite without incrementing
    if out.exists():
        try:
            with open(out, "r", encoding="utf-8") as f:
                existing = json.load(f)
            spec["_version"] = existing.get("_version", 1) + 1
        except Exception:
            spec["_version"] = 1
    try:
        content = json.dumps(spec, ensure_ascii=False, indent=2)
        if safe_write_text(out, content, f"用户模板 {name}"):
            print(f"[OK] 方案模板已固化: {out}")
            print(f"  名称: {name}")
            print(f"  版本: v{spec['_version']}")
            grid = spec.get("grid", {})
            print(f"  网格: {grid.get('rows','?')}×{grid.get('cols','?')}, {len(grid.get('cells',[]))} cells")
            return str(out)
    except Exception as e:
        show_error("文件错误", f"保存用户模板失败: {e}")
    return ""

def list_user_templates():
    """List all user-defined templates"""
    USER_TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)
    files = sorted(USER_TEMPLATES_DIR.glob("*.json"))
    if not files:
        print("  (暂无用户自定义方案模板)")
        return
    print("=== 用户方案模板 ===")
    for f in files:
        try:
            with open(f, "r", encoding="utf-8") as fh:
                spec = json.load(fh)
            name = spec.get("name", f.stem)
            desc = spec.get("desc", "")
            grid = spec.get("grid", {})
            ver = spec.get("_version", 1)
            n_cells = len(grid.get("cells", []))
            print(f"  {f.stem}: {name} (v{ver}, {grid.get('rows','?')}×{grid.get('cols','?')}, {n_cells} cells)")
            if desc:
                print(f"    {desc}")
        except Exception:
            print(f"  {f.stem}: (文件无法解析)")

def export_interfaces():
    """Export complete interface specification as JSON for LLM consumption"""
    return {
        "_schema_version": "2.0.0",
        "interfaces": {
            "grid_spec": {
                "desc": "方案模板 / Grid Spec — 骨架结构+骨架样式+模块分配的完整定义",
                "schema": {
                    "name": "模板名称",
                    "desc": "模板描述",
                    "style_preset": "可选: business / academic / festive / mourning / tech",
                    "card_style": {
                        "max_width": "卡片最大宽度, 如'400px'",
                        "bg": "背景色/渐变, 如 '#ffffff' / 'rgba(...)' / 'linear-gradient(...)'",
                        "border_radius": "圆角, 如 '36px'",
                        "shadow": "阴影CSS, 如 '0 4px 12px rgba(0,0,0,0.08)'",
                        "padding": "内边距, 如 '24px 20px'",
                        "backdrop": "毛玻璃: 'blur(25px)' (可选)",
                        "webkit_backdrop": "毛玻璃WebKit: 'blur(25px)' (可选)",
                        "border": "边框, 如 '1px solid rgba(...)' (可选)"
                    },
                    "grid": {
                        "rows": "行数 (int)",
                        "cols": "列数 (int)",
                        "gap": "格子间距, 如 '8px'",
                        "cells": [
                            {
                                "id": "单元格唯一ID",
                                "row": "行索引 (0-based)",
                                "col": "列索引 (0-based)",
                                "rowspan": "跨行数 (可选, 默认1)",
                                "colspan": "跨列数 (可选, 默认1)",
                                "module": "引用的复合模块, 如 'composite:header-entity'",
                                "html": "直接HTML内容 (与module二选一)",
                                "style": "单元格级CSS覆盖, 如 {'background':'#f5f5f5', 'padding':'16px'}"
                            }
                        ]
                    },
                    "scripts": "自定义JavaScript (可选)"
                }
            },
            "base_module": {
                "desc": "基础模块 / Base — CSS原语，作用于具体元素",
                "format": "base:模块名",
                "examples": {
                    "base:font-size-xl": "大标题 28px Semibold",
                    "base:color-dark": "深色文字 #1a2a3a",
                    "base:bg-gradient-purple": "粉紫渐变背景",
                    "base:radius-lg": "大圆角 24px",
                    "base:pad-md": "中间距 16x20",
                    "base:shadow-glass": "毛玻璃阴影",
                    "base:img-circle": "圆形图片裁剪",
                    "base:flex-center": "Flex居中",
                    "base:anim-fade": "淡入动画"
                }
            },
            "composite_module": {
                "desc": "复合模块 / Composite — 可复用HTML组件",
                "format": "composite:模块名",
                "list": {k: v["desc"] for k, v in COMPOSITE_MODULES.items()}
            },
            "style_preset": {
                "desc": "样式预设 — 一键切换配色和字体",
                "list": {k: v["name"] for k, v in STYLE_PRESETS.items()}
            }
        }
    }

# ══════════════════════════════════════════════════════
# 生成后审计
# ══════════════════════════════════════════════════════

def audit_html(html_str, template_spec=None):
    """
    生成后HTML审查：检查结构完整性和常见问题。
    返回 (passed: bool, issues: list)
    """
    issues = []

    # 1. 文档结构
    if '<!DOCTYPE html>' not in html_str:
        issues.append("[CRITICAL] 缺少 DOCTYPE 声明")
    if '<html' not in html_str.lower():
        issues.append("[CRITICAL] 缺少 <html> 标签")
    if '</html>' not in html_str:
        issues.append("[CRITICAL] 缺少 </html> 关闭标签")
    if '<body' not in html_str.lower():
        issues.append("[CRITICAL] 缺少 <body> 标签")
    if '</body>' not in html_str:
        issues.append("[WARN] 缺少 </body> 关闭标签")

    # 2. 标签平衡（排除 script/style 内容内的标签，用正则精确匹配）
    body_only = html_str.split("<body")[-1].split("</body>")[0] if "</body>" in html_str else html_str
    clean_body = re.sub(r'<script>.*?</script>', '', body_only, flags=re.DOTALL)
    clean_body = re.sub(r'<style>.*?</style>', '', clean_body, flags=re.DOTALL)
    for tag in ['div', 'table', 'tr', 'td', 'th', 'h1', 'h2', 'h3', 'p', 'span', 'ul', 'li', 'a', 'button']:
        opens = len(re.findall(rf'<{tag}(\s|>|/>)', clean_body))
        closes = len(re.findall(rf'</{tag}>', clean_body))
        diff = opens - closes
        if abs(diff) > 2:
            issues.append(f"[WARN] 标签 <{tag}> 可能不平衡 (开={opens}, 关={closes}, 差={diff})")

    # 3. data-field / data-module 引用
    if template_spec:
        cells = get_cells(template_spec)
        for cell in cells:
            module_name = cell.get("module", "")
            cell_id = cell.get("id", "")
            if module_name.startswith("composite:"):
                mname = module_name.split(":", 1)[1]
                if mname not in COMPOSITE_MODULES:
                    issues.append(f"[WARN] 单元格 '{cell_id}' 引用了未知模块 '{module_name}'")

    # 4. 检查 <img> 标签
    img_tags = html_str.count('<img')
    img_alts = len(re.findall(r'<img[^>]*alt=', html_str))
    if img_tags > 0 and img_alts < img_tags:
        issues.append(f"[WARN] 有 {img_tags - img_alts}/{img_tags} 个 <img> 缺少 alt 属性")

    # 5. 检查内联样式中的可疑属性
    suspicious = []
    for pat in ['position:absolute', 'position:fixed', 'z-index:9999']:
        if pat in html_str.lower():
            suspicious.append(pat)
    if suspicious:
        issues.append(f"[INFO] 检测到定位属性: {', '.join(suspicious)}（编辑工具栏使用，正常）")

    # 6. 检查样式块是否有效
    style_blocks = re.findall(r'<style>(.*?)</style>', html_str, re.DOTALL)
    for i, block in enumerate(style_blocks):
        if not block.strip():
            issues.append(f"[WARN] 样式块 #{i+1} 为空")
        # Check for unbalanced braces
        opens = block.count('{')
        closes = block.count('}')
        if opens != closes:
            issues.append(f"[WARN] 样式块 #{i+1} 花括号不平衡 ({{={opens}, }}={closes})")

    # 7. 检查脚本块
    script_blocks = re.findall(r'<script>(.*?)</script>', html_str, re.DOTALL)
    for i, block in enumerate(script_blocks):
        if not block.strip():
            issues.append(f"[WARN] 脚本块 #{i+1} 为空")

    # 8. 检查 meta viewport
    if '<meta name="viewport"' not in html_str:
        issues.append("[WARN] 缺少 viewport meta 标签")

    # 9. Grid spec 验证（仅当 template_spec 提供时）
    if template_spec:
        grid = template_spec.get("grid", {})
        rows = grid.get("rows", 0)
        cols = grid.get("cols", 0)
        cells = grid.get("cells", [])
        if rows > 0 and cols > 0 and cells:
            # 9a. 检查单元格是否越界
            occupied = {}
            for cell in cells:
                r = cell.get("row", 0)
                c = cell.get("col", 0)
                rs = cell.get("rowspan", 1)
                cs = cell.get("colspan", 1)
                if r + rs > rows:
                    issues.append(f"[WARN] 单元格 '{cell.get('id','?')}' rowspan({rs}) 超出网格边界({rows}行)")
                if c + cs > cols:
                    issues.append(f"[WARN] 单元格 '{cell.get('id','?')}' colspan({cs}) 超出网格边界({cols}列)")
                # 9b. 检查单元格是否重叠
                for rr in range(r, r + rs):
                    for cc in range(c, c + cs):
                        key = f"{rr},{cc}"
                        if key in occupied:
                            issues.append(f"[CRITICAL] 单元格 '{cell.get('id','?')}' 与 '{occupied[key]}' 在位置 ({rr},{cc}) 重叠")
                        else:
                            occupied[key] = cell.get("id", "?")

    # 10. 渲染风险检查
    # 10a. backdrop-filter 但无 overflow hidden → 内容可能裁剪
    if "backdrop-filter" in html_str and "overflow: hidden" not in html_str:
        issues.append("[WARN] backdrop-filter 使用但无 overflow:hidden，可能导致内容裁剪")

    # 10b. body 背景色异常
    body_bg_match = re.search(r'body\s*\{[^}]*background\s*:\s*(#[0-9a-fA-F]{3,6}|rgba?\([^)]+\))', html_str, re.DOTALL)
    if body_bg_match:
        bg = body_bg_match.group(1)
        if bg in ("#000", "#000000") and "backdrop-filter" not in html_str:
            issues.append("[INFO] body 背景为纯黑色，非毛玻璃模板建议用浅色背景")
        elif bg.startswith("rgba") and "backdrop-filter" not in html_str:
            issues.append("[WARN] body 使用半透明背景 bg 但无 backdrop-filter，显示可能不正常")

    # 10c. 检查 grid-card 内存在固定定位编辑工具栏 → 正常（INFO）
    if "position:fixed" in html_str and "editor-bar" in html_str:
        pass  # 正常，编辑器工具栏

    passed = len([i for i in issues if i.startswith("[CRITICAL]")]) == 0
    return passed, issues

def print_audit_report(html_str, template_spec=None, silent=False):
    """Print audit results. silent=True skips printing (for non-interactive use)."""
    if silent:
        return audit_html(html_str, template_spec)[0]
    passed, issues = audit_html(html_str, template_spec)
    try:
        print("\n=== HTML 生成后审查 ===")
        if not issues:
            print("  [OK] 全部通过，无问题")
        else:
            for issue in issues:
                print(f"  {issue}")
        print(f"  结果: {'[PASS] 通过' if passed else '[FAIL] 有严重问题'}")
    except UnicodeEncodeError:
        # Fallback for terminals that can't handle Unicode
        print("\n=== HTML Post-Generation Audit ===")
        if not issues:
            print("  [OK] All passed")
        else:
            for issue in issues:
                clean = issue.replace("[CRITICAL]", "[ERR]").replace("[WARN]", "[WARN]").replace("[INFO]", "[INFO]")
                print(f"  {clean}")
        print(f"  Result: {'[PASS]' if passed else '[FAIL]'}")
    return passed

def main():
    try:
        _main_impl()
    except SystemExit as e:
        # argparse 自身错误退出或正常退出 → 静默处理
        pass
    except KeyboardInterrupt:
        print("\n⚠️  用户中断操作")
    except Exception as e:
        show_error("内部错误", f"程序发生未预期的错误: {type(e).__name__}", "请检查参数是否正确。使用 --help 查看完整参数说明。")
        # 仅 debug 模式下输出详细堆栈
        if "--debug" in sys.argv:
            traceback.print_exc()

def _main_impl():
    ap = argparse.ArgumentParser(description="Grid-based HTML Module Engine")
    ap.add_argument("--spec", help="Path to grid spec JSON or built-in template name")
    ap.add_argument("--output", "-o", help="Output HTML file path")
    ap.add_argument("--list-modules", action="store_true", help="List all available modules")
    ap.add_argument("--list-templates", action="store_true", help="List all built-in templates")
    ap.add_argument("--demo", action="store_true", help="Quick demo mode")
    ap.add_argument("--template", help="Template name for demo")
    ap.add_argument("--save", help="Save built-in template to templates/ directory")
    ap.add_argument("--show-css", action="store_true", help="Show base module CSS for reference")
    ap.add_argument("--audit", help="Audit an existing HTML file", metavar="FILE")
    ap.add_argument("--list-presets", action="store_true", help="List available style presets")
    ap.add_argument("--save-as", help="Save current grid spec as user template (方案模板固化)", metavar="NAME")
    ap.add_argument("--list-user-templates", action="store_true", help="List user-defined templates")
    ap.add_argument("--export-interfaces", help="Export complete interface spec as JSON file", metavar="FILE")
    ap.add_argument("--desc", help="Description for --save-as", default="")
    ap.add_argument("--debug", action="store_true", help="显示详细错误堆栈（调试用）")

    args = ap.parse_args()

    if args.list_modules:
        list_modules()
        return

    if args.list_templates:
        list_templates()
        return

    if args.show_css:
        print("=== Base Module CSS Reference ===")
        for name, info in BASE_MODULES.items():
            css_str = css_dict_to_str(info["css"])
            print(f"  base:{name}")
            print(f"    {css_str}")
        return

    if args.list_presets:
        print("=== 样式预设 (Style Presets) ===")
        for name, preset in STYLE_PRESETS.items():
            cs = preset["card_style"]
            print(f"  {name}: {preset['name']}")
            print(f"    背景: {cs.get('bg','')}, 圆角: {cs.get('border_radius','')}")
            print(f"    字体: {preset.get('font','')}, 主色: {preset.get('primary','')}")
        return

    if args.audit:
        p = Path(args.audit)
        if not p.exists():
            show_error("文件错误", f"找不到 HTML 文件: {args.audit}")
            return
        html_str = p.read_text(encoding="utf-8")
        print_audit_report(html_str)
        return

    if args.list_user_templates:
        list_user_templates()
        return

    if args.export_interfaces:
        interfaces = export_interfaces()
        out = Path(args.export_interfaces)
        safe_write_text(out, json.dumps(interfaces, ensure_ascii=False, indent=2), "接口定义")
        print(f"[OK] 接口定义已导出: {out}")
        print(f"  Grid Spec 标准格式: 参考 interfaces.grid_spec.schema")
        print(f"  可用 Base 模块: {len(BASE_MODULES)} 个")
        print(f"  可用 Composite 模块: {len(COMPOSITE_MODULES)} 个")
        print(f"  可用样式预设: {len(STYLE_PRESETS)} 种")
        return

    # Save-as: 将当前 spec 保存为用户方案模板
    if args.save_as:
        if args.spec:
            spec = load_grid_spec(args.spec)
        elif args.demo and args.template in BUILTIN_TEMPLATES:
            spec = BUILTIN_TEMPLATES[args.template]
        else:
            show_error("参数错误", "--save-as 需要 --spec <模板名/路径> 或 --demo --template <内置模板名>",
                       "用法示例: python scripts/grid_builder.py --save-as my-template --spec harmony-app")
            return
        save_user_template(spec, args.save_as, args.desc)
        print_generation_guide(spec)
        return

    # Save built-in template
    if args.save:
        if args.save in BUILTIN_TEMPLATES:
            save_template(BUILTIN_TEMPLATES[args.save], args.save)
        else:
            show_error("模板错误", f"未知模板: {args.save}", f"可用模板: {', '.join(BUILTIN_TEMPLATES.keys())}")
        return

    # Demo mode
    if args.demo:
        tpl_name = args.template or "harmony-app"
        if tpl_name not in BUILTIN_TEMPLATES:
            show_error("模板错误", f"未知模板: {tpl_name}", f"可用模板: {', '.join(BUILTIN_TEMPLATES.keys())}")
            return
        spec = BUILTIN_TEMPLATES[tpl_name]
        out_path = args.output or str(OUTPUT_DIR / f"{tpl_name}.html")
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        html = generate_html(spec)
        safe_write_text(out_path, html, f"HTML {tpl_name}")
        print(f"[OK] 已生成: {out_path}")
        print(f"  模板: {spec['name']}")
        print(f"  网格: {spec['grid']['rows']}×{spec['grid']['cols']}")
        return

    # Normal mode: load spec → generate
    if not args.spec:
        ap.print_help()
        return

    spec = load_grid_spec(args.spec)
    out_path = args.output or str(OUTPUT_DIR / "output.html")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    html = generate_html(spec)
    safe_write_text(out_path, html, "HTML 输出")
    print(f"[OK] 已生成: {out_path}")

if __name__ == "__main__":
    main()
