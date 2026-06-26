"""content_list — 编号/要点列表页。

最常用的内容页：标题 + 若干条目（每条带编号或点）。

data:
  title:   str
  en_sub:  str (optional)
  items:   list[dict | str]
             如果是 str —— 当成 label
             如果是 dict —— label + (optional) desc + (optional) index
  numbered: bool (default True)   是否显示序号
"""

from .helpers import (
    new_slide, add_text, add_oval, add_page_header, add_page_footer,
)


def build(prs, pack, data: dict) -> None:
    slide = new_slide(prs, pack)
    W, H = pack.canvas.width, pack.canvas.height
    t = pack.typography
    sp = pack.spacing

    title = data.get('title', '')
    en_sub = data.get('en_sub', '')
    y_top = add_page_header(slide, pack, title, en_sub)

    items = data.get('items', [])
    numbered = data.get('numbered', True)

    # 归一化
    norm = []
    for i, it in enumerate(items):
        if isinstance(it, str):
            norm.append({'label': it, 'desc': '', 'index': i + 1})
        else:
            norm.append({
                'label': it.get('label', ''),
                'desc': it.get('desc', ''),
                'index': it.get('index', i + 1),
            })

    if not norm:
        return

    # 每条的高度
    available_h = H - y_top - 1.0
    item_h = min(0.95, available_h / max(len(norm), 1))

    y = y_top + sp.stack_md
    for item in norm:
        # 序号（圆点 + 数字 或 单点）
        if numbered:
            dot_d = 0.4
            dot_left = sp.margin_x
            add_oval(slide, pack,
                     dot_left, y + 0.05,
                     dot_d, dot_d,
                     fill_key='accent')
            add_text(slide, pack, f'{item["index"]:02d}',
                     left=dot_left, top=y + 0.05,
                     width=dot_d, height=dot_d,
                     font_size=t.caption + 2, weight='bold',
                     color_key='bg',
                     align='center',
                     valign='middle')
            label_left = dot_left + dot_d + 0.25
        else:
            # 小实心点
            add_oval(slide, pack,
                     sp.margin_x + 0.05, y + 0.2,
                     0.12, 0.12,
                     fill_key='accent')
            label_left = sp.margin_x + 0.4

        # 标题 + 描述
        label = item['label']
        desc = item['desc']
        label_w = W - label_left - sp.margin_x
        add_text(slide, pack, label,
                 left=label_left, top=y,
                 width=label_w, height=0.45,
                 font_size=t.card_title, weight=t.card_weight,
                 color_key='text_primary',
                 align='left',
                 tracking=t.page_tracking)
        if desc:
            add_text(slide, pack, desc,
                     left=label_left, top=y + 0.45,
                     width=label_w, height=item_h - 0.45,
                     font=t.body_font, font_size=t.body,
                     color_key='text_secondary',
                     align='left',
                     leading=t.body_leading)

        y += item_h + sp.gutter

    # 页脚
    page_no = data.get('page', 0)
    company = data.get('company', '')
    if company:
        add_page_footer(slide, pack, company, page_no)
