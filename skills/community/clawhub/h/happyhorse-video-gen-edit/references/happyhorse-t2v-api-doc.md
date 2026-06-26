# HappyHorse Text to Video API Documentation (happyhorse-1.0-t2v)

## Overview

Generate videos from text prompts. Produces physically realistic and smoothly moving video content.

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
  "model": "happyhorse-1.0-t2v",
  "input": {
    "prompt": "一座由硬纸板和瓶盖搭建的微型城市，在夜晚焕发出生机。一列硬纸板火车缓缓驶过，小灯点缀其间，照亮前路。"
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
| prompt | string | Yes | Text prompt for video generation. Max 5000 non-Chinese chars or 2500 Chinese chars. |

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
  "request_id": "99243b47-ec5f-9413-9993-xxxxxx",
  "output": {
    "task_id": "4673458e-28be-4a05-bf2a-xxxxxx",
    "task_status": "SUCCEEDED",
    "submit_time": "2026-04-20 17:55:17.075",
    "scheduled_time": "2026-04-20 17:55:17.129",
    "end_time": "2026-04-20 17:56:36.658",
    "orig_prompt": "一座由硬纸板和瓶盖搭建的微型城市...",
    "video_url": "https://dashscope-result.oss-cn-beijing.aliyuncs.com/xxx.mp4?Expires=xxx"
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
- Billing: resolution (1080P > 720P) × duration (seconds)
- Polling interval: Recommended 15 seconds
