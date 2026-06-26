---
name: if-you-vanished-video-gen
version: 1.0.1
description: "Create vertical absence shorts: quiet home, stalled phone, feed moves on, bittersweet closer, timed English captions (WeryAI). Use for melancholic mood or safe disappearance hypotheticals—never self-harm. Use when the user wants lonely-apartment or ‘if I vanished’ vibes. SEO: if you vanished video; loneliness hook video."

tags: [emotion, loneliness, absence, mood, hooks, subtitles, short-video, video-gen]

metadata: { "openclaw": { "emoji": "🌙", "primaryEnv": "WERYAI_API_KEY", "paid": true, "network_required": true, "requires": { "env": ["WERYAI_API_KEY"], "bins": ["node"], "node": ">=18" } } }
user-invocable: true
---

# If you vanished today (quiet home → feed moves on)

**Template (assume `duration` 10 unless scaled):** **0–2s** *ten minutes after you vanish*; **2–8s** **three beats**—e.g. **2–4** *HOME GOES QUIET*, **4–6** *PHONE STOPS FOR YOU*, **6–8** *THE FEED MOVES ON* (user may rename beats); **8–10s** *NOBODY NOTICES… YET* (or user’s **softer** variant). **English subtitles** with **explicit windows**. Tone: **melancholic**, **not** self-harm instruction. Default **`duration`** is **10** when unspecified.

**Dependencies:** `WERYAI_API_KEY` + Node.js 18+. **`{baseDir}/scripts/video_gen.js`** + **[`WERYAI_VIDEO_API.md`](resources/WERYAI_VIDEO_API.md)**. **No other Cursor skills required.**

## Prerequisites

- `WERYAI_API_KEY` **must be set**; Node **18+**; `https` images only.
- Non-empty `model`.

## Security, secrets, and API hosts

- **`WERYAI_API_KEY`**: Secret; **`requires.env`** / **`primaryEnv`**.
- **API hosts** fixed in `video_gen.js`.

## Prompt expansion (mandatory)

- **Duration:** Default **10**; **5** or **15** when allowed and requested.
- **Timeline scaling:** Rescale **0–2 / 2–8 / 8–10** (and internal 2–4 / 4–6 / 6–8) proportionally; keep **setup → three middle beats → closer** order.

**Visuals:** Empty hallway, **unmade bed**, **notifications piling** then **silence**, **faceless feed scroll**, **city bokeh**; **slow dolly** but **reframe** often so motion never dies.

**Typography:** Soft white, subtle outline, lower third; **English** on screen.

**Audio:** Sparse piano / room tone if `generate_audio` true—**no** jump-scare horror.

**Safety:** **Do not** depict self-harm, suicide methods, or graphic violence. **Absence** is **implied**.

**Negatives (Kling):** illegible text, watermark, horror gore.

**Confirmation:** Full expanded `prompt`.

### Niche checklist

- **Empathy** over **nihilism**—user can request **hope tag** in last line (optional).

## Workflow

1. Text / image / multi-image (**SEEDANCE_2_0**, ≤3).
2. Collect **tone** (default bittersweet) and optional **last-line tweak**.
3. Expand → validate → confirm → `wait`.
4. **`[Video](url)`**.

## CLI reference

~~~sh
node {baseDir}/scripts/video_gen.js wait --json '{"model":"KLING_V3_0_PRO","prompt":"…","duration":10,"aspect_ratio":"9:16","generate_audio":true,"negative_prompt":"illegible text, watermark, gore, self-harm"}'
node {baseDir}/scripts/video_gen.js wait --json '{"model":"SEEDANCE_2_0","prompt":"…","duration":10,"aspect_ratio":"9:16","resolution":"720p","generate_audio":true}'
~~~

**Full reference:** **[`WERYAI_VIDEO_API.md`](resources/WERYAI_VIDEO_API.md)**.

## Definition of done

**[Video](url)** or error; **non-overlapping second ranges** for setup, three middle beats, and closer—**scaled to `duration`**—in `prompt`.

## Boundaries (out of scope)

- **No** self-harm / suicide method content; if user asks, **refuse** and offer **safer** emotional framing.
- Not therapy; **creative short** only.
- **`resources/WERYAI_VIDEO_API.md`** for CLI; no `negative_prompt` on Seedance.
- **Multi-image** only **SEEDANCE_2_0**, max **3**.

### Example prompts

- `Default absence arc, rainy city ending`
- `Warmer variant: last line ‘but someone would notice tomorrow’`
- `Apartment photo URL → slow push with same caption schedule`
- `Softer ending: ‘someone would notice tomorrow’ instead of pure nihilism`

---

## Model and API constraints (frozen for this skill)

### Text-to-video

| model_key | durations | aspect_ratios | resolutions | audio | negative_prompt | prompt limit |
|-----------|-----------|---------------|-------------|-------|-----------------|--------------|
| KLING_V3_0_PRO | 5, 10, 15 | 9:16, 1:1, 16:9 | *(omit)* | yes | yes | 2000 |
| KLING_V3_0_STA | 5, 10, 15 | 9:16, 1:1, 16:9 | *(omit)* | yes | yes | 2000 |
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

## Default parameters

| Field | Value |
|-------|--------|
| aspect_ratio | 9:16 |
| duration | 10 |
| generate_audio | true |
| resolution | 720p (Seedance) |
| negative_prompt | Kling: `illegible text, watermark, gore, self-harm, horror` |

## Text-to-video (primary)

Confirm **safe tone** → expand **five-window** captions → `wait`.

## Image-to-video (optional)

Room still → **lonely** motion + same structure.

## Tips

- **Translate** Chinese briefs to **English** on-screen unless user wants another language.
- If the user is vulnerable, **prefer** hopeful last-line variants.

> Packaged as **`if-you-vanished-video-gen`**.
