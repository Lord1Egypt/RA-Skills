# 模型管理参考

## 模型选择顺序
1. `agents.defaults.model.primary` — 主力模型
2. `agents.defaults.model.fallbacks[]` — 按顺序回退
3. 每个提供商内先进行认证配置文件轮换，全部失败后才移到下一个回退模型

## 模型引用格式
- 格式: `provider/model` (如 `openai/gpt-5.2`)
- 引用会规范化为小写
- 别名: `z.ai/*` → `zai/*`
- OpenRouter 模型含 `/`: 必须带提供商前缀 (如 `openrouter/moonshotai/kimi-k2`)

## 图像模型
- `agents.defaults.imageModel` 仅在主力模型不支持图像输入时使用
- 有独立的 fallbacks 链

## 模型白名单
设置 `agents.defaults.models` 后成为 `/model` 白名单:
```json5
{
  agents: { defaults: {
    model: { primary: "anthropic/claude-sonnet-4-5" },
    models: {
      "anthropic/claude-sonnet-4-5": { alias: "Sonnet" },
      "anthropic/claude-opus-4-5": { alias: "Opus" }
    }
  }}
}
```
未在白名单中的模型会报 "Model is not allowed"。清除白名单: 删除 `agents.defaults.models`。

## 认证配置文件轮换

### 选择顺序
1. `auth.order[provider]` (显式配置)
2. `auth.profiles` 中该提供商的条目
3. `auth-profiles.json` 中存储的条目

### 轮询规则 (无显式顺序时)
- OAuth 优先于 API Key
- 同类型中最久未用的优先
- 冷却/禁用的移到末尾

### 会话粘性
- 每个会话固定认证配置文件(缓存友好)
- 重置条件: `/new`、`/reset`、压缩完成、配置文件冷却
- `/model …@<profileId>` 手动固定，锁定到该配置文件

### 冷却时间 (认证/速率限制失败)
指数退避: 1min → 5min → 25min → 1h(上限)
存储: `auth-profiles.json` → `usageStats.cooldownUntil`

### 账单禁用 (额度不足)
退避: 5h 起步，翻倍，上限 24h
24h 无失败则重置计数器
存储: `usageStats.disabledUntil` + `disabledReason: "billing"`

### 相关配置
```
auth.cooldowns.billingBackoffHours      # 账单退避起始(默认5h)
auth.cooldowns.billingMaxHours          # 账单退避上限(默认24h)
auth.cooldowns.failureWindowHours       # 失败窗口(默认1h)
```

## 内置提供商 (无需 models.providers)

| 提供商 | 环境变量 | 示例模型 | CLI |
|--------|----------|----------|-----|
| `openai` | OPENAI_API_KEY | openai/gpt-5.2 | `onboard --auth-choice openai-api-key` |
| `anthropic` | ANTHROPIC_API_KEY | anthropic/claude-opus-4-5 | `onboard --auth-choice token` |
| `openai-codex` | OAuth(ChatGPT) | openai-codex/gpt-5.2 | `onboard --auth-choice openai-codex` |
| `opencode` | OPENCODE_API_KEY | opencode/claude-opus-4-5 | `onboard --auth-choice opencode-zen` |
| `google` | GEMINI_API_KEY | google/gemini-3-pro-preview | `onboard --auth-choice gemini-api-key` |
| `google-vertex` | gcloud ADC | - | - |
| `google-antigravity` | OAuth插件 | - | `plugins enable google-antigravity-auth` |
| `google-gemini-cli` | OAuth插件 | - | `plugins enable google-gemini-cli-auth` |
| `zai` | ZAI_API_KEY | zai/glm-4.7 | `onboard --auth-choice zai-api-key` |
| `openrouter` | OPENROUTER_API_KEY | openrouter/anthropic/claude-sonnet-4-5 | - |
| `xai` | XAI_API_KEY | - | - |
| `groq` | GROQ_API_KEY | - | - |
| `cerebras` | CEREBRAS_API_KEY | - | - |
| `mistral` | MISTRAL_API_KEY | - | - |
| `github-copilot` | COPILOT_GITHUB_TOKEN | - | - |
| `vercel-ai-gateway` | AI_GATEWAY_API_KEY | vercel-ai-gateway/anthropic/claude-opus-4.5 | - |
| `synthetic` | SYNTHETIC_API_KEY | synthetic/hf:MiniMaxAI/MiniMax-M2.1 | - |

## 自定义提供商 (models.providers)

### 配置模板
```json5
{
  models: {
    mode: "merge",  // merge=合并内置, replace=仅自定义
    providers: {
      "my-provider": {
        baseUrl: "https://api.example.com/v1",
        apiKey: "${MY_API_KEY}",
        api: "openai-completions",  // 或 "anthropic-messages"
        models: [{
          id: "model-id",
          name: "Display Name",
          reasoning: false,
          input: ["text"],  // 或 ["text", "image"]
          cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
          contextWindow: 128000,
          maxTokens: 8192
        }]
      }
    }
  }
}
```

### 字段默认值 (省略时)
- reasoning: false
- input: ["text"]
- cost: 全0
- contextWindow: 200000
- maxTokens: 8192

### 常见自定义提供商示例

**Moonshot AI (Kimi)**
```json5
moonshot: {
  baseUrl: "https://api.moonshot.ai/v1",
  apiKey: "${MOONSHOT_API_KEY}",
  api: "openai-completions",
  models: [{ id: "kimi-k2.5", name: "Kimi K2.5" }]
}
```

**Ollama (本地)**
```json5
// 自动检测 http://127.0.0.1:11434/v1，通常无需配置
ollama: {
  baseUrl: "http://127.0.0.1:11434/v1",
  api: "openai-completions",
  models: [{ id: "llama3.3", name: "Llama 3.3" }]
}
```

**LM Studio / vLLM / LiteLLM**
```json5
lmstudio: {
  baseUrl: "http://localhost:1234/v1",
  apiKey: "LMSTUDIO_KEY",
  api: "openai-completions",
  models: [{ id: "model-id", name: "Model Name", contextWindow: 200000, maxTokens: 8192 }]
}
```

**MiniMax (Anthropic兼容)**
参见 providers/minimax 文档

**Qwen OAuth (免费)**
```bash
openclaw plugins enable qwen-portal-auth
openclaw models auth login --provider qwen-portal --set-default
# 模型: qwen-portal/coder-model, qwen-portal/vision-model
```

## 模型扫描 (OpenRouter 免费模型)
```bash
openclaw models scan [选项]
  --provider openrouter     # 提供商筛选
  --max-candidates 5        # 回退列表大小
  --set-default             # 设为主力模型
  --set-image               # 设为绘图模型
  --no-probe                # 跳过实时探测
  --min-params <b>          # 最小参数量(十亿)
  --max-age-days <days>     # 跳过旧模型
  --yes                     # 非交互模式
```
排名: 图像支持 > 工具延迟 > 上下文大小 > 参数数量

## 模型注册表
自定义提供商写入 `~/.openclaw/agents/<agentId>/models.json`
`models.mode=merge` 时与内置合并，`replace` 时仅用自定义

## /model 聊天命令
```
/model              # 编号选择器
/model list         # 同上
/model 3            # 选择第3个
/model provider/id  # 直接指定
/model status       # 详细状态(认证/端点)
```
