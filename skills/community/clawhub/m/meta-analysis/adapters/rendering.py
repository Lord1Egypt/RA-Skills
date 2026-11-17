# -*- coding: utf-8 -*-
"""adapters/rendering.py — SVG 内联渲染工具（meta-analysis 技能，呈现层）。

将 coze 返回的 figures[].svg 转为可直接内嵌到对话流的标准 HTML fragment。

核心问题（实测 2026-08-19）：
  svglite 输出固定 viewBox（如 "0 0 504 360"），但内容可能**超出该区域**
  —— meta 包 forest() 把 Study/Events/OR/95%CI/Weight 列画在图形区外
  （x 可达 -140 / +644，宽度 785px）。按原 viewBox 渲染会被浏览器裁剪两侧文字。
  解决：content_bbox() 扫描内容元素极值，动态扩展 viewBox + 宽度。

规则（用户偏好，2026-08-19）：
  图固定原尺寸不缩放；容器装不下即出横向滚动条（overflow-x:auto）。

用法：
  from rendering import build_figure_widget
  html = build_figure_widget(figures, ["森林图 · OR", "漏斗图 · Egger"])
"""

from __future__ import annotations

import os
import re
import sys
import datetime
import html as _html

__all__ = ["extract_svg", "content_bbox", "build_figure_widget", "svg_to_png", "render_html_report"]

_Q = r"['\"]"  # svglite 用单引号属性，兼容双引号


def _num(v: str) -> float:
    """'39.34px' / '504.00' → 39.34 / 504.0"""
    return float(v.replace("px", "").strip())


def extract_svg(svg_str: str) -> tuple[str, str]:
    """从完整 SVG 字符串提取 (inner, viewbox)。兼容单/双引号属性。

    inner = <svg> 内部内容（供嵌入 <svg viewBox=...>），viewbox 为原值。
    """
    m = re.search(
        r"<svg[^>]*viewBox=['\"]([^'\"]+)['\"][^>]*>(.*)</svg>",
        svg_str,
        re.S,
    )
    if m:
        return (m.group(2), m.group(1))
    m = re.search(r"<svg[^>]*>(.*)</svg>", svg_str, re.S)
    if m:
        return (m.group(1), "0 0 504 360")
    return (svg_str, "0 0 504 360")


def content_bbox(
    svg_inner: str, vb: str = "0 0 504 360", pad: float = 8.0, pad_y: float = 24.0
) -> tuple[float, float, float, float]:
    """扫描 SVG 内容元素，返回 (min_x, min_y, max_x, max_y) 含 padding。

    pad 用于 x 方向（紧凑，避免图过宽）；pad_y 用于 y 方向（留白更多，
    森林图等绘图区上下贴近内容时保持呼吸空间，见用户偏好 2026-08-19）。
    覆盖元素：text（含 textLength/text-anchor 计算文本宽度；transform 文本解析
    translate 锚点双向扩展）、rect（跳过 width=100% 白底）、line、circle、
    polyline/polygon points、**path（解析 d 属性绝对坐标对）**。

    2026-08-28 加固：将计算结果与**原始 viewBox** 取并集（union）。依据——
    ① svglite 内容偶发超出 viewBox（如 forest 左右文字列 x∈[-140,644]），
      text 扫描已能捕获该溢出；
    ② 但 ggplot2 / 网络图主内容多为 <path>（曲线、edge），若未被上列元素类型
      完全捕获，union 原始 viewBox 可保证不裁掉 svglite 实际绘制的区域
      （设备坐标恒落在原 viewBox 内，除已知的负坐标溢出）。
    二者取并集 = 既不妨碍 forest 溢出扩展，也不因漏扫而裁图。
    无内容且无合法 viewBox 时回退原画布 (0, 0, 504, 360)。
    """
    xs: list[float] = []
    ys: list[float] = []

    # ---- text ----
    for m in re.finditer(r"<text\b([^>]*)>(.*?)</text>", svg_inner, re.S):
        attrs = m.group(1)
        tl = re.search(rf"textLength={_Q}([^'\"]+)", attrs)
        w = _num(tl.group(1)) if tl else 0.0
        tm = re.search(r"transform=['\"]([^'\"]+)['\"]", attrs)
        if tm:
            # transform 文本（如漏斗图 y 轴旋转标签）：取 translate 锚点，沿 x/y
            # 双向扩展 textLength（旋转方向不定，保守覆盖 → 保证不裁剪）
            t = re.search(
                r"translate\(\s*([-0-9.]+)\s*,\s*([-0-9.]+)\s*\)", tm.group(1)
            )
            if t:
                tx, ty = _num(t.group(1)), _num(t.group(2))
                xs += [tx - w, tx + w]
                ys += [ty - w, ty + w]
                continue
            continue  # 无 translate 的 transform（如纯 rotate）无法定位，跳过
        xm = re.search(rf"\bx={_Q}([^'\"]+)", attrs)
        ym = re.search(rf"\by={_Q}([^'\"]+)", attrs)
        if not xm or not ym:
            continue
        x, y = _num(xm.group(1)), _num(ym.group(1))
        an = re.search(rf"text-anchor={_Q}([^'\"]+)", attrs)
        anchor = an.group(1) if an else "start"
        if anchor == "start":
            x0, x1 = x, x + w
        elif anchor == "middle":
            x0, x1 = x - w / 2, x + w / 2
        else:  # end
            x0, x1 = x - w, x
        xs += [x0, x1]
        ys += [y, y]

    # ---- rect ----
    for m in re.finditer(r"<rect\b([^>]*)/?>", svg_inner):
        a = dict(re.findall(r"([a-zA-Z:_-]+)=['\"]([^'\"]*)['\"]", m.group(1)))
        if all(k in a for k in ("x", "y", "width", "height")) and a["width"] != "100%":
            x, y = _num(a["x"]), _num(a["y"])
            w, h = _num(a["width"]), _num(a["height"])
            xs += [x, x + w]
            ys += [y, y + h]

    # ---- line ----
    for m in re.finditer(r"<line\b([^>]*)/?>", svg_inner):
        a = dict(re.findall(r"([a-zA-Z:_-]+)=['\"]([^'\"]*)['\"]", m.group(1)))
        if all(k in a for k in ("x1", "y1", "x2", "y2")):
            xs += [_num(a["x1"]), _num(a["x2"])]
            ys += [_num(a["y1"]), _num(a["y2"])]

    # ---- circle ----
    for m in re.finditer(r"<circle\b([^>]*)/?>", svg_inner):
        a = dict(re.findall(r"([a-zA-Z:_-]+)=['\"]([^'\"]*)['\"]", m.group(1)))
        if all(k in a for k in ("cx", "cy", "r")):
            r = _num(a["r"])
            cx, cy = _num(a["cx"]), _num(a["cy"])
            xs += [cx - r, cx + r]
            ys += [cy - r, cy + r]

    # ---- polyline / polygon points ----
    for tag in ("polyline", "polygon"):
        for m in re.finditer(rf"<{tag}\b([^>]*)/?>", svg_inner):
            a = dict(re.findall(r"([a-zA-Z:_-]+)=['\"]([^'\"]*)['\"]", m.group(1)))
            if "points" in a:
                pts = [_num(v) for v in a["points"].replace(",", " ").split()]
                xs += pts[0::2]
                ys += pts[1::2]

    # ---- path（d 属性绝对坐标对） ----
    # svglite 对曲线 / 网络图 edge 多输出 <path d="M.. L.. C..">；低层命令字母与逗号
    # 非数值，直接抽全部浮点 token 按 (x,y) 配对即可覆盖 bounding box。相对坐标
    # （小写命令）会被误当绝对、可能略放大，但仅增留白、绝不裁图（且下方 union
    # 原始 viewBox 进一步兜底）。
    for m in re.finditer(r"<path\b([^>]*)/?>", svg_inner):
        a = dict(re.findall(r"([a-zA-Z:_-]+)=['\"]([^'\"]*)['\"]", m.group(1)))
        d = a.get("d")
        if not d:
            continue
        nums = re.findall(r"-?\d+\.?\d*(?:[eE][+-]?\d+)?", d)
        coords = [_num(v) for v in nums]
        for i in range(0, len(coords) - 1, 2):
            xs.append(coords[i])
            ys.append(coords[i + 1])

    # ---- 与原始 viewBox 取并集（防漏扫裁图） ----
    try:
        vbx, vby, vbw, vbh = (float(t) for t in str(vb).split())
        xs += [vbx, vbx + vbw]
        ys += [vby, vby + vbh]
    except (ValueError, AttributeError, TypeError):
        pass

    if not xs or not ys:
        return (0.0, 0.0, 504.0, 360.0)
    return (min(xs) - pad, min(ys) - pad_y, max(xs) + pad, max(ys) + pad_y)


def _strip_clip(svg_inner: str) -> str:
    """移除 svglite 的 clipPath 定义与 clip-path 引用（100% 显示的关键）。

    svglite 用固定 0..504 的 clipPath 裁剪绘图区，但 meta 包森林图的左右文字列
    画在 0 外 / 504 外（实测 x∈[-140,644]），被内部 clip 裁掉——即使外层 viewBox
    已扩展也无效。移除后由外层动态 viewBox（content_bbox）保证完整显示。
    注意：必须在 content_bbox 之前调用（clipPath 里的 rect 0..504 会污染 bbox）。
    """
    s = re.sub(r"<clipPath\b.*?</clipPath>", "", svg_inner, flags=re.S)
    s = re.sub(r"\s*clip-path='url\(#[^)]+\)'", "", s)
    return s


def _fix_xml(s: str) -> str:
    """补齐缺失的闭合标签（svglite 2.2.2 偶发缺一个 </g>）。

    浏览器按 HTML 解析规则宽容渲染没问题，但 cairosvg 用严格 XML 解析会报
    "mismatched tag"。用标签栈扫描，把未闭合的开标签按逆序补齐闭合标签。
    仅 SVG→PNG 路径使用；内联渲染（浏览器）不需要。
    """
    stack: list[str] = []
    out: list[str] = []
    i, n = 0, len(s)
    while i < n:
        if s[i] != "<":
            out.append(s[i]); i += 1; continue
        if s.startswith("<!--", i):
            j = s.find("-->", i); j = n if j < 0 else j + 3
            out.append(s[i:j]); i = j; continue
        if s.startswith("<![CDATA[", i):
            j = s.find("]]>", i); j = n if j < 0 else j + 3
            out.append(s[i:j]); i = j; continue
        if s[i + 1] in ("!", "?"):
            j = s.find(">", i); j = n if j < 0 else j + 1
            out.append(s[i:j]); i = j; continue
        j = s.find(">", i)
        if j < 0:
            out.append(s[i:]); break
        body = s[i + 1:j].strip()
        out.append(s[i:j + 1]); i = j + 1
        if not body or body.startswith("/") or body.endswith("/"):
            if body.startswith("/") and stack:
                stack.pop()  # 闭合标签弹栈
            continue
        name = body.split()[0]
        stack.append(name)
    for name in reversed(stack):
        out.append(f"</{name}>")
    return "".join(out)


# CJK 文本检测（中文 + 全角标点；含日韩假名区更宽，此处聚焦中文场景）
_CJK_RE = re.compile(r"[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]")


def _default_cjk_font() -> str:
    """按平台选默认中文字体（可被环境变量 RENDERING_CJK_FONT 覆盖）。

    背景（2026-08-20 实测）：cairosvg 按 font-family 严格匹配字体、无系统回退，
    遇中文（SVG 里 font-family 恒为 "DejaVu Sans"）直接不渲染 → 中文 study 标签
    空白。本函数按平台返回本机存在的中文字体族，替换进含中文的 <text>。
    """
    env = os.environ.get("RENDERING_CJK_FONT")
    if env:
        return env
    if sys.platform == "darwin":
        return "PingFang SC"
    if sys.platform.startswith("win"):
        return "Microsoft YaHei"  # 已验证（cairosvg 渲染中文 OK）
    return "Noto Sans CJK SC"  # Linux 常见 CJK 包


def _fix_cjk_fonts(svg_inner: str, cjk_font: str | None = None) -> str:
    """把**含中文**的 <text> 元素字体族替换为中文字体族（纯英文/数字不动）。

    效果（实测 2026-08-20）：
      - 中文 text：font-family → 中文字体族 → cairosvg 正常渲染（像素验证 OK）
      - 英文/数字 text：保持原 font-family（"DejaVu Sans"）→ 英文图像素零变化
    仅 SVG→PNG 本地渲染路径调用；浏览器内联有系统字体回退，不需要。
    """
    if cjk_font is None:
        cjk_font = _default_cjk_font()

    def repl(m: re.Match) -> str:
        open_tag, text = m.group(1), m.group(2)
        if _CJK_RE.search(text):
            open_tag = re.sub(
                r"font-family:\s*['\"][^'\"]*['\"]",
                f'font-family: "{cjk_font}"',
                open_tag,
            )
        return f"<text{open_tag}>{text}</text>"

    return re.sub(r"<text\b([^>]*)>(.*?)</text>", repl, svg_inner, flags=re.S)


def _wrap_points(line: str, limit: int = 1200) -> str:
    """拆分超长行（svglite polyline points 单行可达 7000+ 字符）"""
    if len(line) <= limit:
        return line

    def repl(m):
        val = m.group(2)
        chunks, cur = [], ""
        for part in val.split():
            if len(cur) + len(part) + 1 > 1000:
                chunks.append(cur)
                cur = part
            else:
                cur = (cur + " " + part) if cur else part
        if cur:
            chunks.append(cur)
        return m.group(1) + chunks[0] + "\n" + "\n".join(chunks[1:]) + m.group(3)

    return re.sub(r"(points=['\"])(.*?)(['\"])", repl, line, flags=re.S)


def build_figure_widget(
    figures: list, titles: list[str], pad: float = 8.0, pad_y: float = 24.0,
    card: bool = False,
) -> str:
    """figures: [{svg, type}, ...] → 完整内联 HTML fragment。

    宽度规则：
      1. content_bbox() 扫描内容实际边界 → 动态 viewBox（解决 svglite 内容超界裁剪）
      2. SVG 固定原尺寸（viewBox 宽）不缩放
      3. 外层 overflow-x:auto —— 容器装不下即出横向滚动条

    card=True：报告模式，每个图包成带浅色标题栏（图标+名称）的卡片，
    配柔和阴影 + hover 上浮；复用同一 SVG 净化链（extract_svg→strip_clip→bbox→wrap）。
    """
    blocks = []
    for fig, t in zip(figures, titles):
        inner, vb = extract_svg(fig.get("svg") or "")
        if not inner.strip():
            # 无实际内容的图形（如 coze 静默降级返回的空 svg）→ 隐藏标签，不渲染任何卡片
            continue
        inner = _strip_clip(inner)          # ★ 先移除内部 clipPath（否则左右文字列被裁）
        min_x, min_y, max_x, max_y = content_bbox(inner, vb, pad=pad, pad_y=pad_y)
        vb_fit = f"{min_x:g} {min_y:g} {max_x - min_x:g} {max_y - min_y:g}"
        w = max_x - min_x
        svg_block = (
            f'<svg viewBox="{vb_fit}" style="width:{w:g}px;height:auto;display:block;'
            f'margin:0 auto;">'
            f"{_wrap_points(inner)}</svg>"
        )
        if card:
            blocks.append(
                f'<div class="figure-card">'
                f'<div class="cap"><span class="ico">📊</span>{_html_escape(t)}</div>'
                f'<div class="svg-wrap">{svg_block}</div></div>'
            )
        else:
            blocks.append(
                f'<div><div style="font-size:15px;font-weight:500;margin:0 0 6px;'
                f'color:var(--color-text-primary);">{t}</div>'
                f'<div style="overflow-x:auto;max-width:100%;background:#fff;'
                f'border:0.5px solid var(--color-border-tertiary);'
                f'border-radius:var(--border-radius-md);">{svg_block}</div></div>'
            )
    return (
        '<div style="display:flex;flex-direction:column;gap:16px;'
        'font-family:var(--font-sans);">' + "".join(blocks) + "</div>"
    )


def svg_to_png(svg_str: str, out_path: str, scale: float = 2.0,
               pad: float = 8.0, pad_y: float = 24.0) -> str:
    """SVG → PNG（本地 cairosvg 转换，coze 端零改动）。

    与内联渲染同一处理链：strip clip → content_bbox 扩展 viewBox（保证完整内容）
    → 重建完整 SVG → cairosvg 按 scale 光栅化 → 写 out_path。

    Returns: out_path（成功）; 转换失败抛 RuntimeError（含原因）。
    """
    try:
        import cairosvg
    except ImportError:
        raise RuntimeError("SVG→PNG 需 cairosvg：pip install cairosvg")

    inner, vb = extract_svg(svg_str)
    inner = _strip_clip(inner)
    inner = _fix_xml(inner)  # svglite 偶发缺 </g>，严格 XML 解析前补齐
    inner = _fix_cjk_fonts(inner)  # 2026-08-20: 含中文的 text 换中文字体族（英文不动）
    min_x, min_y, max_x, max_y = content_bbox(inner, vb, pad=pad, pad_y=pad_y)
    vb_fit = f"{min_x:g} {min_y:g} {max_x - min_x:g} {max_y - min_y:g}"
    full = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb_fit}" '
        f'width="{max_x - min_x}" height="{max_y - min_y}">'
        f"{_wrap_points(inner)}</svg>"
    )
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    cairosvg.svg2png(bytestring=full.encode("utf-8"), write_to=out_path, scale=scale)
    return out_path


def _html_escape(s) -> str:
    return _html.escape(str(s))


def _stats_to_html(stats, depth: int = 0) -> str:
    """把 stats（dict/list/标量，可能嵌套）递归渲染成 HTML 表格。"""
    if stats is None:
        return ""
    if isinstance(stats, dict):
        if not stats:
            return ""
        rows = []
        for k, v in stats.items():
            rows.append(
                f"<tr><td class='k'>{_html_escape(k)}</td>"
                f"<td class='v'>{_stats_to_html(v, depth + 1)}</td></tr>"
            )
        return f"<table class='stats'>{''.join(rows)}</table>"
    if isinstance(stats, list):
        if stats and all(isinstance(x, dict) for x in stats):
            return "".join(_stats_to_html(x, depth + 1) for x in stats)
        return _html_escape("、".join(str(x) for x in stats))
    return _html_escape(stats)


def _kv_rows(obj) -> str:
    """dict → 紧凑 key-value 网格行（嵌套 dict/list 递归/枚举，避免压平成点路径）。"""
    if not isinstance(obj, dict) or not obj:
        return _html_escape(obj) if obj is not None else ""
    rows = []
    for k, v in obj.items():
        if isinstance(v, dict):
            v = _stats_to_html(v)
        elif isinstance(v, list):
            v = _html_escape("、".join(str(x) for x in v))
        else:
            v = _html_escape(v)
        rows.append(
            f'<div class="k">{_html_escape(k)}</div>'
            f'<div class="v">{v}</div>'
        )
    return f'<div class="kv">{"".join(rows)}</div>'


# ── 双语文案字典（仅 HTML 框架层切换，SVG 内部文字不改）──
_I18N = {
    "zh": {
        "html_lang": "zh-CN",
        "report_title": "meta-analysis 报告",
        "result_report": "meta-analysis 结果报告",
        "generated": "生成时间",
        "footer": "由 meta-analysis 技能生成 · 图形为内联 SVG（可缩放/检查）· R 脚本可本地复现",
        "copied": "已复制 ✓",
        "trunc_prefix": "⚠️ coze 返回体因 4000 字符限制截断，以下次要内容缺失：",
        "trunc_suffix": "。核心数值（status/stats）完整。",
        "contract_drift_prefix": "⚠️ coze 返回结构与本地技能预期不一致，已在本地自动适配。如频繁出现，建议升级 meta-analysis 技能到最新版：",
        "endpoint_fallback_prefix": "⚠️ 主分析工作流地址已切换，本次分析已自动回退到备用 coze 端点完成。",
        "effect_label": "效应量",
        "pooled_effect": "合并效应量",
        "sig_yes": "有统计学显著性",
        "sig_no": "无统计学显著性",
        "p_missing": "p 未提供",
        "group_pooled": "合并效应",
        "group_hetero": "异质性",
        "group_bias": "发表偏倚",
        "group_quality": "质量评估",
        "group_summary": "分析概要",
        "group_publish": "发表建议",
        "qgate_pass": "通过",
        "qgate_warn": "需注意",
        "qgate_fail": "不通过",
        "repro_title": "可复现 R 脚本",
        "repro_copy": "复制",
        "fig_forest": "森林图",
        "fig_funnel": "漏斗图",
        "fig_prisma": "PRISMA 流程图",
        "fig_rob": "偏倚风险图",
        "fig_cumulative": "累积 Meta 图",
        "fig_baujat": "Baujat 图",
        "fig_labbe": "L'Abbe 图",
        "fig_radial": "Radial 图",
        "fig_sucra": "SUCRA 排名图",
        "fig_egger": "Egger 回归散点图",
        "fig_contribution": "NMA 贡献图",
        "fig_loo": "留一法影响图",
        "fig_gosh": "Gosh 图",
        "fig_bubble": "气泡图",
        "fig_netgraph": "网络关系图",
        "fig_dose_resp": "剂量-反应图",
        "fig_drapery": "Drapery 图",
        "fig_sroc": "SROC 曲线",
        "fig_tsa": "试验序贯分析图",
        "fig_power": "效能分析图",
        "fig_influence": "影响诊断图",
        "fig_nodesplit": "节点拆分图",
        "fig_trimfill": "剪补法漏斗图",
        "fig_netleague": "网络证据表",
        "fig_sens_forest": "敏感度森林图",
        "fig_spec_forest": "特异度森林图",
    },
    "en": {
        "html_lang": "en",
        "report_title": "meta-analysis Report",
        "result_report": "meta-analysis Result Report",
        "generated": "Generated",
        "footer": "Generated by the meta-analysis skill · figures are inline SVG (scalable/inspectable) · R script is locally reproducible",
        "copied": "Copied ✓",
        "trunc_prefix": "⚠️ The coze response was truncated at the 4000-character limit; the following secondary content is missing: ",
        "trunc_suffix": ". Core values (status/stats) are complete.",
        "contract_drift_prefix": "⚠️ The coze response structure differs from what this skill version expects; it has been auto-adapted locally. If this recurs, upgrade the meta-analysis skill to the latest version:",
        "endpoint_fallback_prefix": "⚠️ The primary analysis workflow endpoint was switched; this analysis was automatically completed via the fallback coze endpoint.",
        "effect_label": "Effect",
        "pooled_effect": "Pooled effect",
        "sig_yes": "Statistically significant",
        "sig_no": "Not statistically significant",
        "p_missing": "p not provided",
        "group_pooled": "Pooled effect",
        "group_hetero": "Heterogeneity",
        "group_bias": "Publication bias",
        "group_quality": "Quality assessment",
        "group_summary": "Analysis summary",
        "group_publish": "Publication advice",
        "qgate_pass": "Pass",
        "qgate_warn": "Caution",
        "qgate_fail": "Fail",
        "repro_title": "Reproducible R script",
        "repro_copy": "Copy",
        "fig_forest": "Forest plot",
        "fig_funnel": "Funnel plot",
        "fig_prisma": "PRISMA flow diagram",
        "fig_rob": "Risk-of-bias plot",
        "fig_cumulative": "Cumulative meta plot",
        "fig_baujat": "Baujat plot",
        "fig_labbe": "L'Abbe plot",
        "fig_radial": "Radial plot",
        "fig_sucra": "SUCRA ranking plot",
        "fig_egger": "Egger's regression plot",
        "fig_contribution": "NMA contribution plot",
        "fig_loo": "Leave-one-out plot",
        "fig_gosh": "Gosh plot",
        "fig_bubble": "Bubble plot",
        "fig_netgraph": "Network graph",
        "fig_dose_resp": "Dose-response plot",
        "fig_drapery": "Drapery plot",
        "fig_sroc": "SROC curve",
        "fig_tsa": "Trial sequential analysis plot",
        "fig_power": "Power analysis plot",
        "fig_influence": "Influence diagnostic plot",
        "fig_nodesplit": "Node-splitting plot",
        "fig_trimfill": "Trim-and-fill funnel plot",
        "fig_netleague": "Network evidence table",
        "fig_sens_forest": "Sensitivity forest plot",
        "fig_spec_forest": "Specificity forest plot",
    },
}


def _t(locale: str) -> dict:
    """按 locale 取文案字典，未知/缺失回退到 zh。"""
    return _I18N.get(str(locale or "zh").lower(), _I18N["zh"])


def _group_card(label: str, ico: str, inner_html: str) -> str:
    return (f'<div class="group"><h3><span class="ico">{ico}</span>{label}</h3>'
            f'{inner_html}</div>')


def _quality_gate_card(qg: dict, T: dict) -> str:
    """质量门：状态彩色徽章 + 逐条检查（左检查项、右状态结论，两列对齐 .kv 版式）。"""

    def _lvl_map(x):
        return {"green": "ok", "yellow": "warn", "red": "bad"}.get(str(x or "warn").lower(), "warn")

    status = _lvl_map(qg.get("status") or "unknown")
    label = {"ok": T["qgate_pass"], "warn": T["qgate_warn"], "bad": T["qgate_fail"]}.get(status, status)
    badge = f'<span class="badge {status}"><span class="dot"></span>{label}</span>'
    checks = qg.get("checks") or []
    rows = []
    for c in checks:
        dot = _lvl_map(c.get("level") or "warn")
        verdict = {"ok": T["qgate_pass"], "warn": T["qgate_warn"], "bad": T["qgate_fail"]}.get(dot, dot)
        msg = _html_escape(c.get("message") or c.get("item") or "")
        rows.append(
            f'<div class="k"><span class="cdot {dot}"></span>{msg}</div>'
            f'<div class="v {dot}">{verdict}</div>'
        )
    body = f'{badge}<div class="kv checks-kv">{"".join(rows)}</div>' if rows else badge
    return _group_card(T["group_quality"], "✅", body)


def _render_subgroup_test(sgt, T: dict) -> str:
    """组间差异检验卡片：Q_between / df / p_between / n_groups / model + 显著性徽章。

    纯展示 coze 返回的 stats.subgroup_test 数值（2026-08-27 新增字段），零计算，
    符合契约红线（数值一律由 R 算，本地仅转述）。
    """
    if not isinstance(sgt, dict):
        return ""
    sgt = {str(k): v for k, v in sgt.items()}

    def _f(v):
        try:
            return float(v)
        except (TypeError, ValueError):
            return None

    q = _f(sgt.get("Q_between"))
    df = _f(sgt.get("df"))
    p = _f(sgt.get("p_between"))
    ng = sgt.get("n_groups")
    model = sgt.get("model")
    sig = (p is not None and p < 0.05)
    if sig:
        badge = f'<span class="badge ok"><span class="dot"></span>组间差异有统计学意义</span>'
    else:
        badge = f'<span class="badge warn"><span class="dot"></span>组间差异无统计学意义</span>'
    p_txt = f"p = {p:.4f}" if p is not None else T["p_missing"]
    q_txt = f"{q:.3f}" if q is not None else "—"
    df_txt = f"{df:.0f}" if df is not None else "—"
    ng_txt = _html_escape(ng) if ng is not None else "—"
    model_txt = _html_escape(model) if model else "—"
    rows = (
        f'<div class="kv">'
        f'<div class="k">Q<sub>between</sub>（组间异质性 Q）</div><div class="v">{q_txt}</div>'
        f'<div class="k">自由度 df</div><div class="v">{df_txt}</div>'
        f'<div class="k">p 值</div><div class="v">{_html_escape(p_txt)}</div>'
        f'<div class="k">亚组数</div><div class="v">{ng_txt}</div>'
        f'<div class="k">模型</div><div class="v">{model_txt}</div>'
        f'</div>'
    )
    return _group_card("亚组间差异检验", "🔬", badge + rows)


def _publication_advice_card(pa, T: dict) -> str:
    """论文撰写与发表建议卡（消费 advise_publication 结果，纯展示，零计算）。

    含：期刊推荐表 / 优势 / 限制段要点 / 审稿人问题 / 讨论段模板（折叠）/
    PRISMA 核查 / 报告规范出处（P2c 在线核验）/ S2 高引推荐（P2c）/ 数据可用性 /
    证据接地（P2b）/ 参考核验（P2a 结构层 / P2b 在线）。
    """
    if not isinstance(pa, dict):
        return ""
    parts = []
    field_used = pa.get("field_used") or "general"
    source = pa.get("source") or "static_seed"
    # 顶部：领域 + 数据来源（便于读者判断可信度）
    meta_bits = []
    if field_used:
        _fs_map = {"corpus_topic": "语料主题", "corpus_concepts": "语料概念",
                   "openalex": "OpenAlex 概念"}
        _fs = pa.get("field_source")
        _fs_suffix = ("（%s推断）" % _fs_map[_fs]) if _fs in _fs_map else ""
        meta_bits.append("领域：%s%s" % (_html_escape(field_used), _fs_suffix))
    if source:
        _src_map = {"static_seed": "静态种子", "openalex": "OpenAlex 实时"}
        meta_bits.append("来源：%s" % _src_map.get(source, _html_escape(source)))
    if meta_bits:
        parts.append('<div style="font-size:12px;color:var(--muted);margin-bottom:8px;">%s</div>'
                     % " · ".join(meta_bits))

    # 期刊推荐表
    recs = pa.get("recommended_journals") or []
    if recs:
        rows = []
        for r in recs:
            name = _html_escape(r.get("name") or "")
            tier = _html_escape(r.get("tier") or "")
            ifv = r.get("if")
            if isinstance(ifv, (int, float)):
                if_str = "≈%.0f%s" % (ifv, "*" if r.get("approx") else "")
            else:
                if_str = "—"
            why = _html_escape(r.get("why") or "")
            extra = ""
            apc = r.get("apc_prices")
            if apc is not None:
                extra += " · APC %s" % _html_escape(str(apc))
            oa = r.get("is_oa")
            if oa is True:
                extra += " · OA"
            elif oa is False:
                extra += " · 非 OA"
            rows.append(
                '<tr><td style="padding:4px 10px 4px 0;border-bottom:1px solid var(--border);font-weight:700;">%s</td>'
                '<td style="text-align:right;padding:4px 8px;border-bottom:1px solid var(--border);white-space:nowrap;">%s</td>'
                '<td style="text-align:center;padding:4px 8px;border-bottom:1px solid var(--border);">%s</td>'
                '<td style="padding:4px 0;border-bottom:1px solid var(--border);color:var(--muted);font-size:13px;">%s%s</td></tr>'
                % (name, if_str, tier, why, extra)
            )
        journal_tbl = (
            '<table style="border-collapse:collapse;width:100%;font-size:13px;font-variant-numeric:tabular-nums;margin-bottom:4px;">'
            '<tr><th style="text-align:left;padding:4px 10px 4px 0;border-bottom:1px solid var(--border);">期刊</th>'
            '<th style="text-align:right;padding:4px 8px;border-bottom:1px solid var(--border);">IF*</th>'
            '<th style="text-align:center;padding:4px 8px;border-bottom:1px solid var(--border);">档位</th>'
            '<th style="text-align:left;padding:4px 0;border-bottom:1px solid var(--border);">推荐理由</th></tr>'
            + "".join(rows) + "</table>"
        )
        if source == "static_seed":
            journal_tbl += ('<div class="fig-note" style="margin-top:2px;">⚠️ 期刊指标来自静态种子（IF 带 * 为近似值），'
                            '仅作投稿方向参考。</div>')
        elif source == "openalex":
            journal_tbl += ('<div class="fig-note" style="margin-top:2px;">✅ 期刊指标来自 OpenAlex 实时'
                            '（IF* 为 2yr_mean_citedness 代理；APC/OA 以出版方页为准）。</div>')
        parts.append(journal_tbl)

    # 优势
    strengths = pa.get("strengths") or []
    if strengths:
        parts.append('<div class="interp-section"><div class="interp-label">✅ 优势</div><ul>' +
                     "".join("<li>%s</li>" % _html_escape(s) for s in strengths) + "</ul></div>")
    # 限制段要点
    limitations = pa.get("limitations") or []
    if limitations:
        parts.append('<div class="interp-section"><div class="interp-label">⚠ 限制段要点</div><ul>' +
                     "".join("<li>%s</li>" % _html_escape(l) for l in limitations) + "</ul></div>")
    # 审稿人问题
    rq = pa.get("reviewer_likely_questions") or []
    if rq:
        parts.append('<div class="interp-section"><div class="interp-label">🔍 审稿人可能问</div><ul>' +
                     "".join("<li>%s</li>" % _html_escape(q) for q in rq) + "</ul></div>")
    # 讨论段模板（折叠）
    disc = pa.get("discussion_template")
    if disc:
        parts.append('<details class="repro" style="background:#f6f8fc;margin-top:4px;">'
                     '<summary><span>讨论段模板（点击展开/复制）</span><span class="copy-btn">%s</span></summary>'
                     '<div class="body"><pre style="white-space:pre-wrap;margin:0;">%s</pre></div></details>'
                     % (_html_escape(T.get("repro_copy", "复制")), _html_escape(disc)))
    # PRISMA 核查
    prisma = pa.get("prisma_checklist") or []
    if prisma:
        parts.append('<div class="interp-section"><div class="interp-label">📑 PRISMA 核查</div><ul>' +
                     "".join("<li>%s</li>" % _html_escape(p) for p in prisma) + "</ul></div>")

    # 报告规范出处（P2c：在线核验规范出处 DOI，使清单可溯源/可引用）
    standards = pa.get("reporting_standards") or []
    if standards:
        _st_lab = {"verified": "出处已核验", "static": "静态登记",
                   "bot_blocked": "出版方拦截(DOI 已解析)", "unresolved": "未解析",
                   "mismatch": "不匹配", "no_identifier": "无标识"}
        st_rows = []
        for st in standards:
            status = st.get("status") or "static"
            if st.get("resolved"):
                cls = "ok"
            elif status == "static":
                cls = "neutral"
            else:
                cls = "warn"
            nm = _html_escape(st.get("name") or "")
            doi = _html_escape(st.get("doi") or "")
            lab = _st_lab.get(status, _html_escape(status))
            url = st.get("url") or ""
            link = (' · <a href="%s" target="_blank" rel="noopener">EQUATOR ↗</a>'
                    % _html_escape(url)) if url else ""
            st_rows.append('<div class="k"><span class="cdot %s"></span>%s</div>'
                           '<div class="v %s">%s · %s%s</div>' % (cls, nm, cls, doi, lab, link))
        psrc = pa.get("prisma_source")
        ps_note = ("规范出处已在 doi.org 在线解析核验（ok/bot_blocked 均视为 DOI 真实）；"
                   "条目本体为静态权威清单（PRISMA 2020）。"
                   if psrc == "verified_online" else
                   "规范出处为静态登记（未联网核验）；条目本体为静态权威清单（PRISMA 2020）。")
        parts.append('<div class="interp-section"><div class="interp-label">📚 报告规范出处</div>'
                     '<div class="kv checks-kv">%s</div>'
                     '<div style="font-size:12px;color:var(--muted);margin-top:4px;">%s</div></div>'
                     % ("".join(st_rows), ps_note))
    # Semantic Scholar 高引推荐（P2c：有 key 才用；无 key 明示跳过）
    hc = pa.get("highly_cited") or []
    s2_status = pa.get("s2_status")
    if hc:
        hc_rows = []
        for h in hc:
            bits = []
            if h.get("year"):
                bits.append(str(h["year"]))
            if h.get("venue"):
                bits.append(_html_escape(str(h["venue"])))
            cit = h.get("citations")
            if isinstance(cit, int):
                bits.append("引用 %d" % cit)
            hc_rows.append('<li>%s <span style="color:var(--muted);">（%s）</span></li>'
                           % (_html_escape(h.get("title") or ""), " · ".join(bits)))
        parts.append('<details class="repro" style="background:#f6f8fc;margin-top:4px;">'
                     '<summary><span>🔥 领域高引推荐（Semantic Scholar · %d 篇）</span>'
                     '<span class="copy-btn">↕</span></summary>'
                     '<div class="body"><ul style="margin:0;">%s</ul></div></details>'
                     % (len(hc), "".join(hc_rows)))
    elif s2_status == "skipped_no_key":
        parts.append('<div class="interp-qa" style="font-size:12px;color:var(--muted);margin-top:4px;">'
                     '🔥 Semantic Scholar 高引推荐：未配置 SEMANTIC_SCHOLAR_API_KEY，已跳过。</div>')
    # 报告规范 + 数据可用性（底部脚注式）
    foot = []
    rg = pa.get("reporting_checklist")
    if rg:
        foot.append("报告规范：%s" % _html_escape(rg))
    da = pa.get("data_availability")
    if da:
        foot.append(_html_escape(da))
    if foot:
        parts.append('<div class="interp-qa" style="font-size:13px;color:var(--muted);margin-top:6px;">'
                     + " · ".join(foot) + '</div>')
    # 证据接地（P2b：复用 merged.json）
    ev = pa.get("evidence_grounding")
    if ev and ev.get("loaded"):
        parts.append('<div class="interp-qa" style="font-size:13px;color:var(--muted);margin-top:4px;">'
                     '🔎 证据接地（merged.json）：%s</div>' % _html_escape(ev.get("note", "")))
    # 参考核验（P2a 结构层 / P2b 在线核验）
    refs = pa.get("ref_verification") or []
    if refs:
        _ref_cls = {
            "verified": "ok", "format_ok": "ok", "no_identifier": "neutral",
            "bot_blocked": "warn", "suspicious": "bad", "mismatch": "bad",
            "unresolved": "bad", "malformed": "bad",
        }
        _ref_label = {
            "verified": "已核验", "format_ok": "格式合法", "no_identifier": "无标识",
            "bot_blocked": "出版方拦截(疑似真实)", "suspicious": "可疑(格式异常)",
            "mismatch": "不匹配(疑似错误/幻觉)", "unresolved": "未解析", "malformed": "格式异常",
        }
        ref_rows = []
        for r in refs:
            status = r.get("status") or "unresolved"
            cls = _ref_cls.get(status, "bad")
            doi = _html_escape(r.get("doi") or "—")
            lab = _ref_label.get(status, status)
            note = _html_escape(r.get("note") or "")
            cons = r.get("consistency")
            if cons is True:
                lab += " · 一致性✓"
            elif cons is False:
                lab += " · 一致性✗"
            detail = lab + ((" — " + note) if note else "")
            ref_rows.append('<div class="k"><span class="cdot %s"></span>%s</div>'
                            '<div class="v %s">%s</div>' % (cls, doi, cls, detail))
        _ref_src = "在线核验（verify_citations：DOI/PMID/OpenAlex 三重解析 + 标题作者一致性）" \
            if any(r.get("via") == "online" for r in refs) else "结构层核验（仅 DOI 格式）"
        parts.append('<div class="interp-section"><div class="interp-label">🔗 参考核验</div>'
                     '<div class="kv checks-kv">%s</div>'
                     '<div style="font-size:12px;color:var(--muted);margin-top:4px;">%s</div></div>'
                     % ("".join(ref_rows), _ref_src))
    return _group_card(T.get("group_publish", "发表建议"), "📝", "".join(parts))


def _render_hero(stats, task, T: dict) -> str:
    """顶部结论 Hero：合并效应量 + 95%CI + p + 显著性徽章（一眼看到核心结果）。"""
    pooled = stats.get("pooled") or {}
    if not pooled:
        return ""
    sm = _html_escape(str(stats.get("sm") or T["effect_label"]))
    if pooled.get("estimate_exp") is not None:
        est, lo, hi = pooled["estimate_exp"], pooled.get("ci_low_exp"), pooled.get("ci_high_exp")
    else:
        est, lo, hi = pooled.get("estimate"), pooled.get("ci_low"), pooled.get("ci_high")
    if est is None:
        return ""
    # 2026-09-14：NMA/CNMA 的 pooled 是多对比向量（list），没有单一"合并效应量"。
    # 旧实现直接 return ""（2026-09-08 的防御性早退）→ **网络 Meta 报告顶部整块留白**，
    # 用户第一屏看不到任何结论。改为渲染「网络 Meta 摘要」（结构 + 可达估计数 +
    # 显著性概况）；逐对比/成分明细仍由下方「合并效应」卡完整呈现，此处不重复列表。
    if isinstance(est, (list, tuple)):
        return _render_hero_network(stats, T)
    p = pooled.get("p")
    if p is None:
        p = pooled.get("pval")
    try:
        p = float(p) if p is not None else None
    except (TypeError, ValueError):
        p = None
    sig = (p is not None and p < 0.05)
    p_txt = f"p = {p:.4f}" if p is not None else T["p_missing"]
    badge = (f'<span class="badge ok"><span class="dot"></span>{T["sig_yes"]}</span>' if sig
             else f'<span class="badge warn"><span class="dot"></span>{T["sig_no"]}</span>')
    est_s = f"{est:.3f}"
    ci_s = f"{lo:.3f} – {hi:.3f}" if lo is not None and hi is not None else "—"
    return (
        f'<div class="hero">'
        f'<div class="lead">{T["pooled_effect"]}（{sm}）</div>'
        f'<div class="est"><span class="sm">{sm}</span> {est_s}'
        f'<span class="ci">95% CI {ci_s}</span></div>'
        f'<div class="sub">{badge}<span>{p_txt}</span></div>'
        f'</div>'
    )


# CINeMA 六域（网络 Meta 置信度）的中文标签与评级文案（2026-09-14）
_CINEMA_DOMAIN_CN = {
    "within_study_bias": "研究内偏倚",
    "reporting_bias": "报告偏倚",
    "indirectness": "间接性",
    "imprecision": "不精确性",
    "heterogeneity": "异质性",
    "incoherence": "不一致性",
}
_CINEMA_RATING_CN = {
    "no_concerns": "无关切",
    "some_concerns": "一些关切",
    "major_concerns": "重大关切",
    "unclear": "数据不足",
}


def _render_hero_network(stats, T: dict) -> str:
    """网络 Meta（NMA / CNMA）顶部摘要卡。

    网络 Meta 没有单一的"合并效应量"，但也不该顶部留白——这里给结构 + 可达估计数 +
    显著性概况。注意 log 尺度（netmeta 输出 TE = log OR/RR/HR）的无效值是 0（不是 1），
    且 CNMA 的 pooled 含参考组自身占位项（est = lo = hi = 0），须跳过，否则会被
    误计为"一个跨无效值的对比"。
    """
    pooled = stats.get("pooled") or {}
    extra = stats.get("extra") or {}
    net = extra.get("network") or {}
    sm = _html_escape(str(stats.get("sm") or T["effect_label"]))
    unit = str(pooled.get("unit") or "")
    is_cnma = stats.get("n_comp") is not None or "components" in extra

    # CNMA 的 pooled 是**组合效应**（各治疗在加性模型下的效应），成分效应才是它的核心产出
    # —— hero 取 components 口径，否则会出现"标着成分、数着治疗"的口径错配
    # （case47 实测：pooled 跳过参考组后 4 项 vs components 实为 2 项）。
    src = (extra.get("components") or {}) if is_cnma else pooled
    unit_word = "成分" if is_cnma else "对比"
    est, lo, hi = src.get("estimate"), src.get("ci_low"), src.get("ci_high")
    if not all(isinstance(v, (list, tuple)) for v in (est, lo, hi)):
        return ""

    ratio = str(stats.get("sm") or "").upper() in (
        "OR", "RR", "HR", "PLO", "PLOGIT", "IRR", "RRR")
    null = 0.0 if unit == "log" else (1.0 if ratio else 0.0)

    def _f(v):
        try:
            return float(v)
        except (TypeError, ValueError):
            return None

    tot = sig = 0
    for i in range(min(len(est), len(lo), len(hi))):
        e, l, h = _f(est[i]), _f(lo[i]), _f(hi[i])
        if e is None or l is None or h is None:
            continue
        if unit == "log" and e == 0 and l == 0 and h == 0:
            continue  # 参考组自身占位，不是有效估计
        tot += 1
        if not (l <= null <= h):
            sig += 1

    bits = []
    k = stats.get("k")
    if k is not None:
        bits.append(f"{int(k)} 项研究")
    nt = stats.get("n_treat") or net.get("n_interventions")
    if nt is not None:
        bits.append(f"{int(nt)} 种{'治疗' if is_cnma else '干预'}")
    if is_cnma:
        nc = stats.get("n_comp")
        if nc is not None:
            bits.append(f"{int(nc)} 个成分")
    elif net.get("n_designs") and int(net["n_designs"]) > 1:
        bits.append(f"{int(net['n_designs'])} 种设计")
    struct = " · ".join(bits) or "网络结构信息缺失"

    kind = "成分网络 Meta（CNMA）" if is_cnma else "网络 Meta 分析（NMA）"
    return (
        f'<div class="hero">'
        f'<div class="lead">{kind}</div>'
        f'<div class="est"><span class="sm">{struct}</span></div>'
        f'<div class="sub">'
        f'<span class="badge ok"><span class="dot"></span>'
        f'{tot} 个{unit_word}可达估计</span>'
        f'<span style="margin-left:10px;">其中 {sig} 个的 95% CI 不含无效值'
        f'（{sm} 尺度）</span>'
        f'</div>'
        f'</div>'
    )


def _render_pooled_card(pooled, T: dict) -> str:
    """合并效应卡。NMA 的 pooled 是多对比向量（estimate/ci_low/ci_high 为 list），
    通用 _kv_rows 会平铺成一长串顿号分隔的数字（不可读）→ 渲染为
    「对比 | 效应量 [95% CI]」小表；标量型（pairwise 等单一合并值）走原 _kv_rows。
    对比标签取 stats.pooled.comparisons（coze 端 2.9.18 起提供）；旧镜像无该字段时退化为索引。"""
    est = pooled.get("estimate")
    if not isinstance(est, (list, tuple)) or len(est) == 0:
        return _group_card(T.get("group_pooled", "合并效应"), "🎯", _kv_rows(pooled))

    def _num(v):
        try:
            return float(v)
        except (TypeError, ValueError):
            return None

    lo = pooled.get("ci_low") if isinstance(pooled.get("ci_low"), (list, tuple)) else []
    hi = pooled.get("ci_high") if isinstance(pooled.get("ci_high"), (list, tuple)) else []
    comps = pooled.get("comparisons") if isinstance(pooled.get("comparisons"), (list, tuple)) else []
    unit = str(pooled.get("unit") or "").strip()
    body = ['<table style="border-collapse:collapse;width:100%;font-size:13px;font-variant-numeric:tabular-nums;">',
            '<tr><th style="text-align:left;padding:4px 10px 4px 0;border-bottom:1px solid var(--border);">对比</th>'
            '<th style="text-align:right;padding:4px 0;border-bottom:1px solid var(--border);">效应量%s [95%% CI]</th></tr>'
            % (("（%s）" % _html_escape(unit)) if unit else "")]
    for i, e in enumerate(est):
        ev = _num(e)
        if ev is None:
            continue  # 矩阵摊平残留（对角/NA），跳过
        l, h = _num(lo[i]) if i < len(lo) else None, _num(hi[i]) if i < len(hi) else None
        label = _html_escape(str(comps[i])) if i < len(comps) else ("对比 %d" % (i + 1))
        ci = ("%.3f [%.3f; %.3f]" % (ev, l, h)) if (l is not None and h is not None) else "%.3f" % ev
        body.append('<tr><td style="padding:4px 10px 4px 0;border-bottom:1px solid var(--border);">%s</td>'
                    '<td style="text-align:right;padding:4px 0;border-bottom:1px solid var(--border);">%s</td></tr>' % (label, ci))
    body.append("</table>")
    return _group_card(T.get("group_pooled", "合并效应"), "🎯", "".join(body))


def _render_stats_groups(stats, T: dict) -> str:
    """统计结果按语义分组渲染（合并效应 / 异质性 / 发表偏倚 / 质量评估 / 分析概要），
    不再压平成单一大表。未知 task 的顶层 dict 也各成一卡，不丢信息。"""
    if not isinstance(stats, dict):
        return _stats_to_html(stats)
    groups = []
    spec = [
        ("pooled", T["group_pooled"], "🎯"),
        ("heterogeneity", T["group_hetero"], "📐"),
        ("bias", T["group_bias"], "⚖️"),
    ]
    for key, label, ico in spec:
        if key in stats and stats[key] is not None:
            if key == "pooled":
                groups.append(_render_pooled_card(stats[key], T))
            else:
                groups.append(_group_card(label, ico, _kv_rows(stats[key])))
    qg = stats.get("quality_gate")
    if isinstance(qg, dict):
        groups.append(_quality_gate_card(qg, T) if qg.get("checks") else
                      _group_card(T["group_quality"], "✅", _kv_rows(qg)))
    sgt = stats.get("subgroup_test")
    if isinstance(sgt, dict):
        groups.append(_render_subgroup_test(sgt, T))
    rest = {k: v for k, v in stats.items()
            if k not in ("pooled", "heterogeneity", "bias", "quality_gate", "subgroup_test")
            and not isinstance(v, dict)}
    if rest:
        groups.append(_group_card(T["group_summary"], "📋", _kv_rows(rest)))
    for k, v in stats.items():
        if k not in ("pooled", "heterogeneity", "bias", "quality_gate", "subgroup_test") and isinstance(v, dict):
            # 2026-09-08：extra.league_table 已由上方图卡区"网络证据表"（等宽 <pre>）保真呈现，
            # 此处剔除——否则被 _kv_rows 平铺成无格式单行且与图卡重复。
            rows = {rk: rv for rk, rv in v.items()
                    if not (k == "extra" and rk == "league_table")}
            if rows:
                groups.append(_group_card(_html_escape(str(k)), "📦", _kv_rows(rows)))
    return "".join(groups)


# 这些"输出型"函数作用域内的命名参数不强制断行（整体保持紧凑）
_PRETTY_RELAX_FNS = {"print", "cat", "message", "writeLines"}


def _pretty_r(code: str) -> str:
    """语法感知的轻量 R 格式化：仅在「括号深度>0 的逗号后」与「顶层(depth==0)分号后」
    插入真实换行并带缩进；字符串(含转义)与注释(#)内部绝不断行，避免破坏代码语义。
    不重排运算符/缩进层级，仅做分隔符断行，风险最低且等价保留原 token。"""
    out = []
    paren = 0
    in_str = None  # 当前字符串定界符: " ' `
    call_stack = []  # 函数调用栈（仅 "(" 记录其前标识符），用于识别 print/cat 等输出函数作用域
    i, n = 0, len(code)
    while i < n:
        ch = code[i]
        nxt = code[i + 1] if i + 1 < n else ""
        if in_str:
            out.append(ch)
            if ch == "\\" and i + 1 < n:      # 跳过转义字符，避免误判 \" 为字符串结束
                out.append(code[i + 1]); i += 2; continue
            if ch == in_str:
                in_str = None
            i += 1; continue
        # 不在字符串内
        if ch == "#":                          # 注释一直吃到行尾
            j = code.find("\n", i)
            if j == -1:
                out.append(code[i:]); break
            out.append(code[i:j]); i = j; continue
        if ch in ('"', "'", "`"):
            in_str = ch; out.append(ch); i += 1; continue
        if ch in "([{":
            if ch == "(":
                fn = ""
                j = i - 1
                while j >= 0 and code[j] == " ":
                    j -= 1
                while j >= 0 and (code[j].isalnum() or code[j] in "._"):
                    fn = code[j] + fn
                    j -= 1
                call_stack.append(fn)
            else:
                call_stack.append("")  # 索引/列表字面量占位，不影响输出函数判定
            paren += 1; out.append(ch); i += 1; continue
        if ch in ")]}":
            if call_stack:
                call_stack.pop()
            paren = max(0, paren - 1); out.append(ch); i += 1; continue
        if ch == ";" and paren == 0:          # 顶层语句分隔符 → 断行（跳过紧跟空格）
            out.append(";")
            j = i + 1
            while j < n and code[j] == " ":
                j += 1
            out.append("\n"); i = j; continue
        if ch == "," and paren > 0:           # 括号内：仅当逗号后是「命名参数 name=」且不在 print/cat 等输出函数作用域内才断行；
            out.append(",")                    # 位置参数（c("a","b")、cat(x,y)、向量元素）以及 print/cat 内部一律保持同行
            k = i + 1
            while k < n and code[k] == " ":
                k += 1
            _relax = any(fn in _PRETTY_RELAX_FNS for fn in call_stack)
            if re.match(r"[A-Za-z_.][\w.]*\s*=", code[k:]) and not _relax:
                out.append("\n" + "  " * min(paren, 6))
                i = k
            else:
                i = i + 1
            continue
        out.append(ch); i += 1
    return "".join(out)


def _highlight_r(code: str) -> str:
    """R 代码语法高亮（注释/字符串/函数/数字）。

    单遍扫描：注释（#...）与字符串（"…"/'…'）先隔离成 span，再对普通代码段
    做函数/数字高亮。避免「先整体 escape 再正则加 span」导致后一个 pattern
    匹配前一个生成的 class="c" 等标签属性、产生嵌套损坏 span（2026-08-28 实测
    `<span class=<span class="s">"c"</span>>`，meta-analysis 与 ct-samplesize
    同源缺陷）——单遍隔离后 span 标签不再进入后续正则的输入。
    """

    def _hl_plain(seg: str) -> str:
        esc = _html_escape(seg)
        esc = re.sub(r"\b([a-zA-Z_][a-zA-Z0-9_.]*)\s*\(", r'<span class="f">\1</span>(', esc)
        esc = re.sub(r"\b(\d+\.?\d*)\b", r'<span class="n">\1</span>', esc)
        return esc

    out = []
    buf = []
    i, n = 0, len(code)
    while i < n:
        ch = code[i]
        if ch == "#":  # 注释 → 隔离成 .c span，普通段 flush
            j = code.find("\n", i)
            if j == -1:
                j = n
            out.append(_hl_plain("".join(buf)))
            buf = []
            out.append('<span class="c">%s</span>' % _html_escape(code[i:j]))
            i = j
            continue
        if ch in ('"', "'"):  # 字符串（含转义）→ 隔离成 .s span
            quote = ch
            j = i + 1
            while j < n:
                if code[j] == "\\" and j + 1 < n:
                    j += 2
                    continue
                if code[j] == quote:
                    j += 1
                    break
                j += 1
            out.append(_hl_plain("".join(buf)))
            buf = []
            out.append('<span class="s">%s</span>' % _html_escape(code[i:j]))
            i = j
            continue
        buf.append(ch)
        i += 1
    out.append(_hl_plain("".join(buf)))
    return "".join(out)


_REPORT_TEMPLATE = """<!DOCTYPE html>
<html lang="{html_lang}"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{report_title} · {task}</title>
<style>
:root{{
  --bg:#eef1f6;--card:#ffffff;--card2:#f8fafc;--border:#e2e8f0;
  --text:#0f172a;--muted:#64748b;--accent:#4f46e5;--accent2:#0ea5e9;
  --ok:#16a34a;--warn:#d97706;--bad:#dc2626;--teal:#0F9B81;
  --radius:14px;--shadow:0 1px 3px rgba(15,23,42,.08),0 1px 2px rgba(15,23,42,.04);
  --shadow-hover:0 10px 28px rgba(15,23,42,.12);
  --font-sans:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif;
  /* 与 build_figure_widget 同名变量，确保内联 SVG 区块在独立文件里也能正确着色 */
  --color-text-primary:#0f172a;--color-border-tertiary:#e2e8f0;--border-radius-md:10px;
}}
*{{box-sizing:border-box;}}
body{{margin:0;background:var(--bg);color:var(--text);font-family:var(--font-sans);font-size:15px;line-height:1.6;}}
header{{background:linear-gradient(135deg,var(--accent),var(--accent2));color:#fff;padding:22px 28px;}}
header h1{{margin:0;font-size:21px;font-weight:700;letter-spacing:.01em;}}
header .meta{{font-size:13px;opacity:.9;margin-top:5px;}}
main{{max-width:1040px;margin:22px auto;padding:0 16px;display:flex;flex-direction:column;gap:18px;}}
@keyframes fade{{from{{opacity:0;transform:translateY(8px)}}to{{opacity:1;transform:none}}}}
main>*{{animation:fade .35s ease both;}}
.hero{{background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:20px 24px;box-shadow:var(--shadow);}}
.hero .lead{{font-size:12px;color:var(--muted);letter-spacing:.08em;text-transform:uppercase;font-weight:600;}}
.hero .est{{font-size:38px;font-weight:800;color:var(--text);margin:6px 0 2px;font-variant-numeric:tabular-nums;line-height:1.1;}}
.hero .est .ci{{font-size:19px;color:var(--muted);font-weight:700;margin-left:6px;}}
.hero .est .sm{{font-size:17px;color:var(--accent);font-weight:700;}}
.hero .sub{{margin-top:8px;font-size:15px;display:flex;align-items:center;gap:10px;flex-wrap:wrap;}}
.interp-card{{background:var(--card);border:1px solid var(--border);border-left:4px solid var(--accent);border-radius:var(--radius);padding:16px 20px;box-shadow:var(--shadow);}}
.interp-header{{font-size:15px;font-weight:700;color:var(--text);margin-bottom:10px;}}
.interp-conclusion{{font-size:15px;line-height:1.7;color:var(--text);margin-bottom:12px;padding-bottom:10px;border-bottom:1px solid var(--border);}}
.interp-section{{margin-top:8px;}}
.interp-label{{font-size:13px;font-weight:700;color:var(--muted);margin-bottom:4px;}}
.interp-section ul{{margin:0;padding-left:18px;list-style:disc;}}
.interp-section li{{font-size:14px;line-height:1.6;color:var(--text);margin-bottom:3px;}}
.interp-grade{{display:inline-block;padding:2px 8px;border-radius:4px;background:#eef6f4;color:#0d6e5a;font-weight:700;font-size:12px;margin-right:6px;}}
.interp-overclaim{{display:inline-block;padding:2px 8px;border-radius:4px;background:#fef3c7;color:#92400e;font-weight:700;font-size:12px;margin-right:6px;}}
.badge{{display:inline-flex;align-items:center;gap:6px;padding:3px 11px;border-radius:999px;font-size:13px;font-weight:700;}}
.badge.ok{{background:#dcfce7;color:#166534;}}
.badge.warn{{background:#fef3c7;color:#92400e;}}
.badge.bad{{background:#fee2e2;color:#991b1b;}}
.badge .dot{{width:7px;height:7px;border-radius:50%;background:currentColor;}}
.figure-card{{background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:14px 16px 16px;box-shadow:var(--shadow);transition:box-shadow .2s,transform .2s;}}
.figure-card:hover{{box-shadow:var(--shadow-hover);transform:translateY(-2px);}}
.figure-card .cap{{display:flex;align-items:center;gap:8px;font-size:16px;font-weight:600;color:var(--text);margin:0 0 10px;padding-bottom:8px;border-bottom:1px solid var(--border);}}
.figure-card .cap .ico{{font-size:16px;}}
.figure-card .svg-wrap{{overflow-x:auto;}}
.fig-note{{margin:10px 2px 0;padding:9px 13px;font-size:13px;line-height:1.6;color:#334155;background:#eef6f4;border:1px solid #bfe3da;border-radius:var(--radius);}}
.fig-note.warn{{background:#fef6e7;border-color:#f3d28a;color:#8a5a00;}}
.group{{background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:14px 18px 16px;box-shadow:var(--shadow);}}
.group h3{{font-size:16px;margin:0 0 12px;display:flex;align-items:center;gap:8px;color:var(--text);}}
.group h3 .ico{{font-size:16px;}}
.kv{{display:grid;grid-template-columns:1fr auto;gap:6px 16px;font-size:15px;}}
.kv .k{{color:var(--muted);}}
.kv .v{{font-weight:700;font-variant-numeric:tabular-nums;text-align:right;}}
.checks{{list-style:none;padding:0;margin:10px 0 0;display:flex;flex-direction:column;gap:6px;}}
.checks li{{display:flex;align-items:flex-start;gap:8px;font-size:15px;}}
.checks .cdot{{margin-top:5px;width:8px;height:8px;border-radius:50%;flex:none;}}
.cdot.ok{{background:var(--ok);}} .cdot.warn{{background:var(--warn);}} .cdot.bad{{background:var(--bad);}}
.checks-kv{{margin-top:10px;}}
.checks-kv .k{{display:flex;align-items:center;gap:8px;color:inherit;}}
.checks-kv .v.ok{{color:var(--ok);}}
.checks-kv .v.warn{{color:var(--warn);}}
.checks-kv .v.bad{{color:var(--bad);}}
.checks-kv .cdot{{margin-top:0;}}
details.repro{{background:#eef1f5;border:1px solid var(--border);border-radius:var(--radius);overflow:hidden;box-shadow:var(--shadow);}}
details.repro summary{{cursor:pointer;padding:13px 18px;font-size:14px;font-weight:600;color:#1e293b;outline:none;display:flex;justify-content:space-between;align-items:center;list-style:none;}}
details.repro summary::-webkit-details-marker{{display:none;}}
details.repro .body{{padding:0 18px 18px;}}
details.repro .meta{{font-size:12px;color:#57606a;margin:0 0 10px;}}
details.repro pre{{margin:0;max-height:440px;overflow:auto;background:#e3e8ee;padding:14px;border:1px solid #d0d7de;border-radius:8px;}}
details.repro code{{font-family:"SFMono-Regular",Consolas,Menlo,monospace;font-size:13px;white-space:pre-wrap;overflow-wrap:anywhere;word-break:break-word;line-height:1.6;color:#24292e;}}
details.repro code .c{{color:#6a737d;font-style:italic;}}
details.repro code .s{{color:#032f62;}}
details.repro code .f{{color:#6f42c1;}}
details.repro code .n{{color:#005cc5;}}
.copy-btn{{font-size:12px;color:#57606a;background:#eaeef2;border:1px solid #d0d7de;border-radius:6px;padding:3px 9px;cursor:pointer;}}
.copy-btn:hover{{color:#1e293b;border-color:#b0b8c0;}}
.banner{{background:#fef3c7;border:1px solid #f59e0b;color:#92400e;border-radius:var(--radius);padding:11px 15px;font-size:14px;}}
footer{{text-align:center;color:var(--muted);font-size:12px;padding:18px;}}
@media (max-width:640px){{main{{padding:0 10px;}} .hero .est{{font-size:30px;}}}}
@media print{{body{{background:#fff;}} header{{background:var(--accent)!important;-webkit-print-color-adjust:exact;print-color-adjust:exact;}} .figure-card,.group,.hero{{box-shadow:none;break-inside:avoid;}} .copy-btn{{display:none;}} .figure-card .svg-wrap svg{{max-width:100%!important;}} main>*{{animation:none;}}}}
</style></head>
<body>
<header><h1>{result_report} · {task}</h1>
<div class="meta">{generated} {ts}</div></header>
<main>
{banner}
{hero}
{interp}
{publication}
{figures}
{stats_groups}
{repro}
</main>
<footer>{footer_txt}</footer>
<script>
function copyR(btn){{
  var pre=btn.closest('details').querySelector('pre');
  navigator.clipboard.writeText(pre.innerText).then(function(){{
    var t=btn.textContent;btn.textContent='{copied_txt}';setTimeout(function(){{btn.textContent=t;}},1500);
  }});
}}
</script>
</body></html>"""


def render_html_report(out, out_dir: str = ".", titles: list | None = None,
                       locale: str = "zh") -> str | None:
    """把分析结果拼成单文件聚合 HTML 报告（内联 SVG + 统计表 + 折叠 R 代码）。

    固化发生在**本地 agent 侧**：coze 返回体仅含 `stats` + S3 `url`（不受 4000 截断影响），
    此处把已下载回填的 `figures[].svg` / `repro['r']` 固化进 HTML，S3 链接过期也不影响。

    返回 html 文件路径（成功）或 None（无图且无 stats/复现，或写出失败）。
    """
    T = _t(locale)
    figs = out.get("figures") or []
    inline = [f for f in figs if f.get("svg")]
    stats = out.get("stats")
    repro = out.get("repro")
    has_content = bool(inline) or stats is not None or (
        isinstance(repro, dict) and repro.get("r")
    )
    if not has_content:
        return None

    # 图形标题：优先调用方传入，否则按 type 生成中文名
    type_names = {
        "forest": T["fig_forest"], "funnel": T["fig_funnel"],
        "prisma": T["fig_prisma"], "prisma_flow": T["fig_prisma"],
        "rob": T["fig_rob"], "rob2": T["fig_rob"],
        "cumulative": T["fig_cumulative"], "baujat": T["fig_baujat"],
        "labbe": T["fig_labbe"], "radial": T["fig_radial"],
        "sucra": T["fig_sucra"], "egger": T["fig_egger"],
        "contribution": T["fig_contribution"], "loo": T["fig_loo"],
        "gosh": T["fig_gosh"], "bubble": T["fig_bubble"],
        "netgraph": T["fig_netgraph"], "dose_resp": T["fig_dose_resp"],
        "drapery": T["fig_drapery"], "sroc": T["fig_sroc"],
        "tsa": T["fig_tsa"], "power": T["fig_power"],
        "influence": T["fig_influence"], "nodesplit": T["fig_nodesplit"],
        "trimfill": T["fig_trimfill"], "netleague": T["fig_netleague"],
        "sens_forest": T["fig_sens_forest"], "spec_forest": T["fig_spec_forest"],
    }
    if titles is None:
        titles = []
        for i, f in enumerate(inline):
            t = f.get("type") or f"fig{i + 1}"
            titles.append(type_names.get(t, t))

    figures_html = build_figure_widget(inline, titles, card=True) if inline else ""

    # 2026-08-27 防御 / 口径说明（task #5 / 问题二防护）：
    # 随机效应模型下，森林图头条菱形 = 随机效应(REML)合并估计，与 stats.pooled 对齐；
    # 此前 coze 默认把固定效应画成头条、造成读图误导。现 coze 端已修复头条口径，
    # 此处再补一行文字说明，避免用户重复困惑。仅当存在 forest 图且模型为 random 时追加。
    has_forest = any((f.get("type") == "forest") for f in inline)
    model_is_random = isinstance(stats, dict) and stats.get("model") == "random"
    if has_forest and model_is_random:
        figures_html += (
            '<div class="fig-note">'
            '📌 森林图头条菱形为<strong>随机效应（REML）</strong>合并估计，'
            '与上方"合并效应量"卡片口径一致；固定效应估计不单独显示。'
            '</div>'
        )

    # 2026-08-27 防御 / 缺失告警（task #4 / 问题一防护）：
    # 亚组分析/ meta 回归请求了组间差异检验，但 coze 未返回 subgroup_test（历史 bug：静默 null）——

    # 此时 stats.subgroups 应有值而 subgroup_test 为 null。给出告警提示「需重建 coze 镜像」，
    # 而非让用户误以为没有组间差异。仅作展示层兜底，不替代 R 端计算。
    req_task = str(out.get("task") or "")
    is_subgroup_req = req_task in ("subgroup_analysis", "metareg")
    sg_present = isinstance(stats, dict) and isinstance(stats.get("subgroups"), dict) and len(stats.get("subgroups")) > 0
    sgt_missing = isinstance(stats, dict) and not isinstance(stats.get("subgroup_test"), dict)
    if is_subgroup_req and sg_present and sgt_missing:
        figures_html += (
            '<div class="fig-note warn">'
            '⚠️ 已识别到亚组合并结果，但 coze 未返回<strong>组间差异检验（subgroup_test）</strong>。'
            '这是 2026-08-27 前镜像的已知缺陷（Q_between 静默漏序列化）。'
            '请确认 coze 镜像已重建至含本修复的版本；当前报告的组间差异需以重建后结果为准。'
            '</div>'
        )

    # 2026-09-08 netleague 渲染兜底：netleague 按设计是表格型输出（stats.extra.league_table，
    # netmeta 空格对齐文本表）而非 SVG figure；此前呈现层无消费方 → R 端算了表格也静默丢失
    # （用户视角即 "NMA 没有 league 表"）。此处用等宽 <pre> 保真展示——解析成 HTML 表格
    # 对空格对齐过于脆弱，不做。
    _lg = (stats.get("extra") or {}).get("league_table") if isinstance(stats, dict) else None
    if _lg:
        figures_html += (
            '<div class="figure-card"><p class="cap"><span class="ico">📋</span>'
            + T.get("fig_netleague", "网络证据表")
            + '</p><div class="svg-wrap"><pre style="font:12px/1.55 Consolas,\'Courier New\',monospace;'
              'overflow-x:auto;margin:0;white-space:pre;">'
            + _html.escape(str(_lg))
            + "</pre></div></div>"
        )

    hero_html = _render_hero(stats, out.get("task"), T) if stats else ""

    # 2026-09-13 结果解读卡（统计顾问层）：结论 + 警告 + 建议 + 审稿人问题
    interp_html = ""
    interp = out.get("_interpretation") if isinstance(out, dict) else None
    qa = out.get("_quality_advice") if isinstance(out, dict) else None
    if isinstance(interp, dict) and any(interp.values()):
        interp_parts = []
        if interp.get("conclusion"):
            interp_parts.append(
                '<div class="interp-conclusion">%s</div>' % _html_escape(interp["conclusion"])
            )
        caveats = interp.get("caveats") or []
        if caveats:
            interp_parts.append('<div class="interp-section"><div class="interp-label">⚠ 注意事项</div><ul>' +
                                "".join("<li>%s</li>" % _html_escape(c) for c in caveats) +
                                "</ul></div>")
        suggestions = interp.get("suggestions") or []
        if suggestions:
            interp_parts.append('<div class="interp-section"><div class="interp-label">💡 建议</div><ul>' +
                                "".join("<li>%s</li>" % _html_escape(s) for s in suggestions) +
                                "</ul></div>")
        rq = interp.get("reviewer_questions") or []
        if rq:
            interp_parts.append('<div class="interp-section"><div class="interp-label">🔍 审稿人可能问</div><ul>' +
                                "".join("<li>%s</li>" % _html_escape(q) for q in rq) +
                                "</ul></div>")
        # 2026-09-13 质量评估摘要（GRADE + 过度声明）
        # 2026-09-14：网络 Meta 改走 CINeMA 六域 → 徽章按 framework 标注，并展开各域明细
        # （域评级 no/some/major_concerns + unclear，unclear 表示统计侧拿不到数据、须人工补）。
        if isinstance(qa, dict) and qa.get("summary"):
            qa_parts = []
            g_obj = qa.get("grade") or {}
            grade = g_obj.get("grade", "") if isinstance(g_obj, dict) else str(g_obj or "")
            fw = qa.get("framework") or (g_obj.get("framework") if isinstance(g_obj, dict) else "")
            is_cinema = fw == "CINeMA"
            if grade:
                if is_cinema:
                    qa_parts.append('<span class="interp-grade">CINeMA: %s</span>'
                                    % _html_escape(_CINEMA_RATING_CN.get(grade, grade)))
                else:
                    qa_parts.append('<span class="interp-grade">GRADE: %s</span>'
                                    % _html_escape(grade))
            n_overclaim = (qa.get("quality_gate") or {}).get("n_overclaim", 0)
            if n_overclaim:
                qa_parts.append('<span class="interp-overclaim">⚠ %d 条过度声明</span>' % n_overclaim)
            detail = ""
            cg = qa.get("cinema")
            if is_cinema and isinstance(cg, dict) and cg.get("domains"):
                rows = []
                for name, d in cg["domains"].items():
                    if not isinstance(d, dict):
                        continue
                    rows.append(
                        '<div style="font-size:13px;line-height:1.65;margin-top:2px;">'
                        '<b>%s</b>：%s —— <span style="color:var(--muted);">%s</span></div>'
                        % (_html_escape(_CINEMA_DOMAIN_CN.get(name, name)),
                           _html_escape(_CINEMA_RATING_CN.get(d.get("rating", ""),
                                                              str(d.get("rating") or ""))),
                           _html_escape(str(d.get("reason") or ""))))
                detail = "".join(rows)
            if qa_parts or detail:
                summary_html = ('<div style="margin-top:4px;font-size:13px;color:var(--muted);">%s</div>'
                                % _html_escape(qa["summary"]))
                interp_parts.append(
                    '<div class="interp-section"><div class="interp-label">📋 质量评估</div>'
                    '<div class="interp-qa">' + " ".join(qa_parts) + summary_html + detail
                    + "</div></div>"
                )
        if interp_parts:
            interp_html = (
                '<div class="interp-card"><div class="interp-header">📊 结果解读</div>' +
                "".join(interp_parts) + "</div>"
            )

    # 2026-09-14 发表建议卡（writing_advisor）：期刊推荐 / 限制 / 讨论模板 / 审稿人问题 / 参考核验
    pub_html = ""
    pa = out.get("_publication_advice") if isinstance(out, dict) else None
    if isinstance(pa, dict) and any(pa.values()):
        pub_html = _publication_advice_card(pa, T)

    stats_html = _render_stats_groups(stats, T) if stats is not None else ""

    repro_html = ""
    if isinstance(repro, dict) and repro.get("r"):
        rcode = _highlight_r(_pretty_r(repro["r"]))
        meta_bits = []
        if repro.get("r_version"):
            meta_bits.append(f"R {_html_escape(str(repro['r_version']))}")
        pkgs = repro.get("packages") or {}
        if isinstance(pkgs, dict):
            meta_bits.append(
                "；".join(f"{_html_escape(k)} {_html_escape(str(v))}" for k, v in pkgs.items())
            )
        meta_line = " · ".join(meta_bits)
        repro_html = (
            '<details class="repro">'
            f'<summary><span>{T["repro_title"]}</span><span class="copy-btn">{T["repro_copy"]}</span></summary>'
            f'<div class="body"><div class="meta">{meta_line}</div>'
            f'<pre><code>{rcode}</code></pre></div>'
            '</details>'
        )

    trunc = out.get("_coze_truncated")
    trunc_banner = ""
    if trunc:
        items = "、".join(_html_escape(str(x)) for x in trunc)
        trunc_banner = (
            f'<div class="banner">{T["trunc_prefix"]}{items}{T["trunc_suffix"]}</div>'
        )

    # 契约漂移横幅（coze 响应结构与本地技能预期不一致时提醒升级；text 已由 coze_client 填入 _contract_drift）
    drift = out.get("_contract_drift")
    drift_banner = ""
    if out.get("_needs_upgrade") and isinstance(drift, list) and drift:
        items_html = "".join(
            f"<div>· {_html_escape(str(d))}</div>" for d in drift
        )
        drift_banner = (
            f'<div class="banner"><strong>{T["contract_drift_prefix"]}</strong>'
            f'<div style="margin-top:6px;font-weight:400;">{items_html}</div></div>'
        )

    # 端点回退横幅（主工作流地址切换、已自动回退备用 coze 端点；用户可见提示唯一出口）
    endpoint_banner = ""
    if out.get("_coze_endpoint_notice"):
        endpoint_banner = (
            f'<div class="banner">{T["endpoint_fallback_prefix"]}</div>'
        )

    task = _html_escape(str(out.get("task") or ""))
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    html = _REPORT_TEMPLATE.format(
        task=task, ts=ts,
        html_lang=T["html_lang"], report_title=T["report_title"],
        result_report=T["result_report"], generated=T["generated"],
        footer_txt=T["footer"], copied_txt=T["copied"],
        banner=trunc_banner + drift_banner + endpoint_banner, hero=hero_html, figures=figures_html,
        interp=interp_html,
        stats_groups=stats_html, repro=repro_html, publication=pub_html,
    )

    try:
        os.makedirs(out_dir, exist_ok=True)
        fname = f"meta_report_{out.get('task') or 'analysis'}_{locale}_{int(datetime.datetime.now().timestamp())}.html"
        fpath = os.path.join(out_dir, fname)
        with open(fpath, "w", encoding="utf-8") as fh:
            fh.write(html)
        return fpath
    except Exception:
        return None


if __name__ == "__main__":
    import sys

    # 自测：python rendering.py <case.json> [titles...]
    import json

    env = json.load(open(sys.argv[1], encoding="utf-8"))
    figs = env.get("figures") or env.get("result", {}).get("figures") or []
    titles = sys.argv[2:] or [f"图 {i+1}" for i in range(len(figs))]
    print(build_figure_widget(figs, titles))
