# Meeting Recorder Assistant

智能会议记录助手 - 录制、转录和分析会议，生成可操作的洞察。

## 功能特性

- **音频录制**: 带时间戳的会议音频录制
- **语音转文字**: 带说话人识别的音频转录
- **会议纪要**: 自动生成结构化会议摘要
- **行动项**: 从讨论中提取任务和分配
- **情感分析**: 分析会议氛围和参与度

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 录制和转录

```python
from scripts.meeting_recorder import MeetingRecorder

# 初始化录制器
recorder = MeetingRecorder()

# 开始录制
recorder.start_recording("/tmp/meeting_audio.wav")

# 停止并转录
transcript = recorder.stop_and_transcribe()
print(f"转录文本: {transcript['text']}")
```

### 生成会议纪要

```python
from scripts.meeting_minutes import generate_minutes

# 生成结构化纪要
minutes = generate_minutes(transcript_path="/tmp/transcript.json")
print(f"摘要: {minutes['summary']}")
print(f"行动项: {minutes['action_items']}")
```

### 提取行动项

```python
from scripts.action_extractor import extract_actions

# 从转录文本中提取任务
actions = extract_actions("/tmp/transcript.txt")
for action in actions:
    print(f"- {action['task']} (分配给: {action['assignee']})")
```

## 支持的音频格式

- WAV
- MP3
- M4A
- OGG

## 输出格式

- JSON (结构化数据)
- Markdown (会议纪要)
- TXT (转录文本)
