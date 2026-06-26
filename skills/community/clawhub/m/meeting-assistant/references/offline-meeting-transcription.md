# 离线会议转写 / Offline Meeting Transcription

当用户提供会议录音或会后文件时，使用 `POST https://api.senseaudio.cn/v1/audio/transcriptions`。
Use `POST https://api.senseaudio.cn/v1/audio/transcriptions` for uploaded meeting recordings.

## 适用场景 / Best Fit

- 会议录音、访谈、培训、电话会议的会后转写 / recorded meetings, calls, interviews, webinars
- 带说话人区分的会议文本整理 / speaker-separated transcripts
- 带时间戳的会议归档 / timestamped transcript export
- 转写同时输出目标语言翻译 / translation of meeting content during transcription

## 模型选择建议 / Recommended Model Choice

- `sense-asr-pro`：会议场景默认首选，适合说话人分离、情感分析、时间戳与翻译 / best default for meeting recordings needing diarization, sentiment, and timestamps
- `sense-asr`：支持翻译，也能覆盖部分增强需求，但会议增强能力弱于 Pro / supports translation with lighter meeting-focused controls
- `sense-asr-deepthink`：更适合偏翻译或语义理解场景；不要传 `language` / use when semantic translation is the priority; do not send `language`
- `sense-asr-lite`：如果需要翻译、说话人分离、时间戳或情感分析，不建议用于会议助手 / avoid for meeting assistants if you need translation, diarization, timestamps, or sentiment

## 接口信息 / Endpoint

- 地址 / URL：`https://api.senseaudio.cn/v1/audio/transcriptions`
- 方法 / Method：`POST`
- Content-Type：`multipart/form-data`
- 鉴权 / Auth：`Authorization: Bearer <SENSEAUDIO_API_KEY>`

## 必填参数 / Required Fields

- `file`：音频或视频文件，如 `wav`、`mp3`、`ogg`、`flac`、`aac`、`m4a`、`mp4`，大小不超过 `10MB` / audio or video file, `<=10MB`
- `model`：`sense-asr-lite`、`sense-asr`、`sense-asr-pro`、`sense-asr-deepthink` 之一

## 会议场景常用参数 / Meeting-Relevant Options

- `response_format`：`json`、`text`、`verbose_json`，会议场景优先 `verbose_json` / prefer `verbose_json`
- `language`：源语言提示，仅 `sense-asr-lite`、`sense-asr`、`sense-asr-pro` 支持 / source language hint
- `target_language`：目标翻译语言，Lite 不支持 / translated output language
- `enable_speaker_diarization=true`：开启说话人分离，`sense-asr` 和 `sense-asr-pro` 支持 / available on `sense-asr` and `sense-asr-pro`
- `max_speakers`：`1-20`，仅 `sense-asr-pro` 支持
- `enable_sentiment=true`：开启情感分析，`sense-asr` 和 `sense-asr-pro` 支持
- `timestamp_granularities[]`：推荐使用 `segment`，必要时加 `word` / use `segment` and optionally `word`
- `enable_punctuation=true`：自动标点，`sense-asr` 和 `sense-asr-pro` 支持
- `stream=true`：HTTP 流式返回，Lite 不支持 / optional streaming HTTP response

## 关键限制 / Important Constraints

- `sense-asr-deepthink` 不支持 `language` / does not support `language`
- `sense-asr-deepthink` 不支持部分其他模型可用的标点 / ITN 相关参数 / does not support punctuation or ITN-only options used by other models
- `max_speakers` 必须与 `enable_speaker_diarization=true` 搭配，并且只能用于 `sense-asr-pro`

## 会议录音推荐请求 / Recommended Request for Meetings

```bash
curl https://api.senseaudio.cn/v1/audio/transcriptions \
  -H "Authorization: Bearer $SENSEAUDIO_API_KEY" \
  -F "file=@meeting.wav" \
  -F "model=sense-asr-pro" \
  -F "response_format=verbose_json" \
  -F "enable_speaker_diarization=true" \
  -F "max_speakers=8" \
  -F "enable_sentiment=true" \
  -F "enable_punctuation=true" \
  -F "timestamp_granularities[]=segment" \
  -F "timestamp_granularities[]=word"
```

## 必须保留的响应字段 / Response Fields To Preserve

使用 `verbose_json` 时，后续流程中要保留这些字段。
In `verbose_json`, keep these fields through the whole pipeline.

- 顶层 `text` / top-level `text`
- 顶层 `duration` / top-level `duration`
- `segments[].start`
- `segments[].end`
- `segments[].speaker`
- `segments[].text`
- `segments[].sentiment`
- `segments[].translation`
- `words[]`（如果开启了字级时间戳） / when word timestamps are enabled

示例分段 / Example segment shape:

```json
{
  "id": 0,
  "start": 0.0,
  "end": 2.0,
  "text": "我们下周上线。",
  "speaker": "speaker_0",
  "sentiment": "positive",
  "translation": "We will launch next week."
}
```

## 推荐的归一化结构 / Normalized Transcript Schema

在进入总结、决策提取或行动项提取前，先整理成稳定结构。
Before summarization, normalize output into a meeting-safe structure such as:

```json
{
  "session_id": "optional",
  "duration": 5230,
  "language": "zh",
  "target_language": "en",
  "segments": [
    {
      "speaker": "speaker_0",
      "start": 0.0,
      "end": 2.0,
      "text": "我们下周上线。",
      "translation": "We will launch next week.",
      "sentiment": "positive"
    }
  ]
}
```

## 会议助手实现建议 / Meeting Assistant Guidance

- 以 `segments` 为准，不要只依赖整段 `text` / use `segments` as the source of truth for speaker turns
- `translation` 应作为并行字段保存，不要覆盖原始转写文本 / use `translation` as a parallel field, not a replacement
- 如果用户要会议纪要，先按说话人和主题对相邻片段做轻度聚合，再总结 / group adjacent segments by speaker and topic before summarizing
- 如果用户要行动项，优先从承诺句、分配句、截止日期句中提取，并保留原始时间点 / keep the source timestamp for action items
