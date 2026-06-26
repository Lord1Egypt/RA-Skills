#!/usr/bin/env python3
"""
Stage 1: 生成封面图片
输入：标题、副标题、集号
输出：封面 PNG

封面布局：
- 左侧：主标题（居中）
- 右侧：琪琪角色图
- 底部：品牌名
- 顶部：副标题 + 集号
"""
import argparse
import os
import random
from PIL import Image, ImageDraw, ImageFont


def find_font(size):
    """查找可用的中文字体"""
    for fp in ['/usr/share/fonts/opentype/noto/NotoSansCJK-Medium.ttc',
               '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
               '/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc']:
        if os.path.exists(fp):
            return ImageFont.truetype(fp, size)
    return ImageFont.load_default()


def create_star_bg(width, height, bg_color="#1a1a3e"):
    """创建星空背景"""
    bg = tuple(int(bg_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
    img = Image.new('RGB', (width, height), bg)
    random.seed(42)
    for _ in range(300):
        x, y = random.randint(0, width-1), random.randint(0, height-1)
        b = random.randint(160, 255)
        r = random.choice([1, 1, 2])
        for dx in range(-r, r+1):
            for dy in range(-r, r+1):
                if dx*dx+dy*dy <= r*r and 0 <= x+dx < width and 0 <= y+dy < height:
                    img.putpixel((x+dx, y+dy), (b, b, min(255, b+20)))
    return img


def add_qiqi(img, qiqi_path, width, height):
    """将琪琪角色图合成到封面右侧"""
    if not qiqi_path or not os.path.exists(qiqi_path):
        print(f"  ⚠️ 琪琪角色图不存在: {qiqi_path}，跳过")
        return img
    
    qiqi = Image.open(qiqi_path).convert('RGBA')
    
    # 计算琪琪位置：右侧，底部对齐，高度占封面 85%
    target_h = int(height * 0.85)
    ratio = target_h / qiqi.height
    target_w = int(qiqi.width * ratio)
    qiqi = qiqi.resize((target_w, target_h), Image.LANCZOS)
    
    # 位置：右侧，底部距底边 40px
    x = width - target_w - 40
    y = height - target_h - 40
    
    # 合成
    img_rgba = img.convert('RGBA')
    img_rgba.paste(qiqi, (x, y), qiqi)
    return img_rgba.convert('RGB')


def main():
    p = argparse.ArgumentParser(description="Stage 1: 生成封面")
    p.add_argument("--output", required=True, help="输出封面 PNG 路径")
    p.add_argument("--title", required=True, help="主标题")
    p.add_argument("--subtitle", default="琪琪遇见小王子", help="副标题/系列名")
    p.add_argument("--episode-id", default="S02E01", help="集号")
    p.add_argument("--brand", default="琪琪的魔法故事屋", help="品牌名")
    p.add_argument("--width", type=int, default=1920)
    p.add_argument("--height", type=int, default=1080)
    p.add_argument("--bg-color", default="#1a1a3e", help="背景色")
    p.add_argument("--qiqi", default=None, help="琪琪角色图路径（PNG，白底透明）")
    args = p.parse_args()

    # 1. 创建星空背景
    img = create_star_bg(args.width, args.height, args.bg_color)
    draw = ImageDraw.Draw(img)

    # 2. 如果有琪琪角色图，先合成琪琪（在文字之前，让文字在琪琪上方）
    qiqi_path = args.qiqi or os.path.expanduser("~/.openclaw/workspace/characters/qiqi_default.png")
    if args.qiqi or os.path.exists(os.path.expanduser("~/.openclaw/workspace/characters/qiqi_default.png")):
        img = add_qiqi(img, qiqi_path, args.width, args.height)
        draw = ImageDraw.Draw(img)  # 重新获取 draw 对象

    # 3. 加载字体
    font_l = find_font(72)
    font_m = find_font(44)
    font_s = find_font(32)
    font_xs = find_font(24)

    # 4. 绘制文字
    # 顶部：副标题
    draw.text((args.width//2, 80), f"★ {args.subtitle} ★",
              fill=(255, 215, 100), font=font_m, anchor="mt")
    # 顶部：集号
    draw.text((args.width//2, 140), args.episode_id,
              fill=(180, 180, 220), font=font_s, anchor="mt")
    
    # 中间：主标题（如果右侧有琪琪，文字稍微左移）
    title_x = args.width // 2 - (args.width // 6) if args.qiqi or os.path.exists(os.path.expanduser("~/.openclaw/workspace/characters/qiqi_default.png")) else args.width // 2
    draw.text((title_x, args.height//2), args.title,
              fill=(255, 255, 255), font=font_l, anchor="mm")
    
    # 底部：品牌名
    draw.text((args.width//2, args.height - 50), args.brand,
              fill=(150, 150, 200), font=font_s, anchor="mb")

    os.makedirs(os.path.dirname(args.output) or '.', exist_ok=True)
    img.save(args.output)
    print(f"✅ 封面: {args.output}")


if __name__ == "__main__":
    main()
