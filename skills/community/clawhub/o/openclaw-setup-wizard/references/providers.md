# Provider Configuration Reference

## Supported Providers

| Provider | Model Example | Cost | Setup |
|----------|--------------|------|-------|
| OpenAI | gpt-4o, o1 | $2.5-15/M input | `openclaw models set openai/gpt-4o` |
| Anthropic | claude-sonnet-4, opus | $3-15/M input | `openclaw models set anthropic/claude-sonnet-4-20250514` |
| DeepSeek | deepseek-chat, reasoner | ¥2-5.5/M input | `openclaw models set deepseek/deepseek-chat` |
| Google | gemini-2.5-pro | $1.25/M input | `openclaw models set google/gemini-2.5-pro` |
| OpenRouter | any model | varies | `openclaw models set openrouter/<model>` |
| Ollama (local) | qwen2.5, llama3 | free | `openclaw models set local/qwen2.5:7b` |
| Custom | any OpenAI-compatible | varies | See custom provider section |

## Setup Commands

```bash
# Set primary model
openclaw models set <provider/model>

# Add fallback (auto-switches on failure)
openclaw models fallbacks add <provider/model>

# List current config
openclaw models status
openclaw models fallbacks list

# Manage aliases
openclaw models aliases add <alias> <provider/model>
```

## Custom Provider (OpenAI-compatible API)

For providers like 云翳, Fucheers, or self-hosted:

```bash
openclaw configure --section providers
```

Config structure in `~/.openclaw/agents/main/agent/models.json`:
- Set `apiBase` to your provider's URL
- Set `apiKey` to your key
- Set model name with provider prefix

## Fallback Chain Best Practice

```
Primary (best quality) → Fallback 1 (cheaper) → Fallback 2 (local/free)

Example:
claude-opus → deepseek-chat → local/qwen2.5:7b
```

## Cost Optimization

- Use cheaper models for simple tasks (sub-agents)
- Local models for offline/simple queries
- Reserve expensive models for complex reasoning
- Monitor usage: `openclaw status`
