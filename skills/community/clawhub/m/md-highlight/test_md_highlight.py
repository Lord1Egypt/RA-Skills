#!/usr/bin/env python
"""
pytest 格式校验：md_highlight 预期输出是否符合 SKILL 规则
- 校验 span 格式、颜色、标注长度、密度
- 不调用 LLM
"""

import re
from pathlib import Path

import pytest

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"
EXPECTED_DIR = FIXTURES_DIR / "expected"

ALLOWED_COLORS = {"#fff3cd", "#d4edda", "#d1ecf1", "#fff2e6"}
CLASS_TO_COLOR = {
    "hl-concept": "#d1ecf1",
    "hl-conclusion": "#fff3cd",
    "hl-data": "#d4edda",
    "hl-warning": "#fff2e6",
}
# 支持 class 格式（方案1）与旧版 inline style 格式
SPAN_CLASS_PATTERN = re.compile(
    r'<span class="(hl-(?:concept|conclusion|data|warning))">([^<]+)</span>'
)
SPAN_STYLE_PATTERN = re.compile(
    r'<span style="background-color:(#[a-fA-F0-9]+); padding:2px 4px; border-radius:3px;">([^<]+)</span>'
)


def _strip_spans(md: str) -> str:
    """Remove all span tags (class or style), preserving inner text."""
    s = SPAN_CLASS_PATTERN.sub(r"\2", md)
    return SPAN_STYLE_PATTERN.sub(r"\2", s)


def validate_highlight_output(md: str) -> tuple[bool, list[str]]:
    """
    Validate md_highlight output against SKILL rules.
    Returns (passed, list of error messages).
    支持 class 格式（hl-concept 等）与旧版 inline style 格式。
    """
    errors: list[str] = []

    # 1. Find spans: class 格式 或 style 格式
    class_spans = list(SPAN_CLASS_PATTERN.finditer(md))
    style_spans = list(SPAN_STYLE_PATTERN.finditer(md))
    spans = class_spans + style_spans

    # Check for any malformed spans (e.g. different format)
    remaining = re.sub(SPAN_CLASS_PATTERN, "", md)
    remaining = re.sub(SPAN_STYLE_PATTERN, "", remaining)
    if "<span" in remaining:
        errors.append("存在非标准格式的 span 标记")

    for m in class_spans:
        cls_name, text = m.group(1), m.group(2)
        if cls_name not in CLASS_TO_COLOR:
            errors.append(f"非法 class {cls_name}，标注内容: {text[:20]}...")
        text_len = len(text.strip())
        if text_len < 2 or text_len > 10:
            errors.append(f"标注长度 {text_len} 超出 2～10 字范围，内容: {text[:20]}...")

    for m in style_spans:
        color, text = m.group(1).lower(), m.group(2)
        if color not in ALLOWED_COLORS:
            errors.append(f"非法颜色 {color}，标注内容: {text[:20]}...")
        text_len = len(text.strip())
        if text_len < 2 or text_len > 10:
            errors.append(f"标注长度 {text_len} 超出 2～10 字范围，内容: {text[:20]}...")

    # 2. Density: split by blank lines, max 3 per paragraph (SKILL: 单段最多3处标注)
    all_span_pattern = re.compile(
        r'<span (?:class="hl-(?:concept|conclusion|data|warning|step)"|style="background-color:[#a-fA-F0-9]+; padding:2px 4px; border-radius:3px;")>[^<]+</span>'
    )
    paragraphs = re.split(r"\n\s*\n", md)
    for i, para in enumerate(paragraphs):
        count = len(all_span_pattern.findall(para))
        if count > 3:
            errors.append(f"第 {i + 1} 段标注密度过高: {count} 处（最多 3 处）")

    # 3. Overall density
    lines = [l for l in md.split("\n") if l.strip()]
    total_spans = len(spans)
    if lines and total_spans > 0:
        ratio = len(lines) / total_spans
        if ratio < 0.4:
            errors.append(f"标注过密: {len(lines)} 行有 {total_spans} 处（约每 {ratio:.1f} 行 1 处）")
        elif ratio > 25:
            errors.append(f"标注过疏: {len(lines)} 行仅 {total_spans} 处")

    # 4. No ==xxx== highlighting
    if re.search(r"==[^=]+==", md):
        errors.append("存在 == 高亮标记（应使用 span）")

    return (len(errors) == 0, errors)


@pytest.mark.parametrize("name", ["narrative", "pop_sci", "technical", "instruction", "essay"])
def test_expected_conforms_to_rules(name: str) -> None:
    """校验 fixtures/expected/<name>.md 符合 SKILL 规则"""
    expected_path = EXPECTED_DIR / f"{name}.md"
    assert expected_path.exists(), f"fixture not found: {expected_path}"
    content = expected_path.read_text(encoding="utf-8")
    passed, errors = validate_highlight_output(content)
    assert passed, "\n".join(errors)


def test_expected_preserves_original_content() -> None:
    """去掉 span 与 style 块后与 input 比对，确保未增删原文"""
    style_block_pattern = re.compile(
        r"<style>[\s\S]*?</style>\s*", re.IGNORECASE
    )
    for name in ["narrative", "pop_sci", "technical", "instruction", "essay"]:
        input_path = FIXTURES_DIR / f"{name}.md"
        expected_path = EXPECTED_DIR / f"{name}.md"
        assert input_path.exists() and expected_path.exists()
        raw_input = input_path.read_text(encoding="utf-8")
        expected = expected_path.read_text(encoding="utf-8")
        # 移除 style 块后再去掉 span
        without_style = style_block_pattern.sub("", expected)
        stripped = _strip_spans(without_style)
        # 忽略首尾空白差异
        input_normalized = "".join(raw_input.split())
        stripped_normalized = "".join(stripped.split())
        assert input_normalized == stripped_normalized, f"{name}: 预期输出与原文件内容不一致（去掉 span 后）"
