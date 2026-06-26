"""火15 带货视频 — 8 个预设角色模板

每个模板包含：
- character / action / scene  → 喂给 Seedance 的 prompt 三要素
- voice                       → edge-tts 音色（zh-CN-XxxNeural）
- voice_rate / voice_pitch    → 语速/音高微调
- bgm                         → 背景音乐风格关键字（匹配 ~/Music/huo15-bgm/{key}.mp3）
- bgm_volume                  → BGM 在最终混音中的音量（0~1，0.18~0.25 较合适）
- categories                  → 推荐品类，给 Agent 选模板时参考
"""

TEMPLATES = {
    "traditional_lady": {
        "label": "传统中年女性（默认）",
        "character": "一位身穿中式传统服饰的中年女性",
        "action": "面带微笑展示给镜头",
        "scene": "柔和暖色灯光，背景干净简约",
        "voice": "zh-CN-XiaoqiuNeural",
        "voice_rate": "-5%",
        "voice_pitch": "+0Hz",
        "bgm": "warm",
        "bgm_volume": 0.20,
        "categories": ["养生", "茶叶", "手工艺", "中式服饰", "古法食品"],
    },
    "fashion_host": {
        "label": "时尚女主播",
        "character": "一位妆容精致、穿着时尚连衣裙的年轻女主播",
        "action": "活力展示产品并打出爱心手势",
        "scene": "粉色直播间灯光，背景虚化彩色光斑",
        "voice": "zh-CN-XiaoxiaoNeural",
        "voice_rate": "+8%",
        "voice_pitch": "+2Hz",
        "bgm": "energetic",
        "bgm_volume": 0.22,
        "categories": ["美妆", "服装", "饰品", "潮玩", "数码配件"],
    },
    "tcm_doctor": {
        "label": "老中医",
        "character": "一位身穿白大褂、戴老花镜、白发白须的老中医",
        "action": "稳重展示产品并轻轻点头",
        "scene": "中药铺背景，木质药柜，暖黄灯光",
        "voice": "zh-CN-YunjianNeural",
        "voice_rate": "-10%",
        "voice_pitch": "-2Hz",
        "bgm": "asian",
        "bgm_volume": 0.18,
        "categories": ["中药", "保健品", "养生茶", "膏方", "艾灸"],
    },
    "kitchen_mom": {
        "label": "厨房主妇",
        "character": "一位系着碎花围裙、温柔亲切的中年妈妈",
        "action": "在厨房展示产品并露出满意笑容",
        "scene": "明亮温馨的家用厨房，自然光从窗户洒入",
        "voice": "zh-CN-XiaohanNeural",
        "voice_rate": "-2%",
        "voice_pitch": "+0Hz",
        "bgm": "warm",
        "bgm_volume": 0.20,
        "categories": ["调味料", "食材", "厨具", "零食", "速食"],
    },
    "beauty_blogger": {
        "label": "美妆博主",
        "character": "一位精致妆容、长卷发的时尚美妆博主",
        "action": "对着镜头展示产品并做出惊喜表情",
        "scene": "ins 风梳妆台，柔光环形灯，化妆品摆件",
        "voice": "zh-CN-XiaomengNeural",
        "voice_rate": "+5%",
        "voice_pitch": "+1Hz",
        "bgm": "soft",
        "bgm_volume": 0.22,
        "categories": ["护肤", "彩妆", "香水", "美容仪", "面膜"],
    },
    "fitness_coach": {
        "label": "健身教练",
        "character": "一位身材健硕、穿着运动背心的男性健身教练",
        "action": "充满力量感地举起产品",
        "scene": "现代健身房，深色调灯光，器械背景",
        "voice": "zh-CN-YunhaoNeural",
        "voice_rate": "+5%",
        "voice_pitch": "+0Hz",
        "bgm": "energetic",
        "bgm_volume": 0.25,
        "categories": ["蛋白粉", "运动器材", "健身服", "运动鞋", "补剂"],
    },
    "outdoor_explorer": {
        "label": "户外探店达人",
        "character": "一位戴着鸭舌帽、穿冲锋衣的年轻探店博主",
        "action": "在户外兴奋展示产品并比 OK 手势",
        "scene": "山野/古镇/集市等户外自然光场景",
        "voice": "zh-CN-YunxiaNeural",
        "voice_rate": "+10%",
        "voice_pitch": "+1Hz",
        "bgm": "cinematic",
        "bgm_volume": 0.20,
        "categories": ["地方特产", "户外装备", "零食", "饮品", "民俗工艺"],
    },
    "tech_geek": {
        "label": "数码博主",
        "character": "一位戴黑框眼镜、穿简约 T 恤的年轻数码博主",
        "action": "专业地展示产品细节并旋转产品",
        "scene": "极简白色桌面，柔光打在产品上，背景虚化",
        "voice": "zh-CN-YunyangNeural",
        "voice_rate": "+0%",
        "voice_pitch": "+0Hz",
        "bgm": "soft",
        "bgm_volume": 0.18,
        "categories": ["手机", "耳机", "数码周边", "智能家居", "电脑配件"],
    },
}

# BGM 关键字 → 风格描述（用于用户自备文件命名 / 在线检索关键词）
BGM_HINTS = {
    "warm":      "温暖治愈钢琴轻音乐 / warm piano background",
    "energetic": "活力电子节拍 / upbeat electronic groove",
    "asian":     "中国风古筝竹笛 / chinese traditional guzheng",
    "soft":      "柔和氛围背景音 / soft ambient",
    "cinematic": "电影感弦乐铺垫 / cinematic strings pad",
}


def list_templates():
    """返回所有模板的简表（给 Agent 选择用）"""
    return [
        {"key": k, "label": v["label"], "categories": v["categories"]}
        for k, v in TEMPLATES.items()
    ]


def get_template(key: str) -> dict:
    """取模板。未知 key 时回退到 traditional_lady"""
    return TEMPLATES.get(key, TEMPLATES["traditional_lady"])


def suggest_template(category_or_keyword: str) -> str:
    """按品类关键词推荐最合适的模板 key"""
    kw = category_or_keyword.strip().lower()
    for key, tpl in TEMPLATES.items():
        for cat in tpl["categories"]:
            if cat.lower() in kw or kw in cat.lower():
                return key
    return "traditional_lady"


if __name__ == "__main__":
    import json
    print(json.dumps(list_templates(), ensure_ascii=False, indent=2))
