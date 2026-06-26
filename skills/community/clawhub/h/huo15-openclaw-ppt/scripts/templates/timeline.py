"""timeline — 时间线页。

横向时间线，若干事件节点。

data:
  title:   str
  en_sub:  str (optional)
  events:  list[dict]   每个 dict:
             time:  str   ("2024", "Q1", "Jan 2025")
             label: str
             desc:  str (optional)
"""

from .helpers import (
    new_slide, add_text, add_oval, add_hline, add_rect,
    add_page_header, add_page_footer,
)


def build(prs, pack, data: dict) -> None:
    slide = new_slide(prs, pack)
    W, H = pack.canvas.width, pack.canvas.height
    t = pack.typography
    sp = pack.spacing

    title = data.get('title', '')
    en_sub = data.get('en_sub', '')
    y_top = add_page_header(slide, pack, title, en_sub)

    events = data.get('events', [])
    if not events:
        return

    n = len(events)

    # 主线 Y 位置（竖向居中）
    mid_y = y_top + (H - y_top - 1.0) * 0.5

    # 水平轴线
    axis_left = sp.margin_x
    axis_right = W - sp.margin_x
    axis_w = axis_right - axis_left
    add_hline(slide, pack, axis_left, mid_y, axis_w,
              color_key='border', thickness=0.015)

    # 每个节点的位置
    if n == 1:
        xs = [axis_left + axis_w * 0.5]
    else:
        xs = [axis_left + axis_w * (i / (n - 1)) for i in range(n)]

    dot_d = 0.3
    for i, ev in enumerate(events):
        cx = xs[i]
        time_s = ev.get('time', '')
        label = ev.get('label', '')
        desc = ev.get('desc', '')

        # 圆点（实心 accent）
        add_oval(slide, pack,
                 cx - dot_d / 2, mid_y - dot_d / 2,
                 dot_d, dot_d,
                 fill_key='accent')

        # 交替上/下
        above = (i % 2 == 0)
        box_w = min(axis_w / max(n, 1) - 0.2, 2.6)

        if above:
            # 时间在上，label + desc 在再上方
            time_top = mid_y - 0.55
            label_top = mid_y - 1.2
            desc_top = mid_y - 1.8
        else:
            time_top = mid_y + 0.25
            label_top = mid_y + 0.7
            desc_top = mid_y + 1.3

        # 时间
        add_text(slide, pack, time_s,
                 left=cx - box_w / 2, top=time_top,
                 width=box_w, height=0.3,
                 font=t.body_font, font_size=t.caption + 2, weight='semibold',
                 color_key='accent',
                 align='center',
                 tracking=0.05)

        # label
        add_text(slide, pack, label,
                 left=cx - box_w / 2, top=label_top,
                 width=box_w, height=0.5,
                 font_size=t.card_title - 2, weight=t.card_weight,
                 color_key='text_primary',
                 align='center',
                 leading=1.2)

        # 描述
        if desc:
            add_text(slide, pack, desc,
                     left=cx - box_w / 2, top=desc_top,
                     width=box_w, height=0.6,
                     font=t.body_font, font_size=t.caption + 1,
                     color_key='text_tertiary',
                     align='center',
                     leading=t.body_leading)

    # 页脚
    page_no = data.get('page', 0)
    company = data.get('company', '')
    if company:
        add_page_footer(slide, pack, company, page_no)
