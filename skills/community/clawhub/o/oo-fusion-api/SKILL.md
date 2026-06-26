---
name: oo-fusion-api
description: "OOMOL Fusion API (oomol.com). Use this skill for ANY OOMOL Fusion API request — reading, creating, updating, and deleting data. Whenever a task involves OOMOL Fusion API, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "OOMOL Fusion API"
  author: "OOMOL"
  version: "1.0.3"
  services: ["fusion-api"]
  icon: "https://static.oomol.com/logo/logo.png"
---

# OOMOL Fusion API

Operate **OOMOL Fusion API** through your OOMOL-connected account. This skill calls the `fusion-api` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

OOMOL Fusion API needs no account connection. Assume the oo CLI is installed and signed in. **Do not run `oo auth login` proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "fusion-api" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "fusion-api" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `cosyvoice_tts_generate` — Generate speech audio with CosyVoice TTS.
- `cphone_nano_banana_result` — Get cphone-nano-banana task result
- `cphone_nano_banana_state` — Get cphone-nano-banana task state
- `cphone_nano_banana_submit` — Edit images with Nano Banana [write]
- `deepseek_ocr_recognize` — Recognize text from a single image.
- `doubao_stt_result` — Get doubao-stt task result
- `doubao_stt_state` — Get doubao-stt task state
- `doubao_stt_submit` — Convert speech to text with Doubao [write]
- `doubao_text_to_image_seedream_generate` — Generate images from text with Doubao Seedream
- `doubao_tts_result` — Get doubao-tts task result
- `doubao_tts_state` — Get doubao-tts task state
- `doubao_tts_submit` — Convert text to speech with Doubao [write]
- `fal_aura_sr_result` — Get fal-aura-sr task result
- `fal_aura_sr_state` — Get fal-aura-sr task state
- `fal_aura_sr_submit` — Image super-resolution upscaling [write]
- `fal_nano_banana_2_result` — Get fal-nano-banana-2 task result
- `fal_nano_banana_2_state` — Get fal-nano-banana-2 task state
- `fal_nano_banana_2_submit` — Generate or edit images with Nano Banana 2 [write]
- `fal_nano_banana_pro_result` — Get fal-nano-banana-pro task result
- `fal_nano_banana_pro_state` — Get fal-nano-banana-pro task state
- `fal_nano_banana_pro_submit` — Edit images with Nano Banana Pro [write]
- `fal_nano_banana_result` — Get fal-nano-banana task result
- `fal_nano_banana_state` — Get fal-nano-banana task state
- `fal_nano_banana_submit` — Edit images with Nano Banana [write]
- `fal_remove_background_result` — Image with background removed [destructive]
- `fal_remove_background_state` — Get fal-remove-background task state [destructive]
- `fal_remove_background_submit` — Remove image backgrounds with the Fal.ai BRIA model [destructive]
- `file_upload_abort_multipart_upload` — Abort multipart upload [write]
- `file_upload_complete_multipart_upload` — Complete multipart upload [write]
- `file_upload_create_multipart_upload` — Initialize multipart upload [write]
- `file_upload_generate_presigned_url` — Generate a presigned URL for file upload [write]
- `file_upload_generate_presigned_urls` — Generate a presigned URL for multipart upload parts [write]
- `jina_reader_read` — Read and extract URL content
- `jina_reader_search` — Search web content
- `oomol_tts_ng_generate` — Generate speech audio
- `oomol_tts_result` — Get oomol-tts task result
- `oomol_tts_state` — Get oomol-tts task state
- `oomol_tts_submit` — Convert text to audio [write]
- `openai_image_async_result` — Get asynchronous OpenAI image generation result
- `openai_image_async_submit` — Submit asynchronous OpenAI image generation requests, including gpt-image-2 image creation. [write]
- `openai_image_edit_async_result` — Get asynchronous OpenAI image edit result [write]
- `openai_image_edit_async_submit` — Submit asynchronous OpenAI image edit requests, including gpt-image-2 image editing. [write]
- `pdf_transform_epub_result` — Get pdf-transform-epub task result
- `pdf_transform_epub_state` — Get pdf-transform-epub task state
- `pdf_transform_epub_submit` — Convert a PDF to EPUB format [write]
- `pdf_transform_markdown_result` — Get pdf-transform-markdown task result
- `pdf_transform_markdown_state` — Get pdf-transform-markdown task state
- `pdf_transform_markdown_submit` — Convert a PDF to Markdown format [write]
- `qwen_asr_filetrans_result` — Get Qwen ASR file transcription task result
- `qwen_asr_filetrans_state` — Get Qwen ASR file transcription task state
- `qwen_asr_filetrans_submit` — Submit a long-audio speech recognition task with Qwen ASR file transcription [write]
- `qwen_doc_turbo_analyze` — Analyze documents with Tongyi Qianwen
- `qwen_image_edit_plus_edit` — Edit images with Tongyi Wanxiang [write]
- `qwen_image_generate` — Generate images with Tongyi Qianwen
- `qwen_mt_image_result` — Get qwen-mt-image task result
- `qwen_mt_image_state` — Get qwen-mt-image task state
- `qwen_mt_image_submit` — Image machine translation [write]
- `qwen_tts_generate` — Generate speech audio
- `qwen_voice_cloning_create` — Create a Qwen voice cloning voice and return a preview audio URL. [write]
- `qwen_voice_design_create` — Create a Qwen voice design voice and return preview audio. [write]
- `qwen_voice_design_delete` — Delete a Qwen voice design voice. [destructive]
- `qwen_voice_design_generate` — Generate speech audio using a Qwen voice design voice.
- `qwen_voice_design_list` — List Qwen voice design voices.
- `qwen_voice_design_query` — Get details for a Qwen voice design voice.
- `seedance_video_result` — Query a Seedance video generation task result
- `seedance_video_state` — Get a Seedance video generation task state
- `seedance_video_submit` — Generate videos with Doubao Seedance [write]
- `text_to_epub_illustrate_generate` — Generate illustrations for EPUB content
- `tinify_png_shrink_compress` — Compress PNG images with the Tinify API
- `wanx_i2v_video_result` — Query first-frame-to-video task result
- `wanx_i2v_video_state` — Get wanx-i2v-video task state
- `wanx_i2v_video_submit` — Generate videos from the first frame with Tongyi Wanxiang [write]
- `wanx_image_result` — Get wanx-image task result
- `wanx_image_state` — Get wanx-image task state
- `wanx_image_submit` — Generate and edit images with Tongyi Wanxiang AI [write]
- `wanx_kf2v_video_result` — Get wanx-kf2v-video task result
- `wanx_kf2v_video_state` — Get wanx-kf2v-video task state
- `wanx_kf2v_video_submit` — Generate videos from keyframes with Tongyi Wanxiang [write]
- `wanx_r2v_video_result` — Query reference-to-video task result
- `wanx_r2v_video_state` — Get wanx-r2v-video task state
- `wanx_r2v_video_submit` — Generate videos from reference assets with Tongyi Wanxiang [write]
- `wanx_t2v_video_result` — Query text-to-video task result
- `wanx_t2v_video_state` — Get wanx-t2v-video task state
- `wanx_t2v_video_submit` — Generate text-to-video videos with Tongyi Wanxiang [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change OOMOL Fusion API state — confirm the exact payload and effect with the user before running.**
- **Actions tagged `[destructive]` remove or overwrite data — always confirm the target and get explicit approval first.**

## First-time setup

These are **one-time** steps — do not repeat them on every call. Run a step only when a command fails for the matching reason.

- **`oo: command not found`** — install the oo CLI (other platforms: <https://cli.oomol.com/install-guide.md>):

  ```bash
  curl -fsSL https://cli.oomol.com/install.sh | bash    # macOS / Linux
  ```

  ```powershell
  irm https://cli.oomol.com/install.ps1 | iex           # Windows PowerShell
  ```

- **Not signed in / authentication error** — sign in to your OOMOL account once:

  ```bash
  oo auth login
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- OOMOL Fusion API homepage: https://www.oomol.com
