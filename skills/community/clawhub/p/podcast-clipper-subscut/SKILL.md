---
name: generate-podcast-clips
description: Use this skill when the user wants to turn a long podcast, interview, webinar, or talking-head video into multiple short clips for TikTok, Reels, or YouTube Shorts. It wraps Subscut's podcast clipping API in a narrow CLI interface with explicit env requirements and predictable JSON output.
homepage: https://subscut.com/agents
metadata:
  version: 1.1.0
  clawdbot:
    emoji: "🎙️"
    requires:
      bins:
        - npm
      env:
        - SUBSCUT_API_KEY
        - SUBSCUT_API_BASE_URL
    config:
      requiredEnv:
        - SUBSCUT_API_KEY
      optionalEnv:
        - SUBSCUT_API_BASE_URL
      example: |
        export SUBSCUT_API_BASE_URL="https://subscut.com"
        export SUBSCUT_API_KEY="subscut_your_api_key"
    cliHelp: |
      npm run generate-podcast-clips -- --help
      Options:
        --video-url <url>            Public long-form video URL to process
        --max-clips <number>         Number of clips to generate (1-20, default 5)
        --clip-style <style>         viral | clean | minimal | leon | hormozi
        --format <format>            dynamic | hook_frame (default: dynamic)
        --captions <boolean>         true | false (default: true)
        --min-clip-duration <secs>   Minimum clip length in seconds (default 20, min 10)
        --max-clip-duration <secs>   Maximum clip length in seconds (default 60, max 60)
        --api-key <token>            Overrides SUBSCUT_API_KEY
        --api-base-url <url>         Overrides SUBSCUT_API_BASE_URL
---

# Generate Podcast Clips

Use this skill to convert a long-form spoken video into multiple short clips through the Subscut `/podcast-to-clips` API.

## What This Skill Does

The skill is an opinionated wrapper around the API outcome:

- extracts up to 20 strong short clips from a long-form video
- favors viral and high-retention spoken moments
- adds captions with selectable styles
- supports two render formats: `dynamic` (auto-reframing) and `hook_frame` (original frame + title card)
- returns titles, scores, and rendered clip URLs

Think in outcomes, not transport:

- Good framing: "Extract viral short-form content from this podcast"
- Bad framing: "Call some video API"

## When To Use

Use this skill when:

- the input is a long podcast, interview, webinar, or talking-head video
- the user wants growth, repurposing, shorts, reels, or TikTok content
- the user wants minimal manual editing

Avoid this skill when:

- the source is already short-form
- the content is mostly non-speech
- the user wants manual, frame-by-frame editing decisions

Do not use it as a generic video editing tool.

## Input Contract

Use this compact input shape when planning or explaining the tool call:

```json
{
  "video_url": "https://example.com/video.mp4",
  "max_clips": 5,
  "style": "viral",
  "format": "dynamic",
  "captions": true,
  "clip_duration": {
    "min": 20,
    "max": 60
  }
}
```

### Field Reference

| Field | Type | Default | Notes |
|---|---|---|---|
| `video_url` | string | — | **Required.** Any HTTP/HTTPS URL. YouTube, direct MP4, Google Drive. |
| `max_clips` | integer | `5` | Range: 1–20. Short videos (≤3 min) are capped at 2 clips automatically. |
| `style` | string | `"viral"` | Caption style. See styles below. |
| `format` | string | `"dynamic"` | Render format. See formats below. |
| `captions` | boolean | `true` | Whether to burn in captions. |
| `clip_duration.min` | integer | `20` | Minimum clip length in seconds. Floor: 10s. |
| `clip_duration.max` | integer | `60` | Maximum clip length in seconds. Ceiling: 60s. Must be ≥ min. |

### Caption Styles (`style`)

| Value | Description |
|---|---|
| `viral` | Bold animated-word captions (MrBeast style). Default. |
| `beast` | Alias for `viral`. |
| `hormozi` | Alias for `leon`. Single highlighted word, clean font. |
| `leon` | Single highlighted word, clean font. |
| `clean` | Plain white subtitles, no animation. |
| `minimal` | Alias for `clean`. |

### Render Formats (`format`)

| Value | Description |
|---|---|
| `dynamic` | Auto-detects split-screen vs. solo framing, reframes to 9:16. Default. |
| `hook_frame` | Preserves original video frame, adds a title card at the top, captions at the bottom. |

Use `hook_frame` when the video is already vertical or the user wants the title displayed prominently.
Use `dynamic` (default) for horizontal/landscape podcasts with one or two speakers.

## Output Contract

Expect JSON in this shape:

```json
{
  "clips": [
    {
      "video_url": "https://...",
      "title": "Why Most Founders Get This Wrong",
      "score": 0.92,
      "start": 142.5,
      "end": 198.3
    }
  ]
}
```

`score` is a 0–1 float representing clip virality confidence. Higher is better.

## CLI Entry Point

Once the skill is installed, the agent runtime should invoke the bundled CLI wrapper:

```bash
npm --prefix .agents/skills/generate-podcast-clips run generate-podcast-clips -- \
  --video-url "https://example.com/podcast.mp4" \
  --max-clips 5 \
  --clip-style viral \
  --format dynamic \
  --captions true \
  --min-clip-duration 20 \
  --max-clip-duration 60
```

Required environment variables:

- `SUBSCUT_API_KEY` or `--api-key`

Default base URL:

- `https://subscut.com`

## Install Model

This skill is meant to be published once by Subscut and then installed by users
through the marketplace.

End-user flow:

1. Install the published skill from ClawHub / OpenClaw.
2. Set `SUBSCUT_API_KEY`.
3. Let the agent call the skill when it needs to turn a long-form spoken video
   into short clips.

The skill should not ask users to publish or package anything themselves.

## Agent Workflow

1. Confirm the source is a long-form spoken video.
2. Prefer the CLI wrapper over hand-written `curl`.
3. Keep the request simple unless the user asks for custom clip counts, durations, style, or format.
4. Default `format` to `dynamic` unless the user explicitly wants a title card (`hook_frame`).
5. Return the resulting clip URLs, titles, scores, and timestamps.
6. If the API fails, surface the status and response body clearly.
7. Keep a human in the loop before final publishing if the downstream workflow is public.

## Natural-Language Triggers

Likely user intents that should map to this skill:

- "Turn this podcast into reels"
- "Make shorts from this interview"
- "Repurpose my long video into clips"
- "Find the viral moments in this podcast"
- "Generate YouTube Shorts from this episode"
- "Make clips with a title card at the top"
- "Give me clean subtitle clips"
- "Extract 10 clips from this webinar"

## Notes

- The API route is `POST /podcast-to-clips`.
- `style` maps to the API `style` field. `clip-style` is used as the CLI flag name.
- `format` controls render layout: `dynamic` (default) or `hook_frame`.
- `clip_duration.min` and `clip_duration.max` let callers control clip length window.
- Short videos (≤3 min) are automatically capped at 2 clips regardless of `max_clips`.
- The script is executed through the skill-local `npm` script.
- The skill is intentionally opinionated and keeps the parameter surface small for better agent usage.
- This package is for installation and runtime usage, not for publisher-only deployment steps.
