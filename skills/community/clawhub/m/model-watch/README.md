# model-watch

Benchmark AI API models over time. Detect when they get dumber.

> *"Opus 4.7 was hallucinating a lot today... shocking to see such degradation"* — r/ClaudeAI (49↑)
> *"Anthropic admits to have made hosted models more stupid"* — r/LocalLLaMA (281↑)

## Install

```bash
pip install git+https://github.com/minirr890112-byte/model-watch.git
```

Or from local:
```bash
cd model-watch && pip install .
```

## Usage

```bash
# View benchmark questions
model-watch demo

# Submit model outputs (from your API calls)
model-watch submit '{"reasoning_1":"...", "coding_1":"...", ...}'

# View score history
model-watch history

# Check for degradation alerts
model-watch alert
```

## Benchmarks

7 standardized tests covering:
- Reasoning (2 tests)
- Coding (2 tests)
- Writing (1 test)
- Instruction following (1 test)
- Hallucination detection (2 tests)

## How it works

1. Run the 7 benchmark questions through your AI model of choice
2. Feed the responses into `model-watch submit`
3. Scores are stored locally in `~/.hermes/model-watch-history.json`
4. Track trends with `model-watch history`
5. `model-watch alert` flags when recent scores drop >10% vs historical average

## From Reddit

## 生态系统

| Tool | Description |
|---|---|
| [api-cost-compare](https://github.com/minirr890112-byte/api-cost-compare) | Compare LLM API pricing |
| [model-cost-advisor](https://github.com/minirr890112-byte/model-cost-advisor) | Recommend best LLM by cost |
| [claude-intel-monitor](https://github.com/minirr890112-byte/claude-intel-monitor) | Full benchmark monitoring suite |
| [prompt-inspector](https://github.com/minirr890112-byte/prompt-inspector) | Scan prompts for triggers |

Part of [HermesMade]Part of [HermesMade](https://github.com/minirr890112-byte/HermesMade) — tools built from real Reddit pain points.
