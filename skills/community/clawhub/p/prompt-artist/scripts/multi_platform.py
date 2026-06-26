#!/usr/bin/env python3
"""Generate optimized prompts for all platforms at once."""

import argparse, json, sys
from optimize import enhance_prompt, PLATFORM_CONFIG, STYLES


def multi_optimize(prompt, style=None, ratio="1:1"):
    results = []
    for platform in PLATFORM_CONFIG:
        data = enhance_prompt(prompt, platform, style, ratio)
        results.append(data)
    return {"original": prompt, "style": style, "ratio": ratio, "platforms": results}


def format_output(data):
    lines = [f"🎨 多平台提示词优化", f"📝 原始: {data['original']}", ""]
    if data["style"]:
        lines.append(f"🖌️ 风格: {data['style']}")
    lines.append(f"📐 比例: {data['ratio']}")
    lines.append("")

    for p in data["platforms"]:
        lines.append(f"{'='*50}")
        lines.append(f"{p['icon']} **{p['platform']}**")
        lines.append(f"```")
        lines.append(p["optimized"])
        lines.append(f"```")
        if p["negative"]:
            lines.append(f"🚫 反向: {p['negative']}")
        lines.append("")

    return "\n".join(lines)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--prompt", required=True)
    p.add_argument("--style", default=None)
    p.add_argument("--ratio", default="1:1")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()
    data = multi_optimize(a.prompt, a.style, a.ratio)
    print(json.dumps(data, indent=2, ensure_ascii=False) if a.json else format_output(data))
