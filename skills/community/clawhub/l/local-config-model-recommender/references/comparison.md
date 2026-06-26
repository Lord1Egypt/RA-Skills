# Model Capability Reference

A comprehensive reference for comparing AI model capabilities across different providers.

## Quick Reference

### Context Length (Tokens)

| Model | Max Input | Max Output |
|-------|-----------|------------|
| gemini-3.1-pro | 2M | - |
| gemini-1.5-flash | 1M | - |
| kimi-k2.5 | 1M | - |
| Claude 3 (Opus/Sonnet) | 200K | - |
| GPT-4o | 128K | - |
| Qwen3 Max | 128K | - |
| DeepSeek V3 | 64K | - |

### Vision Capabilities

| Model | Image Input | Description |
|-------|-------------|-------------|
| gpt-4o | ✅ | Leading multimodal |
| gpt-4v | ✅ | Vision-specific |
| qwen3-vl | ✅ | Chinese-optimized |
| glm-4.6v | ✅ | Chinese vision |
| gemini-1.5-pro | ✅ | Strong vision |

### Code Capabilities

| Model | Specialty |
|-------|-----------|
| minimax-m2.5 | Best overall coding |
| deepseek-coder | Open source code specialist |
| qwen3-coder-plus | Chinese code expert |
| gpt-5-codex | Code-specific |
| claude-code | Code assistance |

### Reasoning Capabilities

| Model | Specialty |
|-------|-----------|
| o3 | State-of-the-art reasoning |
| claude-opus-4.6 | Premium reasoning |
| qwen3-max | Best Chinese reasoning |
| gemini-3.1-pro | Balanced reasoning |

### Cost-Effective Options

| Model | Price Tier |
|-------|------------|
| gpt-4o-mini | Budget-friendly |
| claude-haiku-4.5 | Fast & cheap |
| qwen3-flash | Chinese budget |
| glm-4.7-flash | Chinese fast |

## Model ID Patterns

Common patterns that indicate model capabilities:

| Pattern | Meaning |
|---------|---------|
| `*vl*` | Vision/Multimodal |
| `*coder*` | Code-optimized |
| `*max*` | Premium tier |
| `*flash*` | Fast/lightweight |
| `*mini*` | Small/efficient |
| `*thinking*` | Enhanced reasoning |

## Task → Model Mapping

| Task | Recommended Models |
|------|-------------------|
| Code generation | minimax-m2.5, deepseek-coder |
| Image analysis | qwen3-vl, gpt-4o, gemini-1.5-pro |
| Complex reasoning | o3, claude-opus-4.6, qwen3-max |
| Long document | kimi-k2.5, gemini-3.1-pro |
| Fast response | gpt-4o-mini, qwen3-flash |
| Chinese tasks | qwen3.5-plus, glm-5, kimi-k2.5 |

## Configuration

```bash
# Get available models
cat ~/.openclaw/openclaw.json | jq '[.models.providers[].models[].id] | unique'
```

The recommendation engine automatically adapts to whichever models are configured in your OpenCLAW setup.