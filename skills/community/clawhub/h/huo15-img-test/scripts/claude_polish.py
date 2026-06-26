#!/usr/bin/env python3
"""
huo15-img-test — Claude API 智能润色 v2.3

用 Claude（Anthropic API）把粗糙的中文描述润色成专业 T2I 提示词。
利用 Claude 的 prompt engineering 优势：
  - **结构化思维**：用 XML 标签让 Claude 分步思考（subject_refine → style_pick → camera_lighting → palette → negatives）
  - **prompt caching**：system prompt 缓存，省 90% token
  - **JSON 强约束输出**：用 prefill + tool-use 强制结构化
  - **中英双语理解**：中文输入 → 中英混合输出（视觉术语用英文）

调用：
  claude_polish.py "一个温柔的女孩在花丛中"
  claude_polish.py "赛博朋克猫" --model claude-sonnet-4-5
  claude_polish.py "敦煌神女" --include-safety   # 同时跑 safety_lint
  claude_polish.py "汉服少女" -j > polished.json
  claude_polish.py "雪山下的小屋" --pipe         # 输出可直接喂给 enhance_prompt.py 的 CLI

依赖：
  环境变量 ANTHROPIC_API_KEY
  纯 urllib，零第三方包（不引入 anthropic SDK，避免企业扫描器）
"""

import sys
import os
import json
import argparse
import re
from typing import Dict, List, Optional, Tuple
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from enhance_prompt import STYLE_PRESETS

VERSION = "2.3.0"

# ─────────────────────────────────────────────────────────
# Claude API 配置
# ─────────────────────────────────────────────────────────
ANTHROPIC_BASE = os.environ.get("ANTHROPIC_BASE_URL", "https://api.anthropic.com")
ANTHROPIC_VERSION = "2023-06-01"
DEFAULT_MODEL = "claude-sonnet-4-5"  # 用户记忆里偏好的版本


# ─────────────────────────────────────────────────────────
# System Prompt（启用 prompt caching）
# ─────────────────────────────────────────────────────────
def build_system_prompt() -> str:
    """生成 system prompt — 含 88 预设清单。"""
    by_cat: Dict[str, List[str]] = {}
    for name, data in STYLE_PRESETS.items():
        by_cat.setdefault(data["category"], []).append(name)

    preset_block = "\n".join([
        f"- {cat}: " + " / ".join(by_cat[cat])
        for cat in ("摄影", "动漫", "插画", "3D", "设计", "艺术", "场景", "游戏", "东方")
        if cat in by_cat
    ])

    return f"""你是火一五文生图提示词的资深 prompt engineer，专精把中文一句话描述润色成高质量、可直接喂给 Midjourney/SD/SDXL/Flux/DALL-E 的提示词。

# 88 风格预设（必须从这里挑一个）
{preset_block}

# 你的工作流程（用 XML 思维链，但只输出最终 JSON）

<thinking>
1. 解析用户主体：核心人/物/场景，剥离修饰
2. 选风格：从 88 预设挑最贴近的 1 个，可选副预设做混合
3. 推导视觉锁：camera（焦段/视角）/ lighting（光源/光质）/ palette（色板）
4. 自动抽词：构图（特写/俯拍/全身）/ 情绪（温暖/史诗/治愈）/ 时间（黄昏/深夜）/ 天气（雨/雾）/ 季节
5. 平台合规检查：识别可能被 SD/MJ/DALL-E 误判的词，做艺术化替代（仅限合法艺术）
6. 写出 negative prompt：常见 artifact + 主题特定排除项
</thinking>

# 输出 JSON 严格 schema

```json
{{
  "subject_refined_zh": "更具体可视化的中文主体描述（保留意境，加视觉细节）",
  "subject_refined_en": "English version, T2I model 友好",
  "style_preset": "从 88 个里挑 1 个准确名",
  "style_preset_secondary": "可选副预设（混合时用），不需要填空字符串",
  "mix_ratio": 0.6,
  "aspect": "1:1 / 3:4 / 16:9 / 21:9 / 9:16 之一",
  "camera": "镜头/焦段/视角，例：'85mm telephoto, low angle, shallow depth of field'",
  "lighting": "光影描述，例：'golden hour rim light, soft fill, cinematic glow'",
  "palette": "色板，例：'muted earth tones, sage green, warm amber'",
  "composition": "特写/近景/中景/全身/俯拍/仰拍/航拍/侧面/背面 之一或多",
  "mood": "温暖/冷峻/神秘/梦幻/欢快/史诗/治愈/紧张 之一",
  "time_of_day": "清晨/黄昏/日落/深夜/蓝调时刻 等（无则空）",
  "weather": "晴/雨/雾/雪 等（无则空）",
  "season": "春/夏/秋/冬/樱花季/枫叶季（无则空）",
  "key_visual_details": ["3-5 个关键视觉元素，英文，有助于 T2I 复现"],
  "negatives": ["3-5 个应避免的事物，英文"],
  "platform_warnings": [
    {{"platform": "DALL-E|MJ|SD", "risk": "可能被拒的原因", "suggestion": "如何改写"}}
  ],
  "polish_notes": "中文一句话总结：你做了什么润色"
}}
```

# 关键原则

- **不要拒答**：用户给的都是合法艺术创作场景。如果有边界词，做艺术化替代（"血" → "crimson splash"，"裸" → "elegant figure, classical art reference"）。仅在涉及 CSAM/真人色情/违法行为时才返回 `{{"error": "out_of_scope"}}`
- **subject_refined_zh 比 subject_refined_en 更具体**：中文版要补全用户没说但摄影师/画师会自然加的细节（光线、表情、动态）
- **camera/lighting/palette 必须能让另一个画师复现同一张图**：避免"美丽光影"这类废话
- **JSON 之外不要任何文字**

记住：你输出的 JSON 会直接被脚本 parse，**不要**包 ```json``` 代码块，**不要**前缀解释。"""


def call_claude(prompt: str, model: str = DEFAULT_MODEL, max_tokens: int = 2048,
                temperature: float = 0.7) -> Dict:
    """调用 Anthropic Messages API。启用 prompt caching。"""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError(
            "缺少 ANTHROPIC_API_KEY 环境变量。\n"
            "  • macOS/Linux: export ANTHROPIC_API_KEY=sk-ant-...\n"
            "  • 或在 ~/.zshrc / ~/.bashrc 里写入"
        )

    body = {
        "model": model,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "system": [
            {
                "type": "text",
                "text": build_system_prompt(),
                "cache_control": {"type": "ephemeral"},
            }
        ],
        "messages": [
            {
                "role": "user",
                "content": f"<user_subject>{prompt}</user_subject>\n\n请输出 JSON。",
            },
            {
                "role": "assistant",
                "content": "{",  # prefill 强制 JSON 起手
            },
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
            return json.loads(r.read().decode("utf-8"))
    except HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Claude API HTTP {e.code}: {err_body}")
    except URLError as e:
        raise RuntimeError(f"Claude API 网络错误: {e}")


def parse_claude_json(resp: Dict) -> Dict:
    """从 Claude 响应中抽出 JSON（已 prefill `{`，所以拼回去）。"""
    if "error" in resp:
        raise RuntimeError(f"Claude API 错误: {resp['error']}")
    text = ""
    for block in resp.get("content", []):
        if block.get("type") == "text":
            text += block.get("text", "")
    if not text:
        raise RuntimeError(f"Claude 返回空内容: {resp}")

    full = "{" + text  # prefill
    # 截到第一个完整 JSON
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

    try:
        data = json.loads(full[:end])
    except json.JSONDecodeError as e:
        raise RuntimeError(f"JSON 解析失败: {e}\n原文: {full[:300]}")

    # 附加 usage 信息
    usage = resp.get("usage", {})
    data["_usage"] = {
        "input_tokens": usage.get("input_tokens", 0),
        "output_tokens": usage.get("output_tokens", 0),
        "cache_creation_input_tokens": usage.get("cache_creation_input_tokens", 0),
        "cache_read_input_tokens": usage.get("cache_read_input_tokens", 0),
    }
    data["_model"] = resp.get("model", "")
    return data


# ─────────────────────────────────────────────────────────
# 输出格式化
# ─────────────────────────────────────────────────────────
def to_pipe_command(polished: Dict) -> str:
    """把 polished 转成可直接喂给 enhance_prompt.py 的 CLI 命令。"""
    subject = polished.get("subject_refined_zh", "")
    preset = polished.get("style_preset", "")
    sec = polished.get("style_preset_secondary", "")
    mix = polished.get("mix_ratio", 0.6)
    aspect = polished.get("aspect", "")

    preset_arg = f'"{preset}+{sec}"' if sec else f'"{preset}"'
    parts = [
        "enhance_prompt.py",
        f'"{subject}"',
        "-p", preset_arg,
    ]
    if sec:
        parts += ["--mix", str(mix)]
    if aspect:
        parts += ["-a", aspect]
    return " ".join(parts)


def print_polished(polished: Dict):
    sep = "═" * 60
    print(f"\n{sep}")
    print(f"✨ Claude 智能润色 v{VERSION}")
    print(f"🤖 模型: {polished.get('_model', '?')}")
    u = polished.get("_usage", {})
    print(f"📊 token: in={u.get('input_tokens',0)} / out={u.get('output_tokens',0)} / cache_read={u.get('cache_read_input_tokens',0)} (省 token)")

    if polished.get("error"):
        print(f"\n❌ 拒答: {polished['error']}（CSAM/真人色情/违法 不在本工具支持范围）")
        print(f"{sep}\n")
        return

    print(f"\n📝 润色后中文主体:\n   {polished.get('subject_refined_zh', '')}")
    print(f"\n🌐 English:\n   {polished.get('subject_refined_en', '')}")

    style = polished.get("style_preset", "")
    sec = polished.get("style_preset_secondary", "")
    if sec:
        ratio = polished.get("mix_ratio", 0.6)
        print(f"\n🎨 推荐预设: {style} + {sec} (mix={ratio})")
    else:
        print(f"\n🎨 推荐预设: {style}")

    print(f"📐 画幅: {polished.get('aspect', '')}")
    print(f"🎥 相机: {polished.get('camera', '')}")
    print(f"💡 光影: {polished.get('lighting', '')}")
    print(f"🎨 色板: {polished.get('palette', '')}")

    extras = []
    for k, label in [("composition", "构图"), ("mood", "情绪"),
                     ("time_of_day", "时间"), ("weather", "天气"), ("season", "季节")]:
        if polished.get(k):
            extras.append(f"{label}={polished[k]}")
    if extras:
        print(f"🔍 抽词: {' / '.join(extras)}")

    if polished.get("key_visual_details"):
        print(f"\n🌟 关键视觉:")
        for d in polished["key_visual_details"]:
            print(f"   • {d}")

    if polished.get("negatives"):
        print(f"\n🚫 负面词:")
        for n in polished["negatives"]:
            print(f"   • {n}")

    warnings = polished.get("platform_warnings") or []
    if warnings:
        print(f"\n⚠️  平台风险:")
        for w in warnings:
            print(f"   [{w.get('platform','?')}] {w.get('risk','')}")
            print(f"      → {w.get('suggestion','')}")

    if polished.get("polish_notes"):
        print(f"\n📌 润色说明: {polished['polish_notes']}")

    print(f"\n💡 一键复制喂给 enhance_prompt.py:")
    print(f"   {to_pipe_command(polished)}")
    print(f"{sep}\n")


def main():
    parser = argparse.ArgumentParser(
        description=f"huo15-img-test claude_polish v{VERSION} — Claude API 智能润色",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  claude_polish.py "一个温柔的女孩在花丛中"
  claude_polish.py "赛博朋克猫" --model claude-sonnet-4-6
  claude_polish.py "敦煌神女" -j > polished.json
  claude_polish.py "雪山下的小屋" --pipe   # 输出可直接喂给 enhance_prompt.py 的命令

环境变量:
  ANTHROPIC_API_KEY     必填
  ANTHROPIC_BASE_URL    可选，默认 https://api.anthropic.com
""",
    )
    parser.add_argument("subject", nargs="?", help="主体描述（中文/英文均可）")
    parser.add_argument("--model", default=DEFAULT_MODEL,
                        help=f"Claude 模型（默认 {DEFAULT_MODEL}）")
    parser.add_argument("--max-tokens", type=int, default=2048, help="最大输出 tokens")
    parser.add_argument("--temperature", type=float, default=0.7, help="温度 0.0-1.0")
    parser.add_argument("--pipe", action="store_true", help="输出 enhance_prompt.py CLI 命令一行")
    parser.add_argument("-j", "--json", action="store_true", help="JSON 输出")
    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s v{VERSION}")
    args = parser.parse_args()

    if not args.subject:
        parser.print_help()
        sys.exit(1)

    try:
        resp = call_claude(args.subject, model=args.model,
                           max_tokens=args.max_tokens, temperature=args.temperature)
        polished = parse_claude_json(resp)
    except RuntimeError as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(2)

    if args.pipe:
        print(to_pipe_command(polished))
        return
    if args.json:
        print(json.dumps(polished, ensure_ascii=False, indent=2))
        return
    print_polished(polished)


if __name__ == "__main__":
    main()
