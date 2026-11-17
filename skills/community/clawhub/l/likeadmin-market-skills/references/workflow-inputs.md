# Workflow Inputs

`workflow-runner.mjs` runs deterministic portions of a selected recipe. The agent must still discover tenant availability, compare materially different enabled choices, and ask for any required model or Smart Clip template choice before invoking it.

## Input Rules

- Every media value accepts a public `http(s)` URL, local path, or `file://` URL. A local value is uploaded through `/upload` only when the user has explicitly authorized that transfer; set `confirm_local_upload: true` in the input only after that confirmation.
- Use `--state <file>` to persist completed node IDs and URLs. State does not contain `api_key`.
- Never reuse a `voice_tts` ID as a `music_generation` persona or voice ID.

## Recipes

| Recipe | Required input fields | Result |
| --- | --- | --- |
| `clone-voice` | `reference_audio`, `voice_title` | `voice_id` |
| `tts` | `text`, optional `reference_id` | `audio_url` |
| `lipsync` | `audio`, `source_video` | task and video result |
| `clone-voice-lipsync` | `reference_audio`, `voice_title`, `text`, `source_video` | cloned voice, audio, talking video |
| `image-avatar` | `portrait_image`, `driving_audio` | `video_url` |
| `realman-smart-clip` | `source_video`, `style_id` | task and video result |
| `avatar-smart-clip` | `portrait_image`, `driving_audio`, `style_id` | avatar then edited video |
| `material-smart-clip` | `audio`, `style_id`, `materials[]` | task and video result |
| `news-smart-clip` | `title`, `style_id`, `materials[]` | task and video result |

For `materials[]`, use objects such as `{ "type": "image", "file": "./product.png" }` or `{ "type": "video", "file": "https://example.com/demo.mp4" }`.

## Clone Voice To Talking Video

```json
{
  "confirm_local_upload": true,
  "reference_audio": "./reference.wav",
  "voice_title": "Brand narrator",
  "text": "Welcome to our product launch.",
  "source_video": "./presenter.mp4",
  "tts_options": { "format": "mp3" },
  "lipsync_options": { "model": "xiaojiayu2.0" },
  "poll_timeout_seconds": 900
}
```

Run:

```bash
node scripts/workflow-runner.mjs clone-voice-lipsync input.json --state output/state.json
```

`style_id` is intentionally never auto-selected by the runner. Obtain it from `smart_clip/template?scene=realMan` and let the user choose among materially different templates.
