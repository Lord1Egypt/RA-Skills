"""quote_card — 引用金句卡。

一张 slide 就说一句话，大字展示，作者在下。

data:
  quote:   str            引用的话
  author:  str (optional) 作者
  role:    str (optional) 职位/身份
"""

from .helpers import new_slide, add_text, add_hline


def build(prs, pack, data: dict) -> None:
    slide = new_slide(prs, pack)
    W, H = pack.canvas.width, pack.canvas.height
    t = pack.typography
    sp = pack.spacing
    dec = pack.decoration

    quote = data.get('quote', '')
    author = data.get('author', '')
    role = data.get('role', '')

    # 左侧一个大的引号装饰（accent 色）
    quote_mark_size = max(96, t.hero)
    add_text(slide, pack, '\u201C',   # left double quotation mark
             left=sp.margin_x_hero - 0.3, top=H * 0.2,
             width=1.5, height=1.5,
             font_size=quote_mark_size, weight='bold',
             color_key='accent',
             align='left',
             leading=1.0)

    # 引文本体（中等大字）
    quote_size = max(32, int(t.section * 0.55))
    quote_top = H * 0.35
    add_text(slide, pack, quote,
             left=sp.margin_x_hero, top=quote_top,
             width=W - 2 * sp.margin_x_hero, height=H * 0.4,
             font_size=quote_size, weight='semibold',
             color_key='text_primary',
             align='left',
             tracking=t.page_tracking,
             leading=1.25)

    # 分隔线（装饰）
    line_top = H * 0.78
    add_hline(slide, pack, sp.margin_x_hero, line_top, 0.5,
              color_key='accent', thickness=0.02)

    # 作者 + 职位
    if author:
        author_top = line_top + 0.2
        add_text(slide, pack, '— ' + author,
                 left=sp.margin_x_hero, top=author_top,
                 width=W - 2 * sp.margin_x_hero, height=0.4,
                 font_size=t.card_title, weight='semibold',
                 color_key='text_primary',
                 align='left')
        if role:
            role_top = author_top + 0.4
            add_text(slide, pack, role,
                     left=sp.margin_x_hero + 0.25, top=role_top,
                     width=W - 2 * sp.margin_x_hero, height=0.3,
                     font=t.body_font, font_size=t.caption + 2,
                     color_key='text_tertiary',
                     align='left')
