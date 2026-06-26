---
name: li-summarize
version: "1.0.0"
description: 使用国内 OpenAI 兼容 API 快速总结 URLs、本地文件、YouTube 链接。支持所有国内大模型 API（百度千帆、阿里云、腾讯混元、字节火山、Moonshot、DeepSeek 等）。
metadata: {"clawdbot":{"emoji":"📝","requires":{"bins":["summarize"]},"install":[{"id":"npm","kind":"npm","package":"@steipete/summarize","bins":["summarize"],"label":"Install summarize (npm)"}]},"defaultConfig":{"model":"qwen/qwen2.5-72b-instruct","baseUrl":"https://dashscope.aliyuncs.com/compatible-mode/v1"}}
---

# li-summarize

国内优化版的 summarize CLI，全面支持 OpenAI 兼容 API 的各种国内大模型服务。

## 快速开始

```bash
# 使用环境变量（推荐）
export OPENAI_BASE_URL="https://qianfan.baidubce.com/v2"
export OPENAI_API_KEY="your-api-key"
summarize "https://example.com" --model qianfan/codegeex-4-2025-01-15

# 或者使用模型简称
summarize "https://example.com" --model baidu Ernie-4.0-8K
```

## 支持的国内 API 提供商

### 1. 百度智能云千帆 (QianFan)

```bash
export OPENAI_BASE_URL="https://qianfan.baidubce.com/v2"
export OPENAI_API_KEY="your-bce-api-key"

# 支持的模型
summarize "url" --model qianfan/ernie-4.0-8k
summarize "url" --model qianfan/ernie-3.5-8k
summarize "url" --model qianfan/codegeex-4
```

### 2. 阿里云通义千问 (Dashscope)

```bash
export OPENAI_BASE_URL="https://dashscope.aliyuncs.com/compatible-mode/v1"
export OPENAI_API_KEY="your-api-key"

# 支持的模型
summarize "url" --model qwen/qwen2.5-72b-instruct
summarize "url" --model qwen/qwen2.5-32b-instruct
summarize "url" --model qwen/qwen-max
summarize "url" --model qwen/qwen-turbo
```

### 3. 腾讯混元 (Hunyuan)

```bash
export OPENAI_BASE_URL="https://hunyuancloud.tencent.com/api/v3"
export OPENAI_API_KEY="your-api-key"

summarize "url" --model hunyuan/hunyuan-pro
summarize "url" --model hunyuan/hunyuan-standard
```

### 4. 字节跳动火山引擎 (VeFy)

```bash
export OPENAI_BASE_URL="https://ark.cn-beijing.volces.com/api/v3"
export OPENAI_API_KEY="your-api-key"

summarize "url" --model doubao-pro-32k
summarize "url" --model doubao-standard-32k
```

### 5. Moonshot AI (月之暗面)

```bash
export OPENAI_BASE_URL="https://api.moonshot.cn/v1"
export OPENAI_API_KEY="your-api-key"

summarize "url" --model moonshot/kimi-k2-0711-preview
summarize "url" --model moonshot/kimi-long
```

### 6. DeepSeek

```bash
export OPENAI_BASE_URL="https://api.deepseek.com/v1"
export OPENAI_API_KEY="your-api-key"

summarize "url" --model deepseek-chat
summarize "url" --model deepseek-coder
```

### 7. 智谱 AI (Zhipu)

```bash
export OPENAI_BASE_URL="https://open.bigmodel.cn/api/paas/v4"
export OPENAI_API_KEY="your-api-key"

summarize "url" --model glm-4-plus
summarize "url" --model glm-4-flash
summarize "url" --model glm-4
```

### 8. MiniMax (稀宇)

```bash
export OPENAI_BASE_URL="https://api.minimax.chat/v1"
export OPENAI_API_KEY="your-api-key"

summarize "url" --model MiniMax-Text-01
summarize "url" --model abab6.5s-chat
```

### 9. 阶跃星辰 (StepFun)

```bash
export OPENAI_BASE_URL="https://api.stepfun.com/v1"
export OPENAI_API_KEY="your-api-key"

summarize "url" --model step-1v-8k
summarize "url" --model step-1.5-chat
```

### 10. Ollama (本地部署)

```bash
export OPENAI_BASE_URL="http://localhost:11434/v1"
export OPENAI_API_KEY="not-needed"

summarize "url" --model llama3
summarize "url" --model qwen2.5:72b
```

### 11. OneAPI / All In One

```bash
export OPENAI_BASE_URL="http://your-oneapi-server:3000/v1"
export OPENAI_API_KEY="your-key"

summarize "url" --model gpt-4
summarize "url" --model claude-3
```

## 预设配置（推荐）

为了简化使用，可以在 `~/.summarize/config.json` 中预设常用配置：

```json
{
  "model": "baidu/ernie-4.0-8k",
  "openaiBaseUrl": "https://qianfan.baidubce.com/v2",
  "openaiApiKey": "your-bce-key",
  "length": "xl",
  "language": "zh-CN"
}
```

## 使用示例

```bash
# 总结网页
summarize "https://news.ycombinator.com" --model qwen/qwen2.5-72b-instruct

# 总结 YouTube 视频
summarize "https://youtube.com/watch?v=xxx" --model deepseek-chat

# 总结本地 PDF
summarize "/path/to/file.pdf" --model glm-4-plus

# 指定输出长度
summarize "https://example.com" --length medium

# 输出 JSON 格式
summarize "https://example.com" --json

# 仅提取内容（不总结）
summarize "https://example.com" --extract

# 流式输出
summarize "https://example.com" --stream on
```

## 环境变量速查表

| 提供商 | BASE_URL | API_KEY 环境变量 |
|--------|----------|------------------|
| 百度千帆 | `https://qianfan.baidubce.com/v2` | `OPENAI_API_KEY` |
| 阿里通义 | `https://dashscope.aliyuncs.com/compatible-mode/v1` | `OPENAI_API_KEY` |
| 腾讯混元 | `https://hunyuancloud.tencent.com/api/v3` | `OPENAI_API_KEY` |
| 字节火山 | `https://ark.cn-beijing.volces.com/api/v3` | `OPENAI_API_KEY` |
| Moonshot | `https://api.moonshot.cn/v1` | `OPENAI_API_KEY` |
| DeepSeek | `https://api.deepseek.com/v1` | `OPENAI_API_KEY` |
| 智谱 AI | `https://open.bigmodel.cn/api/paas/v4` | `OPENAI_API_KEY` |
| MiniMax | `https://api.minimax.chat/v1` | `OPENAI_API_KEY` |
| StepFun | `https://api.stepfun.com/v1` | `OPENAI_API_KEY` |
| Ollama | `http://localhost:11434/v1` | 任意 |
| OneAPI | `http://localhost:3000/v1` | `OPENAI_API_KEY` |

## 配置模板

### 百度千帆（推荐）

```bash
# .bashrc 或 .zshrc
export OPENAI_BASE_URL="https://qianfan.baidubce.com/v2"
export OPENAI_API_KEY="your-bce-v3-api-key"

# 使用
summarize "url" --model qianfan/ernie-4.0-8k
```

### 阿里云通义千问

```bash
export OPENAI_BASE_URL="https://dashscope.aliyuncs.com/compatible-mode/v1"
export OPENAI_API_KEY="your-dashscope-api-key"

summarize "url" --model qwen/qwen-max
```

### DeepSeek（便宜好用）

```bash
export OPENAI_BASE_URL="https://api.deepseek.com/v1"
export OPENAI_API_KEY="your-deepseek-api-key"

summarize "url" --model deepseek-chat
```

## 故障排除

### 401 认证错误

- 检查 `OPENAI_API_KEY` 是否正确
- 确认 API Key 有足够余额

### 403 权限错误

- 确认 API Key 已开通对应模型权限
- 百度千帆需要在控制台开通模型试用

### 404 模型不存在

- 确认模型名称拼写正确
- 确认该模型在对应平台可用

### 超时错误

- 增加超时时间: `summarize "url" --timeout 5m`
- 检查网络连接

### 依赖问题

```bash
# 如果缺少 ffmpeg (YouTube 音频处理)
sudo apt install ffmpeg  # Ubuntu/Debian
sudo yum install ffmpeg  # CentOS
brew install ffmpeg      # macOS
```

## 相关链接

- summarize CLI: https://summarize.sh
- 百度千帆: https://cloud.baidu.com/product/wenxinworkshop
- 阿里云Dashscope: https://dashscope.aliyuncs.com/
- 腾讯混元: https://cloud.tencent.com/product/hunyuan
- DeepSeek: https://platform.deepseek.com/
- 智谱AI: https://open.bigmodel.cn/