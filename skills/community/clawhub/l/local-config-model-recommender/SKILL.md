---
name: local-config-model-recommender
description: Intelligently recommends optimal AI models based on task requirements. Dynamically reads the user's OpenCLAW configuration and provides context-aware model suggestions. Supports all major global and domestic models including OpenAI, Claude, Gemini, DeepSeek, Kimi, Zhipu GLM, Qwen, and MiniMax.
---

# Model Recommender

An intelligent model selection assistant that dynamically analyzes your OpenCLAW configuration and recommends the most suitable AI model for your specific task.

## Overview

This skill reads your local OpenCLAW configuration to determine available models, then applies keyword-based capability matching to provide intelligent recommendations based on the task at hand.

## Supported Models

### Global Providers

| Provider | Models |
|----------|--------|
| OpenAI | gpt-5-pro, gpt-4o, gpt-4o-mini, o3, o1 |
| Anthropic Claude | claude-opus-4.6, claude-sonnet-4.6, claude-haiku-4.5 |
| Google Gemini | gemini-3.1-pro, gemini-3.1-flash, gemini-2.5-flash |
| Mistral | mistral-large, mistral-small |
| xAI | grok-4.20-beta, grok-4-fast |

### Domestic (China) Providers

| Provider | Models |
|----------|--------|
| Alibaba Qwen | qwen3-max, qwen3-vl, qwen3.5-plus, qwen3-coder-plus |
| MiniMax | minimax-m2.5, minimax-m2.1 |
| DeepSeek | deepseek-v3.2, deepseek-chat, deepseek-coder |
| Moonshot (Kimi) | kimi-k2.5, kimi-k2 |
| Zhipu GLM | glm-5, glm-4.7-flash, glm-4.6v |
| Baidu ERNIE | ernie-4.5-thinking, ernie-4.5-vl |
| ByteDance Seed | seed-2.0-lite, seed-2.0-mini |

## Capability Mapping

The skill uses keyword-based pattern matching to infer model capabilities:

| Keyword | Capability | Primary Use Case |
|---------|------------|------------------|
| `vl`, `vision`, `image`, `4v`, `4o` | Vision/Multimodal | Image analysis, OCR, chart interpretation |
| `code`, `coder`, `codex` | Code Generation | Programming, debugging, refactoring |
| `o1`, `o3`, `o4`, `reasoning`, `thinking` | Advanced Reasoning | Mathematical reasoning, complex logic |
| `max`, `pro`, `premium`, `large`, `opus` | Premium/Tier-1 | High-quality output, complex tasks |
| `mini`, `small`, `lite`, `flash`, `haiku`, `nano` | Lightweight | Fast response, simple tasks, cost-sensitive |

## Recommendation Logic

```
1. Parse ~/.openclaw/openclaw.json to extract configured models
2. Analyze user's task requirements
3. Match task to model capabilities via keyword detection
4. Return the best-matching model from available configuration
5. Fall back to default model if no specific match found
```

## Usage Examples

**User:** "Which model should I use for coding?"
→ **Recommend:** minimax-m2.5, deepseek-coder, qwen3-coder-plus

**User:** "I need to analyze an image"
→ **Recommend:** qwen3-vl, glm-4.6v, gpt-4o, gemini-1.5-pro

**User:** "For complex reasoning tasks"
→ **Recommend:** o3, claude-opus-4.6, qwen3-max, gemini-3.1-pro

## Notes

- Automatically adapts to your specific configuration
- Prioritizes models that are actually available in your setup
- Falls back gracefully when exact capability matches aren't found
- Supports both global (OpenAI, Claude, Gemini) and domestic (Chinese) model providers