# Editing and rendering

Requires FFmpeg 5 or newer on PATH (`ffmpeg -version`) with libx264, the `xfade`, `zoompan`, `drawtext`, `subtitles`, `sidechaincompress`, `loudnorm` and `amix` (with `normalize`) filters. Standard builds have them. Tested here with FFmpeg 6.1.1.

## How the render works

1. **Timeline.** Each scene lasts its narration length rounded up to whole frames, so picture and voice cannot drift, even over 30 minutes.
2. **Shots.** Each media file becomes a shot rendered to its own cached file:
   - video: scaled to cover 1920x1080, cropped, set to the project fps, looped if shorter than the shot;
   - image: Ken Burns (slow zoom in, pan right, zoom out, pan left in rotation) built from a 2x upscaled frame.
3. **Scenes.** Shots are joined with `xfade` (default alternating `fade` and `dissolve`, 0.5 s). The overlap is planned so the scene keeps its exact length. If a scene is too short for its shots, the extra media are not used. On-screen text (`on_screen_text`) appears as a lower caption between 0.4 s and 4.5 s.
4. **Join.** Scenes are concatenated with hard cuts (stream copy).
5. **Audio.** Scene audio is padded or trimmed to the exact scene length and joined. Music is looped, trimmed, faded in and out, lowered, and ducked under the voice with `sidechaincompress`. Sound effects are placed with `adelay`. The mix is normalised with `loudnorm` (I=-16 LUFS, TP=-1.5 dB, single pass) and encoded AAC 192 kbps.
6. **Output.** `out/video.mp4`, H.264 yuv420p, `+faststart`, 1080p. `--draft` makes `out/preview.mp4` at 640x360.

Rerunning skips unchanged shots and scenes (cache keys include the source file, timing and settings). Delete `build/` to force a full re-render.

## Options

- `--only s03,s04` previews selected scenes. `--draft` is much faster; look at pacing and matching before the final.
- Transitions: pass a short `--transition-sec 0.2` for near-cuts, or any `xfade` name (`fade`, `dissolve`, `slideleft`, `wipeleft`, `fadeblack`, `circleopen`). Fewer transition types look more professional.
- `--burn-subs` re-encodes the whole video to hard-code `out/subtitles.srt`; leave it off if you will upload captions.
- Change `fps` or `resolution` in `project.json` before generating voiceover; the timeline uses `fps`.
- Fonts: the script looks for DejaVu, Liberation, Arial and falls back to `fc-match`; pass `--font PATH` otherwise.

## Time and disk

Roughly: a 10-minute 1080p render takes several minutes on a laptop with `veryfast` and CRF 18; a 30-minute video takes longer and the final file can reach a few GB. Shots are cached in `build/shots`, which can take several GB; clean `build/` after publishing. Render in a session that will not be stopped; sandboxes may reclaim long background jobs, so render on the user's machine for long videos.

## Troubleshooting

- `Missing media file` or `has no media`: run `fetch_clips.py list DIR`, then `pick` or `add-local`.
- Black or frozen frames in a shot: the source is corrupt or very short; replace it with `pick --redo` or `add-local`.
- Audio shorter than video (or the reverse): check that every scene has `audio_duration`; re-run `voiceover.py`.
- `No such filter`: FFmpeg is too old or minimal; install a full build.
- Text shows as boxes: the font lacks the language's glyphs; pass a font that has them.
- Duration warning at the end: compare `out/video.mp4` with the plan; a difference over 0.25 s means a scene file is stale, delete `build/scenes`.

## Why FFmpeg and not MoviePy

FFmpeg does every step here (cut, scale, zoom, transitions, mix, ducking, loudness, subtitles, encode) with one dependency and is faster and more memory-safe on long videos than frame-by-frame Python editing. MoviePy is optional: use it only for custom per-frame effects, and render those to a clip first, then register the clip with `fetch_clips.py add-local`.
