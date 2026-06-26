---
name: model-throughput-tester
name_zh: 吞吐率 测试 · 模型速度对比
tags: [model-throughput-tester, 吞吐率测试, 模型速度对比]
description: Benchmark LLM model throughput — measure tokens/s, latency, and output speed. Supports auto mode (no API key needed) via openclaw infer, or direct API mode for OpenAI-compatible endpoints. Trigger: throughput test, tokens/s, latency test, benchmark, speed test, model test.
description_zh: AI 模型速度对比工具。一句话测出哪个模型更快、延迟更低、吞吐率更高。支持无 Key 的 auto 模式（openclaw infer）和 OpenAI 兼容 API 直连。对比多个模型的 tokens/s、响应延迟、输出速度，生成可视化报告。换模型前先跑个基线，不花冤枉钱。
triggerWords:
  - 模型 哪个快
  - 模型 速度 测试
  - 模型 性能 对比
  - AI 速度 测评
  - LLM 速度 测试
  - token 速度
  - tokens/s 对比
  - 吞吐率 测试
  - 延迟 测试
  - 响应 速度 对比
  - 模型 延迟 排行
  - DeepSeek GPT 哪个快
  - AI 模型 基线
  - 模型 换哪个
  - 测一下 模型 速度
  - 跑个 测试
  - throughput test
  - tokens/s
  - speed test
  - latency test
  - model test
  - 测速
  - benchmark
metadata:
  openclaw:
    requires:
      bins: [python3]
    tags: [model-benchmark, throughput, tokens-per-second, latency, AI-speed, LLM, model-comparison, performance, speed-test, benchmark, 速度测试, 吞吐率, 模型对比, AI性能, 延迟测试, tokens/s, LLM测速, 模型测速]
    permissions:
      file:
        read: ["~/.openclaw/workspace/skills/model-throughput-tester/**"]
        write: ["~/.openclaw/workspace/skills/model-throughput-tester/**"]
---

# Model Throughput Tester

Benchmark LLM model throughput (tokens/s). Two modes available:

- **Auto Mode**: Test current model via `openclaw infer model run`, **no API key required**
- **API Mode**: Direct call to OpenAI-compatible API, requires URL and Key

## When to Use

**Use when:** User explicitly requests a model throughput test.

**Trigger words:**
- throughput test, tokens/s, speed test, benchmark
- model speed, latency test, model test

**Do NOT trigger:** Broad performance discussion terms (e.g. "model performance", standalone "benchmark") should not auto-trigger execution.

**Auto Mode (no API key):**
```bash
python3 throughput.py --auto --model "<current session model>"
```

## Core Features

### 1. Auto Mode (No Key, Recommended)

Auto-detects the current session model and benchmarks throughput, zero configuration needed.

```bash
python3 throughput.py --auto
```

Test a specific model:
```bash
python3 throughput.py --auto --model "zai/glm-5-turbo"
```

### 2. API Mode (Direct API Call)

```bash
python3 throughput.py \
  --url https://api.example.com/v1 \
  --key sk-xxx \
  --models gpt-4o-mini,gpt-4o
```

### 3. Common Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--iterations` | `3` | Test iterations per model |
| `--max-tokens` | `512` | Max output tokens |
| `--test-prompt` | English prose (summer field) | Test prompt |
| `--timeout` | `60` | Single request timeout (seconds) |
| `--output` | `throughput-report.md` | Output report filename |
| `--csv` | false | Also generate CSV |

## Workflow

### Auto Mode Flow

```
1. Read current session model from openclaw.json (provider/model)
2. Send test prompt via openclaw infer model run
3. Timer: command start → output complete
4. Estimate token count from response text (English: 0.75 word/token, Chinese: 1.5 chars/token)
5. Calculate tokens/s
6. Generate summary report
```

### API Mode Flow

```
1. Build /v1/chat/completions request
2. Timer: request start → last token received
3. Extract usage.completion_tokens from response (precise)
4. Calculate tokens/s, error rate
5. Generate summary report
```

### Metrics

| Metric | Description |
|--------|-------------|
| **Tokens/s** | Throughput = Output Tokens / Elapsed Time |
| **Avg Latency** | Average single request latency |
| **Avg Output Tokens** | Average output token count |
| **Error Rate** | Failed request ratio |

## Output Example

```markdown
# Model Throughput Report
**Mode:** Auto (openclaw infer)
**Iterations:** 3

## Summary
| Model | Avg Tokens/s | Avg Latency(s) | Avg Output Tokens | Error Rate |
|-------|-------------|----------------|-------------------|------------|
| zai/glm-5-turbo | 57.9 | 20.6 | 979.0 | 0.0% |

## Detail
### zai/glm-5-turbo
| Iter | Latency(s) | Output Tokens | Tokens/s | Status |
|------|------------|--------------|---------|--------|
| 1 | 19.5 | 950 | 48.7 | ✅ |
| 2 | 21.3 | 1010 | 47.4 | ✅ |
| 3 | 20.9 | 977 | 46.7 | ✅ |
```

## Error Handling

| Scenario | Auto Mode | API Mode |
|----------|-----------|----------|
| openclaw not installed | cli_error | — |
| Model not found | api_error | http_404 |
| Network timeout | timeout | timeout |
| Token estimation | English 0.75 word/token, Chinese 1.5 chars/token | Precise from API |

## Usage Examples

### Quick Test After Install (Auto Mode)

```bash
python3 ~/.openclaw/workspace/skills/model-throughput-tester/throughput.py --auto --model "<current session model>"

# Or auto-detect (may not match session override)
python3 ~/.openclaw/workspace/skills/model-throughput-tester/throughput.py --auto
```

### Test Multiple Models (API Mode)

```bash
python3 throughput.py \
  --url "https://api.openai.com/v1" \
  --key "sk-xxx" \
  --models "gpt-4o-mini,gpt-4o" \
  --iterations 5
```

### Custom Prompt

```bash
python3 throughput.py --auto \
  --test-prompt "Explain quantum computing in detail." \
  --iterations 5
```

## Technical Details

- **Auto Mode**: `openclaw infer model run --json`, Python `subprocess` call
- **API Mode**: `urllib` (Python built-in), OpenAI-compatible `/v1/chat/completions`
- **Timer Precision**: `time.perf_counter()` nanosecond-level
- **Token Counting**: API mode uses `usage.completion_tokens` (precise), Auto mode estimates by character count
- **URL Handling**: Smart detection of `/v1`, `/v4`, `/chat/completions` paths

## Notes

- Auto mode throughput includes gateway routing overhead, slightly lower than direct API (~1-3%)
- Auto mode token count is estimated, API mode is precise
- English prompts recommended for more accurate token estimation
- Anti-cache: random seed suffix appended to each iteration