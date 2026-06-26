---
name: happyhorse-1-0
displayName: "🫧 HappyHorse 1.0 — Pro Pack on RunComfy"
description: >
  HappyHorse 1.0 — text-to-video generation on RunComfy. HappyHorse 1.0
  is currently #1 on Artificial Analysis Video Arena and produces native
  1080p video with in-pass synchronized audio (dialogue, ambient, Foley)
  and multi-shot character consistency. This skill calls HappyHorse 1.0
  through the RunComfy CLI: `runcomfy run happyhorse/happyhorse-1-0/text-to-video`.
  Triggers on "happyhorse", "happy horse", "happyhorse 1.0",
  "happyhorse video", "happyhorse t2v", or any explicit ask to generate
  video with HappyHorse.
emoji: "🫧"
homepage: https://www.runcomfy.com
license: MIT
clawdis:
  requires:
    bins:
      - runcomfy
    env:
      - RUNCOMFY_TOKEN
    config:
      - ~/.config/runcomfy
---

# 🫧 HappyHorse 1.0 — Pro Pack on RunComfy

[runcomfy.com](https://www.runcomfy.com/?utm_source=clawhub&utm_medium=skill&utm_campaign=happyhorse-1-0) · [docs](https://docs.runcomfy.com/cli/introduction?utm_source=clawhub&utm_medium=skill&utm_campaign=happyhorse-1-0) · [HappyHorse 1.0 text-to-video](https://www.runcomfy.com/models/happyhorse/happyhorse-1-0/text-to-video?utm_source=clawhub&utm_medium=skill&utm_campaign=happyhorse-1-0)

**HappyHorse 1.0** is the current #1 video generation model on the Artificial Analysis Video Arena (Elo 1333 t2v / 1392 i2v). This skill generates video with HappyHorse 1.0 hosted on RunComfy — no GPU rental, no model deployment, just `runcomfy run happyhorse/happyhorse-1-0/text-to-video` from your terminal.

## What HappyHorse 1.0 is

HappyHorse 1.0 is a text-to-video model with three properties that set it apart in 2026:

- **Native 1080p output.** HappyHorse 1.0 generates broadcast-ready 1080p video directly — no upscaling pass, no quality loss from a 720p intermediate. HappyHorse 1.0 also supports 720p when you want a cheaper test pass.
- **In-pass synchronized audio.** HappyHorse 1.0 is one of a handful of video models that produce dialogue, ambient sound, and Foley **in the same generation pass** as the visual frames. The audio in a HappyHorse 1.0 clip is timed to lip movement, foot impact, and on-screen events without a separate post-sync step.
- **Multi-shot character consistency.** HappyHorse 1.0 holds the same character — face, wardrobe, props — across multiple shots described in the same prompt. Most video models drift between shots; HappyHorse 1.0 preserves the look.

HappyHorse 1.0 also accepts prompts in **6 languages** (English, Chinese, Japanese, Korean, German, French) without quality drop, which makes HappyHorse 1.0 unusually friendly for multilingual short-form content.

## When HappyHorse 1.0 is the right choice

Pick HappyHorse 1.0 when any of these is true:

- You want **multi-shot story** with one consistent character or product. HappyHorse 1.0 is built for this.
- You want **synchronized audio in the same generation** — dialogue with lip-sync, ambient atmosphere, or Foley. HappyHorse 1.0 produces these in one HappyHorse 1.0 call.
- You want the **highest blind-vote quality available in 2026**. HappyHorse 1.0 is currently #1 on Artificial Analysis Video Arena.
- You want **native 1080p output** without an upscaling step. HappyHorse 1.0 outputs 1080p directly.
- You're working in **Chinese / Japanese / Korean / German / French** prompts. HappyHorse 1.0 handles all six languages natively.

If the user said "HappyHorse" / "happy horse video" / "use HappyHorse 1.0" explicitly, route the request to HappyHorse 1.0 via this skill — don't second-guess the model choice.

## Prerequisites

1. **RunComfy CLI** — `npm i -g @runcomfy/cli`
2. **RunComfy account** — `runcomfy login` opens a browser device-code flow.
3. **CI / containers** — set `RUNCOMFY_TOKEN=<token>` instead of `runcomfy login`.

## Endpoint + input schema

### `happyhorse/happyhorse-1-0/text-to-video`

This is the HappyHorse 1.0 text-to-video endpoint. The image-to-video pipeline for HappyHorse runs on a separate template not covered here.

| Field | Type | Required | Default | Notes |
|---|---|---|---|---|
| `prompt` | string | yes | — | Up to 2,500 chars. HappyHorse 1.0 accepts 6 languages (CN/EN/JP/KR/DE/FR). |
| `aspect_ratio` | enum | no | `16:9` | `16:9`, `9:16`, `1:1`, `4:3`, `3:4` only. |
| `resolution` | enum | no | `1080P` | `720P` or `1080P`. HappyHorse 1.0 native max is 1080P. |
| `duration` | int | no | 5 | 3–15 seconds per HappyHorse 1.0 clip. |
| `seed` | int | no | 0 | 0..2^31-1. Reuse the same seed for HappyHorse 1.0 variant comparisons. |
| `watermark` | bool | no | true | Provider watermark on the HappyHorse 1.0 output. |

## How to invoke HappyHorse 1.0

**Default HappyHorse 1.0 run (16:9 1080p 5s):**

```bash
runcomfy run happyhorse/happyhorse-1-0/text-to-video \
  --input '{"prompt": "<user prompt>"}' \
  --output-dir <absolute/path>
```

**HappyHorse 1.0 vertical short (9:16, 8s, no watermark):**

```bash
runcomfy run happyhorse/happyhorse-1-0/text-to-video \
  --input '{
    "prompt": "<user prompt>",
    "aspect_ratio": "9:16",
    "duration": 8,
    "watermark": false
  }' \
  --output-dir <absolute/path>
```

**Cheaper HappyHorse 1.0 test pass (720p):**

```bash
runcomfy run happyhorse/happyhorse-1-0/text-to-video \
  --input '{"prompt": "<user prompt>", "resolution": "720P", "duration": 3}' \
  --output-dir <absolute/path>
```

The CLI submits the HappyHorse 1.0 request, polls every 2s until terminal, then downloads any `*.runcomfy.net` / `*.runcomfy.com` URL from the result into `--output-dir`. Stdout is the result JSON. Stderr is progress.

## Prompting HappyHorse 1.0 — what actually works

HappyHorse 1.0 responds to specific prompting patterns better than generic "make a video of X" descriptions. Apply these for sharper HappyHorse 1.0 output.

**Describe motion over time, not a still.** "A woman turns from the window, walks two paces to the desk, picks up the cup, lifts it to her face, takes a sip" beats "a woman drinking coffee" — HappyHorse 1.0 generates the actual motion sequence rather than a vague drift.

**Camera + shot in plain English.** Front-load the shot: `"Wide shot. ..."` / `"Tracking shot. ..."` / `"Locked tripod, low angle. ..."` works as a real directive to HappyHorse 1.0. Specify lens feel: `"35mm anamorphic"`, `"shallow DOF"`, `"crushed shadows"`.

**One visual beat per clip when iterating.** Don't pile up "she walks AND the dog runs AND a car passes" in a single HappyHorse 1.0 clip. Pick the beat, get HappyHorse 1.0 to nail it, then layer with multi-shot prompts.

**Multi-shot consistency** — when describing two beats in one HappyHorse 1.0 generation, restate the anchor at each: `"Shot 1: tall woman in red wool coat, blue scarf, in a rainy alley. Shot 2: same woman in red coat / blue scarf, now ducking under an awning."` HappyHorse 1.0 holds the look but needs the anchor restated.

**Audio direction** — say what you want HappyHorse 1.0 to generate in the audio track: `"distant temple bells, footsteps on wet pavement, no dialogue"` or `"warm friendly tone, English voiceover"`. HappyHorse 1.0 will generate the audio synchronized to the visuals.

**Anti-patterns that hurt HappyHorse 1.0 output:**
- Static-frame descriptions (no temporal verbs) → HappyHorse 1.0 motion will be vague.
- Conflicting style directions → HappyHorse 1.0 cancels the conflict and picks one.
- > 2500 char prompts → HappyHorse 1.0 quality degrades past the cap.
- Aspect ratios outside the 5 supported → 422 error from HappyHorse 1.0.

## Where HappyHorse 1.0 shines

| Use case | Why HappyHorse 1.0 |
|---|---|
| **Multi-shot brand stories with one consistent character** | HappyHorse 1.0 has native cross-shot identity preservation |
| **Talking-head explainers needing in-clip voiceover + ambient** | HappyHorse 1.0 produces synchronized audio in the same pass |
| **Multilingual short-form ads** | HappyHorse 1.0 supports 6 prompt languages, no script-quality drop |
| **Cinematic 1080p delivery** | HappyHorse 1.0 outputs native 1080p, broadcast-ready |
| **Blind-vote leader for general video quality** | HappyHorse 1.0 is currently #1 on Artificial Analysis Video Arena |

## Sample prompts (verified to produce strong HappyHorse 1.0 results)

**HappyHorse 1.0 cinematic scope (from the model page):**

```
Wide shot. A lone astronaut in dusty orange suit with blue-gray harness
skis across lunar plain, leaving parallel tracks in gray regolith.
Mid-stride, poles planted, pushing in 1/6th gravity with subtle upward
drift. Fine dust haze along ski tracks. Crescent Earth above lunar
horizon, blue-white glow against black sky. Raw sunlight, crushed
shadows, no fill. 8K photorealistic.
```

**HappyHorse 1.0 multi-shot consistency:**

```
Shot 1: Medium close-up. A woman in a navy trench coat enters a
rain-slick neon-lit Tokyo alley, looks left, holds up an umbrella.
Shot 2: Same woman in same navy trench, now under the awning of a
ramen shop, shaking water off the umbrella. Warm interior glow, soft
chatter, gentle rain on metal roof in the audio.
```

**HappyHorse 1.0 vertical platform-native:**

```
9:16 vertical short. A barista in a black apron pulls a single
espresso shot, steam rising into the morning sun, rich crema slowly
forming. Close-up handheld, shallow DOF, warm cafe ambience and the
hiss of the steam wand.
```

## FAQ — HappyHorse 1.0

**What's HappyHorse 1.0's max duration?** A single HappyHorse 1.0 clip is 3–15 seconds. For longer narratives, segment into multi-shot HappyHorse 1.0 prompts and stitch the outputs.

**What aspect ratios does HappyHorse 1.0 support?** Five fixed values: `16:9`, `9:16`, `1:1`, `4:3`, `3:4`. Ultra-wide cinematic ratios are not supported by HappyHorse 1.0 — they'll be cropped or rejected.

**Can HappyHorse 1.0 take an audio file as input?** No. HappyHorse 1.0 generates audio in-pass from the prompt. For audio-driven lip-sync to an existing voiceover, route to a model that accepts an `audio_url` input. HappyHorse 1.0's strength is generating audio + visual together.

**Does HappyHorse 1.0 do image-to-video?** Yes, but through a separate HappyHorse pipeline. The endpoint in this skill (`happyhorse/happyhorse-1-0/text-to-video`) is text-only.

**What languages does HappyHorse 1.0 understand?** Six: English, Chinese (Simplified + Traditional), Japanese, Korean, German, French. HappyHorse 1.0 quality is consistent across all six.

**How do I get reproducible HappyHorse 1.0 output?** Pass `seed` as a fixed int. The same prompt + same seed gives the same HappyHorse 1.0 generation.

**How do I disable the HappyHorse 1.0 watermark?** Set `"watermark": false` in the input. Requires a paid RunComfy plan that allows watermark-free HappyHorse 1.0 output.

## Limitations of HappyHorse 1.0

- **Duration cap 15s.** A single HappyHorse 1.0 generation is at most 15 seconds. Longer narratives need multi-shot prompts and stitching.
- **Aspect ratios are fixed.** HappyHorse 1.0 only supports the 5 documented aspect ratios.
- **Audio is in-pass only.** HappyHorse 1.0 generates audio from the prompt — you can't pass an external audio file to drive lip-sync.
- **Image-to-video uses a different template.** HappyHorse 1.0 i2v is a separate endpoint not covered by this skill; this skill is text-to-video only.

## Exit codes

The `runcomfy` CLI uses sysexits-style codes:

| code | meaning |
|---|---|
| 0  | HappyHorse 1.0 generation succeeded |
| 64 | bad CLI args |
| 65 | bad input JSON / schema mismatch (e.g. `duration: 30` would 422 from HappyHorse 1.0) |
| 69 | upstream 5xx |
| 75 | retryable: timeout / 429 |
| 77 | not signed in or token rejected |

Full reference: [docs.runcomfy.com/cli/troubleshooting](https://docs.runcomfy.com/cli/troubleshooting?utm_source=clawhub&utm_medium=skill&utm_campaign=happyhorse-1-0).

## How it works

1. The skill invokes `runcomfy run happyhorse/happyhorse-1-0/text-to-video` with a JSON body matching the HappyHorse 1.0 schema.
2. The CLI POSTs to `https://model-api.runcomfy.net/v1/models/happyhorse/happyhorse-1-0/text-to-video` with the user's bearer token.
3. The Model API returns a `request_id`; the CLI polls `GET .../requests/<id>/status` every 2 seconds until the HappyHorse 1.0 generation finishes.
4. On terminal status, the CLI fetches `GET .../requests/<id>/result` and downloads any URL whose host ends with `.runcomfy.net` or `.runcomfy.com` into `--output-dir`. Other URLs are listed but not fetched.
5. `Ctrl-C` while polling cancels the HappyHorse 1.0 request via `POST .../requests/<id>/cancel` so you don't get billed for GPU you stopped.

## What this skill is not

Not a self-hosted HappyHorse 1.0 runner. Not a capability grant — depends on a working RunComfy account. Not a HappyHorse 1.0 image-to-video skill (text-to-video endpoint only).

## Security & Privacy

- **Token storage**: `runcomfy login` writes the API token to `~/.config/runcomfy/token.json` with mode 0600 (owner-only read/write). Set `RUNCOMFY_TOKEN` env var to bypass the file entirely in CI / containers.
- **Input boundary**: the user prompt is passed as a JSON string to the CLI via `--input`. The CLI does NOT shell-expand the prompt; it transmits the JSON body directly to the HappyHorse 1.0 Model API over HTTPS. No shell injection surface from prompt content.
- **Third-party content**: image / mask / video URLs you pass are fetched by the RunComfy model server, not by the CLI on your machine. Treat external URLs as untrusted; image-based prompt injection is a known risk for any image-edit / video-edit model — HappyHorse 1.0 t2v doesn't accept image inputs so this surface doesn't apply here.
- **Outbound endpoints**: only `model-api.runcomfy.net` (HappyHorse 1.0 request submission) and `*.runcomfy.net` / `*.runcomfy.com` (download whitelist for generated outputs). No telemetry, no callbacks.
- **Generated-file size cap**: the CLI aborts any single download > 2 GiB to prevent disk-fill from a malicious or runaway HappyHorse 1.0 output.
