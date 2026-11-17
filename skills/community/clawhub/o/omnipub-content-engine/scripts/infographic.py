# -*- coding: utf-8 -*-
"""
AI Infographic Prompt Generator
================================
Generates standardized AI infographic prompts for industry research reports.

8-element layout: page_num -> main_title -> subtitle -> data_cards -> 3d_visual -> bottom_insight -> data_source -> brand_signature

Supports 4 engines: 即梦, LOVART, ChatGPT, Midjourney

Usage:
    python infographic.py "AI患者渗透率变化趋势" --engine jimeng
    python infographic.py "健康平台流量下滑" --engine all --data "76%->52%" --source "公开年报"
"""
import argparse
import os
import sys
from datetime import datetime

ENGINES = {
    "jimeng": {
        "name": "即梦",
        "strength": "中文文字渲染最强",
        "extra": "Use Chinese text directly on image, no English text overlay.",
        "style_hint": "3D isometric miniature city, glass crystal texture, neon glow",
    },
    "lovart": {
        "name": "LOVART",
        "strength": "设计质感最佳",
        "extra": "High-end editorial design aesthetic, premium magazine quality.",
        "style_hint": "3D isometric architectural scene, premium materials, soft studio lighting",
    },
    "chatgpt": {
        "name": "ChatGPT/DALL-E",
        "strength": "语义理解最强",
        "extra": "Generate all visible text in Simplified Chinese. No English text on image.",
        "style_hint": "3D isometric miniature landscape, clean geometry, data holographic cards",
    },
    "midjourney": {
        "name": "Midjourney",
        "strength": "视觉冲击力最强",
        "extra": "--ar 16:9 --v 6 --style raw. All visible text must be Simplified Chinese.",
        "style_hint": "3D isometric city scene, octane render, volumetric lighting",
    },
}

BRAND_COLORS = "#534AB7 (purple), #639922 (green), #2196F3 (blue), #FF9800 (amber)"


def generate_prompt(title: str, subtitle: str, data_points: str,
                    data_source: str, brand: str, engine: str) -> str:
    eng = ENGINES.get(engine, ENGINES["chatgpt"])

    prompt = f"""[Page Num: 01/01]

[Main Title - Chinese]: {title}

[Subtitle - Chinese]: {subtitle}

[Data Cards - 3-6 items, Chinese]:
{data_points}

[3D Isometric Main Visual]:
{eng['style_hint']}. The scene depicts a miniature 3D city or street view representing the industry landscape. Buildings and structures use glass crystal textures with subtle neon glow accents. Floating holographic data cards hover above key buildings, each displaying a data point in Simplified Chinese. The overall color palette uses: {BRAND_COLORS}. No bar charts, no pie charts, no generic data visualizations - only architectural 3D scenes.

[Bottom Insight - Chinese]:
Key takeaway in one sentence, displayed at bottom of image.

[Data Source - Chinese]:
数据来源: {data_source}

[Brand Signature]:
{brand}

[Engine-specific instructions]:
{eng['extra']}
{eng['style_hint']}
All text on image must be in Simplified Chinese (简体中文).
Image dimensions: 900x506px (16:9 aspect ratio).
"""

    return prompt


def generate_all_engines(title: str, subtitle: str, data_points: str,
                         data_source: str, brand: str) -> dict:
    return {eng: generate_prompt(title, subtitle, data_points, data_source, brand, eng)
            for eng in ENGINES}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate AI infographic prompts")
    parser.add_argument("title", help="Main title (Chinese)")
    parser.add_argument("--subtitle", default="", help="Subtitle (Chinese)")
    parser.add_argument("--data", default="数据点1: xx%\n数据点2: xx%", help="Data points (one per line)")
    parser.add_argument("--source", default="公开数据整理", help="Data source attribution")
    parser.add_argument("--brand", default="心明增长实验室", help="Brand name")
    parser.add_argument("--engine", default="all", choices=list(ENGINES.keys()) + ["all"], help="Target AI engine")
    parser.add_argument("--output", "-o", help="Output file path")
    args = parser.parse_args()

    if args.engine == "all":
        prompts = generate_all_engines(args.title, args.subtitle, args.data,
                                        args.source, args.brand)
        output_lines = []
        for eng_name, prompt_text in prompts.items():
            output_lines.append(f"## {ENGINES[eng_name]['name']} ({eng_name})")
            output_lines.append(f"Strength: {ENGINES[eng_name]['strength']}")
            output_lines.append("")
            output_lines.append("```")
            output_lines.append(prompt_text)
            output_lines.append("```")
            output_lines.append("")
            output_lines.append("---")
            output_lines.append("")
        output = "\n".join(output_lines)
    else:
        output = generate_prompt(args.title, args.subtitle, args.data,
                                 args.source, args.brand, args.engine)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"Prompt saved: {args.output}")
    else:
        print(output)
