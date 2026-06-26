"""section_divider — 分章大字页。

data:
  number:   str (optional)    "01" / "02" 章节号
  title:    str               章节主标题
  subtitle: str (optional)    副标题
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

    number = data.get('number')
    title = data.get('title', '')
    subtitle = data.get('subtitle', '')

    # 1. 先算每一块的实际高度
    number_size = max(56, t.section - 20) if number else 0
    number_h = (number_size / 72.0) * 1.2 if number else 0
    number_gap = 0.2 if number else 0

    sec_w = W - 2 * sp.margin_x_hero
    sec_size = fit_font_size(title, sec_w, t.section,
                             min_size_pt=36, max_lines=1)
    title_h = (sec_size / 72.0) * (t.hero_leading + 0.1)  # 留一点
    title_gap = 0.3 if subtitle else 0

    sub_size = t.page_title - 8 if subtitle else 0
    sub_h = (sub_size / 72.0) * 1.4 if subtitle else 0

    total_h = number_h + number_gap + title_h + title_gap + sub_h
    # 垂直居中整体
    y0 = (H - total_h) / 2

    # 2. 章节号
    y = y0
    if number:
        # 科技风 halo
        if dec.glow_accent:
            align = dec.cover_hero_align
            if align == 'center':
                halo_cx = W / 2
            elif align == 'left':
                halo_cx = sp.margin_x_hero + number_size / 72.0 * 0.5
            else:
                halo_cx = W - sp.margin_x_hero - number_size / 72.0 * 0.5
            halo_cy = y + number_h / 2
            add_glow_halo(slide, pack, halo_cx, halo_cy,
                          radius=number_size / 72.0 * 1.2,
                          color_key='accent', layers=4,
                          strength=dec.glow_strength * 0.8)

        num_tb = add_text(slide, pack, number,
                 left=sp.margin_x_hero, top=y,
                 width=sec_w, height=number_h,
                 font_size=number_size,
                 weight='semibold',
                 color_key='accent',
                 align=dec.cover_hero_align,
                 tracking=-0.02,
                 leading=1.0)
        # 渐变文字
        if dec.accent_gradient is not None:
            runs = num_tb.text_frame.paragraphs[0].runs
            if runs:
                apply_text_gradient(runs[0], dec.accent_gradient[0], dec.accent_gradient[1], angle_deg=0)
        y += number_h + number_gap

    # 3. 主标题
    add_text(slide, pack, title,
             left=sp.margin_x_hero, top=y,
             width=sec_w, height=title_h,
             font_size=sec_size, weight=t.section_weight,
             color_key='text_primary',
             align=dec.cover_hero_align,
             tracking=t.section_tracking,
             leading=t.hero_leading)
    y += title_h + title_gap

    # 4. 副标题
    if subtitle:
        add_text(slide, pack, subtitle,
                 left=sp.margin_x_hero, top=y,
                 width=sec_w, height=sub_h,
                 font_size=sub_size, weight='regular',
                 color_key='text_secondary',
                 align=dec.cover_hero_align)

    # 5. 底部小横线（Apple 暗场会有）
    if pack.name == 'apple-keynote':
        add_hline(slide, pack, W / 2 - 0.8, H - 1.2, 1.6,
                  color_key='accent', thickness=0.025)
