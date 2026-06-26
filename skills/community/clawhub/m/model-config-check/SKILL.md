---
name: model-config-check
description: 校验模型配置是否正确、模型是否可以正常连接和返回内容。当用户说"检查模型"、"测试模型"、"模型能不能用"、"模型配置"、"诊断模型问题"时使用。**每次修改模型配置（config.patch/config.apply涉及models.providers）后必须自动执行校验。** 用户只给模型名+API key时，自动识别provider、查找配置、写入并校验。
---

# 模型配置校验 Skill

## ⚡ 自动触发规则

**当以下情况发生时，必须自动运行校验脚本，无需用户请求：**

1. 使用 `gateway config.patch` 修改了 `models` 相关配置（新增/修改 provider 或 model）
2. 使用 `gateway config.apply` 替换了整个配置且包含 models 变更
3. 使用 `gateway update.run` 更新后（模型接口可能有变化）

**自动校验流程：**
1. 配置写入完成 + gateway 重启后，等待 5 秒让服务就绪
2. 执行 `bash ~/.openclaw/workspace/skills/model-config-check/scripts/check_models.sh`
3. 解析输出，向用户汇报校验结果
4. 如果新模型不可用，立即告知用户具体原因和修复建议

**手动触发：** 用户说"检查模型"/"测试模型"/"模型能不能用"/"诊断模型"时也执行同样流程。

## 🤖 自动配置流程

当用户只提供「模型名 + API key」时，按以下流程自动完成配置：

### Step 1: 识别 Provider

根据模型名前缀匹配已知 provider：

| 模型名前缀 | Provider | Base URL | API 类型 |
|-----------|----------|----------|----------|
| `gpt-*`, `o1-*`, `o3-*`, `o4-*`, `chatgpt-*` | OpenAI | `https://api.openai.com` | `openai-completions` → `/v1/chat/completions` |
| `claude-*` | Anthropic | `https://api.anthropic.com` | `anthropic-messages` → `/v1/messages` |
| `deepseek-*` | DeepSeek | `https://api.deepseek.com` | `openai-completions` → `/v1/chat/completions` |
| `glm-*`, `chatglm-*` | 智谱 (Zhipu) | `https://open.bigmodel.cn/api/paas/v4` | `openai-completions` → `/v1/chat/completions` |
| `qwen-*`, `qwq-*`, `qvq-*` | 阿里通义 (DashScope) | `https://dashscope.aliyuncs.com/compatible-mode/v1` | `openai-completions` → `/v1/chat/completions` |
| `moonshot-*`, `kimi-*` | 月之暗面 (Moonshot) | `https://api.moonshot.cn/v1` | `openai-completions` → `/v1/chat/completions` |
| `doubao-*`, `ep-*` | 火山引擎 (豆包) | `https://ark.cn-beijing.volces.com/api/v3` | `openai-completions` → `/v1/chat/completions` |
| `minimax-*`, `abab-*` | MiniMax | `https://api.minimax.chat/v1` | `openai-completions` → `/v1/chat/completions` |
| `yi-*` | 零一万物 (01.AI) | `https://api.lingyiwanwu.com/v1` | `openai-completions` → `/v1/chat/completions` |
| `ernie-*`, `baidu-*` | 百度文心 | `https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop` | `openai-completions` |
| `grok-*` | xAI (Grok) | `https://api.x.ai/v1` | `openai-completions` → `/v1/chat/completions` |
| `gemini-*` | Google Gemini | `https://generativelanguage.googleapis.com/v1beta` | 特殊接口，需单独处理 |
| `mistral-*`, `codestral-*` | Mistral | `https://api.mistral.ai/v1` | `openai-completions` → `/v1/chat/completions` |
| `mimo-*` | 小米 (MiMo) | `https://api.xiaomimimo.com/anthropic` | `anthropic-messages` → `/v1/messages` |

**未匹配时：** 自动搜索 "[model_name] API documentation base_url" 确认配置。

### Step 2: 生成配置

根据匹配结果生成 config.patch 格式的配置，包含：
- provider 名称（用 provider 小写名作为 key）
- baseUrl
- apiKey（用户提供的）
- api 类型
- models 列表（至少包含用户提到的模型）
- 每个 model 的 contextWindow 和 maxTokens（根据已知信息填写默认值）

### Step 3: 应用配置

使用 `gateway config.patch` 写入配置并重启。

### Step 4: 自动校验

重启完成后执行校验脚本，汇报结果。

### 模型上下文/输出默认值

常见模型的 contextWindow 和 maxTokens 参考值：

| 模型 | contextWindow | maxTokens |
|------|-------------|-----------|
| gpt-4o | 128000 | 16384 |
| gpt-4-turbo | 128000 | 4096 |
| o1/o1-mini | 128000 | 100000 |
| claude-3.5-sonnet | 200000 | 8192 |
| claude-3-opus | 200000 | 4096 |
| deepseek-chat | 64000 | 8192 |
| deepseek-reasoner | 64000 | 8192 |
| glm-4 | 128000 | 4096 |
| qwen-max | 32000 | 8192 |
| qwen-long | 1000000 | 65536 |
| kimi-latest | 128000 | 4096 |
| doubao-pro | 4096 (volcengine) | 4096 |
| minimax-abab6.5 | 245760 | 4096 |
| mimo-v2-pro | 262144 | 8192 |

**未知模型：** contextWindow 默认 128000，maxTokens 默认 4096。搜文档确认后更新。

按以下顺序逐项检查，每项给出 ✅/❌ 结果：

### 1. 读取配置

使用 `read` 工具读取 `~/.openclaw/openclaw.json`，提取所有 `models.providers` 下的模型配置。

### 2. 配置完整性检查

对每个 provider 检查：
- `baseUrl` 是否存在且格式正确（http/https 开头）
- `apiKey` 是否存在且非空
- `api` 类型是否正确（`openai-completions` / `anthropic-messages` / `anthropic-completions`）
- 每个 model 的 `id` 是否存在
- `contextWindow` 和 `maxTokens` 是否设置

### 3. 网络连通性检查

使用 `exec` 执行 curl 测试每个 provider 的 baseUrl 是否可达：

```bash
curl -s -o /dev/null -w "%{http_code}" --connect-timeout 5 "<baseUrl>"
```

### 4. API 实际调用测试

对每个 provider，使用 `exec` 执行实际 API 调用测试：

**OpenAI 兼容接口 (`openai-completions`)**：
```bash
curl -s -X POST "<baseUrl>" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <apiKey>" \
  -d '{"model":"<modelId>","messages":[{"role":"user","content":"reply 1"}],"max_tokens":10}' \
  --connect-timeout 10 --max-time 30
```

**Anthropic 兼容接口 (`anthropic-messages`)**：
```bash
curl -s -X POST "<baseUrl>/v1/messages" \
  -H "Content-Type: application/json" \
  -H "x-api-key: <apiKey>" \
  -H "anthropic-version: 2023-06-01" \
  -d '{"model":"<modelId>","max_tokens":10,"messages":[{"role":"user","content":"reply 1"}]}' \
  --connect-timeout 10 --max-time 30
```

注意：对于 anthropic-messages，baseUrl 通常不带 `/v1/messages`，需要拼接。有些 baseUrl 已经包含路径，则直接用。

### 5. 结果解析

检查返回结果：
- HTTP 状态码是否为 200
- 响应体是否包含有效内容（非空）
- 对于 OpenAI 接口：检查 `choices[0].message.content` 是否非空
- 对于 Anthropic 接口：检查 `content[0].text` 是否非空
- 如果 content 为空但 reasoning_content 有值，说明模型把输出放到了思考字段，需标注配置问题

### 6. 生成报告

汇总输出格式：

```
## 模型配置校验报告

### Provider: <name>
- 配置完整性: ✅/❌
- 网络连通: ✅/❌ (HTTP <code>)
- API 认证: ✅/❌
- 模型返回: ✅/❌
- 模型: <modelId> → 状态: ✅/❌ [备注]

### 总结
- 可用模型: X/Y
- 不可用模型: [列表]
- 建议: [修复建议]
```

## URL 路径处理规则

不同 provider 的 baseUrl 结构不同，脚本自动处理：

| API 类型 | 处理规则 |
|----------|----------|
| `anthropic-messages` | 自动追加 `/v1/messages`（除非 URL 已包含） |
| `openai-completions` | 自动追加 `/chat/completions`（除非 URL 已以 `/chat/completions` 或 `/completions` 结尾） |

## 常见问题及修复

| 问题 | 原因 | 修复方式 |
|------|------|----------|
| HTTP 401/403 | API Key 无效或过期 | 更新 apiKey |
| HTTP 500 | 服务端错误/账户耗尽 | 检查账户余额或联系服务商 |
| 连接超时 | baseUrl 不可达 | 检查网络或更换 baseUrl |
| content 为空 | 接口类型不匹配 | 检查 api 字段是否正确（openai vs anthropic） |
| content 为空但 reasoning 有值 | 模型输出到了思考字段 | 增加 max_tokens 或切换接口类型 |
| Relay service error | 中转服务异常 | 检查中转服务状态和账户 |
| THINKING_ONLY | 推理模型思考未完成 | 正常现象，模型可用，增加 max_tokens 可获取完整输出 |
