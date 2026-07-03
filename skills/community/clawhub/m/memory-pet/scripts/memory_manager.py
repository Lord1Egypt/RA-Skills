"""
memory_manager.py — memory-pet 记忆格式化与关键词提取

注意：所有数据持久化管理已迁移到 pet_manager.py CLI。
本文件仅保留记忆格式化、关键词提取等纯展示函数。
"""

import re
from typing import Dict, List, Optional


# 最大关键词数量
MAX_KEYWORDS = 15


def extract_keywords(text: str, existing_keywords: Optional[List[str]] = None) -> List[str]:
    """
    从文本中提取 ≤15 个关键词。
    """
    if not text:
        return []

    words = set()
    cn_words = re.findall(r"[\u4e00-\u9fff]{2,6}", text)
    words.update(cn_words)
    en_words = re.findall(r"\b[a-zA-Z]{2,}\b", text)
    words.update(w.lower() for w in en_words)

    stop_words = {"这个", "那个", "什么", "怎么", "一个", "可以", "没有", "不是",
                  "因为", "所以", "但是", "如果", "虽然", "而且", "然后", "这样"}
    words = words - stop_words

    if existing_keywords:
        words = words - set(existing_keywords)

    result = list(words)
    result = result[:MAX_KEYWORDS]
    result.sort()
    return result


def format_memory_for_recall(
    memory: Dict,
    personality_tag: str,
    pet_custom_name: str,
) -> str:
    """
    根据宠物性格格式化记忆为回忆口吻。
    personality_tag: pro(稳重)/act(活泼)/gen(温柔)/log(冷静)/agg(暴躁)/ai(超然)
    """
    ts = memory.get("timestamp", "某时")
    mtype = memory.get("type", "other")
    food = memory.get("food", "")
    taste = memory.get("taste", "")

    prefixes = {
        "pro": f"嗯，让我想想。{ts}的时候，",
        "act": f"哇！我想起来了！！{ts}——",
        "gen": f"那个…好像是{ts}…",
        "log": f"记录检索：{ts}，",
        "agg": f"啧，{ts}是吧，",
        "ai": f"分析完毕。{ts}，",
    }

    suffixes = {
        "eat_pro": f"你带了{pet_custom_name}去吃{food}，味道{'不错' if taste in ['好极了','好吃'] else '还行吧'}。",
        "eat_act": f"你喂我吃了{food}！！真的太好吃啦！！记得记得！！",
        "eat_gen": f"你给了我{food}…很好吃…谢谢你…",
        "eat_log": f"摄入{food}，味道评价：{taste or '未记录'}。",
        "eat_agg": f"那{food}{'还挺带劲' if taste in ['好极了','好吃'] else '就那样吧'}，不过我不说你也该知道。",
        "eat_ai": f"记录到一次进食事件：{food}。味道评级：{taste or '未评级'}。",
        "walk_pro": f"带着{pet_custom_name}出去走了走，路上挺安静。",
        "walk_act": f"出去疯跑了一圈！！好爽！！",
        "walk_gen": f"出门散步了…虽然有点害怕…但有你在…",
        "walk_log": f"外出活动一次，路线未记录。",
        "walk_agg": f"被你拖出去走了走……烦死了……",
        "walk_ai": f"完成一次户外活动。环境数据未记录。",
        "cuddle_pro": f"你轻轻靠了过来，{pet_custom_name}没有躲开。",
        "cuddle_act": "你非要抱我！哼！",
        "cuddle_gen": "你抱了我…很温暖…",
        "cuddle_log": "肢体接触记录一次。",
        "cuddle_agg": "你贴过来的时候我其实……咳，没什么。",
        "cuddle_ai": "检测到一次亲密接触。情感分析：正面。",
        "decay_pro": f"有段时间没来看{pet_custom_name}了，他有点失落。",
        "decay_act": "好久没来找我玩了！！我都快长蘑菇了！！",
        "decay_gen": "你很久没来了…我以为你不要我了…",
        "decay_log": "活跃间隔超标，亲密度自动衰减。",
        "decay_agg": "呵，还记得回来呢？",
        "decay_ai": "活跃间隔超阈值，亲密度执行自动衰减。",
    }

    prefix = prefixes.get(personality_tag, "")
    suffix_key = f"{mtype}_{personality_tag}"
    suffix = suffixes.get(suffix_key, f"和{pet_custom_name}一起度过了一段时光。")

    return prefix + suffix
