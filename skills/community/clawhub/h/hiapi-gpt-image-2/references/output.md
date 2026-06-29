# Output Handling

HiAPI `gpt-image-2` image generation is asynchronous:

```text
1. POST /v1/tasks creates an image task and returns data.taskId.
2. GET /v1/tasks/{taskId} returns task status.
3. When status is success, image assets are in data.output[].
```

Common task output:

```json
{
  "data": {
    "taskId": "task_123",
    "status": "success",
    "output": [
      {
        "type": "image",
        "url": "https://cdn.example.com/image.png"
      }
    ]
  }
}
```

The CLI extracts image targets from `data.output[]`:

- `https://...` values are returned as URLs.
- `data:image/...;base64,...` values are saved under `outputs/`.

The CLI prints JSON:

```json
{
  "model": "gpt-image-2",
  "taskId": "task_123",
  "aspectRatio": "16:9",
  "resolution": "1K",
  "outputs": [
    {
      "kind": "file",
      "path": "/absolute/path/to/outputs/gpt-image-2-20260429-154500-1.png"
    }
  ]
}
```

If no image can be extracted after a successful task, treat the run as failed and show the returned task summary.

## User-Facing Failure Copy

- Missing key: "Set `HIAPI_API_KEY` first. You can create a key at https://www.hiapi.ai/en/register."
- Invalid key: "HiAPI rejected the API key. Check or regenerate it at https://www.hiapi.ai/en/register."
- Insufficient balance: "Your HiAPI balance or credits may be insufficient. Add credits or check billing at https://www.hiapi.ai/en/dashboard."
- Rate limited: "The request was rate limited. Wait and retry, or reduce concurrent image requests."
- Safety policy: "The prompt may have triggered a safety policy. Revise the prompt and try again."
