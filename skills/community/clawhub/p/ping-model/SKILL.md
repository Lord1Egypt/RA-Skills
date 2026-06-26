---
name: ping-model
description: Measure and display AI model response latency. Use when the user types /ping or /ping followed by a model name to test round-trip time. Captures precise timing between command receipt and response generation, with smart duration formatting (ms, seconds, or minutes). Supports cross-model testing by temporarily switching models and measuring latency.
metadata: {"clawdbot":{"emoji":"🧪","requires":{"bins":["node"]}}}
---

# Ping Model

Measure AI model response latency with consistent formatting.

## Quick Start

### Simple Ping (current model)
```bash
bash command:"node {baseDir}/ping-model.js"
```

### Ping Specific Model
```bash
bash command:"node {baseDir}/ping-model.js --model minimax"
```

### Compare Multiple Models
```bash
bash command:"node {baseDir}/ping-model.js --compare kimi,minimax,deepseek"
```

## Command Reference

| Command | Description |
|---------|-------------|
| `/ping` | Ping current active model |
| `/ping kimi` | Switch to kimi, ping, return |
| `/ping minimax` | Switch to minimax, ping, return |
| `/ping deepseek` | Switch to deepseek, ping, return |
| `/ping all` | Compare all available models |

## Output Format

**Required format - ALWAYS use this exact structure:**

```
🧪 PING {model-name}

📤 Sent:     {HH:MM:SS.mmm}
📥 Received: {HH:MM:SS.mmm}
⏱️  Latency:  {formatted-duration}

🎯 Pong!
```

### Latency Formatting Rules

- **< 1 second**: Display as `XXXms` (e.g., `847ms`)
- **≥ 1 second, < 60 seconds**: Display as `X.XXs` (e.g., `1.23s`)
- **≥ 60 seconds**: Display as `X.XXmin` (e.g., `2.5min`)

### Examples

**Fast response (< 1s):**
```
🧪 PING kimi

📤 Sent:     09:34:15.123
📥 Received: 09:34:15.247
⏱️  Latency:  124ms

🎯 Pong!
```

**Medium response (1-60s):**
```
🧪 PING minimax

📤 Sent:     09:34:15.123
📥 Received: 09:34:16.456
⏱️  Latency:  1.33s

🎯 Pong!
```

**Slow response (> 60s):**
```
🧪 PING gemini

📤 Sent:     09:34:15.123
📥 Received: 09:35:25.456
⏱️  Latency:  1.17min

🎯 Pong!
```

## Cross-Model Testing

When testing a non-active model:

1. Save current model context
2. Switch to target model
3. Execute ping
4. Measure latency
5. Restore original model
6. Display result

**Critical:** Always return to the original model after testing.

## Comparison Mode

```bash
bash command:"node {baseDir}/ping-model.js --compare kimi,minimax,deepseek,gpt"
```

Output format:
```
══════════════════════════════════════════════════
🧪 MODEL COMPARISON
══════════════════════════════════════════════════

🥇 kimi      124ms
🥈 minimax   1.33s
🥉 deepseek  2.45s
4️⃣  openai    5.67s

🏆 Fastest: kimi (124ms)
```

## Implementation

The ping latency is measured as the time between:
- T1: Message received by the agent
- T2: Response ready to send

This captures the model's internal processing time, not network latency.
