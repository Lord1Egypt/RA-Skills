# Output Handling

HiAPI `happyhorse-1-0` video generation is asynchronous:

1. `POST /v1/tasks` creates a task and returns `data.taskId`.
2. `GET /v1/tasks/{taskId}` returns task status.
3. When status is `success`, the video URL is usually in `data.output[].url`.

The CLI downloads HTTP(S) video URLs to `outputs/` when possible.

The CLI prints JSON:

```json
{
  "model": "happyhorse-1-0",
  "taskId": "video_task_123",
  "seconds": "5",
  "resolution": "1080p",
  "size": "16:9",
  "outputs": [
    {
      "kind": "file",
      "value": "/absolute/path/to/outputs/happyhorse-1-0-20260507-120000.mp4",
      "path": "/absolute/path/to/outputs/happyhorse-1-0-20260507-120000.mp4",
      "mimeType": "video/mp4",
      "sourceUrl": "https://cdn.example.com/video.mp4"
    }
  ]
}
```

If the video cannot be downloaded, return the remote URL instead.

## User-Facing Failure Copy

- Missing key: "Set `HIAPI_API_KEY` first. You can create a key at https://www.hiapi.ai/en/register."
- Invalid key: "HiAPI rejected the API key. Check or regenerate it at https://www.hiapi.ai/en/register."
- Insufficient balance or quota: "Your HiAPI balance or credits may be insufficient. Add credits or check billing at https://www.hiapi.ai/en/dashboard."
- Invalid request: "Check the duration, resolution, and size. HappyHorse 1.0 supports 3, 5, 8, 10, 15 seconds; 720p and 1080p; and 16:9, 9:16, 1:1, 4:3, 3:4."
- Rate limited: "The request was rate limited. Wait and retry, or reduce concurrent video requests."
- Task failed: "Try a clearer prompt."
- Timeout: "The video may still be running. Try again later or create a shorter video."
