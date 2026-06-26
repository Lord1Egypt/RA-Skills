---
name: one-detail-reads-person-video-gen
version: 1.0.0
description: "Create vertical social-read shorts: one-cue thesis, example beat, playful closer, timed English captions (WeryAI). Use for psychology hooks, micro-behavior reads, or respectful debate-bait. Use when the user asks to judge someone from one signal. SEO: read people cue video; social psychology video."

tags: [psychology, social, behavior, hooks, subtitles, short-video, video-gen]

metadata: { "openclaw": { "emoji": "🎭", "primaryEnv": "WERYAI_API_KEY", "paid": true, "network_required": true, "requires": { "env": ["WERYAI_API_KEY"], "bins": ["node"], "node": ">=18" } } }
user-invocable: true
---

# One detail reads a person (cue → example → debate line)

**Template (timings assume `duration` 10; rescale for 5 or 15):** **0–3s** *you can read someone by ONE cue*; **3–8s** **one concrete example** (user-chosen: e.g. how they treat service staff, how they handle a small promise, phone posture at dinner—**no** real non-public figures); **8–10s** **provocative summary** that invites disagreement (e.g. *THAT’S THE TELL—FIGHT ME* toned **playfully**, not harassment). **English subtitles** with **explicit timing**. Default **`duration`** is **10** when unspecified.

**Dependencies:** `WERYAI_API_KEY` + Node.js 18+. **`scripts/video_gen.js`** + **[`WERYAI_VIDEO_API.md`](resources/WERYAI_VIDEO_API.md)**. **No other Cursor skills required.**

## Prerequisites

- `WERYAI_API_KEY` **must be set**; Node **18+**. Prefer public **`https`** image URLs; if the assembled `scripts/video_gen.js` supports local file paths, review/verify the script and explicitly consent before local read-and-upload to WeryAI.
- Non-empty `model`.

## Security, secrets, and API hosts

- **`WERYAI_API_KEY`**: Secret; **`requires.env`** / **`primaryEnv`**.
- **API hosts** fixed in `video_gen.js`; no URL env overrides.
- **Local image handling disclosure**: Prefer public **`https`** image URLs. If the assembled `scripts/video_gen.js` supports local file paths, it may read a local image and upload it to WeryAI to obtain a public URL; require review / verification and explicit consent before using that path.
- **Higher assurance**: Prefer a short-lived or isolated environment; review `scripts/video_gen.js` before production use. Verify whether the runtime can read local image files and upload them to WeryAI, and obtain explicit consent before using that path.

## Prompt expansion (mandatory)

- **Duration:** Default **10**; **5** or **15** when allowed and requested.
- **Timeline scaling:** Rescale **0–3 / 3–8 / 8–10** proportionally; keep **thesis → example → closer** order.

**Locked rhythm (example for duration 10):**

- **0.0–3.0s** — Thesis: e.g. *ONE DETAIL EXPOSES THEIR LEVEL*.
- **3.0–8.0s** — Example beat (split into **two** on-screen lines if needed, e.g. **3–5.5** and **5.5–8.0**) describing **generic silhouettes**, not identifiable people.
- **8.0–10.0s** — Closer: **strong opinion**, **playful fight-me** energy—**no** slurs, **no** targeting protected groups.

**Visuals:** Close-ups **hands, eyes, cafe table, door holds**; shallow DOF; **constant** micro-motion.

**Typography:** Bold sans, outline, lower third; **English** on screen.

**Negatives (Kling):** illegible text, watermark.

**Confirmation:** Full `prompt` in table.

### Niche checklist

- **Example** must be **filmable in B-roll**, not a lecture.
- Avoid **diagnosing** real individuals or mental illness.

## Workflow

1. Text / image / multi-image (**SEEDANCE_2_0**, ≤3).
2. Collect **which cue** the user cares about.
3. Expand → validate → confirm → `wait`.
4. **`[Video](url)`** for results.

## CLI reference

~~~sh
node scripts/video_gen.js wait --json '{"model":"KLING_V3_0_PRO","prompt":"…","duration":10,"aspect_ratio":"9:16","generate_audio":true,"negative_prompt":"illegible text, watermark"}'
node scripts/video_gen.js wait --json '{"model":"SEEDANCE_2_0","prompt":"…","duration":10,"aspect_ratio":"9:16","resolution":"720p","generate_audio":true}'
~~~

**Full reference:** **[`WERYAI_VIDEO_API.md`](resources/WERYAI_VIDEO_API.md)**.

## Definition of done

**[Video](url)** or error; timed **English** captions follow **thesis / example / closer** structure with **ranges scaled to `duration`** (or user-approved split).

## Boundaries (out of scope)

- **No** harassment, hate, or doxxing framing.
- Not professional psychology advice.
- Captions via **prompt** only; CLI details in **`resources/WERYAI_VIDEO_API.md`**.
- **Multi-image** only **SEEDANCE_2_0**, max **3**.

### Example prompts

- `Cue: how they treat waiters—cafe B-roll, playful closer`
- `Cue: punctuality on small promises—office hands clock`
- `Image: anonymous crowd silhouette URL → same beat structure`
- `Cue: how they apologize after a mistake—cafe reenactment, playful closer`

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
| negative_prompt | Kling: `illegible text, garbled captions, watermark` |

## Text-to-video (primary)

Collect **cue** → map to **three windows** → confirm → `wait`.

## Image-to-video (optional)

Reference still → emotional read with same structure.

## Tips

- Closer works when it’s **obviously rhetorical**, not cruel.
- **Translate** user Chinese brief to **English** captions unless they specify another on-screen language.

> Packaged as **`one-detail-reads-person-video-gen`**.
