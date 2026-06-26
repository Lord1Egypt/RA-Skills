# MiniMax API Notes

Reference summary for the local `minimax-tools` skill.

## Authentication

- Env var: `MINIMAX_API_KEY`
- Auth header: `Authorization: Bearer <MINIMAX_API_KEY>`

## Base URL

- `https://api.minimaxi.com`

## Endpoints used by this skill

### 1) TTS

- `POST /v1/t2a_v2`
- Recommended non-streaming mode for local file generation
- Useful request fields:
  - `model`
  - `text`
  - `stream`
  - `voice_setting.voice_id`
  - `voice_setting.speed`
  - `voice_setting.vol`
  - `voice_setting.pitch`
  - `voice_setting.emotion`
  - `audio_setting.sample_rate`
  - `audio_setting.bitrate`
  - `audio_setting.format`
  - `audio_setting.channel`
  - `output_format` = `url` or `hex`
  - `subtitle_enable`
- Text limit: under 10000 chars for sync API
- Response may include:
  - `data.audio` (hex or url depending on output mode)
  - `data.subtitle_file`
  - `extra_info`
  - `trace_id`
  - `base_resp.status_code/status_msg`

### 2) Voice cloning

- Upload clone source audio: `POST /v1/files/upload` with `purpose=voice_clone`
- Upload optional prompt audio: `POST /v1/files/upload` with `purpose=prompt_audio`
- Clone voice: `POST /v1/voice_clone`
- Main request fields:
  - `file_id`
  - `voice_id`
  - `clone_prompt.prompt_audio`
  - `clone_prompt.prompt_text`
  - `text`
  - `model`
  - `language_boost`
  - `need_noise_reduction`
  - `need_volume_normalization`
  - `aigc_watermark`
- Source clone audio constraints:
  - mp3 / m4a / wav
  - 10 seconds to 5 minutes
  - <= 20 MB
- Prompt audio constraints:
  - mp3 / m4a / wav
  - under 8 seconds
  - <= 20 MB
- If `text` and `model` are provided, response may include `demo_audio`
- A cloned `voice_id` can be used later in TTS
- MiniMax docs note cloned voices are temporary unless used within 7 days in actual TTS

### 3) Image generation

- `POST /v1/image_generation`
- Supports both text-to-image and image-to-image / subject-reference generation
- Useful request fields:
  - `model` (`image-01` or `image-01-live`)
  - `prompt`
  - `subject_reference`
  - `style.style_type`
  - `style.style_weight`
  - `aspect_ratio`
  - `width`
  - `height`
  - `response_format` = `url` or `base64`
  - `seed`
  - `n`
  - `prompt_optimizer`
  - `aigc_watermark`
- Response may include:
  - `data.image_urls`
  - `data.image_base64`
  - `metadata.success_count`
  - `metadata.failed_count`
  - `id`
  - `base_resp`
- Subject reference images support public URLs or Data URLs; local files can be converted to Data URLs by the wrapper script

### 4) Video generation

- Create task: `POST /v1/video_generation`
- Query task: `GET /v1/query/video_generation?task_id=...`
- Download result file: `GET /v1/files/retrieve_content?file_id=...`
- Supported wrapper modes:
  - text-to-video via `prompt`
  - image-to-video via `first_frame_image`
  - first/last-frame video via `first_frame_image` + `last_frame_image`
- Main request fields:
  - `model`
  - `prompt`
  - `first_frame_image`
  - `last_frame_image`
  - `prompt_optimizer`
  - `fast_pretreatment`
  - `duration`
  - `resolution`
  - `aigc_watermark`
- Local image paths can be converted to Data URLs by the wrapper script
- Query statuses:
  - `Preparing`
  - `Queueing`
  - `Processing`
  - `Success`
  - `Fail`

### 5) Music generation

- `POST /v1/music_generation`
- Useful request fields:
  - `model` (`music-2.5+` recommended)
  - `prompt`
  - `lyrics`
  - `lyrics_optimizer`
  - `is_instrumental`
  - `stream`
  - `output_format`
  - `audio_setting.sample_rate`
  - `audio_setting.bitrate`
  - `audio_setting.format`
- Response may include:
  - `data.audio` (hex or url depending on output mode)
  - `trace_id`
  - `extra_info`
  - `base_resp`

## Common error codes

- `0`: success
- `1002`: rate limited
- `1004`: auth failed
- `1008`: insufficient balance
- `1026`: sensitive input
- `1027`: sensitive output
- `1042`: invalid/invisible characters too high (mainly speech/text inputs)
- `2013`: invalid parameters
- `2049`: invalid API key

## Skill conventions

- Prefer `output_format=url` in non-streaming mode, then download immediately
- TTS wrapper built-in defaults: Chinese = `Chinese (Mandarin)_Lyrical_Voice`, English = `English_Graceful_Lady`
- For image generation, prefer `response_format=url` unless raw Base64 is specifically needed
- Save outputs under `skills/minimax-tools/outputs/`
- Print JSON only from scripts
- Include `trace_id` in failures whenever present

## Sources

- API overview
- TTS HTTP
- Voice cloning (upload / clone)
- Image generation (text-to-image / image-to-image)
- Video generation create/query
- Music generation
- File retrieve_content
- Error codes
