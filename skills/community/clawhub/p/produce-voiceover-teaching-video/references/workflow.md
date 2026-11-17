# Seven-worker workflow

Use the roles below as isolated employees. Pass file paths and compact manifests, not the full chat transcript.

## Execution waves

| Wave | Worker | Reads | Writes | Can run with |
| --- | --- | --- | --- | --- |
| A | 1. Intake and rights | `00-source/source-manifest.json`, `job.json` | `01-intake/input-report.json` | 2, 3 |
| A | 2. Timing and captions | prepared audio, local article/transcript | `02-timing/timing.json`, `segments.json`, `subtitles.srt` | 1, 3 |
| A | 3. Editorial distillation | local article, user goals | `03-editorial/editorial-brief.json` | 1, 2 |
| B | 4. Teaching storyboard | timing, editorial brief, image index | `04-storyboard/storyboard.json` | 5 asset preflight |
| B | 5. Visual preparation | storyboard, source images | `05-visuals/visual-manifest.json`, derivatives | 4 after beat ids stabilize |
| C | 6. Composition and finishing | timing, storyboard, visual manifest | proxy, final composition, `08-delivery/final.mp4` | no conflicting renderer |
| D | 7. QC and publishing | final video, source facts, user exclusions | QC report, cover, publish copy | deterministic probes |

Limit active workers to available capacity. Prefer three workers in Wave A and two in Wave B. Rendering is usually resource-bound; do not start multiple full-resolution renders on the same machine.

## Worker briefs

### 1. Intake and rights

Probe formats, dimensions, duration, readability, source hashes, and available rights notes. Do not extract the whole article into the report. Return missing items and `needs-human` for voice, image, music, or article rights that are unclear.

### 2. Timing and captions

Treat the prepared audio as authoritative. Reuse an existing transcript when its hash matches. Otherwise transcribe locally, align sentence timings, and create captions of one semantic phrase per cue. Before alignment, shorten only anomalous silences of roughly 0.85 seconds or longer while retaining about 0.30-0.40 seconds; preserve normal phrase boundaries. Prefer formant-preserving Rubber Band retiming when available. Keep English product names intact. Output timing data only; do not design scenes.
Mark source-video interludes as timeline insertions rather than narration segments. Captions stop at the insertion boundary and resume from the next narration cue after the interlude.

### 3. Editorial distillation

Extract the promise, audience, problem, teaching steps, examples, caveats, verified facts, prohibited copy, and final call to action. Keep the brief under 1,200 words. Do not rewrite narration that has already been recorded; flag contradictions between narration and source.

### 4. Teaching storyboard

Map every timing segment to one beat and one visual id. Choose real screenshots for proof and diagrams/cards for explanation. Declare on-screen text, source id, safe bounds, transition family, and caption collision risk. Reuse one visual run across adjacent sentences when the teaching idea does not change.
For each source video with meaningful audio, declare one standalone interlude immediately before its explanation beat. Record the insertion boundary, natural-speed duration, poster fallback, and exact narration segment that resumes afterward.

### 5. Visual preparation

Index, rotate, crop, annotate, and convert only assets referenced by the storyboard. Preserve source aspect ratio and meaning. Generate diagrams with exact text in SVG/HTML rather than image models when labels matter. Record source and license for every visual.

### 6. Composition and finishing

Author a seek-safe 9:16 composition. Render the configured proxy first. Use narration-led timing, mobile-safe captions, sparse transitions, and audio ducking. After proxy approval, render only dirty chunks, concatenate deterministically, then encode one final delivery file.
Keep narration and its captions completely absent during standalone source-video playback. Use the source clip's original audio without ducking under narration. After playback, resume at the exact next narration sample and caption cue. Build revisions to a temporary file, fully decode it, and atomically replace only `08-delivery/final.mp4`.

### 7. QC and publishing

Run full decode and technical probes, then inspect sampled frames and every flagged transition/caption boundary. Compare factual text to the frozen source. Create exact-text cover and platform-ready copy only after video QC passes. Never publish automatically unless the user separately authorizes the destination and account.
For every source-video interlude, inspect its start, midpoint, end, and return-to-narration boundary. Confirm natural-speed playback, original audio, zero narration overlap, zero narration-caption overlap, and gap-free continuation. Reject black or visually empty intervals of 0.20 seconds or longer.

## Handoff discipline

- Each worker receives `job.json`, its listed inputs, and a maximum five-line task note.
- Each report contains facts, artifact paths, issues, and status; no narrative diary.
- Use relative paths inside the job directory.
- Record input hashes in each report. A matching hash means the stage is cacheable.
- On failure, rerun the owning worker only. Invalidate downstream artifacts, not upstream artifacts.
