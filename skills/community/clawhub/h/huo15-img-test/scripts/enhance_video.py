#!/usr/bin/env python3
"""
huo15-img-test — T2V 视频提示词增强脚本 v2.2

把 enhance_prompt.py 的 88 风格预设 + 一致性锁，扩展到视频维度：
  - 镜头运动（推/拉/摇/移/跟/环绕/手持/无人机...）
  - 节奏（缓慢 / 中速 / 紧张快切）
  - 时长（建议秒数 + 关键帧拆分）
  - 主体动作（自动从描述中抽词，或显式 --action）
  - 模型适配：Sora / Kling 可灵 / Runway Gen-3/Gen-4 / Pika / Luma DreamMachine / 即梦 / Hailuo MiniMax / Wan2.1

调用：
  enhance_video.py "雨夜霓虹街头一只猫漫步" -p 赛博朋克 -m Sora --duration 8
  enhance_video.py "汉服少女转身回眸" -p 汉服写真 -m Kling --motion 慢速跟拍
  enhance_video.py "宇宙飞船穿越星云" -p scifi -m Runway --action "ship accelerates, lens flare"

依赖：
  enhance_prompt.py 同目录（复用其预设 + 意图解析 + 一致性锁）
"""

import sys
import os
import json
import re
import argparse
import hashlib
from typing import Dict, List, Optional, Tuple

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from enhance_prompt import (
    STYLE_PRESETS,
    ALIASES,
    QUALITY_TIERS,
    resolve_preset,
    parse_requirement,
    parse_mix_preset,
    mix_presets,
    sanitize_subject,
    strip_negative_clauses,
    stable_seed,
    list_presets as list_image_presets,
)

VERSION = "2.3.0"

# ─────────────────────────────────────────────────────────
# 镜头运动（中文 → 英文 + 视频专业术语）
# ─────────────────────────────────────────────────────────
CAMERA_MOTION: Dict[str, str] = {
    "推": "slow push-in (dolly in)",
    "推镜": "smooth dolly in, gradual close-up",
    "拉": "pull back (dolly out)",
    "拉镜": "slow pull back revealing wider scene",
    "摇": "pan (horizontal)",
    "横摇": "horizontal pan from left to right",
    "竖摇": "vertical tilt up to down",
    "移": "lateral tracking shot",
    "跟": "tracking shot following the subject",
    "跟拍": "smooth tracking shot, subject locked in frame",
    "环绕": "360 orbital shot around the subject",
    "围绕": "360 orbit shot, slow rotation",
    "手持": "handheld camera, slight shake, documentary feel",
    "稳定": "smooth gimbal stabilized, fluid motion",
    "无人机": "aerial drone shot, high-altitude reveal",
    "航拍": "aerial drone descent, cinematic reveal",
    "升": "crane up, vertical rise",
    "降": "crane down, descent",
    "变焦": "zoom in, focal length change",
    "希区柯克": "dolly zoom (vertigo effect)",
    "希区": "dolly zoom (vertigo effect)",
    "鱼眼": "fisheye lens distortion, wide warped perspective",
    "POV": "first-person POV, immersive",
    "POV视角": "first-person POV, immersive",
    "子弹时间": "bullet-time freeze, 360 frozen pan",
    "延时": "time-lapse, accelerated motion",
    "慢动作": "slow motion 120fps, ultra-smooth",
    "快切": "rapid cuts, high-energy montage",
}

# 节奏 → 英文
PACING: Dict[str, str] = {
    "缓慢": "slow steady pacing, contemplative rhythm",
    "舒缓": "slow steady pacing, contemplative rhythm",
    "宁静": "calm, atmospheric, lingering shots",
    "中速": "moderate pacing, balanced cuts",
    "紧张": "tense pacing, building intensity",
    "急促": "fast pacing, urgent cuts",
    "快切": "rapid cuts, high-energy edit",
    "动感": "kinetic energy, dynamic motion",
    "史诗": "epic crescendo, sweeping movement",
}

# 主体动作关键词（自动抽词）
ACTION_KEYWORDS: Dict[str, str] = {
    "走": "walking forward",
    "漫步": "walking calmly",
    "奔跑": "running fast",
    "跑": "running",
    "跳": "jumping",
    "飞": "flying through the air",
    "舞": "dancing gracefully",
    "舞蹈": "dancing gracefully",
    "回眸": "turning to look back over shoulder",
    "转身": "turning around",
    "微笑": "smiling softly",
    "战斗": "fighting, dynamic combat motion",
    "挥剑": "swinging a sword",
    "射箭": "drawing and releasing an arrow",
    "骑马": "riding a horse at full gallop",
    "驾驶": "driving forward",
    "穿越": "traveling through, breaking forward",
    "升起": "rising up slowly",
    "落下": "falling down gently",
    "爆炸": "explosion blooming outward",
    "绽放": "blooming open",
    "凝视": "gazing intently into the camera",
    "对视": "locking eyes with the viewer",
    "睁眼": "eyes opening slowly",
    "闭眼": "eyes closing slowly",
    "呼吸": "breathing softly, chest rising and falling",
    "拥抱": "embracing tenderly",
    "牵手": "holding hands",
    "握手": "shaking hands",
}

# ─────────────────────────────────────────────────────────
# 模型规格
# ─────────────────────────────────────────────────────────
VIDEO_MODELS: Dict[str, Dict[str, str]] = {
    "Sora": {
        "max_duration": "20s (Sora 2 Pro)",
        "default_duration": 10,
        "aspect_default": "16:9",
        "tip": "支持长自然语言描述。可叠加 'cinematic, IMAX, 35mm film, photorealistic'。一致性强，可复用 character description。",
        "format": "natural",
    },
    "Kling": {
        "max_duration": "10s (1080p Pro)",
        "default_duration": 5,
        "aspect_default": "16:9",
        "tip": "可灵 1.6/2.0：建议提示前置主体，后置镜头/光影。支持首尾帧控制（image-to-video）。",
        "format": "natural",
    },
    "可灵": {
        "max_duration": "10s (1080p Pro)",
        "default_duration": 5,
        "aspect_default": "16:9",
        "tip": "可灵 1.6/2.0：中文提示词支持良好，可加 'cinematic 电影感'。",
        "format": "natural",
    },
    "Runway": {
        "max_duration": "10s (Gen-3 Alpha Turbo)",
        "default_duration": 5,
        "aspect_default": "16:9",
        "tip": "Gen-3 / Gen-4：英文提示效果最佳。支持 Motion Brush 局部运动。CFG ~7。",
        "format": "natural",
    },
    "Pika": {
        "max_duration": "10s (Pika 2.0)",
        "default_duration": 4,
        "aspect_default": "16:9",
        "tip": "Pika：标签式提示，支持 -gs (guidance scale) 和 -motion (1-4)。",
        "format": "tag",
    },
    "Luma": {
        "max_duration": "9s (Dream Machine 1.6)",
        "default_duration": 5,
        "aspect_default": "16:9",
        "tip": "Luma Dream Machine：自然语言 + 关键帧（首尾图）。Loop 模式支持无缝循环。",
        "format": "natural",
    },
    "DreamMachine": {
        "max_duration": "9s",
        "default_duration": 5,
        "aspect_default": "16:9",
        "tip": "Luma Dream Machine：自然语言 + 关键帧。",
        "format": "natural",
    },
    "Hailuo": {
        "max_duration": "10s (MiniMax 02 / S2V-01)",
        "default_duration": 6,
        "aspect_default": "16:9",
        "tip": "海螺 MiniMax 02：中文支持优秀。S2V-01 可指定参考人物。",
        "format": "natural",
    },
    "MiniMax": {
        "max_duration": "10s",
        "default_duration": 6,
        "aspect_default": "16:9",
        "tip": "MiniMax 视频：中英双语，长描述效果好。",
        "format": "natural",
    },
    "即梦": {
        "max_duration": "12s (Seedance 1.0)",
        "default_duration": 5,
        "aspect_default": "16:9",
        "tip": "即梦 / Seedance：抖音生态，支持中文 + 多镜头剧情连贯。",
        "format": "natural",
    },
    "Seedance": {
        "max_duration": "12s",
        "default_duration": 5,
        "aspect_default": "16:9",
        "tip": "Seedance 1.0：多镜头剧情连贯，支持中文。",
        "format": "natural",
    },
    "Wan": {
        "max_duration": "8s (Wan 2.1)",
        "default_duration": 4,
        "aspect_default": "16:9",
        "tip": "通义 Wan 2.1：阿里开源，I2V 支持高分辨率。中英双语提示。",
        "format": "natural",
    },
    "Wan2.1": {
        "max_duration": "8s",
        "default_duration": 4,
        "aspect_default": "16:9",
        "tip": "通义 Wan 2.1：阿里开源 14B / 1.3B 双参数。",
        "format": "natural",
    },
    "通用": {
        "max_duration": "—",
        "default_duration": 5,
        "aspect_default": "16:9",
        "tip": "通用模板：自然语言 + 镜头 + 节奏 + 主体动作。",
        "format": "natural",
    },
}

MODEL_ALIASES: Dict[str, str] = {
    "sora": "Sora", "kling": "Kling", "kelin": "Kling", "klingai": "Kling",
    "runway": "Runway", "gen3": "Runway", "gen4": "Runway",
    "pika": "Pika", "luma": "Luma", "dreammachine": "Luma",
    "hailuo": "Hailuo", "minimax": "Hailuo",
    "jimeng": "即梦", "seedance": "即梦",
    "wan": "Wan", "wan21": "Wan", "wan2.1": "Wan",
    "tongyi": "Wan",
}


def resolve_video_model(name: str) -> str:
    if not name:
        return "通用"
    key = name.strip().lower().replace("-", "").replace("_", "").replace(" ", "")
    if key in MODEL_ALIASES:
        return MODEL_ALIASES[key]
    for m in VIDEO_MODELS:
        if m.lower() == key:
            return m
    return name if name in VIDEO_MODELS else "通用"


# ─────────────────────────────────────────────────────────
# 解析
# ─────────────────────────────────────────────────────────
def parse_motion(text: str) -> str:
    for zh, en in CAMERA_MOTION.items():
        if zh in text:
            return en
    return ""


def parse_pacing(text: str) -> str:
    for zh, en in PACING.items():
        if zh in text:
            return en
    return ""


def parse_action(text: str) -> str:
    actions = []
    for zh, en in ACTION_KEYWORDS.items():
        if zh in text and en not in actions:
            actions.append(en)
    return ", ".join(actions[:3])


# ─────────────────────────────────────────────────────────
# 关键帧拆分
# ─────────────────────────────────────────────────────────
def keyframe_breakdown(subject: str, motion: str, duration: int) -> List[Dict[str, str]]:
    """简单的三段式拆分：开场（建立）→ 中段（动作）→ 结尾（落点）。"""
    if duration <= 3:
        return [{"t": "0s", "desc": f"establish shot: {subject}"}]
    third = max(1, duration // 3)
    return [
        {"t": "0s", "desc": f"opening: establish {subject} in scene, static composition"},
        {"t": f"{third}s", "desc": f"mid: {motion or 'subject performs main action'}, peak motion"},
        {"t": f"{2*third}s", "desc": f"closing: settle into resting frame, fade or hold"},
    ]


# ─────────────────────────────────────────────────────────
# 主构建
# ─────────────────────────────────────────────────────────
def build_video_prompt(
    subject: str,
    preset: str,
    model: str = "通用",
    aspect: str = "",
    duration: Optional[int] = None,
    motion: str = "",
    pacing: str = "",
    action: str = "",
    seed: Optional[int] = None,
    quality_tier: str = "pro",
    extra_negatives: str = "",
    mix_secondary: Optional[str] = None,
    mix_ratio: float = 0.6,
) -> Dict:
    preset = resolve_preset(preset) or "电影感"
    if mix_secondary:
        mix_secondary = resolve_preset(mix_secondary) or ""
    model = resolve_video_model(model)
    spec = VIDEO_MODELS[model]

    # 视觉锁（复用 image preset）
    if mix_secondary and mix_secondary != preset:
        data = mix_presets(preset, mix_secondary, mix_ratio, model)
        mixed_label = f"{preset}+{mix_secondary}@{mix_ratio:.2f}"
    else:
        data = STYLE_PRESETS[preset]
        mixed_label = ""

    # 时长 / 画幅
    if duration is None:
        duration = spec["default_duration"]
    if not aspect:
        aspect = data.get("aspect", spec["aspect_default"])

    # 自动解析
    auto = parse_requirement(subject)
    subject_clean = sanitize_subject(strip_negative_clauses(subject))
    if not motion:
        motion = parse_motion(subject) or "smooth gimbal stabilized, fluid motion"
    if not pacing:
        pacing = parse_pacing(subject) or "moderate pacing, balanced cuts"
    if not action:
        action = parse_action(subject)

    # ambient
    ambient_parts = [auto["time_of_day"], auto["weather"], auto["season"]]
    ambient = ", ".join([x for x in ambient_parts if x])

    # 视觉锁字段
    visual_lock = ", ".join([
        x for x in [data["tags"], data.get("camera", ""), data.get("lighting", ""), data.get("palette", "")] if x
    ])

    quality_phrase = QUALITY_TIERS.get(quality_tier, QUALITY_TIERS["pro"])

    seed_key = mixed_label or preset
    seed_value = seed or stable_seed(subject_clean, seed_key)

    # 构造正向提示
    if spec["format"] == "tag":  # Pika 标签格式
        parts = [
            subject_clean,
            f"{motion}",
            f"{pacing}",
            visual_lock,
            ambient,
            action,
            quality_phrase,
            "cinematic video",
        ]
        positive = ", ".join([p for p in parts if p])
        positive += f" -gs 12 -motion 3 -ar {aspect}"
    else:  # 自然语言格式
        sentences = []
        sentences.append(f"A {duration}-second video of {subject_clean}.")
        sentences.append(f"Camera movement: {motion}.")
        if action:
            sentences.append(f"The subject is {action}.")
        sentences.append(f"Pacing: {pacing}.")
        sentences.append(f"Visual style: {visual_lock}.")
        if ambient:
            sentences.append(f"Atmosphere: {ambient}.")
        sentences.append(f"Quality: {quality_phrase}, cinematic, smooth temporal coherence, no flicker, consistent character across frames.")
        positive = " ".join(sentences)

    # 负面
    base_neg = data["neg"]
    video_neg = (
        "flicker, frame drop, motion blur artifacts, jittery camera, "
        "low fps, choppy motion, morphing artifacts, identity drift, "
        "deformed limbs mid-motion, inconsistent character, watermark"
    )
    neg_parts = [base_neg, video_neg, extra_negatives, ", ".join(auto.get("user_negatives", []))]
    negative = ", ".join([x for x in neg_parts if x])

    # 关键帧
    keyframes = keyframe_breakdown(subject_clean, motion, duration)

    hint = (
        f"{model} tips：\n"
        f"  • {spec['tip']}\n"
        f"  • 推荐时长：{duration}s（上限 {spec['max_duration']}）\n"
        f"  • 一致性：i2v 模式可固定首帧角色 / 用 image-prompt 保持服装色彩\n"
        f"  • seed: {seed_value}（同一 seed + 同一 prompt 在多数模型可复现）"
    )

    return {
        "version": VERSION,
        "type": "t2v",
        "original": subject,
        "preset": preset,
        "mix_secondary": mix_secondary or "",
        "mix_label": mixed_label,
        "model": model,
        "aspect": aspect,
        "duration_s": duration,
        "max_duration": spec["max_duration"],
        "motion": motion,
        "pacing": pacing,
        "action": action,
        "time_of_day": auto.get("time_of_day", ""),
        "weather": auto.get("weather", ""),
        "season": auto.get("season", ""),
        "seed_suggestion": seed_value,
        "quality_tier": quality_tier,
        "positive": positive,
        "negative": negative,
        "keyframes": keyframes,
        "hint": hint,
        "consistency_lock": {
            "camera": data.get("camera", ""),
            "lighting": data.get("lighting", ""),
            "palette": data.get("palette", ""),
            "aspect": aspect,
            "motion": motion,
        },
    }


def print_video_prompt(r: Dict):
    sep = "═" * 60
    print(f"\n{sep}")
    print(f"🎬 视频提示词（v{r['version']}）")
    print(f"📌 原始描述   : {r['original']}")
    if r.get("mix_label"):
        print(f"🎨 风格预设   : {r['mix_label']} (混合)")
    else:
        print(f"🎨 风格预设   : {r['preset']}")
    print(f"🤖 目标模型   : {r['model']}（上限 {r['max_duration']}）")
    print(f"📐 画幅       : {r['aspect']}")
    print(f"⏱  时长       : {r['duration_s']}s")
    print(f"🎥 镜头运动   : {r['motion']}")
    print(f"🎵 节奏       : {r['pacing']}")
    if r.get("action"):
        print(f"💪 主体动作   : {r['action']}")
    if r.get("time_of_day") or r.get("weather") or r.get("season"):
        amb = ", ".join([x for x in [r.get("time_of_day", ""), r.get("weather", ""), r.get("season", "")] if x])
        print(f"🌤  环境       : {amb}")
    print(f"⭐ 质量档位   : {r['quality_tier']}")
    print(f"🎲 种子建议   : {r['seed_suggestion']}")
    print(f"\n✅ 正向提示词：\n{r['positive']}")
    print(f"\n❌ 负向提示词：\n{r['negative']}")
    print(f"\n🎞  关键帧拆分：")
    for kf in r["keyframes"]:
        print(f"   {kf['t']:>4s}  {kf['desc']}")
    print(f"\n🔒 一致性锁：")
    for k, v in r["consistency_lock"].items():
        if v:
            print(f"   {k:8s}: {v}")
    print(f"\n💡 {r['hint']}")
    print(f"{sep}\n")


def main():
    parser = argparse.ArgumentParser(
        description=f"huo15-img-test enhance_video v{VERSION} — T2V 视频提示词增强",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  enhance_video.py "雨夜霓虹街头一只猫漫步" -p 赛博朋克 -m Sora --duration 8
  enhance_video.py "汉服少女转身回眸" -p 汉服写真 -m Kling --motion 慢速跟拍
  enhance_video.py "宇宙飞船穿越星云" -p scifi -m Runway --duration 5 --pacing 史诗
  enhance_video.py "山中神女腾云" -p "原神+敦煌壁画" --mix 0.6 -m Hailuo
  enhance_video.py "侠客挥剑" -p 水墨 -m 即梦 --action "spinning sword strike"
""",
    )
    parser.add_argument("subject", nargs="?", help="主体描述")
    parser.add_argument("-p", "--preset", help="风格预设（沿用 88 款图像预设；支持 A+B 混合）")
    parser.add_argument("--mix", type=float, default=0.6, help="主预设权重 0.1-0.9（默认 0.6）")
    parser.add_argument(
        "-m", "--model", default="通用",
        help="视频模型: Sora / Kling / Runway / Pika / Luma / Hailuo / 即梦 / Wan / 通用",
    )
    parser.add_argument("-a", "--aspect", default="", help="画幅 16:9 / 9:16 / 1:1 / 21:9")
    parser.add_argument("--duration", type=int, help="时长（秒），不给走模型默认")
    parser.add_argument("--motion", default="", help="镜头运动覆盖（中/英）")
    parser.add_argument("--pacing", default="", help="节奏覆盖")
    parser.add_argument("--action", default="", help="主体动作覆盖")
    parser.add_argument("--avoid", default="", help="额外负面词")
    parser.add_argument("-t", "--tier", choices=["basic", "pro", "master"], default="pro")
    parser.add_argument("--seed", type=int, help="种子")
    parser.add_argument("-l", "--list", action="store_true", help="列出图像预设（视频沿用）")
    parser.add_argument("--list-models", action="store_true", help="列出视频模型规格")
    parser.add_argument("-j", "--json", action="store_true", help="JSON 输出")
    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s v{VERSION}")
    args = parser.parse_args()

    if args.list:
        list_image_presets()
        return

    if args.list_models:
        print(f"\n🎬 视频模型规格 (v{VERSION})\n" + "─" * 50)
        for name, spec in VIDEO_MODELS.items():
            print(f"\n【{name}】")
            print(f"  上限时长: {spec['max_duration']}")
            print(f"  默认时长: {spec['default_duration']}s")
            print(f"  默认画幅: {spec['aspect_default']}")
            print(f"  说明: {spec['tip']}")
        return

    if not args.subject:
        parser.print_help()
        sys.exit(1)

    raw_preset = args.preset or "电影感"
    primary_raw, secondary_raw = parse_mix_preset(raw_preset)
    if secondary_raw:
        primary_resolved = resolve_preset(primary_raw)
        secondary_resolved = resolve_preset(secondary_raw)
        if not primary_resolved or not secondary_resolved:
            unknown = [n for n, r in [(primary_raw, primary_resolved), (secondary_raw, secondary_resolved)] if not r]
            print(f"❌ 未知预设：{', '.join(unknown)}", file=sys.stderr)
            sys.exit(1)
        preset, mix_secondary = primary_resolved, secondary_resolved
    else:
        preset, mix_secondary = primary_raw, None

    result = build_video_prompt(
        args.subject, preset, model=args.model, aspect=args.aspect,
        duration=args.duration, motion=args.motion, pacing=args.pacing,
        action=args.action, seed=args.seed, quality_tier=args.tier,
        extra_negatives=args.avoid, mix_secondary=mix_secondary, mix_ratio=args.mix,
    )

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_video_prompt(result)


if __name__ == "__main__":
    main()
