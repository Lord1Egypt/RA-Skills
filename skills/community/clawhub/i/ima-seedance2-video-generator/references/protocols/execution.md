# Execution Protocol

This is the canonical OpenClaw execution protocol for this skill.

## Hard Rule

OpenClaw must call `scripts/ima_video_create.py`.

OpenClaw must not:

- build `/open/v1/tasks/create` payloads directly
- compute `attribute_id`
- compute `credit`
- build `src_img_url`
- build `src_image`
- build `src_video`
- build `src_audio`

## OpenClaw Responsibilities

OpenClaw may:

1. understand user intent
2. collect media files or URLs
3. choose high-level script arguments
4. run the script
5. consume event stream

## Script Responsibilities

The script owns:

1. task-type inference
2. strict preflight validation
3. media upload
4. compliance verification for all supported reference media
5. payload construction
6. create-task
7. polling
8. result emission

## Task Type Defaults

- text only -> `text_to_video`
- one image -> `image_to_video`
- explicit first-last-frame + 2 images -> `first_last_frame_to_video`
- video input -> `reference_image_to_video`
- audio input -> `reference_image_to_video`
- mixed reference media -> `reference_image_to_video`

## Related References

- [`../contracts/create-task.md`](../contracts/create-task.md)
- [`../contracts/payload-rules.md`](../contracts/payload-rules.md)
- [`../flows/reference-image-to-video.md`](../flows/reference-image-to-video.md)
- [`../limits/reference-media-rules.md`](../limits/reference-media-rules.md)
- [`event-stream.md`](event-stream.md)
