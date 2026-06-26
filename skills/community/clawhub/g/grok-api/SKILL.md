# Grok API Skill

## Description
通过 LeonAI 代理调用 xAI Grok API，支持文本对话、推理、图片生成/编辑、视频生成。兼容 OpenAI Chat Completions 格式。

## 触发场景
- 用户说"用 Grok 聊天/问问题/分析"
- 用户说"用 Grok 生成图片/画图"
- 用户说"用 Grok 生成视频"
- 用户提到 Grok 模型名（grok-3, grok-4, grok-4.1 等）

## 环境变量要求
- `GROK_API_KEY` — LeonAI 代理的 API Key（存入 personal-secrets.json）
- `GROK_BASE_URL` — 默认 `https://apileon.leonai.top/grok/v1`

## 可用模型

### 文本模型
| 模型 | 特点 | Tier | Cost |
|------|------|------|------|
| grok-3 | 基础文本 | basic | low |
| grok-3-mini | 轻量推理 | basic | low |
| grok-3-thinking | 深度推理 | basic | low |
| grok-4 | 进阶文本 | basic | low |
| grok-4-mini | 快速回复 | basic | low |
| grok-4-thinking | 进阶推理 | basic | low |
| grok-4-heavy | 重量级 | super | high |
| grok-4.1-mini | 最新快速 | basic | low |
| grok-4.1-fast | 极速 | basic | low |
| grok-4.1-expert | 专家级 | basic | high |
| grok-4.1-thinking | 最新推理 | basic | high |
| grok-4.20-beta | Beta测试 | basic | low |

### 图片/视频模型
| 模型 | 功能 |
|------|------|
| grok-imagine-1.0 | 图片生成 |
| grok-imagine-1.0-fast | 快速图片生成 |
| grok-imagine-1.0-edit | 图片编辑 |
| grok-imagine-1.0-video | 视频生成 |

## 使用方式

### 1. 文本对话
```bash
curl -s -X POST "$GROK_BASE_URL/chat/completions" \
  -H "Authorization: Bearer $GROK_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "grok-4.1-mini",
    "stream": false,
    "messages": [{"role": "user", "content": "你好"}]
  }'
```

### 2. 推理模式
```bash
curl -s -X POST "$GROK_BASE_URL/chat/completions" \
  -H "Authorization: Bearer $GROK_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "grok-4.1-thinking",
    "stream": false,
    "reasoning_effort": "high",
    "messages": [{"role": "user", "content": "分析量子计算的前景"}]
  }'
```

### 3. 图片生成
```bash
curl -s -X POST "$GROK_BASE_URL/images/generations" \
  -H "Authorization: Bearer $GROK_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "描述文本",
    "model": "grok-imagine-1.0",
    "n": 1,
    "size": "1024x1024",
    "response_format": "url",
    "enable_nsfw": true
  }'
```
可选 size: `1024x1024` / `1280x720` / `720x1280` / `1792x1024` / `1024x1792`

### 4. 视频生成
```bash
curl -s -X POST "$GROK_BASE_URL/videos" \
  -H "Authorization: Bearer $GROK_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "视频描述",
    "model": "grok-imagine-1.0-video",
    "size": "1792x1024",
    "seconds": 6,
    "quality": "standard"
  }'
```
seconds: 6-30 | quality: standard(480p) / high(720p)

### 5. 脚本调用
```bash
# 文本
python3 scripts/grok_chat.py "你好Grok"
python3 scripts/grok_chat.py --model grok-4.1-thinking --reasoning high "分析问题"

# 图片
python3 scripts/grok_chat.py --image "描述"

# 视频
python3 scripts/grok_chat.py --video "描述"

# 列出模型
python3 scripts/grok_chat.py --list-models
```

## 推荐模型选择
- **日常对话/快速问答** → `grok-4.1-mini` 或 `grok-4.1-fast`
- **深度分析/推理** → `grok-4.1-thinking` + `reasoning_effort: high`
- **图片生成** → `grok-imagine-1.0`（高质量）或 `grok-imagine-1.0-fast`（快速）
- **视频生成** → `grok-imagine-1.0-video`

## 注意事项
- API 通过 LeonAI 代理转发，非 xAI 直连
- 额度：Basic tier 80次/20h，Super tier 140次/2h
- 图片/视频生成为异步，URL 有时效性，建议及时下载
- `enable_nsfw: true` 可开启 NSFW 内容生成
