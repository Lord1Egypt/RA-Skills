#!/usr/bin/env python3
"""
huo15-img-prompt — 闭环自动迭代 v2.5

把 enhance_prompt + render_prompt + image_review 串成闭环：
  生成 → 出图 → 评审 → 不达标？让 Claude 改 prompt 再来一轮（≤ 3 轮）

这是 v2.5 的核心护城河：GPT-4o image / Imagen / Claude Imagen 内部都做不到，
因为它们的 prompt 是黑盒。我们在用户侧补这个反馈循环。

工作流（每轮）：
  Step 1: enhance_prompt 生成 recipe（首轮用基础推荐，后续用上轮 fix 后的）
  Step 2: render_prompt 出图（任意 backend）
  Step 3: image_review 五维评审
  Step 4: overall_score >= target_score → 完成
          < target_score 且 attempt < max_attempts:
            → 用 Claude 把 actionable_fixes 综合成新 prompt
            → 回 Step 1
  Step 5: 返回历史最高分图 + 全过程 trace

调用：
  auto_iterate.py "持剑女侠" -p 赛博朋克 --backend dalle --target 7.5
  auto_iterate.py "汉服少女" -p 汉服写真 --backend jimeng --max-rounds 3
  auto_iterate.py "敦煌神女" -p 敦煌壁画 --backend none --no-render   # 评审现有 recipe，不真出图

依赖：
  - 同目录 enhance_prompt.py / render_prompt.py / image_review.py
  - ANTHROPIC_API_KEY（评审 + 改 prompt）
  - 后端对应的 API key（DALL-E / Replicate / 即梦 / 可灵 等）
"""

import sys
import os
import json
import time
import argparse
from typing import Dict, List, Optional
from urllib.request import Request, urlopen
from urllib.error import HTTPError

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from enhance_prompt import (
    build_prompt, parse_mix_preset, resolve_preset,
    parse_requirement, STYLE_PRESETS, ASPECT_TO_SDXL,
)
from image_review import review_image, parse_review_json, ANTHROPIC_BASE, ANTHROPIC_VERSION

VERSION = "3.1.0"
DEFAULT_MODEL = "claude-sonnet-4-5"
DEFAULT_TARGET_SCORE = 7.5
DEFAULT_MAX_ROUNDS = 3


# ─────────────────────────────────────────────────────────
# Claude 改 prompt（基于上轮评审）
# ─────────────────────────────────────────────────────────
REVISION_SYSTEM_PROMPT = """你是 prompt revision 专家，给定一张图的 5 维评审，输出改进版 prompt。

# 工作流
1. 读 actionable_fixes（按优先级，high 必处理）
2. 读 issues（避免下轮重蹈覆辙）
3. 读 good_points（保留这些优势）
4. 输出新 prompt（只输出主体描述部分，不要带 style/camera/lighting 模板，因为 enhance_prompt.py 会再加这些锁）

# 输出 JSON 严格 schema

```json
{
  "revised_subject": "改进后的主体描述（中文，可加视觉细节），喂给 enhance_prompt.py 的 subject 参数",
  "preset_change": null,
  "extra_negatives": ["补充负面词 1", "补充负面词 2"],
  "extra_mood": "如需更改情绪覆盖（无则空）",
  "extra_composition": "如需更改构图覆盖（无则空）",
  "rationale": "中文一句话说明这次改动针对哪个维度的 issue"
}
```

`preset_change` 只在评审里明确说"风格不对"时改，否则保持 null。

只输出 JSON，不要解释。"""


def call_claude_revise(original_subject: str, original_preset: str,
                       review: Dict, model: str = DEFAULT_MODEL) -> Dict:
    """让 Claude 基于 review 输出改进 subject。"""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("缺少 ANTHROPIC_API_KEY")

    review_summary = {
        "overall_score": review.get("overall_score", 0),
        "verdict": review.get("verdict", "?"),
        "summary": review.get("summary", ""),
        "actionable_fixes": review.get("actionable_fixes", []),
        "weak_dimensions": [],
    }
    for dim in ("subject_match", "composition", "lighting", "palette", "technical"):
        d = review.get(dim, {})
        score = d.get("score", 0)
        if score < 7:
            review_summary["weak_dimensions"].append({
                "dim": dim, "score": score, "issues": d.get("issues", []),
            })

    user_msg = f"""<original>
subject: {original_subject}
preset: {original_preset}
</original>

<review>
{json.dumps(review_summary, ensure_ascii=False, indent=2)}
</review>

请输出改进后的 JSON。"""

    body = {
        "model": model,
        "max_tokens": 1500,
        "system": [{
            "type": "text",
            "text": REVISION_SYSTEM_PROMPT,
            "cache_control": {"type": "ephemeral"},
        }],
        "messages": [
            {"role": "user", "content": user_msg},
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
        with urlopen(req, timeout=60) as r:
            resp = json.loads(r.read().decode("utf-8"))
    except HTTPError as e:
        raise RuntimeError(f"Claude HTTP {e.code}: {e.read().decode('utf-8', errors='replace')}")

    return parse_review_json(resp)


# ─────────────────────────────────────────────────────────
# 后端调用（直接 import render_prompt 函数，不重复实现）
# ─────────────────────────────────────────────────────────
def render_via_backend(backend: str, recipe: Dict, aspect: str, output_dir: str,
                       remote_model: str = "", steps: int = 25, cfg: float = 7.0) -> Dict:
    """统一 backend dispatch，复用 render_prompt 内部函数。"""
    from render_prompt import (
        render_dalle, render_sdwebui, render_comfyui,
        render_replicate, render_fal,
        render_jimeng, render_kling, render_hailuo,
        DALLE_SIZES,
    )

    seed = recipe["seed_suggestion"]
    pos, neg = recipe["positive"], recipe["negative"]

    if backend == "dalle":
        size = DALLE_SIZES.get(aspect, "1024x1024")
        return render_dalle(pos, size, output_dir)
    elif backend == "sd-webui":
        return render_sdwebui(pos, neg, aspect, seed, steps, cfg, "DPM++ 2M Karras", output_dir)
    elif backend == "comfyui":
        return render_comfyui(pos, neg, aspect, seed, steps, cfg, None, output_dir)
    elif backend == "replicate":
        ref = remote_model or "black-forest-labs/flux-schnell"
        return render_replicate(pos, neg, aspect, seed, ref, output_dir, steps=steps, cfg=cfg)
    elif backend == "fal":
        ref = remote_model or "fal-ai/flux/schnell"
        return render_fal(pos, neg, aspect, seed, ref, output_dir, steps=steps)
    elif backend == "jimeng":
        return render_jimeng(pos, neg, aspect, seed, output_dir)
    elif backend == "kling":
        return render_kling(pos, neg, aspect, seed, output_dir)
    elif backend in ("hailuo", "minimax"):
        return render_hailuo(pos, neg, aspect, seed, output_dir)
    else:
        raise RuntimeError(f"未知 backend: {backend}")


# ─────────────────────────────────────────────────────────
# 闭环主流程
# ─────────────────────────────────────────────────────────
def auto_iterate(
    subject: str,
    preset: str,
    backend: str,
    target_score: float = DEFAULT_TARGET_SCORE,
    max_rounds: int = DEFAULT_MAX_ROUNDS,
    aspect: str = "",
    model_adapt: str = "SDXL",
    output_dir: str = "./renders",
    remote_model: str = "",
    no_render: bool = False,
    quality_tier: str = "pro",
    seed: Optional[int] = None,
) -> Dict:
    """主闭环。返回 trace + 最佳轮次。"""
    primary_raw, secondary_raw = parse_mix_preset(preset)
    if secondary_raw:
        primary = resolve_preset(primary_raw)
        secondary = resolve_preset(secondary_raw)
        if not primary or not secondary:
            raise RuntimeError(f"未知预设: {primary_raw} 或 {secondary_raw}")
        preset_resolved, mix_secondary = primary, secondary
    else:
        preset_resolved, mix_secondary = (resolve_preset(primary_raw) or "写实摄影"), None

    auto = parse_requirement(subject)
    if not aspect:
        aspect = auto["aspect_suggestion"] or STYLE_PRESETS.get(preset_resolved, {}).get("aspect", "1:1")

    rounds: List[Dict] = []
    current_subject = subject
    current_extra_neg = ""
    current_mood = ""
    current_composition = ""
    locked_seed = seed  # 整轮锁同一 seed，便于对比

    for attempt in range(1, max_rounds + 1):
        print(f"\n🔄 第 {attempt}/{max_rounds} 轮...", file=sys.stderr)

        recipe = build_prompt(
            current_subject, preset_resolved, model_adapt, aspect,
            extra_mood=current_mood, extra_composition=current_composition,
            extra_negatives=current_extra_neg,
            seed=locked_seed,
            quality_tier=quality_tier,
            mix_secondary=mix_secondary,
        )
        if locked_seed is None:
            locked_seed = recipe["seed_suggestion"]
        round_data = {"attempt": attempt, "subject": current_subject, "recipe": recipe}

        if no_render:
            print(f"   🧪 dry-run 模式：不出图，仅评审 prompt 文本（跳过本轮，需 --no-render 配合外部出图）", file=sys.stderr)
            round_data["skipped"] = "no-render mode (cannot review without image)"
            rounds.append(round_data)
            break

        # 出图
        try:
            print(f"   🎨 出图: backend={backend}", file=sys.stderr)
            render = render_via_backend(backend, recipe, aspect, output_dir,
                                        remote_model=remote_model)
        except Exception as e:
            round_data["render_error"] = str(e)
            rounds.append(round_data)
            print(f"   ❌ 出图失败: {e}", file=sys.stderr)
            break

        saved = render.get("saved", [])
        if not saved:
            round_data["render_error"] = "no images saved"
            rounds.append(round_data)
            break

        round_data["image_path"] = saved[0]
        round_data["render"] = render

        # 评审
        try:
            print(f"   🔍 Claude Vision 评审...", file=sys.stderr)
            review = review_image(saved[0], prompt=recipe["positive"][:500],
                                  quick=False, model=DEFAULT_MODEL)
        except Exception as e:
            round_data["review_error"] = str(e)
            rounds.append(round_data)
            print(f"   ❌ 评审失败: {e}", file=sys.stderr)
            break

        round_data["review"] = review
        score = review.get("overall_score", 0)
        verdict = review.get("verdict", "?")
        print(f"   📊 得分: {score:.1f}/10 → {verdict}", file=sys.stderr)
        rounds.append(round_data)

        # 收敛？
        if score >= target_score:
            print(f"   ✅ 达标 ({score:.1f} ≥ {target_score})，停止迭代", file=sys.stderr)
            break

        if attempt >= max_rounds:
            print(f"   ⏱  达到最大轮次 {max_rounds}", file=sys.stderr)
            break

        # 让 Claude 改 prompt
        try:
            print(f"   ✏️  让 Claude 改 prompt...", file=sys.stderr)
            revision = call_claude_revise(current_subject, preset_resolved, review)
        except Exception as e:
            round_data["revision_error"] = str(e)
            print(f"   ⚠️  改 prompt 失败: {e}，停止迭代", file=sys.stderr)
            break

        round_data["revision"] = revision
        if revision.get("revised_subject"):
            current_subject = revision["revised_subject"]
            print(f"   📝 新 subject: {current_subject}", file=sys.stderr)
        if revision.get("extra_negatives"):
            extras = ", ".join(revision["extra_negatives"])
            current_extra_neg = f"{current_extra_neg}, {extras}".strip(", ")
        if revision.get("extra_mood"):
            current_mood = revision["extra_mood"]
        if revision.get("extra_composition"):
            current_composition = revision["extra_composition"]

    # 选出最佳轮
    best_round = max(
        [r for r in rounds if r.get("review", {}).get("overall_score") is not None],
        key=lambda r: r["review"]["overall_score"],
        default=None,
    )

    return {
        "version": VERSION,
        "subject": subject,
        "preset": preset,
        "backend": backend,
        "target_score": target_score,
        "max_rounds": max_rounds,
        "rounds": rounds,
        "rounds_executed": len(rounds),
        "best_round": best_round,
        "best_score": best_round["review"]["overall_score"] if best_round else None,
        "best_image": best_round.get("image_path") if best_round else None,
    }


def print_summary(result: Dict):
    sep = "═" * 60
    print(f"\n{sep}")
    print(f"🔁 闭环自动迭代结果 v{result['version']}")
    print(f"📌 主体: {result['subject']}")
    print(f"🎨 预设: {result['preset']}")
    print(f"🔧 后端: {result['backend']}")
    print(f"🎯 目标: {result['target_score']:.1f}/10  最大 {result['max_rounds']} 轮")
    print(f"📊 实际: {result['rounds_executed']} 轮")
    print(f"\n{sep}")

    for r in result["rounds"]:
        attempt = r["attempt"]
        score = r.get("review", {}).get("overall_score")
        verdict = r.get("review", {}).get("verdict", "?")
        if score is None:
            err = r.get("render_error") or r.get("review_error") or r.get("revision_error") or r.get("skipped", "?")
            print(f"\n  轮 {attempt}: ❌ {err}")
            continue
        emoji = "🟢" if score >= 7.5 else ("🟡" if score >= 5 else "🔴")
        print(f"\n  轮 {attempt}: {emoji} {score:.1f}/10 → {verdict}")
        print(f"     图: {r.get('image_path', '?')}")
        print(f"     subject: {r.get('subject', '')[:80]}")
        if r.get("revision", {}).get("rationale"):
            print(f"     ✏️  下轮理由: {r['revision']['rationale']}")

    if result["best_round"]:
        print(f"\n{sep}")
        print(f"🏆 最佳轮: 第 {result['best_round']['attempt']} 轮  得分 {result['best_score']:.1f}/10")
        print(f"📷 文件: {result['best_image']}")
    print(f"{sep}\n")


def main():
    parser = argparse.ArgumentParser(
        description=f"huo15-img-prompt auto_iterate v{VERSION} — 闭环自动迭代",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  auto_iterate.py "持剑女侠" -p 赛博朋克 --backend dalle --target 7.5
  auto_iterate.py "汉服少女" -p 汉服写真 --backend jimeng --max-rounds 3
  auto_iterate.py "敦煌神女" -p 敦煌壁画 --backend replicate \\
                  --remote-model black-forest-labs/flux-schnell

环境变量:
  ANTHROPIC_API_KEY   必填（评审 + 改 prompt）
  + 后端对应的 API key（OPENAI_API_KEY / REPLICATE_API_TOKEN / ARK_API_KEY 等）
""",
    )
    parser.add_argument("subject", help="主体描述")
    parser.add_argument("-p", "--preset", required=True, help="风格预设（支持 A+B 混合）")
    parser.add_argument("-a", "--aspect", default="", help="画幅")
    parser.add_argument("-t", "--tier", choices=["basic", "pro", "master"], default="pro")
    parser.add_argument("-m", "--model", default="SDXL", help="提示词模型适配（不影响 backend）")
    parser.add_argument("--backend", required=True,
                        choices=["dalle", "sd-webui", "comfyui",
                                 "replicate", "fal", "jimeng", "kling", "hailuo", "minimax"],
                        help="出图后端")
    parser.add_argument("--remote-model", default="", help="Replicate/Fal 模型 ref")
    parser.add_argument("--target", type=float, default=DEFAULT_TARGET_SCORE,
                        help=f"目标分数 0-10（默认 {DEFAULT_TARGET_SCORE}）")
    parser.add_argument("--max-rounds", type=int, default=DEFAULT_MAX_ROUNDS,
                        help=f"最大迭代轮数（默认 {DEFAULT_MAX_ROUNDS}）")
    parser.add_argument("--output", default="./renders", help="输出目录")
    parser.add_argument("--seed", type=int, help="种子（不给则按 subject+preset 哈希）")
    parser.add_argument("--no-render", action="store_true",
                        help="不真出图，仅生成 recipe（用于测试 prompt revision 链路）")
    parser.add_argument("-j", "--json", action="store_true", help="JSON 输出")
    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s v{VERSION}")
    args = parser.parse_args()

    try:
        result = auto_iterate(
            subject=args.subject,
            preset=args.preset,
            backend=args.backend,
            target_score=args.target,
            max_rounds=args.max_rounds,
            aspect=args.aspect,
            model_adapt=args.model,
            output_dir=args.output,
            remote_model=args.remote_model,
            no_render=args.no_render,
            quality_tier=args.tier,
            seed=args.seed,
        )
    except RuntimeError as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(2)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_summary(result)


if __name__ == "__main__":
    main()
