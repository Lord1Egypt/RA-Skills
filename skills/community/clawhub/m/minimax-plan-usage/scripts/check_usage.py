#!/usr/bin/env python3
"""查询 MiniMax Token Plan 剩余用量"""
import os, sys, json, argparse

try:
    import requests
except ImportError:
    print("Error: pip install requests")
    sys.exit(1)

API_HOST = os.environ.get("MINIMAX_API_HOST", "https://www.minimaxi.com")

def check_usage(api_key: str) -> dict:
    url = f"{API_HOST}/v1/api/openplatform/coding_plan/remains"
    resp = requests.get(url, headers={"Authorization": f"Bearer {api_key}"}, timeout=30)
    resp.raise_for_status()
    return resp.json()

def format_output(data: dict) -> str:
    lines = ["**MiniMax Token Plan 用量**", ""]
    for item in data.get("model_remains", []):
        name = item.get("model_name", "")
        total = item.get("current_interval_total_count", 0)
        remaining = item.get("current_interval_usage_count", 0)
        ms = item.get("remains_time", 0)

        label = {
            "MiniMax-M*": "M2.7",
            "speech-hd": "Speech 2.8",
            "MiniMax-Hailuo-2.3-Fast-6s-768p": "视频 (Fast)",
            "MiniMax-Hailuo-2.3-6s-768p": "视频",
            "image-01": "图片",
            "music-2.5": "音乐",
        }.get(name, name)

        sec = ms // 1000
        h, m, s = sec // 3600, (sec % 3600) // 60, sec % 60
        reset = f"{h}h {m}m {s}s" if h else f"{m}m {s}s"

        lines.append(f"**{label}**")
        lines.append(f"  剩余次数: {remaining} / {total}")
        lines.append(f"  重置倒计时: {reset}")
        lines.append("")
    return "\n".join(lines)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--api-key", default=os.environ.get("MINIMAX_API_KEY"))
    p.add_argument("--json", action="store_true")
    args = p.parse_args()
    if not args.api_key:
        print("Error: set MINIMAX_API_KEY env var")
        sys.exit(1)
    data = check_usage(args.api_key)
    print(json.dumps(data, indent=2, ensure_ascii=False) if args.json else format_output(data))

if __name__ == "__main__":
    main()
