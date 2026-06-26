---
name: openclaw-seedance-prompt-library
description: Search, rewrite, and generate Seedance 2.0 video prompts with cinematic variants and bilingual output. Seedance提示词检索/改写/生成
---

# OpenClaw Seedance Prompt Library

Use this skill to turn a large prompt collection into a practical working system for prompt selection, prompt rewriting, and prompt generation.

Upstream prompt material was adapted from a public Seedance collection. Keep any required license handling at the repository level, not in the normal user-facing output flow.

## Core use cases

- Find Seedance prompt examples by style, subject, motion, or camera language
- Rewrite a weak prompt into a stronger cinematic prompt
- Convert Chinese prompts to English and English prompts to Chinese
- Turn a user idea into a Seedance-ready prompt pack
- Extract reusable prompt patterns from the library instead of copying blindly

## Working model

Do not dump a giant wall of prompts.

Instead:
1. classify the user's goal
2. search for 3-8 relevant examples
3. identify what actually makes them work
4. synthesize a better prompt for the user's use case
5. return a small, usable set of outputs

## Output modes

Choose the output format that best fits the request:

### 1) Prompt shortlist
Use when the user wants inspiration.

Return:
- 3-8 relevant prompt examples
- one-line note on why each is relevant
- optional source title / ID when available

### 2) Prompt rewrite
Use when the user already has a rough prompt.

Return:
- original prompt
- improved prompt
- what changed: subject / motion / camera / lighting / duration / aspect ratio / pacing

### 3) Prompt pack
Use when the user wants multiple options.

Return 3 variants:
- **safe** — closest to user's request
- **stylized** — stronger cinematic/style choices
- **experimental** — more ambitious motion or scene design

### 4) Bilingual prompt delivery
Use when the user needs Chinese + English.

Return:
- Chinese version
- English version
- short note on any non-literal adaptation

### 5) Prompt generator
Use when the user gives only an idea, image concept, mood, or rough scene.

Return:
- **core prompt** — strongest balanced version
- **safe** — most reliable generation version
- **stylized** — stronger visual identity and camera language
- **experimental** — higher-risk, higher-novelty version
- optional **negative / avoid notes** if they help reduce model drift
- optional **CN + EN** pair when bilingual output helps

## Prompt construction rules

When rewriting or creating prompts, prefer this structure:

1. **Subject** — who / what is on screen
2. **Scene** — environment and setting
3. **Action** — what changes over time
4. **Camera** — shot type, movement, framing
5. **Style** — cinematic, anime, realistic, surreal, etc.
6. **Lighting / mood** — color, atmosphere, time of day
7. **Output constraints** — duration, resolution, aspect ratio if useful

If the source example is strong, extract the structure, not just the wording.

## Generator workflow

When the user gives only a rough idea, generate prompts in this order:

1. lock the subject and scene
2. choose one dominant motion arc
3. choose one camera logic
4. add one style layer, not five competing ones
5. add constraints only if they improve reliability
6. output a **core prompt** first
7. then derive **safe / stylized / experimental** variants

If the request is weak or underspecified, fill gaps with plausible cinematic defaults instead of asking too many questions.

## Quality rules

- Prefer specificity over adjectives spam
- Prefer concrete motion over vague “dynamic” wording
- Prefer camera instructions that imply visual change
- Avoid contradictory style directions
- Keep prompt length proportional to complexity
- If a user asks for a simple result, do not over-engineer it

## Safety notes

- If copyright or character/IP risk is high, flag it and offer an original alternative
- Prefer transformed prompt synthesis over verbatim copying
- If a user wants a close clone of a known character or franchise scene, offer an adjacent original version too

## References

Read these files as needed:

- `references/usage-patterns.md` — how to search, adapt, and package prompts
- `references/source-attribution.md` — source repo, license, and reuse rules
- upstream dataset: `https://github.com/YouMind-OpenLab/awesome-seedance-2-prompts`

## Optional helper scripts

- `scripts/search-seedance-readme.mjs` — keyword search against upstream README prompt entries via GitHub raw URLs
