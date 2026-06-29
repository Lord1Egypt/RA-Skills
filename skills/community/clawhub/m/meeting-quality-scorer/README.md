# meeting-quality-scorer

Objectively score meeting quality from a transcript. Analyzes decision clarity, time efficiency, and participation balance to identify ineffective meetings and produce actionable reports.

## Overview

**meeting-quality-scorer** evaluates meeting transcripts across three quantitative dimensions:

- **Decision Clarity** (40%): Did discussion topics end with clear decisions, owners, and deadlines?
- **Time Efficiency** (30%): How much time was spent on filler or off-topic content?
- **Participation Balance** (30%): Was speaking time distributed evenly among participants?

Outputs include a Markdown report and an HTML visualization with Chart.js radar and bar charts. Works with any OpenAI-compatible LLM endpoint (OpenAI, DeepSeek, Ollama, Moonshot, GLM, Tongyi, vLLM).

Designed to pair with transcription tools like `meeting_whisper` for a complete transcribe-then-score pipeline.

## Installation

```bash
pip install -r requirements.txt
```

**Dependencies:**
- `openai>=1.30.0`
- `pyyaml>=6.0`
- `jinja2>=3.1.0`
- `pytest>=8.0.0`

No native dependencies. Total install size < 30 MB.

## Configuration

The tool requires LLM endpoint configuration. Three configuration methods (priority order):

### 1. Environment Variables

```bash
export MQS_BASE_URL="https://api.openai.com/v1"
export MQS_API_KEY="sk-..."
export MQS_MODEL="gpt-4o-mini"
```

### 2. Config File

Create `~/.config/meeting-quality-scorer/config.yaml`:

```yaml
base_url: "https://api.openai.com/v1"
api_key: "sk-..."
model: "gpt-4o-mini"
timeout: 60
```

Or specify a custom path with `--config`:

```bash
python scripts/score_meeting.py --input meeting.txt --config /path/to/config.yaml
```

### 3. Configuration Table

| Variable | Config Key | Required | Default | Description |
|----------|-----------|----------|---------|-------------|
| `MQS_BASE_URL` | `base_url` | Yes | None | LLM API endpoint (e.g., `http://localhost:11434/v1` for Ollama) |
| `MQS_API_KEY` | `api_key` | Yes | None | API key (use `"ollama"` for local Ollama) |
| `MQS_MODEL` | `model` | Yes | None | Model name (e.g., `qwen2.5:72b`, `gpt-4o-mini`) |
| N/A | `timeout` | No | 60 | Timeout per LLM call in seconds |

**Priority:** Environment variables override config file values.

**Note:** If configuration is incomplete, the tool exits with code 2 and displays help text.

## Usage

### Basic Usage

```bash
python scripts/score_meeting.py \
  --input meeting.txt \
  --out-md report.md \
  --out-html report.html
```

### With Custom Config

```bash
python scripts/score_meeting.py \
  --input meeting.txt \
  --config ~/.config/meeting-quality-scorer/config.yaml
```

### Using Ollama Locally

```bash
MQS_BASE_URL=http://localhost:11434/v1 \
MQS_API_KEY=ollama \
MQS_MODEL=qwen2.5:72b \
python scripts/score_meeting.py --input meeting.txt
```

### Input Format

The tool accepts transcript text in two formats:

**Labeled** (recommended, enables all 3 dimensions):
```
Alice: Let's discuss the Q3 budget increase.
Bob: I propose we allocate 20% more to marketing.
Alice: Agreed. Bob, can you draft the proposal by Aug 15?
Bob: Yes, I'll handle it.
```

**Plain** (degraded mode, 2 dimensions only):
```
The team discussed Q3 budget. Someone proposed increasing 
marketing spend by 20%. Agreement was reached and a proposal 
deadline of Aug 15 was set.
```

Supported labeled formats:
- Simple: `Name: text`
- Numbered: `SPEAKER_01: text`
- WhisperX: `[00:01:23.45 --> 00:01:26.78] SPEAKER_02: text`
- CJK: `张三: 今天讨论...`

**Format Detection:** A transcript is classified as `labeled` if ≥30% of non-empty lines match a speaker label pattern.

## Scoring Dimensions

| Dimension | Weight | Formula | Range | Description |
|-----------|--------|---------|-------|-------------|
| **Decision Clarity** | 40% | `100 × (decided_with_owner / total_topics)` | 0–100 | Percentage of discussion topics that ended with a clear decision, assigned owner, and optional deadline. LLM-driven. |
| **Time Efficiency** | 30% | `100 × (1 - filler_windows / total_windows)` | 0–100 | Percentage of meeting time spent on-topic. Rule-based detection + LLM verification for filler/off-topic content. |
| **Participation Balance** | 30% | `100 × (1 - Gini)` | 0–100 or N/A | Speaking time distribution evenness. Computed via Gini coefficient on character counts per speaker. Only available with labeled transcripts. |

**Total Score:** Weighted average of the three dimensions.

### Scoring Example

```
Decision Clarity: 75/100 (3 of 4 topics decided)
Time Efficiency: 85/100 (15% filler detected)
Participation Balance: 60/100 (moderate imbalance)

Total: 72.5/100
  = 0.40 × 75 + 0.30 × 85 + 0.30 × 60
  = 30 + 25.5 + 18
```

## Degraded Mode

When the transcript has no speaker labels (plain format), Participation Balance cannot be computed.

**Behavior:**
- Participation Balance: reported as `N/A`
- Total score uses 2-dimension weights: **Decision 60% + Time 40%**
- Report includes a banner: *"参与均衡度未评估 — 输入转录无说话人标签。要获得完整评分，请用 WhisperX 或带 diarization 的转录工具重新转录。"*

**Upgrade Path:** Re-transcribe with a diarization-capable tool (WhisperX, Azure Speech, Google Speech-to-Text with diarization enabled) to unlock the full 3-dimension score.

## Failure Modes

| Situation | Behavior | Exit Code |
|-----------|----------|-----------|
| Transcript < 100 characters | Error: "transcript too short to score" | 2 |
| Transcript > 200,000 characters | Error: "transcript too long" (hint: chunk and average) | 2 |
| Missing configuration | Error with help text listing env vars and config paths | 2 |
| LLM API unreachable (timeout, 5xx after 3 retries) | Save partial scores (rule-based dimensions) to `partial-report.md` | 1 |
| LLM returns malformed JSON | Retry once with stricter prompt; if still fails, mark dimension as "evaluation failed" | 0 (partial) |
| 0 discussion topics detected | Decision Clarity = N/A with banner explanation | 0 |
| Single speaker only | Participation Balance = N/A (monologue) | 0 |
| Missing `--input` argument | Argument parsing error | 2 |

## Limitations

### What This Tool Can Do

- Score structural meeting quality (decisions, time use, balance)
- Detect filler and off-topic content via rules + LLM verification
- Highlight under-utilized participants
- Process transcripts in English, Chinese, or mixed languages
- Handle meetings up to ~3 hours (~200k characters)

### What This Tool Cannot Do

- **Audio input:** Use a separate transcription tool first (e.g., `meeting_whisper`, Whisper, WhisperX)
- **Content quality evaluation:** Cannot assess whether decisions were strategically correct
- **Sentiment analysis:** Does not detect emotional tone, sarcasm, or conflict
- **Real-time scoring:** Batch processing only
- **Multi-meeting trend analysis:** Single-meeting scope only
- **Action item tracking:** No execution monitoring or follow-up
- **Causality inference:** Cannot determine why a participant was silent (listening vs. disengaged)

### Privacy & Network

- Transcript content is sent **only** to your configured LLM endpoint
- No telemetry, no third-party services, no cloud uploads
- HTML reports load Chart.js from CDN (`cdn.jsdelivr.net`) by default
- Stateless: no caching, no persistent storage

### Performance

- **LLM calls:** Maximum 2 per run (one for decision analysis, one batched for filler verification)
- **Timeout:** 60 seconds per LLM call
- **Max transcript size:** 200,000 characters (~50k tokens)

## Output Examples

### Markdown Report (`report.md`)

```markdown
# Meeting Quality Report
**Generated:** 2026-06-23 14:30:00
**Total Score:** 72.5/100

## Decision Clarity: 75/100
| Topic | Decided | Owner | Deadline |
|-------|---------|-------|----------|
| Q3 budget increase | ✓ | Alice | Aug 15 |
| New PM hires | ✗ | — | — |
| Office relocation | ✓ | Bob | Sep 1 |

## Time Efficiency: 85/100
Filler detected in 3 of 20 windows (15%).

## Participation Balance: 60/100
| Speaker | Characters | % of Total |
|---------|-----------|------------|
| Alice | 1200 | 45% |
| Bob | 900 | 35% |
| Carol | 500 | 20% |

**Weights Used:** Decision 40%, Time 30%, Participation 30%
```

### HTML Report (`report.html`)

Interactive visualization with:
- **Radar chart:** 3-dimension scores (or 2 in degraded mode)
- **Bar chart:** Speaking time per participant
- Styled with degraded mode banner if applicable

## License

MIT License - see [LICENSE](LICENSE) for details.

## Author

ucsdzehualiu

## Version

1.0.0
