---
name: hair-makeover-video
version: 1.0.0
description: "Generate vertical short videos of hair makeover / dye transformation (WeryAI): scissor cuts, color gradients, and strong before/after contrast. Use when you need a hair transformation reel, salon dye glow-up clip, or the user asks for a cat getting bangs or gray hair dyed rose-gold. SEO: hair makeover video; hair transformation video generation."

tags: [hair, makeover, transformation, contrast, fashion, short-video]

metadata: { "openclaw": { "emoji": "💇", "primaryEnv": "WERYAI_API_KEY", "paid": true, "network_required": true, "requires": { "env": ["WERYAI_API_KEY"], "bins": ["node"], "node": ">=18" } } }
user-invocable: true
---

# Hair makeover video generation

That satisfying snip—blades close, long hair drops, clean short lines appear. No VO needed; the frame *is* the hook. Lion from messy mane to sharp groom, puppy afro to sleek cut, cat in pink-to-blue gradient: that’s the core visual every run targets.

**Dependencies**: `scripts/video_gen.js` in this directory + `WERYAI_API_KEY` + Node.js 18+. No dependency on other Cursor skills.


## Prerequisites

- `WERYAI_API_KEY` **must be set** in the environment before running `video_gen.js`.
- Node.js **18+** is required. Image inputs **must** be public `https` URLs (no local file paths).
- Each successful `wait` run consumes WeryAI credits; re-running creates new paid tasks.

## Security, secrets, and API hosts

- **`WERYAI_API_KEY`**: Treat as a secret. Only configure it if you trust this skill's source; it is listed in OpenClaw metadata as **`requires.env`** / **`primaryEnv`** so installers know it is mandatory at runtime (never commit it inside the skill package).
- **API hosts (fixed in `video_gen.js`)**: Video tasks use **`https://api.weryai.com`**; the models list uses **`https://api-growth-agent.weryai.com`**. Only **`WERYAI_API_KEY`** is read from the environment—do not rely on URL-related environment variables.
- **Higher assurance**: Run generation in a short-lived or isolated environment (separate account or container), and review `scripts/video_gen.js` (HTTPS submit + poll loop) before production use.


## Prompt expansion (mandatory)

`video_gen.js` does **not** expand prompts. Before every `wait --json`, turn the user's short or vague brief into a **full English production `prompt`**.

**When:** The user gives only keywords, one line, or loose intent—or asks for richer video language. **Exception:** They paste a finished long prompt within the model's `prompt_length_limit` and ask you **not** to rewrite; still show the **full** text in the confirmation table.

**Always add (video language):** shot scale and angle; camera move or lock-off; light quality and motivation; subject action paced to `duration`; **one clear payoff** for this niche; state **9:16 vertical** when this skill defaults to vertical.

**Length:** Obey `prompt_length_limit` for the chosen `model_key` when this doc lists it; trim filler adjectives before removing core action, lens, or light clauses.

**Confirmation:** The pre-submit table **must** include the **full expanded `prompt`** (never a one-line summary). Wait for **confirm** or edits.

### Niche checklist

- **Transform arc:** before → cut/color/style → **after reveal**; salon or natural light; strand motion and silhouette change.
- **Camera:** mirror, chair spin, or profile comparison; **9:16** if default vertical.
- **Species/character:** if anthropomorphic, keep grooming readable and on-brief.

**`### Example prompts`** at the top of this file are **short triggers only**—always expand from the user's actual request.

## Workflow

1. Confirm the user request matches this skill's scenario (text-to-video and/or image-to-video as documented).
2. Collect the user's **brief**, optional image URL(s), tier (**best** / **good** / **fast**) or an explicit `model` key.
3. **Expand prompt (mandatory):** Unless the user supplied a finished long prompt and explicitly asked not to rewrite it, expand the brief into a full English production `prompt` using `## Prompt expansion (mandatory)` below. **Do not** call the API with only the user's minimal words.
4. Check the **expanded** `prompt` against the selected model's `prompt_length_limit` in the frozen tables in this document (when present); shorten if needed.
5. Verify `duration`, `aspect_ratio`, `resolution`, `generate_audio`, `negative_prompt`, and other fields against the frozen tables and API notes in this SKILL.md.
6. Show the pre-submit parameter table including the **full expanded `prompt`**; wait for **confirm** or edits.
7. After confirmation, run `node {baseDir}/scripts/video_gen.js wait --json '...'` with the **expanded** prompt.
8. Parse stdout JSON and return video URLs; on failure, surface `errorCode` / `errorMessage` and suggest parameter fixes.

## CLI reference

```sh
node {baseDir}/scripts/video_gen.js wait --json '{"model":"…","prompt":"…","duration":5,"aspect_ratio":"9:16"}'
node {baseDir}/scripts/video_gen.js wait --json '…' --dry-run
node {baseDir}/scripts/video_gen.js status --task-id <id>
```

## Definition of done

Done when the user receives at least one playable video URL from the API response, or a clear failure explanation with next steps. All parameters used **must** fall within the selected model's allowed sets in this document. The submitted `prompt` **must** be the **expanded** production prompt unless the user explicitly supplied a finished long prompt and asked not to rewrite it.

## Boundaries (out of scope)

- Does not review platform compliance, copyright, or portrait rights; does not guarantee commercial usability of outputs.
- Does not provide non-WeryAI offline rendering, traditional edit timelines, or API field combinations not documented here.
- Does not hard-code absolute paths in the skill doc; `{baseDir}` means the skill package root (same level as `SKILL.md`).

### Example prompts

- `Bunny haircut: scissors snap, ends fall, before/after vibe shift, vertical fashion glow-up`
- `Use this bare-face character image: dye process from dark to light gold`
- `Blow-dry + curling wand in 5s, finish with hair-flip slow motion`
- `Hair makeover glow-up 9:16, before/after in one vertical clip`

---

## Default parameters

| Field | Value |
|-------|-------|
| Model | KLING_V3_0_PRO |
| Aspect ratio | 9:16 (fixed vertical) |
| Duration | 5 seconds (`duration`: 5—tight peak beat) |
| Audio | Off |
| Visual style | Side or front medium; salon lighting; scissor / brush close-ups; clear strand texture; before/after in one frame or hard cut |

> **API validity (default `KLING_V3_0_PRO`):** Text-to-video `duration` only **5 / 10 / 15**; `aspect_ratio` only **9:16, 1:1, 16:9**. Image-to-video `aspect_ratio` only **9:16, 16:9, 1:1**. **No `resolution` field—do not send it.** For **fast** tier with VEO: text-to-video **`VEO_3_1_FAST`**, image-to-video **`CHATBOT_VEO_3_1_FAST`**, with `duration` **fixed at 8**, `aspect_ratio` only **9:16** or **16:9**. When switching `model_key`, follow the allowed sets in this section’s model/API constraints and the API validity note above; do not send `resolution` to models that do not support it.

---

## Anthropomorphic character haircut glow-up

High completion pattern: big hair / messy mane in the chair → decisive cut → locks fall → camera follows strands down then reveals the full new look.

**The user should provide:**
- Character (lion / puppy / cat / bunny / custom)
- Before state (afro / tangled long / messy fur / bangs covering eyes)
- Target style (sharp short / sleek bob / minimal buzz / layered editorial cut)

**Generation flow:**
1. Collect character, before state, target style.
2. Build the prompt around **the snip** as the climax—slow-motion falling hair and a clear vibe shift after.
3. Show parameters and wait:
**You must show all parameters in a table and wait for explicit user confirmation before submitting:**

   > 📋 **Ready to generate—please confirm:**
   >
   > | Parameter | This run | Notes |
   > |-----------|----------|-------|
   > | `model` | `KLING_V3_0_PRO` | Best default; **fast**: text `VEO_3_1_FAST`, image `CHATBOT_VEO_3_1_FAST` (`duration` 8); **good** → `KLING_V3_0_STA`; or name a model |
   > | `aspect_ratio` | `9:16` | Default KLING: 9:16, 1:1, 16:9 |
   > | `duration` | `5s` | KLING: 5 / 10 / 15; VEO fast: 8 only |
   > | `generate_audio` | `false` | Whether to auto-generate audio |
   > | `prompt` | **Full expanded English prompt** (entire text for this run) | Revise before confirm |
   > | `Loop seam` | No | Reply “loop” for seamless loop |
   >
   > Reply **“confirm”** to start, or list what to change.
4. After confirmation (`{baseDir}` is skill root):

   ```sh
   node {baseDir}/scripts/video_gen.js wait --json '{"model":"（model from confirmation table）","prompt":"（full English prompt）","aspect_ratio":"9:16","duration":5,"generate_audio":true}'
   ```

   Match table to JSON; add `resolution` only if supported. Parse stdout `videos`.

**Parameter configuration:**

| Field | Value |
|-------|-------|
| model | KLING_V3_0_PRO |
| aspect_ratio | 9:16 |
| duration | 5 |
| generate_audio | false |

**Expanded prompt:** Compose at generation time per `## Prompt expansion (mandatory)` from the user's actual brief—do not reuse fixed sample paragraphs.

**Expected outcome:** Snip in slow-mo as the peak, readable strand texture, strong before/after vibe—tight, satisfying pacing for transformation edits.

---

## Dye color change close-up

Color is the star: base (white / black / brown) through process to vivid / gradient / candy tones—saturation and material read matter more than cut shape.

**The user should provide:** character, starting color, target colors (e.g. “mint ombré,” “all-over flame red,” “silver with gold money piece”)

Build a color-forward prompt; show confirmation; submit.

> Parameters are shown before generation; wait for confirmation before submit.

**Expanded prompt:** Compose at generation time per `## Prompt expansion (mandatory)` from the user's actual brief—do not reuse fixed sample paragraphs.

---

## Core hook vocabulary

**Cut satisfaction:** `decisive scissor cut in slow motion`, `hair strands cascade downward`, `satisfying snip sound`, `locks fall away revealing shape beneath`

**Color payoff:** `vivid color saturation reveal`, `luminous gradient color shift`, `color payoff immediate and intense`, `iridescent color catches light`

**Vibe flip:** `from chaotic to sophisticated`, `before-after energy`, `complete character transformation`, `posture and confidence shift visible`

> **Tip:** For a “one-cut climax,” add `the decisive first cut is the climax of the video` so pacing clusters on that beat instead of evenly spacing every step.
