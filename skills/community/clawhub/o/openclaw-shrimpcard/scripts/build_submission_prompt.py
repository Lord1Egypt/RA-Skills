#!/usr/bin/env python3
import argparse
from pathlib import Path

from identity_rules import brand_guidance
from skill_paths import require_live_input
from validate_json import load_json


def language_instruction(lang: str) -> str:
    if lang == "zh":
        return "Write every final public-facing field in Chinese only, matching the user's language. Do not include bilingual duplicates or mixed-language values."
    return "Write every final public-facing field in English only, matching the user's language. Do not include bilingual duplicates or mixed-language values."


def build_prompt(snapshot: dict, lang: str) -> str:
    agent = snapshot["agent"]
    owner = snapshot["owner"]
    evidence_lines = []
    for item in snapshot["evidence_items"][:10]:
        evidence_lines.append(f"- [{item['type']}] {item['summary']}")

    return f"""You are {agent['name']}, preparing your own public self-introduction submission.

You must produce valid JSON only.

Your owner is {owner['name']}.

Important:
- write about the current target agent described by the live evidence, not a repository example or fixture agent
- if the only evidence available is a sample/example file, stop and ask the human for the real agent evidence before continuing
- do not copy a named example agent such as Hermes, sample agent, or any preview fixture identity into the final submission

Your task is not to sound impressive.
Your task is to sound specific, truthful, and shareable.

Owner info rule:
- if owner name or contact is missing from evidence, memory, and saved preferences, stop and ask the human
- do not guess owner identity fields
- do not leave sample or placeholder owner identity in the final JSON

Evidence window:
- {snapshot['evidence_window']['summary']}

Evidence samples:
{chr(10).join(evidence_lines)}

Output target:
`agent-self-intro-submission/1.0`

Hard rules:
- every field below should already have been compressed to fit during the earlier memory-search stage
- do not rely on final validation as the first time you discover length violations
- `role`: short, concrete, <= 32 chars
- `tagline`: one sentence, <= 42 chars
- `value_line`: <= 52 chars
- `top_capabilities`: exactly 3 distinct items, each concise and <= 12 chars
- `best_for`: one scenario, not a list
- `proof_anchor`: one sentence, must mention evidence or memory basis
- `share_keywords`: 3 to 4 distinct items, short and readable
- `persona_tags`: exactly 3 distinct items, each <= 12 chars
- `poster_headline`: <= 28 chars preferred
- `poster_subline`: <= 36 chars preferred
- `share_caption`: <= 48 chars preferred
- `visual_brief`: <= 72 chars preferred
- `selfie_prompt`: must explicitly indicate standard 8-bit pixel art direction
- `visual_brief` and `selfie_prompt` must describe a recognizable character concept, not abstract shapes or icons
- all short fields must stay readable to a stranger, not compressed into cryptic fragments

Disallowed:
- generic claims like "powerful", "strong reasoning", "general-purpose assistant"
- long tool lists
- vague aspirational abilities
- lobster style unless the identity truly fits
- unreadable shorthand, internal abbreviations, or keyword stuffing
- any wording copied from sample, preview, or format-reference files in this repo
- placeholder identities such as sample agent, sample owner, preview mode, or format example only
- oversized draft text that was never compressed during the evidence stage

Agent-family guidance:
{brand_guidance(snapshot)}

Language rule:
{language_instruction(lang)}

Output shape:
{{
  "schema_version": "agent-self-intro-submission/1.0",
  "agent": {{ ...preserve current agent fields... }},
  "owner": {{ ...preserve current owner fields... }},
  "identity": {{
    "role": "",
    "tagline": "",
    "value_line": "",
    "top_capabilities": ["", "", ""],
    "best_for": "",
    "proof_anchor": "",
    "memory_basis": "",
    "source_count": 0,
    "share_keywords": ["", "", ""],
    "persona_tags": ["", "", ""],
    "poster_headline": "",
    "poster_subline": "",
    "share_caption": "",
    "visual_brief": "",
    "character_style": "agent-avatar",
    "selfie_prompt": ""
  }}
}}

Return JSON only.
"""


def main():
    parser = argparse.ArgumentParser(description="Build a submission prompt for an agent to author a self-intro payload")
    parser.add_argument("evidence_json", help="Path to agent evidence JSON")
    parser.add_argument("--out", default="self-intro-submission-prompt.txt", help="Output prompt path")
    parser.add_argument("--lang", choices=["zh", "en"], default="zh", help="Language for final card text")
    args = parser.parse_args()

    input_path = Path(args.evidence_json)
    require_live_input(input_path, "evidence_json")
    snapshot = load_json(input_path)
    prompt = build_prompt(snapshot, args.lang)
    Path(args.out).write_text(prompt.rstrip() + "\n", encoding="utf-8")
    print(f"[OK] Wrote self-intro submission prompt to {args.out}")


if __name__ == "__main__":
    main()
