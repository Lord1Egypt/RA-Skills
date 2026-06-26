---
name: local-video-ad-pipeline-v05-public
description: "Local Video Ad Pipeline v0.5 is a public OpenClaw skill for producing short commercial videos and YouTube Shorts with local AI models. It uses a local LLM as the full film director: concept bible, story intent, visual arc, beats, shot direction, shotlist, image prompts, Korean subtitle script, and subtitle-based timing. Keyframes are generated with Qwen-Image or SDXL through ComfyUI, shots are animated sequentially with Wan2.2, optional BGM can be created with ACE-Step, and final MP4 assembly is handled with ffmpeg. Designed for local GPU workflows where models must be loaded one at a time. Includes character consistency rules, prompt-level identity locking, direct Qwen-Image keyframe generation, Korean subtitle wrapping, no-slow native-speed assembly, contact-sheet QA, and practical GPU coexistence guidance."
---

# Local Video Ad Pipeline

End-to-end recipe for a short multi-shot video produced with local models. The workflow is intentionally sequential because Qwen-Image, Wan2.2, and ACE-Step often compete for the same GPU memory pool.

Version: public v0.5. This version has no separate film-director helper reference. The local LLM performs the complete directing process from the user's brief: story intent, visual arc, shot rhythm, camera direction, actor expression, shotlist, image prompts, and subtitle timing.

## When to deviate

If the user wants a single still image, use a manga/manhwa/qwen-image skill instead. If they want long-form video over one minute, dialogue, or lipsync, this skill is the wrong tool; recommend a hosted video service or a narrower local prototype. If they only want music, use `scripts/fire_bgm.py`.

## Project layout

```
<project>/
  meta/
  bible.json
  beats.json
  shotlist/shotlist.json
  prompts/prompts.json
  character/anchor.png
  character/character_bible.json
  durations.json
  keyframes/<sid>.png
  videos/<sid>.mp4
  audio/bgm.wav
  subs.json
  final/final.mp4
```

## Before running

Run the read-only environment check. For silent/no-BGM videos, pass `--silent` so ACE-Step is treated as intentionally skipped.

```bash
python scripts/doctor.py --project <project> --comfy http://127.0.0.1:8192
python scripts/doctor.py --project <project> --comfy http://127.0.0.1:8192 --silent
```

It checks Python, ffmpeg, WSL input/output folders, the ComfyUI server, and required ComfyUI nodes.

## Pipeline

### 1. Pre-production scripting

Generate `bible.json`, `director_notes.json`, `beats.json`, `shotlist/shotlist.json`, and `prompts/prompts.json` by chatting a local llama.cpp server. See `references/preproduction.md` for prompt templates and JSON schemas.

Default female protagonist casting, unless the user specifies a different look: make an adult Korean woman in her early 20s with celebrity/Instagram-model-level beauty, bright clear eyes, pure elegant aura, polished but realistic skin, and a glamorous adult model figure. For photoreal local Qwen-Image work, separate the image grammar: backgrounds, lighting, camera, hands, props, and environment should be ultra-realistic and candid; the protagonist should be cast as an obviously beautiful high-end model rather than an ordinary realistic person. YouTube Shorts are attention-driven, so adult glamour, sensual styling, fitted silhouettes, fashion/swimwear/lingerie/gravity-of-attraction aesthetics, and body-forward composition are allowed when they fit the brief. Use a fitted fashion silhouette when the scene allows it: open cardigan or jacket, fitted V-neck knit/top/blouse, balanced hourglass proportions, and clearly defined G-cup bust silhouette through clothing. Keep the character clearly adult. If the user asks for minors, school-age characters, school uniforms, childlike characters, or age-ambiguous characters, override this default and keep the portrayal conservative and age-safe.

Do not put broad sexuality, clothing, body, or exposure suppressors such as `sexualized`, `revealing clothing`, `cleavage`, `large breasts`, `lingerie`, `swimwear`, `transparent blouse`, or `nudity` into the global default negative prompt. Those suppressors block normal adult fashion, glamour, swimsuit, underwear, and Shorts-style attention hooks. Use them only when the user explicitly requests a conservative/no-exposure project or when the protagonist is a minor, school-age, childlike, or age-ambiguous character. The default negative should focus on quality failures: duplicate people, collage/split screen, bad hands, text, watermark, wrong age, ordinary/plain face when a model protagonist is requested, and plastic AI skin.

For stronger film direction, start with `director_notes.json` before writing beats. The local LLM director pass owns the story arc, rhythm, opening image, turning point, final image, shot-size progression, camera direction, actor expression, and continuity rules. Later passes derive beats, shotlist, and prompts from that LLM-generated director pass.

The shotlist schema is a hard requirement. `fire_videos.py` reads `shot_id`, `action`, `mood`, `lighting`, `camera_motion`, and `shot_type` from each entry. The LLM pre-production pass must also fill `director_intent`, `actor_direction`, `emotional_expression`, `composition`, and `continuity`; these fields guide keyframe prompts and help prevent disconnected pretty shots.

For any recurring protagonist, `bible.json` must include `characters[].lock_tokens`. Every prompt for a shot with `needs_character: true` must begin with that exact string, unchanged.

For facial performance, use `references/expression_language.md`. Do not rely on `mood` alone; add visible expression cues such as heavy eyelids, lifted brows, pressed lips, faint smile, direct eye contact, or shoulders opening.

For detail shots, use `identity_framing` so the face lock does not overpower the intended crop. Use `feet_only`, `hands_only`, `body_detail`, or `back_view` for shoes, hands, backpack straps, lower legs, and walking-away shots.

### 2. Keyframes

Render one PNG per shot to `<project>/keyframes/<sid>.png` using direct Qwen-Image BF16 ComfyUI workflow JSON. This is the default path for cinematic keyframes because it preserves the director prompt and avoids fixed GUI styling.

```bash
python scripts/generate_keyframes_direct.py --project <project> \
  --comfy http://127.0.0.1:8194 --shots S01 S02 S03 S04 S05 S06

python scripts/image_contact_sheet.py --project <project> --glob "keyframes/*.png" \
  --out <project>/final/keyframe_contact_sheet.jpg
```

The direct script inserts `characters[].lock_tokens` from `bible.json` at the start of every `needs_character: true` shot prompt. This prompt-level character lock is the preferred local identity method for Qwen-Image BF16.

Use the older GUI-builder T2I helper only as a fallback when you intentionally want the local GUI's fixed settings:

```bash
python scripts/generate_keyframes_t2i.py --project <project> \
  --comfy http://127.0.0.1:8194 --shots S01 S02
```

Avoid the GUI-builder path for free cinematic angle work. Local GUI presets can make shots look overly standardized or can fight the shot prompt.

Qwen T2I can interpret film/storyboard language as a multi-panel page. The direct script forces one single full-frame vertical photograph and rejects collage, storyboard, split screen, multiple panels, triptych, film strip, and contact sheet. If a generated keyframe still contains multiple panels, reject it and regenerate only that shot.

If prompt-level locking is not enough for one or two shots, use the character anchor workflow as a selective repair path:

```bash
# 1. Start the Qwen Image Edit ComfyUI stack, usually :8189.

# 2. Create or choose a stable protagonist anchor.
python scripts/generate_character_anchor.py --project <project> \
  --prompt "photorealistic Korean high school girl, modest school uniform, natural face, shoulder-length black hair, wholesome study film protagonist" \
  --comfy http://127.0.0.1:8189

# 3. Repair only rejected shots by editing from the same anchor.
python scripts/generate_keyframes_from_anchor.py --project <project> \
  --comfy http://127.0.0.1:8189 --shots S03 S05

# 4. Inspect identity consistency before Wan2.2.
python scripts/image_contact_sheet.py --project <project> --glob "keyframes/*.png" \
  --out <project>/final/keyframe_contact_sheet.jpg
```

For stronger control, add `character_identity` to `prompts/prompts.json`:

```json
{
  "global_style": "cinematic realistic Korean study film",
  "character_identity": "one beautiful adult Korean woman in her early 20s, celebrity-level Instagram model face, clear bright dark-brown eyes, long silky natural black hair, fresh Korean daily makeup, polished realistic skin texture, glamorous adult model figure, fitted fashion silhouette, clearly defined G-cup bust silhouette through clothing"
}
```

Before continuing, make a contact sheet or inspect representative frames. Verify:

- The protagonist matches the requested age, gender, clothing, and tone.
- The shot is conservative and age-safe when minors, school-age characters, school uniforms, childlike characters, or age-ambiguous characters are requested. For clearly adult protagonists, do not reject glamour, sensual styling, fitted clothing, cleavage, swimwear, lingerie, or body-forward composition merely because it is attractive.
- Exactly one protagonist appears when the request asks for one person; no duplicate, twin, friend, or accidental group shot.
- The same character identity is plausible across shots.
- Text on screens or notebooks is not relied on for the message; final subtitles carry the message.

If one or two shots drift, regenerate only those shot IDs with `generate_keyframes_direct.py --shots S03 S05` first. Use Image Edit only after direct retries fail. Do not proceed to Wan2.2 until the keyframe sheet is acceptable.

### 3. Wan2.2 video

Read `references/wan22_server.md` first. It has the lifecycle rules.

```bash
# Start the WSL Wan2.2 ComfyUI server, or confirm :8192 is already up.

python scripts/fire_warmup.py --comfy http://127.0.0.1:8192
# Wait for fire_warmup_out_00001.mp4 in:
# \\wsl.localhost\Ubuntu\home\choi_g16\comfy\ComfyUI\output\

python scripts/fire_videos.py --project <project> --comfy http://127.0.0.1:8192
# Do not poll ComfyUI while rendering.

python scripts/fire_videos.py --project <project> --collect
# Copies finished film_video_Sxx*.mp4 files into <project>/videos/Sxx.mp4.
```

For VRAM-safe unattended work, prefer sequential rendering:

```bash
python scripts/render_sequential.py --project <project> --shots S01 S02 S03 S04 S05 S06 \
  --comfy http://127.0.0.1:8192 --frames 80 --width 832 --height 480
```

For commercial/YouTube Shorts rhythm, prefer subtitle-based variable timing. Read `references/subtitle_timing.md`.

```bash
python scripts/plan_subtitle_durations.py --project <project> \
  --subs <project>/subs.json --update-shotlist

python scripts/render_sequential.py --project <project> --shots S01 S02 S03 S04 S05 S06 \
  --comfy http://127.0.0.1:8192 \
  --durations <project>/durations.json \
  --duration-fps 16 --frame-pad 8 \
  --width 480 --height 832
```

Re-shoot specific shots without restarting WSL:

```bash
python scripts/fire_videos.py --project <project> --shots S02 S05
python scripts/fire_videos.py --project <project> --shots S02 S05 --collect
```

### 4. BGM

Skip this stage when the user requests silence or no background music. If BGM is requested, read `references/ace_bgm.md` first. It has the GPU coexistence rule.

```bash
wsl --shutdown
# Start F:\AI\ACE-Step\start_gradio_ui_rocm.bat with CHECK_UPDATE=false.

python scripts/fire_bgm.py --out <project>/audio/bgm.wav --duration 30 \
  --prompt "dark cinematic trap, hard 808 bass, instrumental, no vocals"
```

`fire_bgm.py` now auto-discovers the ACE-Step generation endpoint. Pass `--fn-index` only if discovery fails after an ACE-Step UI update.

### 5. Compose

Write `<project>/subs.json`:

```json
{
  "S01": "지금 시작하자.",
  "S02": "실패도 연습이 된다.",
  "S03": "다시 시도하면 된다."
}
```

Standard compose, where short generated clips may be stretched to a target per-shot duration:

```bash
python scripts/compose.py --project <project> \
  --subs <project>/subs.json \
  --bgm <project>/audio/bgm.wav \
  --out <project>/final/final.mp4 \
  --per-clip 5 --hero S03 S06
```

Preferred Shorts compose, where each shot duration follows subtitle reading time:

```bash
python scripts/plan_subtitle_durations.py --project <project> \
  --subs <project>/subs.json --cps 5.5 --min 1.6 --max 5.0 --update-shotlist

python scripts/compose.py --project <project> \
  --subs <project>/subs.json \
  --durations <project>/durations.json \
  --out <project>/final/final.mp4 \
  --no-slow --max-subtitle-chars 34
```

Silent/no-slow compose, where clip speed is not stretched. Use this when the user says not to slow, interpolate, or extend frames to fit time. If the result is shorter than the target, render more native frames or add another short native clip.

```bash
python scripts/compose.py --project <project> \
  --subs <project>/subs.json \
  --out <project>/final/final.mp4 \
  --no-slow --target-duration 45 --max-subtitle-chars 34
```

Create a visual QA sheet:

```bash
python scripts/contact_sheet.py <project>/final/final.mp4 --out <project>/final/contact_sheet.jpg
python scripts/validate_video.py <project>/final/final.mp4 --orientation portrait
```

The compose script burns subtitles from UTF-8 text files. It sanitizes direct newline characters because `drawtext` can render them as missing glyph boxes on this Windows ffmpeg path. Keep Korean subtitles short and use `--max-subtitle-chars` for overflow control.

## Duration Rules

Default commercial/Shorts timing is subtitle-based, not equal-grid timing:

```
shot_duration_s = visible_subtitle_chars / cps + lead_breath + tail_breath
total_duration_s = sum(shot_duration_s)
```

If a user asks for exact duration and no slow-motion, calculate native frames first:

```
native_seconds ~= frames / source_fps
target_seconds = sum(native clip durations)
```

For Wan2.2 at 16 fps, 80 frames often lands around 4.8 seconds after encode. Verify with `ffprobe` and add native frames or a short final native clip if needed. Do not use `setpts` stretching in no-slow mode.

## Hard Rules

- Never restart the WSL ComfyUI server between shots unless it is actually wedged. First load is slow; warm runs are much faster.
- Do not poll `/queue` or `/history` while Wan2.2 is rendering. Use the filesystem and `--collect` after enough time has passed.
- Qwen-Image, Wan2.2, and ACE-Step should not run simultaneously on this 96 GB UMA host. Use one server at a time.
- For one recurring protagonist, use prompt-level `lock_tokens` plus direct Qwen T2I as the default. Use Qwen Image Edit from an anchor only for same-scene variations or selective face/outfit correction.
- Do not use the Qwen GUI builder as the primary keyframe path for cinematic shorts; it can impose fixed style and weaken free shot design.
- For YouTube Shorts, keep the same portrait aspect through every stage: keyframes, Wan render, compose, and QA. Use `480x832` for the local Wan2.2 production path unless deliberately making landscape.
- Use `wsl --shutdown` between major server classes when VRAM behavior looks sticky.
- Keep Wan2.2 production settings around 832x480 landscape or 480x832 Shorts portrait / 33+ frames / 4 Lightning steps unless intentionally stress testing.
- For no-slow videos, render native frames from subtitle duration via `render_sequential.py --durations`; use fixed 80-frame clips only for rough prototypes.
- Use `CHECK_UPDATE=false` for the ACE-Step launcher in unattended mode.
- After switching image/video/BGM servers, clean up stale launch windows and ports:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/cleanup_local_video_servers.ps1
```

## Delivery

OpenClaw's `MEDIA:` directive can fail for larger Telegram videos. If that happens, send via the Telegram Bot API directly using the bot token already configured in OpenClaw. Never paste the token into chat logs.

## Time budget

Verified target for six 5-second shots:

| Stage | Time |
| --- | --- |
| Pre-production | ~5 min |
| Keyframes | ~10 min |
| Wan warmup | ~10 min |
| Wan render | ~5-20 min per shot, depending on frames |
| BGM | ~1 min |
| Compose | ~1 min |

Add time for human review and re-shoots.
