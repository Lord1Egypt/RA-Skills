#!/usr/bin/env python3
"""Optimize text-to-image prompts for various AI art platforms."""

import argparse, json, sys, re

# Style modifiers library
STYLES = {
    "cinematic": "cinematic lighting, dramatic atmosphere, film grain, anamorphic lens, movie still",
    "anime": "anime style, cel shading, vibrant colors, detailed eyes, studio ghibli inspired",
    "photorealistic": "photorealistic, 8k uhd, DSLR, high detail, sharp focus, professional photography",
    "oil_painting": "oil painting, brush strokes, canvas texture, classical art, rich colors, masterpiece",
    "watercolor": "watercolor painting, soft edges, color bleeding, paper texture, delicate",
    "cyberpunk": "cyberpunk, neon lights, futuristic, rain, holographic, dark atmosphere, blade runner",
    "fantasy": "fantasy art, magical, ethereal glow, mystical atmosphere, detailed, epic composition",
    "minimalist": "minimalist, clean design, simple composition, negative space, modern aesthetic",
    "vintage": "vintage, retro, faded colors, film photography, nostalgic, 1970s aesthetic",
    "3d_render": "3D render, octane render, C4D, volumetric lighting, smooth, high quality",
    "pixel_art": "pixel art, 16-bit, retro gaming, sprite art, low resolution charm",
    "sketch": "pencil sketch, hand drawn, detailed linework, graphite, artistic",
    "pop_art": "pop art, Andy Warhol style, bold colors, halftone dots, graphic design",
    "surreal": "surrealism, Salvador Dali inspired, dreamlike, impossible geometry, melting",
    "ukiyo_e": "ukiyo-e, Japanese woodblock print, traditional art, Hokusai style",
    "ink_wash": "Chinese ink wash painting, 水墨画, traditional, elegant, flowing brush strokes",
}

# Quality boosters per platform
QUALITY = {
    "midjourney": "masterpiece, best quality, highly detailed, sharp focus, 8k resolution",
    "dreamina": "高清, 精细, 大师级, 高质量, 细节丰富",
    "nano_banana": "best quality, masterpiece, ultra detailed, high resolution",
    "qwen": "高质量, 精美, 细节丰富, 专业级",
}

# Negative prompts per platform
NEGATIVES = {
    "midjourney": "--no blurry, low quality, distorted, deformed, ugly, bad anatomy",
    "dreamina": "低质量, 模糊, 变形, 丑陋, 解剖错误",
    "nano_banana": "blurry, low quality, distorted, deformed, bad anatomy, watermark, text",
    "qwen": "低质量, 模糊, 变形, 水印, 文字",
}

# Platform-specific formatting
PLATFORM_CONFIG = {
    "midjourney": {
        "name": "Midjourney",
        "icon": "🎨",
        "lang": "en",
        "max_len": 6000,
        "suffix_template": " --ar {ratio} --v 6.1 --q 2",
        "tips": ["Use :: for multi-prompts", "Use --ar for aspect ratio", "Use --s for stylize value"],
    },
    "dreamina": {
        "name": "极梦 Dreamina",
        "icon": "🌈",
        "lang": "zh",
        "max_len": 2000,
        "suffix_template": "",
        "tips": ["支持中英文混合", "可指定画面比例", "使用逗号分隔关键词"],
    },
    "nano_banana": {
        "name": "Nano Banana",
        "icon": "🍌",
        "lang": "en",
        "max_len": 4000,
        "suffix_template": "",
        "tips": ["Use detailed descriptions", "Separate concepts with commas", "Add quality tags"],
    },
    "qwen": {
        "name": "Qwen",
        "icon": "🤖",
        "lang": "zh",
        "max_len": 2000,
        "suffix_template": "",
        "tips": ["支持中文自然语言描述", "可添加风格关键词", "描述越详细效果越好"],
    },
}


def detect_language(text):
    """Detect if text is primarily Chinese or English."""
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
    return "zh" if chinese_chars > len(text) * 0.3 else "en"


def enhance_prompt(prompt, platform="midjourney", style=None, ratio="1:1", quality=True):
    """Enhance a basic prompt into an optimized one for the target platform."""
    config = PLATFORM_CONFIG.get(platform, PLATFORM_CONFIG["midjourney"])
    parts = []

    # Main prompt
    parts.append(prompt.strip())

    # Add style
    if style and style in STYLES:
        parts.append(STYLES[style])

    # Add quality boosters
    if quality and platform in QUALITY:
        parts.append(QUALITY[platform])

    # Combine
    enhanced = ", ".join(parts)

    # Platform-specific suffix
    suffix = config["suffix_template"].format(ratio=ratio)
    enhanced += suffix

    # Truncate if needed
    if len(enhanced) > config["max_len"]:
        enhanced = enhanced[:config["max_len"] - 3] + "..."

    # Negative prompt
    negative = NEGATIVES.get(platform, "")

    return {
        "platform": config["name"],
        "icon": config["icon"],
        "original": prompt,
        "optimized": enhanced,
        "negative": negative,
        "style": style,
        "ratio": ratio,
        "length": len(enhanced),
        "max_length": config["max_len"],
        "tips": config["tips"],
    }


def format_output(data):
    lines = [f"{data['icon']} {data['platform']} 优化提示词", ""]
    lines.append(f"📝 原始: {data['original']}")
    lines.append("")
    lines.append(f"✨ 优化后:")
    lines.append(f"```")
    lines.append(data["optimized"])
    lines.append(f"```")
    if data["negative"]:
        lines.append(f"\n🚫 反向提示:")
        lines.append(f"```")
        lines.append(data["negative"])
        lines.append(f"```")
    lines.append(f"\n📐 比例: {data['ratio']} | 字数: {data['length']}/{data['max_length']}")
    if data["style"]:
        lines.append(f"🎨 风格: {data['style']}")
    lines.append(f"\n💡 技巧:")
    for t in data["tips"]:
        lines.append(f"  • {t}")
    return "\n".join(lines)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--prompt", required=True, help="Original prompt text")
    p.add_argument("--platform", choices=list(PLATFORM_CONFIG.keys()), default="midjourney")
    p.add_argument("--style", default=None, help="Art style name")
    p.add_argument("--ratio", default="1:1", help="Aspect ratio (e.g. 16:9)")
    p.add_argument("--no-quality", action="store_true", help="Skip quality boosters")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()
    data = enhance_prompt(a.prompt, a.platform, a.style, a.ratio, not a.no_quality)
    print(json.dumps(data, indent=2, ensure_ascii=False) if a.json else format_output(data))
