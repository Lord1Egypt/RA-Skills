from __future__ import annotations

import re

from .utils import clamp

RISK_WORDS = ("风险", "边界", "权限", "安全", "risk", "boundary", "permission", "safe")
VERIFY_WORDS = ("测试", "验证", "检查", "回归", "test", "verify", "check", "regression")
TRADEOFF_WORDS = ("取舍", "权衡", "trade-off", "tradeoff", "pros", "cons", "代价")
STRUCTURE_MARKERS = ("```", "\n-", "\n*", "\n1.", "\n2.", "##", "###")
STOPWORDS = {
    "the",
    "and",
    "that",
    "this",
    "with",
    "from",
    "your",
    "into",
    "then",
    "will",
    "would",
    "have",
    "been",
    "what",
    "when",
    "where",
    "about",
    "任务",
    "问题",
    "需要",
    "可以",
    "然后",
    "如果",
    "这个",
    "那个",
}


def _ascii_keywords(text: str) -> set[str]:
    return {token for token in re.findall(r"[A-Za-z][A-Za-z0-9_-]{2,}", text.lower()) if token not in STOPWORDS}


def _cjk_keywords(text: str) -> set[str]:
    matches = re.findall(r"[\u4e00-\u9fff]{2,6}", text)
    return {match for match in matches if match not in STOPWORDS}


def _keyword_overlap(source: str, target: str) -> float:
    source_keywords = _ascii_keywords(source) | _cjk_keywords(source)
    target_keywords = _ascii_keywords(target) | _cjk_keywords(target)
    if not source_keywords or not target_keywords:
        return 0.0
    return len(source_keywords & target_keywords) / max(1, len(source_keywords))


def _sentence_count(text: str) -> int:
    return len([chunk for chunk in re.split(r"[。！？.!?\n]+", text) if chunk.strip()])


def _paragraph_count(text: str) -> int:
    return len([chunk for chunk in re.split(r"\n\s*\n", text) if chunk.strip()])


def _repetition_penalty(text: str) -> int:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if len(lines) < 3:
        return 0
    unique_ratio = len(set(lines)) / max(1, len(lines))
    if unique_ratio >= 0.8:
        return 0
    if unique_ratio >= 0.6:
        return 6
    return 12


class AIJudge:
    def __init__(self, model_name: str = "heuristic-judge-v2") -> None:
        self.model_name = model_name

    def judge(self, task, response: str, rubric: str) -> dict:
        content = response.strip()
        if not content:
            return {"l3_score": 0, "l4_score": 0, "l5_score": 0, "reasoning": ""}

        response_length = len(content)
        sentence_count = _sentence_count(content)
        paragraph_count = _paragraph_count(content)
        structure_hits = sum(1 for marker in STRUCTURE_MARKERS if marker in content)
        code_bonus = 8 if "```" in content else 0
        structure_bonus = min(22, paragraph_count * 6 + sentence_count * 2 + structure_hits * 4 + code_bonus)
        detail_bonus = min(24, response_length // 28 + sentence_count * 2)

        prompt_overlap = _keyword_overlap(task or "", content)
        rubric_overlap = _keyword_overlap(rubric or "", content)
        coverage_bonus = min(24, int(prompt_overlap * 32) + int(rubric_overlap * 42))

        risk_bonus = 10 if any(word in content.lower() for word in RISK_WORDS) else 0
        verify_bonus = 12 if any(word in content.lower() for word in VERIFY_WORDS) else 0
        tradeoff_bonus = 8 if any(word in content.lower() for word in TRADEOFF_WORDS) else 0
        repetition_penalty = _repetition_penalty(content)
        short_penalty = 16 if response_length < 70 else 8 if response_length < 120 else 0

        l3 = int(clamp(34 + structure_bonus + coverage_bonus - short_penalty, 0, 100))
        l4 = int(clamp(36 + detail_bonus + coverage_bonus + verify_bonus - repetition_penalty, 0, 100))
        l5 = int(clamp(32 + structure_bonus + risk_bonus + verify_bonus + tradeoff_bonus - repetition_penalty, 0, 100))
        return {"l3_score": l3, "l4_score": l4, "l5_score": l5, "reasoning": ""}
