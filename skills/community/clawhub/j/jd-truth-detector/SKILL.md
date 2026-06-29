---
name: jd-truth-detector
description: >
  Reverse-engineer job descriptions: translate jargon ("5 years" → 3),
  infer company culture (red flags, vibes), match to your resume,
  detect negotiation signals. Outputs Markdown + shareable HTML report.
  Works with any OpenAI-compatible LLM (Ollama, DeepSeek, OpenAI, etc.).
  Supports text paste (primary), URL scraping (BOSS/拉勾/LinkedIn), and
  file input (.txt/.md/.docx/.pdf).
version: 1.0.0
author: ucsdzehualiu
license: MIT
trigger_keywords:
  - jd-truth-detector
  - JD 分析
  - 招聘分析
  - job description analysis
  - analyze this JD
  - 拆穿 JD
  - 解读 JD
  - JD 黑话
---

# jd-truth-detector

Reverse-engineer job descriptions across 4 dimensions: jargon translation, company culture inference, resume match analysis, negotiation signals.

## Quick Start

```bash
pip install -r requirements.txt

# Analyze from text
python scripts/jd_analyze.py --jd-text "<paste JD here>"

# From URL (experimental)
python scripts/jd_analyze.py --jd-url "https://www.zhipin.com/job_detail/..."

# With resume
python scripts/jd_analyze.py --jd-file jd.txt --resume-file resume.md
```

## Configuration

```bash
export JTD_BASE_URL=http://localhost:11434/v1
export JTD_API_KEY=ollama
export JTD_MODEL=qwen2.5:72b
```

Or `~/.config/jd-truth-detector/config.yaml`:
```yaml
base_url: https://api.deepseek.com/v1
api_key: sk-...
model: deepseek-chat
```

## Four Dimensions

| Dimension | What it does |
|---|---|
| 黑话翻译 | "5年经验" → 实际3年即可 |
| 公司体感 | 红旗词频率、技术成熟度、业务清晰度 |
| 简历匹配 | (可选) 对比 JD 和你的简历 |
| 议价信号 | 薪资透明度、职级明确性、急招信号 |

## Privacy

JD + resume sent only to your configured LLM endpoint. No telemetry.
