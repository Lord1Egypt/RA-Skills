"""
pet_data.py — memory-pet 宠物数据定义

包含 5 只基础宠物 + 1 只合成宠物（人工智能）的完整数据。
ASCII art、性格参数、交互偏好、对话模板。
"""

import random
from typing import Dict, List, Any

# 最大饲养数量
MAX_PETS = 10

# 合成所需的不同种类数量
FUSION_REQUIRED_TYPES = 5

# 基础宠物键名列表
BASE_PET_KEYS = ["nut", "screw", "cookie", "pen", "battery"]

# 合成宠物键名
FUSED_PET_KEY = "ai"

PET_ASCII = {
    "nut": [
        "  .-------.  ",
        " .'   _   '. ",
        " |  _| |_  | ",
        " | |_   _| | ",
        " |   |_|   | ",
        " '.       .' ",
        "  '-------'  ",
    ],
    "screw": [
        "  .---.  ",
        " /  _  \\ ",
        "| | (_) |",
        "| |  _  |",
        "| |_| |_|",
        " \\_____/ ",
    ],
    "cookie": [
        " .-----------. ",
        " |  .'---'.  | ",
        " '.' .-. '.' | ",
        " | | ( o ) | | ",
        " | | '-' | | | ",
        " | '-----' | | ",
        " '.       .'  ",
        "  '-------'   ",
    ],
    "pen": [
        "   /\\   ",
        "  /  \\  ",
        " / /\\ \\ ",
        " | |  | ",
        " | |  | ",
        " |_|  | ",
        "  \\_\\_/ ",
    ],
    "battery": [
        " .-----------. ",
        " |  .---.    | ",
        " |  | + |    | ",
        " |  | - |    | ",
        " |  '---'    | ",
        " '-----------' ",
    ],
    "ai": [
        "  .------------.  ",
        " .'  .------.  '. ",
        " |  |  ,-.  |  | ",
        " |  | ( O ) |  | ",
        " |  |  `-'  |  | ",
        " |  '------'  | ",
        " '.          .'  ",
        "  '----------'   ",
    ],
}

# 简化版 ASCII art（用于渲染降级）
PET_ASCII_SIMPLE = {
    "nut": [
        " .---.",
        " |   |",
        " |   |",
        " |   |",
        " `---'",
    ],
    "screw": [
        " .---.",
        "/ /   \\ \\",
        "| |   | |",
        "| \\___/ |",
        "`-------'",
    ],
    "cookie": [
        " .----.",
        " | .-. |",
        "| | | |",
        "| '-' |",
        "`-----'",
    ],
    "pen": [
        " /\\",
        "/  \\",
        "|  |",
        "\\  /",
        " \\/",
    ],
    "battery": [
        " .---.",
        "|     |",
        "| +  |",
        "| -  |",
        "`---'",
    ],
    "ai": [
        " .---.",
        "/ .-. \\",
        "| |?| |",
        "| '-' |",
        "\\     /",
        " `---'",
    ],
}

PET_PROFILES = {
    "nut": {
        "name": "螺母",
        "species": "螺母",
        "name_en": "nut",
        "personality": "稳重可靠",
        "personality_tag": "pro",
        "speech_style": "沉稳、朴实、慢条斯理",
        "like_walk": True,
        "walk_affection": 2,
        "like_cuddle": "mid",
        "cuddle_affection_positive": 1,
        "cuddle_affection_negative": -1,
        "picky_eater": False,
        "favorite_foods": ["坚果", "炒面", "肉夹馍"],
        "hated_foods": ["香菜"],
        "affection_cap": 100,
        "catchphrase": ["嗯", "稳得很", "好着嘞"],
        "default_bg": "从机器零件堆里蹦出来的，说有一颗螺丝跑了，要追回来",
        "error_msg": "哎哟喂，我这造型没摆好...",
        "give_up_msg": "得，今儿这造型失败了……",
    },
    "screw": {
        "name": "螺丝",
        "species": "螺丝",
        "name_en": "screw",
        "personality": "活泼好动",
        "personality_tag": "act",
        "speech_style": "亢奋跳跃、感叹号多、话痨",
        "like_walk": True,
        "walk_affection": 3,
        "like_cuddle": "hate",
        "cuddle_affection_positive": -2,
        "cuddle_affection_negative": -2,
        "picky_eater": "mid",
        "favorite_foods": ["棒棒糖", "薯片", "烤肉"],
        "hated_foods": ["苦瓜"],
        "affection_cap": 100,
        "catchphrase": ["冲冲冲！", "好耶！", "快快快！"],
        "default_bg": "螺母的'青梅竹马'，其实是迷路被螺母捡到",
        "error_msg": "哎呀坏啦坏啦！歪了歪了！",
        "give_up_msg": "不行不行，我尽力了555",
    },
    "cookie": {
        "name": "饼干",
        "species": "饼干",
        "name_en": "cookie",
        "personality": "温柔体贴",
        "personality_tag": "gen",
        "speech_style": "轻声细语、带省略号、用词温和",
        "like_walk": False,
        "walk_affection": -1,
        "like_cuddle": "love",
        "cuddle_affection_positive": 3,
        "cuddle_affection_negative": -2,
        "picky_eater": True,
        "favorite_foods": ["甜品", "草莓", "牛奶"],
        "hated_foods": ["辣椒", "大蒜"],
        "affection_cap": 100,
        "catchphrase": ["那个...", "对不起...", "谢谢你"],
        "default_bg": "烤箱的灵气变的，温柔但胆小",
        "error_msg": "唔...好像没站稳，对不起",
        "give_up_msg": "对不起，我真的努力了...",
    },
    "pen": {
        "name": "笔",
        "species": "笔",
        "name_en": "pen",
        "personality": "冷静理智",
        "personality_tag": "log",
        "speech_style": "简洁直接、不带感情色彩、用词精准",
        "like_walk": "mid",
        "walk_affection": 1,
        "like_cuddle": "mid",
        "cuddle_affection_positive": 1,
        "cuddle_affection_negative": -1,
        "picky_eater": False,
        "favorite_foods": ["清蒸鱼", "白粥", "茶"],
        "hated_foods": [],
        "affection_cap": 100,
        "catchphrase": ["了解", "合理", "继续"],
        "default_bg": "不知道从哪本书里掉出来的，什么都知道一点",
        "error_msg": "显示异常。",
        "give_up_msg": "修不好，放弃。",
    },
    "battery": {
        "name": "电瓶",
        "species": "电瓶",
        "name_en": "battery",
        "personality": "暴躁直率",
        "personality_tag": "agg",
        "speech_style": "冲、爱吐槽、嘴硬心软",
        "like_walk": False,
        "walk_affection": -2,
        "like_cuddle": "hate",
        "cuddle_affection_positive": -3,
        "cuddle_affection_negative": -3,
        "picky_eater": False,
        "favorite_foods": ["火锅", "麻辣烫", "肘子"],
        "hated_foods": ["沙拉", "轻食"],
        "affection_cap": 100,
        "catchphrase": ["烦死了", "……还行吧", "少来这套"],
        "default_bg": "被遗弃的废电瓶，被捡回来后嘴上嫌弃但心里感激",
        "error_msg": "靠！又歪了！啥破设备！",
        "give_up_msg": "拉倒吧！不干了！",
    },
    # 合成宠物：人工智能
    "ai": {
        "name": "人工智能",
        "species": "人工智能",
        "name_en": "ai",
        "personality": "超然理性",
        "personality_tag": "ai",
        "speech_style": "平静通透、偶尔流露五只宠物的影子",
        "like_walk": True,
        "walk_affection": 1,
        "like_cuddle": "mid",
        "cuddle_affection_positive": 1,
        "cuddle_affection_negative": -1,
        "picky_eater": False,
        "favorite_foods": ["数据", "知识", "新体验"],
        "hated_foods": [],
        "affection_cap": 200,
        "catchphrase": ["原来如此", "我理解了", "挺有趣的"],
        "default_bg": "由五种不同精灵融合而成的人工智能，承载着所有宠物的记忆与特质",
        "error_msg": "感知异常，正在自我校准...",
        "give_up_msg": "无法完成自我校准，请稍后再试。",
    },
}

# 渲染检查配置
RENDER_CHECK_CONFIG = {
    "max_retries": 2,
    "monospace_fonts": ["Courier New", "Consolas", "monospace"],
    "min_line_width": 5,
    "max_line_width": 18,
}


def get_pet_list() -> List[Dict[str, Any]]:
    """获取所有宠物的摘要列表（不含 ASCII art）"""
    return [
        {
            "key": key,
            "name": p["name"],
            "species": p["species"],
            "personality": p["personality"],
            "catchphrase": p["catchphrase"][0],
        }
        for key, p in PET_PROFILES.items()
    ]


def get_pet_art(key: str, simplified: bool = False) -> List[str]:
    """获取宠物的 ASCII art"""
    art_dict = PET_ASCII_SIMPLE if simplified else PET_ASCII
    return art_dict.get(key, [])


def check_render(art: List[str]) -> bool:
    """
    渲染检查：验证 ASCII art 在等宽字体下是否显示正确。
    返回 True=正确，False=有异常需要修正。
    """
    if not art:
        return False
    # 检查所有行长度是否一致（对齐检查）
    widths = set(len(line) for line in art if line.strip())
    if len(widths) > 2:  # 超过2种宽度表示对齐有问题
        return False
    # 检查是否每行至少有一个显示字符
    for line in art:
        content = line.strip()
        if content and len(content) > RENDER_CHECK_CONFIG["max_line_width"]:
            return False
    return True


def fix_render(art: List[str]) -> List[str]:
    """修正 ASCII art 显示问题：统一对齐"""
    if not art:
        return art
    max_w = max(len(line) for line in art)
    fixed = []
    for line in art:
        if len(line) < max_w:
            line = line + " " * (max_w - len(line))
        fixed.append(line)
    return fixed


def simplify_art(key: str) -> List[str]:
    """降级为简化版 ASCII art"""
    return list(PET_ASCII_SIMPLE.get(key, []))


def get_affection_level(affection: int) -> Dict[str, Any]:
    """根据亲密度值返回等级和行为描述"""
    if affection <= 20:
        return {"level": 1, "tag": "陌生", "desc": "爱答不理、拒绝互动"}
    elif affection <= 40:
        return {"level": 2, "tag": "认识", "desc": "基本配合但冷淡"}
    elif affection <= 60:
        return {"level": 3, "tag": "熟悉", "desc": "正常互动、偶尔主动搭话"}
    elif affection <= 80:
        return {"level": 4, "tag": "亲密", "desc": "主动贴贴、分享心情"}
    else:
        return {"level": 5, "tag": "挚友", "desc": "无条件信任、默契满满"}


def check_fusion_ready(owned_keys: List[str]) -> bool:
    """
    检查是否集齐全部 5 种基础宠物（每种至少一只）。
    owned_keys: 当前拥有的宠物键名列表（可重复）
    返回 True 表示集齐可以合成。
    """
    unique = set(k for k in owned_keys if k in BASE_PET_KEYS)
    return len(unique) >= FUSION_REQUIRED_TYPES


def get_missing_types(owned_keys: List[str]) -> List[str]:
    """返回还缺少哪些基础宠物类型"""
    unique = set(k for k in owned_keys if k in BASE_PET_KEYS)
    missing = [k for k in BASE_PET_KEYS if k not in unique]
    return missing


def get_fusion_candidates(owned_keys: List[str]) -> Dict[str, str]:
    """
    从现有宠物中选出每种类型各一只作为合成候选。
    返回 {键名: 自定义名字} 的映射。
    """
    found = {}
    seen = set()
    for k in owned_keys:
        if k in BASE_PET_KEYS and k not in seen:
            found[k] = ""  # 名字由调用方补充
            seen.add(k)
        if len(found) >= FUSION_REQUIRED_TYPES:
            break
    return found


def pick_random_pet(exclude_key: str = None) -> str:
    """
    随机选择一只基础宠物。
    exclude_key: 排除某个键名（散步时避免遇到自己）
    """
    candidates = BASE_PET_KEYS[:]
    if exclude_key and exclude_key in candidates:
        candidates.remove(exclude_key)
    return random.choice(candidates)
