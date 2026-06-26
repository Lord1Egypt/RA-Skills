"""kpi_triple — 3 宫格 KPI 卡。

典型：3 个数据点并列，每个一个大数字 + 标签。

data:
  title:    str (optional)   页面标题
  en_sub:   str (optional)   英文副标
  items:    list[dict]       每个 dict:
              value:   str   数字（"87%"）
              label:   str   标签（"用户留存率"）
              caption: str   说明（optional）
"""

from .helpers import (
    new_slide, add_text, add_card, add_page_header, add_page_footer,
    fit_font_size,
)


def build(prs, pack, data: dict) -> None:
    slide = new_slide(prs, pack)
    W, H = pack.canvas.width, pack.canvas.height
    t = pack.typography
    sp = pack.spacing
    elev = pack.elevation

    # 标题（可选）
    y_top = 0.5
    title = data.get('title', '')
    en_sub = data.get('en_sub', '')
    if title:
        y_top = add_page_header(slide, pack, title, en_sub)
    else:
        y_top = H * 0.25

    items = data.get('items', [])[:3]
    if not items:
        return

    n = len(items)
    # 卡片布局
    usable_w = W - 2 * sp.margin_x
    gap = sp.stack_md
    card_w = (usable_w - gap * (n - 1)) / n
    card_h = min(3.5, H - y_top - 1.2)
    card_top = y_top + sp.stack_md

    for i, item in enumerate(items):
        left = sp.margin_x + i * (card_w + gap)
        # 卡片背景
        add_card(slide, pack, left, card_top, card_w, card_h)

        # 卡片内文字布局（居中）
        pad_x = sp.card_pad_x
        inner_w = card_w - 2 * pad_x
        # 数字 — 自适应缩字避免溢出（"99.97%" / "$4.8M" 这种长数字常见）
        value = item.get('value', '')
        value_size_base = max(48, int(t.section * 0.65))
        value_size = fit_font_size(str(value), inner_w, value_size_base,
                                   min_size_pt=32, max_lines=1)
        value_h = value_size / 72.0 * 1.2
        value_top = card_top + card_h * 0.28
        add_text(slide, pack, value,
                 left=left + pad_x, top=value_top,
                 width=inner_w, height=value_h,
                 font_size=value_size, weight='bold',
                 color_key='accent',
                 align='center',
                 tracking=-0.02,
                 leading=1.0)

        # 标签
        label = item.get('label', '')
        label_top = value_top + value_h + 0.1
        add_text(slide, pack, label,
                 left=left + pad_x, top=label_top,
                 width=inner_w, height=0.5,
                 font_size=t.card_title, weight=t.card_weight,
                 color_key='text_primary',
                 align='center')

        # 说明
        caption = item.get('caption', '')
        if caption:
            cap_top = label_top + 0.5
            add_text(slide, pack, caption,
                     left=left + pad_x, top=cap_top,
                     width=inner_w, height=0.8,
                     font=t.body_font, font_size=t.caption + 2,
                     color_key='text_tertiary',
                     align='center',
                     leading=t.body_leading)

    # 页脚
    page_no = data.get('page', 0)
    company = data.get('company', '')
    if company:
        add_page_footer(slide, pack, company, page_no)
