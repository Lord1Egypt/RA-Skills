# Payload Rules

## Do Not Let Models Invent Structure

Weak or strong models may infer the correct task type but still construct the wrong payload.

Therefore:

- models may decide **what the user wants**
- models may **not** decide final payload field placement

## Critical Payload Rules

### `src_img_url`

- only image URLs
- no video URLs
- no audio URLs

### `src_video`

- `duration` must be `int`
- `cover` must be non-empty
- `fps` is validation-only and should not be sent in final create payload

### `src_audio`

- `duration` must be `int`

### `parameters[0].parameters`

- `prompt`: required
- `n`: required integer
- `cast`: required object with `points` and `attribute_id`
- `duration`: integer
- `audio`: boolean
- `aspect_ratio`: string
- `resolution`: string

## Failure Policy

If the payload cannot be built to these rules, stop before create-task.
