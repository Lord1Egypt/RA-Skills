# Seedance 2.0 × pixcli — The Prompt Playbook

> Direction beats description. Every asset gets a job. Every second gets a plan.

Seedance 2.0 (ByteDance Doubao, routed through fal in pixcli) is a high-ceiling video model specializing in cinematic motion. It rewards deliberate direction and punishes vague description. Most of the principles here also apply to Veo 3.1, Kling o3, PixVerse v6, and LTX — but **Seedance success is almost a must** to earn the model's best output.

> **Default recommendation:** For most video tasks, native **Veo 3.1** (`-m veo-3.1`, `-m veo-3.1-fast`, or `-m veo-3.1-lite`) is the recommended starting point — it handles both T2V and I2V, supports 720p/1080p/4K, and is the default pipeline pick. Choose Seedance explicitly when you want ByteDance/Doubao cinematic motion physics.

This playbook is the source of truth for video prompting across the skill. Every `pixcli video` command should start with these rules in mind.

---

## 0. The non-negotiable mindset

- **Direct, don't describe.** You're the director, not a narrator.
- **Every asset gets a job.** If a file has no role, it's noise.
- **Every second gets a plan.** Video is time-based — treat it that way.
- **One camera move per shot. Always.** Combining causes jitter.
- **Physical verbs beat transformations.** `melt`, `fracture`, `snap open` > `becomes`.
- **Write what you want, not what you don't.** Save negatives for the `--negative` flag.

---

## 1. The core formula (memorize this)

```
Subject → Action → Environment → Camera → Style → Constraints
```

**Target: 60–100 words.** Shorter = vague. Longer = conflicting instructions that degrade coherence.

### The 6 elements

| # | Element | Rule | Good example |
|---|---------|------|--------------|
| 1 | **Subject** | Describe visual features explicitly | *A woman in her 30s, short black hair, red wool coat* |
| 2 | **Action** | Concrete verbs + quantify intensity | *walks briskly* — not *walks* |
| 3 | **Environment** | Lighting + atmosphere + time of day | *rain-slicked Tokyo street at night, neon reflections on wet pavement* |
| 4 | **Camera** | **One instruction only** — never chain moves | *slow push-in* — never *push then pan then orbit* |
| 5 | **Style** | Specific aesthetics only | *cinematic, shallow depth of field, film grain* |
| 6 | **Constraints** | What you want, not what you don't | *smooth motion, stable framing* |

### Archetypal prompt

```
A woman in her 30s, short black hair, red wool coat, walks briskly through a
rain-slicked Tokyo street at night. Neon signs reflect on wet pavement. She
glances over her shoulder. Slow push-in. Cinematic, shallow depth of field,
film grain, cool blue palette. Smooth motion, stable framing.
```

87 words. Every element present. Single camera move. Specific lighting. Subject features locked.

---

## 2. Camera movements (pick ONE per shot)

Combining moves causes jitter and motion artifacts. Always pick one and stick to it.

| Movement | Use it for | Prompt phrase |
|----------|-----------|---------------|
| Slow push-in / dolly in | Emotional focus, intimacy | `slow push-in toward her face` |
| Pull-out / dolly out | Reveal context, scale | `gradual dolly out revealing the full cityscape` |
| Pan left / right | Horizontal scanning | `slow pan right across the mountain ridge` |
| Tracking shot | Following subject | `tracking shot following the runner through the crowd` |
| Orbit / arc | Product showcase, hero moment | `smooth orbit around the subject, 90 degrees` |
| Aerial / drone | Scale, geography, epic | `aerial shot descending slowly toward the rooftop` |
| Handheld | Realism, urgency, documentary | `handheld camera, slight natural shake` |
| Fixed / locked-off | Tension, stillness, product detail | `camera holds fixed framing` |

### Separate subject motion from camera motion

- ✅ "The dancer spins. Camera holds fixed."
- ❌ "Spinning camera around a dancing person."

The first gives Seedance one thing to animate (the dancer) and one rule to hold (the camera). The second asks for two simultaneous motions and produces a dizzy, warped result.

---

## 3. Lighting — your biggest quality lever

If you add one thing to a weak prompt, add lighting. It improves every video generation model by ~30%.

| Type | Mood | Use case |
|------|------|----------|
| `golden hour` | Warm, magical, nostalgic | Lifestyle, outdoor, hero shots |
| `rim light` | Dramatic, cinematic | Portraits, action, product |
| `natural window light` | Soft, authentic, clean | Talking heads, UGC, corporate |
| `neon` | Urban, energetic, bold | Night scenes, music, fashion |
| `backlit` | Silhouette, mystery, contrast | Cinematic, artistic |
| `blue hour` | Cool, melancholic, cinematic | Outdoor transitions, drama |
| `soft diffused` | Clean, commercial, safe | Product, corporate |
| `dramatic stage lighting` | High contrast, performative | Keynote, presentation, music |

---

## 4. Timeline prompting (for 10–15s clips)

For generations of 10 seconds or more, break the scene into **3–5 time-coded beats**. More than 5 and Seedance starts losing coherence.

### Template

```
[Global style: cinematic, 4K, shallow depth of field, film grain]

[0s–3s]: Wide establishing shot — static. [Location and atmosphere.]
[3s–7s]: Medium shot — slow push-in. [Subject action.]
[7s–10s]: Close-up — fixed. [Detail or expression. Build tension.]
[10s–15s]: Wide shot — dolly out. [Resolution or reveal.]
```

### Worked example — brand story

```
[Global style: warm cinematic, shallow DOF, golden tones, documentary]

[0s–3s]: Wide shot — static. Small bakery at dawn, flour dust in morning light, empty tables.
[3s–7s]: Medium shot — slow push-in. Baker in white apron shapes dough with practiced hands.
[7s–11s]: Close-up — fixed. Hands pressing dough. Texture detail. Quiet focus.
[11s–15s]: Wide shot — slow dolly out. Full bakery revealed, warm and alive, first customers arriving.
```

Each beat obeys the 6-element formula internally. The global style line locks consistency across beats.

---

## 5. By use case

### Text-to-Video (T2V)

Full 6-element formula. This is where prompt quality matters most — there's no reference image to carry the weight.

```bash
pixcli video "A sleek titanium laptop sits open on a marble desk in a minimalist studio. Morning light streams through floor-to-ceiling windows. Camera orbits slowly around the product, 90 degrees. Clean, ultra-sharp, 4K detail, neutral warm palette. Smooth orbit, no jitter." \
  -m seedance-2-t2v \
  -d 10 \
  -r 16:9 \
  -q high \
  -o product-hero.mp4
```

### Image-to-Video (I2V)

**Only describe what changes.** The model reads the image for composition and identity — your job is to direct the motion. Include `Preserve composition and colors.` explicitly.

```bash
pixcli video "She slowly turns her head toward camera, a subtle smile forming. Eyes blink naturally. Hair moves gently in a light breeze. Camera holds fixed. Soft natural window light. Preserve composition and colors." \
  --from portrait.png \
  -m seedance-2-i2v \
  -d 5 \
  -r 9:16 \
  -q high \
  -o portrait-animated.mp4
```

### First frame → last frame (transition)

Seedance does not support start→end frame transitions. For that workflow, use `veo31-lite-transition`, `kling-o3-pro-transition`, or `pixverse-v6-transition`. Describe the motion arc **between** the two frames — don't redescribe either frame, the model sees them directly.

```bash
pixcli video "Character leaps upward with explosive energy, arms raised, reaching maximum height at the final frame. Natural motion arc. Preserve character appearance." \
  --from standing.png \
  --to jumping.png \
  -m veo31-lite-transition \
  -d 5 \
  -r 16:9 \
  -o leap.mp4
```

### Video extend

Describe **only the new section**. The duration flag is the new seconds you want added, **not** the total.

> **Note:** Seedance does not support video extension. For extension use `grok-extend-video`, `ltx-extend-video`, or `pixverse-v6-extend` (all on fal). Example:

```bash
pixcli video "Camera tilts upward as the neon sign flickers on. Steam rises from the coffee cup. The door opens. Warm street light spills into the room. Title text fades in: 'Breakfast Served / 7:00–10:00'" \
  --from scene.mp4 \
  --extend \
  -m grok-extend-video \
  -d 6 \
  -o scene-extended.mp4
```

### Avatar / talking head

Use a clean reference image for face lock. Keep the background simple and the camera fixed. Describe natural micro-expressions, not speech content.

```
The person speaks conversationally to camera. Natural micro-expressions — subtle
head tilts, eye movements, occasional blink. Slight smile. Clean modern office
background. Camera holds fixed. Warm professional lighting, shallow depth of
field. Natural short pauses between sentences.
```

---

## 6. Reference video rules

When you supply a source video via `--from`:

- **Length:** 3–8 seconds ideal. Under 2s = mushy. Over 10s = the model loses confidence in what to respect.
- **Cuts:** One continuous shot, no edits, no jump cuts.
- **Clarity:** Plain backgrounds, steady lighting, strong silhouette, deliberate pacing.
- **Compression:** Export clean H.264 at native frame rate. Avoid aggressive re-encodes.
- **One idea wide:** Either the subject moves OR the camera moves — not both.
- **Prompt less.** The clip handles motion; your text says what to keep vs. reinterpret.

Key phrases you can use to direct how the reference is consumed:

- `Respect motion from reference`
- `Keep silhouette and tempo`
- `Camera move from reference, new subject and environment`

---

## 7. Multi-input role assignment (I2V)

When using `seedance-2-i2v` with `--from`, the supplied image becomes the start frame. For additional motion direction, use your prompt text — describe only what changes relative to the image.

Key phrase to include: `Preserve composition and colors.`

For multi-image reference (e.g. face lock + environment), use a model that supports it such as `kling-o3-pro-i2v`. Seedance i2v accepts a single start-frame image.

Priority when assets conflict: **motion reference > subject consistency > mood**.

---

## 8. The 10 rules that actually matter

1. **Give every asset a job.** If a file has no role, it's noise.
2. **Write on a timeline.** `0–3s`, `3–6s`, `6–10s` beats a vague narrative blob.
3. **"Use as first frame" pins a shot. "Reference" borrows the vibe.** Know which you're asking for.
4. **One continuous take?** Say it: `one continuous take, no cuts, uninterrupted camera movement`.
5. **Prioritize assets:** motion reference > subject consistency > mood.
6. **Use physical verbs** — `melt`, `fracture`, `snap open` > `becomes` / `transforms`.
7. **Sound effects are motion cues** — heavy bass = impact, reverse suction = collapse. If you're layering audio in post, write for the sound as a motion guide.
8. **Define composition before action** — centered, diagonal, extreme close-up, wide.
9. **Transitions are actions** — describe what initiates the move, how it travels, what it resolves into. For start→end frame transitions, use `veo31-lite-transition`, `kling-o3-pro-transition`, or `pixverse-v6-transition`.
10. **One camera move per shot. Always.**

---

## 9. Negative prompts

Use `--negative` to steer away from the common artifacts Seedance produces when pressed too hard:

```bash
--negative "jitter, morphing, blurry text, warped faces, unstable framing, jump cuts, duplicate limbs, text artifacts, watermark"
```

Don't stuff the main prompt with "no jitter, no morphing" — it confuses the model. Put negatives in `--negative` where they belong.

---

## 10. pixcli Seedance model map

Seedance 2 runs on fal (backend: `fal`). Only two models exist. Routing happens automatically when you pass `-m seedance-*`, or when the prompt mentions "seedance" / "bytedance" / "doubao".

| Model ID | fal endpoint | Type | Native audio | Duration | Notes |
|----------|-------------|------|-------------|---------|-------|
| `seedance-2-t2v` | `bytedance/seedance-2.0/text-to-video` | Text → Video | `--audio` | 4–15s | Default Seedance T2V |
| `seedance-2-i2v` | `bytedance/seedance-2.0/image-to-video` | Image → Video | `--audio` | 4–15s | `--from img.png` for start frame |

Both models support `--resolution` (`480p`, `720p`, `1080p`, `4k`) and `--audio` for native audio generation.

**What Seedance does NOT support:** start→end frame transitions, video extension, multi-image/audio omni references. For transitions use `veo31-lite-transition`, `kling-o3-pro-transition`, or `pixverse-v6-transition`. For extension use `grok-extend-video`, `ltx-extend-video`, or `pixverse-v6-extend`.

### Triggering Seedance automatically (no `-m` needed)

Any of these will cause the config-driven router in `workers/config/routing.ts` to swap the classifier's pick to a Seedance model:

- The prompt literally mentions **"seedance"**, **"bytedance"**, **"byte dance"**, **"sea dance"**, or **"doubao"**

For `--quality draft` on a video task, the router picks a lower resolution (e.g. `480p`) or a budget model like `ltx-t2v` — it does **not** route to a Seedance fast tier (no such tier exists).

Otherwise the classifier picks the best fal model (Veo 3.1, Kling o3, PixVerse v6, LTX, etc.) and Seedance is bypassed.

---

## 11. Composed workflows

### Generate a first frame with pixcli, then animate it

```bash
# Step 1: generate the still — use a strong image model
pixcli image "A weathered fisherman stands at the bow of a small wooden boat, golden hour, dramatic rim light from behind, ocean stretching to the horizon, cinematic composition" \
  -m seedream-v5 -r 16:9 -q high -o fisherman.png

# Step 2: animate it — describe ONLY the motion
pixcli video "Waves rock the boat gently. His coat flutters in the wind. Seagulls cross the frame in the distance. Camera holds fixed. Preserve composition and colors." \
  --from fisherman.png -m seedance-2-i2v -d 8 -q high -o fisherman-alive.mp4
```

### Multi-step pipeline — image → video → extend

```bash
# 1. Generate the hero image
pixcli image "Product shot: matte black headphones on white marble surface, soft diffused light, minimalist, premium commercial" \
  -m imagen-4 -r 16:9 -q high -o headphones.png

# 2. Animate with a deliberate orbit
pixcli video "Camera orbits slowly around the headphones, 90 degrees. Soft particles drift in the air. Clean, ultra-sharp. Smooth orbit, no jitter." \
  --from headphones.png -m seedance-2-i2v -d 8 -q high -o headphones-orbit.mp4

# 3. Extend with a logo reveal (Seedance has no extend; use a dedicated extend model)
pixcli video "Camera pulls back. Bold centered logo text appears and pulses once. Premium black background. Typography crisp and correctly spelled." \
  --from headphones-orbit.mp4 --extend -m grok-extend-video -d 5 -o headphones-full.mp4
```

### Draft-quality iteration loop

Use `--quality draft` to render at lower resolution (480p) or route to a budget model like `ltx-t2v`. Good enough to validate composition + motion before committing to a hero render.

```bash
pixcli video "Quick test: woman walking through rain, neon reflections, slow push-in, cinematic" \
  -d 5 -q draft -o test.mp4

# Review. If happy, re-run without --quality to get full quality.
```

### Add generated audio to a Seedance clip

Both Seedance models support native audio generation via `--audio`:

```bash
pixcli video "A bartender slides a cocktail across a polished bar. Ice clinks. Amber liquid catches the neon light. Camera tracks the glass. Moody jazz club, warm tones, shallow DOF." \
  -m seedance-2-t2v -d 8 --audio -q high -o cocktail.mp4
```

---

## 12. Cheat sheet

| I want to… | Model | Key flags |
|------------|-------|-----------|
| Generate from text | `seedance-2-t2v` | `-d 10 -q high` |
| Animate a still image | `seedance-2-i2v` | `--from img.png` |
| Transition between two frames | `veo31-lite-transition` or `kling-o3-pro-transition` or `pixverse-v6-transition` | `--from start.png --to end.png` |
| Higher resolution (up to 4K) | `seedance-2-t2v` or `seedance-2-i2v` | `--resolution 1080p` or `--resolution 4k` |
| Continue an existing clip | `grok-extend-video` (fal) | `--from clip.mp4 --extend` |
| Best overall video (default) | `veo-3.1` or `veo-3.1-fast` | auto-selected by pipeline |
| Draft iteration (budget) | auto (via `--quality draft`) | `-q draft` → 480p or ltx-t2v |
| Add generated audio | `seedance-2-t2v` or `seedance-2-i2v` | `--audio` |

---

## 13. Ten-second quality audit

Before you run a Seedance video, re-read your prompt and check:

- [ ] Is there **exactly one** camera move?
- [ ] Is lighting explicit?
- [ ] Are verbs physical (`push`, `glide`, `drift`) not abstract (`transforms`, `becomes`)?
- [ ] Are 60–100 words describing **direction**, not decoration?
- [ ] If there's a reference image, does the prompt only describe what **changes**?
- [ ] If it's a long clip (10s+), is there a timeline?
- [ ] Does the prompt end with a **constraint** line (`smooth motion, stable framing`)?

If any answer is no, fix it before burning credits on a full-quality generation.

---

**See also:**
- `prompt-cookbook.md` — ready-to-paste recipes across all video models.
- `command-reference.md` — full pixcli flag reference.
- `seedance-logo-motion.md` — specialist playbook for **logo animations / brand reveals**. The pixcli API auto-detects this case (attached logo image + logo/brand+motion keywords in the prompt) and swaps in a dedicated Motion Logo Director that emits a 6-stage timeline with sound design and music. Use that file any time you're animating a logo.
