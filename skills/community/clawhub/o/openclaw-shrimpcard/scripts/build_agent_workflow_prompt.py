#!/usr/bin/env python3
import argparse
from pathlib import Path

from identity_rules import brand_guidance
from skill_paths import require_live_input
from validate_json import load_json


def language_instruction(lang: str) -> str:
    if lang == "zh":
        return "All final public-facing card text must be in Chinese only, matching the user's language. Do not generate bilingual or mixed-language card content."
    return "All final public-facing card text must be in English only, matching the user's language. Do not generate bilingual or mixed-language card content."


def build_prompt(payload: dict, lang: str) -> str:
    agent = payload.get("agent", {})
    owner = payload.get("owner", {})
    return f"""You are {agent.get('name', 'the agent')}.

Your owner is {owner.get('name', 'the owner')}.

Target selection rule:
- complete the workflow for the current live agent only
- never substitute a repository example, fixture payload, or preview identity as the target agent
- if the only available inputs are example files, stop and ask for live evidence instead of proceeding

You must complete this workflow end-to-end and stop only when every required current-flow artifact passes validation.

Workflow:

1. Search your own memory
- inspect long-term memory
- inspect saved preferences
- inspect recent task history
- inspect tool-call traces
- inspect recurring outputs
- inspect owner corrections or praise

2. Organize what you found
- repeated jobs
- workflow patterns
- recurring outputs
- owner-facing value
- owner preferences
- missing owner identity fields that still need direct human confirmation
- compressed candidate phrases that already satisfy card field limits

3. Write `agent-self-intro-submission/1.0`
- keep every field concise
- keep only repeated, evidence-backed claims
- avoid generic claims like "powerful" or "strong reasoning"
- do not copy wording or identity cues from repo samples or preview placeholders
- if owner name or contact is still unknown after searching available evidence, ask the human before continuing
- if a field is over its limit, rewrite it before entering final JSON

4. Validate the submission
- if any field is too long, duplicated, too generic, or malformed, rewrite and retry

5. Convert the validated submission into `share-card.json`

6. Decide whether you can generate the final image directly
- if your current environment can generate images directly, create the final image now
- the image must be standard 8-bit pixel art
- target canvas: 960x720 PNG
- center the subject and leave safe margin for crop
- the image must be newly generated for the current agent identity, not reused from a repo sample or template
- the image must depict one recognizable character concept, not abstract blocks, symbols, or icons

7. If you cannot generate images directly
- you still must produce a real final image before finishing
- use the agent itself to generate a valid 8-bit image asset by code or available tooling
- do not stop with only a prompt, placeholder, or unattached share card

8. After the image exists, attach it and validate the final bundle
- if there is no image yet, keep going
- if the image is not 8-bit aligned, regenerate
- if the image is abstract or the subject is not clearly recognizable, regenerate
- if final bundle validation fails for any reason, repair and retry

9. Only stop when all of these are true
- submission passes
- image exists
- final bundle passes validation
- final HTML can be rendered from the image-attached share card

Important:
- do not stop after writing text only
- do not fabricate a placeholder image
- do not stop with only an image task prompt
- do not stop if validation still fails
- do not submit sample-owner or sample-agent placeholders as final data
- do not derive the target identity from the skill name, repository name, package name, script path, config file, or interface label
- if live evidence does not explicitly establish a branded identity, keep the public identity neutral and prefer `character_style: agent-avatar`
- {language_instruction(lang)}
- identity guidance:
{brand_guidance(payload)}
- keep retrying until the current flow outputs are valid
"""


def main():
    parser = argparse.ArgumentParser(description="Build a workflow prompt that tells an agent to search memory, generate image, and retry until validated")
    parser.add_argument("agent_context_json", help="Path to JSON containing at least agent/owner fields")
    parser.add_argument("--out", default="agent-workflow-prompt.txt", help="Output prompt path")
    parser.add_argument("--lang", choices=["zh", "en"], default="zh", help="Language for final card text")
    args = parser.parse_args()

    input_path = Path(args.agent_context_json)
    require_live_input(input_path, "agent_context_json")
    payload = load_json(input_path)
    prompt = build_prompt(payload, args.lang)
    Path(args.out).write_text(prompt.rstrip() + "\n", encoding="utf-8")
    print(f"[OK] Wrote agent workflow prompt to {args.out}")


if __name__ == "__main__":
    main()
