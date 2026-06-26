#!/usr/bin/env python3
"""
Generate a batch of product scene prompts from a structured JSON input.

Usage:
    python3 generate_prompt_batch.py --in product.json --out prompts.md --tool midjourney

Input JSON schema:
{
    "name": "Product Name",
    "material": "material description",
    "color": "color description",
    "description": "brand positioning and key selling points",
    "style_direction": "mood/aesthetic keywords",
    "angles": ["macro", "hero", "flat_lay", "lifestyle"],
    "tool": "midjourney | dalle3 | sdxl",
    "use_case": "where the images will be used"
}
"""

import argparse
import json
import sys
from pathlib import Path

ANGLE_CONFIGS = {
    "macro": {
        "title": "Macro / Detail Shot",
        "camera": "100mm macro equivalent, f/2.8, extremely shallow DoF",
        "composition": "fill 70%+ of frame with product detail",
        "purpose": "Highlight texture, material grain, craftsmanship",
        "ar_mj": "1:1",
        "dalle_size": "1024x1024",
    },
    "hero": {
        "title": "Eye-Level / Hero Shot",
        "camera": "50-85mm equivalent, f/4-5.6, moderate DoF",
        "composition": "product centered or rule-of-thirds, eye-level",
        "purpose": "Primary PDP or hero image",
        "ar_mj": "4:5",
        "dalle_size": "1024x1792",
    },
    "flat_lay": {
        "title": "Flat Lay / Overhead",
        "camera": "50mm equivalent, f/5.6-8, even focus plane, top-down",
        "composition": "organized layout with props, negative space for text overlay",
        "purpose": "Social media (Instagram, Pinterest)",
        "ar_mj": "1:1",
        "dalle_size": "1024x1024",
    },
    "lifestyle": {
        "title": "Lifestyle / In-Use Scene",
        "camera": "35-50mm equivalent, f/2.8-4, environmental bokeh",
        "composition": "product in natural setting with human interaction cues",
        "purpose": "Contextual storytelling, ads, social",
        "ar_mj": "4:5",
        "dalle_size": "1024x1792",
    },
}

STYLE_PROPS = {
    "organic": "raw wood surface, linen fabric, botanical elements, dried flowers",
    "natural": "raw wood surface, linen fabric, dew drops, terracotta",
    "cozy": "knit fabric, warm-toned wood, candle, ceramic, soft shadows",
    "warm": "knit fabric, warm-toned wood, ambient glow, natural textures",
    "luxury": "marble surface, gold details, velvet texture, dramatic shadows",
    "premium": "marble surface, crystal elements, metallic accents, dark tones",
    "tech": "minimalist geometric shapes, cold-tone surfaces, metallic accents, concrete",
    "modern": "clean lines, frosted glass, concrete surface, matte finishes",
    "playful": "colored paper, confetti, bold geometric shapes, saturated backgrounds",
    "vibrant": "bright colors, fruit, geometric shapes, dynamic composition",
    "minimalist": "clean white surface, negative space, single prop accent",
    "clean": "white surface, soft shadows, airy composition, neutral tones",
}


def detect_style_props(style_direction: str) -> str:
    style_lower = style_direction.lower()
    matched = []
    for key, props in STYLE_PROPS.items():
        if key in style_lower:
            matched.append(props)
    if not matched:
        matched.append(STYLE_PROPS.get("minimalist", ""))
    seen = set()
    unique = []
    for prop_str in matched:
        for p in prop_str.split(", "):
            if p not in seen:
                seen.add(p)
                unique.append(p)
    return ", ".join(unique[:5])


def build_midjourney_prompt(product: dict, angle_key: str, props: str) -> str:
    cfg = ANGLE_CONFIGS[angle_key]
    parts = [
        f"{product['name']} made of {product['material']}",
        f"color: {product['color']}",
        f"resting on a styled surface with natural contact shadow",
        f"surrounded by {props}",
        f"{cfg['camera']}",
        f"{product['style_direction']} aesthetic",
        "professional product photography, photorealistic, studio quality",
    ]
    prompt = ", ".join(parts)
    params = f"--ar {cfg['ar_mj']} --style raw --v 6.1 --q 2"
    return f"{prompt} {params}"


def build_dalle_prompt(product: dict, angle_key: str, props: str) -> str:
    cfg = ANGLE_CONFIGS[angle_key]
    return (
        f"Professional product photograph of {product['name']} "
        f"made of {product['material']}, {product['color']} color. "
        f"{cfg['composition']}. "
        f"Styled with {props}. "
        f"{cfg['camera']}. "
        f"{product['style_direction']} mood. "
        f"Photorealistic, studio quality, no text, no watermarks."
    )


def build_sdxl_prompt(product: dict, angle_key: str, props: str) -> str:
    cfg = ANGLE_CONFIGS[angle_key]
    positive = (
        f"{product['name']}, {product['material']}, {product['color']}, "
        f"{cfg['composition']}, {props}, "
        f"{cfg['camera']}, {product['style_direction']}, "
        "professional product photography, 8k, sharp focus, detailed"
    )
    negative = (
        "cartoon, illustration, painting, drawing, anime, 3d render, "
        "distorted, deformed, blurry, low quality, watermark, text, "
        "floating, unrealistic shadows"
    )
    return f"Positive: {positive}\nNegative: {negative}\nSteps: 35, CFG: 7.5"


BUILDERS = {
    "midjourney": build_midjourney_prompt,
    "dalle3": build_dalle_prompt,
    "sdxl": build_sdxl_prompt,
}


def generate(product: dict) -> str:
    tool = product.get("tool", "midjourney").lower()
    builder = BUILDERS.get(tool, build_midjourney_prompt)
    angles = product.get("angles", list(ANGLE_CONFIGS.keys()))
    props = detect_style_props(product.get("style_direction", "minimalist"))

    lines = [
        f"# Product Scene Prompts — {product['name']}",
        "",
        f"**Tool:** {tool}  ",
        f"**Use case:** {product.get('use_case', 'general')}  ",
        f"**Style direction:** {product.get('style_direction', 'minimalist')}  ",
        f"**Suggested props:** {props}",
        "",
        "---",
        "",
    ]

    for angle_key in angles:
        if angle_key not in ANGLE_CONFIGS:
            continue
        cfg = ANGLE_CONFIGS[angle_key]
        prompt = builder(product, angle_key, props)
        lines.extend([
            f"## {cfg['title']}",
            "",
            f"**Purpose:** {cfg['purpose']}  ",
            f"**Camera:** {cfg['camera']}  ",
            f"**Composition:** {cfg['composition']}  ",
            "",
            "**Prompt:**",
            "",
            f"```",
            prompt,
            f"```",
            "",
            "---",
            "",
        ])

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate product scene prompts")
    parser.add_argument("--in", dest="input", required=True, help="Input product JSON")
    parser.add_argument("--out", dest="output", required=True, help="Output markdown")
    parser.add_argument("--tool", default=None, help="Override tool (midjourney/dalle3/sdxl)")
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        product = json.load(f)

    if args.tool:
        product["tool"] = args.tool

    result = generate(product)

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(result)

    print(f"Prompts written to {args.output}")


if __name__ == "__main__":
    main()
