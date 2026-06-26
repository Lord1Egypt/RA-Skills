# OpenClaw 配置文件格式说明

## 主配置文件位置
- 新版：`~/.openclaw/openclaw.json`
- 旧版（Clawdbot 迁移）：`~/.clawdbot/clawdbot.json`
- 模型专项：`~/.openclaw/models.json`

## 已激活模型检测

路由器通过以下方式判断用户是否激活了某个 provider：

```json
{
  "env": {
    "ANTHROPIC_API_KEY": "sk-ant-...",   // 有值 = Anthropic 已激活
    "OPENAI_API_KEY": "sk-...",          // 有值 = OpenAI 已激活
    "GEMINI_API_KEY": "AIza...",         // 有值 = Google 已激活
    "DEEPSEEK_API_KEY": "sk-...",        // 有值 = DeepSeek 已激活
    "XAI_API_KEY": "xai-...",            // 有值 = xAI/Grok 已激活
    "MOONSHOT_API_KEY": "sk-...",        // 有值 = Kimi 已激活
    "MINIMAX_API_KEY": "...",            // 有值 = MiniMax 已激活
    "ZAI_API_KEY": "...",               // 有值 = Zhipu/GLM 已激活
    "OPENROUTER_API_KEY": "sk-or-...",  // 有值 = OpenRouter 已激活
    "KILOCODE_API_KEY": "..."           // 有值 = Kilocode 已激活
  }
}
```

## 模型 allowlist（限制可用模型）

```json
{
  "agents": {
    "defaults": {
      "models": {
        "anthropic/claude-sonnet-4-6": {},
        "openai/gpt-4o": {},
        "google/gemini-2.5-flash": {}
      }
    }
  }
}
```

若存在 `agents.defaults.models`，路由器只在这个 allowlist 内选择模型。

## Ollama 检测

路由器向 `http://localhost:11434/api/tags` 发请求，成功响应说明 Ollama 在运行，
返回的模型列表即为本地可用模型。

## 自定义 provider

```json
{
  "models": {
    "providers": {
      "my-provider": {
        "baseUrl": "https://api.example.com/v1",
        "apiKey": "${MY_API_KEY}",
        "api": "openai-completions",
        "models": [
          { "id": "my-model-v1", "name": "My Custom Model" }
        ]
      }
    }
  }
}
```
