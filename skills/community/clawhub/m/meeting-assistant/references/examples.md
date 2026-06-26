# 示例 / Examples

## 1. 实时双语会议字幕 / Realtime bilingual meeting captions

会中使用 WebSocket 输出实时字幕，会后基于完整转写生成纪要。
Use WebSocket for live captions during a meeting, then summarize afterwards.

```python
session = start_realtime_meeting(
    api_key=os.environ["SENSEAUDIO_API_KEY"],
    target_language="en"
)
for pcm_chunk in microphone_stream():
    session.send_audio(pcm_chunk)
transcript = session.finish()
notes = summarize_meeting(transcript)
```

## 2. 上传录音并生成会议纪要 / Upload a recording and generate meeting minutes

先使用 HTTP 转写拿到带说话人分离的结果，再基于 `segments` 生成纪要。
Use HTTP transcription with speaker diarization, then generate notes from `segments`.

```python
transcript = transcribe_meeting(
    file_path="meeting.wav",
    model="sense-asr-pro",
    enable_speaker_diarization=True,
    max_speakers=6,
    timestamps=["segment", "word"]
)
notes = build_meeting_notes(transcript)
```

## 3. 实时优先，会后精修 / Realtime first, offline second

这是更推荐的生产方案。
Recommended for production meeting assistants.

1. 会中使用 WebSocket 输出实时字幕 / WebSocket during the meeting for live captions
2. 同时保存原始会议录音 / save raw meeting audio
3. 会后将完整录音交给 `sense-asr-pro` 再处理一次 / re-run the full recording through `sense-asr-pro`
4. 基于离线精修结果生成最终纪要、决策和行动项 / generate final notes, decisions, and action items from offline transcript

## 4. 转写前做音质预检 / Audio quality precheck before transcription

如果用户反馈识别质量差，先调用音频质量分析接口。
If recognition quality is poor, analyze the file first.

```bash
curl -X POST https://api.senseaudio.cn/v1/audio/analysis \
  -H "Authorization: Bearer $SENSEAUDIO_API_KEY" \
  -F "model=sense-asr-check" \
  -F "file=@meeting.wav"
```

如果返回 `has_noise=true` 或严重程度较高，要提前提醒用户：说话人分离、时间戳和纪要质量都可能受影响。
If `has_noise=true` or the severity is high, tell the user to expect weaker diarization and notes.

## 5. 查询历史会议转写记录 / Query historical meeting transcripts

```bash
curl --location --request GET "https://api.senseaudio.cn/v1/audio/records?page=1&page_size=20&session_id=<SESSION_ID>" \
  -H "Authorization: Bearer $SENSEAUDIO_API_KEY"
```

适用于用户希望在保留期内查询过去的识别结果。
Use this when the user wants to fetch a past transcript within the retention window.
