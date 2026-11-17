# HiAPI Handoff

This skill hands the final prompt to one of two HiAPI skills. This reference defines how to pick the target, how to fill the command, and what to do when the constraints conflict.

## Pick The Target Model

| Use Seedance 2.0 when | Use HappyHorse 1.0 when |
| --- | --- |
| The video is image-to-video | The video is text-to-video and the user wants a fast draft |
| Duration is `4` seconds, image-to-video, or cinematic motion control | Text-to-video draft speed matters and duration is an integer from `3` to `15` |
| The user wants cinematic quality | The user wants throughput, not finish |
| The user mentioned Seedance | The user mentioned HappyHorse |

Default to Seedance 2.0 when the brief is ambiguous and quality matters more than speed.

## Seedance 2.0 Constraints

- **Durations** (`--seconds`): any integer from `4` to `15`.
- **Resolutions** (`--resolution`): `480p`, `720p`, `1080p`.
- **Aspect flag**: `--ratio`, one of `16:9`, `9:16`, `1:1`, `4:3`, `3:4`, `21:9`, `adaptive`.
- **Media modes**: text-to-video, first-frame image-to-video, first+last-frame image-to-video, or multimodal references.
- **Mutual exclusion**: do not mix first/last-frame fields with `--reference-image-url`, `--reference-video-url`, or `--reference-audio-url`.
- **Reference limits**: reference images plus first/last-frame images must be at most 9 images total; reference video URLs at most 3 clips, each 2-15 s and total <=15 s; reference audio URLs at most 3 clips, each 2-15 s and total <=15 s.
- **Image-to-video**: pass the start image through `--first-frame-url`. The old `--input-reference` alias still works, but prefer `--first-frame-url` in new handoffs.

Reject the brief or adjust the defaults if the user asks for `30` seconds, `4K`, or a ratio outside the list.

## HappyHorse 1.0 Constraints

- **Durations** (`--seconds`): any integer from `3` to `15`.
- **Resolutions** (`--resolution`): `720p`, `1080p`. Do not produce a `480p` handoff for this model.
- **Aspect flag**: `--size` (not `--ratio`), one of `16:9`, `9:16`, `1:1`, `4:3`, `3:4`. No `21:9`.
- **Input**: text-to-video only. No `--input-reference`.
- **Seed**: optional `--seed` integer from `0` to `2147483647` when the user requests reproducibility.

HappyHorse 1.0 is the lightweight text-to-video draft model. Keep the Output Contract's scene block format, but treat each block as a macro beat rather than a tight micro cut — three to four short beats at 5 s, four to six at 10–15 s. Reserve six-scene fine cutting for Seedance 2.0.

## Handoff Command Templates

The Handoff Command in the output should be ready to paste. The `node scripts/...` line must be run **from inside the installed target skill directory**, because the scripts live there, not in this skill. Always prefix with `cd` so the user can copy both lines.

### Seedance 2.0 — Text-to-Video

```bash
cd "${CODEX_HOME:-$HOME/.codex}/skills/hiapi-seedance-2-0-video-skill" \
  || cd "${CODEX_HOME:-$HOME/.codex}/skills/hiapi-seedance-2-0-video" \
  || cd "$HOME/.claude/skills/hiapi-seedance-2-0-video"
node scripts/hiapi-seedance-2-video.mjs \
  --prompt "<final-copy-ready-prompt>" \
  --seconds <4-15> \
  --resolution <480p|720p|1080p> \
  --ratio <16:9|9:16|1:1|4:3|3:4|21:9|adaptive>
```

### Seedance 2.0 — Image-to-Video

```bash
cd "${CODEX_HOME:-$HOME/.codex}/skills/hiapi-seedance-2-0-video-skill" \
  || cd "${CODEX_HOME:-$HOME/.codex}/skills/hiapi-seedance-2-0-video" \
  || cd "$HOME/.claude/skills/hiapi-seedance-2-0-video"
node scripts/hiapi-seedance-2-video.mjs \
  --prompt "<final-copy-ready-prompt>" \
  --first-frame-url "<https-url-data-uri-or-asset-id>" \
  --seconds <4-15> \
  --resolution <480p|720p|1080p> \
  --ratio <16:9|9:16|1:1|4:3|3:4|21:9|adaptive>
```

### Seedance 2.0 — First+Last-Frame Image-to-Video

```bash
cd "${CODEX_HOME:-$HOME/.codex}/skills/hiapi-seedance-2-0-video-skill" \
  || cd "${CODEX_HOME:-$HOME/.codex}/skills/hiapi-seedance-2-0-video" \
  || cd "$HOME/.claude/skills/hiapi-seedance-2-0-video"
node scripts/hiapi-seedance-2-video.mjs \
  --prompt "<final-copy-ready-prompt>" \
  --first-frame-url "<https-url-data-uri-or-asset-id>" \
  --last-frame-url "<https-url-data-uri-or-asset-id>" \
  --seconds <4-15> \
  --resolution <480p|720p|1080p> \
  --ratio <16:9|9:16|1:1|4:3|3:4|21:9|adaptive>
```

### Seedance 2.0 — Multimodal References

```bash
cd "${CODEX_HOME:-$HOME/.codex}/skills/hiapi-seedance-2-0-video-skill" \
  || cd "${CODEX_HOME:-$HOME/.codex}/skills/hiapi-seedance-2-0-video" \
  || cd "$HOME/.claude/skills/hiapi-seedance-2-0-video"
node scripts/hiapi-seedance-2-video.mjs \
  --prompt "<final-copy-ready-prompt>" \
  --reference-image-url "<https-url-data-uri-or-asset-id>" \
  --reference-video-url "<https-url-data-uri-or-asset-id>" \
  --reference-video-duration <2-15> \
  --reference-audio-url "<https-url-data-uri-or-asset-id>" \
  --reference-audio-duration <2-15> \
  --seconds <4-15> \
  --resolution <480p|720p|1080p> \
  --ratio <16:9|9:16|1:1|4:3|3:4|21:9|adaptive>
```

### HappyHorse 1.0 — Text-to-Video

```bash
cd "${CODEX_HOME:-$HOME/.codex}/skills/hiapi-happyhorse-1-0-video" \
  || cd "$HOME/.claude/skills/hiapi-happyhorse-1-0-video"
node scripts/hiapi-happyhorse-1-video.mjs \
  --prompt "<final-copy-ready-prompt>" \
  --seconds <3-15> \
  --resolution <720p|1080p> \
  --size <16:9|9:16|1:1|4:3|3:4>
```

Refer to the target skill's own SKILL.md for any additional flags it supports.

## What To Do When Constraints Conflict

| Conflict | Resolution |
| --- | --- |
| User wants `30` seconds | Offer `15` seconds for either Seedance 2.0 or HappyHorse 1.0 and a shorter scene plan. Note the change in the output. |
| User wants `4K` | Offer the target's max (`1080p` for Seedance or HappyHorse) and explain the limit. |
| User wants a square ratio for cinematic work | Offer `1:1`, but also offer `16:9` as an alternative. |
| User wants `21:9` on HappyHorse | Either switch the target to Seedance 2.0 or downgrade to `16:9`. Do not emit `21:9` for HappyHorse. |
| User wants image-to-video with HappyHorse | Switch to Seedance 2.0. Note the switch. |
| User wants strict first and last frames plus other image/video/audio references on Seedance | Use first+last-frame mode and move the reference intent into the prompt, or drop strict frame control and use multimodal reference mode. Do not mix the two modes in one command. |
| User asks for a feature the source does not support | Drop the feature from on-screen text. Move it to Negative Constraints. |

## After Handoff

When the user runs the generated command:

- A successful Seedance 2.0 task downloads to `outputs/` when possible, or returns a remote URL.
- HappyHorse 1.0 follows the same shape but with shorter total run time.
- If the user reports an error, follow the Error Guidance section in the target skill's SKILL.md.
