# Subtitle-Based Variable Timing

Use this for commercial or YouTube Shorts style videos where each cut should last only as long as the viewer needs to read or hear that shot's subtitle.

## Principle

Do not divide total duration evenly by shot count. The writer's subtitle script defines the editing rhythm.

Workflow:

1. The film writer creates one subtitle line per shot.
2. `plan_subtitle_durations.py` estimates reading time for each subtitle.
3. The script writes `<project>/durations.json` and updates `shotlist/shotlist.json` `duration_s`.
4. `render_sequential.py --durations` renders a different native frame count per shot.
5. `compose.py --durations --no-slow` trims each native clip to its subtitle duration without stretching.

## Reading Speed Defaults

Korean Shorts campaigns usually work around:

| Style | CPS |
| --- | --- |
| Fast ad / energetic shorts | 6.0-6.5 visible chars/sec |
| Standard narration | 5.0-5.8 visible chars/sec |
| Emotional campaign | 4.4-5.2 visible chars/sec |

The default is `5.5 cps` plus a small lead/tail breath.

## Subtitle File

Create `<project>/subs.json`:

```json
{
  "S01": "하루 종일 화면만 보고 있으면",
  "S02": "마음도 조금씩 굳어버려.",
  "S03": "잠깐만 창밖을 봐.",
  "S04": "봄은 이미 와 있어."
}
```

## Plan Durations

```bash
python scripts/plan_subtitle_durations.py --project <project> \
  --subs <project>/subs.json \
  --cps 5.5 --min 1.6 --max 5.0 \
  --update-shotlist
```

This writes:

```
<project>/durations.json
<project>/meta/subtitle_durations.json
```

## Render With Variable Frames

```bash
python scripts/render_sequential.py --project <project> \
  --shots S01 S02 S03 S04 S05 S06 \
  --comfy http://127.0.0.1:8192 \
  --durations <project>/durations.json \
  --duration-fps 16 --frame-pad 8 \
  --width 480 --height 832
```

`frame-pad` intentionally renders a little extra native motion so the composer can trim cleanly without slowing the clip.

## Compose

```bash
python scripts/compose.py --project <project> \
  --subs <project>/subs.json \
  --durations <project>/durations.json \
  --out <project>/final/final.mp4 \
  --no-slow --max-subtitle-chars 34
```

If a clip is shorter than its subtitle duration, do not stretch it. Re-render that shot with more frames or slightly increase `--frame-pad`.

## Validate

Always validate final Shorts output:

```bash
python scripts/validate_video.py <project>/final/final.mp4 --orientation portrait
python scripts/contact_sheet.py <project>/final/final.mp4 --out <project>/final/contact_sheet.jpg
```

The contact sheet preserves aspect ratio. If it looks stretched, the video itself may have been rendered with the wrong width/height.

## QA

- The subtitle should disappear when the visual thought ends, not at a fixed grid time.
- Short punch lines should be short shots.
- Longer emotional lines should hold longer.
- The final line usually needs extra tail time; `plan_subtitle_durations.py` adds `--final-tail`.
- If the total runtime must be exact, adjust the script first, then regenerate durations.
