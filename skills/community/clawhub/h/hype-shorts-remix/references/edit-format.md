# Plain JSON edits

An edit is ordinary JSON. Paths are relative to the edit file and point to local media files.
Times are in seconds; canvas dimensions are even pixel counts. The renderer preserves source
files and refuses to overwrite existing output.

The first release supports 1–60 shots and up to 180 seconds. Use even width/height from 128 to
1920 with at most 2,073,600 canvas pixels, and integer frame rates from 1 to 60. Inputs are at
most 2 GiB each. Captions support up to 200 entries of 1000 characters; audio volume is 0–2.
The installed fonts must cover the caption language. `FFMPEG_PATH` and `FFPROBE_PATH` may select
the host's executable paths when they are not on PATH.

```json
{
  "version": 1,
  "width": 720,
  "height": 1280,
  "fps": 24,
  "shots": [
    { "file": "assets/shot-01.mp4", "start": 0, "duration": 2.5 },
    { "file": "assets/shot-02.mp4", "start": 0, "duration": 2.5 }
  ],
  "captions": [
    { "start": 0.1, "end": 2.3, "text": "Start with something worth watching." },
    { "start": 2.6, "end": 4.8, "text": "Then give it a new meaning." }
  ],
  "narration": { "file": "assets/narration.wav", "volume": 1 },
  "music": { "file": "assets/music.mp3", "volume": 0.15 }
}
```

Omit `narration` and `music` when unused. Source audio is preserved where present, with silence for
silent shots. Optional narration/music is mixed, padded or trimmed to the video timeline rather
than looped. Review the mix by listening and adjust the supplied audio/volumes when needed.

Each shot can use local video or a still PNG/JPEG/WebP image. `start` selects the video in-point;
`duration` is its timeline length. Captions are literal text, positioned by the renderer's readable
subtitle style. More elaborate typography or motion can be authored separately as local media.

```sh
node "$SKILL_DIR/scripts/media.mjs" render --project edit.json --output final.mp4
```

The command creates the MP4 and `final.mp4.render.json` with measured output information and input
provenance. A 720×1280 canvas containing a 1280×720 generated shot is an edited composition; retain
both sets of dimensions when reporting what was generated and what was delivered.

Run `media.mjs inspect` on a selected reference or output to collect metadata and visual samples.
Use a fresh analysis directory for a new inspection. Rendering another version should use a new
output filename, such as `final-v2.mp4`.
