#!/usr/bin/env python3
"""
TTS 文本预处理模块
根据语境自动判断情绪，并在文本中插入语气词标签和停顿标记
"""

import re


# 情绪关键词映射
EMOTION_KEYWORDS = {
    "happy": ["开心", "高兴", "太好了", "哈哈", "笑死", "太棒了", "嘿嘿", "嘻嘻", "哇", "哇塞", "真好", "喜欢", "爱你", "么么哒"],
    "sad": ["伤心", "难过", "遗憾", "可惜", "算了", "唉", "叹气", "沮丧", "失落", "委屈", "郁闷"],
    "angry": ["生气", "气死", "讨厌", "烦死了", "可恶", "气死我了", "哼", "哼唧"],
    "fearful": ["害怕", "担心", "恐惧", "恐怖", "吓人"],
    "disgusted": ["恶心", "厌恶", "吐了", "受不了"],
    "surprised": ["惊讶", "吃惊", "没想到", "哇", "天哪", "不会吧", "真的吗", "什么", "怎么", "为什么"],
    "calm": ["平静", "淡定", "冷静", "好吧", "嗯", "了解", "明白"],
    "fluent": ["那个", "然后", "接着", "其实"],
    "whisper": ["悄悄", "低声", "小声"],
}

# 语气词音效配置（按优先级）
SOUND_EFFECTS = [
    # 笑声 - 优先匹配长版本
    ("laughs", ["哈哈哈哈", "哈哈哈", "笑死", "嘿嘿嘿", "嘻嘻嘻", "呵呵呵"]),
    ("chuckle", ["嘿嘿", "嘻嘻", "咯咯"]),
    # 惊讶/感叹 - 句首
    ("gasps", ["哇塞", "天哪", "我靠", "我嚓", "不会吧", "真的吗"]),
    ("sighs", ["唉", "哎", "唉声叹气"]),
    # 单字语气词
    ("gasps", ["哇", "哎呀", "哎哟"]),
    # 思考
    ("clear-throat", ["嗯"]),
    # 软萌
    ("humming", ["么么哒", "嗯嗯", "好嘛", "好啦"]),
]


def detect_emotion(text: str) -> str | None:
    """
    根据文本关键词判断情绪
    返回情绪名称，或 None 表示使用默认
    """
    text_lower = text.lower()
    scores = {}
    
    for emotion, keywords in EMOTION_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in text_lower)
        if score > 0:
            scores[emotion] = score
    
    # 问号密度加权：问号多则倾向于 surprised
    question_count = text.count('？') + text.count('?')
    if question_count >= 2:
        scores['surprised'] = scores.get('surprised', 0) + question_count
    
    if not scores:
        return None
    
    # 返回得分最高的情绪
    return max(scores, key=scores.get)


def insert_single_sound(text: str) -> str:
    """
    插入单个语气词音效（避免重复插入）
    笑声插后面，语气词插前面
    如果文本中已有笑声词（如"哈哈哈"），不再插入laughs标签
    """
    # 笑声词列表
    laugh_words = ["哈哈", "嘿嘿", "嘻嘻", "呵呵", "嘎嘎", "笑死", "咯咯"]
    has_laugh = any(lw in text for lw in laugh_words)
    
    for sound_name, keywords in SOUND_EFFECTS:
        sound_tag = f"({sound_name})"
        if sound_tag in text:
            continue
        
        # 如果文本中已有笑声词，跳过laughs标签插入
        if sound_name == "laughs" and has_laugh:
            continue
            
        for kw in keywords:
            if kw not in text:
                continue
            
            idx = text.find(kw)
            
            if sound_name in ["laughs", "chuckle"]:
                # 笑声：插在关键词后面
                insert_pos = idx + len(kw)
                # 跳过标点
                while insert_pos < len(text) and text[insert_pos] in '，、。？！…… ,.：:':
                    insert_pos += 1
                # 避免插在句子中间（只在后半句或句尾）
                before_kw = idx
                after_content = text[insert_pos:].strip()
                if before_kw > 15 and not after_content.endswith(('。', '！', '？')) and after_content and '，' in after_content:
                    # 前半句，在最后一个逗号后插入
                    last_comma = after_content.rfind('，')
                    if last_comma > 0:
                        actual_pos = insert_pos + last_comma + 1
                        text = text[:actual_pos] + " " + sound_tag + text[actual_pos:]
                        return text
                # 否则直接在关键词后插入
                text = text[:insert_pos] + " " + sound_tag + text[insert_pos:]
                return text
            else:
                # 语气词：插在关键词前面
                text = text[:idx] + sound_tag + " " + text[idx:]
                return text
    
    return text


def insert_pause_markers(text: str) -> str:
    """
    在合适的位置插入停顿标记
    """
    patterns = [
        (r'，', '<#0.3#>'),
        (r'。', '<#0.5#>'),
        (r'？', '<#0.5#>'),
        (r'！', '<#0.5#>'),
        (r'…', '<#0.4#>'),
    ]
    
    result = text
    for pattern, marker in patterns:
        if marker not in result:
            result = re.sub(pattern, rf'{pattern}{marker}', result)
    
    return result


def preprocess_for_tts(text: str) -> dict:
    """
    完整的 TTS 文本预处理
    """
    # 1. 检测情绪
    emotion = detect_emotion(text)
    
    # 2. 插入单个语气词音效
    processed_text = insert_single_sound(text)
    
    # 3. 插入停顿标记
    processed_text = insert_pause_markers(processed_text)
    
    return {
        "text": processed_text,
        "emotion": emotion or "happy"
    }


def format_tts_payload(text: str, emotion: str = None) -> dict:
    """
    构造完整的 TTS API payload
    """
    processed = preprocess_for_tts(text)
    
    payload = {
        "model": "speech-2.8-hd",
        "text": processed["text"],
        "stream": False,
        "voice_setting": {
            "voice_id": "Chinese (Mandarin)_Gentle_Senior",
            "speed": 1.0,
            "vol": 1.0,
            "pitch": 0,
            "emotion": emotion or processed["emotion"]
        },
        "audio_setting": {
            "sample_rate": 16000,
            "format": "wav",
            "channel": 1
        },
        "subtitle_enable": False
    }
    
    return payload


if __name__ == "__main__":
    # 测试
    test_texts = [
        "你好想总，我是Miss M",
        "真的吗？太好了！哈哈哈！",
        "唉，这个有点难过了",
        "你讨厌啦，哼！",
        "哇，这也太厉害了吧！",
        "不会吧，还有这种操作？",
    ]
    
    for t in test_texts:
        result = preprocess_for_tts(t)
        print(f"原文: {t}")
        print(f"处理后: {result['text']}")
        print(f"情绪: {result['emotion']}")
        print()
