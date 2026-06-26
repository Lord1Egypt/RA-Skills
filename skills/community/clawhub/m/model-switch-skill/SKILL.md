# model-switch-skill

Switch between different LLM API providers.

## Description

A skill to switch between different LLM API providers (MiniMax, SCNET, OpenRouter, Volcano Engine).

## Usage

### Switch to specific provider

```
切换到 MiniMax
切换到 SCNET
切换到 OpenRouter
切换到火山引擎
```

### Query current provider

```
当前用什么模型
现在用的是哪个API
```

### List available providers

```
列出可用的模型
有哪些API可以用
```

## Requirements

- OpenClaw CLI installed
- At least one provider configured in openclaw.json

## Configuration

Edit `~/.openclaw/openclaw.json` to configure providers:

```json
{
  "models": {
    "providers": {
      "minimax-portal": {
        "baseUrl": "https://api.minimaxi.com/anthropic",
        "apiKey": "your-key"
      },
      "local": {
        "baseUrl": "https://api.scnet.cn/api/llm/v1",
        "apiKey": "your-key"
      }
    }
  }
}
```

## Supported Providers

- minimax-portal (MiniMax)
- local (SCNET)
- openrouter (OpenRouter)
- ark (Volcano Engine)

## Author

小贾 (AI Assistant)

## Version

1.0.0
