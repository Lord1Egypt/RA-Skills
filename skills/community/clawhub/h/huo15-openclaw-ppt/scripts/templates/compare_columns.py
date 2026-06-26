"""compare_columns — 左右对比栏（before / after、方案 A / B）。

data:
  title:   str
  en_sub:  str (optional)
  left:    dict         { label, title, items: list[str] }
  right:   dict         同上
  emphasize: 'left' | 'right' | 'none'  (default 'right')
"""

from .helpers import (
    new_slide, add_text, add_card, add_page_header, add_page_footer,
    add_hline,
)


def build(prs, pack, data: dict) -> None:
    slide = new_slide(prs, pack)
    W, H = pack.canvas.width, pack.canvas.height
    t = pack.typography
    sp = pack.spacing

    title = data.get('title', '')
    en_sub = data.get('en_sub', '')
    y_top = add_page_header(slide, pack, title, en_sub)

    left_col = data.get('left', {})
    right_col = data.get('right', {})
    emphasize = data.get('emphasize', 'right')

    # 布局：两列居中
    gap = sp.stack_md
    usable_w = W - 2 * sp.margin_x
    col_w = (usable_w - gap) / 2
    col_h = H - y_top - 1.2
    col_top = y_top + sp.stack_md

    for idx, (col_data, which) in enumerate([(left_col, 'left'), (right_col, 'right')]):
        left = sp.margin_x + idx * (col_w + gap)
        is_emph = (emphasize == which)

        # 卡片（被强调的一边用 accent_soft 底）
        if is_emph:
            from .helpers import add_rect
            add_rect(slide, pack, left, col_top, col_w, col_h,
                     fill_key='accent_soft',
                     radius=pack.elevation.card_radius)
        else:
            add_card(slide, pack, left, col_top, col_w, col_h)

        pad_x = sp.card_pad_x + 0.1
        pad_y = sp.card_pad_y + 0.1
        inner_w = col_w - 2 * pad_x
        y = col_top + pad_y

        # 标签（小字 eyebrow —— "BEFORE" / "AFTER"）
        label = col_data.get('label', '')
        if label:
            lbl = label.upper() if t.uppercase_en_sub else label
            add_text(slide, pack, lbl,
                     left=left + pad_x, top=y,
                     width=inner_w, height=0.3,
                     font=t.body_font, font_size=t.caption + 1, weight='semibold',
                     color_key='accent' if is_emph else 'text_tertiary',
                     tracking=0.15 if t.uppercase_en_sub else 0.05)
            y += 0.35

        # 标题
        col_title = col_data.get('title', '')
        if col_title:
            add_text(slide, pack, col_title,
                     left=left + pad_x, top=y,
                     width=inner_w, height=0.6,
                     font_size=t.card_title + 4, weight='semibold',
                     color_key='text_primary',
                     tracking=t.page_tracking)
            y += 0.7

            # 小装饰线
            add_hline(slide, pack,
                      left + pad_x, y - 0.1, 0.4,
                      color_key='accent' if is_emph else 'border',
                      thickness=0.02)
            y += 0.15

        # 条目列表（兼容 items / points 两种 schema 命名）
        items = col_data.get('items') or col_data.get('points') or []
        for it in items:
            s = it if isinstance(it, str) else it.get('label', str(it))
            add_text(slide, pack, '·  ' + s,
                     left=left + pad_x, top=y,
                     width=inner_w, height=0.4,
                     font=t.body_font, font_size=t.body + 1,
                     color_key='text_primary' if is_emph else 'text_secondary',
                     leading=t.body_leading)
            y += 0.45

    # 页脚
    page_no = data.get('page', 0)
    company = data.get('company', '')
    if company:
        add_page_footer(slide, pack, company, page_no)
