---
name: gpt-chat
description: GPT聊天 - 使用GPT模型进行对话和内容生成
homepage: https://openai.com/api/pricing/
metadata: { "openclaw": { "emoji": "💬", "requires": { "bins": ["node"], "env": ["OPENAI_API_KEY"] }, "primaryEnv": "OPENAI_API_KEY" } }
---

# GPT 聊天 Skill

使用 GPT 模型进行对话和内容生成。

## 已配置

- **默认模型**: GPT-5.1
- **脚本路径**: `skills/gpt-chat/scripts/gpt.js`

> ⚠️ 使用前请设置环境变量 `OPENAI_API_KEY` 或在对话中提供你的 Key

## 支持的模型

| 模型 | 输入价格 | 输出价格 | 说明 |
|------|----------|----------|------|
| GPT-5.2 | $1.75/1M tokens | $14/1M tokens | 最新旗舰模型 |
| GPT-5.1 | $1.25/1M tokens | $10/1M tokens | 稳定版（默认） |
| GPT-5 | $1.25/1M tokens | $10/1M tokens | 标准版 |

## 使用方法

在对话中可以直接使用以下命令：

1. **查看可用模型**:
   ```
   运行 node skills/gpt-chat/scripts/gpt.js list
   ```

2. **切换模型**:
   ```
   运行 node skills/gpt-chat/scripts/gpt.js set gpt-5.2
   ```

3. **发送消息**:
   ```
   运行 node skills/gpt-chat/scripts/gpt.js chat 你的问题
   ```

4. **查看当前模型**:
   ```
   运行 node skills/gpt-chat/scripts/gpt.js current
   ```

## 直接调用示例

可以直接在对话中说：
- "使用 GPT-5.2 模型"
- "切换到 gpt-5.1"
- "用 gpt-5 回答我的问题"

## API Key 配置

如需使用自己的 API Key，可以设置环境变量 `OPENAI_API_KEY`，或在对话中提供你的 Key。
