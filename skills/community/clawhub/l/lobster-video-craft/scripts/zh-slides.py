#!/usr/bin/env python3
"""通用中文字体幻灯片生成器 - 给vido-craft-pro技能用
任何视频制作直接调用这个，不用再装字体
"""

from PIL import Image, ImageDraw, ImageFont
import os, sys

# 中文字体路径（兼容多个路径）
FONT_PATHS = [
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
    "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
]

FT_BOLD = None
FT_REG = None
FT_CODE = None
FT_BIG = None

for p in FONT_PATHS:
    if os.path.exists(p):
        try:
            FT_BOLD = ImageFont.truetype(p, 60)
            FT_BIG = ImageFont.truetype(p, 76)
            FT_REG = ImageFont.truetype(p, 32)
            FT_CODE = ImageFont.truetype(p, 24)
            break
        except:
            continue

def make_slides(out_dir, slides_config):
    """通用幻灯片生成器
    slides_config: [(类型, 标题, 内容), ...]
    类型: 'title', 'bullet', 'code'
    """
    W, H = 1920, 1080
    BG = (15, 15, 30)
    ACCENT = (100, 200, 255)
    WHITE = (230, 230, 240)
    GRAY = (100, 100, 120)
    
    os.makedirs(out_dir, exist_ok=True)
    
    for idx, (ctype, title, content) in enumerate(slides_config):
        img = Image.new('RGB', (W, H), BG)
        d = ImageDraw.Draw(img)
        
        if ctype == 'title':
            d.text((W//2, H//2-60), title, fill=WHITE, font=FT_BIG, anchor="mm")
            d.text((W//2, H//2+50), content, fill=GRAY, font=FT_REG, anchor="mm")
        
        elif ctype == 'bullet':
            d.text((80, 40), title, fill=ACCENT, font=FT_BOLD)
            d.line([(80, 95), (400, 95)], fill=ACCENT, width=2)
            for i, line in enumerate(content.split('\n')):
                d.text((100, 150 + i*45), line, fill=WHITE, font=FT_REG)
        
        elif ctype == 'code':
            d.text((80, 40), title, fill=ACCENT, font=FT_BOLD)
            d.line([(80, 95), (400, 95)], fill=ACCENT, width=2)
            lines = content.split('\n')
            h = len(lines) * 30 + 30
            d.rectangle([80, 140, 1840, 140+h], fill=(20, 25, 45), outline=(40, 50, 80))
            for i, line in enumerate(lines):
                c = ACCENT if line.strip().startswith('#') else WHITE
                d.text((100, 150 + i*30), line, fill=c, font=FT_CODE)
        
        path = os.path.join(out_dir, f"slide_{idx:02d}.png")
        img.save(path)
    
    return len(slides_config)


if __name__ == '__main__':
    # 测试
    test_dir = "/tmp/test-slides-zh"
    slides = [
        ('title', '测试', '中文幻灯片生成器'),
        ('bullet', '功能', '支持中文字体\n自动检测字体路径\n自动降级'),
    ]
    n = make_slides(test_dir, slides)
    print(f"✅ 生成{n}张幻灯片")
