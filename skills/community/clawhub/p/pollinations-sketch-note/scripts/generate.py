#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "requests",
#     "pillow>=10.0.0",
# ]
# ///
"""
Pollinations Sketch Note - 生成手绘风格知识卡片

Usage:
    python3 generate.py --theme "猫"
    python3 generate.py --theme "咖啡" --output "~/Pictures/coffee_note.png"
    python3 generate.py --theme "猫" --detail "自定义的详细介绍文字..."
"""

import argparse
import os
import sys
import random
import urllib.parse
import hashlib
from pathlib import Path
from datetime import datetime

try:
    import requests
except ImportError:
    print("❌ 缺少依赖：requests")
    print("请运行：pip3 install requests")
    sys.exit(1)

# 配置 - 从环境变量读取
POLLINATIONS_API_KEY = os.environ.get("POLLINATIONS_API_KEY")
TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY")

# 验证 API Key 是否存在
if not POLLINATIONS_API_KEY:
    print("❌ 错误：未找到 POLLINATIONS_API_KEY 环境变量")
    print("请配置：export POLLINATIONS_API_KEY=\"your-api-key\"")
    print("或在 ~/.zshrc 中添加后运行：source ~/.zshrc")
    sys.exit(1)

if not TAVILY_API_KEY:
    print("❌ 错误：未找到 TAVILY_API_KEY 环境变量")
    print("请配置：export TAVILY_API_KEY=\"your-api-key\"")
    print("或在 ~/.zshrc 中添加后运行：source ~/.zshrc")
    sys.exit(1)

DEFAULT_OUTPUT_DIR = Path("/Users/pengshengkai/.openclaw/media")

# 3 种风格：极简、可爱插画、赛博朋克（随机轮换）
STYLE_VARIANTS = [
    # 风格 1：极简干净背景（配色随机）
    "Clean minimalist hand-drawn background with simple organized shapes. Soft watercolor gradient in random colors (blue pink purple, or orange yellow, or green teal). Large empty center area, clean edges, minimal decorative elements. Professional infographic template, NO text, NO letters, NO symbols, NO random marks. Smooth clean background for text overlay --ar 16:9",
    
    # 风格 2：可爱插画风（龙虾 OpenClaw 风格）
    "Anthropomorphic golden retriever wearing red lobster shell hat, sitting at office desk with computer. Positioned on RIGHT side. LEFT side: chalkboard with wooden frame for text. Background: large chalkboard with pink-blue gradient. Clear chalkboard visible, school blackboard style. RIGHT character LEFT chalkboard separation. Cartoon hand-drawn style, warm watercolor, chibi cute --ar 16:9",
    
    # 风格 3：赛博朋克 AI 涂鸦广告牌（广告牌占满画面，文字区域最大化）
    "Cyberpunk city street night, massive AI graffiti billboard filling entire frame, large blank white space center for text. Billboard 80 percent of image, minimal background. Neon electric cyan toxic pink on edges, liquid digital paint borders, binary code graffiti. NO text on billboard, clean blank center --ar 16:9",
]


def search_theme(theme: str) -> str:
    """使用 Jina Reader 抓取维基百科内容"""
    try:
        import requests

        # print(f"🔍 正在搜索：{theme}")  # 静默模式

        # 1. 先尝试百度百科 + Jina Reader
        baidu_url = f"https://baike.baidu.com/item/{urllib.parse.quote(theme)}"
        jina_url = f"https://r.jina.ai/{baidu_url}"

        try:
            response = requests.get(jina_url, timeout=15)
            if response.status_code == 200:
                content = response.text
                # 清理 markdown 格式，找第一句定义
                lines = content.split("\n")
                clean_lines = []
                for line in lines:
                    line = line.strip()
                    # 跳过无关行
                    if not line:
                        continue
                    if "百度百科" in line:
                        continue
                    if line.startswith("http"):
                        continue
                    if line.startswith("#"):
                        continue
                    if line.startswith("Title"):
                        continue
                    if line.startswith("URL"):
                        continue
                    if line.startswith("Markdown"):
                        continue
                    if "同义词" in line:
                        continue
                    if "跳转" in line:
                        continue
                    if len(line) < 15:
                        continue
                    # 优先找包含主题和"是/指"的定义句
                    if theme in line and ("是" in line or "指" in line):
                        clean_lines.insert(0, line)  # 放最前面
                    elif len(line) > 30:
                        clean_lines.append(line)

                # 合并内容（优先使用定义句）
                definition = ""
                if clean_lines:
                    definition = "。".join(clean_lines[:2])  # 取前 2 句

                if definition and len(definition) > 30:
                    # 过滤掉 URL 编码内容
                    import re
                    # 删除所有 http 开头的 URL
                    definition = re.sub(r'https?[a-zA-Z0-9%:/_.=??&-]+', '', definition)
                    # 删除括号内的 URL 残留
                    definition = re.sub(r'\([^)]*baike[^)]*\)', '', definition)
                    # 删除空括号
                    definition = definition.replace('()', '')
                    # 删除多余空格
                    definition = ' '.join(definition.split())

                    # print(f"✅ 百度百科找到内容")  # 静默模式
                    summary = compress_text(definition, target_length=190, theme=theme)
                    # print(f"✅ 总结 {len(summary)} 字")  # 静默模式
                    # print(f"📋 总结内容：{summary}")  # 静默模式
                    return summary
        except Exception as e:
            pass  # 静默模式

        # 2. 尝试英文维基百科 + Jina Reader
        en_wiki_url = f"https://en.wikipedia.org/wiki/{urllib.parse.quote(theme)}"
        jina_url = f"https://r.jina.ai/{en_wiki_url}"

        try:
            response = requests.get(jina_url, timeout=15)
            if response.status_code == 200:
                content = response.text
                lines = content.split("\n")
                first_para = ""
                for i, line in enumerate(lines):
                    if line.strip() and i > 2:
                        first_para += line
                        if len(first_para) > 100:
                            break

                if len(first_para) > 50:
                    # print(f"✅ 英文维基百科找到内容")  # 静默模式
                    summary = compress_text(first_para, target_length=190, theme=theme)
                    # print(f"✅ 总结 {len(summary)} 字")  # 静默模式
                    # print(f"📋 总结内容：{summary}")  # 静默模式
                    return summary
        except Exception as e:
            pass  # 静默模式

        # 3. 兜底
        # print("⚠️ 维基百科搜索失败，使用默认介绍")  # 静默模式
        return f"{theme}是一种常见的事物，具有独特的特点和用途。它在日常生活中扮演着重要角色，深受人们喜爱。"

    except Exception as e:
        print(f"⚠️ 搜索失败：{e}")
        return f"{theme}是一种常见的事物，具有独特的特点和用途。它在日常生活中扮演着重要角色，深受人们喜爱。"


def filter_text(text: str) -> str:
    """过滤文本，只保留中英文和标点"""
    # 保留：中文、英文、数字、常见标点
    # 中文范围：\u4e00-\u9fff
    # 英文：A-Za-z
    # 数字：0-9
    # 标点单独列出，避免范围问题
    allowed_chars = set('，。！？；：、""（）()【】《》-…·- ')

    filtered = []
    for char in text:
        # 中文
        if '\u4e00' <= char <= '\u9fff':
            filtered.append(char)
        # 英文
        elif 'A' <= char <= 'Z' or 'a' <= char <= 'z':
            filtered.append(char)
        # 数字
        elif '0' <= char <= '9':
            filtered.append(char)
        # 允许的标点
        elif char in allowed_chars:
            filtered.append(char)
        # 空格
        elif char == ' ':
            filtered.append(char)

    result = ''.join(filtered)
    # 清理多余空格
    result = ' '.join(result.split())
    return result


def compress_text(text: str, target_length: int = 190, theme: str = "") -> str:
    """压缩文本到目标长度，提取关键信息"""
    # 先过滤，只保留中英文
    text = filter_text(text)

    # 简单压缩：截取 + 找句子边界
    if len(text) <= target_length:
        return text

    # 按句号分割成句子
    sentences = text.replace("!", "。").replace("?", "。").split("。")

    # 优先选择包含主题的句子
    theme_sentences = []
    other_sentences = []
    for sent in sentences:
        sent = sent.strip()
        if len(sent) < 10:  # 太短的句子跳过
            continue
        if theme and theme in sent:
            theme_sentences.append(sent)
        else:
            other_sentences.append(sent)

    # 优先使用包含主题的句子
    result_parts = theme_sentences[:5] + other_sentences[:3]
    result = "。".join(result_parts)

    if len(result) <= target_length:
        return result + "。"

    # 如果还是太长，截取
    truncated = result[:target_length]
    for punct in ["。", "！", "？", ".", "!", "?"]:
        last_pos = truncated.rfind(punct)
        if last_pos > target_length * 0.8:
            return truncated[:last_pos + 1]

    return truncated + "..."


def generate_background(theme: str, style: str, output_path: Path) -> bool:
    """生成海报风格背景图"""
    # 替换提示词中的 {theme}
    prompt = style.replace("{theme}", theme)

    encoded_prompt = urllib.parse.quote(prompt)
    url = f"https://gen.pollinations.ai/image/{encoded_prompt}"
    params = {
        "width": 804,
        "height": 440,
        "model": "flux",
        "key": POLLINATIONS_API_KEY
    }

    # print(f"🎨 正在生成背景图（风格：{style[:50]}...）")  # 静默模式
    response = requests.get(url, params=params, timeout=60)

    if response.status_code == 200:
        with open(output_path, 'wb') as f:
            f.write(response.content)
        # print(f"✅ 背景图已保存：{output_path}")  # 静默模式
        return True
    else:
        # print(f"❌ 生成失败：{response.status_code}")  # 静默模式
        return False


def add_text_to_image(image_path: Path, title: str, detail: str, output_path: Path, style: str = "") -> bool:
    """在图片上添加文字"""
    try:
        from PIL import Image, ImageDraw, ImageFont

        img = Image.open(image_path)
        img = img.convert('RGB')
        width, height = img.size

        # 先加载字体
        font_paths = [
            "/System/Library/Fonts/STHeiti Medium.ttc",
            "/System/Library/Fonts/Hiragino Sans GB.ttc",
            "/System/Library/Fonts/PingFang.ttc",
        ]
        title_font = detail_font = signature_font = None
        for font_path in font_paths:
            try:
                title_font = ImageFont.truetype(font_path, 32)
                detail_font = ImageFont.truetype(font_path, 18)
                signature_font = detail_font
                break
            except:
                continue
        if not title_font or not detail_font:
            title_font = detail_font = signature_font = ImageFont.load_default()

        # 文字区域（根据风格调整位置）
        # 风格 3（可爱插画风）：文字在左侧黑板区域，粉笔字效果
        # 风格 1/2：居中偏下
        if "golden retriever" in style or "lobster" in style:  # 风格 3
            draw = ImageDraw.Draw(img)
            
            # 左侧文字区域（占 40% 宽度，确保不挡右侧狗狗）
            text_x = int(width * 0.05)  # 左边距
            text_width = int(width * 0.40)  # 只占左侧 40%
            text_y = int(height * 0.15)  # 从上 15% 开始
            
            # 标题（粉笔字效果 - 白色带轻微模糊）
            title_y = text_y + 10
            title_x = text_x + 10
            
            # 粉笔字：白色 + 浅灰色描边模拟粉笔质感
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    draw.text((title_x + dx, title_y + dy), title,
                              fill=(180, 180, 180), font=title_font)
            draw.text((title_x, title_y), title, fill=(255, 255, 255), font=title_font)
            
            # 详情（粉笔字效果，多行）
            detail_lines = []
            max_chars_per_line = 14  # 每行更少字，适应窄区域
            for i in range(0, len(detail), max_chars_per_line):
                detail_lines.append(detail[i:i + max_chars_per_line])
            
            detail_y = title_y + 35
            line_height = 20
            for line in detail_lines:
                # 粉笔字效果
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        draw.text((title_x + dx, detail_y + dy), line,
                                  fill=(180, 180, 180), font=detail_font)
                draw.text((title_x, detail_y), line, fill=(255, 255, 255), font=detail_font)
                detail_y += line_height
            
            # 署名（左侧底部，小粉笔字）
            signature = f"sk-openclaw · {datetime.now().strftime('%m-%d %H:%M')}"
            signature_font_small = ImageFont.truetype("/System/Library/Fonts/STHeiti Medium.ttc", 8)
            signature_bbox = draw.textbbox((0, 0), signature, font=signature_font_small)
            signature_width = signature_bbox[2] - signature_bbox[0]
            signature_x = text_x + 10
            signature_y = height - 15
            draw.text((signature_x, signature_y), signature,
                      fill=(160, 160, 160), font=signature_font_small)
            
            img.save(output_path, 'PNG')
            return True
        else:
            # 风格 1/2：居中偏上（微调位置 + 缩小宽度）
            text_box_width = int(width * 0.68)  # 缩小约 3 个字宽度（80% → 68%）
            text_box_height = int(height * 0.50)
            text_box_x = (width - text_box_width) // 2
            text_box_y = int(height * 0.29)  # 从上 29% 开始
        
        draw = ImageDraw.Draw(img)

        # 不加白色背板，直接画文字（带白色描边）

        # 标题（加白色描边，让文字更清晰）
        title_y = text_box_y + 10
        title_text = title
        title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
        title_width = title_bbox[2] - title_bbox[0]
        title_x = text_box_x + (text_box_width - title_width) // 2
        
        # 白色描边
        for dx in [-2, -1, 0, 1, 2]:
            for dy in [-2, -1, 0, 1, 2]:
                if dx != 0 or dy != 0:
                    draw.text((title_x + dx, title_y + dy), title_text,
                              fill=(255, 255, 255), font=title_font)
        # 黑色文字
        draw.text((title_x, title_y), title_text,
                  fill=(30, 30, 30), font=title_font)

        # 详情（自动换行，加白色描边）
        detail_lines = []
        max_chars_per_line = 24
        for i in range(0, len(detail), max_chars_per_line):
            detail_lines.append(detail[i:i + max_chars_per_line])

        detail_y = title_y + 40
        line_height = 26
        for line in detail_lines:
            line_bbox = draw.textbbox((0, 0), line, font=detail_font)
            line_width = line_bbox[2] - line_bbox[0]
            line_x = text_box_x + (text_box_width - line_width) // 2
            
            # 白色描边
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx != 0 or dy != 0:
                        draw.text((line_x + dx, detail_y + dy), line,
                                  fill=(255, 255, 255), font=detail_font)
            # 黑色文字
            draw.text((line_x, detail_y), line,
                      fill=(30, 30, 30), font=detail_font)
            detail_y += line_height

        # 署名（最右下角，贴边）
        signature = f"sk-openclaw · {datetime.now().strftime('%m-%d %H:%M')}"
        signature_font_small = ImageFont.truetype("/System/Library/Fonts/STHeiti Medium.ttc", 10)  # 更小字体
        signature_y = text_box_y + text_box_height - 12  # 更贴底
        signature_bbox = draw.textbbox((0, 0), signature, font=signature_font_small)
        signature_width = signature_bbox[2] - signature_bbox[0]
        signature_x = text_box_x + text_box_width - signature_width - 3  # 更贴右
        draw.text((signature_x, signature_y), signature,
                  fill=(100, 100, 100), font=signature_font_small)

        img.save(output_path, 'PNG')
        # print(f"✅ 文字合成完成：{output_path}")  # 静默模式
        return True

    except Exception as e:
        print(f"ERROR in add_text_to_image: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    parser = argparse.ArgumentParser(description="生成手绘风格知识卡片")
    parser.add_argument("--theme", "-t", required=True, help="主题（例如：猫、咖啡）")
    parser.add_argument("--output", "-o", help="输出路径（可选）")
    parser.add_argument("--detail", "-d", help="自定义详情文字（不提供则自动搜索）")
    parser.add_argument("--style", "-s", type=int, choices=[1,2,3], help="指定风格（1=极简，2=信息图，3=可爱插画）")

    args = parser.parse_args()

    # 输出路径
    if args.output:
        output_path = Path(args.output).expanduser()
    else:
        DEFAULT_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        output_path = DEFAULT_OUTPUT_DIR / f"sketch_{args.theme}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"

    # 获取详情文字
    if args.detail:
        detail = args.detail
        # print(f"📝 使用自定义详情：{len(detail)} 字")  # 静默模式
    else:
        detail = search_theme(args.theme)

    # 选择风格（指定或随机）
    if args.style:
        style = STYLE_VARIANTS[args.style - 1]
        print(f"🎨 使用风格 {args.style}: {list(['极简干净背景', '手绘信息图', '可爱插画风'])[args.style-1]}")
    else:
        style = random.choice(STYLE_VARIANTS)
    # print(f"🎭 使用风格：{style[:50]}...")  # 静默模式

    # 生成背景图
    bg_path = output_path.parent / f"bg_{output_path.name}"
    if not generate_background(args.theme, style, bg_path):
        print(f"ERROR: Failed to generate background. Style: {style[:100]}...")
        sys.exit(1)

    # 添加文字
    if add_text_to_image(bg_path, args.theme, detail, output_path, style):
        # print(f"\n🎉 完成！")  # 静默模式
        print(f"MEDIA:{output_path.resolve()}")
        # 清理背景图
        bg_path.unlink()
    else:
        print("ERROR: Failed to add text to image")
        sys.exit(1)


if __name__ == "__main__":
    main()
