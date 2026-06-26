---
name: nation-resilience-hook-video-gen
version: 1.0.0
description: "Create vertical nation-resilience hooks with timed English on-screen text (WeryAI): map flashes, resource–geography–defense beats, risk twist. Use for geopolitics Shorts, atlas montage, or country-comparison tension. Use when the user asks for map-driven hooks or collapse-vs-risk angles. SEO: geopolitics hook video; nation resilience video."

tags: [geopolitics, maps, documentary, hooks, subtitles, short-video, video-gen]

metadata: { "openclaw": { "emoji": "🗺️", "primaryEnv": "WERYAI_API_KEY", "paid": true, "network_required": true, "requires": { "env": ["WERYAI_API_KEY"], "bins": ["node"], "node": ">=18" } } }
user-invocable: true
---

# Nation resilience hook (map + flashes + risk twist)

**Template (timings assume `duration` 10; rescale proportionally for 5 or 15):** **0–2s** contrarian hook (“almost can’t collapse”); **2–8s** **three** ultra-short on-screen beats (e.g. resources / geography / defense) synced to **fast B-roll**; **8–10s** **twist** line that reframes the biggest risk (open-ended ellipsis allowed). **English subtitles are burned in** with explicit second windows—derived from the user’s **country or theme** unless they supply a final script. Default **`duration`** is **10** when unspecified.

**Dependencies:** `WERYAI_API_KEY` + Node.js 18+. **`scripts/video_gen.js`** + **[`WERYAI_VIDEO_API.md`](resources/WERYAI_VIDEO_API.md)** under **`resources/`** (assembly before run). **No other Cursor skills required.**

## Prerequisites

- `WERYAI_API_KEY` **must be set** before running `video_gen.js`.
- Node.js **18+**; prefer public **`https`** image URLs. If the assembled `scripts/video_gen.js` accepts local paths, review/verify the script and explicitly consent before local read-and-upload to WeryAI.
- `video_gen.js` **requires** a non-empty `model`—pick a tier from **Recommended models** or an explicit `model_key` from the frozen tables.
- Each `wait` run consumes credits.

## Security, secrets, and API hosts

- **`WERYAI_API_KEY`**: Secret; listed as **`requires.env`** / **`primaryEnv`**—never commit the value inside the package.
- **API hosts (fixed in `video_gen.js`)**: Video **`https://api.weryai.com`**; models registry **`https://api-growth-agent.weryai.com`**. No URL overrides documented—only the key is read from the environment.
- **Local image handling disclosure**: Prefer public **`https`** image URLs. If the assembled `scripts/video_gen.js` supports local file paths, it may read a local image and upload it to WeryAI to obtain a public URL; require review / verification and explicit consent before using that path.
- **Higher assurance**: Use a short-lived or isolated environment; review `video_gen.js` before production use. Verify whether the runtime can read local image files and upload them to WeryAI, and obtain explicit consent before using that path.

## Prompt expansion (mandatory)

`video_gen.js` does **not** expand prompts. Build a **full English production `prompt`** that **locks** this template’s timeline.

**When:** Short user input (country name, region, or metaphorical “nation” topic). **Exception:** Finished long prompt within `prompt_length_limit` + user asks not to rewrite—still show **full** text in the confirmation table.

**Always add:**

- **Duration:** Default **10** when unspecified; **5** or **15** when the user asks and the model allows.
- **Timeline scaling:** If **`duration` is 5 or 15**, **proportionally rescale** every subtitle window; keep the **same beat order** (hook → three staccato labels → twist).
- **Locked caption windows (must follow this rhythm at duration 10):**
  - **0.0–2.0s** — Hook: e.g. *THIS NATION ALMOST CAN’T COLLAPSE* (adapt to user topic).
  - **2.0–4.0s**, **4.0–6.0s**, **6.0–8.0s** — **Three** single-focus lines (user-themed): e.g. *RESOURCES* / *GEOGRAPHY* / *DEFENSE* (swap labels to match brief).
  - **8.0–10.0s** — Twist: e.g. *BUT THE REAL RISK IS…* (user fills the implied threat: debt, trust, demographics, etc.—keep **≤6 words** on screen if possible).
- **Visuals:** Animated **map**, **hard cuts**, **data glitch** overlays, **military silhouettes** / strategic geography **without** depicting real identifiable leaders as targets of hate; **sub-bass** tension if `generate_audio` is true.
- **Typography:** Bold sans, white + black outline, lower third, short fades, **no overlapping** windows; **English only** on screen unless user requests otherwise.
- **Motion:** Continuous—**no** static map shots longer than ~1s.
- **Negatives (Kling only):** illegible text, watermark, garbled captions.

**Confirmation:** Pre-submit table includes the **full expanded `prompt`**.

### Niche checklist

- Hook must feel **too bold to skip**—not a textbook opener.
- Middle three lines are **labels**, not paragraphs—match **one visual beat** each.
- Twist is **provocative but not** a call to violence or hate.

**`### Example prompts`** are richness targets only.

## Workflow

1. Confirm **text-to-video** and/or **image-to-video** (optional **multi-image** only with **`SEEDANCE_2_0`**, ≤3 URLs).
2. Collect **brief** (which country / abstract “nation” idea), optional `image`/`images`, tier or `model_key`.
3. **Expand prompt** per above—**author English lines** from the brief unless user supplied a script.
4. Validate JSON fields against frozen tables.
5. Show confirmation table + **full** expanded `prompt`; wait for **confirm**.
6. `node scripts/video_gen.js wait --json '…'`.
7. Return **`[Video](url)`** links or errors—**never** wrap playable URLs in code fences.

## CLI reference

~~~sh
node scripts/video_gen.js wait --json '{"model":"KLING_V3_0_PRO","prompt":"…","duration":10,"aspect_ratio":"9:16","generate_audio":true,"negative_prompt":"illegible text, garbled captions, watermark"}'
node scripts/video_gen.js wait --json '{"model":"SEEDANCE_2_0","prompt":"…","duration":10,"aspect_ratio":"9:16","resolution":"720p","generate_audio":true}'
~~~

**Full reference:** **[`WERYAI_VIDEO_API.md`](resources/WERYAI_VIDEO_API.md)**.

## Definition of done

Playable **[Video](url)** or clear failure. Submitted `prompt` includes **explicit second-by-second caption windows** for the full **`duration`**, matching this template’s **beat order** (scaled when `duration` is not 10), unless the user opted out with a finished prompt.

## Boundaries (out of scope)

- No guarantee of geopolitical accuracy—**entertainment / opinion** tone only; avoid incitement.
- No separate SRT workflow; captions live **inside** the model `prompt`.
- Do not use local image paths unless you have reviewed `scripts/video_gen.js` and explicitly consent to local read-and-upload to WeryAI; otherwise prefer public **`https`** URLs. Do not put secret key values in files.
- Do not link shared `../references/` capability docs; use **`resources/WERYAI_VIDEO_API.md`**.
- Do not send unsupported API fields; no `negative_prompt` on **Seedance 2.0**.
- **Multi-image** only **`SEEDANCE_2_0`**, max **3** URLs.

### Example prompts

- `Japan island supply lines—hook collapse impossible, three beats, twist: aging population`
- `Abstract “digital nation” metaphor, same beat map, twist: attention fragmentation`
- `Image: stylized map poster URL → animate with same subtitle schedule`
- `Island nation energy imports—three beats then twist on grid vulnerability`

---

## Model and API constraints (frozen for this skill)

> From `node scripts/video_gen.js models --mode text_to_video` and `--mode image_to_video` at authoring; re-run after upgrades.

### Text-to-video

| model_key | durations | aspect_ratios | resolutions | audio | negative_prompt | prompt limit |
|-----------|-----------|---------------|-------------|-------|-----------------|--------------|
| KLING_V3_0_PRO | 5, 10, 15 | 9:16, 1:1, 16:9 | *(omit `resolution`)* | yes | yes | 2000 |
| KLING_V3_0_STA | 5, 10, 15 | 9:16, 1:1, 16:9 | *(omit `resolution`)* | yes | yes | 2000 |
| SEEDANCE_2_0 | 5, 10, 15 | 9:16, 1:1, 16:9 | 480p, 720p | yes | no | 2000 |

### Image-to-video

| model_key | durations | aspect_ratios | resolutions | audio | negative_prompt | image slots |
|-----------|-----------|---------------|-------------|-------|-----------------|-------------|
| KLING_V3_0_PRO | 5, 10, 15 | 9:16, 16:9, 1:1 | *(omit)* | yes | yes | single `image` |
| KLING_V3_0_STA | 5, 10, 15 | 9:16, 16:9, 1:1 | *(omit)* | yes | yes | single `image` |
| SEEDANCE_2_0 | 5, 10, 15 | 9:16, 1:1, 16:9 | 480p, 720p | yes | no | up to **3** `images` |

## Recommended models

| Tier | model_key | Default duration |
|------|-----------|------------------|
| ⭐ Best | KLING_V3_0_PRO | 10 |
| 👍 Good | KLING_V3_0_STA | 10 |
| ⚡ Fast | SEEDANCE_2_0 | 10 (`resolution`: **720p**) |

**Tier:** unspecified → Best; “draft/quick” → Fast; “balanced” → Good.

## Default parameters

| Field | Value |
|-------|--------|
| aspect_ratio | 9:16 |
| duration | 10 |
| generate_audio | true |
| resolution | **720p** for Seedance only |
| negative_prompt | Kling: `illegible text, garbled captions, watermark, crowded subtitles` |

## Text-to-video (primary)

User gives **country / theme** + optional tone. Expand with **locked windows** → confirm table → `wait`.

## Image-to-video (optional)

Same subtitle schedule; motion **activates** map or still.

## Tips

- If the user names a **real country**, keep visuals **symbolic** (maps, icons)—avoid hostile targeting of groups.
- Twist line works best as **ellipsis** to drive comments.

> Packaged as **`nation-resilience-hook-video-gen`**.
