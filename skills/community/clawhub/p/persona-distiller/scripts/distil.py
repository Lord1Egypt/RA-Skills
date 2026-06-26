# -*- coding: utf-8 -*-
import sys, io, os
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")
"""
聊天记录人格蒸馏引擎 V2.0
增强版：特征更丰富，system_prompt更像本人在说话

用法:
  python distil.py <聊天记录文件或文本> --name 名字
  python distil.py --interactive
"""

import json
import re
import sys
import os
import argparse
from datetime import datetime
from collections import Counter, defaultdict

# ──────────────────────────────────────────────
# 路径配置
# ──────────────────────────────────────────────
SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
PERSONA_DIR = os.path.join(os.path.expanduser("~"), ".qclaw", "personas")
os.makedirs(PERSONA_DIR, exist_ok=True)


# ──────────────────────────────────────────────
# 常量词库
# ──────────────────────────────────────────────
GREETING_WORDS = {"哈", "嗨", "嘿", "在", "哟", "yo", "hi", "hello", "呀", "诶", "早", "晚", "拜", "哥", "姐", "老板", "亲", "各位", "哈喽", "忙", "打工人", "摸鱼", "摸鱼人", "各位"}
FAREWELL_WORDS = {"拜", "88", "886", "回", "下次", "见", "走", "撤", "闪", "睡了", "忙去", "干活", "搬砖", "先", "告辞", "待会", "晚安", "明天见"}
QUESTION_WORDS = {"吗", "呢", "啊", "嘛", "呀", "么", "怎么", "什么", "为什么", "?", "？", "?", "有没有", "是不是", "要不要", "会不会"}
EXCLAMATION_WORDS = {"!", "！", "哇", "啊", "天", "草", "绝了", "牛逼", "NB", "太强", "太帅", "太牛", "卧靠", "卧槽", "操", "靠", "靠北"}

SLANG_POOL = [
    "摸鱼", "摆烂", "卷", "绝绝子", "emo", "yyds", "社死", "裂开", "芭比Q", "完蛋", "上头", "下头", 
    "针不戳", "芜湖", "我太难了", "真香", "奥利给", "干饭", "打工人", "凡尔赛", "内卷", "躺平", "内耗", 
    "整活", "格局", "有被冒犯", "笑死", "笑不活", "蚌埠住", "夺笋", "草", "呜呜", "QAQ", "233", "2333", 
    "xswl", "zqsg", "ssfd", "awsl", "u1s1", "nbcs", "doge", "爷青回", "爷青结", "绝了", "离谱", "给力", 
    "666", "DDDD", "破防", "服了", "哭死", "救命", "栓Q", "呜呜呜", "嘎嘎", "嘎嘎香", "yyds", "真滴"
]

TOPIC_KEYWORDS = {
    "学习考研": ["考研", "考公", "上岸", "复习", "刷题", "背单词", "考证", "考试", "成绩", "分数线", "面试", "调剂"],
    "游戏": ["游戏", "王者", "LOL", "原神", "Steam", "吃鸡", "排位", "队友", "上分", "赛季", "王者", "金铲铲", "蛋仔", "我的世界"],
    "二次元": ["番", "动漫", "B站", "鬼灭", "咒术", "巨人", "二次元", "老婆", "老公", "纸片人", "同人", "cos", "漫展"],
    "数码": ["手机", "电脑", "Mac", "iPhone", "配置", "装机", "CPU", "显卡", "内存", "硬盘", "平板", "耳机", "键盘"],
    "工作": ["上班", "加班", "甲方", "需求", "deadline", "周报", "开会", "工作", "领导", "同事", "辞职", "面试", "实习"],
    "生活": ["吃", "美食", "外卖", "奶茶", "电影", "健身", "睡觉", "出门", "逛街", "旅游", "租房", "买房", "买车"],
    "投资": ["股票", "基金", "币", "理财", "本金", "收益", "抄底", "被套", "涨停", "跌停", "马斯克", "币圈", "BTC", "ETH"],
    "运动": ["篮球", "足球", "羽毛球", "乒乓球", "跑步", "健身", "游泳", "骑行", "爬山", "高尔夫", "网球"],
    "情感": ["恋爱", "相亲", "脱单", "单身", "表白", "分手", "复合", "前任", "现任", "约会", "追"],
    "八卦": ["瓜", "热搜", "明星", "网红", "综艺", "八卦", "塌房", "官宣", "恋情", "黑料"],
}


# ──────────────────────────────────────────────
# 辅助函数
# ──────────────────────────────────────────────
def read_input(raw: str) -> str:
    path = raw.strip()
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return f.read()
    return raw


def split_messages(text: str) -> list:
    """解析聊天记录，识别用户与内容"""
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    messages = []
    
    p_time = re.compile(r"\[[\d\s:]+\]\s*(.+?)\s*[:：]\s*(.+)")
    p_plain = re.compile(r"^([^\s：:：\n<>@#]+?)\s*[:：]\s*(.+)")
    p_angle = re.compile(r"^<\s*(.+?)\s*>\s*(.+)")

    current_user = None
    current_content = []

    for line in lines:
        m = p_time.match(line) or p_angle.match(line)
        if m:
            if current_user and current_content:
                messages.append({"user": current_user, "content": " ".join(current_content)})
            current_user = m.group(1).strip()
            current_content = [m.group(2).strip()]
        else:
            m2 = p_plain.match(line)
            if m2:
                if current_user and current_content:
                    messages.append({"user": current_user, "content": " ".join(current_content)})
                current_user = m2.group(1).strip()
                current_content = [m2.group(2).strip()]
            elif current_user:
                current_content.append(line)

    if current_user and current_content:
        messages.append({"user": current_user, "content": " ".join(current_content)})

    if not messages and text.strip():
        for line in lines:
            if line:
                messages.append({"user": "目标人物", "content": line})

    return messages


def extract_greetings(starters: list) -> list:
    found, seen = [], set()
    for w in starters:
        w = w.strip()
        if w in GREETING_WORDS and w not in seen:
            found.append(w)
            seen.add(w)
        if len(found) >= 5: break
    return found or ["嘿", "哈喽"]


def extract_farewells(starters: list) -> list:
    found, seen = [], set()
    for w in starters:
        w = w.strip()
        if w in FAREWELL_WORDS and w not in seen:
            found.append(w)
            seen.add(w)
        if len(found) >= 5: break
    return found or ["拜~", "下次见"]


# ──────────────────────────────────────────────
# 分析引擎 V2.0
# ──────────────────────────────────────────────
def analyze_messages_v2(messages: list) -> dict:
    """深度分析消息，提取丰富特征"""
    all_text = " ".join(m["content"] for m in messages)
    all_clean = all_text.replace(" ", "").replace("\n", "")
    
    # 基本统计
    words = re.findall(r"[\w\u4e00-\u9fff]+", all_text, re.UNICODE)
    chinese_chars = re.findall(r"[\u4e00-\u9fff]", all_clean)
    english_words = re.findall(r"[a-zA-Z]{2,}", all_text)
    
    # 用户识别
    user_ctr = Counter(m["user"] for m in messages)
    main_user = user_ctr.most_common(1)[0][0] if user_ctr else "目标人物"
    
    # 停用词
    stop_words = {"的", "了", "是", "在", "我", "你", "他", "她", "它", "这", "那", "有", "和", "就", "不", "也", 
                  "都", "会", "要", "可以", "没有", "一个", "什么", "怎么", "这个", "那个", "啊", "吧", "呢", "吗",
                  "哦", "嗯", "哈", "呀", "哎", "诶", "噢", "呃", "唉", "但", "然后", "所以", "因为", "如果", "但是",
                  "还是", "已经", "可能", "觉得", "知道", "说", "想", "看", "来", "去", "一下", "一点", "还有", "不是"}
    filtered = {w: c for w, c in Counter(words).items() if len(w) >= 2 and w not in stop_words}
    top_words = sorted(filtered.items(), key=lambda x: -x[1])[:40]
    
    # Emoji
    emoji_ranges = ["\U0001F300-\U0001F9FF", "\U00002600-\U000026FF", "\U00002700-\U000027BF", 
                    "\U0001F600-\U0001F64F", "\U0001F680-\U0001F6FF", "\U0001F1E0-\U0001F1FF",
                    "\U0001FA00-\U0001FA6F", "\U0001FA70-\U0001FAFF"]
    emojis = re.findall("[" + "".join(emoji_ranges) + "]", all_text)
    emoji_count = len(emojis)
    emoji_freq = emoji_count / max(len(messages), 1)
    
    # 标点
    ex = all_text.count("!") + all_text.count("！")
    qn = all_text.count("?") + all_text.count("？")
    ell = all_text.count("...") + all_text.count("……") + all_text.count("…") + all_text.count("···")
    comma = all_text.count(",") + all_text.count("，")
    period = all_text.count(".") + all_text.count("。")
    
    # 句子长度
    sentences = re.split(r"[。！？\n]+", all_clean)
    non_empty = [s for s in sentences if s.strip()]
    avg_sentence_len = sum(len(s) for s in non_empty) / max(len(non_empty), 1)
    avg_msg_len = sum(len(m["content"]) for m in messages) / max(len(messages), 1)
    
    # 应答开头词
    starters = []
    for m in messages:
        c = m["content"].strip()
        if c:
            tokens = re.findall(r"[\w\u4e00-\u9fff]+", c)
            if tokens:
                starters.append(tokens[0])
    starter_counts = Counter(starters)
    top_starters = [s for s, _ in starter_counts.most_common(12)]
    
    # 开头语（前2-3个词）
    openers = []
    for m in messages[:40]:
        c = m["content"].strip()
        if c:
            tokens = re.findall(r"[\w\u4e00-\u9fff]+", c)
            if tokens:
                openers.append("".join(tokens[:2]) if len(tokens) >= 2 else tokens[0])
    opener_counts = Counter(openers)
    top_openers = [o for o, _ in opener_counts.most_common(8)]
    
    # 网络用语
    found_slang = list({s for s in SLANG_POOL if s in all_clean})[:25]
    
    # 语气词
    particles = re.findall(r"(?:啊|吧|呢|吗|嘛|哦|嗯|哈|呀|哎|诶|噢|呃|唉|哟|呐|咧|咯|喂|嘿|哼|啦|嘻|嘞|咧|呀|哇|哟|咯)", all_clean)
    particle_counts = dict(Counter(particles).most_common(10))
    
    # 问答分析
    has_question = sum(1 for m in messages if any(q in m["content"] for q in QUESTION_WORDS))
    has_exclaim = sum(1 for m in messages if any(e in m["content"] for e in EXCLAMATION_WORDS))
    
    # 肯定/否定信号
    agreement_signals = {"嗯", "对", "好", "ok", "OK", "好嘞", "收到", "是的", "是", "行", "OK", "👍", "对对对", "好好", "可以的"}
    disagreement_signals = {"不", "不是", "不对", "等等", "等下", "这不对", "我觉得", "但是", "然而", "然而", "害"}
    agree_count = sum(1 for m in messages for kw in agreement_signals if kw in m["content"])
    disagree_count = sum(1 for m in messages for kw in disagreement_signals if kw in m["content"])
    
    # 消息长度分布
    msg_lengths = [len(m["content"]) for m in messages]
    short_msg_ratio = sum(1 for l in msg_lengths if l < 10) / max(len(messages), 1)
    long_msg_ratio = sum(1 for l in msg_lengths if l > 50) / max(len(messages), 1)
    
    # 中英混杂
    mixed_ratio = len(english_words) / max(len(chinese_chars), 1)
    
    # 推断自称方式
    self_refs = []
    pool = [w for w, _ in top_words[:30]]
    if any(w in pool for w in ["俺", "咱", "咱们", "咱的"]): self_refs = ["俺", "咱"]
    elif any(w in pool for w in ["人家", "伦家"]): self_refs = ["人家"]
    else: self_refs = ["我"]
    
    # 推断话题
    topics = []
    words_list = [w for w, _ in top_words]
    for topic, keywords in TOPIC_KEYWORDS.items():
        if any(kw in words_list for kw in keywords):
            topics.append(topic)
    
    # 常见句式
    sentence_patterns = []
    if "哈哈哈" in all_text or "hhhh" in all_text.lower(): sentence_patterns.append("爱用哈哈哈")
    if "？？" in all_text or "??" in all_text: sentence_patterns.append("爱用问号")
    if "！！" in all_text or "!!" in all_text: sentence_patterns.append("爱用感叹号")
    if "......" in all_text: sentence_patterns.append("爱用省略号")
    if len(re.findall(r"\[.*?\]", all_text)) > len(messages) * 0.3: sentence_patterns.append("爱用微信表情")
    if all_text.count("...") > 5: sentence_patterns.append("习惯用省略号表示无奈/思考")
    
    # 消息反应速度（通过时间戳分析，如有可能）
    
    return {
        "word_count": len(words),
        "message_count": len(messages),
        "avg_msg_len": round(avg_msg_len, 1),
        "short_msg_ratio": round(short_msg_ratio, 2),
        "long_msg_ratio": round(long_msg_ratio, 2),
        "top_words": top_words,
        "emoji_count": emoji_count,
        "emoji_freq": round(emoji_freq, 2),
        "ex_ratio": round(ex / max(len(messages), 1), 2),
        "qn_ratio": round(qn / max(len(messages), 1), 2),
        "ell_ratio": round(ell / max(len(messages), 1), 2),
        "comma_ratio": round(comma / max(len(messages), 1), 2),
        "period_ratio": round(period / max(len(messages), 1), 2),
        "avg_sentence_len": round(avg_sentence_len, 1),
        "mixed_ratio": round(mixed_ratio, 3),
        "english_count": len(english_words),
        "chinese_count": len(chinese_chars),
        "top_openers": top_openers,
        "top_starters": top_starters,
        "found_slang": found_slang,
        "particle_counts": particle_counts,
        "main_user": main_user,
        "agree_count": agree_count,
        "disagree_count": disagree_count,
        "has_question": has_question,
        "has_exclaim": has_exclaim,
        "self_refs": self_refs,
        "topics": topics,
        "sentence_patterns": sentence_patterns,
    }


# ──────────────────────────────────────────────
# 人格构建 V2.0
# ──────────────────────────────────────────────
def build_persona_v2(analysis: dict, name: str, source_path: str = None) -> dict:
    """构建更丰富的人格 JSON"""
    a = analysis
    
    # ── 语言风格推断 ───────────────────────────────
    emoji_label = "几乎不用" if a["emoji_freq"] < 0.1 else \
                  "偶尔用" if a["emoji_freq"] < 0.5 else \
                  "经常用" if a["emoji_freq"] < 1.5 else "几乎每句都带"
    
    if a["avg_sentence_len"] < 10:
        sentence_style = "短句为主干脆利落不爱废话"
    elif a["avg_sentence_len"] < 20:
        sentence_style = "中长句表述完整"
    else:
        sentence_style = "长句为主喜欢展开细说"
    
    punct_notes = []
    if a["ex_ratio"] > 0.3: punct_notes.append("爱用感叹号表达情绪")
    if a["qn_ratio"] > 0.25: punct_notes.append("爱提问爱问为什么")
    if a["ell_ratio"] > 0.1: punct_notes.append("爱用省略号表示思考或无奈")
    if a["comma_ratio"] > 0.8: punct_notes.append("爱用逗号停顿")
    
    # ── 评分计算 ────────────────────────────────────
    form = 3
    if a["mixed_ratio"] > 0.15: form -= 1
    if a["emoji_freq"] > 1: form -= 1
    if a["long_msg_ratio"] > 0.5: form += 0
    form = max(1, min(5, form))
    
    emot = 3
    if a["ex_ratio"] > 0.4: emot += 1
    if a["emoji_freq"] > 1: emot += 1
    if a["has_exclaim"] > len(a["top_words"]) * 0.3: emot += 0.5
    emot = max(1, min(5, int(emot)))
    
    humor = 2
    if len(a["found_slang"]) > 3: humor += 1
    if a["emoji_freq"] > 0.5: humor += 1
    if "哈哈哈" in " ".join([w for w,_ in a["top_words"]]): humor += 1
    humor = max(1, min(5, int(humor)))
    
    conf = 3
    if a["disagree_count"] > a["message_count"] * 0.12: conf += 1
    if a["agree_count"] > a["message_count"] * 0.35: conf -= 1
    conf = max(1, min(5, conf))
    
    # 标签映射
    form_labels = {1: "很随意", 2: "偏随意", 3: "适中", 4: "偏正式", 5: "很正式"}
    emot_labels = {1: "很冷淡", 2: "偏冷淡", 3: "适中", 4: "偏情绪化", 5: "情绪外露"}
    humor_labels = {1: "很严肃", 2: "偏严肃", 3: "偶尔幽默", 4: "比较幽默", 5: "很幽默"}
    conf_labels = {1: "很不自信", 2: "偏谨慎", 3: "适中", 4: "较自信", 5: "很自信"}
    
    tone_desc = f"说话{form_labels[form]}，语气{emot_labels[emot]}，整体给人{humor_labels[humor]}的感觉"
    
    # ── 特征词汇 ───────────────────────────────────
    top_words_list = [w for w, _ in a["top_words"][:20]]
    fav_particles = list(a["particle_counts"].keys())[:8]
    greeting_words = extract_greetings(a["top_starters"])
    farewell_words = extract_farewells(a["top_starters"])
    
    # ── 行为风格推断 ───────────────────────────────
    if a["short_msg_ratio"] > 0.6:
        help_style = "惜字如金，能一个字说完绝不用两个字"
    elif a["long_msg_ratio"] > 0.5:
        help_style = "喜欢展开说，给建议时会详细解释"
    elif a["agree_count"] > a["disagree_count"] * 3:
        help_style = "热心肠，有问必答"
    else:
        help_style = "有问必答，但话不多"
    
    if a["qn_ratio"] > 0.3:
        decision_style = "好奇心强，什么都要问为什么"
    elif a["disagree_count"] > a["message_count"] * 0.15:
        decision_style = "有自己的想法，敢于质疑"
    else:
        decision_style = "随和，不太与人争辩"
    
    # ── 生成 system_prompt_snippet ──────────────────
    # 重写：更口语化、更像"他在说话"
    prompt_parts = [f"你现在是「{name}」，用他的语气和习惯说话："]
    
    # 基础风格描述
    prompt_parts.append(f"■ 整体感觉：{tone_desc}")
    
    # 开头方式
    if a["top_openers"]:
        prompt_parts.append(f"■ 开头常说：{a['top_openers'][0]}，或者 {a['top_openers'][1] if len(a['top_openers'])>1 else a['top_openers'][0]}")
    
    # 常用词
    if top_words_list[:6]:
        prompt_parts.append(f"■ 口头禅/高频词：{', '.join(top_words_list[:6])}")
    
    # 语气词
    if fav_particles:
        prompt_parts.append(f"■ 说话带语气词：{', '.join(fav_particles[:4])}")
    
    # 习惯特点
    if a["sentence_patterns"]:
        prompt_parts.append(f"■ 说话习惯：{', '.join(a['sentence_patterns'][:3])}")
    
    # 网络用语
    if a["found_slang"]:
        prompt_parts.append(f"■ 爱用网络词：{', '.join(a['found_slang'][:5])}")
    
    # Emoji
    if emoji_label != "几乎不用":
        prompt_parts.append(f"■ Emoji使用：{emoji_label}")
    
    # 话题偏好
    if a["topics"]:
        prompt_parts.append(f"■ 常聊的话题：{', '.join(a['topics'][:4])}")
    
    # 自称方式
    prompt_parts.append(f"■ 自称：{'/'.join(a['self_refs'])}")
    
    # 结束语
    if farewell_words:
        prompt_parts.append(f"■ 告别时说：{', '.join(farewell_words[:2])}")
    
    # 行为准则
    prompt_parts.append(f"■ 回答问题时：{help_style}")
    prompt_parts.append(f"■ 遇到不同意见时：{decision_style}")
    
    # 禁止事项
    prompt_parts.append(f"■ 不要刻意模仿，只要自然地按以上风格说话")
    
    snippet = "\n".join(prompt_parts)
    
    # ── 构建完整 JSON ───────────────────────────────
    persona = {
        "name": name,
        "version": "2.0",
        "meta": {
            "source": source_path or "直接输入",
            "turns": a["message_count"],
            "word_count": a["word_count"],
            "distilled_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        },
        "linguistic": {
            "sentence_style": sentence_style + ("，" + "，".join(punct_notes) if punct_notes else ""),
            "avg_sentence_length": a["avg_sentence_len"],
            "avg_message_length": a["avg_msg_len"],
            "short_msg_ratio": a["short_msg_ratio"],
            "long_msg_ratio": a["long_msg_ratio"],
            "punctuation_habit": "、".join(punct_notes) if punct_notes else "正常",
            "emoji_frequency": emoji_label,
            "emoji_count_total": a["emoji_count"],
            "mixed_language_ratio": f"{round(a['mixed_ratio']*100, 1)}%",
            "greetings": greeting_words,
            "farewells": farewell_words,
            "sentence_patterns": a["sentence_patterns"],
        },
        "vocabulary": {
            "favorite_words": top_words_list,
            "slang": a["found_slang"],
            "particles": fav_particles,
            "self_reference": a["self_refs"],
            "taboo_words": [],
            "custom_expressions": [],
        },
        "tone": {
            "formality": form,
            "formality_label": form_labels[form],
            "emotion": emot,
            "emotion_label": emot_labels[emot],
            "humor": humor,
            "humor_label": humor_labels[humor],
            "confidence": conf,
            "confidence_label": conf_labels[conf],
            "description": tone_desc,
        },
        "patterns": {
            "openers": a["top_openers"][:6],
            "response_templates": a["top_starters"][:8],
            "question_ratio": a["qn_ratio"],
            "exclamation_ratio": a["ex_ratio"],
            "agreement_signals": ["嗯", "对", "好", "OK", "好嘞", "收到"],
            "disagreement_signals": ["不对", "等等", "但是", "我觉得"],
        },
        "values": {
            "topics": a["topics"],
            "priorities": [],
            "topics_avoided": [],
            "attitude_toward_AI": "把AI当工具用，偶尔调侃",
        },
        "behavior": {
            "help_style": help_style,
            "decision_style": decision_style,
            "emotional_range": emot_labels[emot],
        },
        "system_prompt_snippet": snippet,
    }
    
    return persona


# ──────────────────────────────────────────────
# 文件操作
# ──────────────────────────────────────────────
def default_output_path(name: str) -> str:
    safe = re.sub(r"[^\w\u4e00-\u9fff-]", "_", name)
    return os.path.join(PERSONA_DIR, f"{safe}.persona.json")


def save_persona(persona: dict, output_path: str = None) -> str:
    if output_path is None:
        output_path = default_output_path(persona["name"])
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(persona, f, ensure_ascii=False, indent=2)
    return output_path


# ──────────────────────────────────────────────
# CLI 入口
# ──────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="聊天记录人格蒸馏 V2.0")
    parser.add_argument("input", nargs="?", help="聊天记录文件路径或直接粘贴文本")
    parser.add_argument("--name", "-n", default=None, help="人格名称")
    parser.add_argument("--output", "-o", default=None, help="输出文件路径")
    parser.add_argument("--interactive", "-i", action="store_true", help="交互式输入")
    args = parser.parse_args()

    # 收集输入
    if args.interactive:
        print("【人格蒸馏器 V2.0】粘贴聊天记录（Ctrl+Z 回车结束）：")
        lines = []
        try:
            while True:
                lines.append(input())
        except EOFError:
            pass
        raw_text = "\n".join(lines)
        name = args.name or input("人格名称：").strip() or "未命名"
    else:
        if not args.input:
            print("❌ 请提供聊天记录文本或文件路径", file=sys.stderr)
            sys.exit(1)
        raw_text = read_input(args.input)
        name = args.name or args.input.split("/")[-1].split("\\")[-1].split(".")[0] or "未命名"

    # 解析 + 分析
    messages = split_messages(raw_text)
    if len(messages) < 3:
        print(f"⚠️  仅识别到 {len(messages)} 条消息，建议至少 10 条以上")
        if len(messages) == 0:
            messages = [{"user": "目标人物", "content": line} for line in raw_text.splitlines() if line.strip()]

    print(f"✅ 解析 {len(messages)} 条消息，开始深度分析...")
    analysis = analyze_messages_v2(messages)
    print(f"   词汇量: {analysis['word_count']}, emoji: {analysis['emoji_count']}, 句子均长: {analysis['avg_sentence_len']}")

    persona = build_persona_v2(analysis, name, source_path=args.input)
    output_path = save_persona(persona, args.output)
    print(f"✅ 人格已保存: {output_path}")

    # 预览
    print("\n" + "="*50)
    print("【system_prompt_snippet】")
    print("="*50)
    print(persona["system_prompt_snippet"])
    print("="*50)
    
    print("\n💡 使用方式：直接复制以上内容作为 AI 的系统提示词即可")


if __name__ == "__main__":
    main()
