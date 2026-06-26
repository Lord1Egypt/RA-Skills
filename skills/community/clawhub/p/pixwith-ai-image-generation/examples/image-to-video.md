# Example: Image to Video

This example shows the recommended Pixwith MCP flow for an image-conditioned
video request.

## User Intent

Create a short cinematic video from one reference image.

## Recommended Tool Flow

1. `list_models(type="video")`
2. `get_model_schema(model_id)`
3. `upload_image(input)` if the image is local or unreliable as a public URL
4. `get_credits()`
5. `generate(input)`
6. `get_task_result(input)` until terminal state

## Example Sequence

### 1. Discover video models

Call:

```json
{
  "tool": "list_models",
  "arguments": {
    "type": "video"
  }
}
```

Choose a compatible model from `data.video`, for example `2-36`.

### 2. Inspect the chosen model

Call:

```json
{
  "tool": "get_model_schema",
  "arguments": {
    "model_id": "2-36"
  }
}
```

Confirm from `data.input_schema`:

- `image_urls` is allowed
- `max_count` is sufficient
- valid `resolution`, `duration`, and `aspect_ratio` values
- `estimated_time`

### 3. Upload the image if needed

If the user image is local or not reliably public, call:

```json
{
  "tool": "upload_image",
  "arguments": {
    "input": {
      "filename": "reference.jpg",
      "content_type": "image/jpeg",
      "file_size_bytes": 5242880
    }
  }
}
```

Then upload the actual bytes to the returned `upload_url` using the returned
`form_fields`, and keep the returned `data.image_url`.

### 4. Check credits

Call:

```json
{
  "tool": "get_credits",
  "arguments": {}
}
```

Stop if the selected resolution and duration exceed the available balance.

### 5. Create the task

Call:

```json
{
  "tool": "generate",
  "arguments": {
    "input": {
      "prompt": "The subject slowly turns toward camera as wind moves through the hair, cinematic natural light, subtle camera motion, realistic motion",
      "model_id": "2-36",
      "image_urls": [
        "https://cdn.pixwith.ai/path/from-upload-or-other-public-image.jpg"
      ],
      "options": {
        "resolution": "720p",
        "duration": 5,
        "prompt_optimization": true
      }
    }
  }
}
```

Expected success shape:

```json
{
  "code": 1,
  "msg": "success",
  "data": {
    "task_id": "....",
    "estimated_time": 150
  }
}
```

### 6. Poll for completion

Call:

```json
{
  "tool": "get_task_result",
  "arguments": {
    "input": {
      "task_id": "returned-task-id"
    }
  }
}
```

Repeat until:

- `data.status = 2`: completed
- `data.status = 3`: failed

When completed, consume `data.result_urls`.

## Notes

- Do not invent a different model ID for image-to-video mode.
- Pass `image_urls` only if the schema allows them.
- Prefer `upload_image` over fragile third-party image URLs.
- Video jobs are usually more expensive and slower than image jobs, so check
  credits first.
- `min_credits` from `list_models` is only a lower-bound cost hint, not the final price.
