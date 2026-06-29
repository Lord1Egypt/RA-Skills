#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""analyzer.py — 4 LLM analyses for JD reverse-engineering."""
from __future__ import annotations

_JARGON_PROMPT = """\
You are a job market analyst. Translate JD jargon to real requirements.
For vague/inflated phrases, output the actual threshold:

Example: "5年经验" → "3年+中型项目即可"

JD stats: {stats}
JD text:
{jd_text}

Return ONLY valid JSON (no markdown fences):
[
  {{"jd_text": "...", "real_requirement": "..."}},
  ...
]
"""

_CULTURE_PROMPT = """\
Based on this JD's phrasing, infer company culture signals.

Red flags detected: {red_flags}
Structure: {structure}

JD text:
{jd_text}

Return ONLY valid JSON (no markdown fences):
{{
  "pace": "relaxed|normal|high-pressure",
  "red_flags": ["list occurrences of 抗压/996/owner/etc"],
  "tech_maturity": "high|medium|low — does JD list versions?",
  "business_clarity": "high|medium|low — is product scope clear?",
  "candidate_questions": ["问加班频率?", "..."]
}}
"""

_RESUME_PROMPT = """\
Compare JD to candidate resume. Output match analysis.

JD text:
{jd_text}

Resume:
{resume_text}

Return ONLY valid JSON (no markdown fences):
{{
  "match_score": 0-100,
  "hard_met": ["list"],
  "hard_unmet": ["list"],
  "soft_met": ["list"],
  "soft_unmet": ["list"],
  "recommendation": "strong fit|moderate fit|weak fit|dealbreaker gaps"
}}
"""

_NEGOTIATION_PROMPT = """\
Analyze JD for negotiation leverage signals. DO NOT estimate salary numbers.
Identify SIGNALS only:

Stats: {stats}

JD text:
{jd_text}

Return ONLY valid JSON (no markdown fences):
{{
  "salary_transparency": "explicit range|面议|not mentioned",
  "level_specified": true|false,
  "equity_water": "high|medium|low|n/a — specific % mentioned?",
  "urgency": true|false — 急招/立即到岗?",
  "leverage_summary": "high|medium|low 议价空间 — brief reason"
}}
"""


def analyze_jargon(jd_text: str, stats: dict, llm) -> list[dict]:
    msgs = [{"role": "user", "content": _JARGON_PROMPT.format(jd_text=jd_text, stats=str(stats))}]
    result = llm.chat(msgs)
    return result if isinstance(result, list) else []


def analyze_culture(jd_text: str, stats: dict, llm) -> dict:
    red_flags = {k: v for k, v in stats["red_flag_keywords"].items() if v > 0}
    msgs = [{"role": "user", "content": _CULTURE_PROMPT.format(
        jd_text=jd_text, red_flags=str(red_flags), structure=str(stats["structure"])
    )}]
    result = llm.chat(msgs)
    return result if isinstance(result, dict) else {}


def analyze_resume_match(jd_text: str, resume_text: str, llm) -> dict | None:
    if not resume_text or len(resume_text.strip()) < 50:
        return None
    msgs = [{"role": "user", "content": _RESUME_PROMPT.format(jd_text=jd_text, resume_text=resume_text)}]
    result = llm.chat(msgs)
    return result if isinstance(result, dict) else None


def analyze_negotiation(jd_text: str, stats: dict, llm) -> dict:
    msgs = [{"role": "user", "content": _NEGOTIATION_PROMPT.format(jd_text=jd_text, stats=str(stats))}]
    result = llm.chat(msgs)
    return result if isinstance(result, dict) else {}


def run_analysis(jd_text: str, resume_text: str | None, stats: dict, llm) -> dict:
    """Orchestrate all 4 LLM calls."""
    return {
        "jargon": analyze_jargon(jd_text, stats, llm),
        "culture": analyze_culture(jd_text, stats, llm),
        "resume_match": analyze_resume_match(jd_text, resume_text, llm) if resume_text else None,
        "negotiation": analyze_negotiation(jd_text, stats, llm),
    }
