# PoYo Meshy 6 3D API Reference

## Endpoint

- Submit task: `POST https://api.poyo.ai/api/generate/submit`
- Status query: `GET https://api.poyo.ai/api/generate/status/{task_id}`
- Source docs: <https://docs.poyo.ai/api-manual/3d-series/meshy-6-3d>
- Model page: <https://poyo.ai/models/meshy-6-3d>
- Main examples repository: <https://github.com/PoyoAPI/poyo-examples>

## Auth

Send:

```http
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json
```

Get API keys from <https://poyo.ai/dashboard/api-key>.

Recommended skill env var:

- `POYO_API_KEY`

## Models

- `meshy-6-text-to-3d`: prompt-to-3D asset generation
- `meshy-6-image-to-3d`: single image-to-3D asset generation
- `meshy-6-multi-image-to-3d`: multi-image or multi-view 3D asset generation

## Request Schema

Top-level fields:

- `model` string, required
- `callback_url` string URI, optional
- `input` object, required

Common `input` fields:

- `prompt` string, required for text-to-3D
- `image_urls` string array, required for image-based workflows
- `mode` string, optional
- `topology` string, optional
- `target_polycount` number, optional
- `should_remesh` boolean, optional
- `symmetry_mode` string, optional
- `should_texture` boolean, optional
- `enable_pbr` boolean, optional
- `texture_prompt` string, optional
- `texture_image_url` string, optional
- `enable_rigging` boolean, optional
- `enable_animation` boolean, optional
- `enable_safety_checker` boolean, optional
- `seed` number, optional

Always verify current field support in the PoYo docs before relying on model-specific options.

## Text-to-3D Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "meshy-6-text-to-3d",
    "input": {
      "prompt": "A compact futuristic desk lamp with rounded corners, matte white body, small blue accent light, product design style"
    }
  }'
```

## Image-to-3D Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "meshy-6-image-to-3d",
    "callback_url": "https://example.com/api/poyo/webhook",
    "input": {
      "image_urls": [
        "https://example.com/source-object.png"
      ],
      "should_texture": true
    }
  }'
```

## Multi-Image-to-3D Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "meshy-6-multi-image-to-3d",
    "input": {
      "image_urls": [
        "https://example.com/front.png",
        "https://example.com/side.png",
        "https://example.com/back.png"
      ],
      "should_texture": true
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
    "created_time": "2026-05-19T08:00:00"
  }
}
```

## Polling Notes

- Save `data.task_id` immediately after submission.
- Poll the status endpoint for local tests.
- Use `callback_url` for production asset pipelines and long-running workflows.
- Returned files may include preview images, model files, textures, rigging files, or animation files.
- Store final asset URLs only after the task reaches a terminal success state.

## Practical Guidance

- Start with `meshy-6-text-to-3d` when the user only has a prompt.
- Use `meshy-6-image-to-3d` when one source image defines the object.
- Use `meshy-6-multi-image-to-3d` when multiple views should guide geometry.
- Keep prompts concise and object-focused.
- Avoid logging API keys, private prompts, private source image URLs, generated asset URLs, or callback URLs.
