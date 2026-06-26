# Example: Text to Image

This example shows the recommended Pixwith MCP flow for a plain text-to-image
request.

## User Intent

Create a product-style hero image from a text prompt.

## Recommended Tool Flow

1. `list_models(type="image")`
2. `get_model_schema(model_id)`
3. `get_credits()`
4. `generate(input)`
5. `get_task_result(input)` until terminal state

## Example Sequence

### 1. Discover image models

Call:

```json
{
  "tool": "list_models",
  "arguments": {
    "type": "image"
  }
}
```

Choose a model from the returned `data.image` list, for example `0-41`.

### 2. Inspect the chosen model

Call:

```json
{
  "tool": "get_model_schema",
  "arguments": {
    "model_id": "0-41"
  }
}
```

Read from `data.input_schema`:

- whether prompt is required
- whether `image_urls` is optional or disallowed
- valid `options`
- allowed enum values
- `estimated_time`

### 3. Check credits

Call:

```json
{
  "tool": "get_credits",
  "arguments": {}
}
```

If credits are too low for the selected schema, stop and ask the user to
recharge.

### 4. Create the generation task

Call:

```json
{
  "tool": "generate",
  "arguments": {
    "input": {
      "prompt": "A clean premium skincare product hero shot on a reflective surface, soft daylight, subtle water droplets, commercial photography, high detail",
      "model_id": "0-41",
      "image_urls": [],
      "options": {
        "aspect_ratio": "1:1",
        "resolution": "1K",
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
    "estimated_time": 50
  }
}
```

### 5. Poll for completion

Wait about 75% of `estimated_time`, then call:

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

When completed, read `data.result_urls`.

## Notes

- Do not guess valid option keys. Use `get_model_schema`.
- Do not treat `generate` as a synchronous image response.
- Always inspect the outer `code` before trusting `data`.
- `min_credits` from `list_models` is only a lower-bound cost hint, not the final price.
