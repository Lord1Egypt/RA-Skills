#!/usr/bin/env python3
"""
Model Shot Prompt Generator
Generates AI image prompts for Amazon product model/wear shots.
Supports diverse models, poses, and styling guidance.

Usage:
    python model-shot-prompt.py --product "Yoga Leggings" --category "Apparel" \
        --model-type "athletic" --pose "standing" --count 3
"""

import argparse
import json
import sys
from datetime import datetime


MODEL_TYPES = {
    "athletic": {"desc": "Fit, sporty build", "outfit_hint": "activewear styling"},
    "casual": {"desc": "Everyday, relatable look", "outfit_hint": "casual everyday styling"},
    "professional": {"desc": "Business/professional look", "outfit_hint": "clean professional styling"},
    "lifestyle": {"desc": "Aspirational, trendy look", "outfit_hint": "trendy lifestyle styling"},
    "diverse": {"desc": "Mix of body types and ethnicities", "outfit_hint": "inclusive diverse styling"},
}

POSES = {
    "standing": "standing naturally, confident posture, facing camera at slight angle",
    "walking": "mid-stride walking pose, dynamic movement feel",
    "sitting": "seated pose, relaxed and comfortable",
    "action": "action pose relevant to product use, dynamic energy",
    "detail": "close-up on product detail, hands or specific body part",
    "3quarter": "three-quarter turn, shows product from angle, natural stance",
}

BACKGROUNDS = {
    "studio_white": "clean white studio background, professional lighting",
    "studio_gray": "light gray studio background, soft shadows",
    "lifestyle_home": "modern home interior, natural window light",
    "lifestyle_outdoor": "outdoor urban or natural setting, environmental context",
    "gradient": "subtle gradient background, modern and clean",
}


def generate_prompts(product: str, category: str, model_type: str, pose: str,
                      background: str, count: int, features: list = None) -> dict:
    """Generate model shot prompts."""
    model_info = MODEL_TYPES.get(model_type, MODEL_TYPES["lifestyle"])
    pose_desc = POSES.get(pose, POSES["standing"])
    bg_desc = BACKGROUNDS.get(background, BACKGROUNDS["studio_white"])
    feature_text = ", ".join(features[:2]) if features else ""

    prompts = []
    for i in range(count):
        variation = f"variation {i+1}" if count > 1 else ""
        prompt_text = (
            f"Professional e-commerce model photography, {model_info['desc']} model "
            f"wearing {product}, {pose_desc}, {bg_desc}, "
            f"{model_info['outfit_hint']}, highlighting {feature_text}, "
            f"natural expression, {variation}, "
            f"high resolution, studio quality, no text, no watermark, no logo, "
            f"Amazon-compliant product photography"
        )

        prompts.append({
            "index": i + 1,
            "prompt": prompt_text.strip(),
            "model_type": model_type,
            "model_desc": model_info["desc"],
            "pose": pose,
            "background": background,
            "compliance_notes": [
                "Model should appear confident but not overly posed",
                "Product must be clearly visible and identifiable",
                "No brand logos visible unless it's your own brand",
                "Avoid suggestive poses for Amazon compliance",
            ],
        })

    return {
        "product": product,
        "category": category,
        "model_type": model_type,
        "pose": pose,
        "prompt_count": len(prompts),
        "prompts": prompts,
        "amazon_image_rules": [
            "Main image: white background (RGB 255,255,255), product fills 85% of frame",
            "Model images: allowed as secondary images, must focus on product",
            "No nudity, suggestive poses, or offensive content",
            "Minimum 1000px on longest side, recommended 2000x2000px",
        ],
    }


def format_output(result: dict) -> str:
    lines = []
    lines.append("📸 模特图提示词方案")
    lines.append("━" * 40)
    lines.append(f"产品：{result['product']}")
    lines.append(f"模特类型：{result['model_type']}")
    lines.append("")

    for p in result["prompts"]:
        lines.append(f"  【{p['index']}】{p['model_desc']} / {p['pose']}")
        lines.append(f"  提示词：")
        lines.append(f"  {p['prompt']}")
        lines.append("")

    lines.append("📋 亚马逊图片规则：")
    for rule in result["amazon_image_rules"]:
        lines.append(f"  • {rule}")

    lines.append("━" * 40)
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Model Shot Prompt Generator")
    parser.add_argument("--product", required=True)
    parser.add_argument("--category", required=True)
    parser.add_argument("--model-type", default="lifestyle", choices=list(MODEL_TYPES.keys()))
    parser.add_argument("--pose", default="standing", choices=list(POSES.keys()))
    parser.add_argument("--background", default="studio_white", choices=list(BACKGROUNDS.keys()))
    parser.add_argument("--count", type=int, default=3)
    parser.add_argument("--features", default="")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--input", type=str)

    args = parser.parse_args()
    params = json.loads(args.input) if args.input else None

    if params:
        result = generate_prompts(
            params.get("product", ""), params.get("category", ""),
            params.get("model_type", "lifestyle"), params.get("pose", "standing"),
            params.get("background", "studio_white"), params.get("count", 3),
            params.get("features", []),
        )
    else:
        features = [f.strip() for f in args.features.split(",") if f.strip()]
        result = generate_prompts(args.product, args.category, args.model_type, args.pose, args.background, args.count, features)

    if args.json or (params and params.get("json")):
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(format_output(result))


if __name__ == "__main__":
    main()
