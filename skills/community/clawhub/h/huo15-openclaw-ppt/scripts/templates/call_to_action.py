"""call_to_action — 行动号召（封底页）。

典型：大字主语 + 辅助信息 + 一个 call-to-action（邮箱/网址/微信号）。

data:
  title:    str            大字主语（"Thank You." / "让我们开始吧。"）
  subtitle: str (optional) 下方说明
  cta:      str (optional) 联系方式/行动项（"hello@huo15.com"）
  footnote: str (optional) 底部小字
"""

from .helpers import new_slide, add_text, add_hline, fit_font_size


def build(prs, pack, data: dict) -> None:
    slide = new_slide(prs, pack)
    W, H = pack.canvas.width, pack.canvas.height
    t = pack.typography
    sp = pack.spacing
    dec = pack.decoration

    title = data.get('title', 'Thank You.')
    subtitle = data.get('subtitle', '')
    cta = data.get('cta', '')
    footnote = data.get('footnote', '')

    # 顶部装饰线
    if dec.cover_top_line:
        add_hline(slide, pack, sp.margin_x_hero, 0.5,
                  W - 2 * sp.margin_x_hero,
                  color_key='accent', thickness=0.015)

    # 主标题（比封面略小一号，给 cta 留位置）+ auto-fit
    base_size = int(t.hero * 0.85)
    hero_w = W - 2 * sp.margin_x_hero
    hero_size = fit_font_size(title, hero_w, base_size,
                              min_size_pt=48, max_lines=1)
    if dec.cover_hero_align == 'center':
        hero_top = H * 0.3
    else:
        hero_top = H * 0.38

    add_text(slide, pack, title,
             left=sp.margin_x_hero, top=hero_top,
             width=hero_w, height=H * 0.35,
             font_size=hero_size, weight=t.hero_weight,
             color_key='text_primary',
             align=dec.cover_hero_align,
             tracking=t.hero_tracking,
             leading=t.hero_leading)

    # 副标题
    y = hero_top + (hero_size / 72.0) * 1.3
    if subtitle:
        add_text(slide, pack, subtitle,
                 left=sp.margin_x_hero, top=y,
                 width=W - 2 * sp.margin_x_hero, height=0.7,
                 font_size=t.page_title - 8, weight='regular',
                 color_key='text_secondary',
                 align=dec.cover_hero_align,
                 tracking=t.page_tracking)
        y += 0.7

    # CTA（联系方式 —— 强调色）
    if cta:
        add_text(slide, pack, cta,
                 left=sp.margin_x_hero, top=y + 0.2,
                 width=W - 2 * sp.margin_x_hero, height=0.5,
                 font_size=t.card_title + 4, weight='semibold',
                 color_key='accent',
                 align=dec.cover_hero_align,
                 tracking=0.03)

    # Footnote
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
