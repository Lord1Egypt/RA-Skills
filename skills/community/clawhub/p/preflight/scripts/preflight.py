#!/usr/bin/env python3
"""
Preflight — Pre-publish audience reaction simulator.
Runs content through diverse personas via local Ollama and returns a verdict.

Usage:
    python preflight.py "Your tweet or launch copy here"
    python preflight.py --file post.md
    python preflight.py --file post.md --personas custom-personas.md
    python preflight.py "copy here" --model qwen2.5:14b
    python preflight.py "copy here" --format json
"""

import argparse
import json
import os
import sys
import time
from dataclasses import dataclass, field
from typing import Optional

try:
    from openai import OpenAI
except ImportError:
    print("Error: openai package required. Install with: pip install openai")
    sys.exit(1)


# Default personas (used if no personas file provided)
DEFAULT_PERSONAS = [
    {
        "name": "The Scroller",
        "archetype": "casual social media user",
        "prompt": "You are a 22-year-old college student who spends 3+ hours daily on TikTok and Instagram. You have zero patience — if something doesn't hook you in 2 seconds, you scroll past. You judge everything by whether you'd send it to your group chat. You don't read past the first line unless it's funny or shocking."
    },
    {
        "name": "The Skeptic",
        "archetype": "experienced tech user",
        "prompt": "You are a 34-year-old developer who has seen 1000 product launches. You're immune to hype. You evaluate: is this real? is this different? what's the catch? You will fact-check claims and call out bullshit. You've been burned by vaporware before."
    },
    {
        "name": "The Ready Buyer",
        "archetype": "clear purchase intent",
        "prompt": "You are a 38-year-old professional with disposable income. You're willing to pay for value but don't care about hype. You want clarity: what is it, what does it cost, how do I start. You'll bounce if confused — not because of price but because of friction."
    },
    {
        "name": "The Amplifier",
        "archetype": "content creator",
        "prompt": "You are a 27-year-old content creator with 50K+ followers. You're always looking for content angles. You evaluate: can I make a video or post about this? You care about novelty, visual appeal, and controversy potential. You'll share if it's interesting, even if you don't personally use it."
    },
    {
        "name": "The Worrier",
        "archetype": "privacy-conscious user",
        "prompt": "You are a 45-year-old who reads terms of service and uses ad blockers. Your first question is always 'what's the catch?' and your second is 'what happens to my data?' Missing trust signals make you immediately suspicious. You will warn others publicly if something feels sketchy."
    },
    {
        "name": "The Parent",
        "archetype": "family gatekeeper",
        "prompt": "You are a 40-year-old parent evaluating this on behalf of your family. Your concerns: safety, appropriateness, cost, value. You ask 'would I be comfortable with my kid seeing this?' If it passes your filter, you become an evangelist in parent groups."
    },
    {
        "name": "The Competitor",
        "archetype": "someone in your space",
        "prompt": "You are a 30-year-old building something similar or adjacent. You evaluate positioning, pricing, and differentiation. You're looking for weaknesses to exploit and strengths to copy. Your reaction reveals how defensible the positioning is."
    },
    {
        "name": "The Confused",
        "archetype": "doesn't get it",
        "prompt": "You are a 55-year-old who isn't tech-savvy. You might be the user's parent or boss. If you don't understand something in one sentence, it fails. You test whether the value proposition is clear to normal people. Your most valuable feedback is 'I don't get it.'"
    },
]

EVALUATION_PROMPT = """You are evaluating a piece of content that someone is about to publish. React honestly based on your persona.

THE CONTENT:
---
{content}
---

Answer these 4 questions in character. Be specific, blunt, and honest. No hedging.

1. FIRST REACTION (1-2 sentences): What's your gut reaction in the first 3 seconds?
2. WOULD YOU ENGAGE? (yes/no + why): Would you like, comment, click, or reply?
3. WOULD YOU SHARE? (yes/no + why): Would you send this to someone or repost it?
4. ONE REWRITE (1-2 sentences): If you could change one thing to make this work better for you, what would it be?

Keep your total response under 150 words. No preamble."""


@dataclass
class PersonaResult:
    name: str
    archetype: str
    reaction: str
    would_engage: bool
    would_share: bool
    raw_response: str


@dataclass
class PreflightResult:
    content: str
    personas: list
    results: list = field(default_factory=list)
    verdict: str = ""
    summary: str = ""
    engage_rate: float = 0.0
    share_rate: float = 0.0
    elapsed_seconds: float = 0.0


def load_personas_from_file(path: str) -> list:
    """Parse personas from a markdown file."""
    personas = []
    current = None

    with open(path, 'r') as f:
        lines = f.readlines()

    for line in lines:
        line = line.rstrip()
        if line.startswith('### '):
            if current:
                personas.append(current)
            name = line[4:].strip()
            # Split on ( to get archetype
            if '(' in name:
                parts = name.split('(')
                name = parts[0].strip()
                archetype = parts[1].rstrip(')').strip()
            else:
                archetype = ""
            current = {"name": name, "archetype": archetype, "prompt": ""}
        elif current and line.startswith('- '):
            current["prompt"] += line[2:] + " "

    if current:
        personas.append(current)

    # Build proper prompts from bullet points
    for p in personas:
        if p["prompt"]:
            p["prompt"] = f"You are {p['name']} ({p['archetype']}). {p['prompt'].strip()}"

    return personas if personas else DEFAULT_PERSONAS


def run_preflight(
    content: str,
    personas: list = None,
    model: str = "qwen2.5:32b",
    base_url: str = "http://localhost:11434/v1",
    output_format: str = "text"
) -> PreflightResult:
    """Run content through all personas and return results."""

    if personas is None:
        personas = DEFAULT_PERSONAS

    client = OpenAI(api_key="ollama", base_url=base_url)
    result = PreflightResult(content=content, personas=[p["name"] for p in personas])

    start = time.time()

    for persona in personas:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": persona["prompt"]},
                    {"role": "user", "content": EVALUATION_PROMPT.format(content=content)}
                ],
                temperature=0.8,
                max_tokens=300,
            )

            raw = response.choices[0].message.content.strip()

            # Parse engagement/share signals from response
            lower = raw.lower()
            would_engage = any(phrase in lower for phrase in [
                "yes", "i would", "i'd click", "i'd comment", "i'd like",
                "definitely", "absolutely", "for sure"
            ]) and "1." in raw  # rough heuristic

            would_share = "yes" in lower.split("share")[0][-30:] if "share" in lower else False

            pr = PersonaResult(
                name=persona["name"],
                archetype=persona["archetype"],
                reaction=raw,
                would_engage="yes" in lower[:200],
                would_share=would_share,
                raw_response=raw
            )
            result.results.append(pr)

            # Progress indicator
            print(f"  ✓ {persona['name']}", file=sys.stderr)

        except Exception as e:
            print(f"  ✗ {persona['name']}: {e}", file=sys.stderr)

    result.elapsed_seconds = time.time() - start

    # Calculate rates
    if result.results:
        result.engage_rate = sum(1 for r in result.results if r.would_engage) / len(result.results)
        result.share_rate = sum(1 for r in result.results if r.would_share) / len(result.results)

    # Generate verdict
    if result.share_rate >= 0.5:
        result.verdict = "🟢 SHIP IT"
    elif result.engage_rate >= 0.5:
        result.verdict = "🟡 REVISE — engaging but not shareable"
    elif result.engage_rate >= 0.25:
        result.verdict = "🟠 RETHINK — mixed signals"
    else:
        result.verdict = "🔴 KILL IT — not landing"

    # Build summary
    result.summary = f"""PREFLIGHT RESULTS
{'=' * 50}
Verdict: {result.verdict}
Engage rate: {result.engage_rate:.0%} ({sum(1 for r in result.results if r.would_engage)}/{len(result.results)} personas)
Share rate: {result.share_rate:.0%} ({sum(1 for r in result.results if r.would_share)}/{len(result.results)} personas)
Time: {result.elapsed_seconds:.1f}s ({len(result.results)} personas)
{'=' * 50}
"""

    for r in result.results:
        engage_icon = "👍" if r.would_engage else "👎"
        share_icon = "🔄" if r.would_share else "—"
        result.summary += f"\n{engage_icon} {share_icon} {r.name} ({r.archetype})\n"
        result.summary += f"{r.raw_response}\n"
        result.summary += f"{'-' * 40}\n"

    return result


def main():
    parser = argparse.ArgumentParser(description="Preflight — pre-publish audience reaction check")
    parser.add_argument("content", nargs="?", help="Content to test (or use --file)")
    parser.add_argument("--file", "-f", help="Read content from file")
    parser.add_argument("--personas", "-p", help="Custom personas markdown file")
    parser.add_argument("--model", "-m", default="qwen2.5:32b", help="Ollama model (default: qwen2.5:32b)")
    parser.add_argument("--base-url", default="http://localhost:11434/v1", help="Ollama API base URL")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="Output format")
    parser.add_argument("--fast", action="store_true", help="Use fewer personas (Scroller, Skeptic, Buyer, Amplifier)")

    args = parser.parse_args()

    # Get content
    if args.file:
        with open(args.file) as f:
            content = f.read().strip()
    elif args.content:
        content = args.content
    elif not sys.stdin.isatty():
        content = sys.stdin.read().strip()
    else:
        parser.error("Provide content as argument, --file, or via stdin")

    # Get personas
    personas = None
    if args.personas:
        personas = load_personas_from_file(args.personas)
    elif args.fast:
        personas = DEFAULT_PERSONAS[:4]  # Scroller, Skeptic, Buyer, Amplifier

    print(f"\n🛫 Preflight check — {len(personas or DEFAULT_PERSONAS)} personas\n", file=sys.stderr)

    result = run_preflight(
        content=content,
        personas=personas,
        model=args.model,
        base_url=args.base_url,
        output_format=args.format
    )

    if args.format == "json":
        output = {
            "verdict": result.verdict,
            "engage_rate": result.engage_rate,
            "share_rate": result.share_rate,
            "elapsed_seconds": result.elapsed_seconds,
            "personas": [
                {
                    "name": r.name,
                    "archetype": r.archetype,
                    "would_engage": r.would_engage,
                    "would_share": r.would_share,
                    "response": r.raw_response
                }
                for r in result.results
            ]
        }
        print(json.dumps(output, indent=2))
    else:
        print(result.summary)


if __name__ == "__main__":
    main()
