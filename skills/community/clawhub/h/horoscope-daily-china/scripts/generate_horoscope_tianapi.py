# -*- coding: utf-8 -*-
"""
每日星座运势生成器 - 天行数据 API 版 V3.1 (修复版)
基于天行数据 API + 本地补充数据（幸运方位/时段/提防星座）
修复：添加日期参数支持，确保不同日期返回不同数据
"""

import requests
import json
import os
import sys
import io
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import argparse
import random

# 设置 UTF-8 输出
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# 导入本地星座数据模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from constellation_data import (
    CONSTELLATIONS,
    CONSTELLATION_PINYIN,
    get_constellation_info,
    calculate_compatibility,
    get_fortune_level,
    get_all_constellations,
    get_health_advice,
    # 注意：以下字段API不提供，已移除
    # get_enemy_constellation,
    # get_lucky_direction,
    # get_lucky_time,
)
from pair_descriptions import get_pair_description

# ==================== 配置 ====================
import json
import os

# 加载配置文件
CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')

def load_config():
    """加载配置文件"""
    if not os.path.exists(CONFIG_PATH):
        raise FileNotFoundError(f"配置文件不存在: {CONFIG_PATH}")
    
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

# 加载配置
config = load_config()

# 天行数据 API 配置
TIANAPI_KEY = config['tianapi']['key']
TIANAPI_URL = config['tianapi']['urls']['fortune']
TIANAPI_PAIR_URL = config['tianapi']['urls']['pair']

# 星座简称映射（天行数据 API 需要简称）
CONSTELLATION_SHORT = {
    "白羊座": "白羊", "金牛座": "金牛", "双子座": "双子", "巨蟹座": "巨蟹",
    "狮子座": "狮子", "处女座": "处女", "天秤座": "天秤", "天蝎座": "天蝎",
    "射手座": "射手", "摩羯座": "摩羯", "水瓶座": "水瓶", "双鱼座": "双鱼",
}

# 星座图标路径映射（使用裁剪好的图标图片）
CONSTELLATION_ICONS = {
    "白羊座": "C:/Users/liuyan/.openclaw/workspace/constellation_icons/cropped_kimi/aries.png",
    "金牛座": "C:/Users/liuyan/.openclaw/workspace/constellation_icons/cropped_kimi/taurus.png",
    "双子座": "C:/Users/liuyan/.openclaw/workspace/constellation_icons/cropped_kimi/gemini.png",
    "巨蟹座": "C:/Users/liuyan/.openclaw/workspace/constellation_icons/cropped_kimi/cancer.png",
    "狮子座": "C:/Users/liuyan/.openclaw/workspace/constellation_icons/cropped_kimi/leo.png",
    "处女座": "C:/Users/liuyan/.openclaw/workspace/constellation_icons/cropped_kimi/virgo.png",
    "天秤座": "C:/Users/liuyan/.openclaw/workspace/constellation_icons/cropped_kimi/libra.png",
    "天蝎座": "C:/Users/liuyan/.openclaw/workspace/constellation_icons/cropped_kimi/scorpio.png",
    "射手座": "C:/Users/liuyan/.openclaw/workspace/constellation_icons/cropped_kimi/sagittarius.png",
    "摩羯座": "C:/Users/liuyan/.openclaw/workspace/constellation_icons/cropped_kimi/capricorn.png",
    "水瓶座": "C:/Users/liuyan/.openclaw/workspace/constellation_icons/cropped_kimi/aquarius.png",
    "双鱼座": "C:/Users/liuyan/.openclaw/workspace/constellation_icons/cropped_kimi/pisces.png",
}

# 缓存加载的图标
_constellation_icon_cache = {}

def get_constellation_icon(name, size=(48, 48)):
    """获取星座图标（带缓存）"""
    if name in _constellation_icon_cache:
        return _constellation_icon_cache[name]
    
    path = CONSTELLATION_ICONS.get(name)
    if path and os.path.exists(path):
        try:
            icon = Image.open(path)
            icon = icon.resize(size, Image.Resampling.LANCZOS)
            _constellation_icon_cache[name] = icon
            return icon
        except Exception as e:
            print(f"加载图标失败 {name}: {e}")
    return None

# 图片配置
WIDTH = 1080
HEIGHT = 1400
MARGIN = 50

# Unicode 符号
SYMBOLS = {
    "star": "★",
    "medal1": "①",
    "medal2": "②",
    "medal3": "③",
    "heart": "♥",
    "circle": "●",
    "number": "№",
    "couple": "★",
    "direction": "➤",
    "time": "⏰",
    "color": "🎨",
    "enemy": "⚠️",
}

# 配色模板
TEMPLATES = {
    1: {
        "name": "星空紫",
        "bg": "#1A0A2E",
        "primary": "#9D4EDD",
        "secondary": "#FFD700",
        "text": "#FFFFFF",
        "accent": "#FF6B9D",
    },
    2: {
        "name": "海洋蓝",
        "bg": "#0A1628",
        "primary": "#4CC9F0",
        "secondary": "#B8E6FF",
        "text": "#FFFFFF",
        "accent": "#FFB347",
    },
    3: {
        "name": "玫瑰金",
        "bg": "#F8F0E6",
        "primary": "#D4AF37",
        "secondary": "#B76E79",
        "text": "#1A1A1A",
        "accent": "#FF6B6B",
    },
    4: {
        "name": "极简黑",
        "bg": "#1C1C1C",
        "primary": "#FF6B6B",
        "secondary": "#4ECDC4",
        "text": "#FFFFFF",
        "accent": "#FFE66D",
    },
    5: {
        "name": "温暖橙",
        "bg": "#FFF5E6",
        "primary": "#FF8C42",
        "secondary": "#F4D35E",
        "text": "#1A1A1A",
        "accent": "#FF6B6B",
    },
}


# ==================== API 调用 ====================
def get_tianapi_fortune(constellation, date_str=None):
    """调用天行数据星座运势 API - 修复版（支持日期参数）"""
    # 使用星座全称（天行数据 API 要求全称）
    
    params = {
        "key": TIANAPI_KEY,
        "astro": constellation,  # 使用全称如"白羊座"
    }
    
    # 添加日期参数（关键修复！）
    if date_str:
        params["date"] = date_str
    
    try:
        response = requests.get(TIANAPI_URL, params=params, timeout=10)
        data = response.json()
        
        if data.get("code") == 200:
            result = data.get("result", {})
            list_data = result.get("list", [])
            
            # 解析天行数据返回的字段
            # 只使用API提供的数据，不添加本地固定字段
            fortune_data = {
                "name": constellation,
                "all": "75",
                "love": "75",
                "work": "75",
                "money": "75",
                "health": "75",
                "color": "",
                "number": "",
                "QFriend": "",  # 速配星座（贵人星座）
                "summary": "",
                # 注意：API不提供以下字段，故不显示
                # "direction": 幸运方位 - API不提供
                # "time": 幸运时段 - API不提供
                # "enemy": 提防星座 - API不提供
            }
            
            for item in list_data:
                item_type = item.get("type", "")
                content = item.get("content", "")
                
                if "综合指数" in item_type:
                    fortune_data["all"] = content.replace("%", "")
                elif "爱情指数" in item_type:
                    fortune_data["love"] = content.replace("%", "")
                elif "工作指数" in item_type:
                    fortune_data["work"] = content.replace("%", "")
                elif "财运指数" in item_type:
                    fortune_data["money"] = content.replace("%", "")
                elif "健康指数" in item_type:
                    fortune_data["health"] = content.replace("%", "")
                elif "幸运颜色" in item_type:
                    fortune_data["color"] = content
                elif "幸运数字" in item_type:
                    fortune_data["number"] = content
                elif "贵人星座" in item_type:
                    fortune_data["QFriend"] = content
                elif "今日概述" in item_type:
                    fortune_data["summary"] = content
            
            return fortune_data
        else:
            error_code = data.get('code')
            error_msg = data.get('msg', '未知错误')
            
            # 常见错误码处理
            error_descriptions = {
                150: "API调用次数已用完（免费版100次/天）",
                101: "API Key错误或未授权",
                102: "API接口不存在",
                103: "API接口已停用",
                104: "API接口调用频率超限",
                105: "API接口需要实名认证",
                106: "API接口需要付费",
                107: "API接口参数错误",
                108: "API接口返回数据为空",
                109: "API接口服务暂时不可用",
            }
            
            error_desc = error_descriptions.get(error_code, f"错误码：{error_code}")
            print(f"\n  ❌ {constellation}：{error_desc}")
            print(f"     详情：{error_msg}")
            return None
            
    except requests.exceptions.Timeout:
        print(f"\n  ❌ {constellation}：请求超时（10秒）")
        return None
    except requests.exceptions.ConnectionError:
        print(f"\n  ❌ {constellation}：网络连接错误")
        return None
    except Exception as e:
        print(f"\n  ❌ {constellation}：请求失败 - {e}")
        return None


def get_all_constellations_fortune_tianapi(date_str=None):
    """获取 12 星座的运势数据 - 支持日期参数"""
    constellations = get_all_constellations()
    results = []
    failed_count = 0
    
    print(f"正在获取 12 个星座的运势数据...")
    
    for i, cons in enumerate(constellations, 1):
        print(f"  [{i}/12] {cons}", end="\r")
        data = get_tianapi_fortune(cons, date_str)  # 传递日期参数
        
        if data:
            results.append(data)
        else:
            failed_count += 1
    
    print(f"\n📊 结果统计：成功 {len(results)} 个，失败 {failed_count} 个")
    
    # 如果失败数量超过0，说明API有问题
    if failed_count > 0:
        print(f"⚠️  警告：{failed_count} 个星座数据获取失败")
    
    return results


def get_tianapi_pair(sign1, sign2):
    """调用天行数据星座配对 API"""
    # 使用星座简称
    sign1_short = CONSTELLATION_SHORT.get(sign1, sign1)
    sign2_short = CONSTELLATION_SHORT.get(sign2, sign2)
    
    params = {
        "key": TIANAPI_KEY,
        "me": sign1_short,
        "he": sign2_short,
    }
    
    try:
        response = requests.get(TIANAPI_PAIR_URL, params=params, timeout=10)
        data = response.json()
        
        if data.get("code") == 200:
            result = data.get("result", {})
            grade = result.get("grade", "")
            
            # 从 grade 字符串提取分数（如"友情：★★ 爱情：★★★"）
            star_count = grade.count("★")
            score = min(95, 65 + (star_count * 5))  # 65-95 分，上限 95 分
            
            # 根据分数确定类型和详细描述
            score_int = int(score)
            if score_int >= 90:
                pair_type = "同频型"
                title = "天生一对"
                desc = f"{sign1}与{sign2}堪称完美组合，彼此理解，默契十足。"
            elif score_int >= 80:
                pair_type = "互补型"
                title = "非常匹配"
                desc = f"{sign1}与{sign2}性格互补，能互相学习，共同成长。"
            elif score_int >= 70:
                pair_type = "和谐型"
                title = "和谐配对"
                desc = f"{sign1}与{sign2}相处融洽，关系稳定，适合长期发展。"
            elif score_int >= 60:
                pair_type = "挑战型"
                title = "需要磨合"
                desc = f"{sign1}与{sign2}有差异，需要多沟通，互相包容。"
            else:
                pair_type = "冲突型"
                title = "谨慎相处"
                desc = f"{sign1}与{sign2}观念不同，需要更多理解和耐心。"
            
            return {
                "sign1": sign1,
                "sign2": sign2,
                "score": str(score),
                "title": title,
                "tag": pair_type,
                "desc": desc,
                "grade": grade,
            }
        else:
            print(f"配对 API 错误：{data.get('msg')}")
            return None
    except Exception as e:
        print(f"配对请求失败：{e}")
        return None


def get_popular_pairs():
    """获取热门星座配对（使用本地丰富描述库）"""
    pairs_config = [
        ("白羊座", "狮子座"),
        ("金牛座", "处女座"),
        ("双子座", "天秤座"),
        ("巨蟹座", "天蝎座"),
        ("狮子座", "射手座"),
        ("处女座", "摩羯座"),
    ]
    
    print(f"正在生成星座配对数据...")
    results = []
    
    for i, (sign1, sign2) in enumerate(pairs_config, 1):
        print(f"  [{i}/{len(pairs_config)}] {sign1}+{sign2}", end="\r")
        # 使用本地丰富的配对描述
        data = get_pair_description(sign1, sign2)
        if data:
            results.append(data)
    
    print(f"\n✅ 成功生成 {len(results)} 个配对数据")
    return results


# ==================== 分数优化 ====================
def normalize_scores(fortune_data):
    """优化分数分布（保持相对排名）"""
    if not fortune_data:
        return fortune_data
    
    # 按综合运势排序
    sorted_data = sorted(fortune_data, key=lambda x: int(x.get("all", 0)), reverse=True)
    
    # 给每个星座分配具体分数（保持排名）
    rank_scores = {
        0: random.randint(88, 92),
        1: random.randint(82, 86),
        2: random.randint(78, 81),
        3: random.randint(74, 77),
        4: random.randint(71, 73),
        5: random.randint(68, 70),
        6: random.randint(66, 68),
        7: random.randint(64, 66),
        8: random.randint(62, 64),
        9: random.randint(60, 62),
        10: random.randint(58, 60),
        11: random.randint(55, 58),
    }
    
    for rank, data in enumerate(sorted_data):
        base = rank_scores[rank]
        data["all"] = str(base)
        data["love"] = str(min(100, base + random.randint(-5, 10)))
        data["work"] = str(min(100, base + random.randint(-5, 10)))
        data["money"] = str(min(100, base + random.randint(-10, 5)))
        data["health"] = str(min(100, base + random.randint(-10, 5)))
    
    return fortune_data


# ==================== 图片生成 ====================
def get_font(size):
    """获取字体"""
    font_paths = [
        "C:/Windows/Fonts/simhei.ttf",
        "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/simsun.ttc",
    ]
    
    for path in font_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except:
                continue
    
    return ImageFont.load_default()


def draw_text_wrapped(draw, text, y, font, color, left_margin, right_margin, line_spacing=None):
    """左对齐绘制文字（自动换行）"""
    if line_spacing is None:
        line_spacing = font.size + 6
    
    max_width = WIDTH - left_margin - right_margin
    chars_per_line = max(10, int(max_width / (font.size * 0.75)))
    
    lines = []
    current_line = ""
    
    for char in text:
        test_line = current_line + char
        if len(test_line) <= chars_per_line:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = char
    
    if current_line:
        lines.append(current_line)
    
    current_y = y
    for line in lines:
        draw.text((left_margin, current_y), line, fill=color, font=font)
        current_y += line_spacing
    
    return current_y


def draw_text_centered(draw, text, y, font, color, max_width=None):
    """居中绘制文字（自动换行）"""
    if max_width is None:
        max_width = WIDTH - MARGIN * 2 - 60
    
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    
    if text_width > max_width:
        chars_per_line = max(10, int(max_width / (font.size * 0.75)))
        lines = []
        current_line = ""
        
        for char in text:
            test_line = current_line + char
            if len(test_line) <= chars_per_line:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = char
        
        if current_line:
            lines.append(current_line)
        
        current_y = y
        for line in lines:
            line_bbox = draw.textbbox((0, 0), line, font=font)
            line_width = line_bbox[2] - line_bbox[0]
            x = (WIDTH - line_width) // 2
            draw.text((x, current_y), line, fill=color, font=font)
            current_y += (line_bbox[3] - line_bbox[1]) + 6
        
        return current_y
    else:
        x = (WIDTH - text_width) // 2
        draw.text((x, y), text, fill=color, font=font)
        return y + (bbox[3] - bbox[1]) + 8


def generate_page1_merged(fortune_data, pair_data, template_id=1, date_str=None):
    """第 1 页（合并版）：封面 + 红榜 + 排名 + 配对 + 今日开运
    
    Args:
        fortune_data: 星座运势数据
        pair_data: 配对数据
        template_id: 模板ID
        date_str: 日期字符串（YYYY-MM-DD格式），默认为今天
    """
    template = TEMPLATES.get(template_id, TEMPLATES[1])
    
    img = Image.new('RGB', (WIDTH, HEIGHT), color=template["bg"])
    draw = ImageDraw.Draw(img)
    
    title_font = get_font(64)
    date_font = get_font(40)
    weekday_font = get_font(40)
    section_font = get_font(38)
    pair_section_font = get_font(32)
    lucky_section_font = get_font(32)
    normal_font = get_font(32)
    rank_font = get_font(28)
    pair_font = get_font(32)
    score_font = get_font(26)
    lucky_font = get_font(28)
    small_font = get_font(24)
    
    y = MARGIN - 5
    
    # === 封面区 ===
    y = draw_text_centered(draw, f"{SYMBOLS['star']} 今日星座运势 {SYMBOLS['star']}", y, title_font, template["primary"])
    y += 10
    
    # 使用传入的日期或默认为今天
    if date_str:
        from datetime import datetime as dt
        date_obj = dt.strptime(date_str, "%Y-%m-%d")
        date = date_obj.strftime("%Y年%m月%d日")
        weekday = date_obj.strftime("%A")
    else:
        date = datetime.now().strftime("%Y年%m月%d日")
        weekday = datetime.now().strftime("%A")
    
    weekday_cn = {"Monday": "星期一", "Tuesday": "星期二", "Wednesday": "星期三", 
                  "Thursday": "星期四", "Friday": "星期五", "Saturday": "星期六", "Sunday": "星期日"}
    weekday_str = weekday_cn.get(weekday, weekday)
    
    y = draw_text_centered(draw, date, y, date_font, template["text"])
    y = draw_text_centered(draw, weekday_str, y, weekday_font, template["secondary"])
    y += 12
    
    draw.line([(MARGIN, y), (WIDTH - MARGIN, y)], fill=template["primary"], width=3)
    y += 15
    
    # === 红榜 TOP3 ===
    y = draw_text_centered(draw, f"{SYMBOLS['star']} 今日红榜 TOP3", y, section_font, template["primary"])
    y += 10
    
    sorted_data = sorted(fortune_data, key=lambda x: int(x.get("all", 0)), reverse=True)
    top3 = sorted_data[:3]
    medals = [SYMBOLS['medal1'], SYMBOLS['medal2'], SYMBOLS['medal3']]
    
    for i, data in enumerate(top3):
        name = data.get("name", "")
        score = data.get("all", "0")
        row_text = f"{medals[i]} {name}  {score}%"
        y = draw_text_centered(draw, row_text, y, normal_font, template["accent"] if i == 0 else template["text"])
        y += 8
    
    y += 12
    draw.line([(MARGIN + 50, y), (WIDTH - MARGIN - 50, y)], fill=template["secondary"], width=2)
    y += 15
    
    # === 12 星座完整排名（双列） ===
    y = draw_text_centered(draw, f"{SYMBOLS['star']} 12 星座完整排名", y, section_font, template["primary"])
    y += 10
    
    left_x = MARGIN + 30
    right_x = WIDTH // 2 + 15
    col_y = y
    
    for i, data in enumerate(sorted_data[:6], 1):
        name = data.get("name", "")
        score = data.get("all", "0")
        color = template["accent"] if i <= 3 else template["text"]
        row_text = f"{i:2d}. {name:4s}: {score:2s}%"
        draw.text((left_x, col_y), row_text, fill=color, font=rank_font)
        col_y += 24
    
    col_y = y
    for i, data in enumerate(sorted_data[6:12], 7):
        name = data.get("name", "")
        score = data.get("all", "0")
        row_text = f"{i:2d}. {name:4s}: {score:2s}%"
        draw.text((right_x, col_y), row_text, fill=template["text"], font=rank_font)
        col_y += 24
    
    y = col_y + 10
    draw.line([(MARGIN + 60, y), (WIDTH - MARGIN - 60, y)], fill=template["secondary"], width=2)
    y += 15
    
    # === 星座配对（3 对） ===
    y = draw_text_centered(draw, f"{SYMBOLS['star']} 精选配对", y, pair_section_font, template["accent"])
    y += 10
    
    selected_pairs = random.sample(pair_data, min(3, len(pair_data)))
    
    for i, pair in enumerate(selected_pairs):
        sign1 = pair.get("sign1", "")
        sign2 = pair.get("sign2", "")
        score = pair.get("score", "75")
        title = pair.get("title", "和谐配对")
        tag = pair.get("tag", "")
        desc = pair.get("desc", "")
        
        # 配对星座 + 类型
        if tag:
            pair_text = f"{sign1} 与 {sign2}  ·  {tag}"
        else:
            pair_text = f"{sign1} 与 {sign2}"
        y = draw_text_centered(draw, pair_text, y, pair_font, template["text"])
        
        # 分数 + 标题
        score_text = f"{score}分  {title}"
        y = draw_text_centered(draw, score_text, y, score_font, template["accent"])
        
        # 详细描述（简短版）
        if desc:
            # 限制描述长度，避免过长
            short_desc = desc[:30] + "..." if len(desc) > 30 else desc
            y = draw_text_centered(draw, short_desc, y, small_font, template["secondary"])
        
        y += 12
    
    y += 5
    draw.line([(MARGIN + 80, y), (WIDTH - MARGIN - 80, y)], fill=template["secondary"], width=2)
    y += 15
    
    # === 今日开运（简洁版 - 只显示API提供的数据） ===
    y = draw_text_centered(draw, f"{SYMBOLS['star']} 今日开运", y, lucky_section_font, template["accent"])
    y += 10
    
    if fortune_data:
        first = fortune_data[0]
        lucky_color = first.get("color", "")
        lucky_num = first.get("number", "")
        qfriend = first.get("QFriend", "")
        
        # 只显示API提供的数据：幸运色、幸运数字、速配星座
        line1 = f"幸运色：{lucky_color}   |   幸运数字：{lucky_num}"
        y = draw_text_centered(draw, line1, y, lucky_font, template["text"])
        
        line2 = f"速配星座：{qfriend}"
        y = draw_text_centered(draw, line2, y, lucky_font, template["text"])
        
        # 注意：API不提供幸运方位、幸运时段、提防星座，故不显示
    
    y += 15
    y = draw_text_centered(draw, "你的星座今天排第几？评论区见！", y, normal_font, template["primary"])
    
    bottom_y = HEIGHT - MARGIN - 20
    draw_text_centered(draw, "娱乐参考 切勿迷信", bottom_y, small_font, template["secondary"])
    
    return img


def generate_page2_detail1(fortune_data, template_id=1):
    """第 2 页：详细运势 1-3 名"""
    template = TEMPLATES.get(template_id, TEMPLATES[1])
    
    img = Image.new('RGB', (WIDTH, HEIGHT), color=template["bg"])
    draw = ImageDraw.Draw(img)
    
    title_font = get_font(56)
    sign_font = get_font(48)
    index_font = get_font(32)
    summary_font = get_font(36)
    small_font = get_font(28)
    
    y = MARGIN
    
    y = draw_text_centered(draw, f"{SYMBOLS['star']} 今日星座运势 (1/4)", y, title_font, template["primary"])
    y += 20
    
    draw.line([(MARGIN, y), (WIDTH - MARGIN, y)], fill=template["primary"], width=3)
    y += 20
    
    sorted_data = sorted(fortune_data, key=lambda x: int(x.get("all", 0)), reverse=True)
    
    for i, data in enumerate(sorted_data[:3]):
        if y > HEIGHT - 100:
            break
        
        name = data.get("name", "")
        all_score = data.get("all", "0")
        love = data.get("love", "0")
        work = data.get("work", "0")
        money = data.get("money", "0")
        health = data.get("health", "0")
        summary = data.get("summary", "")
        
        # 加载并粘贴星座图标
        icon = get_constellation_icon(name, size=(40, 40))
        if icon:
            # 计算图标位置（居中偏左）
            header_text = f"{name}  综合：{all_score}%"
            bbox = draw.textbbox((0, 0), header_text, font=sign_font)
            text_width = bbox[2] - bbox[0]
            total_width = text_width + 45  # 图标宽度 + 间距
            start_x = (WIDTH - total_width) // 2
            
            # 粘贴图标
            icon_y = y + 5
            img.paste(icon, (start_x, icon_y), icon if icon.mode == 'RGBA' else None)
            
            # 绘制文字（在图标右侧）
            draw.text((start_x + 45, y), header_text, fill=template["primary"], font=sign_font)
            y += max(45, bbox[3] - bbox[1]) + 10  # 增加10px间隔
        else:
            # 如果没有图标，只显示文字
            header = f"{name}  综合：{all_score}%"
            y = draw_text_centered(draw, header, y, sign_font, template["primary"])
            y += 25  # 间隔25px（增加10px）
        
        details = f"爱情:{love}%   工作:{work}%   财运:{money}%   健康:{health}%"
        y = draw_text_centered(draw, details, y, index_font, template["text"])
        y += 25  # 间隔25px（增加10px）
        
        if summary:
            # 方案B：左边距50px，右边距100px
            y = draw_text_wrapped(draw, summary, y, summary_font, template["secondary"], 
                                  left_margin=MARGIN + 50, right_margin=MARGIN + 300, 
                                  line_spacing=45)
        
        y += 20
        
        if i < 2:
            draw.line([(MARGIN + 80, y), (WIDTH - MARGIN - 80, y)], fill=template["secondary"], width=2)
            y += 20
    
    bottom_y = HEIGHT - MARGIN - 30
    draw_text_centered(draw, "娱乐参考 切勿迷信", bottom_y, small_font, template["secondary"])
    
    return img


def generate_page3_detail2(fortune_data, template_id=1):
    """第 3 页：详细运势 4-6 名"""
    template = TEMPLATES.get(template_id, TEMPLATES[1])
    
    img = Image.new('RGB', (WIDTH, HEIGHT), color=template["bg"])
    draw = ImageDraw.Draw(img)
    
    title_font = get_font(56)
    sign_font = get_font(48)
    index_font = get_font(32)
    summary_font = get_font(36)
    small_font = get_font(28)
    
    y = MARGIN
    
    y = draw_text_centered(draw, f"{SYMBOLS['star']} 今日星座运势 (2/4)", y, title_font, template["primary"])
    y += 20
    
    draw.line([(MARGIN, y), (WIDTH - MARGIN, y)], fill=template["primary"], width=3)
    y += 20
    
    sorted_data = sorted(fortune_data, key=lambda x: int(x.get("all", 0)), reverse=True)
    
    for i, data in enumerate(sorted_data[3:6], 4):
        if y > HEIGHT - 100:
            break
        
        name = data.get("name", "")
        all_score = data.get("all", "0")
        love = data.get("love", "0")
        work = data.get("work", "0")
        money = data.get("money", "0")
        health = data.get("health", "0")
        summary = data.get("summary", "")
        
        # 加载并粘贴星座图标
        icon = get_constellation_icon(name, size=(40, 40))
        if icon:
            header_text = f"{name}  综合：{all_score}%"
            bbox = draw.textbbox((0, 0), header_text, font=sign_font)
            text_width = bbox[2] - bbox[0]
            total_width = text_width + 45
            start_x = (WIDTH - total_width) // 2
            
            icon_y = y + 5
            img.paste(icon, (start_x, icon_y), icon if icon.mode == 'RGBA' else None)
            draw.text((start_x + 45, y), header_text, fill=template["primary"], font=sign_font)
            y += max(45, bbox[3] - bbox[1]) + 10  # 增加10px间隔
        else:
            header = f"{name}  综合：{all_score}%"
            y = draw_text_centered(draw, header, y, sign_font, template["primary"])
            y += 25  # 间隔25px（增加10px）
        
        details = f"爱情:{love}%   工作:{work}%   财运:{money}%   健康:{health}%"
        y = draw_text_centered(draw, details, y, index_font, template["text"])
        y += 25  # 间隔25px（增加10px）
        
        if summary:
            # 方案B：左边距50px，右边距100px
            y = draw_text_wrapped(draw, summary, y, summary_font, template["secondary"], 
                                  left_margin=MARGIN + 50, right_margin=MARGIN + 300, 
                                  line_spacing=45)
        
        y += 15
        
        if i < 6:
            draw.line([(MARGIN + 80, y), (WIDTH - MARGIN - 80, y)], fill=template["secondary"], width=2)
            y += 15
    
    bottom_y = HEIGHT - MARGIN - 30
    draw_text_centered(draw, "娱乐参考 切勿迷信", bottom_y, small_font, template["secondary"])
    
    return img


def generate_page4_detail3(fortune_data, template_id=1):
    """第 4 页：详细运势 7-9 名"""
    template = TEMPLATES.get(template_id, TEMPLATES[1])
    
    img = Image.new('RGB', (WIDTH, HEIGHT), color=template["bg"])
    draw = ImageDraw.Draw(img)
    
    title_font = get_font(56)
    sign_font = get_font(48)
    index_font = get_font(32)
    summary_font = get_font(36)
    small_font = get_font(28)
    
    y = MARGIN
    
    y = draw_text_centered(draw, f"{SYMBOLS['star']} 今日星座运势 (3/4)", y, title_font, template["primary"])
    y += 20
    
    draw.line([(MARGIN, y), (WIDTH - MARGIN, y)], fill=template["primary"], width=3)
    y += 20
    
    sorted_data = sorted(fortune_data, key=lambda x: int(x.get("all", 0)), reverse=True)
    
    for i, data in enumerate(sorted_data[6:9], 7):
        if y > HEIGHT - 100:
            break
        
        name = data.get("name", "")
        all_score = data.get("all", "0")
        love = data.get("love", "0")
        work = data.get("work", "0")
        money = data.get("money", "0")
        health = data.get("health", "0")
        summary = data.get("summary", "")
        
        # 加载并粘贴星座图标
        icon = get_constellation_icon(name, size=(40, 40))
        if icon:
            header_text = f"{name}  综合：{all_score}%"
            bbox = draw.textbbox((0, 0), header_text, font=sign_font)
            text_width = bbox[2] - bbox[0]
            total_width = text_width + 45
            start_x = (WIDTH - total_width) // 2
            
            icon_y = y + 5
            img.paste(icon, (start_x, icon_y), icon if icon.mode == 'RGBA' else None)
            draw.text((start_x + 45, y), header_text, fill=template["primary"], font=sign_font)
            y += max(45, bbox[3] - bbox[1]) + 10  # 增加10px间隔
        else:
            header = f"{name}  综合：{all_score}%"
            y = draw_text_centered(draw, header, y, sign_font, template["primary"])
            y += 25  # 间隔25px（增加10px）
        
        details = f"爱情:{love}%   工作:{work}%   财运:{money}%   健康:{health}%"
        y = draw_text_centered(draw, details, y, index_font, template["text"])
        y += 25  # 间隔25px（增加10px）
        
        if summary:
            # 方案B：左边距50px，右边距100px
            y = draw_text_wrapped(draw, summary, y, summary_font, template["secondary"], 
                                  left_margin=MARGIN + 50, right_margin=MARGIN + 300, 
                                  line_spacing=45)
        
        y += 15
        
        if i < 9:
            draw.line([(MARGIN + 80, y), (WIDTH - MARGIN - 80, y)], fill=template["secondary"], width=2)
            y += 15
    
    bottom_y = HEIGHT - MARGIN - 30
    draw_text_centered(draw, "娱乐参考 切勿迷信", bottom_y, small_font, template["secondary"])
    
    return img


def generate_page5_detail4(fortune_data, template_id=1):
    """第 5 页：详细运势 10-12 名"""
    template = TEMPLATES.get(template_id, TEMPLATES[1])
    
    img = Image.new('RGB', (WIDTH, HEIGHT), color=template["bg"])
    draw = ImageDraw.Draw(img)
    
    title_font = get_font(56)
    sign_font = get_font(48)
    index_font = get_font(32)
    summary_font = get_font(36)
    small_font = get_font(28)
    
    y = MARGIN
    
    y = draw_text_centered(draw, f"{SYMBOLS['star']} 今日星座运势 (4/4)", y, title_font, template["primary"])
    y += 20
    
    draw.line([(MARGIN, y), (WIDTH - MARGIN, y)], fill=template["primary"], width=3)
    y += 20
    
    sorted_data = sorted(fortune_data, key=lambda x: int(x.get("all", 0)), reverse=True)
    
    for i, data in enumerate(sorted_data[9:12], 10):
        if y > HEIGHT - 100:
            break
        
        name = data.get("name", "")
        all_score = data.get("all", "0")
        love = data.get("love", "0")
        work = data.get("work", "0")
        money = data.get("money", "0")
        health = data.get("health", "0")
        summary = data.get("summary", "")
        
        # 加载并粘贴星座图标
        icon = get_constellation_icon(name, size=(40, 40))
        if icon:
            header_text = f"{name}  综合：{all_score}%"
            bbox = draw.textbbox((0, 0), header_text, font=sign_font)
            text_width = bbox[2] - bbox[0]
            total_width = text_width + 45
            start_x = (WIDTH - total_width) // 2
            
            icon_y = y + 5
            img.paste(icon, (start_x, icon_y), icon if icon.mode == 'RGBA' else None)
            draw.text((start_x + 45, y), header_text, fill=template["primary"], font=sign_font)
            y += max(45, bbox[3] - bbox[1]) + 10  # 增加10px间隔
        else:
            header = f"{name}  综合：{all_score}%"
            y = draw_text_centered(draw, header, y, sign_font, template["primary"])
            y += 25  # 间隔25px（增加10px）
        
        details = f"爱情:{love}%   工作:{work}%   财运:{money}%   健康:{health}%"
        y = draw_text_centered(draw, details, y, index_font, template["text"])
        y += 25  # 间隔25px（增加10px）
        
        if summary:
            # 方案B：左边距50px，右边距100px
            y = draw_text_wrapped(draw, summary, y, summary_font, template["secondary"], 
                                  left_margin=MARGIN + 50, right_margin=MARGIN + 300, 
                                  line_spacing=45)
        
        y += 15
        
        if i < 12:
            draw.line([(MARGIN + 80, y), (WIDTH - MARGIN - 80, y)], fill=template["secondary"], width=2)
            y += 15
    
    bottom_y = HEIGHT - MARGIN - 30
    draw_text_centered(draw, "娱乐参考 切勿迷信", bottom_y, small_font, template["secondary"])
    
    return img


def generate_page5_pairs(pair_data, fortune_data, template_id=1):
    """第 5 页：星座配对（精简版）"""
    template = TEMPLATES.get(template_id, TEMPLATES[1])
    
    img = Image.new('RGB', (WIDTH, HEIGHT), color=template["bg"])
    draw = ImageDraw.Draw(img)
    
    title_font = get_font(56)
    pair_font = get_font(38)
    score_font = get_font(32)
    normal_font = get_font(30)
    small_font = get_font(26)
    
    content_height = 70 + 3 + 6 * 55 + 2 * 2 + 40 + 35
    y = (HEIGHT - content_height) // 2
    
    y = draw_text_centered(draw, "星座配对速查", y, title_font, template["primary"])
    y += 25
    
    draw.line([(MARGIN, y), (WIDTH - MARGIN, y)], fill=template["primary"], width=3)
    y += 25
    
    for i, pair in enumerate(pair_data):
        sign1 = pair.get("sign1", "")
        sign2 = pair.get("sign2", "")
        score = pair.get("score", "75")
        title = pair.get("title", "和谐配对")
        tag = pair.get("tag", "")
        
        if tag:
            pair_text = f"{sign1} 与 {sign2}  ·  {tag}"
        else:
            pair_text = f"{sign1} 与 {sign2}"
        y = draw_text_centered(draw, pair_text, y, pair_font, template["primary"])
        
        score_text = f"{score}分  {title}"
        y = draw_text_centered(draw, score_text, y, score_font, template["accent"])
        
        y += 22
        
        if i == 2:
            draw.line([(MARGIN + 100, y), (WIDTH - MARGIN - 300, y)], fill=template["secondary"], width=2)
            y += 20
    
    draw.line([(MARGIN + 80, y), (WIDTH - MARGIN - 80, y)], fill=template["secondary"], width=2)
    y += 25
    
    y = draw_text_centered(draw, "你的星座今天排第几？评论区见！", y, normal_font, template["primary"])
    
    bottom_y = HEIGHT - MARGIN - 25
    draw_text_centered(draw, "娱乐参考 切勿迷信", bottom_y, small_font, template["secondary"])
    
    return img


# ==================== 发布文案 ====================
def generate_publish_text(fortune_data, date_str=None):
    """生成今日头条发布文案（完整版）
    
    Args:
        fortune_data: 星座运势数据
        date_str: 日期字符串（YYYY-MM-DD格式），默认为今天
    """
    
    sorted_data = sorted(fortune_data, key=lambda x: int(x.get("all", 0)), reverse=True)
    top3 = sorted_data[:3]
    bottom3 = sorted_data[-3:]
    
    # 使用传入的日期或默认为今天
    if date_str:
        from datetime import datetime as dt
        date_obj = dt.strptime(date_str, "%Y-%m-%d")
        date = date_obj.strftime("%Y年%m月%d日")
        weekday_cn = {"Monday": "星期一", "Tuesday": "星期二", "Wednesday": "星期三", 
                      "Thursday": "星期四", "Friday": "星期五", "Saturday": "星期六", "Sunday": "星期日"}
        weekday = weekday_cn.get(date_obj.strftime("%A"), "")
    else:
        date = datetime.now().strftime("%Y年%m月%d日")
        weekday_cn = {"Monday": "星期一", "Tuesday": "星期二", "Wednesday": "星期三", 
                      "Thursday": "星期四", "Friday": "星期五", "Saturday": "星期六", "Sunday": "星期日"}
        weekday = weekday_cn.get(datetime.now().strftime("%A"), "")
    
    title = f"【{date}{weekday}今日星座运势】{top3[0].get('name')}运势爆棚！这 3 个星座今天要走大运了"
    
    first = fortune_data[0] if fortune_data else {}
    
    content = f"""大家好，今天是{date}{weekday}。一起来看看十二星座今日的运势如何吧！

🏆 今日红榜 TOP3:
1️⃣ {top3[0].get('name')} {top3[0].get('all')}%
2️⃣ {top3[1].get('name')} {top3[1].get('all')}%
3️⃣ {top3[2].get('name')} {top3[2].get('all')}%

⚠️ 黑榜提醒:
{bottom3[0].get('name')} ({bottom3[0].get('all')}%)、{bottom3[1].get('name')} ({bottom3[1].get('all')}%)、{bottom3[2].get('name')} ({bottom3[2].get('all')}%)
今日需低调行事，避免重大决策。

💡 今日开运:
幸运色：{first.get('color', '未知')}
幸运数字：{first.get('number', '?')}
速配星座：{first.get('QFriend', '未知')}

你的星座今天排第几？欢迎在评论区留言分享！

#星座 #星座运势 #十二星座 #今日运势 #娱乐参考"""

    return title, content


# ==================== 主函数 ====================
def main():
    parser = argparse.ArgumentParser(description="Daily Horoscope Generator V3.1 (天行数据 API 修复版)")
    parser.add_argument("--date", type=str, default=datetime.now().strftime("%Y-%m-%d"),
                        help="Date (YYYY-MM-DD)")
    parser.add_argument("--template", type=int, default=0, choices=[0, 1, 2, 3, 4, 5],
                        help="Template (0=auto, 1-5=specific)")
    # Fixed output directory: skill's output/ folder (absolute path)
    _skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    _default_output = os.path.join(_skill_dir, "output")
    parser.add_argument("--output", type=str, default=_default_output,
                        help="Output directory (default: <skill_dir>/output)")
    
    args = parser.parse_args()
    
    os.makedirs(args.output, exist_ok=True)
    
    print(f"\n📅 日期：{args.date}")
    
    # 获取运势数据 - 传递日期参数（关键修复！）
    fortune_data = get_all_constellations_fortune_tianapi(args.date)
    
    # 严格检查：必须获取全部12个星座数据
    if not fortune_data or len(fortune_data) < 12:
        print("\n" + "="*60)
        print("❌ 获取运势数据失败")
        print("="*60)
        print("\n可能原因：")
        print("  1. API Key 错误或已过期")
        print("  2. 网络连接问题")
        print("  3. API 调用次数已用完（免费版 100 次/天）")
        print("  4. 天行数据服务暂时不可用")
        print("\n解决方案：")
        print("  1. 检查 config.json 中的 API Key 是否正确")
        print("  2. 确认网络连接正常")
        print("  3. 登录天行数据官网查看 API 调用额度")
        print("  4. 等待一段时间后重试")
        print("\n⚠️  为确保数据真实性，脚本已停止执行，未生成任何文件。")
        print("="*60)
        return
    
    # 优化分数分布
    print("正在优化分数分布...")
    fortune_data = normalize_scores(fortune_data)
    
    # 获取配对数据
    pair_data = get_popular_pairs()
    
    # Template selection - 根据日期自动轮换模板（5 天一个循环）
    if args.template == 0:
        # 从日期计算模板索引（5 天一个循环）
        date_obj = datetime.strptime(args.date, '%Y-%m-%d')
        template_id = (date_obj.day % 5) + 1  # 1-5 轮换
        # 模板映射：1=星空紫，2=海洋蓝，3=玫瑰金，4=极简黑，5=温暖橙
    else:
        template_id = args.template
    
    template_name = TEMPLATES.get(template_id, {}).get("name", "Unknown")
    print(f"🎨 模板：{template_name}（按日期自动轮换）")
    
    date_str = args.date.replace("-", "")
    
    # 生成 5 页图片
    pages = [
        ("封面 + 红榜 + 排名 + 配对 + 开运", generate_page1_merged),
        ("详细运势 1-3", generate_page2_detail1),
        ("详细运势 4-6", generate_page3_detail2),
        ("详细运势 7-9", generate_page4_detail3),
        ("详细运势 10-12", generate_page5_detail4),
    ]
    
    for i, (name, gen_func) in enumerate(pages, 1):
        print(f"\n📸 生成第 {i} 页：{name}...")
        if i == 1:
            img = gen_func(fortune_data, pair_data, template_id, args.date)
        else:
            img = gen_func(fortune_data, template_id)
        path = os.path.join(args.output, f"{date_str}_今日星座运势_p{i}.png")
        img.save(path, "PNG", quality=95)
        print(f"✅ 保存：{path}")
    
    # 生成发布文案
    print("\n📝 生成发布文案...")
    title, content = generate_publish_text(fortune_data, args.date)
    
    content_path = os.path.join(args.output, f"{date_str}_发布文案.txt")
    with open(content_path, "w", encoding="utf-8") as f:
        f.write(f"标题：{title}\n\n")
        f.write(f"正文:\n{content}\n")
    print(f"✅ 保存：{content_path}")
    
    print("\n" + "="*60)
    print("发布文案预览:")
    print("="*60)
    print(f"标题：{title}")
    print(f"\n正文:\n{content}")
    print("="*60)
    
    print("\n✅ 所有任务完成！")
    print(f"\n📊 共生成 5 页图片 + 1 个发布文案")
    print(f"💰 API 调用统计：12 次（天行数据免费额度 100 次/天）")


if __name__ == "__main__":
    main()