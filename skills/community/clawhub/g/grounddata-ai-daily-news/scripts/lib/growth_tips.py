"""
growth_tips.py — Render user-facing growth tips with actionable examples.

Each tip is designed as "directly usable commands" users can copy into chat.
To avoid repetitive wording fatigue, example lines are randomly sampled.
"""

import random
from typing import Dict, List


_TIP_EXAMPLES: Dict[str, List[str]] = {
    "onboarding": [
        '"Summarize the 5 most important AI news stories today in Chinese."',
        '"From now on, prioritize AI Coding and Agent news for me."',
        '"Turn today\'s news into a shareable Markdown briefing."',
        '"Based on today\'s news, generate a product opportunity scan."',
        '"I want to integrate daily AI news into my workflow."',
        '"Give me a 3-minute AI news quick read in English."',
        '"Show me the top 3 first, then add 3 more worth tracking."',
        '"Summarize today\'s news from technology, product, and business angles."',
        '"Start with developer-relevant AI news, then cover other major updates."',
        '"Generate a version of today\'s AI briefing suitable for team chat."',
    ],
    "preference": [
        '"From now on, prioritize Agent, AI Coding, and open-source model news for me."',
        '"Show less fundraising news and more product launches and technical updates."',
        '"I am a product manager. Organize news by competitor moves and user value."',
        '"Use English output, keep it concise, and give me top 8 every day."',
        '"I mainly care about updates from OpenAI, Anthropic, and Google."',
        '"Use an engineer perspective and focus on tools, frameworks, and infrastructure."',
        '"Exclude marketing and announcement-heavy stories; keep only high-signal updates."',
        '"Add multimodal and chip topics to my interests and lower fundraising weight."',
        '"Remember my preference: Chinese output, deeper analysis, and key takeaways."',
        '"Use a researcher perspective and prioritize papers, benchmarks, and method innovation."',
    ],
    "automation": [
        '"Help me set up a daily AI news briefing plan at 9:00 AM."',
        '"I want an AI weekly brief every Monday. Start with a platform-agnostic setup."',
        '"For OpenClaw, generate an executable scheduled pull configuration."',
        '"For Hermes, provide setup steps for daily delivery."',
        '"Give me both cron and GitHub Actions automation guides so I can choose."',
        '"Use Asia/Shanghai timezone and push tech-focused AI news at 8:30 AM daily."',
        '"Send me a short AI digest every weekday morning with source links."',
        '"Provide configuration guidance for daily delivery to a Discord channel."',
        '"Provide a practical automation integration guide for WeChat/WeCom."',
        '"Draft the automation intent first: frequency, time, timezone, channel, and format."',
    ],
    "workflow": [
        '"Turn today\'s news into an AI Coding tech radar."',
        '"Rewrite today\'s news into publish-ready content materials."',
        '"Generate a structured note version suitable for knowledge base capture."',
        '"Based on today\'s news, produce a product opportunity scan."',
        '"Output an investment/strategy brief focused on fundraising, M&A, and regulation."',
        '"Convert today\'s news into a Notion-ready weekly meeting material format."',
        '"Generate an Obsidian-ready knowledge card format."',
        '"Restructure the news into a newsletter draft with 5 sections."',
        '"Create an executive-facing AI strategy observation brief."',
        '"Transform today\'s news into a team task list with actionable items."',
    ],
}


_TIP_TITLES: Dict[str, str] = {
    "onboarding": "🚀 You can say this directly:",
    "preference": "🎯 Set preferences (send one line directly):",
    "automation": "⚡ Set automation (copy one line and send):",
    "workflow": "🧰 Workflow templates (pick one and send):",
}


def _sample_examples(tip_type: str, count: int = 2) -> List[str]:
    examples = _TIP_EXAMPLES.get(tip_type, [])
    if not examples:
        return []
    if len(examples) <= count:
        return examples
    return random.sample(examples, count)


def render_growth_tip(tip_type: str) -> str:
    """
    Render tip as markdown block with directly usable command examples.
    Returns empty string for unknown tip type.
    """
    title = _TIP_TITLES.get(tip_type)
    if not title:
        return ""

    examples = _sample_examples(tip_type, count=2)
    if not examples:
        return ""

    lines = ["", "---", title]
    for item in examples:
        lines.append(f"- {item}")
    lines.append("")
    return "\n".join(lines)
