# Create Task Contract

This document defines the canonical create-task payload built by `scripts/ima_video_create.py`.

## Rule

OpenClaw must **not** build `/open/v1/tasks/create` payloads directly.

See also: [`credit-rules.md`](credit-rules.md)

The script is the only execution kernel allowed to:

- select `attribute_id`
- select `credit`
- build `src_img_url`
- build `src_image`
- build `src_video`
- build `src_audio`
- normalize parameter types

## Top-Level Payload

```json
{
  "task_type": "reference_image_to_video",
  "enable_multi_model": false,
  "parameters": [ ... ],
  "src_img_url": [ ...images only... ],
  "src_image": [ ... ],
  "src_video": [ ... ],
  "src_audio": [ ... ]
}
```

## Field Rules

| Field | Source | Rule |
|---|---|---|
| `task_type` | script task-type inference | Must match validated task intent |
| `enable_multi_model` | script constant | `false` |
| `parameters[0].attribute_id` | matched credit rule | Must come from product list / rule match |
| `parameters[0].credit` | matched credit rule | Must match `attribute_id` |
| `parameters[0].parameters.input_images` | prepared media input URLs | May include image/video/audio URLs in reference mode |
| `src_img_url` | `src_image` only | Images only; never include video/audio URLs |
| `src_image` | image metadata | `url`, `width`, `height` |
| `src_video` | video metadata | `url`, `duration:int`, `width`, `height`, `cover` |
| `src_audio` | audio metadata | `url`, `duration:int` |

## Known Contract Constraints

- `src_img_url` is image-only
- `src_video.duration` is `int`
- `src_audio.duration` is `int`
- `src_video.cover` must be a real uploaded image URL
- current implementation strips `fps` from final create payload

## Credit Pairing

`attribute_id` and `credit` must always be paired from the same matched credit rule.

See [`credit-rules.md`](credit-rules.md) for details.

## Canonical Reference Task

For `reference_image_to_video`, the execution path is:

1. infer task type
2. validate reference media
3. upload media
4. compliance verification for all supported reference media
5. build typed payload
6. create task
7. poll result
