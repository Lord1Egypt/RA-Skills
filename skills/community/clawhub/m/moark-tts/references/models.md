# TTS Model Routing

Use this file only after `moark-tts` is selected and you need to decide which model to call or which follow-up
parameters to request.

## Supported user-facing choices

### `audiofly`

- Official model name on March 4, 2026: `AudioFly`
- API support on March 4, 2026:
    - Async only: `/async/audio/speech`
    - Task polling fallback: `/task/{task_id}`
- Required input:
    - `text` (script maps to API field `inputs`)
- Optional follow-up parameters:
    - `num_inference_steps`
    - `guidance_scale`
    - `output_format`
- Routing rule:
    - Always use async.
    - Map `num_inference_steps`, `guidance_scale`, and `output_format` to dedicated CLI flags.
    - Pass only the AudioFly-specific fields the user actually mentioned or requested.

### `chattts`

- Official model name: `ChatTTS`
- API support on March 3, 2026:
    - Sync: `/audio/speech`
- Required input:
    - `text`
- Optional follow-up parameters:
    - `voice`
    - `prompt`
    - `temperature`
    - `top_P`
    - `top_K`
    - `voice_url`
- Routing rule:
    - Always use sync.
    - If the user provides an OpenAI SDK style `extra_body`, map `prompt`, `temperature`, `top_P`, `top_K`, and
      `voice_url` to the dedicated CLI flags instead of forcing `--extra-body-json`.
    - Pass only the ChatTTS-specific fields the user actually mentioned or requested.

### `cosyvoice2`

- Official model name: `CosyVoice2`
- API support on March 3, 2026:
    - Sync: `/audio/speech`
- Required input:
    - `text`
- Optional follow-up parameters:
    - `voice`
    - `prompt_wav_url`
    - `prompt_text`
    - `instruct_text`
    - `seed`
- Routing rule:
    - Always use sync.
    - If the user provides an OpenAI SDK style `extra_body`, map `prompt_wav_url`, `prompt_text`, `instruct_text`, and
      `seed` to the dedicated CLI flags instead of forcing `--extra-body-json`.
    - Pass only the CosyVoice2-specific fields the user actually mentioned or requested.

### `cosyvoice3`

- Official model name on March 4, 2026: `CosyVoice3`
- API support on March 4, 2026:
    - Async only: `/async/audio/speech`
    - Task polling fallback: `/task/{task_id}`
- Required input:
    - `text` (script maps to API field `inputs`)
- Optional follow-up parameters:
    - `prompt_wav_url`
    - `prompt_text`
    - `instruct_text`
    - `speed` (integer)
    - `seed`
- Routing rule:
    - Always use async.
    - If the user provides an OpenAI SDK style `extra_body`, map `prompt_wav_url`, `prompt_text`, `instruct_text`,
      `speed`, and `seed` to dedicated CLI flags.
    - Pass only the CosyVoice3-specific fields the user actually mentioned or requested.

### `cosyvoice-300m`

- Official model name: `FunAudioLLM-CosyVoice-300M`
- API support on March 3, 2026:
    - Sync speech: `/audio/speech`
    - Voice feature extraction: `/audio/voice-feature-extraction`
- Required input (speech):
    - `text`
- Optional follow-up parameters (speech):
    - `voice`
    - `voice_url`
    - `failover_enabled`
- Required input (voice feature extraction):
    - `prompt`
    - `file_url` (URL only)
- Routing rule:
    - For TTS generation, use `perform_tts.py` with sync mode.
    - Map OpenAI `extra_body.voice_url` to `--voice-url`.
    - For voice feature extraction, use `perform_voice_feature_extraction.py` and require URL-only `--file-url`.
    - By default send `X-Failover-Enabled: true`; only disable it when the user explicitly asks for `false`.
    - If extraction API returns binary content, return the `VOICE_FEATURE_FILE` path from script output.

### `fish-speech-1.2-sft`

- Official model name: `fish-speech-1.2-sft`
- API support on March 3, 2026:
    - Sync: `/audio/speech`
- Required input:
    - `text`
- Optional follow-up parameters:
    - `voice`
    - `voice_url`
    - `failover_enabled`
- Routing rule:
    - Always use sync.
    - By default send `X-Failover-Enabled: true`; only disable it when the user explicitly asks for `false`.
    - If the user provides an OpenAI SDK style `extra_body.voice_url`, map it to `--voice-url`.

### `step-audio-tts-3b`

- Official model name: `Step-Audio-TTS-3B`
- API support on March 3, 2026:
    - Sync: `/audio/speech`
- Required input:
    - `text`
- Optional follow-up parameters:
    - `voice`
    - `prompt_audio_url`
    - `prompt_text`
    - `failover_enabled`
- Routing rule:
    - Always use sync.
    - By default send `X-Failover-Enabled: true`; only disable it when the user explicitly asks for `false`.
    - If the user provides an OpenAI SDK style `extra_body`, map `prompt_audio_url` and `prompt_text` to the dedicated
      CLI flags instead of forcing `--extra-body-json`.
    - If the user provides `default_headers={"X-Failover-Enabled":"false"}`, map it to `--failover-enabled false`.

### `spark-tts-0.5b`

- Official model name: `Spark-TTS-0.5B`
- API support on March 3, 2026:
    - Async: `/async/audio/speech`
    - Task polling fallback: `/task/{task_id}`
- Required input:
    - `text`
- Optional follow-up parameters:
    - `prompt_audio_url`
    - `prompt_text`
    - `gender`
    - `pitch`
    - `speed`
    - `failover_enabled`
- Routing rule:
    - Always use async.
    - For plain synthesis, pass only `text`.
    - For voice cloning, map `prompt_audio_url` and `prompt_text` from the user's OpenAI `extra_body` to dedicated CLI
      flags.
    - If the user provides `gender`/`pitch`/`speed`, pass them directly.
    - By default send `X-Failover-Enabled: true`; only disable it when the user explicitly asks for `false`.

### `index-tts-1.5`

- Official model name: `IndexTTS-1.5`
- API support on March 3, 2026:
    - Sync: `/audio/speech`
- Required input:
    - `text`
- Optional follow-up parameters:
    - `prompt_audio_url`
    - `voice`
- Routing rule:
    - Always use sync.
    - If the user provides an OpenAI SDK style `extra_body.prompt_audio_url`, map it to the script's
      `--prompt-audio-url`.
    - Pass `voice` only when the user explicitly gives or requests it.

### `index-tts-2`

- Official model name: `IndexTTS-2`
- API support on March 3, 2026:
    - Sync: `/audio/speech`
    - Async: `/async/audio/speech`
    - Task polling fallback: `/task/{task_id}`
- Required input:
    - `text`
- Optional follow-up parameters:
    - `prompt_text`
    - `prompt_audio_url`
    - `emo_audio_prompt_url`
    - `emo_alpha`
    - `emo_text`
    - `use_emo_text`
    - `voice`
    - `failover_enabled`
- Routing rule:
    - Supports 4 patterns:
        1) Sync + audio emotion control (`prompt_audio_url` + `prompt_text` + `emo_audio_prompt_url` + `emo_alpha`)
        2) Async + audio emotion control (`--mode async` + same fields above)
        3) Sync + text emotion control (`prompt_audio_url` + `prompt_text` + `emo_text` + `use_emo_text`)
        4) Async + text emotion control (`--mode async` + same fields above)
    - In auto mode, default to sync. If the user asks for async, explicitly set `--mode async`.
    - By default send `X-Failover-Enabled: true`; only disable it when the user explicitly asks for `false`.
    - Map OpenAI `extra_body` fields `emo_audio_prompt_url`, `emo_alpha`, `emo_text`, and `use_emo_text` to the
      dedicated CLI flags.

### `glm-tts`

- Official model name: `GLM-TTS`
- API support on March 3, 2026:
    - Sync only: `/audio/speech`
- Required input:
    - `text`
- Optional follow-up parameters:
    - None documented in the official OpenAPI spec for this model.
- Routing rule:
    - Always use sync.
    - If the user explicitly provides undocumented extra parameters, pass them only through `--extra-body-json` as a
      best-effort forward-compatible escape hatch.

### `megatts3`

- Official model name: `MegaTTS3`
- API support on March 4, 2026:
    - Sync only: `/audio/speech`
- Required input:
    - `text`
- Optional follow-up parameters:
    - `voice`
    - `prompt_language`
    - `intelligibility_weight`
    - `similarity_weight`
    - `failover_enabled`
- Routing rule:
    - Always use sync.
    - If the user provides an OpenAI SDK style `extra_body`, map `prompt_language`, `intelligibility_weight`, and
      `similarity_weight` to dedicated CLI flags instead of forcing `--extra-body-json`.
    - Pass only the MegaTTS3-specific fields the user actually mentioned or requested.

### `moss-ttsd-v0.5`

- Official model name on March 4, 2026: `MOSS-TTSD-v0.5`
- API support on March 4, 2026:
    - Async only: `/async/audio/speech`
    - Task polling fallback: `/task/{task_id}`
- Required input:
    - `text` (script maps to API field `inputs`)
    - `audio_mode` (`Single` or `Role`)
- Required follow-up parameters by `audio_mode`:
    - `Single`:
        - `prompt_audio_single_url`
        - `prompt_text_single`
    - `Role`:
        - `prompt_audio_1_url`
        - `prompt_text_1`
        - `prompt_audio_2_url`
        - `prompt_text_2`
- Optional follow-up parameters:
    - `seed`
    - `use_normalize`
- Routing rule:
    - Always use async.
    - If user says “单音频模式”, map to `--audio-mode single`.
    - If user says “角色音频模式”, map to `--audio-mode role`.
    - Do not mix single-mode and role-mode prompt fields in one request.
    - Map `use_normalize` to `--use-normalize true|false`.

### `vibevoice-large`

- Official model name on March 4, 2026: `VibeVoice-Large`
- API support on March 4, 2026:
    - Async only: `/async/audio/speech`
    - Task polling fallback: `/task/{task_id}`
- Required input:
    - `text` (script maps to API field `inputs`)
- Optional follow-up parameters:
    - `prompt_audio_urls`
    - `seed`
- Routing rule:
    - Always use async.
    - Map `prompt_audio_urls` to `--prompt-audio-urls`.
    - `--prompt-audio-urls` supports two formats:
        - One URL string: `https://example.com/ref.wav`
        - JSON array string: `["https://a.wav","https://b.wav"]`
    - If user only provides one `prompt_audio_url`, map it to `prompt_audio_urls` automatically.

### `qwen-tts`

- Official model name on March 4, 2026: `Qwen3-TTS`
- API support on March 4, 2026:
    - Async only: `/async/audio/speech`
- Required input:
    - `inputs` (single object or array of objects)
- Optional follow-up parameters:
    - `output_format`
- Routing rule:
    - Always use async.
    - If the user says `qwen-tts`, map it to `Qwen3-TTS`.
    - Prefer structured `inputs` entries.
    - Built-in speaker entry fields:
        - `prompt`
        - `speaker` (`Vivian`, `Serena`, `Uncle_Fu`, `Dylan`, `Eric`, `Ryan`, `Aiden`, `Ono_Anna`, `Sohee`)
        - optional `language` (`Chinese` or `English`)
        - optional `instruction`
    - Custom voice entry fields:
        - `prompt`
        - `prompt_audio_url`
        - `prompt_text`
        - optional `language` (`Chinese` or `English`)
        - optional `instruction`
    - Use `--qwen-inputs-json` to pass multiple entries in one request (built-in/custom mix is allowed).
    - For single-entry requests, map CLI flags `--speaker`, `--language`, `--instruction`, `--prompt-audio-url`, and
      `--prompt-text` into one `inputs` object.

## Follow-up policy

- If the user did not pick a model, ask them to choose one of:
    - `audiofly`
    - `chattts`
    - `cosyvoice2`
    - `cosyvoice3`
    - `cosyvoice-300m`
    - `fish-speech-1.2-sft`
    - `index-tts-1.5`
    - `index-tts-2`
    - `glm-tts`
    - `megatts3`
    - `moss-ttsd-v0.5`
    - `qwen-tts`
    - `spark-tts-0.5b`
    - `step-audio-tts-3b`
    - `vibevoice-large`
- After the model is chosen, only ask for parameters that are relevant to that model.
- Do not ask for every optional parameter up front. Only ask for the ones the user clearly needs.

## Script outputs

The bundled script prints parseable lines:

- `AUDIO_URL: ...`
- `AUDIO_FILE: ...`
- `TASK_ID: ...`
- `TASK_STATUS: ...`
- `TTS_RESULT: {...}`
- `VOICE_URL: ...`
- `VOICE_FEATURE_FILE: ...`
- `VOICE_FEATURE_RESULT: {...}`

Prefer `AUDIO_URL` when present. If only `AUDIO_FILE` exists, return the saved file path. If neither exists, summarize
`TTS_RESULT`.
