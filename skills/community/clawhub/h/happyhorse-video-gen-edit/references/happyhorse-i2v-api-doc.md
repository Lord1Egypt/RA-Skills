# HappyHorse Image to Video API Documentation (happyhorse-1.0-i2v)

## Overview

Generate video from a first-frame image with optional text prompt guidance. The output video aspect ratio automatically follows the input image.

## API Endpoint

```
POST https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis
```

## Request Headers

| Header | Required | Description |
| --- | --- | --- |
| Content-Type | Yes | Must be `application/json` |
| Authorization | Yes | `Bearer {API_KEY}` |
| X-DashScope-Async | Yes | Must be `enable` for async processing |

## Request Body

```json
{
  "model": "happyhorse-1.0-i2v",
  "input": {
    "prompt": "一只猫在草地上奔跑",
    "media": [
      {
        "type": "first_frame",
        "url": "https://example.com/first.png"
      }
    ]
  },
  "parameters": {
    "resolution": "720P",
    "duration": 5,
    "watermark": true,
    "seed": 12345
  }
}
```

### Input Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| prompt | string | No | Text prompt for video generation. Max 5000 non-Chinese chars or 2500 Chinese chars. |
| media | array | Yes | Media list. Must contain exactly 1 `first_frame` element. |

### Media Element

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| type | string | Yes | Must be `first_frame` |
| url | string | Yes | Image URL (HTTP/HTTPS). Format: JPEG/JPG/PNG/WEBP. Min resolution: 300px per side. Aspect ratio: 1:2.5~2.5:1. Max 10MB. |

### Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| resolution | string | No | `720P` or `1080P` (default: 1080P). Output aspect ratio follows input image automatically. |
| duration | integer | No | Video duration in seconds, 3-15 (default: 5) |
| watermark | boolean | No | Add "Happy Horse" watermark (default: true) |
| seed | integer | No | Random seed [0, 2147483647] for reproducibility |

**Note:** There is no `ratio` parameter. The output video aspect ratio automatically follows the input first-frame image.

## Response

### Task Creation Response

```json
{
  "output": {
    "task_status": "PENDING",
    "task_id": "0385dc79-5ff8-4d82-bcb6-xxxxxx"
  },
  "request_id": "4909100c-7b5a-9f92-bfe5-xxxxxx"
}
```

### Task Query Endpoint

```
GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}
```

### Success Response

```json
{
  "request_id": "8ae698ba-df2d-966c-abcf-xxxxxx",
  "output": {
    "task_id": "e56d806f-76f9-4037-aefa-xxxxxx",
    "task_status": "SUCCEEDED",
    "submit_time": "2026-04-20 19:33:50.425",
    "scheduled_time": "2026-04-20 19:33:50.463",
    "end_time": "2026-04-20 19:35:34.216",
    "orig_prompt": "一只猫在草地上奔跑",
    "video_url": "https://dashscope-result.oss-cn-beijing.aliyuncs.com/xxx.mp4?Expires=xxx"
  },
  "usage": {
    "duration": 5,
    "input_video_duration": 0,
    "output_video_duration": 5,
    "video_count": 1,
    "SR": 720
  }
}
```

## Task Status Values

| Status | Description |
| --- | --- |
| PENDING | Task queued |
| RUNNING | Task processing |
| SUCCEEDED | Task completed successfully |
| FAILED | Task execution failed |
| CANCELED | Task canceled |
| UNKNOWN | Task not found or expired |

## Important Notes

- Task ID validity: 24 hours
- Video URL validity: 24 hours (download immediately)
- Output aspect ratio follows input image (no ratio parameter)
- Video frame rate: 24fps, format: MP4 (H.264)
- Polling interval: Recommended 15 seconds
