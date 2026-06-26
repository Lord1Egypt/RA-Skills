#!/usr/bin/env python3
"""
content_producer.py - 品牌多渠道内容生成模块

接收品牌简报、内容策略、竞品洞察，调用 LLM 生成各渠道真实内容草稿。
输入：stdin JSON
输出：stdout JSON（schema 与 content_producer_stub.py 保持向后兼容）
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

# 允许直接运行时找到同目录的 oc_llm_client
sys.path.insert(0, str(Path(__file__).parent))
from oc_llm_client import llm_complete  # noqa: E402

# ─── 常量 ────────────────────────────────────────────────────────────────────

MAX_TOKENS = 3000

# ─── 工具函数 ─────────────────────────────────────────────────────────────────


def _build_competitor_gaps_summary(competitor_insights: list) -> str:
    """构建竞品差异化机会摘要（最多3个竞品）。"""
    if not competitor_insights:
        return "无竞品数据，根据行业通用最佳实践生成内容。"
    lines = []
    for ci in competitor_insights[:3]:
        gaps = ci.get("gaps", [])
        if gaps:
            lines.append(
                f"- {ci.get('competitor', '?')}: 弱点在{', '.join(gaps[:2])}，可在此差异化"
            )
    return "\n".join(lines) if lines else "竞品分析无显著弱点。"


def _build_prompt(payload: dict) -> str:
    """构建发送给 LLM 的完整 prompt。"""
    brand = payload.get("brand_brief", {})
    strategy = payload.get("content_strategy", {})
    competitor_insights = payload.get("competitor_insights", [])
    channels: list[str] = payload.get("channels", ["xiaohongshu", "weibo", "douyin"])
    generate_count: int = max(1, int(payload.get("generate_count", 2)))

    brand_name = brand.get("brand_name", "品牌")
    brand_positioning = brand.get("brand_positioning", "")
    brand_tone = brand.get("brand_tone", "")
    target_audience: list = brand.get("target_audience", [])
    brand_dos: list = brand.get("brand_dos", [])
    brand_donts: list = brand.get("brand_donts", [])
    content_pillars: list = strategy.get("content_pillars", [])

    audience_str = "、".join(target_audience) if target_audience else "广泛受众"
    dos_str = "、".join(brand_dos) if brand_dos else "无"
    donts_str = "、".join(brand_donts) if brand_donts else "无"
    pillars_str = "、".join(content_pillars) if content_pillars else "品牌故事"
    channels_str = "、".join(channels)
    competitor_gaps_summary = _build_competitor_gaps_summary(competitor_insights)

    # 各渠道格式说明（只列出输入中指定的渠道）
    channel_format_map = {
        "xiaohongshu": "xiaohongshu：300字以内，1-3个话题标签（#话题），情感化叙事，适合配图",
        "weibo": "weibo：140字以内，可带话题，轻松直接",
        "douyin": "douyin：60秒视频脚本大纲（格式：开头10秒钩子 | 主体 | 结尾CTA）",
        "wechat": "wechat：800-1200字，加小标题，公众号文章风格",
        "linkedin": "linkedin：英文，200词以内，专业叙事，B2B语气",
        "x": "x：英文，280字符以内，话题标签不超过2个",
    }
    channel_format_lines = [
        channel_format_map.get(ch, f"{ch}：适合该平台的内容格式")
        for ch in channels
    ]
    channel_format_str = "\n- ".join(channel_format_lines)

    # posts 字段示例（动态按渠道生成）
    posts_example_lines = []
    for ch in channels:
        examples = ", ".join(f'"{ch}内容{i+1}"' for i in range(generate_count))
        posts_example_lines.append(f'    "{ch}": [{examples}]')
    posts_example = "{\n" + ",\n".join(posts_example_lines) + "\n  }"

    topics_example = ", ".join(f'"内容话题{i+1}"' for i in range(generate_count))
    titles_example = ", ".join(f'"标题{i+1}"' for i in range(generate_count))
    scripts_example = '"视频脚本大纲1"'
    replies_example = '"回复模板1", "回复模板2"'

    prompt = f"""你是资深品牌内容策划专家。请根据以下品牌 Brief 和竞品洞察，生成高质量、品牌调性一致的多渠道内容草稿。

【品牌 Brief】
品牌名：{brand_name}
定位：{brand_positioning}
语气：{brand_tone}
目标受众：{audience_str}
品牌 DOs（必须体现）：{dos_str}
品牌 DON'Ts（绝对避免）：{donts_str}

【竞品差异化机会】
{competitor_gaps_summary}

【内容策略】
内容支柱：{pillars_str}

【质量要求】
1. 内容必须紧扣品牌定位，每句话都能体现品牌调性
2. 标题要有吸引力，能在3秒内抓住受众注意力
3. 正文要有情感共鸣，避免空洞的促销语言
4. 严格检查：绝不出现 DON'Ts 列表中的任何关键词或概念
5. 各渠道内容要适配平台特性，但保持品牌一致性

【任务】
生成 {generate_count} 套内容草稿，覆盖以下渠道：{channels_str}

各渠道格式要求：
- {channel_format_str}

【输出格式】
只输出以下 JSON 格式，不要其他说明：
{{
  "topics": [{topics_example}],
  "titles": [{titles_example}],
  "posts": {posts_example},
  "scripts": [{scripts_example}],
  "comment_replies": [{replies_example}]
}}"""
    return prompt


def _call_llm_with_fallback(prompt: str, max_retries: int = 3) -> str:
    """调用 LLM（使用用户 openclaw.json 中配置的默认模型），带重试机制。"""
    import time
    last_error = None
    
    for attempt in range(max_retries):
        try:
            return llm_complete(prompt, max_tokens=MAX_TOKENS)
        except Exception as e:
            last_error = e
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # 指数退避: 1s, 2s, 4s
                time.sleep(wait_time)
            continue
    
    # 所有重试失败，返回一个安全的 fallback 响应
    print(f"[WARN] LLM call failed after {max_retries} retries: {last_error}", file=sys.stderr)
    raise last_error  # 重新抛出，让上层处理


def _extract_json_from_response(text: str) -> dict:
    """从 LLM 响应文本中提取 JSON 对象（兼容 markdown 代码块包装）。"""
    # 去除 markdown 代码块包装（```json ... ``` 或 ``` ... ```）
    text = re.sub(r"^```(?:json)?\s*", "", text.strip(), flags=re.MULTILINE)
    text = re.sub(r"\s*```$", "", text.strip(), flags=re.MULTILINE)
    text = text.strip()

    # 尝试直接解析
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # 尝试提取第一个 { ... } 块
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        try:
            return json.loads(text[start:end + 1])
        except json.JSONDecodeError:
            pass

    return {}


def _check_brand_donts(data: dict, brand_donts: list) -> bool:
    """检查生成内容是否含 brand_donts 关键词，返回 True 表示存在违规。"""
    if not brand_donts:
        return False

    # 提取所有文本字段
    texts: list[str] = []
    texts.extend(data.get("topics", []))
    texts.extend(data.get("titles", []))
    texts.extend(data.get("scripts", []))
    texts.extend(data.get("comment_replies", []))
    for ch_posts in data.get("posts", {}).values():
        if isinstance(ch_posts, list):
            texts.extend(ch_posts)

    combined = " ".join(str(t) for t in texts).lower()
    violated = []
    for dont in brand_donts:
        if dont.lower() in combined:
            violated.append(dont)

    if violated:
        print(f"[content_producer] 品牌一致性警告：生成内容含 DON'T 关键词: {violated}",
              file=sys.stderr)
        return True
    return False


def _build_fallback_output(channels: list[str]) -> dict:
    """LLM 调用或解析失败时返回的兜底空结构。"""
    return {
        "topics": [],
        "titles": [],
        "posts": {c: [] for c in channels},
        "scripts": [],
        "comment_replies": [],
        "platform_variants": channels,
        "error": "content generation failed",
    }


# ─── 主函数 ───────────────────────────────────────────────────────────────────


def main() -> int:
    # 1. 读取输入
    raw = sys.stdin.read().strip()
    try:
        payload = json.loads(raw) if raw else {}
    except json.JSONDecodeError as e:
        print(f"[content_producer] 输入 JSON 解析失败: {e}", file=sys.stderr)
        payload = {}

    channels: list[str] = payload.get("channels", ["xiaohongshu", "weibo", "douyin"])
    brand_donts: list[str] = payload.get("brand_brief", {}).get("brand_donts", [])

    # 2. 构建 prompt 并调用 LLM
    prompt = _build_prompt(payload)
    try:
        llm_response = _call_llm_with_fallback(prompt)
    except RuntimeError as e:
        print(f"[content_producer] LLM 调用全部失败: {e}", file=sys.stderr)
        print(json.dumps(_build_fallback_output(channels), ensure_ascii=False, indent=2))
        return 1

    # 3. 解析 LLM JSON 响应
    parsed = _extract_json_from_response(llm_response)
    if not parsed:
        print(f"[content_producer] LLM 响应 JSON 解析失败，原始内容:\n{llm_response[:500]}",
              file=sys.stderr)
        print(json.dumps(_build_fallback_output(channels), ensure_ascii=False, indent=2))
        return 1

    # 4. 品牌一致性检查（DON'Ts 关键词检测）
    low_confidence = _check_brand_donts(parsed, brand_donts)

    # 5. 构建输出（向后兼容 stub schema）
    posts_raw = parsed.get("posts", {})
    # 兼容：若 LLM 把 posts 输出为 list 而不是 dict（降级处理）
    if isinstance(posts_raw, list):
        posts_dict = {}
        for i, ch in enumerate(channels):
            posts_dict[ch] = [posts_raw[i]] if i < len(posts_raw) else []
    else:
        posts_dict = {ch: posts_raw.get(ch, []) for ch in channels}

    output: dict = {
        "topics": parsed.get("topics", []),
        "titles": parsed.get("titles", []),
        "posts": posts_dict,
        "scripts": parsed.get("scripts", []),
        "comment_replies": parsed.get("comment_replies", []),
        "platform_variants": channels,
    }
    if low_confidence:
        output["low_confidence"] = True

    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
