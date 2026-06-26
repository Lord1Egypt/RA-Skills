---
name: moark-tts
description: Text-to-Speech (TTS) and voice-feature skill for Gitee AI that lets the user choose audiofly, chattts, cosyvoice2, cosyvoice3, cosyvoice-300m, fish-speech-1.2-sft, index-tts-1.5, index-tts-2, glm-tts, megatts3, moss-ttsd-v0.5, qwen-tts, spark-tts-0.5b, step-audio-tts-3b, or vibevoice-large, then fills in only model-specific parameters for speech or voice feature extraction, including multi-item Qwen3-TTS inputs with built-in or custom voices.
metadata:
  openclaw:
    emoji: "🎤"
    requires:
      bins: [ "python" ]
      env: [ "GITEEAI_API_KEY" ]
    primaryEnv: "GITEEAI_API_KEY"
---

# Text-to-Speech (TTS)

This skill supports Gitee AI TTS plus CosyVoice voice feature extraction workflows.
It supports fifteen user-facing model choices for TTS:

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

When the user does not specify a model, ask them to choose one. After the model is chosen, only ask for parameters that
are relevant to that model.

## Usage

Use the bundled script to generate speech.

```bash
python {baseDir}/scripts/perform_tts.py --model cosyvoice2 --text "你好，我是模力方舟。" --voice alloy --api-key YOUR_API_KEY
```

For CosyVoice-300M voice feature extraction (voice cloning prep), use:

```bash
python {baseDir}/scripts/perform_voice_feature_extraction.py --model FunAudioLLM-CosyVoice-300M --prompt "提供用于声纹提取的提示文本" --file-url "https://example.com/sample.mp3" --api-key YOUR_API_KEY
```

## Options

- `--model` required: `audiofly`, `chattts`, `cosyvoice2`, `cosyvoice3`, `cosyvoice-300m`, `fish-speech-1.2-sft`,
  `index-tts-1.5`, `index-tts-2`, `glm-tts`, `megatts3`, `moss-ttsd-v0.5`, `qwen-tts`, `spark-tts-0.5b`,
  `step-audio-tts-3b`, or `vibevoice-large`
- `--text` required in general: text to synthesize. For Qwen3-TTS multi-input mode (`--qwen-inputs-json`), `--text` is
  optional
- `--mode` optional: `auto`, `sync`, or `async`
- `--prompt` optional: model-specific style prompt such as ChatTTS tags
- `--prompt-text` optional: reference transcript for style-conditioned models
- `--prompt-audio-url` optional: reference audio URL for style-conditioned models
- `--qwen-inputs-json` optional: structured Qwen3-TTS `inputs` JSON (array/object). Supports mixed built-in and custom
  voice items
- `--speaker` optional: Qwen3-TTS built-in speaker for single input (`Vivian`, `Serena`, `Uncle_Fu`, `Dylan`, `Eric`,
  `Ryan`, `Aiden`, `Ono_Anna`, `Sohee`)
- `--language` optional: Qwen3-TTS language for single input (`Chinese` or `English`)
- `--instruction` optional: Qwen3-TTS style instruction for single input
- `--prompt-audio-urls` optional: `vibevoice-large` reference audio; supports one URL or JSON array string such as
  `["https://a.wav","https://b.wav"]`
- `--emo-audio-prompt-url` optional: emotion reference audio URL for IndexTTS-2
- `--emo-alpha` optional: emotion mixing weight for IndexTTS-2 audio emotion control
- `--emo-text` optional: emotion control text for IndexTTS-2
- `--use-emo-text` optional: enable or disable `emo_text` for IndexTTS-2 (`true`/`false`)
- `--prompt-wav-url` optional: reference prompt WAV URL for CosyVoice2 or CosyVoice3
- `--voice-url` optional: reference voice audio URL for ChatTTS or fish-speech-1.2-sft cloning
- `--instruct-text` optional: model-specific instruction text such as CosyVoice2 or CosyVoice3 speaking style guidance
- `--seed` optional: model-specific seed value such as CosyVoice2 or CosyVoice3
- `--audio-mode` optional: `single` or `role` for `moss-ttsd-v0.5` (required when mode cannot be inferred from fields)
- `--prompt-audio-single-url` optional: single-speaker reference audio URL for `moss-ttsd-v0.5` single mode
- `--prompt-text-single` optional: single-speaker reference transcript for `moss-ttsd-v0.5` single mode
- `--prompt-audio-1-url` optional: speaker-1 reference audio URL for `moss-ttsd-v0.5` role mode
- `--prompt-text-1` optional: speaker-1 reference transcript for `moss-ttsd-v0.5` role mode
- `--prompt-audio-2-url` optional: speaker-2 reference audio URL for `moss-ttsd-v0.5` role mode
- `--prompt-text-2` optional: speaker-2 reference transcript for `moss-ttsd-v0.5` role mode
- `--use-normalize` optional: enable or disable `use_normalize` for `moss-ttsd-v0.5` (`true`/`false`)
- `--prompt-language` optional: prompt language hint for models such as MegaTTS3
- `--intelligibility-weight` optional: pronunciation intelligibility weight for models such as MegaTTS3
- `--similarity-weight` optional: timbre similarity weight for models such as MegaTTS3
- `--temperature` optional: model-specific sampling temperature
- `--top-p` optional: model-specific top-p sampling value
- `--top-k` optional: model-specific top-k sampling value
- `--gender` optional: async TTS gender hint
- `--pitch` optional: async TTS pitch hint
- `--speed` optional: async TTS speed hint (for example CosyVoice3, Spark-TTS-0.5B, or Qwen3-TTS)
- `--num-inference-steps` optional: AudioFly generation step count
- `--guidance-scale` optional: AudioFly classifier-free guidance scale
- `--output-format` optional: AudioFly or Qwen3-TTS output format such as `mp3` or `wav`
- `--voice` optional: OpenAI-compatible voice field when supported by the target model
- `--extra-body-json` optional: JSON object for explicitly requested undocumented fields
- `--response-data-format` optional: `url` or `blob` for sync TTS
- `--output` optional: output file path when sync TTS returns binary audio
- `--failover-enabled` optional: request header `X-Failover-Enabled`, defaults to `true`
- `perform_voice_feature_extraction.py` options: `--prompt`, `--file-url` (URL only), `--model` (default
  `FunAudioLLM-CosyVoice-300M`), `--failover-enabled`, `--output`, `--api-key`

## Workflow

1. Determine whether the user wants speech synthesis or CosyVoice voice-feature extraction.
2. For speech synthesis: ask the user to choose one of `audiofly`, `chattts`, `cosyvoice2`, `cosyvoice3`,
   `cosyvoice-300m`, `fish-speech-1.2-sft`, `index-tts-1.5`, `index-tts-2`, `glm-tts`, `megatts3`, `moss-ttsd-v0.5`,
   `qwen-tts`, `spark-tts-0.5b`, `step-audio-tts-3b`, or `vibevoice-large` if not specified.
3. For speech synthesis: read [references/models.md](./references/models.md), gather missing model-specific params, and
   execute `perform_tts.py`.
4. For voice-feature extraction: execute `perform_voice_feature_extraction.py` with `--prompt` and URL-only
   `--file-url`.
5. Parse script output.
6. For TTS output, prioritize `AUDIO_URL:` then `AUDIO_FILE:` then `TTS_RESULT:`.
7. For voice feature output, prioritize `VOICE_URL:` (if present), otherwise return `VOICE_FEATURE_FILE:` and summarize
   `VOICE_FEATURE_RESULT:`.

## Notes

- Keep the answer language consistent with the user's language.
- This script is standard-library only and is intended to run directly with `python`; do not require `uv` for
  `moark-tts`.
- If `GITEEAI_API_KEY` is missing, remind the user to provide `--api-key`.
- By default, all TTS requests send `X-Failover-Enabled: true`. Only set `--failover-enabled false` when the user
  explicitly needs to disable failover.
- `audiofly` is mapped to the official model name `AudioFly`. Use async mode only. When the user shows an OpenAI SDK
  example that puts `num_inference_steps`, `guidance_scale`, or `output_format` under `extra_body`, map them to
  `--num-inference-steps`, `--guidance-scale`, and `--output-format`.
- `chattts` is mapped to the official model name `ChatTTS`. When the user shows an OpenAI SDK example that puts
  `prompt`, `temperature`, `top_P`, `top_K`, or `voice_url` under `extra_body`, map them to `--prompt`, `--temperature`,
  `--top-p`, `--top-k`, and `--voice-url`.
- `cosyvoice2` is mapped to the official model name `CosyVoice2`. When the user shows an OpenAI SDK example that puts
  `prompt_wav_url`, `prompt_text`, `instruct_text`, or `seed` under `extra_body`, map them to `--prompt-wav-url`,
  `--prompt-text`, `--instruct-text`, and `--seed`.
- `cosyvoice3` is mapped to the official model name `CosyVoice3`. Use async mode only. When the user shows an OpenAI SDK
  example that puts `prompt_wav_url`, `prompt_text`, `instruct_text`, `speed`, or `seed` under `extra_body`, map them to
  `--prompt-wav-url`, `--prompt-text`, `--instruct-text`, `--speed`, and `--seed`.
- `cosyvoice-300m` is mapped to `FunAudioLLM-CosyVoice-300M` for sync `/audio/speech`. Map OpenAI `extra_body.voice_url`
  to `--voice-url`.
- CosyVoice voice-feature extraction uses `/audio/voice-feature-extraction` and is handled by
  `perform_voice_feature_extraction.py`; `--file-url` must be an http(s) URL (no local file path support).
- `fish-speech-1.2-sft` uses sync `/audio/speech`. When the user shows an OpenAI SDK example that puts `voice_url` under
  `extra_body`, map it to `--voice-url`.
- `index-tts-1.5` currently uses the sync `/audio/speech` endpoint. When the user shows an OpenAI SDK example that puts
  `prompt_audio_url` under `extra_body`, map it to the script's `--prompt-audio-url`.
- `index-tts-2` supports four emotion-control patterns: sync/async + audio-emotion/text-emotion. Map
  `emo_audio_prompt_url` + `emo_alpha` to `--emo-audio-prompt-url` + `--emo-alpha`; map `emo_text` + `use_emo_text` to
  `--emo-text` + `--use-emo-text`. In auto mode it defaults to sync; when user asks async, force `--mode async`.
- `megatts3` is mapped to the official model name `MegaTTS3`. When the user shows an OpenAI SDK example that puts
  `prompt_language`, `intelligibility_weight`, or `similarity_weight` under `extra_body`, map them to
  `--prompt-language`, `--intelligibility-weight`, and `--similarity-weight`.
- `step-audio-tts-3b` is mapped to the official model name `Step-Audio-TTS-3B`. When the user shows an OpenAI SDK
  example that puts `prompt_audio_url` and `prompt_text` under `extra_body`, map them to `--prompt-audio-url` and
  `--prompt-text`.
- `spark-tts-0.5b` is mapped to the official model name `Spark-TTS-0.5B`. Use async mode only. For plain synthesis, just
  pass text. For voice cloning, map `prompt_audio_url` and `prompt_text` to `--prompt-audio-url` and `--prompt-text`;
  `gender`/`pitch`/`speed` can be passed when explicitly requested.
- `qwen-tts` is mapped to the official model name `Qwen3-TTS`. Use async mode only. Prefer structured `inputs` items:
    - Built-in speaker item: `prompt` + `speaker` + optional `language` (`Chinese`/`English`) + optional `instruction`.
    - Custom voice item: `prompt` + `prompt_audio_url` + `prompt_text` + optional `language` + optional `instruction`.
    - Use `--qwen-inputs-json` for multiple items in one request; use `--speaker`/`--language`/`--instruction` for
      single-item mode.
    - Built-in speakers: `Vivian`, `Serena`, `Uncle_Fu`, `Dylan`, `Eric`, `Ryan`, `Aiden`, `Ono_Anna`, `Sohee`.
- `moss-ttsd-v0.5` is mapped to the official model name `MOSS-TTSD-v0.5`. Use async mode only. Map single mode fields
  `prompt_audio_single_url` + `prompt_text_single` to `--prompt-audio-single-url` + `--prompt-text-single`, and role
  mode fields (`prompt_audio_1_url`, `prompt_text_1`, `prompt_audio_2_url`, `prompt_text_2`) to the matching CLI
  options. Pass `audio_mode` through `--audio-mode` and `use_normalize` through `--use-normalize`.
- `vibevoice-large` is mapped to the official model name `VibeVoice-Large`. Use async mode only. Map `prompt_audio_urls`
  to `--prompt-audio-urls`, and accept both a single URL string and a JSON array string. When the user provides only
  `prompt_audio_url`, map it into `prompt_audio_urls` automatically for compatibility.
- `glm-tts` currently exposes only the basic sync request in the official OpenAPI spec.
- Do not invent model parameters. If a field is not documented for that model, only pass it when the user explicitly
  asked for it and use `--extra-body-json`.
