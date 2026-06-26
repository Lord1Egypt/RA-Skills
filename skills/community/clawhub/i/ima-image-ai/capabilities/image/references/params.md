# Image Params

Primary user-facing controls:

- `size` via `--size`
- `aspect_ratio` via `--extra-params '{"aspect_ratio":"16:9"}'`
- `n` via `--extra-params '{"n":4}'`

Runtime rule:

- extract defaults from `form_config`
- match credit rules using canonicalized attribute values
- preserve matched rule values when building `parameters[].parameters`
- when multiple model hints appear in the prompt, choose the first match by prompt position
- explicit `--model-id` always overrides prompt inference
- explicit CLI params override prompt-inferred controls
- if `aspect_ratio` and `size` are both inferred, keep both and let backend validation decide

Detailed usage examples live in `parameter-tuning.md`.

Timeouts:

- product-list / task-create / task-detail request timeout: 30s per HTTP call
- upload timeout: 60s
- image generation poll interval: 5s
- image generation total poll timeout: 600s
