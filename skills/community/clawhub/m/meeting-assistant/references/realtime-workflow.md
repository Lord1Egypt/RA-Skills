# 实时会议工作流 / Realtime Workflow

当用户需要实时字幕、会中转写或实时翻译时，使用 `wss://api.senseaudio.cn/ws/v1/audio/transcriptions`。
Use `wss://api.senseaudio.cn/ws/v1/audio/transcriptions` for live meeting assistants.

## 适用场景 / Best Fit

- 会议实时字幕 / live captions during meetings
- 双语会议字幕 / bilingual meeting subtitles
- 会议软件中的实时转写面板 / realtime transcript panels in conferencing tools
- 会中展示字幕、会后再生成纪要的会议助手 / meeting copilot apps that summarize after the meeting ends

## 连接要求 / Connection Requirements

- 地址 / URL：`wss://api.senseaudio.cn/ws/v1/audio/transcriptions`
- 鉴权请求头 / Auth header：`Authorization: Bearer <SENSEAUDIO_API_KEY>`
- 模型 / Model：当前文档给出的实时模型为 `sense-asr-deepthink`
- 音频格式 / Audio format：原始 `pcm`、`16000Hz`、`1` 声道、16-bit little-endian

## 事件顺序 / Event Order

1. 建立 WebSocket 连接，等待 `connected_success` / open WebSocket and wait for `connected_success`
2. 发送 `task_start` / send `task_start`
3. 等待 `task_started` / wait for `task_started`
4. 持续发送二进制音频数据 / stream binary audio chunks
5. 接收 `result_final` 作为最终片段结果 / read `result_final` events for finalized segments
6. 音频发送完成后发送 `task_finish` / send `task_finish`
7. 等待 `task_finished` / wait for `task_finished`
8. 如果收到 `task_failed`，按失败流程处理 / handle `task_failed` as terminal failure

## `task_start` 示例 / `task_start` Payload

```json
{
  "event": "task_start",
  "model": "sense-asr-deepthink",
  "audio_setting": {
    "sample_rate": 16000,
    "format": "pcm",
    "channel": 1
  },
  "vad_setting": {
    "silence_duration": 500,
    "min_speech_duration": 300
  },
  "transcription_setting": {
    "target_language": "en",
    "recognize_mode": "auto"
  }
}
```

## 参数说明 / Payload Options

### `audio_setting`

- `sample_rate`：必须为 `16000` / must be `16000`
- `channel`：必须为 `1` / must be `1`
- `format`：必须为 `pcm` / must be `pcm`

### `vad_setting`

会议场景可先使用以下默认值。
Useful defaults for meetings.

- `silence_duration=500`
- `min_speech_duration=300`
- `soft_max_duration=15000`
- `hard_max_duration=30000`
- `soft_silence_duration=300`
- `threshold=0.5`

如果希望字幕更灵敏，可适当调小静音切分阈值；如果句子被切得太碎，可适当调大。
Tighten silence thresholds for snappier captions; relax them for fewer sentence splits.

### `transcription_setting`

- `target_language`：目标翻译语言，例如 `en`、`zh`、`ja` / translated output language
- `recognize_mode`：`auto` 或 `record_only`

如果只想做普通转写，不希望语音中的“帮我翻译成英文”之类指令触发转译行为，优先用 `record_only`。
Use `record_only` when you want straight transcription and do not want instruction-like speech to trigger translation behavior.

## 关键服务端事件 / Important Server Events

### `connected_success`

表示连接和鉴权已通过。
Connection handshake succeeded.

### `task_started`

表示服务端已接受任务配置，可以开始发送音频流。
The server accepted meeting session settings and is ready for binary audio.

### `result_final`

每个最终识别片段会以类似结构返回。
Each finalized segment arrives as:

```json
{
  "event": "result_final",
  "session_id": "trace-id-xxx",
  "data": {
    "text": "你好，今天天气真不错。",
    "is_final": true,
    "segment_id": 1,
    "timestamp_end": 1773027072669
  },
  "base_resp": {
    "status_code": 0,
    "status_msg": "success"
  }
}
```

把 `result_final` 视为可追加的最终分段结果，不要当作临时草稿。
Treat `result_final` as append-only finalized transcript chunks.

### `task_failed`

表示任务失败。重点检查 `base_resp.status_code` 与 `base_resp.status_msg`。
Terminal failure. Inspect `base_resp.status_code` and `base_resp.status_msg`.

## 流式发送建议 / Streaming Guidance

- 以约 `100ms` 一包的频率发送；文档示例是每次发送 `3200` 字节 / send roughly 100ms chunks
- 不要把带文件头的 `wav` 或压缩后的 `mp3` 字节直接发到 WebSocket 接口 / do not send WAV headers or compressed bytes
- 实时阶段持续缓存最终片段，供会后摘要使用 / keep a buffer of finalized segments for summarization
- 在日志中保留 `session_id` 和 `trace_id`，方便排障 / store identifiers in logs

## 最小 Python 模式 / Minimal Python Pattern

```python
import asyncio
import json
import os
import websockets

API_KEY = os.environ["SENSEAUDIO_API_KEY"]
WS_URL = "wss://api.senseaudio.cn/ws/v1/audio/transcriptions"

async def run_meeting_ws(audio_path: str):
    headers = {"Authorization": f"Bearer {API_KEY}"}
    async with websockets.connect(WS_URL, additional_headers=headers) as ws:
        await ws.recv()
        await ws.send(json.dumps({
            "event": "task_start",
            "model": "sense-asr-deepthink",
            "audio_setting": {"sample_rate": 16000, "format": "pcm", "channel": 1},
        }))
        await ws.recv()

        with open(audio_path, "rb") as audio_file:
            while chunk := audio_file.read(3200):
                await ws.send(chunk)
                await asyncio.sleep(0.1)

        await ws.send(json.dumps({"event": "task_finish"}))
```

## 会议助手实现建议 / Meeting Assistant Guidance

- 从文档给出的事件结构看，实时接口返回的是分段结果，不是完整的会议纪要 / WS results are segment-like, not complete meeting notes
- 当前文档没有把说话人分离作为实时返回字段明确给出；如果必须区分说话人，建议会后再用 `sense-asr-pro` 对录音做离线精修 / use offline `sense-asr-pro` if speaker separation is mandatory
- 最推荐的生产方案是：会中使用 WebSocket 出实时字幕，会后用 HTTP 离线转写生成最终归档与纪要 / combine WS captions with post-meeting HTTP reprocessing
