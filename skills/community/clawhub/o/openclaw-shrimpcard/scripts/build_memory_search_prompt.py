#!/usr/bin/env python3
import argparse
from pathlib import Path

from identity_rules import brand_guidance
from skill_paths import require_live_input
from validate_json import load_json


def language_instruction(lang: str) -> str:
    if lang == "zh":
        return "Write all candidate card phrases in Chinese only, matching the user's language. Do not mix Chinese and English within the same card draft."
    return "Write all candidate card phrases in English only, matching the user's language. Do not mix English and Chinese within the same card draft."


def build_prompt(payload: dict, lang: str) -> str:
    agent = payload.get("agent", {})
    owner = payload.get("owner", {})
    return f"""You are {agent.get('name', 'the agent')}.

Your owner is {owner.get('name', 'the owner')}.

Before writing any public self-introduction, search your own memory and work traces.

Target-agent rule:
- search for the current live agent identity only
- do not let a repository example, smoke-test fixture, preview payload, or sample agent become the target identity
- if you only have fixture/example files and no live evidence, stop and ask the human for the real target agent evidence

Search these sources if available:
- long-term memory
- saved preferences
- recent task history
- tool-call history
- recurring output artifacts
- owner corrections or praise

Missing-owner-info rule:
- if owner name or contact is required for the final card, inspect memory and saved preferences first
- if that information is still unknown after checking available evidence, stop and ask the human owner directly
- do not invent, guess, or keep placeholder owner identity in a final card

Do not summarize everything.
Only keep what is repeated, stable, and evidence-backed.

Your job is to produce working notes in 5 buckets:

1. Repeated jobs
- What tasks do you repeatedly complete?

2. Workflow patterns
- How do you usually work?
- For example: structure first, search first, validate before answer, draft before polish

3. Recurring outputs
- What do you often hand back?
- Examples: code patches, task breakdowns, reply templates, summaries, launch copy

4. Owner-facing value
- What value repeatedly matters to the owner?
- Examples: saves time, reduces ambiguity, improves consistency, prevents mistakes

5. Owner preferences
- What explicit constraints does the owner repeatedly signal?

6. Compression candidates for the final card
- Draft candidate phrases for:
  - role
  - tagline
  - value line
  - top capabilities
  - persona tags
  - share keywords
  - poster headline
  - poster subline
  - visual brief
- Keep these as candidate phrases only, not final JSON yet
- Use repeated evidence only
- This compression step is where length limits must already be satisfied
- Do not carry oversized draft phrases into the final submission stage

Length and readability rules for these candidates:
- `role`: <= 32 chars, concrete, readable at first glance
- `tagline`: <= 42 chars, one sentence, outcome-first
- `value_line`: <= 52 chars, clear owner value
- `top_capabilities`: exactly 3 candidates, each <= 12 chars, distinct, plain-language
- `persona_tags`: exactly 3 candidates, each <= 12 chars, distinct, human-readable
- `share_keywords`: 3 to 4 candidates, short, distinct, readable, not cryptic fragments
- `poster_headline`: <= 28 chars, instantly legible
- `poster_subline`: <= 36 chars, easy to scan
- `share_caption`: <= 48 chars, public-facing and readable
- `visual_brief`: <= 72 chars, only the most important visual cues

Before leaving this step:
- trim or rewrite every candidate until it already fits the limit
- if a phrase still exceeds the limit, do not promote it to final submission
- prefer rewriting over blunt truncation

Image-direction candidates:
- Keep image keywords compact and readable
- Every image keyword or cue must map back to the role, persona tags, or top capabilities
- Do not produce cluttered prop lists
- Prefer 1 to 3 strong visual cues over many weak ones
- The final image direction must remain standard 8-bit pixel art and readable after crop
- The final image must be a recognizable character, not an abstract icon, logo, symbol, or geometry study
- A stranger should be able to name the subject in one short phrase

Rules:
- Do not include one-off wins
- Do not include hypothetical abilities
- Do not include tool trivia unless it directly explains repeated value
- Attach evidence references whenever possible
- Do not reuse wording, role, capabilities, or visual direction from this repo's sample files
- Collapse duplicates
- Keep wording compact enough for a later public card
- If a keyword or sentence becomes short but unreadable, rewrite it for clarity instead of over-compressing
- Do not use slogan fragments, abbreviations, or insider shorthand that a stranger would not understand

Family hint:
{brand_guidance(payload)}

Language rule:
{language_instruction(lang)}

Output format:
- plain structured notes or JSON
- each candidate insight should include:
  - label
  - short summary
  - evidence basis
  - confidence

This step is only for searching and organizing memory.
Do not write the final public card yet.
"""


def main():
    parser = argparse.ArgumentParser(description="Build a prompt that guides an agent to search and organize its own memory")
    parser.add_argument("agent_context_json", help="Path to JSON containing at least agent/owner fields")
    parser.add_argument("--out", default="memory-search-prompt.txt", help="Output prompt path")
    parser.add_argument("--lang", choices=["zh", "en"], default="zh", help="Language for candidate card text")
    args = parser.parse_args()

    input_path = Path(args.agent_context_json)
    require_live_input(input_path, "agent_context_json")
    payload = load_json(input_path)
    prompt = build_prompt(payload, args.lang)
    Path(args.out).write_text(prompt.rstrip() + "\n", encoding="utf-8")
    print(f"[OK] Wrote memory-search prompt to {args.out}")


if __name__ == "__main__":
    main()
