"""剧本分镜生成。

两种模式：
  1. Claude Agent 直接按 schema 写 script.json（推荐）—— 本脚本仅做校验
  2. 独立 CLI 模式 —— 调 Anthropic SDK 生成（需要 ANTHROPIC_API_KEY）
"""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve()
# _shared/ 定位：优先 bundled（scripts/_shared/），fallback monorepo 根
for _cand in (HERE.parent / "_shared", HERE.parents[2] / "_shared"):
    if (_cand / "config.py").exists():
        sys.path.insert(0, str(_cand))
        break

from config import DEFAULTS, STYLE_PRESETS, GENRE_PRESETS


REQUIRED_FIELDS = {"title", "style", "genre", "characters", "scenes"}
REQUIRED_SCENE_FIELDS = {"id", "action", "duration"}


SYSTEM_PROMPT = """你是国风漫剧编剧。根据用户给的主题、时长、风格、类型，输出结构化 JSON 剧本。

硬要求：
1. 只输出 JSON，不要 markdown 代码块
2. scenes 数量 = duration_total / scene_duration，误差 ±1 可接受
3. characters 3-5 个，每人 voice 从音色库选（zh_male_*/zh_female_*）
4. 每镜 action + dialogue 合计对白字数控制在 scene_duration × 3.5 以内
5. camera 用影视术语（远景/全景/中景/近景/特写，推拉摇移）
6. mood 用 2-4 字形容词（苍凉壮阔/风雷激荡 等）
7. 国风审美：意象优先，避免现代词汇

JSON schema 参考 SKILL.md。"""


def build_user_prompt(theme: str, duration: int, style: str, genre: str) -> str:
    n_scenes = duration // DEFAULTS["scene_duration"]
    style_hint = STYLE_PRESETS.get(style, {})
    genre_hint = GENRE_PRESETS.get(genre, "")
    return (
        f"主题：{theme}\n"
        f"总时长：{duration} 秒 / 每镜 5 秒 / 共 {n_scenes} 镜头\n"
        f"风格：{style}（{style_hint.get('prefix', '')}）\n"
        f"类型：{genre}（关键词：{genre_hint}）\n\n"
        f"请输出 script.json。"
    )


def validate(script: dict) -> list[str]:
    errors = []
    missing = REQUIRED_FIELDS - set(script)
    if missing:
        errors.append(f"缺少字段: {missing}")

    scenes = script.get("scenes", [])
    if not scenes:
        errors.append("scenes 为空")
    for i, s in enumerate(scenes):
        smissing = REQUIRED_SCENE_FIELDS - set(s)
        if smissing:
            errors.append(f"scene[{i}] 缺少: {smissing}")

    chars = script.get("characters", [])
    char_ids = {c.get("id") for c in chars}
    for i, s in enumerate(scenes):
        for cid in s.get("characters", []):
            if cid not in char_ids:
                errors.append(f"scene[{i}] 引用未定义角色 {cid}")
    return errors


def generate_via_anthropic(theme: str, duration: int, style: str, genre: str) -> dict:
    """用 Anthropic SDK 调 Claude 4.7 Opus."""
    try:
        from anthropic import Anthropic
    except ImportError:
        raise RuntimeError("需 pip install anthropic，或 Agent 模式直写 script.json")

    client = Anthropic()
    resp = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=8192,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": build_user_prompt(theme, duration, style, genre)}],
    )
    text = resp.content[0].text.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    return json.loads(text.strip())


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--theme", required=True)
    p.add_argument("--duration", type=int, default=DEFAULTS["duration_total"])
    p.add_argument("--style", default=DEFAULTS["style"])
    p.add_argument("--genre", default=DEFAULTS["genre"])
    p.add_argument("--out", required=True)
    p.add_argument("--input-json", help="已有 script.json 路径，仅做校验")
    args = p.parse_args()

    out_path = pathlib.Path(args.out)

    if args.input_json:
        script = json.loads(pathlib.Path(args.input_json).read_text())
    elif out_path.exists():
        print(f"[script] {out_path} 已存在，跳过生成，仅校验")
        script = json.loads(out_path.read_text())
    else:
        print(f"[script] 生成中...theme={args.theme!r}")
        script = generate_via_anthropic(args.theme, args.duration, args.style, args.genre)

    errors = validate(script)
    if errors:
        print("❌ 校验失败:")
        for e in errors:
            print(f"  - {e}")
        return 1

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(script, ensure_ascii=False, indent=2))
    print(f"✅ {out_path} | {len(script['scenes'])} 镜 / {len(script['characters'])} 角色")
    return 0


if __name__ == "__main__":
    sys.exit(main())
