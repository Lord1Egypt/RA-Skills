---
name: meeting-quality-scorer
description: >
  Objectively score meeting quality from a transcript. Three dimensions:
  decision clarity, time efficiency, participation balance. Outputs a
  Markdown report and an HTML visualization. Works with any
  OpenAI-compatible LLM endpoint (Ollama, DeepSeek, OpenAI, etc.).
  Pairs with meeting_whisper for a transcribe-then-score pipeline.
version: 1.0.0
author: ucsdzehualiu
license: MIT
trigger_keywords:
  - meeting-quality-scorer
  - meeting score
  - 会议评分
  - 会议质量
  - 会议有效性
  - score this meeting
  - rate the meeting
---

# meeting-quality-scorer

Score meeting quality from a transcript.

## Quick Start

```bash
pip install -r requirements.txt

# Score a meeting transcript
python scripts/score_meeting.py --input meeting.txt

# Or with custom output paths
python scripts/score_meeting.py --input meeting.txt --out-md my-report.md --out-html my-report.html
```

## Configuration

Set LLM backend via environment variables:
```bash
export MQS_BASE_URL=http://localhost:11434/v1  # Ollama
export MQS_API_KEY=ollama
export MQS_MODEL=qwen2.5:72b
```

Or create `~/.config/meeting-quality-scorer/config.yaml`:
```yaml
base_url: https://api.openai.com/v1
api_key: sk-...
model: gpt-4o-mini
```

## Three Dimensions

| Dimension | Weight | How scored |
|---|---|---|
| 决议明确度 | 40% | LLM detects topics + decisions + owners |
| 时间效率 | 30% | LLM identifies off-topic / filler segments |
| 参与均衡度 | 30% | Gini coefficient on speaker word counts |

If no speaker labels → participation skipped, weights redistribute to 60/40.

## Privacy

Transcript is sent only to your configured LLM endpoint. No telemetry.
