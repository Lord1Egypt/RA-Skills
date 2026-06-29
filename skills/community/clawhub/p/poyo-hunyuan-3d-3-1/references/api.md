# PoYo Hunyuan 3D v3.1 API Reference

## Endpoint

- Submit task: `POST https://api.poyo.ai/api/generate/submit`
- 3D status query: `GET https://api.poyo.ai/api/generate/3d-status/{task_id}`
- Source docs: <https://docs.poyo.ai/api-manual/3d-series/hunyuan-3d-3-1>
- Model page: <https://poyo.ai/models/hunyuan-3d-3-1>

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

- `hunyuan-3d/v3.1/pro/text-to-3d`: Pro text-to-3D.
- `hunyuan-3d/v3.1/pro/image-to-3d`: Pro image-to-3D.
- `hunyuan-3d/v3.1/rapid/text-to-3d`: Rapid text-to-3D.
- `hunyuan-3d/v3.1/rapid/image-to-3d`: Rapid image-to-3D.

## Request Schema

Top-level fields:

- `model` string, required
- `callback_url` string URI, optional
- `input` object, required

Common `input` fields:

- `prompt` string, required for text-to-3D
- `image_urls` string array, required for image-to-3D, exactly one image URL
- `generate_type` string, optional for Pro models: `Normal` or `Geometry`
- `enable_pbr` boolean, optional when supported
- `face_count` integer, optional for Pro models, 40000 to 1500000
- `enable_geometry` boolean, optional for Rapid models
- `back_image_url`, `left_image_url`, `right_image_url`, `top_image_url`, `bottom_image_url`, `left_front_image_url`, and `right_front_image_url` strings, optional for Pro image-to-3D when aligned object views are available

Always verify current field support in the PoYo docs before relying on model-specific options.

## Pro Text-to-3D Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "hunyuan-3d/v3.1/pro/text-to-3d",
    "input": {
      "prompt": "A detailed sci-fi cargo drone with compact landing legs, clean panel lines, and game-ready proportions",
      "generate_type": "Normal",
      "enable_pbr": true,
      "face_count": 500000
    }
  }'
```

## Pro Image-to-3D Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "hunyuan-3d/v3.1/pro/image-to-3d",
    "callback_url": "https://example.com/api/poyo/webhook",
    "input": {
      "image_urls": [
        "https://example.com/object-front.png"
      ],
      "left_image_url": "https://example.com/object-left.png",
      "right_image_url": "https://example.com/object-right.png",
      "generate_type": "Normal",
      "enable_pbr": true,
      "face_count": 500000
    }
  }'
```

## Rapid Text-to-3D Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "hunyuan-3d/v3.1/rapid/text-to-3d",
    "input": {
      "prompt": "A rustic wooden treasure chest with metal bands, simple readable silhouette",
      "enable_pbr": false
    }
  }'
```

## Rapid Image-to-3D Example

```bash
curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer YOUR_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "hunyuan-3d/v3.1/rapid/image-to-3d",
    "input": {
      "image_urls": [
        "https://example.com/object-front.png"
      ],
      "enable_geometry": false,
      "enable_pbr": false
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
    "created_time": "2026-06-26T08:00:00"
  }
}
```

## Result Notes

- Save `data.task_id` immediately after submission.
- Poll the 3D status endpoint for local tests.
- Use `callback_url` for production asset pipelines and long-running workflows.
- Returned files may include model assets, previews, thumbnails, or material files when available.
- Store final asset URLs only after the task reaches a terminal success state.

## Practical Guidance

- Use Pro when the user needs higher-control output or extra view guidance.
- Use Rapid when the user wants a simpler text-to-3D or image-to-3D path.
- Use extra view URL fields only when images show the same object from clear aligned angles.
- Keep prompts object-focused and avoid background-heavy descriptions for asset generation.
- Avoid logging API keys, private prompts, private source image URLs, generated asset URLs, or callback URLs.
