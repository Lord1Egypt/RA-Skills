# Reference Image To Video Flow

This flow covers multimodal reference inputs:

- images
- videos
- audio

## Execution Flow

```text
collect inputs
  -> infer task_type=reference_image_to_video
  -> strict preflight validation
  -> upload media
  -> compliance verification for all supported reference media
  -> build canonical payload
  -> create task
  -> poll result
```

## Supported Entry Patterns

- image only
- image + video
- image + audio
- image + video + audio
- video + audio

## Stop Conditions

Stop before create-task if:

- media count exceeds limits
- format is unsupported
- duration is out of range
- dimensions are out of range
- FPS is out of range
- remote URL metadata cannot be probed
- any reference media fails compliance verification
