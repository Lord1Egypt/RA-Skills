#!/usr/bin/env python3
"""
Scene Prompt Generator
Generates AI image prompts for Amazon product scene/lifestyle shots.
Outputs structured prompts with style, lighting, angle, and mood guidance.

Usage:
    python scene-prompt-generator.py --product "Camping Tent" --category "Outdoor" \
        --style "lifestyle" --season "summer" --count 3
"""

import argparse
import json
import sys
from datetime import datetime


SCENE_STYLES = {
    "lifestyle": {
        "name": "生活场景",
        "prompt_prefix": "Lifestyle product photography",
        "lighting": "natural warm golden hour lighting",
        "mood": "aspirational, comfortable, authentic",
    },
    "outdoor": {
        "name": "户外场景",
        "prompt_prefix": "Outdoor adventure product photography",
        "lighting": "natural daylight, sun rays",
        "mood": "adventurous, free, energetic",
    },
    "home": {
        "name": "家居场景",
        "prompt_prefix": "Home interior product photography",
        "lighting": "soft diffused window light",
        "mood": "cozy, clean, organized",
    },
    "studio": {
        "name": "棚拍场景",
        "prompt_prefix": "Professional studio product photography",
        "lighting": "studio softbox, clean white background",
        "mood": "premium, trustworthy, clear",
    },
    "flatlay": {
        "name": "平铺展示",
        "prompt_prefix": "Flat lay product photography, overhead view",
        "lighting": "even flat lighting from above",
        "mood": "organized, aesthetic, editorial",
    },
}

CAMERA_ANGLES = [
    {"angle": "45-degree elevated", "desc": "slightly above, shows depth and surface"},
    {"angle": "Eye level", "desc": "natural perspective, relatable"},
    {"angle": "Low angle", "desc": "hero shot, makes product look impressive"},
    {"angle": "Close-up detail", "desc": "texture and material focus"},
    {"angle": "Wide environmental", "desc": "product in context, shows scale"},
]

SEASON_MOODS = {
    "spring": {"colors": "soft pastels, fresh greens, light wood tones", "props": "flowers, light fabrics, open windows"},
    "summer": {"colors": "bright blues, warm yellows, vivid greens", "props": "sunlight, water elements, outdoor settings"},
    "autumn": {"colors": "warm oranges, deep reds, amber tones", "props": "fallen leaves, warm beverages, cozy textiles"},
    "winter": {"colors": "cool whites, soft grays, deep navy", "props": "snow elements, warm lighting, indoor comfort"},
}


def generate_prompts(product: str, category: str, style: str, season: str,
                      count: int, features: list = None) -> dict:
    """Generate scene prompts for product photography."""
    style_info = SCENE_STYLES.get(style, SCENE_STYLES["lifestyle"])
    season_info = SEASON_MOODS.get(season, SEASON_MOODS["summer"])

    prompts = []
    for i in range(count):
        angle = CAMERA_ANGLES[i % len(CAMERA_ANGLES)]
        feature_text = ", ".join(features[:2]) if features else ""

        prompt_text = (
            f"{style_info['prompt_prefix']} of {product}, "
            f"{angle['angle']} view, {style_info['lighting']}, "
            f"{season_info['colors']}, {style_info['mood']} mood, "
            f"featuring {feature_text} if visible, "
            f"props: {season_info['props']}, "
            f"shallow depth of field, high resolution, professional quality, "
            f"no text overlay, no watermark, no logo"
        )

        prompts.append({
            "index": i + 1,
            "prompt": prompt_text.strip(),
            "style": style_info["name"],
            "angle": angle["angle"],
            "angle_desc": angle["desc"],
            "lighting": style_info["lighting"],
            "season_colors": season_info["colors"],
            "platform_spec": {
                "amazon_main": "Resize to 2000x2000px, white or lifestyle background",
                "amazon_secondary": "Resize to 2000x2000px, lifestyle context",
                "tiktok": "Resize to 1080x1920px vertical, add text overlay",
            },
        })

    return {
        "product": product,
        "category": category,
        "style": style,
        "style_name": style_info["name"],
        "season": season,
        "prompt_count": len(prompts),
        "prompts": prompts,
        "tips": [
            f"For Amazon: Use {style_info['name']} style images as secondary images, keep main image as white background",
            f"Shoot in RAW format for maximum editing flexibility",
            f"Consistent lighting across all shots creates a cohesive listing feel",
        ],
    }


def format_output(result: dict) -> str:
    lines = []
    lines.append("🎨 场景图提示词方案")
    lines.append("━" * 40)
    lines.append(f"产品：{result['product']}")
    lines.append(f"风格：{result['style_name']}")
    lines.append(f"季节：{result['season']}")
    lines.append("")

    for p in result["prompts"]:
        lines.append(f"  【{p['index']}】{p['style']} / {p['angle']}")
        lines.append(f"  角度说明：{p['angle_desc']}")
        lines.append(f"  提示词：")
        lines.append(f"  {p['prompt']}")
        lines.append("")

    for tip in result["tips"]:
        lines.append(f"  💡 {tip}")

    lines.append("━" * 40)
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Scene Prompt Generator")
    parser.add_argument("--product", required=True)
    parser.add_argument("--category", required=True)
    parser.add_argument("--style", default="lifestyle", choices=list(SCENE_STYLES.keys()))
    parser.add_argument("--season", default="summer", choices=list(SEASON_MOODS.keys()))
    parser.add_argument("--count", type=int, default=3)
    parser.add_argument("--features", default="", help="Key features, comma-separated")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--input", type=str)

    args = parser.parse_args()
    params = json.loads(args.input) if args.input else None

    if params:
        result = generate_prompts(
            params.get("product", ""), params.get("category", ""),
            params.get("style", "lifestyle"), params.get("season", "summer"),
            params.get("count", 3), params.get("features", []),
        )
    else:
        features = [f.strip() for f in args.features.split(",") if f.strip()]
        result = generate_prompts(args.product, args.category, args.style, args.season, args.count, features)

    if args.json or (params and params.get("json")):
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(format_output(result))


if __name__ == "__main__":
    main()
