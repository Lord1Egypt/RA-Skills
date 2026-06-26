"""hero_cover — 封面 hero 大字。

data:
  title:    str
  subtitle: str (optional)
  eyebrow:  str (optional)  顶部小字（Apple 常用，比如 "INTRODUCING"）
  footnote: str (optional)  底部小字（年份 / 公司）
  image:    str (optional)  背景图路径
"""

from .helpers import (
    new_slide, add_text, add_rect, add_hline, add_image, fit_font_size,
    apply_text_gradient, add_glow_halo, add_dev_badge, format_dev_badge,
    add_mono_text,
)


def build(prs, pack, data: dict) -> None:
    slide = new_slide(prs, pack)
    W, H = pack.canvas.width, pack.canvas.height
    t = pack.typography
    dec = pack.decoration
    sp = pack.spacing

    # 可选背景图
    if data.get('image'):
        add_image(slide, pack, data['image'],
                  left=0, top=0, width=W, height=H)
        # 加一层半透明黑覆盖，保证文字可读
        overlay = add_rect(slide, pack, 0, 0, W, H,
                           fill_key='bg')
        # 半透明度用 XML
        from pptx.oxml.ns import qn
        elem = overlay.fill.fore_color._xFill
        alpha_elem = elem.find(qn('a:alpha'))

    # 顶部装饰线（小红书/复古会有）
    if dec.cover_top_line:
        add_hline(slide, pack, sp.margin_x_hero, 0.5,
                  W - 2 * sp.margin_x_hero,
                  color_key='accent', thickness=0.015)

    # Eyebrow（Apple 常用）
    y = H * 0.2
    eyebrow = data.get('eyebrow')
    if eyebrow:
        ey = eyebrow.upper() if t.uppercase_en_sub else eyebrow
        add_text(slide, pack, ey,
                 left=sp.margin_x_hero, top=y,
                 width=W - 2 * sp.margin_x_hero, height=0.4,
                 font=t.body_font, font_size=t.page_sub, weight='semibold',
                 color_key='accent',
                 align=dec.cover_hero_align,
                 tracking=0.2 if t.uppercase_en_sub else 0.05)
        y += 0.55

    # Hero title
    title = data.get('title', '')
    case = dec.cover_hero_case
    if case == 'upper':
        title = title.upper()
    elif case == 'lower':
        title = title.lower()

    # 居中风格整体上移
    if dec.cover_hero_align == 'center':
        hero_top = H * 0.33
    else:
        hero_top = H * 0.42

    # 自动 fit — 如果是长文本（比如 CJK 7 字以上），降字号保 1 行
    hero_w = W - 2 * sp.margin_x_hero
    hero_size = fit_font_size(title, hero_w, t.hero,
                              min_size_pt=48, max_lines=1)

    # 如果 pack 启用了 glow_accent 且 align 是 left/center → 在 hero 附近画 halo
    if dec.glow_accent:
        halo_cx = W / 2 if dec.cover_hero_align == 'center' else sp.margin_x_hero + hero_w * 0.35
        halo_cy = hero_top + (hero_size / 72.0) * 0.5
        add_glow_halo(slide, pack, halo_cx, halo_cy,
                      radius=hero_size / 72.0 * 2.0,
                      color_key='accent', layers=4,
                      strength=dec.glow_strength)

    hero_tb = add_text(slide, pack, title,
             left=sp.margin_x_hero, top=hero_top,
             width=hero_w, height=H * 0.4,
             font_size=hero_size, weight=t.hero_weight,
             color_key='text_primary',
             align=dec.cover_hero_align,
             tracking=t.hero_tracking,
             leading=t.hero_leading)

    # 如果 pack 有 accent_gradient，给 hero 文字注入渐变填充
    if dec.accent_gradient is not None:
        # 第一段 run 就是 hero 文字
        runs = hero_tb.text_frame.paragraphs[0].runs
        if runs:
            apply_text_gradient(runs[0], dec.accent_gradient[0], dec.accent_gradient[1], angle_deg=0)

    # Subtitle（fit 自适应防溢出 — v5.0.1 修长副标题溢出）
    subtitle = data.get('subtitle', '')
    if subtitle:
        sub_top = hero_top + (hero_size / 72.0) * 1.3  # 在 hero 下方
        sub_w = W - 2 * sp.margin_x_hero
        sub_size = fit_font_size(subtitle, sub_w, t.page_title,
                                 min_size_pt=18, max_lines=2)
        add_text(slide, pack, subtitle,
                 left=sp.margin_x_hero, top=sub_top,
                 width=sub_w, height=0.8,
                 font_size=sub_size, weight='regular',
                 color_key='text_secondary',
                 align=dec.cover_hero_align,
                 tracking=t.page_tracking)

    # Footnote（底部）
    footnote = data.get('footnote', '')
    if footnote:
        add_text(slide, pack, footnote,
                 left=sp.margin_x_hero, top=H - 0.7,
                 width=W - 2 * sp.margin_x_hero, height=0.4,
                 font=t.body_font, font_size=t.caption,
                 color_key='text_tertiary',
                 align=dec.cover_hero_align)

    # 底部装饰线
    if dec.cover_bottom_line:
        add_hline(slide, pack, sp.margin_x_hero, H - 0.35,
                  W - 2 * sp.margin_x_hero,
                  color_key='accent', thickness=0.015)

    # 开发版本戳（科技风专属）
    if dec.dev_badge:
        badge = format_dev_badge(
            pack,
            year=str(data.get('year', '2026')),
            build=str(data.get('build', '0001')),
        )
        add_dev_badge(slide, pack, badge, position='bottom-left')
