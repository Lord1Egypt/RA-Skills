---
name: glass-cut-video
version: 1.0.0
description: "Generate satisfying vertical short videos of glass cutting and shattering (WeryAI): text-to-video or animate a glass photo into cuts, crack spread, and break motion for Douyin/Kuaishou-style ASMR. Use when you need glass cutting video, glass shatter clip, scratch-and-crack ASMR, or users ask for clean slices, crack propagation, or glass ASMR sound."

tags: [asmr, satisfying, short-video, glass, vertical-video]

metadata: { "openclaw": { "emoji": "🪟", "primaryEnv": "WERYAI_API_KEY", "paid": true, "network_required": true, "requires": { "env": ["WERYAI_API_KEY"], "bins": ["node"], "node": ">=18" } } }
user-invocable: true
---

# Glass cutting & shatter videos

Built for satisfying-content creators. Whether it’s the perfection of a straight cut, the rush of tempered glass exploding, or stained glass glowing in the light—you can go from one line of text or one image to a ready-to-post **9:16** clip.

**Dependencies:** `scripts/video_gen.js` in this folder + `WERYAI_API_KEY` in the environment + Node.js 18+. No other Cursor skills required.

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

- **Glass grammar:** score line, crack propagation, snap, shards, tempered burst, or stained-glass glow—pick one clear beat.
- **Macro & light:** caustics, speculars, transmitted color; **ASMR** glass tone if audio on.
- **Safety tone:** stylized satisfying break, not real injury context.

**`### Example prompts`** at the top of this file are **short triggers only**—always expand from the user's actual request.

## Workflow

1. Confirm the request matches this skill (text-to-video and/or image-to-video as documented).
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

Done when the user receives at least one playable video URL from the API response, or a clear failure explanation with next steps. All parameters used **must** fall within the selected model’s allowed sets in this document. The submitted `prompt` **must** be the **expanded** production prompt unless the user explicitly supplied a finished long prompt and asked not to rewrite it.

## Boundaries (out of scope)

- We do not review platform compliance, copyright, or likeness; we do not warrant commercial usability of outputs.
- We do not provide offline rendering, traditional NLE projects, or API field combinations not documented here.
- Do not hard-code absolute paths in this doc; `{baseDir}` is this skill root (next to `SKILL.md`).

### Example prompts

- `Vertical clip: cutting thick glass, satisfying sound, crack spreading from one point`
- `This image is a windowpane—animate a blade scratch and cracks growing in the reflection`
- `Satisfying glass ASMR 9:16, clean slice, translucent look, not gory`
- `Glass cutting ASMR 9:16, slow crack propagation, clean slice reveal`

---

## Default parameters

| Field | Value |
|-------|--------|
| Model | KLING_V3_0_PRO |
| Aspect | 9:16 (fixed, vertical short video) |
| Duration | 5 s |
| Resolution | — (`KLING_V3_0_PRO` has no `resolution` field—do not send) |
| Audio | On (auto glass cut / shatter sounds) |
| Look | Extreme macro, cold white light, slow motion, minimal background, translucency first |

> **API validity (default `KLING_V3_0_PRO`):** Text-to-video: `duration` only **5 / 10 / 15**, `aspect_ratio` only **9:16, 1:1, 16:9**; image-to-video: `aspect_ratio` only **9:16, 16:9, 1:1**; **no `resolution` field—do not send.** Fast VEO tier: text **`VEO_3_1_FAST`**, image **`CHATBOT_VEO_3_1_FAST`**, `duration` **fixed 8**, `aspect_ratio` only **9:16** or **16:9**. For other `model_key` values, follow the allowed sets in this document; do not send unsupported fields.

---

## Text-to-video: cutting glass

The user describes glass type and how it breaks; you generate the clip. Good for batch ideation and hook testing.

**User should provide:**

- Glass type (clear / stained / tempered / frosted / laminated)
- Cut or break style (straight score-and-snap / irregular cut / slow shatter / full burst / crack spread)
- Optional: angle or detail (“shards fly”, “side light on refraction”)

**Flow:**

1. Collect glass type and break style; ask if missing.
2. Build an English prompt emphasizing cut marks, refraction, and break motion.
3. After confirmation, run (`{baseDir}` = this skill root):

   ```sh
   node {baseDir}/scripts/video_gen.js wait --json '{"model":"KLING_V3_0_PRO","prompt":"(full English prompt)","aspect_ratio":"9:16","duration":5,"generate_audio":true}'
   ```

   Match JSON to the confirmed table; add `resolution` only if the model supports it. Parse `videos` from stdout.
4. Return URLs and what to tweak next.

**Parameters:**

| Field | Value |
|-------|--------|
| model | KLING_V3_0_PRO |
| aspect_ratio | 9:16 |
| duration | 5 |
| generate_audio | true |

**Sample prompt (stained glass straight cut):**
> Extreme close-up macro shot of vibrant stained glass being scored and snapped cleanly along a straight line, cold white backlighting makes colors saturate brilliantly, the crack propagates with satisfying precision, glass edge perfectly smooth, slow motion 240fps, dust motes caught in light beam, ASMR cutting sound, minimal white background, shallow depth of field

**Sample prompt (tempered shatter):**
> Ultra close-up of tempered glass shattering into thousands of tiny cubed fragments in extreme slow motion, cold studio lighting catches every spinning shard, crystalline transparency, satisfying explosive burst contained in frame, glass pebbles cascade like water, cinematic depth of field, ASMR crunch and tinkle

**Expected result:** 5 s vertical clip with coherent cut/shatter motion, readable glass texture and light, synced break sounds, high completion rate.

---

## Image-to-video: glass motion

User supplies a glass image URL; you add crack spread or cut motion on top of that look.

**User should provide:**

- Image URL (public `https` only)
- Desired motion (crack from center / blade scratch clean line / slow full break / edge chip)

**Flow:**

1. Validate `https://` URL (not a local path).
2. Build motion prompt anchored to the image’s glass material.
3. After confirmation:

   ```sh
   node {baseDir}/scripts/video_gen.js wait --json '{"model":"KLING_V3_0_PRO","prompt":"(full English prompt)","image":"(user HTTPS URL)","aspect_ratio":"9:16","duration":5,"generate_audio":true}'
   ```

4. Return URLs.

**Parameters:**

| Field | Value |
|-------|--------|
| model | KLING_V3_0_PRO |
| aspect_ratio | 9:16 |
| duration | 5 |
| generate_audio | true |
| image | User’s image URL |

**Sample prompt (crack spread):**
> The glass surface in the image begins to crack, a single hairline fracture propagates outward in extreme slow motion, branching into a web of perfect cracks, cold white light refracts through each fracture line creating rainbow caustics, satisfying tension-release moment, ASMR glass stress sound

**Expected result:** Motion matches the uploaded glass; strong refraction; consistent with the source image.

---

## Prompt building blocks

**Brittle snap:** `satisfying snap`, `perfect clean break`, `zero resistance`, `ultra-brittle`

**Clean edge:** `laser-precise cut line`, `mirror-smooth edge`, `factory perfect`, `atomic-level clean slice`

**Clarity:** `crystal clear transparency`, `light refracts into spectrum`, `backlit caustics`, `liquid-like clarity`

**Safe tension:** `controlled shatter`, `contained explosion`, `safe distance macro`, `slow motion danger`

**Slow-mo:** `240fps extreme slow motion`, `time dilation effect`, `every shard frozen mid-air`

> **Note:** Image URLs must be publicly reachable over HTTPS or the API will fail. Upload to a host first if needed.
