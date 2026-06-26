"""家族共享默认参数与模型 ID.

基于 2026-04 实测火山方舟/Kling/Suno 文档核对。
"""

DEFAULTS = {
    "duration_total": 240,          # 秒，3-5 分钟区间默认 4 分钟
    "scene_duration": 5,            # 单镜头秒数（Seedance 2.0 支持 4-15）
    "ratio": "9:16",                # 竖屏；Seedance 2.0 支持 9:16/16:9/4:3/3:4/21:9/1:1/adaptive
    "resolution": "720p",           # 默认 720p 省钱；可选 480p/720p/1080p/2K
    "style": "三渲二国风",
    "genre": "仙侠",
    "cost_cap": 600.0,
    "cost_warn_ratio": 0.7,
    "cost_hard_ratio": 1.0,
    "watermark": False,
    "concurrency": 3,
    "scene_retry": 2,
    "fast_mode": False,             # True 用 seedance-fast（便宜但质量低）
}

MODELS = {
    "script":  "claude-opus-4-7",
    "image":   "doubao-seedream-4-0-250828",                # 方舟 Seedream 4.0
    "video":   "doubao-seedance-2-0-260128",                # 方舟 Seedance 2.0 标准版
    "video_fast": "doubao-seedance-2-0-fast-260128",        # 方舟 Seedance 2.0 fast
    "tts":     "doubao-tts-bigtts",                         # 方舟豆包大模型 TTS
    "lipsync": "kling-v2.6",                                # Kling 2.6 原生对口型
    "music":   "suno-v5.5",                                 # Suno v5.5（via sunoapi.org）
}

# API 端点（2026-04 核对）
ENDPOINTS = {
    "ark_base":      "https://ark.cn-beijing.volces.com/api/v3",
    "kling_base":    "https://api.klingai.com/v1",         # 官方；第三方 piapi.ai/fal.ai 亦可
    "suno_base":     "https://api.sunoapi.org",             # 第三方（Suno 无公开官方 API）
}

# 单位价（元），2026-04 核对
# Seedance 2.0: token-based 46¥/M tokens（1080p 文生/图生视频），28¥/M tokens（视频参考）
# 按秒估算的便利值：token = duration × width × height × fps / 1024，用 token × 46 / 1e6 得元价
PRICING = {
    "image_per_pic":        0.08,    # Seedream 4.0 每张
    "video_480p_per_sec":   0.50,    # 480p 9:16 ≈ 5s ¥2.5
    "video_720p_per_sec":   0.994,   # 720p 9:16 ≈ 5s ¥5
    "video_1080p_per_sec":  2.26,    # 1080p 9:16 ≈ 5s ¥11.3
    "video_fast_discount":  0.5,     # fast 模型约 5 折
    "video_per_mtoken":     46.0,    # 官方 token 单价（M tokens）
    "tts_per_char":         0.0008,  # 豆包大模型 TTS
    "lipsync_per_5s":       0.72,    # Kling 官方 $0.1/5s ≈ ¥0.72
    "bgm_per_track":        3.0,     # sunoapi.org 第三方均价
}


def video_unit_price(resolution: str = "720p", fast: bool = False) -> float:
    """返回每秒元价，用于预估."""
    base = {
        "480p":  PRICING["video_480p_per_sec"],
        "720p":  PRICING["video_720p_per_sec"],
        "1080p": PRICING["video_1080p_per_sec"],
        "2K":    PRICING["video_1080p_per_sec"] * 1.5,
    }.get(resolution, PRICING["video_720p_per_sec"])
    if fast:
        base *= PRICING["video_fast_discount"]
    return base


# 国风专用提示词片段
STYLE_PRESETS = {
    "三渲二国风": {
        "prefix": "三渲二国风动画风格，工笔线条，中国传统审美",
        "lighting": "柔和自然光，水墨晕染",
        "palette": "青绿山水色调，朱砂点缀",
    },
    "水墨": {
        "prefix": "中国水墨画风格，留白意境",
        "lighting": "墨色浓淡",
        "palette": "黑白灰为主，偶尔赭石",
    },
    "古风赛璐璐": {
        "prefix": "日式赛璐璐+中国古风融合，清新明亮",
        "lighting": "柔光晴天",
        "palette": "淡雅国风配色",
    },
    "工笔": {
        "prefix": "中国工笔画风格，细腻线条，重彩渲染",
        "lighting": "平光",
        "palette": "矿物颜料，金线勾勒",
    },
}

GENRE_PRESETS = {
    "仙侠": "门派纷争 / 修仙问道 / 御剑飞行 / 法宝秘术",
    "宫斗": "宫廷权谋 / 妃嫔博弈 / 皇家礼仪 / 雕梁画栋",
    "江湖": "快意恩仇 / 武林纷争 / 客栈酒肆 / 刀光剑影",
    "志怪": "山海异兽 / 妖怪传说 / 古籍志异 / 诡谲氛围",
}

# 豆包大模型 TTS 音色（2026-04 核对，_conversation_wvae_bigtts 后缀=豆包大模型版）
# 实际音色 ID 较多，这里列常用。完整列表见 https://www.volcengine.com/docs/6561/97465
VOICE_PRESETS = {
    # 男声
    "male_young":    "zh_male_ahu_conversation_wvae_bigtts",       # 温暖阿虎（青年温润）
    "male_mature":   "zh_male_M392_conversation_wvae_bigtts",      # 京腔侃爷（成熟磁性）
    "male_elder":    "zh_male_yanqing_conversation_wvae_bigtts",   # 沉稳长者
    # 女声
    "female_young":  "zh_female_sinong_conversation_wvae_bigtts",  # 爽快思思（清新少女）
    "female_mature": "zh_female_xiaohe_conversation_wvae_bigtts",  # 湾湾小何（温柔熟女）
    "female_elder":  "zh_female_guniang_conversation_wvae_bigtts", # 端庄长辈
}
