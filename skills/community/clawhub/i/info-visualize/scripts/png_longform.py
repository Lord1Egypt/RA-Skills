#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
png_longform.py  —  通用深色主题 PNG 长图渲染器
info-visualize skill 核心脚本

依赖: pip install Pillow

用法（命令行）:
    python png_longform.py --input report.json --output report.png

用法（Python 导入）:
    from png_longform import LongformRenderer
    r = LongformRenderer(config)
    r.render(sections, output_path)

report.json 格式:
    {
      "title": "报告标题",
      "subtitle": "副标题 / 报告时间",
      "status_tag": {"text": "CRITICAL", "level": "critical"},  // normal/warning/critical
      "kpis": [{"label": "指标名", "value": "显示值"}, ...],    // 最多 3 个
      "sections": [
        {
          "type": "text",
          "title": "章节标题",
          "content": "正文内容，支持\\n换行"
        },
        {
          "type": "table",
          "title": "表格标题",
          "headers": ["列1", "列2", "列3"],
          "rows": [["值1", "值2", "值3"], ...]
        },
        {
          "type": "bar",
          "title": "条形图标题",
          "items": [{"label": "标签", "value": 数字, "color": "#FF5533"}, ...],
          "max_value": 可选最大值,
          "value_suffix": "%"
        },
        {
          "type": "cards",
          "title": "卡片组标题",
          "items": [{"title": "卡片标题", "content": "内容", "level": "normal/warning/critical"}, ...]
        },
        {
          "type": "timeline",
          "title": "时间线标题",
          "events": [{"date": "日期", "text": "事件描述"}, ...]
        }
      ],
      "footer": "页脚说明"
    }
"""

import json
import textwrap
import argparse
import os
import shutil
from pathlib import Path
from datetime import datetime

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("ERROR: 请先安装 Pillow: pip install Pillow")
    raise

# ─── 配色方案 ───────────────────────────────────────────────────────────
W         = 900
PAD       = 52
BG        = (14, 22, 36)
BG2       = (22, 35, 54)
BG3       = (18, 28, 44)
ACCENT    = (46, 196, 182)
ACCENT2   = (255, 200, 60)
RED       = (230, 80, 80)
GREEN     = (60, 200, 120)
ORANGE    = (255, 140, 40)
WHITE     = (235, 242, 252)
GRAY      = (150, 168, 190)
DIVIDER   = (38, 58, 82)
HEADER_BG = (8, 18, 30)
TABLE_HDR = (20, 40, 64)

LEVEL_COLORS = {
    "normal":   GREEN,
    "warning":  ORANGE,
    "critical": RED,
    "info":     ACCENT,
}

FONT_DIR = "C:/Windows/Fonts"

def load_font(name, size):
    for p in [
        os.path.join(FONT_DIR, name),
        os.path.join(FONT_DIR, "msyhbd.ttc"),
        os.path.join(FONT_DIR, "msyh.ttc"),
        os.path.join(FONT_DIR, "simhei.ttf"),
        os.path.join(FONT_DIR, "simsun.ttc"),
    ]:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue
    return ImageFont.load_default()

F_TITLE  = load_font("msyhbd.ttc", 28)
F_H1     = load_font("msyhbd.ttc", 18)
F_H2     = load_font("msyhbd.ttc", 15)
F_BODY   = load_font("msyh.ttc",   13)
F_SMALL  = load_font("msyh.ttc",   11)
F_KPI    = load_font("msyhbd.ttc", 24)
F_TAG    = load_font("msyhbd.ttc", 12)


class LongformRenderer:
    """PNG 长图渲染器"""

    def __init__(self, width=900):
        self.W = width
        self.elements = []   # list of (height, draw_fn)
        self.total_h = 0

    def _text_height(self, text: str, font, max_width: int) -> int:
        """估算多行文字高度"""
        dummy = ImageDraw.Draw(Image.new("RGB", (1, 1)))
        bbox = dummy.textbbox((0, 0), "汉字Ag", font=font)
        line_h = bbox[3] - bbox[1] + 4
        # 按字符宽度估算换行
        char_w = (bbox[2] - bbox[0]) / 4
        chars_per_line = max(1, int(max_width / max(char_w, 1)))
        lines = 0
        for para in text.split("\n"):
            if not para:
                lines += 1
            else:
                lines += math.ceil(len(para) / chars_per_line)
        return lines * line_h

    def add_header(self, title: str, subtitle: str = "", status_tag: dict = None, kpis: list = None):
        HEADER_H = 160 if kpis else 100
        elems = (title, subtitle, status_tag, kpis, HEADER_H)

        def draw(draw_obj, img, y0):
            # 背景
            draw_obj.rectangle([0, y0, self.W, y0 + HEADER_H], fill=HEADER_BG)
            draw_obj.rectangle([0, y0, self.W, y0 + 3], fill=ACCENT)

            # 标题
            title_w = draw_obj.textbbox((0, 0), title, font=F_TITLE)[2]
            draw_obj.text(((self.W - title_w) // 2, y0 + 18), title, font=F_TITLE, fill=ACCENT)

            # 副标题
            if subtitle:
                sub_w = draw_obj.textbbox((0, 0), subtitle, font=F_BODY)[2]
                draw_obj.text(((self.W - sub_w) // 2, y0 + 58), subtitle, font=F_BODY, fill=GRAY)

            # 状态标签
            if status_tag:
                lv = status_tag.get("level", "normal")
                color = LEVEL_COLORS.get(lv, ACCENT)
                tag_text = status_tag.get("text", lv.upper())
                tag_w = draw_obj.textbbox((0, 0), tag_text, font=F_TAG)[2] + 24
                tx = self.W - 30 - tag_w
                ty = y0 + 20
                draw_obj.rounded_rectangle([tx, ty, tx + tag_w, ty + 26], radius=5, fill=(*color, 40), outline=color)
                draw_obj.text((tx + 12, ty + 5), tag_text, font=F_TAG, fill=color)

            # KPI 卡片
            if kpis:
                kpi_list = kpis[:3]
                n = len(kpi_list)
                card_w = (self.W - PAD * 2 - 10 * (n - 1)) // n
                for ki, kpi in enumerate(kpi_list):
                    cx = PAD + ki * (card_w + 10)
                    cy = y0 + 85
                    draw_obj.rounded_rectangle([cx, cy, cx + card_w, cy + 60], radius=8,
                                              fill=(46, 196, 182, 20), outline=ACCENT)
                    val_str = str(kpi.get("value", ""))
                    val_w = draw_obj.textbbox((0, 0), val_str, font=F_KPI)[2]
                    draw_obj.text((cx + (card_w - val_w) // 2, cy + 8), val_str, font=F_KPI, fill=ACCENT2)
                    lbl_str = str(kpi.get("label", ""))
                    lbl_w = draw_obj.textbbox((0, 0), lbl_str, font=F_SMALL)[2]
                    draw_obj.text((cx + (card_w - lbl_w) // 2, cy + 38), lbl_str, font=F_SMALL, fill=GRAY)

        self.elements.append((HEADER_H, draw))
        self.total_h += HEADER_H

    def add_section_header(self, title: str, index: int = None):
        H = 48

        def draw(draw_obj, img, y0):
            draw_obj.rectangle([0, y0, self.W, y0 + H], fill=BG2)
            num = f"{index:02d}" if index is not None else ""
            if num:
                draw_obj.ellipse([PAD, y0 + 10, PAD + 26, y0 + 36], fill=ACCENT)
                num_w = draw_obj.textbbox((0, 0), num, font=F_TAG)[2]
                draw_obj.text((PAD + 13 - num_w // 2, y0 + 14), num, font=F_TAG, fill=BG)
                tx = PAD + 36
            else:
                draw_obj.rectangle([PAD, y0 + 18, PAD + 4, y0 + 30], fill=ACCENT)
                tx = PAD + 14
            draw_obj.text((tx, y0 + 14), title, font=F_H1, fill=WHITE)
            draw_obj.line([0, y0 + H - 1, self.W, y0 + H - 1], fill=DIVIDER, width=1)

        self.elements.append((H, draw))
        self.total_h += H

    def add_text_block(self, content: str, indent: int = PAD):
        import math
        MAX_W = self.W - indent * 2
        dummy = ImageDraw.Draw(Image.new("RGB", (1, 1)))
        bbox = dummy.textbbox((0, 0), "汉字Ag", font=F_BODY)
        line_h = bbox[3] - bbox[1] + 6
        char_w = (bbox[2] - bbox[0]) / 4
        cpl = max(1, int(MAX_W / max(char_w, 1)))

        lines = []
        for para in content.split("\n"):
            if not para.strip():
                lines.append("")
            else:
                # 简单按字符数分行（中英混合）
                while len(para) > cpl:
                    lines.append(para[:cpl])
                    para = para[cpl:]
                lines.append(para)

        H = len(lines) * line_h + 24
        captured_lines = lines
        captured_line_h = line_h

        def draw(draw_obj, img, y0):
            draw_obj.rectangle([0, y0, self.W, y0 + H], fill=BG)
            for li, line in enumerate(captured_lines):
                draw_obj.text((indent, y0 + 12 + li * captured_line_h), line, font=F_BODY, fill=WHITE)

        self.elements.append((H, draw))
        self.total_h += H

    def add_table(self, headers: list, rows: list):
        n_cols = len(headers)
        col_w = (self.W - PAD * 2) // n_cols
        ROW_H = 30
        H = ROW_H * (len(rows) + 1) + 20

        def draw(draw_obj, img, y0):
            draw_obj.rectangle([0, y0, self.W, y0 + H], fill=BG3)
            # 表头
            draw_obj.rectangle([PAD, y0 + 10, self.W - PAD, y0 + 10 + ROW_H], fill=TABLE_HDR)
            for ci, h in enumerate(headers):
                cx = PAD + ci * col_w
                draw_obj.text((cx + 8, y0 + 16), str(h), font=F_H2, fill=ACCENT)
            # 数据行
            for ri, row in enumerate(rows):
                ry = y0 + 10 + (ri + 1) * ROW_H
                bg = BG2 if ri % 2 == 0 else BG3
                draw_obj.rectangle([PAD, ry, self.W - PAD, ry + ROW_H], fill=bg)
                for ci, cell in enumerate(row[:n_cols]):
                    cx = PAD + ci * col_w
                    draw_obj.text((cx + 8, ry + 8), str(cell), font=F_BODY, fill=WHITE)
                # 底部线
                draw_obj.line([PAD, ry + ROW_H - 1, self.W - PAD, ry + ROW_H - 1],
                              fill=DIVIDER, width=1)

        self.elements.append((H, draw))
        self.total_h += H

    def add_bar_chart(self, items: list, max_value: float = None, value_suffix: str = ""):
        BAR_LEFT = PAD + 130
        BAR_RIGHT = self.W - 120
        ROW_H = 28
        H = ROW_H * len(items) + 20
        max_v = max_value or max((it.get("value", 0) for it in items), default=100)
        max_v = max(max_v, 0.001)

        bar_colors = [
            (255, 34, 68), (255, 85, 51), (255, 136, 0),
            (255, 170, 0), (221, 204, 0), (46, 196, 182),
        ]

        def draw(draw_obj, img, y0):
            draw_obj.rectangle([0, y0, self.W, y0 + H], fill=BG)
            for i, item in enumerate(items):
                iy = y0 + 10 + i * ROW_H
                val = float(item.get("value", 0))
                label = str(item.get("label", ""))
                color_hex = item.get("color")
                if color_hex and color_hex.startswith("#"):
                    h = color_hex.lstrip("#")
                    color = tuple(int(h[j:j+2], 16) for j in (0, 2, 4))
                else:
                    color = bar_colors[i % len(bar_colors)]

                bar_w = max(2, int((val / max_v) * (BAR_RIGHT - BAR_LEFT)))
                bg = BG2 if i % 2 == 0 else BG
                draw_obj.rectangle([0, iy, self.W, iy + ROW_H - 2], fill=bg)
                # 标签
                draw_obj.text((PAD, iy + 6), label, font=F_BODY, fill=GRAY)
                # 条形
                draw_obj.rounded_rectangle([BAR_LEFT, iy + 4, BAR_LEFT + bar_w, iy + ROW_H - 6],
                                          radius=3, fill=color)
                # 数值
                val_str = f"{val:+.2f}{value_suffix}" if val >= 0 else f"{val:.2f}{value_suffix}"
                draw_obj.text((BAR_RIGHT + 8, iy + 6), val_str, font=F_BODY, fill=color)

        self.elements.append((H, draw))
        self.total_h += H

    def add_cards(self, items: list):
        CARD_H = 80
        CARD_W = (self.W - PAD * 2 - 20) // 2
        n_rows = (len(items) + 1) // 2
        H = n_rows * (CARD_H + 10) + 20

        def draw(draw_obj, img, y0):
            draw_obj.rectangle([0, y0, self.W, y0 + H], fill=BG)
            for ci, item in enumerate(items):
                row = ci // 2
                col = ci % 2
                cx = PAD + col * (CARD_W + 20)
                cy = y0 + 10 + row * (CARD_H + 10)
                lv = item.get("level", "normal")
                color = LEVEL_COLORS.get(lv, ACCENT)
                # 卡片背景
                draw_obj.rounded_rectangle([cx, cy, cx + CARD_W, cy + CARD_H],
                                          radius=8, fill=BG2, outline=(*color, 80))
                # 左侧色条
                draw_obj.rounded_rectangle([cx, cy, cx + 5, cy + CARD_H], radius=3, fill=color)
                # 标题
                draw_obj.text((cx + 14, cy + 10), str(item.get("title", "")), font=F_H2, fill=color)
                # 内容
                content = str(item.get("content", ""))
                draw_obj.text((cx + 14, cy + 38), content[:60], font=F_BODY, fill=WHITE)

        self.elements.append((H, draw))
        self.total_h += H

    def add_timeline(self, events: list):
        EVT_H = 40
        H = EVT_H * len(events) + 20

        def draw(draw_obj, img, y0):
            draw_obj.rectangle([0, y0, self.W, y0 + H], fill=BG)
            LINE_X = PAD + 80
            draw_obj.line([LINE_X, y0 + 10, LINE_X, y0 + H - 10], fill=DIVIDER, width=2)
            for i, evt in enumerate(events):
                iy = y0 + 10 + i * EVT_H
                # 节点圆点
                draw_obj.ellipse([LINE_X - 5, iy + 13, LINE_X + 5, iy + 23], fill=ACCENT)
                # 日期
                draw_obj.text((PAD, iy + 11), str(evt.get("date", "")), font=F_SMALL, fill=GRAY)
                # 事件文本
                draw_obj.text((LINE_X + 14, iy + 11), str(evt.get("text", "")), font=F_BODY, fill=WHITE)

        self.elements.append((H, draw))
        self.total_h += H

    def add_divider(self, height: int = 16):
        def draw(draw_obj, img, y0):
            draw_obj.rectangle([0, y0, self.W, y0 + height], fill=BG)
            draw_obj.line([PAD, y0 + height // 2, self.W - PAD, y0 + height // 2],
                          fill=DIVIDER, width=1)
        self.elements.append((height, draw))
        self.total_h += height

    def add_footer(self, text: str, next_update: str = ""):
        H = 60

        def draw(draw_obj, img, y0):
            draw_obj.rectangle([0, y0, self.W, y0 + H], fill=HEADER_BG)
            draw_obj.line([0, y0, self.W, y0], fill=DIVIDER, width=1)
            now = datetime.now().strftime("%Y-%m-%d %H:%M")
            main_text = f"报告时间: {now}  |  {text}"
            tw = draw_obj.textbbox((0, 0), main_text, font=F_SMALL)[2]
            draw_obj.text(((self.W - tw) // 2, y0 + 12), main_text, font=F_SMALL, fill=GRAY)
            if next_update:
                nt_w = draw_obj.textbbox((0, 0), next_update, font=F_SMALL)[2]
                draw_obj.text(((self.W - nt_w) // 2, y0 + 34), next_update, font=F_SMALL, fill=DIVIDER)
            # WorkBuddy 水印
            wm = "Powered by WorkBuddy"
            wm_w = draw_obj.textbbox((0, 0), wm, font=F_SMALL)[2]
            draw_obj.text((self.W - wm_w - PAD, y0 + 22), wm, font=F_SMALL, fill=(38, 58, 82))

        self.elements.append((H, draw))
        self.total_h += H

    def render(self, output_path: str) -> str:
        """渲染所有元素到 PNG 文件，返回输出路径。"""
        img = Image.new("RGB", (self.W, self.total_h), color=BG)
        draw_obj = ImageDraw.Draw(img, "RGBA")

        y = 0
        for height, draw_fn in self.elements:
            draw_fn(draw_obj, img, y)
            y += height

        # 裁剪到实际内容高度
        img = img.crop((0, 0, self.W, self.total_h))
        img.save(output_path, "PNG")
        print(f"已生成 PNG: {Path(output_path).resolve()}  ({self.W}x{self.total_h}px)")
        return output_path


import math


def render_from_json(data: dict, output_path: str) -> str:
    """从结构化 JSON 数据渲染长图。"""
    r = LongformRenderer()

    r.add_header(
        title=data.get("title", "报告"),
        subtitle=data.get("subtitle", ""),
        status_tag=data.get("status_tag"),
        kpis=data.get("kpis"),
    )

    for idx, sec in enumerate(data.get("sections", []), 1):
        sec_type = sec.get("type", "text")
        sec_title = sec.get("title", "")

        if sec_title:
            r.add_section_header(sec_title, index=idx)

        if sec_type == "text":
            r.add_text_block(sec.get("content", ""))
        elif sec_type == "table":
            r.add_table(sec.get("headers", []), sec.get("rows", []))
        elif sec_type == "bar":
            r.add_bar_chart(
                sec.get("items", []),
                max_value=sec.get("max_value"),
                value_suffix=sec.get("value_suffix", ""),
            )
        elif sec_type == "cards":
            r.add_cards(sec.get("items", []))
        elif sec_type == "timeline":
            r.add_timeline(sec.get("events", []))

        r.add_divider()

    r.add_footer(
        text=data.get("footer", ""),
        next_update=data.get("next_update", ""),
    )

    return r.render(output_path)


def main():
    parser = argparse.ArgumentParser(description="生成深色主题 PNG 长图报告")
    parser.add_argument("--input", "-i", required=True, help="输入 JSON 文件路径")
    parser.add_argument("--output", "-o", default="report.png", help="输出 PNG 文件路径")
    parser.add_argument("--archive", help="同时复制到归档目录（可选）")
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        data = json.load(f)

    out = render_from_json(data, args.output)

    if args.archive:
        archive_dir = Path(args.archive)
        archive_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(out, archive_dir / Path(out).name)
        print(f"已归档到: {archive_dir / Path(out).name}")


if __name__ == "__main__":
    main()
