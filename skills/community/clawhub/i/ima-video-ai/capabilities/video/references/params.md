# Video Params

Primary user-facing controls:

- `duration` via `--extra-params '{"duration":10}'`
- `resolution` via `--extra-params '{"resolution":"720p"}'`
- `aspect_ratio` via `--extra-params '{"aspect_ratio":"16:9"}'`
- `audio` or `generate_audio` via `--extra-params '{"audio":false}'`
- `n` via `--extra-params '{"n":1}'`

Runtime rules:

- extract defaults from the bound `form_config`
- match credit rules using canonicalized attribute values
- preserve matched rule values when building `parameters[].parameters`
- explicit `--model-id` always overrides recommendations or saved preferences
- explicit CLI params override `form_config` defaults unless a matched credit rule requires canonical replacement
- for Seedance `reference_image_to_video`, `input_images` keeps all prepared reference URLs and the payload may additionally carry `src_image`, `src_video`, and `src_audio`

Normalization:

- broad natural-language normalization is still out of scope
- only rule-participating values such as `duration`, `resolution`, and some model-specific fields are canonicalized to match the selected `attribute_id`
- aspect ratio is treated as a normal parameter, not a rule selector; pass the backend-supported value directly
- when `form_config.is_ui_virtual == true`, runtime resolves default `ui_params` into the backend target param and also remaps user overrides before credit-rule matching and payload assembly
- example: a UI-facing `quality=1080p` override may be remapped to a backend-facing `mode=pro`

Task-type shaping:

- `text_to_video` drops image-only payload fields from the extra params path
- `image_to_video` keeps exactly one image input
- `first_last_frame_to_video` keeps exactly two image inputs
- `reference_image_to_video` keeps reference assets and, for Seedance only, may expand them into `src_image` / `src_video` / `src_audio`
- `n` is forced to an integer and defaults to `1`

Detailed usage examples live in `parameter-tuning.md`.

Timeouts:

- product-list / task-create / task-detail request timeout: `30s` per HTTP call
- upload timeout: `60s`
- video generation poll interval: `8s`
- video generation total poll timeout: `2400s`

If you need exact supported values, inspect the live product list with `--list-models` and bind against its `form_config` and `credit_rules`.
