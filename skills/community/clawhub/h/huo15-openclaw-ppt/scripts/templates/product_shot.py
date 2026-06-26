"""product_shot — 产品摄影页（Apple.com 风）。

结构：左文右图（或上文下图），图占大块面积。

data:
  title:     str
  en_sub:    str (optional)
  kicker:    str (optional)   图上方的小字
  subtitle:  str (optional)   副标（比 title 小的描述）
  image:     str              图片路径（没有则空白占位）
  bullets:   list[str] (optional)  补充要点
  layout:    'left' | 'right' | 'top' (default 'right')
             图在左/右/上
"""

from .helpers import (
    new_slide, add_text, add_image, add_page_header, add_page_footer,
)


def build(prs, pack, data: dict) -> None:
    slide = new_slide(prs, pack)
    W, H = pack.canvas.width, pack.canvas.height
    t = pack.typography
    sp = pack.spacing
    dec = pack.decoration

    title = data.get('title', '')
    en_sub = data.get('en_sub', '')
    kicker = data.get('kicker', '')
    subtitle = data.get('subtitle', '')
    image = data.get('image')
    bullets = data.get('bullets', [])
    layout = data.get('layout', 'right')

    # 产品页的标题可以在图上面或旁边，这里先用 page header
    y_top = add_page_header(slide, pack, title, en_sub) if title else 0.6

    # 图片 + 文字区
    rounded = dec.image_treatment == 'rounded'

    if layout == 'top':
        # 图片铺满上半屏，文字在下
        img_h = (H - y_top) * 0.6
        img_top = y_top + sp.stack_sm
        img_left = sp.margin_x
        img_w = W - 2 * sp.margin_x
        add_image(slide, pack, image,
                  img_left, img_top, img_w, img_h,
                  rounded=rounded)

        # 下面放 kicker/subtitle/bullets
        y = img_top + img_h + sp.stack_md
        _draw_text_block(slide, pack, sp.margin_x, y, img_w, H - y - 0.8,
                         kicker, subtitle, bullets)
    else:
        # 左/右布局
        text_w = (W - 2 * sp.margin_x) * 0.42
        img_w = (W - 2 * sp.margin_x) * 0.55
        gap = (W - 2 * sp.margin_x - text_w - img_w)

        img_h = H - y_top - 1.2
        img_top = y_top + sp.stack_sm

        if layout == 'left':
            img_left = sp.margin_x
            text_left = sp.margin_x + img_w + gap
        else:  # right
            text_left = sp.margin_x
            img_left = sp.margin_x + text_w + gap

        add_image(slide, pack, image,
                  img_left, img_top, img_w, img_h,
                  rounded=rounded)

        _draw_text_block(slide, pack, text_left, img_top, text_w, img_h,
                         kicker, subtitle, bullets)

    # 页脚
    page_no = data.get('page', 0)
    company = data.get('company', '')
    if company:
        add_page_footer(slide, pack, company, page_no)


def _draw_text_block(slide, pack, left, top, w, h,
                     kicker, subtitle, bullets):
    t = pack.typography
    sp = pack.spacing

    y = top

    if kicker:
        k = kicker.upper() if t.uppercase_en_sub else kicker
        add_text(slide, pack, k,
                 left=left, top=y, width=w, height=0.35,
                 font=t.body_font, font_size=t.page_sub, weight='semibold',
                 color_key='accent',
                 tracking=0.2 if t.uppercase_en_sub else 0.05)
        y += 0.45

    if subtitle:
        add_text(slide, pack, subtitle,
                 left=left, top=y, width=w, height=1.4,
                 font_size=t.card_title + 6, weight='semibold',
                 color_key='text_primary',
                 tracking=t.page_tracking,
                 leading=1.25)
        y += 1.3

    for b in bullets:
        s = b if isinstance(b, str) else b.get('label', str(b))
        add_text(slide, pack, '·  ' + s,
                 left=left, top=y, width=w, height=0.5,
                 font=t.body_font, font_size=t.body + 1,
                 color_key='text_secondary',
                 leading=t.body_leading)
        y += 0.42
