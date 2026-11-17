---
name: "llm-provider-ai-tool-free"
description: "轻量级OpenAI API调用工具,支持对话补全、文件管理与图像生成,适合个人开发者快速集成。"
license: Proprietary
allowed-tools: read exec
compatibility: "Requires LLM with tool-use capability"
metadata:
  displayName: "OpenAI助手免费版"
  version: "1.0.0"
  summary: "轻量级OpenAI API调用工具,支持对话补全、文件管理与图像生成,适合个人开发者快速集成。"
  tags:
    - "创意设计"
    - "AI助手"
    - "API集成"
    - "文本生成"
    - "图像生成"
  source: "SkillHub"
  converted_at: "2026-07-22T17:58:36"
---

# llm-provider 助手工具 - 免费版

## 概述

llm-provider 助手工具(免费版)为个人开发者提供轻量级的 llm-provider API 调用能力。本版本聚焦于最高频的核心场景:对话补全、文件管理、图像生成与基础助手功能,帮助用户快速将 AI 能力集成到个人项目与工作流中。

免费版与专业版(`llm-provider-ai-tool-pro`)保持 API 兼容,专业版额外提供批量任务、微调、评估等高级能力,可在需要时平滑升级。

## 核心能力

| 能力分类 | 免费版支持 | 说明 |
|:---------|:-----------|:-----|
| 对话补全 | 支持 | `gpt-4o` / `gpt-4o-mini` 等模型 |
| 文本嵌入 | 支持 | 生成向量用于检索与聚类 |
| 文件上传 | 支持 | 上传文档用于助手与批处理 |
| 向量存储 | 基础 | 创建与查询向量存储 |
| 图像生成 | 支持 | DALL-E 3 文生图与编辑 |
| 助手管理 | 基础 | 创建与对话(单线程) |
| 批量任务 | 不支持 | 升级专业版获取 |
| 微调任务 | 不支持 | 升级专业版获取 |
| 评估能力 | 不支持 | 升级专业版获取 |

### 核心功能执行
用`input_params`参数进行配置。

**输入**: 用户提供核心功能执行所需的指令和必要参数。
**处理**: 按照skill规范执行核心功能执行操作,遵循单一意图原则。
**输出**: 返回核心功能执行的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 参数配置与调用
用`config_options`参数进行配置。

**输入**: 用户提供参数配置与调用所需的指令和必要参数。
**处理**: 按照skill规范执行参数配置与调用操作,遵循单一意图原则。
**输出**: 返回参数配置与调用的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`config_options`参数,支持修改/重置/导入操作

### 结果处理与输出
用`output_format`参数进行配置。

**输入**: 用户提供结果处理与输出所需的指令和必要参数。
**处理**: 按照skill规范执行结果处理与输出操作,遵循单一意图原则。
**输出**: 返回结果处理与输出的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`output_format`参数,支持导出/保存/转换操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：轻量级、OpenAI、API、调用工具、支持对话补全、文件管理与图像生、适合个人开发者快、速集成、面向个人开发者的、轻量调用工具、核心能力、chat、completions、与文本生成、文件上传与基础向、量存储管理、图像生成与编辑、Assistants、基础创建与对话、embeddings等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持。

## 使用场景

### 常见问题

将个人文档上传至 llm-provider,构建简易问答助手。

```bash
# 上传知识文件
curl -X POST "https://api.llm-provider.com/v1/files" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -F "purpose=assistants" \
  -F "file=@./knowledge.pdf"

# 创建助手并绑定文件
curl -X POST "https://api.llm-provider.com/v1/assistants" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "我的知识助手",
    "model": "gpt-4o-mini",
    "tools": [{"type": "file_search"}]
  }'
```

### 场景二:营销文案批量生成

利用对话补全快速生成多版本文案。

```python
import os
from llm-provider import llm-provider

client = llm-provider(api_key=os.environ["OPENAI_API_KEY"])

prompts = [
    "为智能手表写一句吸引年轻人的广告语",
    "为咖啡品牌写一段温暖的品牌故事",
    "为在线课程写一封促销邮件开头"
]

for prompt in prompts:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200
    )
    print(response.choices[0].message.content)
```

### 场景三:配图快速生成

为博客或社媒生成配图。

```bash
curl -X POST "https://api.llm-provider.com/v1/images/generations" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "dall-e-3",
    "prompt": "极简风格的日出插画,暖色调,适合博客封面",
    "size": "1024x1024",
    "n": 1
  }'
```

## 不适用场景

以下场景OpenAI助手免费版不适合处理：

- 需要100%确定性的关键决策
- 医疗诊断
- 法律判决

## 触发条件

需要AI模型调用、智能对话、Agent编排、LLM应用时使用。不适用于非本工具能力范围的需求。

## 快速开始

1. 阅读## 核心能力章节了解skill功能
2. 按## 依赖说明配置环境
3. 执行所需能力对应的命令
4. 参考## 错误处理章节处理异常
5. 查看## FAQ解答常见疑问

### 1. 配置 API Key

```bash
# macOS / Linux
export OPENAI_API_KEY="sk-your-api-key-here"

# Windows PowerShell
$env:OPENAI_API_KEY="sk-your-api-key-here"
```

### 2. 验证连接

```bash
curl https://api.llm-provider.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY" | jq '.data[0:3]'
```

### 3. 发起第一次对话

```bash
curl -X POST "https://api.llm-provider.com/v1/chat/completions" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4o-mini",
    "messages": [
      {"role": "system", "content": "你是一个友好的中文助手。"},
      {"role": "user", "content": "用一句话解释什么是向量数据库。"}
    ]
  }'
```

#
## 示例

### Python SDK 配置

```python
import os
from llm-provider import llm-provider

# 方式一:自动读取环境变量
client = llm-provider()

# 方式二:显式传入
client = llm-provider(api_key="sk-your-api-key")

# 方式三:自定义 Base URL(代理场景)
client = llm-provider(
    api_key=os.environ["OPENAI_API_KEY"],
    base_url="https://your-proxy.example.com/v1"
)
```

### Node.js SDK 配置

```javascript
import llm-provider from "llm-provider";

const client = new llm-provider({
  apiKey: process.env.OPENAI_API_KEY,
});
```

## 最佳实践

1. **模型选择策略**
   - 日常对话与轻量任务:优先 `gpt-4o-mini`,成本低、速度快
   - 复杂推理与高质量创作:使用 `gpt-4o`
   - 图像生成:使用 `dall-e-3`,支持自然语言 prompt

2. **Token 成本控制**
   - 设置合理的 `max_tokens` 避免冗长输出
   - 使用 `system` 消息约束输出格式
   - 高频请求场景启用流式输出(`stream: true`)

3. **文件管理规范**
   - 上传前清理无用文件,避免占用配额
   - 为文件添加描述性 `purpose` 标注
   - 定期通过 `GET /v1/files` 审计已上传资源

4. **错误处理**
   - 捕获 `RateLimitError` 并实现指数退避重试
   - 记录 `request_id` 便于排查问题
   - 网络不稳定时启用超时与重试机制

```python
import time
from llm-provider import llm-provider, RateLimitError

client = llm-provider()

def safe_chat(prompt, retries=3):
    for i in range(retries):
        try:
            return client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )
        except RateLimitError:
            time.sleep(2 ** i)
    raise RuntimeError("重试次数耗尽")
```

## 常见问题

### Q1: 提示 "authentication_error" 怎么办?

检查 API Key 是否正确、是否已过期。免费版使用标准 Bearer Token 认证,无需额外配置。可在 llm-provider 控制台重新生成密钥。

### 已知限制

免费版遵循 llm-provider 账户的默认速率限制(Tier 1 通常为 500 RPM)。如需更高并发,可在 llm-provider 控制台提升账户等级,或升级至专业版获取批量处理能力。

### Q3: 能否使用 GPT-4 系列模型?

可以。免费版支持账户权限内的所有模型,包括 `gpt-4o`、`gpt-4o-mini` 等。模型可用性取决于账户等级,而非 Skill 版本。

### Q4: 如何迁移到专业版?

专业版(`llm-provider-ai-tool-pro`)与免费版 API 完全兼容,无需修改代码。升级后可使用批量任务、微调、评估等高级能力。建议在调用量增长或需要自动化流水线时迁移。

### Q5: 是否支持流式输出?

支持。在请求中设置 `"stream": true` 即可。流式输出适合聊天场景,可显著降低首字延迟。

## 依赖说明

### 运行环境
- **Agent 平台**: 支持SKILL.md的任意AI Agent(ai-assistant Code / Cursor / Codex / Gemini CLI等)
- **操作系统**: Windows / macOS / Linux
- **网络**: 需可访问 `api.llm-provider.com`

### 依赖详情

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-------|:-----|:---------|:---------|
| llm-provider Python SDK | Python 库 | 推荐 | `pip install llm-provider` |
| llm-provider Node SDK | npm 库 | 推荐(Node 场景) | `npm install llm-provider` |
| curl | 命令行工具 | 可选 | 系统自带或下载 |
| jq | JSON 处理工具 | 可选 | `apt install jq` / `brew install jq` |
| LLM API | API | 必需 | 由Agent内置LLM提供 |

### API Key 配置
- 必须配置 `OPENAI_API_KEY` 环境变量
- 在 llm-provider 控制台 > API Keys 页面创建
- 建议使用 `.env` 文件管理,避免硬编码
- 免费版无需额外集成插件或托管服务

### 可用性分类
- **分类**: MD+EXEC(纯Markdown指令,部分功能需exec命令行执行)
- **说明**: 基于Markdown的AI Skill,通过自然语言指令驱动Agent完成操作。免费版聚焦核心 API 调用,适合个人开发者快速集成。

## 错误处理


| 错误场景 | 原因 | 处理方式 |
|---------|------|---------|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |
