#!/usr/bin/env python3
"""
competitor_ai_analyzer.py - 竞品 AI 分析模块

从 stdin 读取 competitor_fetcher 的原始抓取数据 + 品牌简报，
调用 LLM 提取营销信号，输出格式兼容 competitor_cluster.py。

输入（stdin JSON）：
  {
    "raw_data": [{"competitor_name", "raw_text", "source_type", "fetch_ok"}, ...],
    "brand_brief": {"brand_name", "brand_positioning", "brand_tone", ...}
  }

输出（stdout JSON）：
  [{"competitor", "theme", "tone", "frequency", "hooks",
    "content_patterns", "channel_strength", "gaps", "fetch_ok"}, ...]
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

# ─── 依赖导入 ─────────────────────────────────────────────────────────────────

sys.path.insert(0, str(Path(__file__).parent))
from gateway_client import llm_complete

# ─── 常量 ────────────────────────────────────────────────────────────────────

ANALYSIS_MODEL = "gpt-5.4-mini"
ANALYSIS_MAX_TOKENS = 800

FALLBACK_ANALYSIS: dict = {
    "theme": "unknown",
    "tone": "neutral",
    "frequency": "unknown",
    "hooks": [],
    "content_patterns": [],
    "channel_strength": [],
    "gaps": [],
}

# ─── Prompt 构建 ──────────────────────────────────────────────────────────────


def _build_brand_summary(brand_brief: dict) -> str:
    """从 brand_brief 构建简洁的品牌背景描述。"""
    parts = []
    if name := brand_brief.get("brand_name"):
        parts.append(f"品牌名：{name}")
    if positioning := brand_brief.get("brand_positioning"):
        parts.append(f"定位：{positioning}")
    if tone := brand_brief.get("brand_tone"):
        parts.append(f"语气风格：{tone}")
    if audience := brand_brief.get("target_audience"):
        parts.append(f"目标受众：{', '.join(audience) if isinstance(audience, list) else audience}")
    if dos := brand_brief.get("brand_dos"):
        parts.append(f"品牌应为：{', '.join(dos) if isinstance(dos, list) else dos}")
    if donts := brand_brief.get("brand_donts"):
        parts.append(f"品牌禁忌：{', '.join(donts) if isinstance(donts, list) else donts}")
    return "；".join(parts) if parts else "（无品牌简报）"


def _build_prompt(competitor_name: str, raw_text: str, source_type: str, brand_summary: str) -> str:
    """构建竞品分析 prompt。"""
    return f"""你是品牌竞争情报分析师。分析以下竞品公开内容，提取营销信号。

竞品名称：{competitor_name}
品牌背景（你的品牌，作为参照）：{brand_summary}

竞品原始内容（来源：{source_type}）：
{raw_text}

请用 JSON 格式输出，只含以下字段（全英文，不要中文值）：
{{
  "theme": "主题定位（1-3英文词，如 minimalism / productivity-platform / lifestyle-brand）",
  "tone": "内容语气（2-4英文词）",
  "frequency": "内容频率估计（daily/weekly/irregular）",
  "hooks": ["钩子1", "钩子2", "钩子3"],
  "content_patterns": ["模式1", "模式2", "模式3"],
  "channel_strength": ["渠道1", "渠道2"],
  "gaps": ["弱点/差异化机会1", "弱点2"]
}}

只输出 JSON，不要其他说明文字。"""


# ─── 核心分析 ─────────────────────────────────────────────────────────────────


def _parse_llm_json(raw: str, competitor_name: str) -> dict:
    """从 LLM 输出中提取 JSON，解析失败时返回兜底默认值。"""
    text = raw.strip()
    # 剥除 markdown 代码块（```json ... ``` 或 ``` ... ```）
    if text.startswith("```"):
        lines = text.splitlines()
        # 去掉首行（```json 或 ```）和尾行（```）
        inner_lines = lines[1:]
        if inner_lines and inner_lines[-1].strip() == "```":
            inner_lines = inner_lines[:-1]
        text = "\n".join(inner_lines).strip()

    try:
        parsed = json.loads(text)
        if isinstance(parsed, dict):
            return parsed
        print(
            f"[competitor_ai_analyzer] WARNING: LLM returned non-dict JSON for {competitor_name!r}",
            file=sys.stderr,
        )
    except json.JSONDecodeError as exc:
        print(
            f"[competitor_ai_analyzer] WARNING: JSON parse failed for {competitor_name!r}: {exc}",
            file=sys.stderr,
        )
    return dict(FALLBACK_ANALYSIS)


def _analyze_competitor(item: dict, brand_summary: str) -> dict:
    """分析单个竞品，返回结构化结果。"""
    competitor_name = item.get("competitor_name", "unknown")
    raw_text = item.get("raw_text", "")
    source_type = item.get("source_type", "unknown")
    fetch_ok = item.get("fetch_ok", False)

    # 跳过抓取失败且无内容的条目
    if not fetch_ok and not raw_text:
        return {
            "competitor": competitor_name,
            **FALLBACK_ANALYSIS,
            "fetch_ok": False,
        }

    prompt = _build_prompt(competitor_name, raw_text, source_type, brand_summary)

    try:
        llm_response = llm_complete(
            prompt=prompt,
            model=ANALYSIS_MODEL,
            max_tokens=ANALYSIS_MAX_TOKENS,
        )
        analysis = _parse_llm_json(llm_response, competitor_name)
    except Exception as exc:
        print(
            f"[competitor_ai_analyzer] ERROR: LLM call failed for {competitor_name!r}: {exc}",
            file=sys.stderr,
        )
        analysis = {**FALLBACK_ANALYSIS, "llm_error": str(exc)}

    return {
        "competitor": competitor_name,
        "theme": analysis.get("theme", FALLBACK_ANALYSIS["theme"]),
        "tone": analysis.get("tone", FALLBACK_ANALYSIS["tone"]),
        "frequency": analysis.get("frequency", FALLBACK_ANALYSIS["frequency"]),
        "hooks": analysis.get("hooks", FALLBACK_ANALYSIS["hooks"]),
        "content_patterns": analysis.get("content_patterns", FALLBACK_ANALYSIS["content_patterns"]),
        "channel_strength": analysis.get("channel_strength", FALLBACK_ANALYSIS["channel_strength"]),
        "gaps": analysis.get("gaps", FALLBACK_ANALYSIS["gaps"]),
        "fetch_ok": fetch_ok,
        **({"llm_error": analysis["llm_error"]} if "llm_error" in analysis else {}),
    }


# ─── 入口 ─────────────────────────────────────────────────────────────────────


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError as exc:
        print(f"[competitor_ai_analyzer] FATAL: invalid stdin JSON: {exc}", file=sys.stderr)
        sys.exit(1)

    raw_data: list[dict] = payload.get("raw_data", [])
    brand_brief: dict = payload.get("brand_brief", {})
    brand_summary = _build_brand_summary(brand_brief)

    results = []
    for item in raw_data:
        result = _analyze_competitor(item, brand_summary)
        results.append(result)

    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
