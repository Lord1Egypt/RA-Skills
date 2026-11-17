# Performance modes

Select one mode at initialization. Default to `fast` unless the user asks for higher polish.

| Setting | fast | balanced | quality |
| --- | --- | --- | --- |
| Proxy | 540x960, 15 fps | 720x1280, 24 fps | 720x1280, 30 fps |
| Final | 1080x1920, 30 fps | 1080x1920, 30 fps | 1080x1920, 30 fps |
| Proxy CRF | 30 | 27 | 24 |
| Sample interval | 60 s | 30 s | 15 s |
| Targeted repair rounds | 1 | 2 | 3 |
| Final encoder preset | veryfast | medium | slow |
| Motion density | section transitions only | section plus key examples | custom per beat |

## Token controls

- Let only timing and editorial workers read source text. Other workers consume structured subsets.
- Cap editorial prose at 1,200 words and each worker report at 600 words plus JSON data.
- Reuse transcripts, probes, crops, diagrams, and render chunks when input and config hashes match.
- Never paste binary metadata, full HTML, full subtitles, or console logs into agent messages. Pass paths.
- Use scripts for hashes, duration math, audio retiming, media probes, frame sampling, and package scans.
- Run one coordinator plus the workers needed for the active wave. Do not keep idle workers alive.

## Render controls

- Detect hardware H.264 encoders in this order when available and verified: NVENC, Quick Sync, AMF, then libx264.
- Render proxy before final. Do not render full resolution to discover layout errors.
- Divide long videos into stable 30-90 second chunks at section boundaries. Use at most two concurrent chunks on a workstation unless benchmarks support more.
- Store each chunk under a key derived from timing, storyboard, visual, style, and renderer versions.
- For caption or outro changes, invalidate only overlapping chunks.
- Insert or replace source-video interludes by rebuilding only the adjacent chunks and concat boundary. Do not rerender narration-led sections whose hashes are unchanged.
- Concatenate unchanged compatible chunks without re-encoding. Re-encode once only when stream parameters differ.
- Write revisions to a temporary master, run a full decode, then atomically replace the canonical final. Do not retain duplicate version-suffixed videos unless requested.

## Quality safeguards

Fast mode still requires full decode, nonblank first/last frames, safe-area checks, speech intelligibility, caption coverage, source-video audio isolation, gap-free narration resume, final factual comparison, and delivery validation. It reduces redundant inspection and rendering, not release standards.
