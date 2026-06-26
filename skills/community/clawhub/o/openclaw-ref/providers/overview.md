# 提供商配置参考

## 内置提供商 (无需 models.providers)

| 提供商 | 环境变量 | 示例模型 | 认证方式 |
|--------|----------|----------|----------|
| `openai` | OPENAI_API_KEY | openai/gpt-5.2 | API Key |
| `openai-codex` | OAuth | openai-codex/gpt-5.2 | ChatGPT登录 |
| `anthropic` | ANTHROPIC_API_KEY | anthropic/claude-opus-4-5 | API Key / setup-token |
| `opencode` | OPENCODE_API_KEY | opencode/claude-opus-4-5 | API Key |
| `google` | GEMINI_API_KEY | google/gemini-3-pro-preview | API Key |
| `google-vertex` | gcloud ADC | - | ADC |
| `google-antigravity` | OAuth插件 | - | `plugins enable google-antigravity-auth` |
| `google-gemini-cli` | OAuth插件 | - | `plugins enable google-gemini-cli-auth` |
| `zai` | ZAI_API_KEY | zai/glm-4.7 | API Key |
| `openrouter` | OPENROUTER_API_KEY | openrouter/anthropic/claude-sonnet-4-5 | API Key |
| `xai` | XAI_API_KEY | - | API Key |
| `groq` | GROQ_API_KEY | - | API Key |
| `cerebras` | CEREBRAS_API_KEY | - | API Key |
| `mistral` | MISTRAL_API_KEY | - | API Key |
| `github-copilot` | COPILOT_GITHUB_TOKEN | - | Token |
| `vercel-ai-gateway` | AI_GATEWAY_API_KEY | vercel-ai-gateway/anthropic/claude-opus-4.5 | API Key |

## OpenAI

### 方式A: API Key
```json5
{ env: { OPENAI_API_KEY: "sk-..." },
  agents: { defaults: { model: { primary: "openai/gpt-5.2" } } } }
```
CLI: `openclaw onboard --auth-choice openai-api-key`

### 方式B: Codex订阅 (OAuth)
```json5
{ agents: { defaults: { model: { primary: "openai-codex/gpt-5.2" } } } }
```
CLI: `openclaw onboard --auth-choice openai-codex` 或 `openclaw models auth login --provider openai-codex`

## Anthropic

### 方式A: API Key
```json5
{ env: { ANTHROPIC_API_KEY: "sk-ant-..." },
  agents: { defaults: { model: { primary: "anthropic/claude-opus-4-5" } } } }
```

### 方式B: setup-token (推荐订阅用户)
```bash
claude setup-token                                    # 任意机器生成
openclaw models auth setup-token --provider anthropic # 网关主机粘贴
openclaw models auth paste-token --provider anthropic # 远程粘贴
```

### 提示缓存
```json5
agents: { defaults: { models: {
  "anthropic/claude-opus-4-5": { params: { cacheRetention: "short" } }  // none|short(5min)|long(1h)
}}}
```
API Key认证默认 `short`。

### 常见问题
- "OAuth token refresh failed": 用 setup-token 重新认证
- "No API key found": 认证按智能体独立，新智能体需重新设置
- "All in cooldown": `openclaw models status --json` 查看 `auth.unusableProfiles`

## OpenRouter
```json5
{ env: { OPENROUTER_API_KEY: "sk-or-..." },
  agents: { defaults: { model: { primary: "openrouter/anthropic/claude-sonnet-4-5" } } } }
```
模型格式: `openrouter/<provider>/<model>`

## 自定义提供商 (models.providers)

### 通用模板
```json5
models: {
  mode: "merge",  // merge(合并内置) | replace(仅自定义)
  providers: {
    "my-provider": {
      baseUrl: "https://api.example.com/v1",
      apiKey: "${MY_API_KEY}",
      api: "openai-completions",  // 或 "anthropic-messages"
      models: [{
        id: "model-id", name: "Display Name",
        reasoning: false, input: ["text"],
        contextWindow: 128000, maxTokens: 8192
      }]
    }
  }
}
```

### Moonshot AI (Kimi)
```json5
moonshot: {
  baseUrl: "https://api.moonshot.ai/v1",
  apiKey: "${MOONSHOT_API_KEY}", api: "openai-completions",
  models: [{ id: "kimi-k2.5", name: "Kimi K2.5" }]
}
```
Kimi Coding (Anthropic兼容): 提供商 `kimi-coding`, api: `anthropic-messages`

### DeepSeek
```json5
deepseek: {
  baseUrl: "https://api.deepseek.com/v1",
  apiKey: "${DEEPSEEK_API_KEY}", api: "openai-completions",
  models: [{ id: "deepseek-chat", name: "DeepSeek Chat" }]
}
```

### Ollama (本地)
自动检测 `http://127.0.0.1:11434/v1`，通常无需配置。
```bash
ollama pull llama3.3
```
```json5
{ agents: { defaults: { model: { primary: "ollama/llama3.3" } } } }
```

### MiniMax
```json5
minimax: {
  baseUrl: "https://api.minimax.chat/v1",
  apiKey: "${MINIMAX_API_KEY}", api: "anthropic-messages",
  models: [{ id: "MiniMax-M2.1", name: "MiniMax M2.1" }]
}
```

### Synthetic
```json5
synthetic: {
  baseUrl: "https://api.synthetic.new/anthropic",
  apiKey: "${SYNTHETIC_API_KEY}", api: "anthropic-messages",
  models: [{ id: "hf:MiniMaxAI/MiniMax-M2.1", name: "MiniMax M2.1" }]
}
```

### Qwen OAuth (免费)
```bash
openclaw plugins enable qwen-portal-auth
openclaw models auth login --provider qwen-portal --set-default
```
模型: `qwen-portal/coder-model`, `qwen-portal/vision-model`

### LM Studio / vLLM / LiteLLM
```json5
lmstudio: {
  baseUrl: "http://localhost:1234/v1",
  apiKey: "LMSTUDIO_KEY", api: "openai-completions",
  models: [{ id: "model-id", name: "Model", contextWindow: 200000, maxTokens: 8192 }]
}
```

### Amazon Bedrock
需要 AWS 凭证 + Bedrock 访问权限。
```json5
bedrock: {
  baseUrl: "https://bedrock-runtime.us-east-1.amazonaws.com",
  api: "anthropic-messages",
  models: [{ id: "anthropic.claude-3-5-sonnet-20241022-v2:0", name: "Claude 3.5 Sonnet" }]
}
```

### Venice AI (隐私优先)
```json5
venice: {
  baseUrl: "https://api.venice.ai/api/v1",
  apiKey: "${VENICE_API_KEY}", api: "openai-completions",
  models: [{ id: "llama-3.3-70b", name: "Llama 3.3 70B" }]
}
```

### Xiaomi
```json5
xiaomi: {
  baseUrl: "https://api.xiaomi.com/v1",
  apiKey: "${XIAOMI_API_KEY}", api: "openai-completions",
  models: [{ id: "MiMo-7B-RL", name: "MiMo 7B" }]
}
```

## 转录提供商

### Deepgram
```json5
tts: { provider: "deepgram" }
// 或
env: { DEEPGRAM_API_KEY: "..." }
```

## 认证管理CLI
```bash
openclaw models auth setup-token --provider anthropic
openclaw models auth paste-token --provider <name> --profile-id <id>
openclaw models auth login --provider <name> [--set-default]
openclaw models auth order set --provider <name> <profile1> <profile2>
openclaw models status [--json] [--probe]
```
