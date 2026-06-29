# HiAPI HappyHorse 1.0 Video API

## Endpoint

`happyhorse-1-0` uses HiAPI's unified async task API:

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
  "model": "happyhorse-1-0",
  "input": {
    "prompt": "A wuxia swordswoman leaps across temple rooftops at dusk",
    "duration": 5,
    "resolution": "1080p",
    "aspect_ratio": "16:9",
    "seed": 12345
  }
}
```

## Parameters

| Parameter | Required | Notes |
| --- | --- | --- |
| `model` | yes | Must be `happyhorse-1-0`. |
| `input.prompt` | yes | Text video instruction. Describe subject, motion, camera movement, style, and audio atmosphere. |
| `input.duration` | no | Integer seconds from `3` to `15`. Defaults to `5`. |
| `input.resolution` | no | `720p` or `1080p`. Defaults to `1080p`. |
| `input.aspect_ratio` | no | Aspect ratio value: `16:9`, `9:16`, `1:1`, `4:3`, or `3:4`. Defaults to `16:9`. |
| `input.seed` | no | Integer from `0` to `2147483647` for reproducible generation. Omit when not needed. |

HappyHorse 1.0 is text-to-video. It does not use image inputs. The CLI accepts `--seconds`, `--size`, and `--seed` as user-facing aliases for `input.duration`, `input.aspect_ratio`, and `input.seed`.
