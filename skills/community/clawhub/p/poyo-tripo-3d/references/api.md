# PoYo Tripo3D API Reference

## Endpoint

- Submit task: `POST https://api.poyo.ai/api/generate/submit`
- 3D status query: `GET https://api.poyo.ai/api/generate/3d-status/{task_id}`
- H3.1 source docs: <https://docs.poyo.ai/api-manual/3d-series/tripo-h31-3d>
- P1 source docs: <https://docs.poyo.ai/api-manual/3d-series/tripo-p1-3d>
- H3.1 model page: <https://poyo.ai/models/tripo-h31-3d>
- P1 model page: <https://poyo.ai/models/tripo-p1-3d>

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

- `tripo3d-h3.1-text-to-3d`: high-detail text-to-3D.
- `tripo3d-h3.1-image-to-3d`: high-detail image-to-3D.
- `tripo3d-h3.1-multiview-to-3d`: high-detail multiview-to-3D.
- `tripo3d-p1-text-to-3d`: lightweight text-to-3D.
- `tripo3d-p1-image-to-3d`: lightweight image-to-3D.

## Request Schema

Top-level fields:

- `model` string, required
- `callback_url` string URI, optional
- `input` object, required

Common `input` fields:

- `prompt` string, required for text-to-3D
- `image_urls` string array, required for image-based workflows
- `negative_prompt` string, optional for H3.1 text-to-3D
- `face_limit` integer, optional
- `texture` boolean, optional
- `pbr` boolean, optional when textures are enabled
- `texture_quality` string, optional: `standard` or `detailed`
- `geometry_quality` string, optional: `standard` or `detailed`
- `auto_size` boolean, optional
- `quad` boolean, optional
- `model_seed`, `image_seed`, and `texture_seed` integers, optional

Always verify current field support in the PoYo docs before relying on model-specific options.

## H3.1 Text-to-3D Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "tripo3d-h3.1-text-to-3d",
    "input": {
      "prompt": "A compact sci-fi desk lamp with a matte white shell, blue accent light, rounded industrial design, product asset style",
      "texture": true,
      "texture_quality": "standard",
      "geometry_quality": "standard",
      "quad": false
    }
  }'
```

## H3.1 Multiview-to-3D Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "tripo3d-h3.1-multiview-to-3d",
    "callback_url": "https://example.com/api/poyo/webhook",
    "input": {
      "image_urls": [
        "https://example.com/object-front.png",
        "https://example.com/object-side.png",
        "https://example.com/object-back.png"
      ],
      "texture": true,
      "pbr": true,
      "texture_quality": "standard",
      "geometry_quality": "standard"
    }
  }'
```

## P1 Text-to-3D Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "tripo3d-p1-text-to-3d",
    "input": {
      "prompt": "A clean low-poly delivery robot asset, friendly proportions, simple readable shapes",
      "texture": true,
      "face_limit": 12000
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
    "created_time": "2026-05-23T08:00:00"
  }
}
```

## Result Notes

- Save `data.task_id` immediately after submission.
- Poll the 3D status endpoint for local tests.
- Use `callback_url` for production asset pipelines and long-running workflows.
- Returned files may include a GLB model, thumbnail, base model, or PBR model files when available.
- Store final asset URLs only after the task reaches a terminal success state.

## Practical Guidance

- Use H3.1 when the user needs higher-detail models or multiview support.
- Use P1 when the user wants lightweight, clean-mesh assets.
- Use multiview only when images show the same object from different angles.
- Keep prompts object-focused and avoid background-heavy descriptions for asset generation.
- Avoid logging API keys, private prompts, private source image URLs, generated asset URLs, or callback URLs.
