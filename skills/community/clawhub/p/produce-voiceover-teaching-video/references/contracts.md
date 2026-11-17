# Artifact contracts

## Job layout

```text
video-job/
  job.json
  00-source/source-manifest.json
  01-intake/input-report.json
  02-timing/audio-report.json, timing.json, segments.json, subtitles.srt
  03-editorial/editorial-brief.json
  04-storyboard/storyboard.json
  05-visuals/visual-manifest.json, assets/
  06-edit/composition-report.json, proxy.mp4, chunks/
  07-qc/qc-report.json
  08-delivery/final.mp4, cover.png, publish-copy.json
```

## Common report envelope

Every stage JSON uses:

```json
{
  "schema_version": 1,
  "stage": "01-intake",
  "worker": "intake-and-rights",
  "status": "pass",
  "input_hash": "sha256",
  "outputs": {},
  "issues": []
}
```

Use `needs-human` for editorial taste or missing rights confirmation. Use `fail` for unreadable input, unsupported format, factual mismatch, synchronization errors, render failures, or invalid delivery media.

## Editorial brief minimum fields

`audience`, `promise`, `problem`, `teaching_steps`, `examples`, `caveats`, `verified_facts`, `prohibited_copy`, `cta`, and `rights_notes`.

## Timing segment minimum fields

`segment_id`, `start`, `end`, `text`, `confidence`, and optional `words`. Times are seconds from the prepared narration start.

## Storyboard beat minimum fields

`beat_id`, `start`, `end`, `timing_segment_ids`, `teaching_goal`, `visual_id`, `visual_kind`, `source_id`, `on_screen_text`, `safe_bounds`, and `transition`.

## Source-video interlude minimum fields

`interlude_id`, `source_id`, `insert_before_segment_id`, `duration`, `playback_rate`, `audio_policy`, `narration_policy`, `caption_policy`, `poster_frame`, and `resume_segment_id`.

Use `playback_rate: 1.0`, `audio_policy: original-only`, `narration_policy: pause-resume`, and `caption_policy: pause-resume` unless the user explicitly requests different treatment. Interludes extend the final timeline; they never consume or overlap narration time.

## Visual manifest minimum fields

`visual_id`, `path`, `kind`, `width`, `height`, `source_id`, `license`, `used_by_beats`, and `sha256`.

## Publish copy minimum fields

`title`, `description`, `hashtags`, `pinned_comment`, `reply_prompt`, `cover_title`, and `cover_subtitle`. Do not place hashtags inside `description`.

## QC source-video fields

When source videos are present, `qc-report.json` must include:

`source_video_count`, `source_video_speed`, `source_video_audio`, `narration_during_source_video`, `captions_during_source_video`, `resume_continuity`, `black_intervals`, and `canonical_master_sha256`.

`narration_during_source_video` and `captions_during_source_video` must be `false`. `resume_continuity` must be `pass`.

## Ending CTA fields

When a voiced ending CTA is enabled, record `text`, `audio_path`, `voice_source`, and `authorization`. Never synthesize or imitate a supplied voice without explicit authorization.
