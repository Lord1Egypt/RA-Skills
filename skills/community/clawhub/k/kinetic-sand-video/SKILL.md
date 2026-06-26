---
name: kinetic-sand-video
version: 1.0.0
description: "Generate vertical kinetic / magic sand satisfying shorts (WeryAI): text or sand-shape image to slice, mold release, or collapse motion. Use when you need kinetic sand ASMR, space-sand satisfying clip, or the user asks for clean slice cross-sections, mold demolding, or column collapse. SEO: kinetic sand video; kinetic sand shaping video generation."

tags: [satisfying, asmr, kinetic-sand, magic-sand, healing, kid-friendly, short-video]

metadata: { "openclaw": { "emoji": "🏖️", "primaryEnv": "WERYAI_API_KEY", "paid": true, "network_required": true, "requires": { "env": ["WERYAI_API_KEY"], "bins": ["node"], "node": ">=18" } } }
user-invocable: true
---

# Kinetic sand shaping video generation

Imagine: a blade eases into a bright yellow kinetic sand block—the cross-section opens from the center, grain friction and a perfect cut. Soft yet orderly satisfaction is what this skill is for.

Core beats:
- **Clean slice:** Sharp kerf, even color in the face, grain texture readable
- **Mold release:** Castle / star / geometry lifts out, edges crisp
- **Layered collapse:** Colored strata slip at the edge like a soft solid in slow motion
- **Streaming pour:** Sand falls evenly; pile-up feels fluffy and fine

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

- **ASMR slice:** blade entry, clean plane, **lattice cross-section**, slow pull-apart or restack.
- **Texture:** saturated layers, crisp edges, fine grain; macro top-down or 45°.
- **Payoff:** satisfying separation or collapse moment.

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

- `Rainbow kinetic sand one clean slice, neat cross-section, dense grains, vertical satisfying`
- `This image is a sandcastle: mold lifts off and the whole shape stands, motion`
- `Space sand collapse slow motion, colored layers like cake strata`
- `Kinetic sand cutting ASMR 9:16, clean slice cross-section`

---

## Default parameters

| Field | Value |
|-------|-------|
| Model | KLING_V3_0_PRO |
| Aspect ratio | 9:16 (fixed vertical) |
| Duration | Short (`duration`: 5) |
| Style | Top-down or ~45° close-up, white/light gray seamless bg, slow motion for grain texture (fixed) |
| Audio | On (grain scrape + slice are core ASMR) |

> **API validity (default `KLING_V3_0_PRO`):** Text-to-video `duration` only **5 / 10 / 15**; `aspect_ratio` only **9:16, 1:1, 16:9**. Image-to-video `aspect_ratio` only **9:16, 16:9, 1:1**. **No `resolution` field—do not send it.** For **fast** tier with VEO: text-to-video **`VEO_3_1_FAST`**, image-to-video **`CHATBOT_VEO_3_1_FAST`**, with `duration` **fixed at 8**, `aspect_ratio` only **9:16** or **16:9**. When switching `model_key`, follow the allowed sets in this section’s model/API constraints and the API validity note above; do not send `resolution` to models that do not support it.

---

## Text-to-video

User names colors / layers and action (slice / demold / collapse / pour)—skip asset hunting.

Tell me in one line: sand color or layer count, and the action.

**Generation flow:**
1. Collect palette + action; ask if missing.
2. Pick the best angle per action—slice: expose the cross-section; demold: whole shape clearing the mold; collapse: edge slippage; pour: top-down stacking.
3. If the user didn’t specify params, show this run and wait:
   > Generating with the parameters below—reply **confirm** or say what to change:
   > - model: KLING_V3_0_PRO
   > - aspect_ratio: 9:16
   > - duration: 5s
   > - generate_audio: true
   > - Loop seam: off by default (reply **loop** to append `seamless loop, perfectly looping video, first and last frame identical` to the prompt)
4. After confirmation (and optional loop keywords), run `node {baseDir}/scripts/video_gen.js wait --json '…'` (text-to-video); parse stdout.
5. Return URLs; note swaps (palette / action / loop).

**Parameter configuration:**

| Field | Value |
|-------|-------|
| model | KLING_V3_0_PRO |
| aspect_ratio | 9:16 |
| duration | 5 |
| generate_audio | true |

**Expanded prompt:** Compose at generation time per `## Prompt expansion (mandatory)` from the user's actual brief—do not reuse fixed sample paragraphs.

---

## Sand-shape image to motion

Public **HTTPS** photo of a kinetic sand shape → slice, press, or collapse starting from that look. Good for remixing assets or branded shapes.

**Generation flow:**
1. Confirm URL starts with `https://`.
2. Read shape (block / castle / free stack / mold imprint) and key colors; pick motion.
3. If unspecified, show and wait:
   > Generating with the parameters below—reply **confirm** or say what to change:
   > - model: KLING_V3_0_PRO
   > - aspect_ratio: 9:16
   > - duration: 5s
   > - generate_audio: true
   > - Loop seam: off (reply **loop** to enable)
4. Run `node {baseDir}/scripts/video_gen.js wait --json '…'` with `image`; parse stdout.
5. Return URLs.

**Parameter configuration:**

| Field | Value |
|-------|-------|
| model | KLING_V3_0_PRO |
| aspect_ratio | 9:16 |
| duration | 5 |
| generate_audio | true |
| image | User-supplied image URL |

**Expanded prompt:** Compose at generation time per `## Prompt expansion (mandatory)` from the user's actual brief—do not reuse fixed sample paragraphs.

---

## Tips

**Prompt boosts**
- Cross-section: `powdery matte cross-section`, `sharp color strata exposed`, `grain texture visible at the cut face`
- Flow: `individual grains tumble in slow motion`, `sand cascades like liquid but holds shape`, `fine particles catch the light mid-air`
- Demold: `mold lifts cleanly revealing intact geometry`, `crisp edges hold for one suspended second before softening`, `air pocket release at mold separation`
- Soft solid: `kinetic sand deforms like a soft solid`, `no bounce, zero rebound, pure absorption`

**Notes**
- More saturation and more layers strengthen the slice payoff—aim for at least three colors.
- For **loop** playback, say so before generate; loop phrases are appended to the prompt.
- Clearer, more centered reference images track the shape better in image-to-video.

> **Note:** Image URLs must be public HTTPS; private hosts or local paths will error at the API.
