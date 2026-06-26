#!/usr/bin/env python3
"""
pic-gen: 提示词优化脚本 v2.0
基于全网最佳实践重构，让生成的图片真正「哇塞」
"""

import argparse
import os
import re
import sys
import yaml

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
CONFIG_PATH = os.path.join(SKILL_DIR, "config", "models.yaml")
REF_DIR = os.path.join(SKILL_DIR, "references")


# ============================================================
# 通义万相优化器
# 公式：[主体描述] + [风格设定] + [细节要求] + [视觉氛围] + [分辨率/比例]
# 来源：通义万相官方提示词技巧
# ============================================================

def _qwen_enhance(prompt: str) -> list[str]:
    """生成通义万相增强关键词列表"""
    enhancements = []
    prompt_lower = prompt.lower()

    # 质量基础包
    base = ["细节丰富", "高品质", "高精度"]
    enhancements.extend(base)

    # 风格检测（梵高、宫崎骏、皮克斯、油画等）
    if any(k in prompt_lower for k in ["梵高", "van gogh", "油画", "后印象派"]):
        enhancements.extend(["浓烈色彩", "笔触感", "后印象派风格", "厚涂感"])
    elif any(k in prompt_lower for k in ["宫崎骏", "吉卜力", "新海诚", "动漫", "anime"]):
        enhancements.extend(["动画风格", "柔和色调", "宫崎骏光影", "细腻色彩"])
    elif any(k in prompt_lower for k in ["皮克斯", "pixar", "3d", "卡通"]):
        enhancements.extend(["3D动画风格", "皮克斯质感", "柔和光影", "可爱感"])
    elif any(k in prompt_lower for k in ["水彩", "watercolor"]):
        enhancements.extend(["水彩渲染", "柔和边缘", "通透感", "艺术感"])

    # 光影氛围包（根据场景自动选择）
    if any(k in prompt_lower for k in ["雨", "rain", "雨夜"]):
        enhancements.extend(["雨丝光束", "湿润质感", "霓虹倒影", "冷色调", "氛围感"])
    elif any(k in prompt_lower for k in ["赛博朋克", "cyberpunk", "霓虹", "neon"]):
        enhancements.extend(["霓虹灯光", "赛博光效", "冷色调", "科技感"])
    elif any(k in prompt_lower for k in ["夜", "星空", "月亮", "night", "star"]):
        enhancements.extend(["月光", "星芒", "深邃夜空", "冷色调"])
    elif any(k in prompt_lower for k in ["日出", "日落", "sunrise", "sunset", "黄昏"]):
        enhancements.extend(["金色时刻", "暖色调", "柔和逆光", "天空渲染"])
    elif any(k in prompt_lower for k in ["森林", "绿", "自然"]):
        enhancements.extend(["自然光", "森林光影", "斑驳光影", "清新感"])
    elif any(k in prompt_lower for k in ["海", "沙滩", "ocean", "beach"]):
        enhancements.extend(["海风光影", "水面倒影", "清澈蓝", "空气感"])
    else:
        enhancements.extend(["自然光", "柔和光影", "氛围感"])

    # 风格加成（根据关键词匹配）
    if any(k in prompt_lower for k in ["猫", "cat", "狗", "dog", "动物"]):
        enhancements.extend(["毛发纹理", "真实感", "大眼睛"])
    if any(k in prompt_lower for k in ["人", "girl", "boy", "woman", "man"]):
        enhancements.extend(["光影立体感", "轮廓分明", "质感皮肤"])

    # 摄影感
    if any(k in prompt_lower for k in ["风景", "landscape", "城市", "city", "建筑"]):
        enhancements.extend(["电影感构图", "广角视野", "层次分明"])
    if any(k in prompt_lower for k in ["食物", "food", "美食"]):
        enhancements.extend(["食欲感", "商业摄影", "浅景深"])

    return enhancements


def optimize_for_qwen(prompt: str) -> str:
    """通义万相提示词优化"""
    enhancements = _qwen_enhance(prompt)
    # 去掉原prompt中已有的重复词
    parts = [prompt.strip()]
    for e in enhancements:
        if e not in prompt and e.lower() not in prompt.lower():
            parts.append(e)
    return "，".join(parts)


# ============================================================
# Midjourney 优化器
# 公式：摄影类型 + 主体描述 + 相机型号 + 打光 + 角度 + 辅助词
# 来源：今日头条「Midjourney神公式直接出大片」
# ============================================================

MJ_PHOTOGRAPHY_TYPES = [
    "portrait photography", "fashion photography", "landscape photography",
    "street photography", "product photography", "food photography",
    "cinematic photography", "editorial photography", "fine art photography",
    "documentary photography", "wildlife photography", "macro photography",
]

MJ_CAMERAS = [
    "shot on Canon EOS R5", "shot on Sony A7R V", "shot on Hasselblad X2D",
    "shot on Leica M11", "shot on Nikon Z9", "shot on Fujifilm GFX 100 II",
    "shot on ARRI Alexa", "shot on RED", "shot on iPhone 15 Pro Max",
    "85mm lens", "35mm lens", "50mm lens", "135mm lens",
    "f/1.4 aperture", "f/2.8 aperture", "shallow depth of field",
]

MJ_LIGHTING = [
    "golden hour lighting", "blue hour lighting", "dramatic natural lighting",
    "studio lighting", "soft box lighting", "rim lighting", "backlighting",
    "cinematic lighting", "volumetric lighting", "neon lighting",
    "low key lighting", "high key lighting", "moody lighting",
    "practical lighting", "window light", "tungsten lighting",
]

MJ_ANGLES = [
    "low angle shot", "high angle shot", "eye level shot",
    "bird's eye view", "worm's eye view", "dutch angle",
    "over the shoulder", "close-up", "extreme close-up",
    "medium shot", "wide shot", "full body shot",
    "cowboy shot", "Italian shot",
]

MJ_QUALITY_BOOSTERS = [
    "award winning", "masterpiece", "8k resolution", "ultra detailed",
    "hyperrealistic", "photorealistic", "cinematic", "film grain",
    "professional color grading", "HDR", "RAW photo",
]


def optimize_for_midjourney(prompt: str) -> str:
    """Midjourney 提示词优化 - 神公式"""
    parts = [prompt.strip()]

    # 检测摄影类型
    prompt_lower = prompt.lower()
    photo_type = "cinematic photography"
    for pt in MJ_PHOTOGRAPHY_TYPES:
        if pt.split()[0] in prompt_lower:
            photo_type = pt
            break
    parts.append(photo_type)

    # 相机
    parts.append(MJ_CAMERAS[0])  # 默认 Canon EOS R5

    # 光照（根据场景智能选择）
    lighting = MJ_LIGHTING[0]  # 默认 golden hour
    if any(k in prompt_lower for k in ["雨", "rain", "wet", "雨夜"]):
        lighting = "neon reflections on wet streets, rain effect, cinematic"
    elif any(k in prompt_lower for k in ["赛博朋克", "cyberpunk", "科幻", "scifi", "霓虹"]):
        lighting = "neon lighting, volumetric fog, cyberpunk atmosphere"
    elif any(k in prompt_lower for k in ["夜", "night", "星空", "star", "月亮", "moon"]):
        lighting = "neon lighting, colorful glow, night atmosphere"
    elif any(k in prompt_lower for k in ["日", "sun", "黎明", "dawn", "黄昏", "dusk"]):
        lighting = "golden hour, warm tones, soft light"
    elif any(k in prompt_lower for k in ["森林", "nature", "绿", "green"]):
        lighting = "natural sunlight, dappled light, forest atmosphere"
    elif any(k in prompt_lower for k in ["室内", "room", "cafe", "咖啡"]):
        lighting = "warm interior lighting, cozy atmosphere"
    elif any(k in prompt_lower for k in ["梵高", "van gogh", "油画", "向日葵"]):
        lighting = "post-impressionist, bold brushstrokes, vivid colors, artistic"
    elif any(k in prompt_lower for k in ["宫崎骏", "吉卜力", "anime", "动漫"]):
        lighting = "soft watercolor lighting, Studio Ghibli style, dreamy atmosphere"
    elif any(k in prompt_lower for k in ["皮克斯", "pixar", "3d", "卡通"]):
        lighting = "bright studio lighting, Pixar color palette, soft shadows"
    parts.append(lighting)

    # 角度
    parts.append(MJ_ANGLES[4])  # 默认 cinematic
    # 质量提升
    if any(k in prompt_lower for k in ["梵高", "van gogh"]):
        parts.append("post-impressionist art style, Van Gogh inspired, bold colors, visible brushstrokes")
    elif any(k in prompt_lower for k in ["宫崎骏", "吉卜力"]):
        parts.append("Studio Ghibli anime style, Hayao Miyazaki inspired, soft watercolor aesthetic")
    elif any(k in prompt_lower for k in ["皮克斯", "pixar"]):
        parts.append("Pixar 3D animation style, high quality CGI, vibrant colors")
    else:
        parts.append("hyperrealistic, ultra detailed, 8k, cinematic, film grain")

    # 检查是否已有 --ar 参数
    if "--ar" not in prompt:
        parts.append("--ar 16:9")
    if "--s" not in prompt:
        parts.append("--s 250")
    if "--v" not in prompt:
        parts.append("--v 6")

    # 负面词
    parts.append("--no blur, watermark, text, signature, low quality")

    return ", ".join(parts)


# ============================================================
# Stable Diffusion 优化器
# 公式：[画质前缀] + [主体] + [场景] + [风格/光影]
# 来源：CSDN / 知乎最佳实践
# ============================================================

SD_QUALITY_PREFIX = [
    "masterpiece", "best quality", "high quality", "official art",
    "extremely detailed CG unity 8k wallpaper", "absurdres",
    "incredibly absurdres", "huge filesize",
]

SD_STYLES = [
    "photorealistic", "realistic", "digital illustration",
    "oil painting", "watercolor", "anime", "manga",
    "concept art", "matte painting", "3d render",
    "cyberpunk", "artstation", "pixiv",
]

SD_LIGHTING = [
    "cinematic lighting", "natural lighting", "dramatic lighting",
    "soft lighting", "studio lighting", "rim lighting",
    "volumetric lighting", "god rays", "neon glow",
    "backlit", "frontlit", "side lighting",
]

SD_CAMERA = [
    "wide angle lens", "85mm portrait lens", "35mm lens",
    "depth of field", "bokeh", "sharp focus",
    "cinematic composition", "film grain", "RAW",
]

SD_NEGATIVE = [
    "low quality", "worst quality", "normal quality",
    "blurry", "blur", "bokeh", "noise",
    "watermark", "text", "signature", "logo",
    "deformed", "bad anatomy", "bad hands", "extra limbs",
    "missing fingers", "fused fingers", "bad teeth",
    "mutated", "malformed", "gross proportions",
    "bad shadow", "incorrect anatomy", "poorly drawn face",
]


def optimize_for_stable_diffusion(prompt: str) -> tuple[str, str]:
    """SD 提示词优化 - 质量标签 + 主体 + 场景 + 光影"""
    positive_parts = []

    # 质量前缀
    positive_parts.extend(SD_QUALITY_PREFIX[:4])

    # 主体
    positive_parts.append(prompt.strip())

    # 自动检测风格
    prompt_lower = prompt.lower()
    detected_styles = []
    for style in SD_STYLES:
        if style.split()[0] in prompt_lower:
            detected_styles.append(style)
    if not detected_styles:
        positive_parts.append("photorealistic")  # 默认写实

    # 光影
    positive_parts.extend(SD_LIGHTING[:2])

    # 相机/构图
    positive_parts.append(SD_CAMERA[0])

    positive = ", ".join(positive_parts)
    negative = ", ".join(SD_NEGATIVE)
    return positive, negative


# ============================================================
# Flux 优化器
# 原则：Flux 偏好自然语言，不要堆标签，用完整句子描述场景
# 来源：Flux 官方文档
# ============================================================

FLUX_STYLE_PHRASES = [
    "cinematic, photorealistic", "award winning photography",
    "professional color grading", "ultra detailed", "8k resolution",
    "volumetric lighting", "sharp focus", "shallow depth of field",
]


def optimize_for_flux(prompt: str) -> str:
    """Flux 提示词优化 - 自然语言优先，不要堆标签"""
    prompt_lower = prompt.lower()

    # 检测是否已有风格词
    has_style = any(s in prompt_lower for s in ["cinematic", "photorealistic", "realistic", "style"])
    has_quality = any(s in prompt_lower for s in ["detailed", "8k", "4k", "quality", "high"])

    parts = [prompt.strip()]

    if not has_style:
        parts.append("cinematic, photorealistic")
    if not has_quality:
        parts.append("ultra detailed, 8k resolution")
    if "lighting" not in prompt_lower and "light" not in prompt_lower:
        parts.append("volumetric lighting")

    # Flux 不需要参数，简洁
    return ", ".join(parts)


# ============================================================
# DALL-E 3 优化器
# 原则：自然语言，英文，详细场景描述，对中文用户要翻译
# ============================================================

DALLE_STYLE_TERMS = [
    "photorealistic", "cinematic", "oil painting", "digital illustration",
    "watercolor", "concept art", "editorial photography",
    "fine art", "vivid", "natural",
]

DALLE_QUALITY = {
    "standard": "vivid colors, high detail",
    "hd": "hyper-detailed, ultra realistic, 8k quality",
}

ZH_TO_EN = {
    "猫": "cat", "狗": "dog", "女孩": "young woman", "男孩": "young man",
    "城市": "cityscape", "风景": "landscape", "日出": "sunrise",
    "日落": "sunset", "夜晚": "night", "星空": "starry sky",
    "海": "ocean", "沙滩": "beach", "森林": "forest", "山": "mountain",
    "春天": "spring", "夏天": "summer", "秋天": "autumn", "冬天": "winter",
    "下雨": "rainy", "雪": "snowy", "樱花": "cherry blossoms",
    "赛博朋克": "cyberpunk", "梵高": "Van Gogh", "宫崎骏": "Studio Ghibli",
    "皮克斯": "Pixar style", "油画": "oil painting", "水彩": "watercolor",
    "雨夜": "rainy night", "霓虹灯": "neon lights", "雨": "rain",
}


def _translate_to_en(text: str) -> str:
    """简单中译英辅助"""
    result = text
    for zh, en in ZH_TO_EN.items():
        # 加空格避免连在一起
        result = result.replace(zh, " " + en + " ")
    # 清理多余空格
    import re
    result = re.sub(r'\s+', ' ', result).strip()
    return result


def optimize_for_dalle(prompt: str, quality: str = "standard") -> str:
    """DALL-E 3 提示词优化 - 自然语言英文，详细场景"""
    # 翻译
    if any('\u4e00' <= c <= '\u9fff' for c in prompt):
        prompt_en = _translate_to_en(prompt)
    else:
        prompt_en = prompt.strip()

    # 质量词
    quality_str = DALLE_QUALITY.get(quality, DALLE_QUALITY["standard"])

    # 组装：场景化详细描述
    parts = [prompt_en]
    parts.append(quality_str)
    parts.append("professional photography")
    parts.append("highly detailed")
    parts.append("perfect composition")

    return ", ".join(parts)


# ============================================================
# 主入口
# ============================================================

def optimize(prompt: str, platform: str = "all") -> dict:
    """
    主优化函数

    Args:
        prompt: 用户原始描述
        platform: 目标平台 ["qwen", "midjourney", "stable_diffusion", "flux", "dalle", "all"]

    Returns:
        dict: 各平台优化结果
    """
    platforms_map = {
        "qwen": ("通义万相版", "⚡", "text"),
        "midjourney": ("Midjourney 版", "🎨", "text"),
        "stable_diffusion": ("Stable Diffusion 版", "🖌️", "text_with_negative"),
        "flux": ("Flux 版", "🌊", "text"),
        "dalle": ("DALL-E 3 版", "🖼️", "text"),
    }

    if platform == "all":
        results = {}
        for key, (label, emoji, fmt) in platforms_map.items():
            try:
                result = _optimize_single(prompt, key, fmt)
                results[key] = {"label": label, "emoji": emoji, **result}
            except Exception as e:
                results[key] = {"label": label, "emoji": emoji, "error": str(e)}
        return results
    elif platform in platforms_map:
        label, emoji, fmt = platforms_map[platform]
        result = _optimize_single(prompt, platform, fmt)
        return {platform: {"label": label, "emoji": emoji, **result}}
    else:
        return {"error": f"Unknown platform: {platform}"}


def _optimize_single(prompt: str, platform: str, fmt: str) -> dict:
    if platform == "qwen":
        return {"prompt": optimize_for_qwen(prompt)}
    elif platform == "midjourney":
        return {"prompt": optimize_for_midjourney(prompt)}
    elif platform == "stable_diffusion":
        pos, neg = optimize_for_stable_diffusion(prompt)
        return {"prompt": pos, "negative": neg}
    elif platform == "flux":
        return {"prompt": optimize_for_flux(prompt)}
    elif platform == "dalle":
        return {"prompt": optimize_for_dalle(prompt)}


def format_output(results: dict) -> str:
    """格式化输出"""
    lines = []
    for key, data in results.items():
        if "error" in data:
            lines.append(f"{data['emoji']} {data['label']}: 错误 - {data['error']}")
            continue
        lines.append(f"{data['emoji']} **{data['label']}**：")
        lines.append(f"「{data['prompt']}」")
        if "negative" in data:
            lines.append(f"   🚫 负面词：{data['negative']}")
        lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="pic-gen 提示词优化器 v2.0")
    parser.add_argument("--input", "-i", required=True, help="用户原始描述")
    parser.add_argument("--platform", "-p", default="all",
                        choices=["qwen", "midjourney", "stable_diffusion", "flux", "dalle", "all"])
    parser.add_argument("--format", "-f", default="text",
                        choices=["text", "yaml", "json"])
    args = parser.parse_args()

    results = optimize(args.input, args.platform)

    if args.format == "text":
        print(format_output(results))
    elif args.format == "yaml":
        print(yaml.dump(results, allow_unicode=True, default_flow_style=False))
    elif args.format == "json":
        import json
        print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
