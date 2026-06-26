"""big_stat — 单数字大字页（Apple 发布会招牌页）。

Apple 在发布会 1 张 slide 只放一个数字，比如 "2 Billion"、"100M"。
这个模板就是给这种时刻准备的。

data:
  value:     str            要放大的数字/短语（"2", "100M", "1,000,000"）
  unit:      str (optional) 单位（"Billion", "Users", "%"）
  caption:   str (optional) 数字上方的一句说明（小字）
  footnote:  str (optional) 数字下方的一句说明
  accent:    bool (optional) 数字是否用 accent 颜色（默认 text_primary）
"""

from .helpers import (
    new_slide, add_text, add_hline, fit_font_size,
    apply_text_gradient, add_glow_halo,
)


def build(prs, pack, data: dict) -> None:
    slide = new_slide(prs, pack)
    W, H = pack.canvas.width, pack.canvas.height
    t = pack.typography
    sp = pack.spacing
    dec = pack.decoration

    value = data.get('value', '')
    unit = data.get('unit', '')
    caption = data.get('caption', '')
    footnote = data.get('footnote', '')
    use_accent = data.get('accent', False)

    value_color = 'accent' if use_accent else 'text_primary'

    # 布局预算：从顶部 caption 到底部 footnote 之间留给 stat + unit
    caption_top = H * 0.18
    caption_h = 0.4
    footnote_top = H - 0.9
    usable_top = caption_top + caption_h + 0.3
    usable_bot = footnote_top - 0.3
    usable_h = usable_bot - usable_top  # 给 stat + unit 的总纵向空间

    # 保留 unit 所需空间（如果有 unit）
    unit_size = max(24, t.page_title)
    unit_h = (unit_size / 72.0) * 1.3 if unit else 0.0
    unit_gap = 0.15 if unit else 0.0

    # stat 能用的高度
    stat_budget_h = usable_h - unit_h - unit_gap
    # stat 字号先按 pack 预设，再被 width + height 双约束
    stat_size_max_by_h = stat_budget_h / 1.15 * 72
    stat_w = W - 2 * sp.margin_x_hero
    stat_size_try = min(dec.stat_hero_size, stat_size_max_by_h)
    stat_size = fit_font_size(str(value), stat_w, stat_size_try,
                              min_size_pt=80, max_lines=1)
    stat_h = stat_size / 72.0 * 1.15

    # 整体 stat + unit 块垂直居中
    total_block_h = stat_h + unit_gap + unit_h
    block_top = usable_top + (usable_h - total_block_h) / 2

    # 顶部 caption
    if caption:
        cap = caption.upper() if t.uppercase_en_sub else caption
        add_text(slide, pack, cap,
                 left=sp.margin_x_hero, top=caption_top,
                 width=W - 2 * sp.margin_x_hero, height=caption_h,
                 font=t.body_font, font_size=t.page_sub,
                 weight='semibold',
                 color_key='accent',
                 align='center',
                 tracking=0.2 if t.uppercase_en_sub else 0.05)

    # 科技风：在 stat 下叠辉光
    if dec.glow_accent and use_accent:
        halo_cx = W / 2
        halo_cy = block_top + stat_h * 0.5
        add_glow_halo(slide, pack, halo_cx, halo_cy,
                      radius=stat_size / 72.0 * 1.6,
                      color_key='accent', layers=5,
                      strength=dec.glow_strength)

    # 巨字号数字
    stat_tb = add_text(slide, pack, str(value),
             left=sp.margin_x_hero, top=block_top,
             width=stat_w, height=stat_h,
             font_size=stat_size,
             weight=dec.stat_hero_weight,
             color_key=value_color,
             align='center',
             tracking=-0.04,
             leading=0.9)

    # 如果 pack 开启了 accent_gradient 且 stat 用 accent，给数字注入渐变
    if use_accent and dec.accent_gradient is not None:
        runs = stat_tb.text_frame.paragraphs[0].runs
        if runs:
            apply_text_gradient(runs[0], dec.accent_gradient[0], dec.accent_gradient[1], angle_deg=0)

    # 单位
    if unit:
        add_text(slide, pack, unit,
                 left=sp.margin_x_hero,
                 top=block_top + stat_h + unit_gap,
                 width=W - 2 * sp.margin_x_hero, height=unit_h,
                 font_size=unit_size,
                 weight='semibold',
                 color_key='text_secondary',
                 align='center',
                 tracking=t.page_tracking)

    # 底部说明
    if footnote:
        add_text(slide, pack, footnote,
                 left=sp.margin_x_hero, top=footnote_top,
                 width=W - 2 * sp.margin_x_hero, height=0.5,
                 font=t.body_font, font_size=t.caption + 2,
                 color_key='text_tertiary',
                 align='center')
