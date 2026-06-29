# PoYo ElevenLabs Music API Reference

## Endpoint

- Submit task: `POST https://api.poyo.ai/api/generate/submit`
- Task status: use the standard PoYo task status endpoint documented by PoYo.
- Source docs: <https://docs.poyo.ai/api-manual/music-series/elevenlabs-music>
- Model page: <https://poyo.ai/models/elevenlabs-music>

## Auth

Send:

```http
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json
```

Get API keys from <https://poyo.ai/dashboard/api-key>.

Recommended skill env var:

- `POYO_API_KEY`

## Model

- `elevenlabs-music`: music generation with text and composition-plan controls.

## Request Schema

Top-level fields:

- `model` string, required
- `callback_url` string URI, optional
- `input` object, required

Supported `input` paths:

- `text` string, use for a single natural-language music brief. Do not send with `composition_plan`.
- `composition_plan` object, use for structured section control. Do not send with `text`.

Text path fields:

- `text` string, required for this path
- `duration` number of seconds, optional, only valid with `text`
- `is_instrumental` boolean, optional, only valid with `text`
- `output_format` string, optional

Composition-plan fields:

- `positive_global_styles` string array
- `negative_global_styles` string array
- `sections` non-empty array
- `respect_sections_durations` boolean, optional, only valid with `composition_plan`
- `output_format` string, optional

Each section may include:

- `section_name` string
- `positive_local_styles` string array
- `negative_local_styles` string array
- `duration` number of seconds
- `lines` string array for lyric lines

Common output formats include `mp3_44100_128`, `mp3_44100_192`, `opus_48000_128`, `pcm_44100`, `ulaw_8000`, and `alaw_8000`. Verify the current full list in the PoYo docs before relying on a specific format.

## Text Brief Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "elevenlabs-music",
    "callback_url": "https://example.com/api/poyo/webhook",
    "input": {
      "text": "Create a bright electronic background track for a product walkthrough, clean drums, warm synths, no vocals",
      "duration": 45,
      "is_instrumental": true,
      "output_format": "mp3_44100_128"
    }
  }'
```

## Composition Plan Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "elevenlabs-music",
    "input": {
      "composition_plan": {
        "positive_global_styles": ["cinematic", "warm synths", "steady percussion"],
        "negative_global_styles": ["harsh noise", "distorted vocals"],
        "sections": [
          {
            "section_name": "Intro",
            "positive_local_styles": ["soft pads", "simple pulse"],
            "negative_local_styles": ["busy drums"],
            "duration": 20,
            "lines": []
          },
          {
            "section_name": "Main",
            "positive_local_styles": ["clear beat", "uplifting melody"],
            "negative_local_styles": ["muddy bass"],
            "duration": 35,
            "lines": []
          }
        ]
      },
      "respect_sections_durations": true,
      "output_format": "opus_48000_128"
    }
  }'
```

## Typical Submit Response

```json
{
  "code": 200,
  "data": {
    "task_id": "task_unified_example",
    "status": "not_started",
    "created_time": "2026-06-29T08:00:00"
  }
}
```

## Result Retrieval Notes

- Save `data.task_id` immediately after submission.
- Use the standard PoYo task status endpoint for generated music results.
- Use `callback_url` for production queues and long-running user workflows.
- Treat `finished` and `failed` as terminal states when receiving callbacks.
- Generated music is returned in task `files` with an audio file type when the task succeeds.

## Practical Guidance

- Start with `text` for quick generation.
- Use `composition_plan` when the user needs section names, local styles, lyrics, or timing control.
- Do not send `text` and `composition_plan` together.
- Keep private lyrics, prompts, callback URLs, task ids, and generated audio URLs out of logs unless explicitly allowed by the product policy.
