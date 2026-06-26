# Grok 搜索技能

使用 Grok 模型的网络搜索能力，获取实时信息。

## 快速开始

### 1. 配置 API Key

```bash
# 设置 API Key
export GROK_API_KEY="your-api-key"

# 设置 API 端点（可选，默认使用官方 API）
export GROK_API_URL="https://api.x.ai/v1"

# 如果使用中转 API
# export GROK_API_URL="https://your-proxy.com/v1"
```

### 2. 使用

```bash
./grok-search.sh "今天北京天气"
```

## 支持的 API

- **xAI 官方**: `https://api.x.ai/v1`
- **中转 API**: 支持任何 OpenAI 兼容的中转服务

## 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `GROK_API_KEY` | API 密钥 | - |
| `GROK_API_URL` | API 端点 | `https://api.x.ai/v1/chat/completions` |
| `GROK_MODEL` | 模型名称 | `grok-4.1-fast` |

## 许可证

MIT
