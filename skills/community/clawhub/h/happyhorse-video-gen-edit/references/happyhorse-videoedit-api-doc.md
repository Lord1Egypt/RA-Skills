# HappyHorse Video Edit API Documentation (happyhorse-1.0-video-edit)

## Overview

Edit existing videos with text instructions and optional reference images. Supports style transfer, local replacement, and other editing tasks.

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
  "model": "happyhorse-1.0-video-edit",
  "input": {
    "prompt": "让视频中的马头人身角色穿上图片中的条纹毛衣",
    "media": [
      {
        "type": "video",
        "url": "https://example.com/original.mp4"
      },
      {
        "type": "reference_image",
        "url": "https://example.com/clothes.webp"
      }
    ]
  },
  "parameters": {
    "resolution": "720P",
    "watermark": true,
    "audio_setting": "auto",
    "seed": 12345
  }
}
```

### Input Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| prompt | string | Yes | Editing instruction. Describes the edit intent (style transfer, local replacement, etc.). Max 5000 non-Chinese chars or 2500 Chinese chars. |
| media | array | Yes | Media list. Must contain exactly 1 `video` element. Optionally 0-5 `reference_image` elements. |

### Media Elements

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| type | string | Yes | `video` (required, exactly 1) or `reference_image` (optional, 0-5) |
| url | string | Yes | Media URL (HTTP/HTTPS) |

**Video constraints:**
- Format: MP4, MOV (H.264 recommended)
- Duration: 3-60 seconds input. Output: 3-15 seconds. If input > 15s, auto-truncated to first 15s.
- Resolution: Long side <= 2160px, short side >= 320px
- Aspect ratio: 1:2.5 ~ 2.5:1
- File size: <= 100MB
- Frame rate: > 8fps

**Reference image constraints:**
- Format: JPEG/JPG/PNG/WEBP
- Resolution: Width and height >= 300px
- Aspect ratio: 1:2.5 ~ 2.5:1
- File size: <= 10MB

### Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| resolution | string | No | `720P` or `1080P` (default: 1080P) |
| watermark | boolean | No | Add "Happy Horse" watermark (default: true) |
| audio_setting | string | No | `auto` (default, model controls) or `origin` (keep original audio) |
| seed | integer | No | Random seed [0, 2147483647] for reproducibility |

**Note:** There is no `ratio` or `duration` parameter. Output aspect ratio and duration follow the input video.

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
  "request_id": "c11018a8-3f83-9591-a636-xxxxxx",
  "output": {
    "task_id": "051c7b40-b2c5-4341-aee4-xxxxxx",
    "task_status": "SUCCEEDED",
    "submit_time": "2026-04-26 14:13:14.373",
    "scheduled_time": "2026-04-26 14:13:14.419",
    "end_time": "2026-04-26 14:14:13.679",
    "orig_prompt": "让视频中的马头人身角色穿上图片中的条纹毛衣",
    "video_url": "https://dashscope-result.oss-cn-beijing.aliyuncs.com/xxxx.mp4"
  },
  "usage": {
    "duration": 13.24,
    "input_video_duration": 6.62,
    "output_video_duration": 6.62,
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
- Input video: 3-60s, output auto-truncated to max 15s
- Output aspect ratio follows input video (no ratio parameter)
- Output duration follows input video (no duration parameter)
- Polling interval: Recommended 15 seconds
