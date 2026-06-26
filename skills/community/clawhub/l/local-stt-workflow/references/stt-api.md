# STT API 调用文档

本文档对应 `/v1/audio/transcriptions`、`/v1/audio/translations` 与 STT 相关模型管理接口，适用于仅启用 STT 或同时启用 TTS/STT 的服务实例。

## 服务启用方式

通过环境变量 `MLX_AUDIO_SERVER_TASKS` 控制能力：

- `tts`：仅启用 TTS
- `stt`：仅启用 STT
- `all` / `audio` / `tts,stt`：启用全部能力

示例：

```bash
MLX_AUDIO_SERVER_TASKS=stt uv run python server.py
```

## 通用接口

### `GET /`

返回服务状态与已启用任务。

### `GET /health`

返回健康状态。

### `GET /v1/models`

列出当前已注册模型。

响应 schema：

```json
{
 "object": "list",
 "data": [ModelCard]
}
```

其中 `ModelCard` 结构为：

```json
{
 "id": "string",
 "object": "model",
 "created": 1710000000,
 "owned_by": "local",
 "task": "stt",
 "source": "Qwen/Qwen3-ASR-4B-Instruct-2507",
 "loaded": true
}
```

### `POST /v1/models`

注册 STT 模型。

请求 schema：

```json
{
 "model_id": "string",
 "task": "stt",
 "source": "string | null",
 "preload": true
}
```

## 当前实现审计结论

基于当前实现，可确认：

- `/v1/audio/transcriptions` 已优先按 OpenAI Audio API 客户端的 `multipart/form-data` 习惯兼容
- `language` 会传给 STT 模型，默认回退为 `auto`
- `prompt` 不再直接丢弃；当前会作为 `context` 的后备值，在模型签名允许时透传
- `timestamp_granularities[]` 只在服务端用于控制返回结构，不会下传给模型
- `include[]` 已支持 OpenAI 风格数组字段解析，但当前仅接受 `logprobs`；其余值会直接报错
- `stream=true` 时返回 SSE：`transcript.text.delta` / `transcript.text.done`
- `context`、`prefill_step_size`、`chunk_duration`、`frame_threshold`、`max_tokens`、`text` 会在模型签名允许时透传
- `temperature` 目前仍仅为兼容字段，不参与实际推理
- 翻译接口固定通过 `task="translate"` 调用 STT 模型
- 仍依赖签名过滤，因此不同 STT 模型之间仍可能存在“传入但被静默忽略”的差异
- 本轮没有实现 OpenAI 文档中的 `Improving reliability` 相关增强逻辑

## 语音转写接口

### `POST /v1/audio/transcriptions`

`multipart/form-data` 表单字段完整 schema：

```json
{
 "file": "binary",
 "model": "string",
 "language": "string | null",
 "prompt": "string | null",
 "response_format": "json",
 "temperature": null,
 "timestamp_granularities[]": ["segment", "word"],
 "include[]": ["logprobs"],
 "stream": false,
 "verbose": false,
 "max_tokens": 1024,
 "chunk_duration": 30.0,
 "frame_threshold": 25,
 "context": "string | null",
 "prefill_step_size": 2048,
 "text": "string | null"
}
```

字段说明：

- `file`：上传的音频文件
- `model`：已注册 STT 模型 ID
- `language`：识别语言，默认 `auto`
- `prompt`：OpenAI 兼容字段；当前作为 `context` 的后备值，在模型签名支持时透传
- `response_format`：支持 `json`、`text`、`verbose_json`、`srt`、`vtt`
- `temperature`：兼容字段，当前服务端不参与推理
- `timestamp_granularities[]`：支持 `segment`、`word`；兼容多种 OpenAI 风格传法；仅影响服务端返回结构
- `include[]`：当前仅接受 `logprobs`，但本地 Qwen3-ASR 还没有实际返回 logprobs
- `stream`：是否流式返回 SSE
- `verbose`：是否请求模型输出更详细结果
- `max_tokens`：仅在模型签名支持时透传
- `chunk_duration`：仅在模型签名支持时透传
- `frame_threshold`：仅在模型签名支持时透传
- `context`：仅在模型签名支持时透传
- `prefill_step_size`：仅在模型签名支持时透传
- `text`：仅在模型签名支持时透传

### 请求示例

```bash
curl -X POST http://127.0.0.1:8000/v1/audio/transcriptions \
 -F file=@sample.wav \
 -F model=qwen3-asr \
 -F response_format=verbose_json \
 -F 'timestamp_granularities[]=segment' \
 -F 'timestamp_granularities[]=word'
```

OpenAI Python 客户端调用形态示例：

```python
from openai import OpenAI

client = OpenAI(base_url="http://127.0.0.1:8000/v1", api_key="dummy")

with open("sample.wav", "rb") as audio_file:
    transcript = client.audio.transcriptions.create(
        model="qwen3-asr",
        file=audio_file,
        response_format="verbose_json",
        timestamp_granularities=["word"],
    )

print(transcript.text)
```

## 响应格式

### `response_format=json`

返回：

```json
{
 "text": "识别出的文本"
}
```

### `response_format=text`

返回纯文本 `text/plain`。

### `response_format=verbose_json`

服务端会规范化结果，常见结构如下：

```json
{
 "text": "识别出的文本",
 "language": "Chinese",
 "words": [
   {
     "text": "识别",
     "start": 0.0,
     "end": 0.5,
     "duration": 0.5
   }
 ],
 "segments": [
   {
     "id": 0,
     "start": 0.0,
     "end": 2.5,
     "text": "识别出的文本",
     "words": [
       {
         "text": "识别",
         "start": 0.0,
         "end": 0.5,
         "duration": 0.5
       }
     ]
   }
 ],
 "sentences": [
   {
     "text": "识别出的文本",
     "start": 0.0,
     "end": 2.5,
     "duration": 2.5,
     "speaker_id": 0,
     "tokens": []
   }
 ]
}
```

说明：

- `language` 为服务端归一化后的语言名，不一定保持上游原始值
- 只有当模型实际返回 `segments` / `words` / `sentences` 时，这些字段才会出现
- 请求 `timestamp_granularities[]=word` 时，服务端会尝试把 `segments[].words` 扁平展开到顶层 `words`
- 若模型本身没有 word 级时间戳数据，而你请求了 `word`，服务端会报错，而不是伪造空数据

### `response_format=srt`

服务端会把 `segments` 渲染为 SRT 文本；若模型未返回分段，则结果可能为空。

### `response_format=vtt`

服务端会把 `segments` 渲染为 WebVTT 文本；若模型未返回分段，则结果可能为空。

### `stream=true`

返回 `text/event-stream`，至少会发出：

#### `transcript.text.delta`

```text
event: transcript.text.delta
data: {"type":"transcript.text.delta","delta":"片段文本"}
```

#### `transcript.text.done`

```text
event: transcript.text.done
data: {"type":"transcript.text.done","text":"完整文本"}
```

说明：

- 当前仅对 `response_format=json` 与 `response_format=text` 开放流式模式
- 当前没有实现 diarization 相关流式事件
- 事件负载优先追求 OpenAI 风格兼容，不等于 OpenAI 的全量字段集合

## 语音翻译接口

### `POST /v1/audio/translations`

`multipart/form-data` 表单字段 schema：

```json
{
 "file": "binary",
 "model": "string",
 "response_format": "json",
 "verbose": false,
 "max_tokens": 1024,
 "chunk_duration": 30.0,
 "frame_threshold": 25
}
```

说明：

- 内部会以 `task=translate` 调用 STT 模型生成
- 返回结构复用转写响应规范化逻辑
- 当前翻译接口不支持 `stream`、`timestamp_granularities`、`context`、`prefill_step_size`
- 是否具备高质量翻译能力，取决于底层模型

请求示例：

```bash
curl -X POST http://127.0.0.1:8000/v1/audio/translations \
 -F file=@sample.wav \
 -F model=qwen3-asr \
 -F response_format=json
```

## 错误响应 schema

统一错误结构：

```json
{
 "error": {
   "message": "Unsupported response_format 'xml'.",
   "type": "invalid_request_error",
   "param": "response_format",
   "code": "unsupported_response_format"
 }
}
```

## 当前限制

- 尚未建立完整的分模型 capability 白名单
- 仍存在基于签名过滤的静默降级行为
- `temperature` 仍仅为兼容字段，不参与实际推理
- `include[]` 当前只做有限兼容，尚未输出真实 `logprobs`
- 未实现 OpenAI 文档中的 diarization 能力
- 未实现 `Improving reliability` 一节中的增强能力
- 当前兼容目标聚焦在 `transcriptions` / `translations` 的常用文件上传路径，不包含 Realtime transcription
