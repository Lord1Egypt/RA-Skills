#!/usr/bin/env python3
"""游戏帧率参考查询工具。

只查询离线表中已有的公开样本整理结果，不做 CPU/GPU 倍率推算。
查不到就返回未收录，避免把帧率模块做成不可维护的估算器。
"""

import argparse
import json
import re
import sys
from pathlib import Path

import yaml

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

GPU_TOKENS = (
    "RTX5090DV2", "RTX5090D", "RTX5090",
    "RTX5080", "RTX5070TI", "RTX5070", "RTX5060TI", "RTX5060",
    "RX9070XT", "RX9070", "ARCB580",
)

CPU_TOKENS = (
    "9950X3D", "9800X3D", "7800X3D", "9700X", "9600X",
    "285K", "270K", "265K", "265KF", "250K", "250KF",
    "14600KF", "14600K", "14400F", "13400F", "12600KF", "12400F",
)


def compact_text(value):
    return "".join(ch for ch in str(value or "").upper() if ch.isalnum())


def hardware_key(value, tokens):
    text = compact_text(value)
    for token in sorted(tokens, key=len, reverse=True):
        if token in text:
            return token
    if tokens is GPU_TOKENS:
        for token in sorted(tokens, key=len, reverse=True):
            bare = re.sub(r"^(?:RTX|RX|ARC)", "", token)
            if text == bare:
                return token
    return text


def normalize_resolution(value):
    text = compact_text(value)
    if text in {"1K", "1080P", "FHD", "1920X1080"}:
        return "1080p"
    if text in {"2K", "1440P", "QHD", "2560X1440"}:
        return "1440p"
    if text in {"4K", "2160P", "UHD", "3840X2160"}:
        return "2160p"
    if text in {"1080", "1920"}:
        return "1080p"
    if text in {"1440", "2560"}:
        return "1440p"
    if text in {"2160", "3840"}:
        return "2160p"
    return str(value or "1080p")


def load_db():
    path = DATA / "game_fps.yaml"
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def find_game(db, query):
    target = compact_text(query)
    for game in db.get("games", []):
        aliases = [game.get("id", ""), game.get("name", "")] + list(game.get("aliases", []))
        if any(compact_text(alias) == target for alias in aliases):
            return game
    for game in db.get("games", []):
        aliases = [game.get("id", ""), game.get("name", "")] + list(game.get("aliases", []))
        if any(target and target in compact_text(alias) for alias in aliases):
            return game
    return None


def _text_matches(sample_text, query_text, kind):
    if not query_text:
        return True
    if kind == "gpu":
        return hardware_key(sample_text, GPU_TOKENS) == hardware_key(query_text, GPU_TOKENS)
    if kind == "cpu":
        return hardware_key(sample_text, CPU_TOKENS) == hardware_key(query_text, CPU_TOKENS)
    sample = compact_text(sample_text)
    query = compact_text(query_text)
    return bool(sample and sample == query)


def choose_row(rows, cpu_text, gpu_text, memory_text=""):
    if not rows:
        return None
    filtered = [
        row for row in rows
        if _text_matches(row.get("cpu"), cpu_text, "cpu")
        and _text_matches(row.get("gpu"), gpu_text, "gpu")
        and (not memory_text or not row.get("memory") or _text_matches(row.get("memory"), memory_text, "memory"))
    ]
    if filtered:
        return filtered[0]
    return None


def target_result(avg_range, low_range, target):
    if not target:
        return "no_target"
    if low_range and low_range[0] >= target:
        return "target_likely_stable"
    if avg_range[0] >= target:
        return "avg_meets_target_p1_low_not_guaranteed"
    if avg_range[1] >= target:
        return "near_target"
    return "below_target"


def target_human(result_code, target, low_metric=None):
    if result_code == "target_likely_stable":
        if low_metric == "fps_range":
            return f"目标 {target} FPS 处在样本区间内。"
        return f"目标 {target} FPS 处在样本参考范围内。"
    if result_code == "avg_meets_target_p1_low_not_guaranteed":
        return f"平均帧接近 {target} FPS，实际以同配置实测为准。"
    if result_code == "near_target":
        return f"接近 {target} FPS，实际以同配置实测为准。"
    if result_code == "below_target":
        return f"不建议按 {target} FPS 目标来配，需要提高 CPU/显卡档位或降低画质。"
    return ""


def query_one(db, game_id, resolution, preset, cpu, gpu, memory, target_fps=None):
    game = next((item for item in db.get("games", []) if item.get("id") == game_id), None)
    if not game:
        return None
    preset = preset or game.get("default_preset")
    rows = [
        row for row in db.get("benchmarks", [])
        if row.get("game") == game_id
        and row.get("resolution") == resolution
        and row.get("preset") == preset
    ]
    row = choose_row(rows, cpu, gpu, memory)
    if not row:
        return None
    result = dict(row)
    low_range = result.get("p1_low_fps") or result.get("fps_range")
    low_metric = "p1_low" if result.get("p1_low_fps") else ("fps_range" if result.get("fps_range") else None)
    code = target_result(result["avg_fps"], low_range, target_fps)
    result["game_name"] = game.get("name")
    result["preset_name"] = db.get("presets", {}).get(preset, preset)
    result["target_fps"] = target_fps
    result["target_result"] = code
    result["target_note"] = target_human(code, target_fps, low_metric)
    result["low_metric"] = low_metric
    result["source_sample_date"] = db.get("metadata", {}).get("sample_date")
    result["sample_match"] = "direct"
    return result


def build_result(db, args):
    game = find_game(db, args.game)
    if not game:
        return {
            "ok": False,
            "reason": "game_not_found",
            "message": "离线帧率表暂未收录该游戏；可只给硬件方向，不给具体 FPS。"
        }
    resolution = normalize_resolution(args.resolution)
    target = int(args.target_fps) if args.target_fps else None
    if game.get("representatives"):
        reps = []
        for rep in game["representatives"]:
            item = query_one(db, rep, resolution, args.preset, args.cpu, args.gpu, args.memory, target)
            if item:
                reps.append(item)
        return {
            "ok": bool(reps),
            "game": game.get("id"),
            "game_name": game.get("name"),
            "resolution": resolution,
            "representatives": reps,
            "message": "3A 未指定具体游戏，使用代表性游戏做参考。"
        }
    item = query_one(db, game["id"], resolution, args.preset, args.cpu, args.gpu, args.memory, target)
    if not item:
        return {
            "ok": False,
            "reason": "sample_not_found",
            "game": game.get("id"),
            "game_name": game.get("name"),
            "resolution": resolution,
            "message": "该游戏、分辨率、画质或硬件组合暂未收录已核验来源样本；不要编 FPS，可提示需要实时查评测。"
        }
    item["ok"] = True
    return item


def format_range(values):
    start = int(values[0])
    end = int(values[1])
    if start == end:
        return str(start)
    return f"{start}-{end}"


def human_line(item):
    if item.get("preset") == "source_default_unknown":
        base = f"{item['game_name']} / {item['resolution']} 大约帧率：平均约 {format_range(item['avg_fps'])} FPS"
    else:
        base = (
            f"{item['game_name']} / {item['resolution']} / {item['preset_name']}："
            f"平均约 {format_range(item['avg_fps'])} FPS"
        )
    if item.get("p1_low_fps"):
        base += f"，1% low 约 {format_range(item['p1_low_fps'])} FPS。"
    elif item.get("fps_range"):
        base += f"，FPS 区间约 {format_range(item['fps_range'])} FPS。"
    else:
        base += "。"
    if item.get("generated_frames"):
        base += "这是含帧生成的观感帧率，手感仍要看基础帧和延迟。"
    elif item.get("note"):
        base += item["note"]
    return base


def format_human(result):
    if not result.get("ok"):
        return result.get("message", "未找到可用帧率参考。")
    if result.get("representatives"):
        lines = [result.get("message", "代表游戏参考如下：")]
        lines.extend(human_line(item) for item in result["representatives"])
        lines.append("帧率仅供装机选配参考，实际以同配置实测为准。")
        return "\n".join(lines)
    lines = [human_line(result)]
    lines.append("帧率仅供装机选配参考，实际以同配置实测为准。")
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Query rough game FPS reference ranges.")
    parser.add_argument("--game", required=True, help="游戏名或别名，例如 三角洲/打瓦/3A")
    parser.add_argument("--resolution", required=True, help="必须明确分辨率: 1080p/1K/1440p/2K/2160p/4K")
    parser.add_argument("--preset", help="competitive_low/high_no_rt/rt_dlss_fg")
    parser.add_argument("--cpu", default="", help="已选 CPU 型号")
    parser.add_argument("--gpu", default="", help="已选显卡型号或芯片")
    parser.add_argument("--memory", default="", help="内存规格，例如 DDR5 6000 C30 32GB")
    parser.add_argument("--target-fps", type=int, help="用户目标帧数")
    parser.add_argument("--json", action="store_true", help="输出 JSON")
    args = parser.parse_args(argv)

    result = build_result(load_db(), args)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(format_human(result))
    return 0 if result.get("ok") else 2


if __name__ == "__main__":
    raise SystemExit(main())
