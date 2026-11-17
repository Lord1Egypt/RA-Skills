---
name: oceantoken-media
description: Create images, video, voice-overs and subtitles with OceanToken models and save them into the project. Use when the user wants a generated or edited image (hero, illustration, icon, product shot, background, a change to an existing picture), a video clip (from text, or animating an image), narration / text-to-speech, or a transcript or subtitles, and the OceanToken tools are connected. Also for Chinese requests such as 生成图片、做图、改图、海报、生成视频、图生视频、配音、语音合成、朗读、字幕、转写.
metadata:
  openclaw:
    homepage: https://oceantoken.ai
    requires:
      bins:
        - curl
---

# Images, video and audio with OceanToken

Every generation spends the user's OceanToken balance. Work like a producer on a
budget: settle the brief, price it, generate once well, save the result, report.

If the host also has a built-in image tool, use OceanToken when the user asks
for OceanToken or a specific model, wants several options or a batch, needs
video, audio or subtitles, or wants the cost up front.

## Connect first

These steps use the OceanToken MCP tools (`search_models`, `estimate_cost`,
`generate_image`, ...). If they are not available, the server is not connected
yet. It is `https://mcp.oceantoken.ai/mcp` (streamable HTTP) with an OAuth
sign-in. In OpenClaw:

```bash
openclaw mcp set oceantoken '{"url":"https://mcp.oceantoken.ai/mcp","transport":"streamable-http","auth":"oauth"}'
openclaw mcp login oceantoken
```

For other hosts see https://github.com/NextFormAI/oceantoken-plugins#install.

## 1. Settle the brief

Know before generating: what the asset is for, where the file goes, its shape
(aspect ratio, pixel size, duration), and the look. Read the project first
(existing assets, design tokens, the `<img>`/CSS that will hold it) so you ask
the user only what the code cannot tell you.

## 2. Pick the model

- `search_models` with `type` = `image`, `video`, `speech` or `transcription`.
  `featured` models are OceanToken's directly served defaults; `sort="price"`
  finds cheap ones. Never invent a model id.
- Call `get_model` before using non-default options: it lists the sizes, aspect
  ratios, resolutions, durations, audio and first/last-frame support the model
  really accepts. Sending an option the model lacks fails the request.
- Rough guide (confirm with search): text-heavy or precise edits favour
  GPT Image; illustration and vector styles favour Recraft; photoreal and
  product shots favour Seedream or Gemini image models; video: Seedance is the
  value pick, Veo and Sora for top quality.

## 3. Price it, and say the price

Call `estimate_cost` for any video, any batch (`n > 1`), 4K images and long
speech, and tell the user the figure and its `confidence`. Ask before spending
more than about $2 unless the user already agreed to a budget. When they gave a
budget, pass it as `max_cost_usd`: the tool then refuses anything over it before
spending. Never loop regenerations without telling them: each attempt costs money.

## 4. Generate

- **Image**: `generate_image(model, prompt, size, quality, n)`. A good prompt
  names subject, setting, composition, lighting, style and mood. Few models
  render text reliably: leave text out of the image and overlay it in HTML/CSS
  unless the user wants it baked in (then quote the exact words).
- **Edit / restyle / keep a character consistent**: pass the source images in
  `reference_image_urls`. Local files go through `upload_file` first (small
  files as `content_base64`, big ones with the returned `curl` command).
- **Video**: `create_video` returns a `job_id`; call `get_job(job_id,
  wait_seconds=50)` until `status` is `completed` (usually 1-5 minutes). To
  animate a still, generate or upload the image and pass it as
  `first_frame_url`; add `last_frame_url` to control the ending. Keep prompts
  about motion and camera ("slow dolly-in, waves roll left to right").
- **Voice-over**: `generate_speech(model, text, voice)`; `instructions` steers
  tone on models that support it.
- **Subtitles / transcript**: `transcribe_audio(model, audio_url,
  response_format="srt")` (or `"vtt"`, or `"verbose_json"` for timestamps).

If `generate_image` answers `in_progress` with a `job_id`, the model is slow:
poll `get_job` the same way.

## 5. Save, check, report

- Download at once; links expire in about 24 hours:
  `curl -L -o public/hero.png "<url>"`. Use the path and name the code expects,
  and ask before overwriting an existing file.
- Look at the preview (image tools return one) before wiring the file in. If it
  is off, change the prompt specifically ("camera lower, warmer light") rather
  than re-rolling blindly.
- Wire it in with the right dimensions and alt text.
- Tell the user: what was made, which model, what it cost (`cost_usd`), where
  it was saved.

## Errors

- Balance too low: the tool says so; `get_account` shows the balance. The user
  adds credit in the OceanToken console. Offer a cheaper model as the alternative.
- Parameter rejected: re-read `get_model` and use a listed value.
- Failed video jobs are not charged; the hold is released automatically.
- Reconnect prompt: the user's OceanToken sign-in or key was revoked; they need
  to reconnect the plugin.
