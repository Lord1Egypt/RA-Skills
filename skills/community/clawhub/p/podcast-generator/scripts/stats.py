#!/usr/bin/env python3
"""Podcast generation statistics and batch processing."""

import argparse, json, os, sys
from datetime import datetime

STATS_FILE = os.path.expanduser("~/.openclaw/workspace/podcast-generator/data/stats.json")


def load():
    os.makedirs(os.path.dirname(STATS_FILE), exist_ok=True)
    if os.path.exists(STATS_FILE):
        return json.load(open(STATS_FILE))
    return {"generations": [], "total_audio_seconds": 0, "total_calls": 0}


def save(data):
    os.makedirs(os.path.dirname(STATS_FILE), exist_ok=True)
    json.dump(data, open(STATS_FILE, "w"), indent=2, ensure_ascii=False)


def log_generation(title, format_type, audio_seconds, cost=0.001):
    data = load()
    entry = {
        "id": len(data["generations"]) + 1,
        "title": title,
        "format": format_type,
        "audio_seconds": audio_seconds,
        "cost": cost,
        "timestamp": datetime.now().isoformat(),
    }
    data["generations"].append(entry)
    data["total_audio_seconds"] += audio_seconds
    data["total_calls"] += 1
    # Keep last 100
    data["generations"] = data["generations"][-100:]
    save(data)
    return entry


def get_stats():
    data = load()
    total_cost = sum(g["cost"] for g in data["generations"])
    
    # Format breakdown
    formats = {}
    for g in data["generations"]:
        fmt = g["format"]
        formats[fmt] = formats.get(fmt, 0) + 1
    
    return {
        "total_generations": data["total_calls"],
        "total_audio_seconds": data["total_audio_seconds"],
        "total_audio_minutes": data["total_audio_seconds"] / 60,
        "total_cost": total_cost,
        "format_breakdown": formats,
        "recent": data["generations"][-10:],
    }


def format_output(data):
    lines = ["📊 Podcast Generator 统计", ""]
    lines.append(f"🎙️ 总生成次数：{data['total_generations']}")
    lines.append(f"⏱️ 总音频时长：{data['total_audio_minutes']:.1f} 分钟 ({data['total_audio_seconds']:.0f} 秒)")
    lines.append(f"💰 总花费：${data['total_cost']:.4f} USDT")
    lines.append("")
    
    if data["format_breakdown"]:
        lines.append("📋 格式分布:")
        for fmt, count in data["format_breakdown"].items():
            lines.append(f"   • {fmt}: {count} 次")
        lines.append("")
    
    if data["recent"]:
        lines.append("📜 最近 10 次:")
        for g in data["recent"]:
            lines.append(f"   [{g['id']}] {g['title'][:30]} - {g['format']} ({g['audio_seconds']}s)")
    
    return "\n".join(lines)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--action", choices=["show", "log"], default="show")
    p.add_argument("--title", default=None)
    p.add_argument("--format", default="solo")
    p.add_argument("--audio-seconds", type=int, default=0)
    p.add_argument("--json", action="store_true")
    a = p.parse_args()
    
    if a.action == "log":
        r = log_generation(a.title, a.format, a.audio_seconds)
        print(f"✅ 已记录：[{r['id']}] {r['title']} ({r['audio_seconds']}s)")
    else:
        data = get_stats()
        print(json.dumps(data, indent=2) if a.json else format_output(data))
