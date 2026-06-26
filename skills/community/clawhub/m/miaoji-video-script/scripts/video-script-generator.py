#!/usr/bin/env python3
"""
Video Script Generator
Generates structured video scripts for Amazon product videos, TikTok, and Shorts.
Supports multiple script structures with timing and shot guidance.

Usage:
    python video-script-generator.py --product "Wireless Earbuds" --category "Electronics" \
        --duration 30 --style "demo" --platform "amazon"
    python video-script-generator.py --input '{"product":"...","category":"...","duration":30,"style":"demo"}'
"""

import argparse
import json
import sys
from datetime import datetime


# ── Script Templates ─────────────────────────────────────────────

SCRIPT_STRUCTURES = {
    "demo": {
        "name": "产品演示型",
        "phases": [
            {"name": "Hook", "duration_pct": 0.15, "purpose": "Attention grab in first 3s"},
            {"name": "Problem", "duration_pct": 0.15, "purpose": "Show the pain point"},
            {"name": "Demo", "duration_pct": 0.40, "purpose": "Product in action"},
            {"name": "Benefit", "duration_pct": 0.20, "purpose": "Result & transformation"},
            {"name": "CTA", "duration_pct": 0.10, "purpose": "Call to action"},
        ],
    },
    "unboxing": {
        "name": "开箱体验型",
        "phases": [
            {"name": "Teaser", "duration_pct": 0.10, "purpose": "Product silhouette or box"},
            {"name": "Unbox", "duration_pct": 0.30, "purpose": "Opening and first impression"},
            {"name": "Detail", "duration_pct": 0.30, "purpose": "Close-up features"},
            {"name": "Setup", "duration_pct": 0.15, "purpose": "Quick setup demo"},
            {"name": "Verdict", "duration_pct": 0.15, "purpose": "Final reaction and CTA"},
        ],
    },
    "story": {
        "name": "故事场景型",
        "phases": [
            {"name": "Scene", "duration_pct": 0.20, "purpose": "Relatable life scene"},
            {"name": "Conflict", "duration_pct": 0.15, "purpose": "Problem arises"},
            {"name": "Solution", "duration_pct": 0.30, "purpose": "Product as hero"},
            {"name": "Joy", "duration_pct": 0.20, "purpose": "Happy outcome"},
            {"name": "CTA", "duration_pct": 0.15, "purpose": "Soft call to action"},
        ],
    },
    "comparison": {
        "name": "对比评测型",
        "phases": [
            {"name": "Setup", "duration_pct": 0.15, "purpose": "What we're comparing"},
            {"name": "Test1", "duration_pct": 0.25, "purpose": "First comparison point"},
            {"name": "Test2", "duration_pct": 0.25, "purpose": "Second comparison point"},
            {"name": "Result", "duration_pct": 0.20, "purpose": "Overall verdict"},
            {"name": "CTA", "duration_pct": 0.15, "purpose": "Recommendation"},
        ],
    },
    "tutorial": {
        "name": "使用教程型",
        "phases": [
            {"name": "Intro", "duration_pct": 0.10, "purpose": "What you'll learn"},
            {"name": "Step1", "duration_pct": 0.25, "purpose": "First setup/usage step"},
            {"name": "Step2", "duration_pct": 0.25, "purpose": "Second usage step"},
            {"name": "ProTips", "duration_pct": 0.25, "purpose": "Advanced tips"},
            {"name": "CTA", "duration_pct": 0.15, "purpose": "Subscribe/learn more"},
        ],
    },
}

PLATFORM_SPECS = {
    "amazon": {"max_duration": 60, "aspect": "16:9", "tip": "Focus on product features and benefits"},
    "tiktok": {"max_duration": 60, "aspect": "9:16", "tip": "Hook in first 1s, fast cuts, trending audio"},
    "shorts": {"max_duration": 60, "aspect": "9:16", "tip": "Quick pacing, text overlays, vertical-first"},
    "reels": {"max_duration": 90, "aspect": "9:16", "tip": "Aesthetic editing, music sync, lifestyle feel"},
}

HOOK_TEMPLATES = {
    "problem": "Tired of [common problem]? Watch this.",
    "question": "Did you know [surprising fact about product]?",
    "shock": "[Unexpected result] in just [timeframe]!",
    "demo": "Watch what happens when I [action with product]...",
    "story": "I never thought [transformation] was possible until...",
}


def generate_script(product: str, category: str, duration: int, style: str,
                     platform: str, features: list = None, target_audience: str = "") -> dict:
    """Generate structured video script."""
    structure = SCRIPT_STRUCTURES.get(style, SCRIPT_STRUCTURES["demo"])
    platform_spec = PLATFORM_SPECS.get(platform, PLATFORM_SPECS["amazon"])

    # Generate phases with timing
    phases = []
    for phase in structure["phases"]:
        phase_duration = round(duration * phase["duration_pct"])
        phases.append({
            "name": phase["name"],
            "duration_seconds": phase_duration,
            "purpose": phase["purpose"],
            "shot_type": _suggest_shot_type(phase["name"], style),
            "script_guidance": _generate_phase_guidance(phase["name"], product, category, features or []),
        })

    # Generate hook options
    hooks = []
    for hook_type, template in HOOK_TEMPLATES.items():
        hook_text = template.replace("[common problem]", f"struggling with your {category.lower()}")
        hook_text = hook_text.replace("[surprising fact about product]", f"this {product.lower()} can do this")
        hook_text = hook_text.replace("[Unexpected result]", "This happened")
        hook_text = hook_text.replace("[timeframe]", f"{duration} seconds")
        hook_text = hook_text.replace("[action with product]", f"use this {product.lower()}")
        hook_text = hook_text.replace("[transformation]", "this kind of result")
        hooks.append({"type": hook_type, "text": hook_text})

    return {
        "product": product,
        "category": category,
        "style": style,
        "style_name": structure["name"],
        "platform": platform,
        "platform_spec": platform_spec,
        "duration": duration,
        "total_phases": len(phases),
        "phases": phases,
        "hook_options": hooks,
        "target_audience": target_audience or "General consumers interested in " + category,
    }


def _suggest_shot_type(phase_name: str, style: str) -> str:
    """Suggest camera shot type for each phase."""
    shot_map = {
        "Hook": "Close-up reaction or product hero shot",
        "Problem": "Wide shot of frustrated user",
        "Demo": "Medium close-up, hands-on product",
        "Benefit": "Split screen: before/after or result showcase",
        "CTA": "Product shot with text overlay",
        "Teaser": "Product silhouette or mystery angle",
        "Unbox": "Overhead or POV hands opening box",
        "Detail": "Macro close-up on key features",
        "Setup": "Hands assembling/connecting product",
        "Verdict": "User reaction + product showcase",
        "Scene": "Lifestyle wide shot with natural lighting",
        "Conflict": "Close-up on problem detail",
        "Solution": "Product hero shot entering frame",
        "Joy": "Happy user with product, warm tones",
        "Setup_compare": "Side-by-side product framing",
        "Test1": "Split screen comparison",
        "Test2": "Split screen comparison",
        "Result": "Winner reveal with stats overlay",
        "Intro": "Host facing camera, product nearby",
        "Step1": "Hands-on POV with text step numbers",
        "Step2": "Continued POV with progress shown",
        "ProTips": "Quick cuts with text tip overlays",
    }
    return shot_map.get(phase_name, "Medium shot, product in focus")


def _generate_phase_guidance(phase_name: str, product: str, category: str, features: list) -> str:
    """Generate brief script guidance for each phase."""
    feature_text = ", ".join(features[:3]) if features else "key features"
    guidance_map = {
        "Hook": f"Open with a bold visual or question about {category}. Show the {product} immediately.",
        "Problem": f"Show common frustration with {category.lower()} products. No talking needed — visual storytelling.",
        "Demo": f"Demonstrate {feature_text}. Show real usage, not just the product sitting there. Keep cuts every 2-3 seconds.",
        "Benefit": f"Show the result: how {product.lower()} makes life easier/better. Transformation shot.",
        "CTA": f"End with product shot + text: 'Available on Amazon' or 'Link in bio'. Keep it simple.",
        "Teaser": f"Show only a glimpse of {product} — build curiosity before the full reveal.",
        "Unbox": f"Slowly open packaging, show accessories, first reaction to build authenticity.",
        "Detail": f"Close-up on {feature_text}. Use macro lens or zoom for texture and quality feel.",
        "Setup": f"Quick assembly or connection — show it's easy, not intimidating.",
        "Verdict": f"Honest reaction: 'This is actually really good for [use case]' + show product.",
        "Scene": f"Set up a relatable daily scenario where {product} solves a real problem naturally.",
        "Conflict": f"Zoom into the frustration moment — no audio needed, just visual discomfort.",
        "Solution": f"{product} enters the frame naturally — let the visual tell the story.",
        "Joy": f"Show the positive outcome — user smiling, task completed easily.",
        "Intro": f"Face camera: 'Let me show you the easiest way to [use case for {product}]'",
        "Step1": f"Show the first step with clear text overlay: 'Step 1: [action]'",
        "Step2": f"Continue with step 2, show progress visibly.",
        "ProTips": f"Rapid-fire tips: 'Pro tip #1: [tip]', quick cut, 'Pro tip #2: [tip]'",
        "Result": f"Show the comparison result clearly with visual proof.",
        "Test1": f"First test point — keep it visual and objective.",
        "Test2": f"Second test point — different angle or use case.",
    }
    return guidance_map.get(phase_name, f"Focus on {product} and its {feature_text}.")


def format_script(result: dict) -> str:
    """Format script as readable document."""
    lines = []
    lines.append("🎬 视频脚本方案")
    lines.append("━" * 40)
    lines.append(f"产品：{result['product']}")
    lines.append(f"品类：{result['category']}")
    lines.append(f"风格：{result['style_name']}")
    lines.append(f"平台：{result['platform']} ({result['platform_spec']['aspect']}, ≤{result['platform_spec']['max_duration']}s)")
    lines.append(f"时长：{result['duration']}秒")
    lines.append("")

    lines.append("📋 分镜表：")
    for i, phase in enumerate(result["phases"], 1):
        lines.append(f"")
        lines.append(f"  【{i}】{phase['name']}（{phase['duration_seconds']}秒）")
        lines.append(f"  目的：{phase['purpose']}")
        lines.append(f"  镜头：{phase['shot_type']}")
        lines.append(f"  指导：{phase['script_guidance']}")

    lines.append("")
    lines.append("🪝 Hook选项：")
    for h in result["hook_options"]:
        lines.append(f"  [{h['type']}] {h['text']}")

    lines.append("")
    lines.append(f"💡 平台提示：{result['platform_spec']['tip']}")
    lines.append("━" * 40)
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Video Script Generator")
    parser.add_argument("--product", required=True, help="Product name")
    parser.add_argument("--category", required=True, help="Product category")
    parser.add_argument("--duration", type=int, default=30, help="Video duration in seconds")
    parser.add_argument("--style", default="demo", choices=list(SCRIPT_STRUCTURES.keys()), help="Script style")
    parser.add_argument("--platform", default="amazon", choices=list(PLATFORM_SPECS.keys()), help="Target platform")
    parser.add_argument("--features", default="", help="Key features, comma-separated")
    parser.add_argument("--audience", default="", help="Target audience")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    parser.add_argument("--input", type=str, help="JSON string with all parameters")

    args = parser.parse_args()

    if args.input:
        params = json.loads(args.input)
    else:
        features = [f.strip() for f in args.features.split(",") if f.strip()]
        params = {
            "product": args.product,
            "category": args.category,
            "duration": args.duration,
            "style": args.style,
            "platform": args.platform,
            "features": features,
            "target_audience": args.audience,
        }

    result = generate_script(
        params.get("product", ""),
        params.get("category", ""),
        params.get("duration", 30),
        params.get("style", "demo"),
        params.get("platform", "amazon"),
        params.get("features", []),
        params.get("target_audience", ""),
    )

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(format_script(result))


if __name__ == "__main__":
    main()
