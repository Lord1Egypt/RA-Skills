---
name: pressure-wash-video
version: 1.0.1
description: "Generate vertical satisfying pressure-wash shorts (WeryAI): text-to-video or dirty-surface image to rinse motion and a moving clean/dirty line. Use when you need pressure washing satisfying video, power-wash reveal clips, or users ask for moss blasted off pavers, wall refresh, garage grime. SEO: pressure wash video; pressure wash video generation."

tags: [satisfying, cleaning, asmr, visual-payoff, short-video, pressure-wash]

metadata: { "openclaw": { "emoji": "💦", "primaryEnv": "WERYAI_API_KEY", "paid": true, "network_required": true, "requires": { "env": ["WERYAI_API_KEY"], "bins": ["node"], "node": ">=18" } } }
user-invocable: true
---

# Pressure wash video generation

Built for cleaning / satisfying creators. The instant the jet passes, years of buildup strip away—bright surface advances along a clean/dirty frontier. That line is the retention hook. Garage floors, stone paths, carved facades: one line of text or one dirty photo, ready to post.

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

- **Striping & reveal:** grime vs clean contrast, **fan of water**, slow wipe of dirt; outdoor motivated light.
- **Surface:** concrete, deck, siding—match user; splash and mist for depth.
- **Audio:** engine/water hiss if on; satisfying **first clean streak** as peak.

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

- `Patio tiles, moss blasted into clean stripes, vertical before/after`
- `This image is a filthy garage floor—jet line advances, black mud washes away`
- `Statue / outdoor furniture, years of stain gone, slow-mo spray`
- `Pressure washing satisfying 9:16, grime removal line moving across surface`

---

## Default parameters

| Field | Value |
|-------|--------|
| Model | KLING_V3_0_PRO |
| Aspect | 9:16 (fixed, vertical short) |
| Duration | Short (`duration: 5`, minimum for KLING_V3_0_PRO) |
| Audio | On (jet + runoff ASMR is core) |
| Look | Overhead or eye-level, cool natural light, slow water advance, sharp clean/dirty line, minimal background (fixed) |

> **API validity (default `KLING_V3_0_PRO`):** Text-to-video: `duration` only **5 / 10 / 15**, `aspect_ratio` only **9:16, 1:1, 16:9**; image-to-video: `aspect_ratio` only **9:16, 16:9, 1:1**; **no `resolution` field—do not send.** Fast VEO tier: text **`VEO_3_1_FAST`**, image **`CHATBOT_VEO_3_1_FAST`**, `duration` **fixed 8**, `aspect_ratio` only **9:16** or **16:9**. For other `model_key` values, follow the allowed sets in this document and the API validity notes above; do not send unsupported fields such as `resolution`.

---

## Text-to-video: wash from description

User describes target and stain type; generate directly. Good for batch-testing materials or fast satisfying hooks.

**User provides:**
- Surface (garage floor / stone path / brick wall / carved stone / outdoor wood / roof tiles / patio steps)
- Stain (years of black grime / moss & algae / mud / oil / heavy dust)
- Optional: angle (overhead / frontal / side tracking the water line)

**Flow:**
1. Collect surface and stain; ask if missing
2. Build prompt stressing moving clean/dirty boundary, peel moment, true color return
3. After confirmation, in the terminal from the skill package root:

   ```sh
   node scripts/video_gen.js wait --json '{"model":"KLING_V3_0_PRO","prompt":"(full English prompt)","aspect_ratio":"9:16","duration":5,"generate_audio":true}'
   ```

   Replace JSON fields with confirmed values; add `resolution` only if the model supports it. Parse `videos` from stdout JSON.
4. Return URLs; note tweak directions (e.g. moss macro vs. wide overhead advance)

**Parameters:**

| Field | Value |
|-------|--------|
| model | KLING_V3_0_PRO |
| aspect_ratio | 9:16 |
| duration | 5 |
| generate_audio | true |

**Sample prompt (garage floor, years of grime):**
> Top-down overhead shot of a filthy concrete garage floor covered in years of oil and tire grime, a high-pressure water jet sweeps methodically from left to right, the clean-dirty boundary line advances with each pass revealing bright white-grey concrete beneath the black crust, dirty brown water cascades off the clean edge, slow motion 120fps captures the satisfying peel of grime, cold overcast daylight, ASMR pressure washer jet sound, tight crop no background distractions

**Sample prompt (stone path, moss):**
> Eye-level tracking shot along a moss-covered stone garden path, a pressure washer wand moves steadily forward, green and black algae blasts away in an explosive mist revealing the warm honey-toned original stone beneath, the clean-dirty frontier pushes through frame like a curtain being drawn back, 240fps slow motion water droplets backlit by soft morning light, ASMR high-pressure hiss and stone drip, shallow depth of field blurring the path ahead

**Sample prompt (brick wall, half dirty half clean):**
> Straight-on flat shot of an exterior brick wall, perfectly bisected vertically — left half coated in dark grey pollution and biological crust, right half freshly blasted to reveal vivid red-orange brickwork, a pressure washer nozzle enters frame from the right and slowly erases the dirty half millimeter by millimeter, dirty water rivulets run down the wall, flat diffused daylight makes the color contrast brutal and satisfying, locked-off camera, ASMR jet and drip sounds

**Expected outcome:** Clean/dirty line moves with the jet; peel reads clearly; original color emerges progressively; jet ASMR boosts hold time and completion.

---

## Dirty surface image → wash motion

Upload a dirty surface image; generate motion centered on that surface with pressure washing. Good for reusing photos or custom cleaning showcases.

**User provides:**
- **Image** for `image` in JSON: **public `https` URL** (best) **or** a **local path** the Node process can read (typical for OpenClaw attachments—`video_gen.js` uploads first; prefer **absolute** paths)
- Desired angle (overhead advance / frontal sweep / end-to-end push)

**Flow:**
1. Resolve `image`: valid **`https://`** remote URL **or** readable local path (not plain `http://` for remote)
2. Infer material (concrete / stone / brick / wood) and stain level; tailor wash-motion prompt
3. After confirmation:

   ```sh
   node scripts/video_gen.js wait --json '{"model":"KLING_V3_0_PRO","prompt":"(full English prompt)","image":"(user HTTPS image URL)","aspect_ratio":"9:16","duration":5,"generate_audio":true}'
   ```

   Fields match the parameter table. Parse stdout for video URLs.
4. Return URLs

**Parameters:**

| Field | Value |
|-------|--------|
| model | KLING_V3_0_PRO |
| aspect_ratio | 9:16 |
| duration | 5 |
| generate_audio | true |
| image | User image URL |

**Sample prompt (image surface, jet advance):**
> A high-pressure water jet sweeps across the dirty surface in the image from one side to the other, the powerful stream blasts away layers of grime and discoloration revealing the clean original material beneath, a sharp clean-dirty boundary line advances steadily through the frame, dirty water flows downward in rivulets, top-down or frontal perspective matching the image angle, 120fps slow motion at the boundary line, cold natural light, ASMR pressure washer impact sound

**Expected outcome:** Motion grounded in the uploaded material; direction and contrast align with stain distribution; strong true-color return.

---

## Prompt building tips

**Boundary hook:** `clean-dirty boundary line advances`, `the frontier pushes through frame`, `sharp demarcation between grime and clean`, `erases the dirty half millimeter by millimeter`

**Peel feel:** `grime blasts away in explosive mist`, `biological crust peels under pressure`, `years of buildup stripped in seconds`, `algae explodes off surface`

**Material notes:**
- Concrete / stone: `reveals bright original concrete`, `warm honey-toned stone emerges`, `brutal color contrast`
- Brick: `vivid red-orange brickwork beneath grey pollution`, `mortar lines reappear`
- Wood: `natural wood grain texture restored`, `weathered grey blasted to reveal warm timber`
- Metal / statue: `oxidation stripped away`, `original bronze patina emerges`, `details sharpen as grime lifts`

**Water visuals:** `dirty brown water cascades off edge`, `pressure mist backlit by light`, `rivulets run down the surface`, `240fps water droplets frozen mid-air`

> **Note:** Prefer public **`https`** URLs so the API can fetch references. If the assembled `scripts/video_gen.js` supports local file paths, review/verify the script and explicitly consent before local read-and-upload to WeryAI.
