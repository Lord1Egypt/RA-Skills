---
name: outfit-transition-video
version: 1.0.0
description: "Generate vertical shorts of anthropomorphic outfit changes on beat (WeryAI): one-second cuts, style jumps, accessory macros. Use when you need outfit transition reels, fashion look-change clips, or users ask for pajamas→gown and sunglasses landing on the downbeat. SEO: outfit transition video; outfit change video generation."

tags: [outfit-change, fashion, style, beat-sync, look, short-video]

metadata: { "openclaw": { "emoji": "👗", "primaryEnv": "WERYAI_API_KEY", "paid": true, "network_required": true, "requires": { "env": ["WERYAI_API_KEY"], "bins": ["node"], "node": ">=18" } } }
user-invocable: true
---

# Outfit transition video generation

Three rhythm-driven hooks:

- **One-second cuts:** each look is a flash—tempo is the content
- **Style jumps:** pajamas→gown, athleisure→cyber—the bigger the gap, the stickier
- **Detail beats:** props in frame, heel tap, sunglasses landing on the beat

Cats / bunnies / pandas as leads; one line for look count and vibe, straight to clip.

**Dependencies:** `WERYAI_API_KEY` + Node.js 18+. When you run the CLI, **`scripts/video_gen.js`** must exist; **[`WERYAI_VIDEO_API.md`](resources/WERYAI_VIDEO_API.md)** must exist under **`resources/`** (supply both via publish or pre-use assembly). Full commands and JSON fields: see **`resources/WERYAI_VIDEO_API.md`**. No other Cursor skills. **Default parameters** and model tiers are in the tables below; live API limits follow **weryai** models. Before installing or running, review the bundled `video_gen.js` to confirm it meets your requirements. Pay particular attention to how it handles local files if you choose to allow their usage, ensuring this behavior aligns with the skill's intended workflow for image-to-video requests.


## Prerequisites

- `WERYAI_API_KEY` **must be set** in the environment before running `video_gen.js`.
- Node.js **18+** is required. Prefer public **`https`** image URLs. If the assembled `scripts/video_gen.js` supports local file paths, review and verify the script first, then get **explicit consent** before it reads a local image and uploads it to WeryAI to obtain a public URL.
- Each successful `wait` run consumes WeryAI credits; re-running creates new paid tasks.

## Security, secrets, and API hosts

- **`WERYAI_API_KEY`**: Treat as a secret. Only configure it if you trust this skill's source; it is listed in OpenClaw metadata as **`requires.env`** / **`primaryEnv`** so installers know it is mandatory at runtime (never commit it inside the skill package).
- **API hosts (fixed in `video_gen.js`)**: Video tasks use **`https://api.weryai.com`**; the models list uses **`https://api-growth-agent.weryai.com`**. Only **`WERYAI_API_KEY`** is read from the environment—do not rely on URL-related environment variables.
- **Local image handling disclosure**: Prefer public **`https`** image URLs. If the assembled `scripts/video_gen.js` supports local file paths, it may read a local image and upload it to WeryAI to obtain a public URL; require review / verification and explicit consent before using that path.
- **Higher assurance**: Run generation in a short-lived or isolated environment (separate account or container), and review `scripts/video_gen.js` (HTTPS submit + poll loop) before production use. Verify whether the runtime can read local image files and upload them to WeryAI, and obtain explicit consent before using that path.


## Prompt expansion (mandatory)

`video_gen.js` does **not** expand prompts. Before every `wait --json`, turn the user's short or vague brief into a **full English production `prompt`**.

**When:** The user gives only keywords, one line, or loose intent—or asks for richer video language. **Exception:** They paste a finished long prompt within the model's `prompt_length_limit` and ask you **not** to rewrite; still show the **full** text in the confirmation table.

**Always add (video language):** shot scale and angle; camera move or lock-off; light quality and motivation; subject action paced to `duration`; **one clear payoff** for this niche; state **9:16 vertical** when this skill defaults to vertical.

**Length:** Obey `prompt_length_limit` for the chosen `model_key` when this doc lists it; trim filler adjectives before removing core action, lens, or light clauses.

**Confirmation:** The pre-submit table **must** include the **full expanded `prompt`** (never a one-line summary). Wait for **confirm** or edits.

### Niche checklist

- **Outfit beat:** transition device (jump cut, spin, curtain, snap)—**look A → look B** obvious in one vertical clip.
- **Fashion read:** fabric drape, silhouette, accessories; mirror or street backdrop as user says.
- **Pacing:** sync to short vertical hook; full body or three-quarter as needed.

**`### Example prompts`** at the top of this file are **short triggers only**—always expand from the user's actual request.

## Workflow

1. Confirm the user request matches this skill's scenario (text-to-video and/or image-to-video as documented).
2. Collect the user's **brief**, optional image URL(s), tier (**best** / **good** / **fast**) or an explicit `model` key.
3. **Expand prompt (mandatory):** Unless the user supplied a finished long prompt and explicitly asked not to rewrite it, expand the brief into a full English production `prompt` using `## Prompt expansion (mandatory)` below. **Do not** call the API with only the user's minimal words.
4. Check the **expanded** `prompt` against the selected model's `prompt_length_limit` in the frozen tables in this document (when present); shorten if needed.
5. Verify `duration`, `aspect_ratio`, `resolution`, `generate_audio`, `negative_prompt`, and other fields against the frozen tables in this document and **[`WERYAI_VIDEO_API.md`](resources/WERYAI_VIDEO_API.md)**.
6. Show the pre-submit parameter table including the **full expanded `prompt`**; wait for **confirm** or edits.
7. After confirmation, run `node scripts/video_gen.js wait --json '...'` with the **expanded** prompt.
8. Parse stdout JSON and return video URLs; on failure, surface `errorCode` / `errorMessage` and suggest parameter fixes.

## CLI reference

```sh
node scripts/video_gen.js wait --json '{"model":"…","prompt":"…","duration":5,"aspect_ratio":"9:16"}'
node scripts/video_gen.js wait --json '…' --dry-run
node scripts/video_gen.js status --task-id <id>
```

**Full reference:** **[`WERYAI_VIDEO_API.md`](resources/WERYAI_VIDEO_API.md)**.

## Definition of done

Done when the user receives at least one playable video URL from the API response, or a clear failure explanation with next steps. All parameters used **must** fall within the selected model's allowed sets in this document. The submitted `prompt` **must** be the **expanded** production prompt unless the user explicitly supplied a finished long prompt and asked not to rewrite it.

## Boundaries (out of scope)

- We do not review platform compliance, copyright, or likeness; we do not warrant commercial usability of outputs.
- We do not provide offline rendering outside WeryAI, traditional NLE projects, or API field combinations not documented in this SKILL or **[`WERYAI_VIDEO_API.md`](resources/WERYAI_VIDEO_API.md)**.
- Do not link to `weryai-model-capabilities.md` or shared `../references/` paths; use **`resources/WERYAI_VIDEO_API.md`** for CLI/API details.
- Do not hard-code absolute paths in this doc; run from the skill package root (next to `SKILL.md`) so `scripts/` and `resources/` paths resolve.

### Example prompts

- `Cat, four looks, snap-cut each, vertical fashion beat`
- `From this pajama photo: one-tap cyber outfit transition`
- `Heel down + sunglasses on two accent frames, fast tempo`
- `Outfit transition montage 9:16, hard cuts on beat`

---

## Default parameters

| Field | Value |
|-------|--------|
| Model | KLING_V3_0_PRO |
| Aspect | 9:16 (fixed) |
| Duration | 5 s (`duration: 5`, tight for beat cuts) |
| Audio | Off |
| Look | Front medium shots; clear visual beat on swaps; one hero frame per look; white / solid seamless bg |

> **API validity (default `KLING_V3_0_PRO`):** Text-to-video: `duration` only **5 / 10 / 15**, `aspect_ratio` only **9:16, 1:1, 16:9**; image-to-video: `aspect_ratio` only **9:16, 16:9, 1:1**; **no `resolution` field—do not send.** Fast VEO tier: text **`VEO_3_1_FAST`**, image **`CHATBOT_VEO_3_1_FAST`**, `duration` **fixed 8**, `aspect_ratio` only **9:16** or **16:9**. For other `model_key` values, follow the allowed sets in this document and the API validity notes above; do not send unsupported fields such as `resolution`.

---

## Multi-look rapid cuts

User describes the character and number of looks / style direction; generate fast swaps on rhythm.

Collect character + direction; other params are fixed—confirm before run:

> About to generate with:
> - model: KLING_V3_0_PRO
> - aspect_ratio: 9:16
> - duration: 5
> - generate_audio: false
> - seamless loop: off (reply "loop" for loop-friendly outfit video)

Embed in the brief: one line for character and count, e.g. “kitten, five commuter looks” or “panda, ten hoodies”—visual detail per look is auto-filled.

**Expanded prompt:** Compose at generation time per `## Prompt expansion (mandatory)` from the user's actual brief—do not reuse fixed sample paragraphs.

**Parameters:**

| Field | Value |
|-------|--------|
| model | KLING_V3_0_PRO |
| aspect_ratio | 9:16 |
| duration | 5 |
| generate_audio | false |

---

## Single look: accessory detail macros

One outfit, detail beats: ring on, belt buckled, sunglasses seated, laces tied—these frames outperform full-body for shareability.

State accessories + character vibe; generate directly.

**Show all parameters in a table and wait for explicit user confirmation before submitting:**

   > 📋 **Ready to generate—please confirm:**
   >
   > | Field | This run | Notes |
   > |-------|----------|-------|
   > | `model` | `KLING_V3_0_PRO` | Best tier default; fast: text `VEO_3_1_FAST`, image `CHATBOT_VEO_3_1_FAST` (`duration` fixed 8); good → `KLING_V3_0_STA`; or specify a model name |
   > | `aspect_ratio` | `9:16` | Default KLING: 9:16, 1:1, 16:9 only; if you switch model, check that row’s `aspect_ratios` etc. |
   > | `duration` | `5s` | KLING family: 5 / 10 / 15; VEO fast: duration 8 only |
   > | `generate_audio` | `false` | Auto-generate audio or not |
   > | `prompt` | **Full expanded English prompt** (entire text for this run) | Revise before confirm |
   > | `seamless loop` | off | Reply "loop" to add seamless loop |
   >
   > Reply **"confirm"** to start, or list what to change.

**Sample prompt:**

> Extreme close-up sequence of a cat's paws accessorizing a complete outfit, series of tight macro shots cut in rhythm — first: a gold stacked ring slides onto a slender finger; then: a leather belt cinches at the waist, buckle clicking shut in slow motion; then: oversized tortoiseshell sunglasses arms unfold and settle onto the bridge of the nose, world goes slightly bronze-tinted; final shot: ankle strap heel buckled, foot placed forward, heel lifts — full look assembled, warm golden hour side light, fashion campaign energy, bokeh background throughout

---

> **Beat tip:** Use `transitions timed to invisible beat` or `single frame cut between each look` for rhythm closer to real edit beats. For five looks, add `5 complete looks in succession` so time splits across looks.
