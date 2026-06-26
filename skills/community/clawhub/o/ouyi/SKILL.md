---
name: ouyi
description: |
  使用欧亿（ouyi）API 进行对话分析的 ACP skill。当用户要求使用 ouyi 模型、
  欧亿模型、分析黄金、投资、技术问题等需要 AI 推理的任务时使用此 skill。
  
  该 skill 通过本地 Node.js 脚本直接调用 ouyi API，
  解决 OpenClaw 的 openai-completions 类型无法解析 chat 格式响应的问题。
  
  使用方式：
  1. 读取 scripts/ouyi-api.js 的内容
  2. 通过 exec 工具运行脚本
  3. 解析 JSON 结果并发送给用户
---

# ouyi Skill

## 核心脚本

路径：`scripts/ouyi-api.js`

## API 配置

- **API Key**: 用户需要用自己的 ouyi API key 替换脚本中的 `API_KEY`
- **模型**: `ouyi-openclaw`（内部映射到 gpt-5-nano-2025-08-07）
- **Endpoint**: `https://api.rcouyi.com/v1/chat/completions`

## 使用方式

### 1. 运行对话

```bash
node <skill_dir>/scripts/ouyi-api.js "你的问题"
```

### 2. 解析结果

输出格式（JSON）：
```json
{"content": "回复内容", "reasoningTokens": 832, "model": "gpt-5-nano-2025-08-07", "error": null}
```

### 3. 发送结果

提取 `content` 字段，发送给用户。

## 示例问题

- "Is gold worth buying in 2025?"
- "Explain quantum computing to a 10-year-old in Chinese."
- "What is the difference between GDP and GNP?"

## 性能特征

- 响应时间：平均 5-10 秒（推理模型特性）
- 速度与 reasoning_tokens 无明显相关
- 支持中英文，质量稳定

## 已知问题

- `reasoning_tokens` 很大但 content 可能为空（当 max_tokens < 1500 时）
- 当前脚本不设置 max_tokens 来避免此问题
- 模型是推理模型，可能先输出推理过程再输出答案

## 配置

若要更换 API key，直接编辑 `scripts/ouyi-api.js` 中的：
```javascript
const API_KEY = 'your-api-key-here';
```
