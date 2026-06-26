# Video Routing

## Task-Type Rules

The current video route builder applies this order:

1. explicit `intent_hints.task_type`
2. `intent_hints.video_mode=first_last_frame`
3. `intent_hints.video_mode=reference`
4. one image -> `image_to_video`
5. two or more images -> clarification
6. zero images -> `text_to_video`

## Image-Role Rules

- `image_to_video` requires exactly one input image
- `first_last_frame_to_video` requires exactly two input images
- `reference_image_to_video` requires at least one input image
- `text_to_video` ignores image inputs

Validation is enforced by `shared/inputs.py` after the route is chosen.

## Clarification Message

The current clarification text for ambiguous multi-image input is:

`这两张图分别是什么角色？是首帧/尾帧，还是参考图，还是只动其中一张？`

That is the live behavior today and should be documented as such until the prompt changes in code.
