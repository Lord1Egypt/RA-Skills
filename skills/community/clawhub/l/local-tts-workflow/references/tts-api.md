# TTS API 调用文档

本文档对应 `/v1/audio/speech` 与 TTS 相关模型管理接口，适用于仅启用 TTS 或同时启用 TTS/STT 的服务实例。

## 服务启用方式

通过环境变量 `MLX_AUDIO_SERVER_TASKS` 控制能力：

- `tts`：仅启用 TTS
- `stt`：仅启用 STT
- `all` / `audio` / `tts,stt`：启用全部能力

示例：

```bash
MLX_AUDIO_SERVER_TASKS=tts uv run python server.py
```

## 自定义语音上传接口

### `POST /v1/audio/voice_consents`

该接口用于上传 consent-based clone 所需的参考音频，并额外支持 `ref_text`。

```bash
curl http://127.0.0.1:8000/v1/audio/voice_consents \
 -X POST \
 -F 'name=test_consent' \
 -F 'language=en' \
 -F 'recording=@./consent_recording.wav;type=audio/x-wav' \
 -F 'ref_text=This is my consent recording.'
```

表单字段：

- `name`：自定义语音名称，也是后续 consent-based clone 使用的外部 `voice.id`
- `language`：支持语言名或两字代码，例如 `Chinese`/`zh`、`English`/`en`
- `recording`：录音文件
- `ref_text`：推荐必填；对 Base clone 来说，只有同时具备 `ref_audio` 与 `ref_text` 才能进入标准 ICL clone 路径

服务端持久化规则：

- 音频保存为 `voices/name.wav`（保留上传文件后缀）
- 元数据保存为 `voices/name.json`
- JSON 中记录：`id`、`language`、`ref_text`、`recording`

响应示例：

```json
{
 "id": "test_consent",
 "object": "voice_consent",
 "created": 1710000000,
 "name": "test_consent",
 "language": "English",
 "recording": "/absolute/path/to/voices/test_consent.wav",
 "metadata": "/absolute/path/to/voices/test_consent.json"
}
```

## 文本转语音接口

### `POST /v1/audio/speech`

建议显式带上 `Content-Type: application/json`。

### vLLM Omni 对齐备注

vLLM Omni 的 Speech API 也是 OpenAI-compatible 的 `/v1/audio/speech`，但它的文档语义更接近“每个服务实例只跑一个模型”。对 Qwen3-TTS CustomVoice，官方示例直接使用：

- `model`: `Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice`
- `voice`: `vivian`
- `input`: 文本
- `language`: `English`

这说明至少在 vLLM Omni 语义里：

- `voice` 允许是**纯字符串**，不一定非得是 `{ "id": "..." }`
- `CustomVoice` 的 speaker 选择主要通过 `voice` 表达
- 响应默认可直接作为音频文件落盘

如果你的服务后端已经迁到 vLLM 主机，优先验证它接受的是：

1. `voice: "lj"`
2. 还是 `voice: {"id":"lj"}`
3. 以及它是否要求完整模型名 vs 本地别名/路径别名

请求体常见 schema：

```json
{
 "model": "string",
 "voice": {
   "id": "string"
 },
 "input": "string",
 "instructions": "string | null",
 "language": "fr",
 "format": "wav",
 "ref_audio": "string | null",
 "ref_text": "string | null",
 "custom_voice": {
   "speaker": "string"
 }
}
```

基础字段说明：

- `model`：已注册的 TTS 模型 ID
- `input`：待合成文本
- `voice`：支持字符串，也支持 `{ "id": "..." }`
- `instructions`：风格指令；对 VoiceDesign 则是必填的音色描述
- `language`：语言提示；未提供时服务会按当前模式回退默认值或 consent 元数据
- `format`：推荐字段，同时兼容旧字段 `response_format`
- `stream`：是否启用流式推理；默认不传时按 OpenAI 风格走流式响应
- `stream_format`：`audio` 或 `event`，默认 `audio`
- `streaming_interval`：增量解码间隔，默认值偏低延迟
- `ref_audio` / `ref_text`：显式 clone 输入；对 Base clone 必须同时提供
- `custom_voice`：当前仅用于兼容旧请求形态

## 流式与非流式行为

### 默认行为

- 如果不传 `stream`，服务默认按流式响应处理
- 如果需要整段完成后一次性返回完整音频，请显式传 `"stream": false`

### 非流式

- `stream=false` 时返回完整音频
- 支持 `mp3`、`opus`、`aac`、`flac`、`wav`、`pcm`

### 真正流式推理

当前实现直接使用增量生成能力，不是整段生成后再切片伪流式。

可选 warmup 环境变量：

```bash
MLX_AUDIO_KEEP_LOADED=tts
MLX_AUDIO_TTS_WARMUP=1
MLX_AUDIO_TTS_STREAMING_INTERVAL=0.25
```

支持两种流式返回模式：

#### `stream_format="audio"`

- 返回原始音频字节流
- 支持 `format="pcm"` 与 `format="wav"`
- `pcm` 延迟最低
- `wav` 采用单个连续 WAV 响应头 + 持续 PCM 数据输出

示例：

```bash
curl http://127.0.0.1:8000/v1/audio/speech \
 -H 'Content-Type: application/json' \
 -X POST \
 -d '{
 "model": "qwen3-tts-base",
 "voice": {"id": "Chelsie"},
 "input": "你好，这是实时流式语音合成测试。",
 "format": "wav",
 "stream": true,
 "stream_format": "audio",
 "streaming_interval": 1.0
 }' \
 | ffplay -i -
```

强制非流式：

```bash
curl http://127.0.0.1:8000/v1/audio/speech \
 -X POST \
 -H 'Content-Type: application/json' \
 -d '{
 "model": "qwen3-tts-base",
 "voice": {"id": "Chelsie"},
 "input": "你好，这是一次性返回完整音频的测试。",
 "format": "wav",
 "stream": false
 }' \
 --output sample.wav
```

#### `stream_format="event"`

- 返回 `text/event-stream`
- 每个 SSE event 都包含 base64 音频 chunk、序号、采样率、格式、是否 final
- 适合前端、网关或自定义播放器消费

事件示例：

```text
event: audio.chunk
data: {"type":"audio.chunk","index":0,"format":"pcm","sample_rate":24000,"audio":"...base64...","is_final":false}

event: audio.completed
data: {"type":"audio.completed","format":"pcm","chunks":4}
```

## 当前已建模的四种模式

服务端会先识别模型类型，再解析请求模式，并在响应头返回：

- `X-TTS-Mode`
- `X-TTS-Model-Type`
- `X-Model-Language`
- `X-Style-Instruct-Applied`

### 1. Base speaker

适用条件：

- 模型类型为 `base`
- 请求未提供完整 `ref_audio + ref_text`
- `voice.id` 被解释为模型内置 speaker

### 2. Base clone

适用条件：

- 模型类型为 `base`
- 请求存在完整 `ref_audio + ref_text`
- `voice.id` 若提供，仅作为外部 identity

支持两种来源：

1. 显式提供 `ref_audio` 与 `ref_text`
2. 仅提供 `voice.id` / `custom_voice.id`，由服务端从 consent 存储中回填参考音频与参考文本

关键约束：

- 若只有 `ref_audio` 没有 `ref_text`，服务会直接返回错误

### 3. CustomVoice

适用条件：

- 模型类型为 `custom_voice`
- 请求使用预置 speaker
- 可选传 `instructions` 控制风格

当前语义：

- `voice` 或 `custom_voice.speaker` 表示模型内置 speaker
- 在一些 OpenAI-compatible 实现（例如 vLLM Omni 文档）里，`voice` 直接就是字符串，而不是对象
- 不接受 clone 风格 `ref_audio` / `ref_text`
- 不接受 consent-based clone 载荷

本 workspace 的硬规则：

- `lj-qwen3-tts` 是 CustomVoice 模型
- 要得到正确音色，必须显式指定 speaker/voice `lj`

### 4. VoiceDesign

适用条件：

- 模型类型为 `voice_design`
- 必须提供 `instructions`
- 不允许提供 `voice`、`ref_audio`、`ref_text` 或 consent/custom clone 载荷

## `voice.id` 的语义边界

- 在 Base speaker 中，`voice.id` 表示模型内置 speaker 名
- 在 Base clone 中，`voice.id` 表示服务器保存的外部 voice identity
- 在 CustomVoice 中，`voice.id` 表示模型内置 speaker 名
- 在 VoiceDesign 中，不允许传 `voice`

## 常见错误场景

### clone 缺少 `ref_text`

返回 `400`，典型错误码：`missing_required_parameter`

```json
{
 "error": {
   "message": "Base clone requires both 'ref_audio' and 'ref_text'. Upload voice consent with ref_text or provide both fields explicitly.",
   "type": "invalid_request_error",
   "param": "ref_text",
   "code": "missing_required_parameter"
 }
}
```

### 模型类型与请求模式不匹配

例如对 CustomVoice 模型传入 clone 风格载荷，会返回 `400`，错误码 `model_mode_mismatch`。

### speaker 与 consent id 混用

例如同时传不一致的 `voice.id` 与 `custom_voice.id`，会返回 `400`，错误码 `conflicting_parameters`。

### VoiceDesign 缺少 `instructions`

会返回 `400`，错误码 `missing_required_parameter`。

## TTS-only 模式说明

仅启用 TTS 时，健康状态显示 `stopped` 仍可能是正常的，这表示尚未配置活动模型，不代表进程崩溃。