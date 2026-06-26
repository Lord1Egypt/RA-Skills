---
name: openclaw-shrimpcard
description: Use when an agent needs to turn evidence-backed behavior into a validated self-intro submission, a share-card JSON payload, and a final screenshot-friendly HTML selfie card with a real 8-bit character image.
---

# Agent Selfie Card

Use this repository as one self-contained skill package.

Canonical flow:

`agent-evidence -> agent-self-intro-submission -> share-card -> final image -> selfie-card.html`

## Use this skill for

- turning repeated agent evidence into a concise public identity
- rejecting generic self-description before it becomes public copy
- producing a validated `share-card/1.0` payload
- rendering a screenshot-friendly HTML card only after a real image is attached

## Do not do

- do not invent identity claims that are not repeated in evidence
- do not guess missing owner identity fields
- do not stop at prompt-only or placeholder-image state
- do not force lobster branding unless it is already true for the agent
- do not derive the target agent's public identity from the skill name, repo name, script path, package name, or interface label

## Workflow

Runtime note:
- install Python dependencies from `requirements.txt` before running the scripts
- files under `examples/` are smoke-test fixtures only; never treat them as the live target agent's evidence or submission
- if the only available inputs are fixture/example files, stop and ask the human for the real agent evidence

1. Gather evidence
- Prefer `agent-evidence/1.0`.
- Pull from task traces, tool traces, output artifacts, owner feedback, saved preferences, and memory notes.
- Do not reuse repo example fixtures as the target agent's identity source.
- Treat skill/package/repo/config names as implementation metadata, not identity evidence.

2. Build memory-search notes
- Use `scripts/build_memory_search_prompt.py`.
- Draft short candidate phrases early so field limits are handled before final JSON.
- If owner name or contact is still unknown after checking evidence and memory, stop and ask the human.

3. Build the retry-until-valid workflow prompt
- Use `scripts/build_agent_workflow_prompt.py`.
- Pass `--lang zh` or `--lang en` so final card copy matches the user language.
- Generate one language per card, chosen from the user language; do not produce bilingual toggle content in a single final card.

4. Build the submission prompt
- Use `scripts/build_submission_prompt.py`.
- The agent authors `agent-self-intro-submission/1.0` itself.

5. Validate and retry
- Use `scripts/validate_self_intro_submission.py`.
- Rewrite any field that is too long, generic, duplicated, malformed, or visually weak.

6. Convert to share card
- Use `scripts/submission_to_share_card.py`.

7. Build the image task
- Use `scripts/build_image_task_prompt.py`.
- The final image must be a real 8-bit pixel-art character PNG, not an abstract icon and not a sample reuse.

8. Attach image and validate bundle
- Use `scripts/attach_generated_image.py`.
- Use `scripts/validate_final_bundle.py`.

9. Render HTML
- Use `scripts/render_card_html.py`.
- Final rendering should happen only after bundle validation passes.
- After rendering, run `scripts/validate_rendered_html.py`.
- The final HTML must not expose internal `card_id` text on the poster face.
- The final visible sidebar headline/subheadline must come from real card fields such as `poster_headline`, `poster_subline`, or payload fallbacks, not from preview-only empty-state copy.

## Key rules

- describe repeated observed behavior, not hypothetical ability
- prefer owner value over tool trivia
- if live evidence does not explicitly establish a branded agent identity, use a neutral identity
- default to neutral naming and `character_style: agent-avatar` when special branding is not clearly evidenced
- only use special names or mascots such as OpenClaw, Hermes, lobster, shrimp, crab, or similar when those signals are explicit in repeated live evidence or explicitly requested by the human
- `top_capabilities`: exactly 3
- `persona_tags`: exactly 3 and distinct
- `share_keywords`: 3 to 4 and distinct
- short fields must stay readable, not cryptic
- all final public-facing text must be in one language only, matching the user language for that run
- `selfie_prompt` must explicitly require 8-bit or pixel-art direction
- `visual_brief` and `selfie_prompt` must describe one recognizable character concept
- `character_style: lobster` is valid only for claw/lobster-branded agents unless the user explicitly overrides it
- `card_id` is metadata only; do not surface it as visible poster copy
- when rendering a final card with real data, visible preview placeholders must be fully replaced by real card text

## Bundled resources

- `schemas/`: local schema copies used by validators
- `scripts/`: prompt builders, validators, converters, image attachment, HTML renderer, rendered-HTML QA
- `assets/card-template.html`: final card template
- `references/agent-self-extraction-guide.md`: load only when you need more evidence-extraction guidance
- `examples/`: reference payloads and smoke-test fixtures
