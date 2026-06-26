# Telegram / openclaw Workflow

## Goal

Convert Telegram voice input into text for openclaw, then convert the final concise reply back into Telegram-compatible voice.

## Supported modes

This skill supports three modes:

1. **Telegram/openclaw voice workflow**
2. **Direct text-to-speech**
3. **Direct speech-to-text**

---

## Mode 1: Telegram/openclaw voice workflow

### 1. Receive Telegram voice message

Input is usually one of:
- Telegram voice file path
- downloaded local OGG file
- downloaded local audio file in another format

### 2. Run ASR

Call Liber SpeechAPI ASR with:
- `file=<local audio file>`
- `language=<configured language>`
- `task=transcribe`
- `timestamps=chunk`

Extract:
- `text`

### 3. Send transcript to openclaw

Use the ASR transcript as the user message for the chatbot workflow.

### 4. Produce final textual reply

Let openclaw generate the full answer first.

### 5. Compress for voice

If the final answer is too long for a natural voice reply:
- summarize it to within 100 Chinese characters
- keep the direct answer, essential facts, and next action
- remove markdown, long examples, code, and repeated explanation

### 6. Run TTS

Call Liber SpeechAPI TTS with:
- `text=<voice-ready text>`
- `model=<configured model>`
- `language=<configured language>`
- `format=ogg_opus`

If clone audio is enabled:
- include `audio_prompt=<configured file>`

### 7. Return audio to Telegram

Use the returned `audio_url` or downloaded file to send a Telegram voice message.

---

## Mode 2: Direct text-to-speech

Use this mode when the user explicitly asks to convert text into audio.

Default behavior:
- default output format: `wav`
- do not force summarization unless the caller requests a short spoken version
- use clone audio only when enabled and the file exists

Examples:
- “把这段文字转成语音”
- “把这段回复合成为 wav”
- “朗读这段文字并输出音频”

---

## Mode 3: Direct speech-to-text

Use this mode when the user explicitly asks to convert audio into text.

Default behavior:
- default output mode: `json`
- return plain `text` only when explicitly requested

Examples:
- “把这段录音转文字”
- “识别这段音频并返回 JSON”
- “帮我做语音转文字”

---

## Compression guidance

Good spoken reply:
- short
- direct
- natural
- no markdown formatting
- no code syntax
- no excessive detail

Example:

Original:
- “这个问题通常是因为 API 地址配置错误、鉴权失败，或者 OGG/Opus 文件没有正确生成。建议先检查 health 接口，再核对 API key，最后确认 TTS format 是否为 ogg_opus。”

Compressed:
- “可能是地址、鉴权或音频格式有误。先检查 health、API key，并确认 TTS 输出为 ogg_opus。”

---

## Failure strategy

### ASR failure
- return plain error text
- optionally ask the user to resend clearer audio

### Summarization failure
- conservatively trim text to the configured limit

### TTS failure
- return plain text reply instead of blocking the whole chatbot response

### Clone-audio missing
- continue without cloning
