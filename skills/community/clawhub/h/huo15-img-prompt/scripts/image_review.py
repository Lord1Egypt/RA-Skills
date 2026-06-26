#!/usr/bin/env python3
"""
huo15-img-prompt — Claude Vision 图像评审 v2.5

把 Claude Vision 当作图像质量评审师。给一张图（本地路径或 URL）+ 原 prompt，
输出五维结构化打分 + 缺陷列表 + 可执行修复建议（喂给下一轮迭代）。

为什么这个能力 GPT-4o image gen / Imagen 内部做不到？
  - 它们是端到端黑盒：prompt → 图，没有 prompt-image 闭环数据回流
  - 我们在用户侧补这个回路，每张图都能产出 "下一轮怎么改 prompt" 的可执行指令
  - 这就是 v2.5 的核心护城河：迭代提升而不是单次出图

五维评分：
  1. subject_match    主体准确度（图与 prompt 的吻合）
  2. composition      构图（黄金分割、留白、视觉层次、引导线）
  3. lighting         光影（光源逻辑、明暗关系、艺术化处理）
  4. palette          色彩（和谐度、风格一致性、色温情绪）
  5. technical        技术质量（锐度、噪点、artifact、anatomy 错误）

调用：
  image_review.py /path/to/image.png --prompt "原 prompt"
  image_review.py https://example.com/img.png -p "..." -j > review.json
  image_review.py img.png --quick               # 简评，只给 overall 分
  image_review.py a.png b.png c.png --rank      # 多图排名

依赖：纯 urllib + ANTHROPIC_API_KEY，零 SDK
"""

import sys
import os
import json
import base64
import argparse
import re
from typing import Dict, List, Optional, Tuple
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

VERSION = "3.1.0"

ANTHROPIC_BASE = os.environ.get("ANTHROPIC_BASE_URL", "https://api.anthropic.com")
ANTHROPIC_VERSION = "2023-06-01"
DEFAULT_MODEL = "claude-sonnet-4-5"


# ─────────────────────────────────────────────────────────
# 评审 system prompt（启用 prompt caching，多图调用省 90% token）
# ─────────────────────────────────────────────────────────
def build_review_system_prompt(quick: bool = False) -> str:
    if quick:
        return """你是图像质量评审师。给一张图，输出严格 JSON：
{"overall_score": 0.0-10.0, "verdict": "PASS|RETRY|REJECT", "summary": "一句话总结"}
PASS ≥ 7.5, RETRY 5-7.5, REJECT < 5。只输出 JSON。"""

    return """你是火一五图像质量评审师，专门给 T2I 出图打专业分 + 给可执行修复指令。

# 五维评分（每维 0-10 分）

1. **subject_match**（主体准确度）
   - 图中主体是否符合 prompt 描述？
   - 数量、姿态、表情、服饰、动作是否对得上？
   - 多余/缺失元素扣分

2. **composition**（构图）
   - 黄金分割 / 三分法 / 中心构图等运用是否合理？
   - 视觉重心明确吗？引导线、留白、层次？
   - 主体是否被边框切到、是否过分挤压？

3. **lighting**（光影）
   - 光源逻辑统一吗？阴影方向一致？
   - 光质（硬/软、暖/冷）是否符合 prompt 的氛围？
   - 高光/中调/暗部分布合理？过曝/欠曝？

4. **palette**（色彩）
   - 整体色调和谐吗？是否符合 prompt 风格？
   - 互补色/邻近色/单色的运用？
   - 色温情绪与主题契合？

5. **technical**（技术质量）
   - 锐度、噪点、压缩 artifact
   - 解剖错误（多指、错位、扭曲）
   - 文字渲染（如果有）
   - 边缘清晰度、纹理细节

# 输出 JSON 严格 schema

```json
{
  "subject_match": {
    "score": 8.5,
    "good_points": ["亮点 1", "亮点 2"],
    "issues": ["问题 1", "问题 2"]
  },
  "composition": {"score": ..., "good_points": [...], "issues": [...]},
  "lighting":    {"score": ..., "good_points": [...], "issues": [...]},
  "palette":     {"score": ..., "good_points": [...], "issues": [...]},
  "technical":   {"score": ..., "good_points": [...], "issues": [...]},
  "overall_score": 0.0-10.0,
  "verdict": "PASS|RETRY|REJECT",
  "actionable_fixes": [
    {
      "target": "subject_match|composition|lighting|palette|technical",
      "fix": "具体怎么改 prompt（中英混合，可直接拼接）",
      "priority": "high|medium|low"
    }
  ],
  "summary": "一句话总结这张图的最强点和最弱点"
}
```

# 评分标准

- **PASS** ≥ 7.5：可以发布
- **RETRY** 5-7.5：值得改一轮
- **REJECT** < 5：建议大改 prompt 或换风格

# 关键原则

- **actionable_fixes 必须能直接喂给下一轮 prompt** — 不要写"改善光线"，要写"add: golden hour rim light, soft fill from camera left"
- **issues 要具体** — 不要"构图不好"，要"主体偏左被切到，建议向中心移 15%"
- **good_points 也要具体** — 帮助保留下一轮的优势
- **overall_score 是加权平均**：subject_match × 0.3 + composition × 0.2 + lighting × 0.2 + palette × 0.15 + technical × 0.15

只输出 JSON，不要包 markdown 代码块，不要前缀解释。"""


# ─────────────────────────────────────────────────────────
# IO + Vision API 调用
# ─────────────────────────────────────────────────────────
def load_image_b64(src: str) -> Tuple[str, str]:
    """返回 (base64_string, media_type)。"""
    if src.startswith(("http://", "https://")):
        req = Request(src, headers={"User-Agent": "huo15-review/1.0"})
        with urlopen(req, timeout=30) as r:
            blob = r.read()
    else:
        with open(os.path.expanduser(src), "rb") as f:
            blob = f.read()

    if blob[:8] == b"\x89PNG\r\n\x1a\n":
        media = "image/png"
    elif blob[:3] == b"\xff\xd8\xff":
        media = "image/jpeg"
    elif blob[:6] in (b"GIF87a", b"GIF89a"):
        media = "image/gif"
    elif blob[:4] == b"RIFF" and blob[8:12] == b"WEBP":
        media = "image/webp"
    else:
        media = "image/png"

    return base64.b64encode(blob).decode("ascii"), media


def call_claude_vision(image_src: str, prompt: str = "", quick: bool = False,
                       model: str = DEFAULT_MODEL, max_tokens: int = 2048) -> Dict:
    """调用 Claude Vision 评审一张图。"""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("缺少 ANTHROPIC_API_KEY 环境变量")

    img_b64, media_type = load_image_b64(image_src)

    user_content = []
    user_content.append({
        "type": "image",
        "source": {"type": "base64", "media_type": media_type, "data": img_b64},
    })
    if prompt:
        user_content.append({
            "type": "text",
            "text": f"<original_prompt>{prompt}</original_prompt>\n\n请评审这张图，输出 JSON。",
        })
    else:
        user_content.append({
            "type": "text",
            "text": "请评审这张图（无原 prompt 上下文，只看视觉品质），输出 JSON。",
        })

    body = {
        "model": model,
        "max_tokens": max_tokens,
        "system": [
            {
                "type": "text",
                "text": build_review_system_prompt(quick=quick),
                "cache_control": {"type": "ephemeral"},
            }
        ],
        "messages": [
            {"role": "user", "content": user_content},
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
        with urlopen(req, timeout=180) as r:
            return json.loads(r.read().decode("utf-8"))
    except HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Claude Vision HTTP {e.code}: {err_body}")
    except URLError as e:
        raise RuntimeError(f"Claude Vision 网络错误: {e}")


def parse_review_json(resp: Dict) -> Dict:
    """从 Claude 响应中抽 JSON（已 prefill `{`）。"""
    if "error" in resp:
        raise RuntimeError(f"Claude API 错误: {resp['error']}")
    text = ""
    for block in resp.get("content", []):
        if block.get("type") == "text":
            text += block.get("text", "")
    if not text:
        raise RuntimeError(f"Claude 返回空内容")

    full = "{" + text
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
# 评分聚合 / 显示
# ─────────────────────────────────────────────────────────
SCORE_EMOJI = lambda s: "🟢" if s >= 7.5 else ("🟡" if s >= 5 else "🔴")


def review_image(src: str, prompt: str = "", quick: bool = False,
                 model: str = DEFAULT_MODEL) -> Dict:
    resp = call_claude_vision(src, prompt=prompt, quick=quick, model=model)
    parsed = parse_review_json(resp)
    parsed["_image"] = src
    return parsed


def print_review(r: Dict):
    sep = "═" * 60
    print(f"\n{sep}")
    print(f"🔍 Claude Vision 图像评审 v{VERSION}")
    print(f"📷 图像: {r.get('_image', '?')}")
    print(f"🤖 模型: {r.get('_model', '?')}")
    u = r.get("_usage", {})
    print(f"📊 token: in={u.get('input_tokens',0)} / out={u.get('output_tokens',0)}")

    overall = r.get("overall_score", 0)
    verdict = r.get("verdict", "?")
    emoji = SCORE_EMOJI(overall)
    print(f"\n{emoji} 综合评分: {overall:.1f}/10  → {verdict}")

    if r.get("summary"):
        print(f"📝 总结: {r['summary']}")

    if "subject_match" in r:  # 完整评审
        print(f"\n📐 五维分项:")
        for dim, label in [
            ("subject_match", "主体准确"), ("composition", "构图"),
            ("lighting", "光影"), ("palette", "色彩"), ("technical", "技术"),
        ]:
            d = r.get(dim, {})
            score = d.get("score", 0)
            print(f"   {SCORE_EMOJI(score)} {label:8s}: {score:4.1f}/10")
            for issue in (d.get("issues") or [])[:2]:
                print(f"      ❌ {issue}")
            for good in (d.get("good_points") or [])[:1]:
                print(f"      ✅ {good}")

    fixes = r.get("actionable_fixes", []) or []
    if fixes:
        print(f"\n🔧 可执行修复（按优先级）:")
        order = {"high": 0, "medium": 1, "low": 2}
        for f in sorted(fixes, key=lambda x: order.get(x.get("priority", "low"), 3))[:5]:
            p = f.get("priority", "low")
            mark = "🔴" if p == "high" else ("🟡" if p == "medium" else "🟢")
            print(f"   {mark} [{f.get('target', '?')}] {f.get('fix', '')}")

    print(f"{sep}\n")


def rank_images(srcs: List[str], prompt: str = "", quick: bool = True,
                model: str = DEFAULT_MODEL) -> List[Dict]:
    """多图排名：调用 review_image 然后按 overall_score 排序。"""
    results = []
    for s in srcs:
        try:
            r = review_image(s, prompt=prompt, quick=quick, model=model)
            results.append(r)
        except Exception as e:
            results.append({"_image": s, "error": str(e), "overall_score": 0})
    results.sort(key=lambda x: x.get("overall_score", 0), reverse=True)
    return results


def print_ranking(ranked: List[Dict]):
    sep = "═" * 60
    print(f"\n{sep}")
    print(f"🏆 多图评审排名 (n={len(ranked)})")
    print(f"{sep}")
    for i, r in enumerate(ranked, 1):
        score = r.get("overall_score", 0)
        emoji = SCORE_EMOJI(score)
        if r.get("error"):
            print(f"  {i}. ❌ {r.get('_image', '?')}: {r['error']}")
        else:
            print(f"  {i}. {emoji} {score:4.1f}/10  {r.get('_image', '?')}")
            if r.get("summary"):
                print(f"     {r['summary']}")
    print(f"{sep}\n")


def main():
    parser = argparse.ArgumentParser(
        description=f"huo15-img-prompt image_review v{VERSION} — Claude Vision 图像评审",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  image_review.py /path/to/image.png --prompt "原 prompt"
  image_review.py https://example.com/img.png -p "..." -j > review.json
  image_review.py img.png --quick                 # 简评只给 overall
  image_review.py a.png b.png c.png --rank        # 多图排名（自动 quick）

环境变量:
  ANTHROPIC_API_KEY   必填
""",
    )
    parser.add_argument("images", nargs="+", help="图片路径或 URL（支持多个走排名）")
    parser.add_argument("-p", "--prompt", default="", help="原始生成 prompt（评审参考）")
    parser.add_argument("--quick", action="store_true", help="简评模式（只 overall_score）")
    parser.add_argument("--rank", action="store_true", help="多图排名（自动 quick）")
    parser.add_argument("--model", default=DEFAULT_MODEL, help=f"Claude 模型（默认 {DEFAULT_MODEL}）")
    parser.add_argument("-j", "--json", action="store_true", help="JSON 输出")
    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s v{VERSION}")
    args = parser.parse_args()

    try:
        if args.rank or len(args.images) > 1:
            ranked = rank_images(args.images, prompt=args.prompt,
                                 quick=args.quick or args.rank, model=args.model)
            if args.json:
                print(json.dumps({"version": VERSION, "ranked": ranked}, ensure_ascii=False, indent=2))
            else:
                print_ranking(ranked)
        else:
            r = review_image(args.images[0], prompt=args.prompt,
                             quick=args.quick, model=args.model)
            if args.json:
                print(json.dumps(r, ensure_ascii=False, indent=2))
            else:
                print_review(r)
    except RuntimeError as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
