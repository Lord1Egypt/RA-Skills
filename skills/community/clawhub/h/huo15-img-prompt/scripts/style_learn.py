#!/usr/bin/env python3
"""
huo15-img-prompt — 风格学习引擎 v3.0

给 N 张参考图（用户喜欢的风格样本），用 Claude Vision 提取每张的视觉特征，
综合归纳出共性 → 生成一个新的"learned preset"，存到 ~/.huo15/learned_presets/<name>.json。

后续 enhance_prompt.py 用 `-p @<name>` 复用这个学到的风格。

工作流：
  Step 1: 对每张参考图调 Claude Vision 提取 tags / camera / lighting / palette
  Step 2: 用 Claude 综合 N 张图的共性，输出统一风格 spec
  Step 3: 保存为 learned preset，schema 与 STYLE_PRESETS 兼容

调用：
  style_learn.py --name 我的小清新 ref1.jpg ref2.jpg ref3.jpg
  style_learn.py --list                                # 列出所有 learned presets
  style_learn.py --show 我的小清新                      # 详情
  style_learn.py --delete 旧风格                        # 删除
  enhance_prompt.py "猫咪" -p "@我的小清新"             # 在出图时复用

依赖：
  - 同目录 image_review.py (Claude Vision)
  - ANTHROPIC_API_KEY
"""

import sys
import os
import json
import re
import time
import argparse
from typing import Dict, List, Optional
from urllib.request import Request, urlopen
from urllib.error import HTTPError

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from image_review import call_claude_vision, parse_review_json, ANTHROPIC_BASE, ANTHROPIC_VERSION

VERSION = "3.1.0"
DEFAULT_MODEL = "claude-sonnet-4-5"
LEARNED_DIR = os.path.expanduser("~/.huo15/learned_presets")


def safe_name(name: str) -> str:
    return re.sub(r"[^\w\-]", "_", name)


def learned_path(name: str) -> str:
    return os.path.join(LEARNED_DIR, f"{safe_name(name)}.json")


# ─────────────────────────────────────────────────────────
# 单图特征提取（用 Claude Vision 但不是评分模式）
# ─────────────────────────────────────────────────────────
EXTRACT_SYSTEM_PROMPT = """你是图像视觉风格分析师。给一张图，提取它的可复现视觉风格 spec，输出严格 JSON：

```json
{
  "tags": "用 5-8 个英文风格标签描述这张图，逗号分隔（例：'cinematic, anamorphic, golden hour, dreamy bokeh'）",
  "camera": "镜头/视角/焦段（英文，例：'85mm telephoto, low angle, shallow depth of field'）",
  "lighting": "光影描述（英文，例：'warm golden hour rim light, soft fill, cinematic glow'）",
  "palette": "主色板（英文，例：'muted teal and orange, warm amber highlights, soft pastels'）",
  "aspect": "推断画幅 1:1/3:4/4:3/16:9/9:16/21:9 之一",
  "subject_type": "主体类型（人像/风景/物品/抽象 等）",
  "mood": "情绪关键词（中英混合）",
  "key_elements": ["3-5 个关键视觉元素"],
  "neg_to_avoid": "应该避免出现的事物（英文，逗号分隔）"
}
```

只输出 JSON，不要解释。"""


def extract_image_style(image_src: str, model: str = DEFAULT_MODEL) -> Dict:
    """调 Claude Vision 提取一张图的视觉特征。"""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("缺少 ANTHROPIC_API_KEY")

    from image_review import load_image_b64
    img_b64, media_type = load_image_b64(image_src)

    body = {
        "model": model,
        "max_tokens": 1500,
        "system": [{
            "type": "text",
            "text": EXTRACT_SYSTEM_PROMPT,
            "cache_control": {"type": "ephemeral"},
        }],
        "messages": [
            {"role": "user", "content": [
                {"type": "image", "source": {"type": "base64", "media_type": media_type, "data": img_b64}},
                {"type": "text", "text": "请提取这张图的视觉风格 spec，输出 JSON。"},
            ]},
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

    return parse_review_json(resp)


# ─────────────────────────────────────────────────────────
# N 张图综合 → 共性 spec
# ─────────────────────────────────────────────────────────
SYNTHESIZE_SYSTEM_PROMPT = """你是视觉风格提炼师。给定 N 张参考图各自的风格 spec，提炼共性，输出一个统一的 huo15-img-prompt preset 定义。

# 输出 JSON 严格 schema（与 STYLE_PRESETS 兼容）

```json
{
  "category": "推断分类（摄影/动漫/插画/3D/设计/艺术/场景/游戏/东方 之一）",
  "tags": "5-10 个英文风格标签（必须是 N 张图共有的特征，去掉只在 1-2 张出现的）",
  "quality": "画质修饰词（英文，例：'masterpiece, raw photo, kodak portra 400 film stock'）",
  "neg": "负面词（英文逗号分隔，从 N 张图的 neg_to_avoid 综合）",
  "camera": "共性镜头（英文）",
  "lighting": "共性光影（英文）",
  "palette": "共性色板（英文）",
  "aspect": "最常出现的画幅",
  "synthesis_notes": "中文一句话说明这风格的精髓",
  "best_subject_examples": ["这风格适合画什么的 3 个例子"],
  "confidence": 0.0-1.0
}
```

# 关键

- 至少 50% 参考图共有的特征才算"共性"
- 只出现在 1 张图的特征忽略
- tags 不要互相矛盾（"vintage" 和 "futuristic" 不应同时出现）
- confidence 反映共性强度：> 0.7 才适合做新预设；< 0.5 说明 N 张图风格太散

只输出 JSON，不要解释。"""


def synthesize_style(per_image_specs: List[Dict], model: str = DEFAULT_MODEL) -> Dict:
    """让 Claude 综合 N 张图的共性。"""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("缺少 ANTHROPIC_API_KEY")

    user_msg = f"""<reference_images_specs count="{len(per_image_specs)}">
{json.dumps(per_image_specs, ensure_ascii=False, indent=2)}
</reference_images_specs>

请综合这 {len(per_image_specs)} 张图的共性，输出统一的 preset 定义 JSON。"""

    body = {
        "model": model,
        "max_tokens": 2000,
        "temperature": 0.5,
        "system": [{
            "type": "text",
            "text": SYNTHESIZE_SYSTEM_PROMPT,
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
# 主流程
# ─────────────────────────────────────────────────────────
def learn_style(name: str, images: List[str], model: str = DEFAULT_MODEL) -> Dict:
    """主入口：N 张图 → learned preset。"""
    if len(images) < 2:
        raise RuntimeError("至少需要 2 张参考图")

    per_image = []
    for i, img in enumerate(images, 1):
        print(f"  🔍 提取第 {i}/{len(images)} 张: {img}", file=sys.stderr)
        spec = extract_image_style(img, model=model)
        spec["_source"] = img
        per_image.append(spec)

    print(f"  ✏️  综合 {len(per_image)} 张图的共性...", file=sys.stderr)
    synthesized = synthesize_style(per_image, model=model)

    learned = {
        "name": name,
        "version": VERSION,
        "created_at": int(time.time()),
        "use_count": 0,
        "category": synthesized.get("category", "学习"),
        "tags": synthesized.get("tags", ""),
        "quality": synthesized.get("quality", "high quality, detailed"),
        "neg": synthesized.get("neg", "low quality, blurry"),
        "camera": synthesized.get("camera", ""),
        "lighting": synthesized.get("lighting", ""),
        "palette": synthesized.get("palette", ""),
        "aspect": synthesized.get("aspect", "1:1"),
        "synthesis_notes": synthesized.get("synthesis_notes", ""),
        "best_subject_examples": synthesized.get("best_subject_examples", []),
        "confidence": synthesized.get("confidence", 0.5),
        "source_count": len(images),
        "source_images": images,
        "per_image_specs": per_image,
    }

    os.makedirs(LEARNED_DIR, exist_ok=True)
    with open(learned_path(name), "w", encoding="utf-8") as f:
        json.dump(learned, f, ensure_ascii=False, indent=2)

    return learned


def learned_load(name: str) -> Optional[Dict]:
    p = learned_path(name)
    if not os.path.isfile(p):
        return None
    try:
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return None


def learned_list() -> List[Dict]:
    if not os.path.isdir(LEARNED_DIR):
        return []
    out = []
    for fn in sorted(os.listdir(LEARNED_DIR)):
        if not fn.endswith(".json"):
            continue
        try:
            with open(os.path.join(LEARNED_DIR, fn), "r", encoding="utf-8") as f:
                out.append(json.load(f))
        except (json.JSONDecodeError, IOError):
            continue
    return out


def learned_delete(name: str) -> bool:
    p = learned_path(name)
    if os.path.isfile(p):
        os.remove(p)
        return True
    return False


def print_learned(p: Dict):
    print(f"\n🎨 @{p['name']}")
    print(f"  分类: {p.get('category', '?')}")
    print(f"  Confidence: {p.get('confidence', 0):.2f}")
    print(f"  来源: {p.get('source_count', 0)} 张图")
    print(f"  用过: {p.get('use_count', 0)} 次")
    print(f"  风格标签: {p.get('tags', '')[:120]}")
    if p.get("camera"):
        print(f"  相机: {p['camera']}")
    if p.get("lighting"):
        print(f"  光影: {p['lighting']}")
    if p.get("palette"):
        print(f"  色板: {p['palette']}")
    if p.get("synthesis_notes"):
        print(f"\n  📝 精髓: {p['synthesis_notes']}")
    if p.get("best_subject_examples"):
        print(f"  💡 适合画:")
        for e in p["best_subject_examples"]:
            print(f"     • {e}")


def main():
    parser = argparse.ArgumentParser(
        description=f"huo15-img-prompt style_learn v{VERSION} — 风格学习引擎",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  style_learn.py --name 我的小清新 ref1.jpg ref2.jpg ref3.jpg
  style_learn.py --list
  style_learn.py --show 我的小清新
  style_learn.py --delete 旧风格

✨ 在 enhance_prompt.py 里使用:
  enhance_prompt.py "猫咪" -p "@我的小清新"
""",
    )
    g = parser.add_mutually_exclusive_group(required=True)
    g.add_argument("--name", help="给学到的风格起个名字（配合 image 参数）")
    g.add_argument("--list", action="store_true", help="列出所有 learned preset")
    g.add_argument("--show", help="显示详情")
    g.add_argument("--delete", help="删除")

    parser.add_argument("images", nargs="*", help="参考图路径或 URL（≥2 张）")
    parser.add_argument("--model", default=DEFAULT_MODEL, help=f"Claude 模型（默认 {DEFAULT_MODEL}）")
    parser.add_argument("-j", "--json", action="store_true", help="JSON 输出")
    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s v{VERSION}")
    args = parser.parse_args()

    if args.list:
        ps = learned_list()
        if args.json:
            print(json.dumps({"version": VERSION, "learned_presets": ps}, ensure_ascii=False, indent=2))
            return
        if not ps:
            print(f"\n📭 暂无 learned preset ({LEARNED_DIR})")
            print("💡 创建：style_learn.py --name 我的风格 ref1.jpg ref2.jpg ref3.jpg\n")
            return
        print(f"\n🎨 Learned Presets ({len(ps)} 个):")
        for p in ps:
            print(f"  • @{p['name']:20s}  {p.get('category', '?'):10s}  conf={p.get('confidence', 0):.2f}  {p.get('source_count', 0)} 图  用过 {p.get('use_count', 0)} 次")
        print()
        return

    if args.show:
        p = learned_load(args.show)
        if not p:
            print(f"❌ 不存在: {args.show}", file=sys.stderr)
            sys.exit(1)
        if args.json:
            print(json.dumps(p, ensure_ascii=False, indent=2))
        else:
            print_learned(p)
            print()
        return

    if args.delete:
        if learned_delete(args.delete):
            print(f"✅ 已删除: @{args.delete}")
        else:
            print(f"❌ 不存在: {args.delete}", file=sys.stderr)
            sys.exit(1)
        return

    if args.name:
        if not args.images:
            print(f"❌ 至少需要 2 张参考图", file=sys.stderr)
            sys.exit(1)
        try:
            learned = learn_style(args.name, args.images, model=args.model)
        except RuntimeError as e:
            print(f"❌ {e}", file=sys.stderr)
            sys.exit(2)
        if args.json:
            print(json.dumps(learned, ensure_ascii=False, indent=2))
        else:
            print_learned(learned)
            print(f"\n✅ 已保存: ~/.huo15/learned_presets/{safe_name(args.name)}.json")
            print(f"💡 使用: enhance_prompt.py \"主体\" -p \"@{args.name}\"\n")


if __name__ == "__main__":
    main()
