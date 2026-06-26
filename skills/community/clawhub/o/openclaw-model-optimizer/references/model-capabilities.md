# Common Model Capabilities Reference

Known defaults for popular models. Use as reference when user cannot confirm exact specs.

## Alibaba Cloud (DashScope)

| Model | input | contextWindow | maxTokens | reasoning |
|-------|-------|---------------|-----------|-----------|
| qwen3.5-plus | text, image | 256000 | 16384 | true |
| qwen3.5-max | text, image | 1000000 | 16384 | true |
| qwen-vl-max | text, image | 128000 | 8192 | false |
| qwen-turbo | text | 128000 | 8192 | false |

## ByteDance (Volcano Engine)

| Model | input | contextWindow | maxTokens | reasoning |
|-------|-------|---------------|-----------|-----------|
| doubao-seed-2.0-pro | text, image | 128000 | 16384 | true |
| doubao-1.5-pro | text, image | 128000 | 8192 | false |

## Anthropic

| Model | input | contextWindow | maxTokens | reasoning |
|-------|-------|---------------|-----------|-----------|
| claude-opus-4-6 | text, image | 1000000 | 32000 | true |
| claude-sonnet-4-6 | text, image | 200000 | 16000 | true |
| claude-haiku-4-5 | text, image | 200000 | 8192 | false |

## OpenAI

| Model | input | contextWindow | maxTokens | reasoning |
|-------|-------|---------------|-----------|-----------|
| gpt-5.4 | text, image | 256000 | 32000 | true |
| gpt-4.1 | text, image | 1000000 | 32000 | false |
| gpt-4.1-mini | text, image | 1000000 | 16000 | false |

## Moonshot (月之暗面)

| Model | input | contextWindow | maxTokens | reasoning |
|-------|-------|---------------|-----------|-----------|
| kimi-k2.5 | text, image | 256000 | 65535 | true |

## Zhipu (智谱)

| Model | input | contextWindow | maxTokens | reasoning |
|-------|-------|---------------|-----------|-----------|
| glm-5 | text | 200000 | 128000 | true |

## Google

| Model | input | contextWindow | maxTokens | reasoning |
|-------|-------|---------------|-----------|-----------|
| gemini-3.1-pro | text, image | 2000000 | 65536 | true |
| gemini-3.1-flash | text, image | 1000000 | 32768 | false |

## Notes

- These values reflect known specs as of early 2026 and may change
- API provider endpoints may impose lower limits than the model supports
- Always verify with user when possible
