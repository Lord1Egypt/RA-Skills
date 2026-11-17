---
name: mixcut-art-supplies-video
description: Create mixed-cut promotional videos for art supplies, drawing tools, sketching lessons, or painting material clips. Use when the user provides one or more art/drawing source videos and wants a finished vertical short video with stable mixed editing, Chinese male AI voiceover, synchronized Chinese subtitles, original sound kept as low background audio, and product-promotion style copy without explicitly mentioning platform names unless requested.
---

# 混剪美术用品视频skill

## Core Output

Create a finished vertical promotional video from user-provided art supplies or drawing-practice素材. Favor stable, readable segments over fast montage. The current preferred style is:

- Each source video appears at most once.
- Each displayed source segment is at least 4 seconds.
- Total duration may exceed 30 seconds when there are many素材.
- Preserve original video sound as low background audio.
- Add Chinese male AI voiceover, preferably a lively young male / monkey-like style when available.
- Add synchronized Chinese subtitles: no background plate, white fill with black outline, larger font, positioned higher than the very bottom.
- Do not mention 拼多多/PDD or any platform unless the user explicitly asks.

## Editing Rules

1. Treat videos of active drawing, shading, coloring, object shaping, or hand movement as重点素材.
2. Treat tool-only, product-detail-only, or static display clips as非重点素材, but still show them for at least 4 seconds if used.
3. Use each source material only once in the final timeline. Do not create end-of-video recap sections that repeat previous素材.
4. Prefer one continuous representative segment per source video. Do not split a single素材 into many 0.5s or 0.8s fragments unless the user explicitly requests fast montage.
5. If素材数量较少, use 5-8 seconds per素材. If素材数量很多, use 4-6 seconds per素材.
6. If a source clip is shorter than 4 seconds, use the full clip and optionally slow it slightly only if motion still looks natural.
7. Choose segment starts where the action is clear: the hand is visible, the drawing change is readable, and the subject is not blocked for most of the segment.

## Story And Copy

Write one voiceover sentence group per source segment. The copy must describe what is visible in that same segment.

Recommended order:

1. Overall hook: show main drawing effect or the most attractive active画面.
2. Technique detail: dark areas, highlights, edges, shading, transitions, texture.
3. Composition or complete still-life view.
4. Tool/material value: smooth laying, clean highlights, controllable lines, suitable practice.
5. Closing: stable continuous final画面, often geometry/basic practice or finished result.

Copy style:

- Short, direct Chinese promotional commentary.
- Explain visible art effects instead of generic selling slogans.
- Keep each segment's voiceover shorter than that segment by at least 0.2 seconds.
- Avoid saying "this" if the visual will cut before the phrase finishes.
- Do not force a material label such as "glass vessel" unless the current scene clearly shows it.

## Subtitle And Audio Timing

- Generate voice per segment, then assemble the voice track according to segment durations.
- Subtitle timings should match the actual segment/voice timings, not a fixed 5-second template.
- If TTS is longer than a segment, either shorten the copy or extend the segment; do not let the voice continue into the next unrelated visual.
- Keep original audio under the AI voice, typically around 15-30% before the final mix. Raise or lower by ear if the original sound is too loud or too quiet.
- Use a large bold Chinese font with white fill and black outline. Use no subtitle background box.

Suggested ASS style for 720x1280 vertical video:

```ass
Style: Promo, Microsoft YaHei, 56, &H00FFFFFF, &H00FFFFFF, &H00000000, &H00000000, 1, 0, 0, 0, 100, 100, 0, 0, 1, 5, 0, 2, 36, 36, 205, 1
```

## Workflow

1. Inspect all provided source videos for duration, audio presence, and visible content.
2. Decide a single segment for each source video, with every segment at least 4 seconds.
3. Build a timeline table before final generation: source file, start time, duration, scene description, voiceover text, subtitle timing.
4. Generate or synthesize Chinese male voiceover per segment.
5. Combine segments into one vertical 720x1280 video, preserving low original audio.
6. Mix AI voice above original audio and burn synchronized subtitles into the video.
7. Validate the final file:
   - duration is expected and may exceed 30 seconds;
   - each source appears once;
   - no segment shorter than 4 seconds unless the source itself is shorter;
   - voice and subtitles match the visible scene;
   - playback has no decode errors.
8. Report the output path and the final timing composition to the user.

## Defaults

- Output format: MP4, vertical 720x1280, H.264 video, AAC audio.
- Target duration: no fixed cap; use 4-8 seconds per素材.
- Segment pacing: stable, tutorial-promo style, not fast music-video montage.
- Subtitle location: lower third but higher than platform UI-safe bottom.
- Voice style: Chinese male, energetic but clear.
