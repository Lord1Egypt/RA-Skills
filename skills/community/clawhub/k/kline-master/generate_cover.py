#!/usr/bin/env python3
"""
生成 K线大师 技能包封面图
"""

from PIL import Image, ImageDraw, ImageFont
import os

# 创建封面图 (1200x630 - ClawHub 推荐尺寸)
width, height = 1200, 630
img = Image.new('RGB', (width, height), color='#1a1a2e')

# 创建绘图对象
draw = ImageDraw.Draw(img)

# 背景渐变效果（简化版 - 使用纯色）
# 主色调：深蓝紫色
draw.rectangle([0, 0, width, height], fill='#1a1a2e')

# 装饰：K线图案（简化版）
# 绘制几根K线作为背景装饰
def draw_candle(draw, x, y, width, height, is_green=True):
    """绘制单根K线"""
    color = '#00d4aa' if is_green else '#ff6b6b'
    # 实体
    draw.rectangle([x, y, x + width, y + height], fill=color)
    # 影线（上）
    draw.line([x + width//2, y - 15, x + width//2, y], fill=color, width=2)
    # 影线（下）
    draw.line([x + width//2, y + height, x + width//2, y + height + 15], fill=color, width=2)

# 绘制背景K线（半透明效果用浅色模拟）
candle_positions = [
    (50, 200, 40, 100, True),
    (120, 180, 40, 120, True),
    (190, 250, 40, 80, False),
    (260, 200, 40, 130, True),
    (330, 170, 40, 140, True),
    (400, 220, 40, 100, False),
    (900, 200, 40, 110, True),
    (970, 190, 40, 120, True),
    (1040, 230, 40, 90, False),
    (1110, 180, 40, 130, True),
]

for pos in candle_positions:
    draw_candle(draw, pos[0], pos[1], pos[2], pos[3], pos[4])

# 主标题（使用 Arial 字体）
title_font = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', 72)
subtitle_font = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf', 32)
price_font = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', 48)
small_font = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf', 24)

# 标题文字（英文版）
title = "Kline Master"
subtitle = "Professional Trading Skill Pack | AI-Powered"
price = "$29"
features = "50+ Patterns | MACD/RSI/BOLL | 30+ Real Cases | AI Guidance"

# 绘制标题（居中）
title_bbox = draw.textbbox((0, 0), title, font=title_font)
title_width = title_bbox[2] - title_bbox[0]
title_x = (width - title_width) // 2
draw.text((title_x, 150), title, font=title_font, fill='#00d4aa')

# 绘制副标题
subtitle_bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
subtitle_x = (width - subtitle_width) // 2
draw.text((subtitle_x, 240), subtitle, font=subtitle_font, fill='#ffffff')

# 绘制价格标签
draw.ellipse([540, 340, 660, 460], fill='#ff6b6b')
price_bbox = draw.textbbox((0, 0), price, font=price_font)
price_width = price_bbox[2] - price_bbox[0]
price_height = price_bbox[3] - price_bbox[1]
price_x = 600 - price_width // 2
price_y = 400 - price_height // 2
draw.text((price_x, price_y), price, font=price_font, fill='#ffffff')

# 绘制特性
features_bbox = draw.textbbox((0, 0), features, font=small_font)
features_width = features_bbox[2] - features_bbox[0]
features_x = (width - features_width) // 2
draw.text((features_x, 500), features, font=small_font, fill='#cccccc')

# 底部装饰线
draw.line([100, 580, 1100, 580], fill='#00d4aa', width=3)

# 保存
output_dir = '/Users/jideaiqiang/.openclaw/workspace/skills-for-sale/kline-master/'
output_path = os.path.join(output_dir, 'cover.png')
img.save(output_path, 'PNG', optimize=True)
print(f"✅ 封面图已生成: {output_path}")
print(f"📐 尺寸: {width}x{height}")
print(f"📦 大小: {os.path.getsize(output_path) / 1024:.1f} KB")
