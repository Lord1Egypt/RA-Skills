# HappyHorse Reference to Video API Documentation (happyhorse-1.0-r2v)

## Overview

Generate video from reference images. Supports multiple reference images as character/object sources, fusing them into a coherent video guided by text prompts. Use "character1", "character2", etc. in the prompt to reference images in order.

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
  "model": "happyhorse-1.0-r2v",
  "input": {
    "prompt": "身着红色旗袍的女性character1，镜头先以侧面中景勾勒旗袍修身剪裁与S型曲线，随即切换至低角度仰拍，捕捉她轻抬玉手展开折扇character2时流苏耳坠character3随头部转动轻盈摆动的细节。",
    "media": [
      {
        "type": "reference_image",
        "url": "https://example.com/girl.jpg"
      },
      {
        "type": "reference_image",
        "url": "https://example.com/fan.jpg"
      },
      {
        "type": "reference_image",
        "url": "https://example.com/earrings.jpg"
      }
    ]
  },
  "parameters": {
    "resolution": "720P",
    "ratio": "16:9",
    "duration": 5,
    "watermark": true,
    "seed": 12345
  }
}
```

### Input Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| prompt | string | Yes | Text prompt with character references. Use "character1", "character2", etc. to reference images in order. Max 5000 non-Chinese chars or 2500 Chinese chars. |
| media | array | Yes | Reference image list. 1-9 images of type `reference_image`. |

### Media Element

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| type | string | Yes | Must be `reference_image` |
| url | string | Yes | Image URL (HTTP/HTTPS). Format: JPEG/JPG/PNG/WEBP. Short side >= 400px, recommend 720P+. Max 10MB. |

**Note:** The 1st image in media array corresponds to `character1`, the 2nd to `character2`, and so on.

### Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| resolution | string | No | `720P` or `1080P` (default: 1080P) |
| ratio | string | No | Aspect ratio: `16:9` (default), `9:16`, `1:1`, `4:3`, `3:4` |
| duration | integer | No | Video duration in seconds, 3-15 (default: 5) |
| watermark | boolean | No | Add "Happy Horse" watermark (default: true) |
| seed | integer | No | Random seed [0, 2147483647] for reproducibility |

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
  "request_id": "35137489-2862-96cb-b6f2-xxxxxx",
  "output": {
    "task_id": "1469cfc3-3004-4d9e-ab10-xxxxxx",
    "task_status": "SUCCEEDED",
    "submit_time": "2026-04-25 15:03:25.848",
    "scheduled_time": "2026-04-25 15:03:25.884",
    "end_time": "2026-04-25 15:04:05.882",
    "orig_prompt": "身着红色旗袍的女性character1...",
    "video_url": "https://dashscope-result.oss-cn-beijing.aliyuncs.com/xxxx.mp4"
  },
  "usage": {
    "duration": 5,
    "input_video_duration": 0,
    "output_video_duration": 5,
    "video_count": 1,
    "SR": 720,
    "ratio": "16:9"
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
- Reference images: 1-9 images, use "character1/character2/..." in prompt to reference them
- Avoid low-resolution, blurry, or heavily compressed images for best results
- Polling interval: Recommended 15 seconds
