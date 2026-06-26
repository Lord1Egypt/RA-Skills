---
name: nanobanana
description: Nano Banana 2 Pro AI 图像生成工具。当用户提到"生图"、"生成图片"、"AI画图"、"nano banana"、"nanobanana"、或需要调用 Nano Banana API 生成/编辑图片时触发。支持文本生成图片、图片编辑（以图生图）、多模态对话。
---

# Nano Banana 2 Pro 图片生成

## 快速开始

```bash
# 文本对话
node nanobanana.js "你好"

# 图片生成
node nanobanana.js "一只可爱的橘猫"

# 图片编辑（以图生图）
node nanobanana.js "把这只猫变成机器人" --image cat.jpg

# 查看帮助
node nanobanana.js
```

## 配置

脚本位于 `scripts/nanobanana.js`，API 配置在文件顶部：

```javascript
const CONFIG = {
  baseURL: "https://claw.cjcook.site/v1",
  apiKey: "YOUR_API_KEY",
  model: "nanobanana-2pro",
  maxTokens: 4096,
  outputDir: path.join(__dirname, "output"),
};
```

图片输出到 `output/` 目录。

## API 基础信息

- **Endpoint**: `https://claw.cjcook.site/v1/chat/completions`
- **模型**: `nanobanana-2pro`（实际为 gemini-3.1-flash-image）
- **认证**: Bearer Token
- **返回格式**: 图片在 `message.images[0].image_url.url`（base64 JPEG）
- **文本回复**: `message.content`（可能为 null）

## 核心函数

```javascript
// 生成图片（含输入图片时为编辑模式）
generateImage(prompt, inputImage = null, options = {})

// 纯文本对话
chat(text)
```

## 环境要求

- Node.js >= 18
- 需要 `openai` npm 包（已在 `/root/.openclaw/workspace-moma/node_modules` 安装）
- 工作目录需有 `node_modules`（或通过 NODE_PATH 指定）

## 常见错误

| 错误 | 原因 | 处理 |
|------|------|------|
| `auth_unavailable` | 服务端临时过载 | 稍后重试 |
| `401` | API Key 无效/过期 | 检查 key |
| `429` | 请求频率超限 | 降低频率 |
| `500` | 服务端错误 | 稍后重试 |
