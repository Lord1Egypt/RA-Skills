---
name: hydraulic-crush-video
version: 1.0.0
description: "Generate vertical hydraulic-press crushing shorts (WeryAI): text or object image to flatten/burst motion—destruction aesthetics and material contrast for short-video feeds. Use when you need hydraulic press crushing clips, satisfying crush video, crushing ASMR, or the user asks to crush lipstick, glass marbles, or gadgets. SEO: hydraulic crush video; hydraulic press crush video generation."

tags: [satisfying, destruction, curiosity, short-video, hydraulic-press]

metadata: { "openclaw": { "emoji": "🔧", "primaryEnv": "WERYAI_API_KEY", "paid": true, "network_required": true, "requires": { "env": ["WERYAI_API_KEY"], "bins": ["node"], "node": ">=18" } } }
user-invocable: true
---

# Hydraulic press crush video generation

Built for destruction-aesthetic and satisfying creators. Lipstick smear bursts, glass marbles shattering, gadget shells tearing—one line of copy or one image → 9:16 vertical. Core hooks: material contrast, unexpected internals, tension between machine force and fragile objects.

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

- **Crush read:** compression progress, material yield (bend, burst, powder), **one peak squeeze**; object identity clear.
- **Camera:** locked macro or slow push; industrial plate framing; stylized destruction only.
- **Audio:** metal groan, pop, hiss if `generate_audio` true.

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

- `9:16 hydraulic press crushing a glass marble: slow motion and burst close-ups`
- `Use this image: lipstick crushed flat with color burst, vertical`
- `Destruction-aesthetic short: crush electronic shell, stress material tear and internal contrast`
- `Generate a vertical hydraulic press crush clip with cold lighting and macro deformation`

---

## Default parameters

| Field | Value |
|-------|-------|
| Model | KLING_V3_0_PRO |
| Aspect ratio | 9:16 (fixed vertical) |
| Duration | Short (`duration`: 5—minimum for KLING_V3_0_PRO) |
| Audio | On (press + break sounds are core satisfaction) |
| Visual style | Extreme macro, cool white light, slow motion, minimal background—deformation and detail first |

> **API validity (default `KLING_V3_0_PRO`):** Text-to-video `duration` only **5 / 10 / 15**; `aspect_ratio` only **9:16, 1:1, 16:9**. Image-to-video `aspect_ratio` only **9:16, 16:9, 1:1**. **No `resolution` field—do not send it.** For **fast** tier with VEO: text-to-video **`VEO_3_1_FAST`**, image-to-video **`CHATBOT_VEO_3_1_FAST`**, with `duration` **fixed at 8**, `aspect_ratio` only **9:16** or **16:9**. When switching `model_key`, follow the allowed sets in this section’s model/API constraints and the API validity note above; do not send `resolution` to models that do not support it.

---

## Text-to-video crush

User names the object and how it should fail—good for batch ideas, testing hooks, or quick look dev.

**The user should provide:**
- Object (lipstick, glass marble, figure, phone case, macaron, etc.)
- Optional failure mode (slow squash / instant burst / contents jet / deform-then-crack)
- Optional visual emphasis (internals, colored splash, etc.)

**Generation flow:**
1. Collect object and failure mode; ask if missing.
2. Prompt: press descent, deformation detail, material contrast, slow motion.
3. After user confirmation, run (`{baseDir}` is skill root):

   ```sh
   node {baseDir}/scripts/video_gen.js wait --json '{"model":"KLING_V3_0_PRO","prompt":"（full English prompt this run）","aspect_ratio":"9:16","duration":5,"generate_audio":true}'
   ```

   Replace JSON fields with confirmed values; add `resolution` only if the model supports it. Parse stdout `videos`.
4. Return URLs and note what to tweak next (hook angle, material, speed).

**Parameter configuration:**

| Field | Value |
|-------|-------|
| model | KLING_V3_0_PRO |
| aspect_ratio | 9:16 |
| duration | 5 |
| generate_audio | true |

**Expanded prompt:** Compose at generation time per `## Prompt expansion (mandatory)` from the user's actual brief—do not reuse fixed sample paragraphs.

**Expected outcome:** Ram enters from top, object deforms/bursts in macro, generated mechanical + material audio, strong tension and satisfaction.

---

## Image-to-video crush

Public **HTTPS** image of an object → that object crushed slowly or bursting. Reuse assets or brand-specific product shots.

**The user should provide:**
- Image URL (public `https`, not a local path)
- Desired failure (slow flatten / burst / crack spread / contents squeeze-out)

**Generation flow:**
1. Confirm URL starts with `https://` (not local).
2. Infer material; tailor deformation/break language.
3. After confirmation:

   ```sh
   node {baseDir}/scripts/video_gen.js wait --json '{"model":"KLING_V3_0_PRO","prompt":"（full English prompt）","image":"（user HTTPS image URL）","aspect_ratio":"9:16","duration":5,"generate_audio":true}'
   ```

   Match the confirmation table. Parse stdout for URLs.
4. Return URLs.

**Parameter configuration:**

| Field | Value |
|-------|-------|
| model | KLING_V3_0_PRO |
| aspect_ratio | 9:16 |
| duration | 5 |
| generate_audio | true |
| image | User-supplied image URL |

**Expanded prompt:** Compose at generation time per `## Prompt expansion (mandatory)` from the user's actual brief—do not reuse fixed sample paragraphs.

**Expected outcome:** Motion centered on the uploaded object, consistent look, readable material detail.

---

## Prompt building tips

**Pressure:** `descends with immense force`, `hydraulic ram presses down`, `irresistible mechanical pressure`, `slow inevitable crush`

**Materials:**
- Brittle (glass/ceramic): `shatters into fragments`, `hairline fractures propagate`, `crystalline shards cascade`
- Soft (lipstick/food): `deforms and smears`, `internal contents squeeze out`, `viscous material splays`
- Hard shells (electronics/toys): `casing buckles and splits`, `internal structure exposed`, `plastic fractures with resistance`

**Slow motion:** `240fps extreme slow motion`, `time dilation effect`, `every deformation frozen in detail`

**Contrast hooks:** `unexpectedly satisfying internal structure`, `reveals hidden contents`, `luxury exterior destroyed`

> **Note:** Image URLs must be publicly reachable over HTTPS or the API errors. Upload to an image host first if needed.
