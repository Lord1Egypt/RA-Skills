#!/usr/bin/env python3
"""
huo15-img-prompt — 故事板模式 v3.0

把一段剧本/文案 → Claude 拆 N 个关键帧 → 每帧出 T2I prompt + 帧间 T2V 衔接 prompt
→ 产出完整视频脚本包（可直接喂给 Sora/Kling/Runway/即梦）。

这是 v3.0 的杀手级 feature：把文生图 + 文生视频的"单点能力"组合成"短片生产管线"。
视频内容创作者远多于静态图创作者。

工作流（一次调用完成）：
  Step 1: Claude 读剧本 → 拆 N scenes，每个 scene 给主体描述/构图/光影/动作
  Step 2: 对每个 scene，复用 enhance_prompt 生成 T2I 提示词
  Step 3: 对每两个相邻 scene，复用 enhance_video 生成衔接 T2V 提示词
  Step 4: 整合输出 storyboard.json + scenes/*.txt + README.md（可读视图）

调用：
  storyboard.py "一只猫从城市走进雨夜" -p 电影感 --scenes 4 -m Sora
  storyboard.py < script.txt --scenes 8
  storyboard.py "..." --scenes 5 --output ./my_story --video-model Kling
  storyboard.py "..." --scenes 6 -j > storyboard.json   # JSON 输出

依赖：
  - 同目录 enhance_prompt.py / enhance_video.py
  - ANTHROPIC_API_KEY
"""

import sys
import os
import json
import argparse
import time
import re
from typing import Dict, List, Optional
from urllib.request import Request, urlopen
from urllib.error import HTTPError

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from enhance_prompt import (
    build_prompt, parse_mix_preset, resolve_preset, STYLE_PRESETS, stable_seed,
)
from enhance_video import build_video_prompt
from claude_polish import ANTHROPIC_BASE, ANTHROPIC_VERSION

VERSION = "3.1.0"
DEFAULT_MODEL = "claude-sonnet-4-5"


# ─────────────────────────────────────────────────────────
# Claude 拆剧本 system prompt（启用 cache）
# ─────────────────────────────────────────────────────────
def build_storyboard_system_prompt(target_scenes: int) -> str:
    return f"""你是火一五故事板分镜师。给定一段剧本/文案，拆成 {target_scenes} 个关键帧（key frames），每帧用一句话主体描述 + 视觉/动作要素，相邻帧之间标注衔接动作。

# 工作流

1. 读剧本，提取叙事节奏（开场 → 起 → 承 → 转 → 合）
2. 拆成 {target_scenes} 个连贯关键帧
3. 每帧给：
   - 主体（人/物/场景核心，一句话中文）
   - 构图（特写/中景/全身/俯拍/航拍/侧面 等）
   - 光影/氛围（黄昏/雨夜/霓虹/逆光 等）
   - 主体动作/表情（用于 T2I）
4. 每相邻两帧之间给衔接动作（用于 T2V，描述镜头/主体怎么从 A 帧过渡到 B 帧）

# 输出 JSON 严格 schema

```json
{{
  "title": "整段剧本的简短标题（5-10 字）",
  "logline": "一句话总结",
  "narrative_arc": "开场→起→承→转→合 之类的节奏说明",
  "scenes": [
    {{
      "index": 1,
      "subject": "中文一句话主体描述（具体可视）",
      "subject_en": "English subject for T2I",
      "composition": "特写/中景/全身/俯拍/仰拍/航拍/侧面/背面 之一",
      "lighting": "光影/时间/天气/氛围（中文）",
      "action": "主体动作/表情（用于 T2I 增强）",
      "narrative_role": "叙事角色（开场建立/冲突起点/高潮/落幕 等）"
    }},
    ...{target_scenes} 个
  ],
  "transitions": [
    {{
      "from_scene": 1,
      "to_scene": 2,
      "camera_motion": "推镜/拉镜/摇镜/跟拍/手持/航拍 等（中文）",
      "duration_s": 3,
      "description": "衔接动作描述（中文+英文混合，用于 T2V）"
    }},
    ...{target_scenes - 1} 个
  ],
  "total_duration_s": "估算总时长，秒"
}}
```

# 关键

- {target_scenes} 个 scene，{target_scenes - 1} 个 transition
- 每帧 subject 都要"画面感强"，让 T2I 能复现具体场景
- transitions 描述要让 T2V 模型知道镜头怎么动 + 主体怎么变化
- 全程中文为主，T2I 模型友好的视觉术语英文混合
- 只输出 JSON，不要解释"""


def call_claude_storyboard(script: str, target_scenes: int,
                           model: str = DEFAULT_MODEL) -> Dict:
    """调 Claude 拆剧本。"""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("缺少 ANTHROPIC_API_KEY 环境变量")

    body = {
        "model": model,
        "max_tokens": 4096,
        "temperature": 0.7,
        "system": [{
            "type": "text",
            "text": build_storyboard_system_prompt(target_scenes),
            "cache_control": {"type": "ephemeral"},
        }],
        "messages": [
            {"role": "user", "content": f"<script>\n{script}\n</script>\n\n请输出 JSON。"},
            {"role": "assistant", "content": "{"},
        ],
    }
    req = Request(
        f"{ANTHROPIC_BASE}/v1/messages",
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": ANTHROPIC_VERSION,
        },
        method="POST",
    )
    try:
        with urlopen(req, timeout=120) as r:
            resp = json.loads(r.read().decode("utf-8"))
    except HTTPError as e:
        raise RuntimeError(f"Claude HTTP {e.code}: {e.read().decode('utf-8', errors='replace')}")

    if "error" in resp:
        raise RuntimeError(f"Claude API 错误: {resp['error']}")

    text = ""
    for block in resp.get("content", []):
        if block.get("type") == "text":
            text += block.get("text", "")
    full = "{" + text

    # 抽完整 JSON
    depth = 0
    end = -1
    in_str = False
    esc = False
    for i, ch in enumerate(full):
        if esc:
            esc = False
            continue
        if ch == "\\":
            esc = True
            continue
        if ch == '"':
            in_str = not in_str
            continue
        if in_str:
            continue
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                end = i + 1
                break
    if end == -1:
        raise RuntimeError(f"未找到完整 JSON: {full[:300]}")

    data = json.loads(full[:end])
    usage = resp.get("usage", {})
    data["_usage"] = {
        "input_tokens": usage.get("input_tokens", 0),
        "output_tokens": usage.get("output_tokens", 0),
        "cache_read_input_tokens": usage.get("cache_read_input_tokens", 0),
    }
    data["_model"] = resp.get("model", "")
    return data


# ─────────────────────────────────────────────────────────
# 整合：剧本 → scenes + transitions + T2I/T2V prompts
# ─────────────────────────────────────────────────────────
def storyboard(script: str, preset: str, target_scenes: int = 5,
               i2i_model: str = "通用", t2v_model: str = "通用",
               aspect: str = "", duration_per_transition: int = 3,
               quality_tier: str = "pro",
               claude_model: str = DEFAULT_MODEL) -> Dict:
    """主入口：剧本 → 完整 storyboard 包。"""
    # 1. Claude 拆剧本
    primary, secondary = parse_mix_preset(preset)
    if secondary:
        p1, p2 = resolve_preset(primary), resolve_preset(secondary)
        if not p1 or not p2:
            raise RuntimeError(f"未知预设: {primary} 或 {secondary}")
        preset_resolved, mix_secondary = p1, p2
    else:
        preset_resolved = resolve_preset(primary) or "电影感"
        mix_secondary = None

    if not aspect:
        aspect = STYLE_PRESETS[preset_resolved].get("aspect", "16:9")

    plan = call_claude_storyboard(script, target_scenes, model=claude_model)
    scenes_raw = plan.get("scenes", [])[:target_scenes]
    transitions_raw = plan.get("transitions", [])

    # 共享 seed 锁定整段一致性（角色/场景跨帧不漂移）
    base_seed = stable_seed(script[:80], preset_resolved)

    # 2. 每帧出 T2I prompt
    scene_prompts = []
    for s in scenes_raw:
        subject = s.get("subject", "")
        action = s.get("action", "")
        composition = s.get("composition", "")
        lighting_atmos = s.get("lighting", "")
        full_subject = subject
        if action:
            full_subject = f"{full_subject}, {action}"
        if lighting_atmos:
            full_subject = f"{full_subject}, {lighting_atmos}"

        recipe = build_prompt(
            full_subject, preset_resolved,
            model=i2i_model, aspect=aspect,
            extra_composition=composition,
            seed=base_seed,
            quality_tier=quality_tier,
            mix_secondary=mix_secondary,
        )
        scene_prompts.append({
            "index": s.get("index"),
            "narrative_role": s.get("narrative_role", ""),
            "subject": subject,
            "subject_en": s.get("subject_en", ""),
            "composition": composition,
            "lighting_atmosphere": lighting_atmos,
            "action": action,
            "t2i_prompt": recipe["positive"],
            "t2i_negative": recipe["negative"],
            "consistency_lock": recipe["consistency_lock"],
            "seed": recipe["seed_suggestion"],
        })

    # 3. 每对相邻帧出 T2V 衔接 prompt
    transition_prompts = []
    for t in transitions_raw:
        from_idx = t.get("from_scene")
        to_idx = t.get("to_scene")
        if not from_idx or not to_idx:
            continue
        # 用 from-scene 的 subject 做基础，加 transition 描述
        from_scene = next((s for s in scene_prompts if s["index"] == from_idx), None)
        to_scene = next((s for s in scene_prompts if s["index"] == to_idx), None)
        if not from_scene or not to_scene:
            continue

        transition_subject = (
            f"transition from scene {from_idx} '{from_scene['subject']}' "
            f"to scene {to_idx} '{to_scene['subject']}': {t.get('description', '')}"
        )
        camera_motion = t.get("camera_motion", "")

        video_recipe = build_video_prompt(
            transition_subject, preset_resolved,
            model=t2v_model, aspect=aspect,
            duration=t.get("duration_s", duration_per_transition),
            motion=camera_motion,
            seed=base_seed,
            quality_tier=quality_tier,
            mix_secondary=mix_secondary,
        )
        transition_prompts.append({
            "from_scene": from_idx,
            "to_scene": to_idx,
            "camera_motion": camera_motion,
            "duration_s": t.get("duration_s", duration_per_transition),
            "description": t.get("description", ""),
            "t2v_prompt": video_recipe["positive"],
            "t2v_negative": video_recipe["negative"],
            "keyframes": video_recipe.get("keyframes", []),
        })

    return {
        "version": VERSION,
        "title": plan.get("title", ""),
        "logline": plan.get("logline", ""),
        "narrative_arc": plan.get("narrative_arc", ""),
        "preset": preset_resolved,
        "mix_secondary": mix_secondary,
        "aspect": aspect,
        "i2i_model": i2i_model,
        "t2v_model": t2v_model,
        "base_seed": base_seed,
        "total_scenes": len(scene_prompts),
        "total_transitions": len(transition_prompts),
        "estimated_duration_s": plan.get("total_duration_s")
                                or sum(t["duration_s"] for t in transition_prompts) + 2 * len(scene_prompts),
        "scenes": scene_prompts,
        "transitions": transition_prompts,
        "_claude": plan.get("_usage", {}),
    }


# ─────────────────────────────────────────────────────────
# 输出
# ─────────────────────────────────────────────────────────
def write_storyboard_files(result: Dict, output_dir: str) -> List[str]:
    """把 storyboard 写到多个文件。"""
    os.makedirs(output_dir, exist_ok=True)
    written = []

    # 1. scenes.json
    p = os.path.join(output_dir, "storyboard.json")
    with open(p, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    written.append(p)

    # 2. 每个 scene 的 t2i_prompt
    for s in result["scenes"]:
        idx = s["index"]
        p = os.path.join(output_dir, f"scene-{idx:02d}-t2i.txt")
        with open(p, "w", encoding="utf-8") as f:
            f.write(f"# Scene {idx}: {s['subject']}\n")
            f.write(f"# 角色: {s['narrative_role']}\n\n")
            f.write("## Positive\n")
            f.write(s["t2i_prompt"] + "\n\n")
            f.write("## Negative\n")
            f.write(s["t2i_negative"] + "\n")
        written.append(p)

    # 3. 每个 transition 的 t2v_prompt
    for t in result["transitions"]:
        p = os.path.join(output_dir, f"transition-{t['from_scene']:02d}-to-{t['to_scene']:02d}-t2v.txt")
        with open(p, "w", encoding="utf-8") as f:
            f.write(f"# Transition: scene {t['from_scene']} → {t['to_scene']}\n")
            f.write(f"# 镜头: {t['camera_motion']}\n")
            f.write(f"# 时长: {t['duration_s']}s\n\n")
            f.write("## Positive\n")
            f.write(t["t2v_prompt"] + "\n\n")
            f.write("## Negative\n")
            f.write(t["t2v_negative"] + "\n")
        written.append(p)

    # 4. README.md（可读总览）
    p = os.path.join(output_dir, "README.md")
    lines = [
        f"# {result['title']}",
        "",
        f"> {result['logline']}",
        "",
        f"**叙事弧**: {result['narrative_arc']}",
        "",
        f"- 预设: {result['preset']}" + (f" + {result['mix_secondary']}" if result['mix_secondary'] else ""),
        f"- 画幅: {result['aspect']}",
        f"- 总场景: {result['total_scenes']} | 转场: {result['total_transitions']}",
        f"- 估算时长: {result['estimated_duration_s']} s",
        f"- I2I 模型: {result['i2i_model']} | T2V 模型: {result['t2v_model']}",
        f"- 锁定 seed: {result['base_seed']}",
        "",
        "## 场景",
        "",
    ]
    for s in result["scenes"]:
        lines.append(f"### Scene {s['index']}: {s['subject']}")
        lines.append("")
        lines.append(f"**角色**: {s['narrative_role']}  |  **构图**: {s['composition']}  |  **氛围**: {s['lighting_atmosphere']}")
        lines.append("")
        lines.append(f"📷 T2I prompt → 见 `scene-{s['index']:02d}-t2i.txt`")
        lines.append("")

    lines.append("## 转场")
    lines.append("")
    for t in result["transitions"]:
        lines.append(f"### Scene {t['from_scene']} → {t['to_scene']}（{t['duration_s']}s）")
        lines.append("")
        lines.append(f"**镜头**: {t['camera_motion']}")
        lines.append("")
        lines.append(f"{t['description']}")
        lines.append("")
        lines.append(f"🎥 T2V prompt → 见 `transition-{t['from_scene']:02d}-to-{t['to_scene']:02d}-t2v.txt`")
        lines.append("")

    lines.append("## 生产管线")
    lines.append("")
    lines.append("```bash")
    lines.append("# Step 1: 出每个 scene 的关键帧（T2I）")
    lines.append("for f in scene-*.txt; do")
    lines.append("  cat $f | grep -A100 '## Positive' | tail -1")
    lines.append("  # 喂给 Midjourney / DALL-E / SD ...")
    lines.append("done")
    lines.append("")
    lines.append("# Step 2: 出每个 transition 的衔接（T2V）")
    lines.append("for f in transition-*.txt; do")
    lines.append("  cat $f | grep -A100 '## Positive' | tail -1")
    lines.append("  # 喂给 Sora / Kling / Runway ...")
    lines.append("done")
    lines.append("")
    lines.append("# Step 3: 剪辑串联")
    lines.append("# scenes 用作关键帧定格；transitions 填充帧间动画")
    lines.append("```")
    lines.append("")
    lines.append(f"由 huo15-img-prompt v{result['version']} 故事板模式生成。")

    with open(p, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    written.append(p)

    return written


def print_storyboard_summary(result: Dict):
    sep = "═" * 60
    print(f"\n{sep}")
    print(f"🎬 故事板 v{result['version']}")
    print(f"📌 标题: {result['title']}")
    print(f"📝 简介: {result['logline']}")
    print(f"🎭 弧线: {result['narrative_arc']}")
    print(f"🎨 预设: {result['preset']}" + (f" + {result['mix_secondary']}" if result['mix_secondary'] else ""))
    print(f"📐 画幅: {result['aspect']}")
    print(f"🎲 锁定 seed: {result['base_seed']}")
    print(f"⏱  估算: {result['estimated_duration_s']}s ({result['total_scenes']} 场 + {result['total_transitions']} 转场)")
    print(f"\n📋 场景列表:")
    for s in result["scenes"]:
        print(f"  [{s['index']}] {s['subject'][:50]}")
        print(f"      角色: {s['narrative_role']} | 构图: {s['composition']} | 氛围: {s['lighting_atmosphere']}")
    print(f"\n🎥 转场:")
    for t in result["transitions"]:
        print(f"  Scene {t['from_scene']} → {t['to_scene']}: {t['camera_motion']} ({t['duration_s']}s)")
    u = result.get("_claude", {})
    print(f"\n📊 Claude token: in={u.get('input_tokens', 0)} / out={u.get('output_tokens', 0)} / cache={u.get('cache_read_input_tokens', 0)}")
    print(f"{sep}\n")


def main():
    parser = argparse.ArgumentParser(
        description=f"huo15-img-prompt storyboard v{VERSION} — 剧本→关键帧+转场 视频脚本包",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  storyboard.py "一只猫从城市走进雨夜" -p 电影感 --scenes 4 -m Midjourney --video-model Sora
  storyboard.py < script.txt --scenes 8 --output ./my_story
  storyboard.py "汉服少女夜游京都" -p 汉服写真 --scenes 6 --video-model 即梦
""",
    )
    parser.add_argument("script", nargs="?", help="剧本/文案（不给则从 stdin）")
    parser.add_argument("-p", "--preset", required=True, help="风格预设（支持 A+B 混合）")
    parser.add_argument("--scenes", type=int, default=5, help="拆几个关键帧（默认 5）")
    parser.add_argument("-a", "--aspect", default="", help="画幅（默认走预设默认）")
    parser.add_argument("-t", "--tier", choices=["basic", "pro", "master"], default="pro")
    parser.add_argument("-m", "--model", default="通用",
                        help="T2I 适配模型 Midjourney/SD/SDXL/Flux/DALL-E/通用（默认通用）")
    parser.add_argument("--video-model", default="通用",
                        help="T2V 适配模型 Sora/Kling/Runway/Pika/Luma/Hailuo/即梦/Wan/通用")
    parser.add_argument("--transition-duration", type=int, default=3,
                        help="每个转场默认时长（秒）")
    parser.add_argument("--claude-model", default=DEFAULT_MODEL,
                        help=f"Claude 模型（默认 {DEFAULT_MODEL}）")
    parser.add_argument("--output", default="", help="输出目录（不给则只打印）")
    parser.add_argument("-j", "--json", action="store_true", help="JSON 输出")
    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s v{VERSION}")
    args = parser.parse_args()

    script = args.script
    if not script:
        if sys.stdin.isatty():
            parser.print_help()
            sys.exit(1)
        script = sys.stdin.read().strip()
    if not script:
        print("❌ 剧本为空", file=sys.stderr)
        sys.exit(1)

    try:
        result = storyboard(
            script, preset=args.preset, target_scenes=args.scenes,
            i2i_model=args.model, t2v_model=args.video_model,
            aspect=args.aspect, duration_per_transition=args.transition_duration,
            quality_tier=args.tier, claude_model=args.claude_model,
        )
    except RuntimeError as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(2)

    if args.output:
        files = write_storyboard_files(result, args.output)
        result["_files_written"] = files
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print_storyboard_summary(result)
            print(f"📁 已写入 {len(files)} 个文件到 {args.output}/")
            for f in files[:5]:
                print(f"   • {f}")
            if len(files) > 5:
                print(f"   ... 还有 {len(files) - 5} 个")
    else:
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print_storyboard_summary(result)
            print("💡 加 --output ./my_story 把所有 prompt 写到文件夹\n")


if __name__ == "__main__":
    main()
