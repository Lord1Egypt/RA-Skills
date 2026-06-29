# HiAPI Seedance 2.0 Video API

## Endpoint

`seedance-2-0` uses HiAPI's unified async task API:

```text
POST https://api.hiapi.ai/v1/tasks
GET https://api.hiapi.ai/v1/tasks/{taskId}
```

Set `HIAPI_BASE_URL` to override the host.

## Authentication

Send the user's HiAPI key as a bearer token:

```http
Authorization: Bearer $HIAPI_API_KEY
Content-Type: application/json
```

Do not print API keys in logs or final answers.

If the user does not have a key, send them to:

```text
https://www.hiapi.ai/en/register
```

If generation fails because of balance, credits, quota, or payment status, send them to:

```text
https://www.hiapi.ai/en/dashboard
https://www.hiapi.ai/en/pricing
```

## Request Body

Text-to-video:

```json
{
  "model": "seedance-2-0",
  "input": {
    "prompt": "A cinematic ocean cliff shot at golden hour",
    "duration": 5,
    "resolution": "720p",
    "aspect_ratio": "16:9"
  }
}
```

Image-to-video:

```json
{
  "model": "seedance-2-0",
  "input": {
    "prompt": "The product photo comes alive with soft camera movement",
    "first_frame_url": "https://example.com/product.jpg",
    "duration": 5,
    "resolution": "720p",
    "aspect_ratio": "16:9"
  }
}
```

First+last-frame image-to-video:

```json
{
  "model": "seedance-2-0",
  "input": {
    "prompt": "Move from the first frame to the final hero frame",
    "first_frame_url": "asset://first-frame",
    "last_frame_url": "asset://last-frame",
    "duration": 5,
    "resolution": "720p",
    "aspect_ratio": "16:9"
  }
}
```

Multimodal reference mode:

```json
{
  "model": "seedance-2-0",
  "input": {
    "prompt": "Use the reference images, motion video, and audio mood to create a product spot",
    "reference_image_urls": ["asset://image-1"],
    "reference_video_urls": ["asset://video-1"],
    "reference_audio_urls": ["asset://audio-1"],
    "duration": 5,
    "resolution": "720p",
    "aspect_ratio": "16:9"
  }
}
```

## Parameters

| Parameter | Required | Notes |
| --- | --- | --- |
| `model` | yes | Must be `seedance-2-0`. |
| `input.prompt` | yes | Text video instruction. Describe the subject, motion, camera movement, mood, and sound atmosphere. |
| `input.duration` | no | Integer seconds from `4` to `15`. Defaults to `5`. |
| `input.resolution` | no | `480p`, `720p`, or `1080p`. Defaults to `720p`. |
| `input.aspect_ratio` | no | `16:9`, `9:16`, `1:1`, `4:3`, `3:4`, `21:9`, or `adaptive`. Defaults to `16:9`. |
| `input.first_frame_url` | no | Public image URL, data URI, or `asset://` id for first-frame image-to-video. |
| `input.last_frame_url` | no | Public image URL, data URI, or `asset://` id for first+last-frame image-to-video. Requires `input.first_frame_url`. |
| `input.reference_image_urls` | no | Multimodal reference images. Combined count with first/last frames must not exceed 9 images. Do not mix with first/last-frame fields. |
| `input.reference_video_urls` | no | Multimodal reference videos. At most 3; each 2-15 seconds; total duration at most 15 seconds. Do not mix with first/last-frame fields. |
| `input.reference_audio_urls` | no | Multimodal reference audio clips. At most 3; each 2-15 seconds; total duration at most 15 seconds. Do not mix with first/last-frame fields. |
| `input.generate_audio` | no | Boolean. API default is `true` (synchronized audio on). The CLI omits this field unless `--generate-audio` or `--no-audio` is passed. |
| `input.return_last_frame` | no | Boolean. Return the last frame of the generated video when supported. |
| `input.web_search` | no | Boolean. Enable web search when supported. |
| `input.nsfw_checker` | no | Boolean. Enable content checking when supported. |
| `input.seed` | no | Integer from `0` to `2147483647` for reproducible generation. Omit for a random seed. |

Seedance 2.0 supports text-to-video without media. Three media modes are mutually exclusive: first-frame image-to-video, first+last-frame image-to-video, and multimodal reference generation. The CLI accepts `--input-reference` as a legacy alias for `--first-frame-url`.
