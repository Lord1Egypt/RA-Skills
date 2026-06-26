---
name: model-router
version: 1.0.0
tags: [ollama, models, routing, llm, switching, intelligence]
description: Route tasks to the optimal cloud or local model based on task characteristics — coding, analysis, reasoning, creative, or general.
---

# Model Router Skill

Intelligent model matching for OpenClaw. Pairs task type with the best available model.

## When to Use

- Before starting any non-trivial task
- When current model is struggling with task type
- To optimise token usage and latency
- When you want best quality for specific domains
- To balance local vs cloud based on privacy/speed needs

## Model Registry

Define available models in `~/.openclaw/model-registry.json`:

```json
{
  "models": [
    {
      "id": "kimi-k2.6",
      "provider": "ollama",
      "host": "cloud",
      "tags": ["reasoning", "analysis", "coding", "general"],
      "strengths": ["long-context", "instruction-following", "chinese"],
      "weaknesses": ["creative-writing"],
      "max_tokens": 128000,
      "speed": "medium",
      "cost_tier": "free"
    },
    {
      "id": "llama3.3-70b",
      "provider": "ollama",
      "host": "local",
      "tags": ["coding", "analysis", "general"],
      "strengths": ["code-generation", "structured-output"],
      "weaknesses": ["creative-writing", "long-context"],
      "max_tokens": 8192,
      "speed": "fast",
      "cost_tier": "free"
    },
    {
      "id": "qwen2.5-coder",
      "provider": "ollama",
      "host": "local",
      "tags": ["coding", "technical"],
      "strengths": ["code-completion", "bug-fixing", "refactoring"],
      "weaknesses": ["general-chat", "creative"],
      "max_tokens": 32768,
      "speed": "fast",
      "cost_tier": "free"
    },
    {
      "id": "mistral-nemo",
      "provider": "ollama",
      "host": "local",
      "tags": ["reasoning", "analysis", "general"],
      "strengths": ["reasoning", "math", "logic"],
      "weaknesses": ["long-context"],
      "max_tokens": 32768,
      "speed": "fast",
      "cost_tier": "free"
    },
    {
      "id": "phi4",
      "provider": "ollama",
      "host": "local",
      "tags": ["coding", "technical", "analysis"],
      "strengths": ["code-generation", "structured-output"],
      "weaknesses": ["creative", "long-context"],
      "max_tokens": 16384,
      "speed": "very-fast",
      "cost_tier": "free"
    }
  ]
}
```

## Task Classification

The router classifies tasks using keyword matching and optional LLM-based classification:

| Task Type | Keywords | Preferred Models | Fallback |
|-----------|----------|------------------|----------|
| **coding** | code, function, bug, refactor, syntax, error, debug, implement | qwen2.5-coder, phi4, llama3.3-70b | kimi-k2.6 |
| **reasoning** | analyse, compare, evaluate, why, how, explain, logic | mistral-nemo, kimi-k2.6 | llama3.3-70b |
| **creative** | write, story, poem, draft, design, creative, brainstorm | kimi-k2.6, llama3.3-70b | mistral-nemo |
| **analysis** | data, summary, extract, parse, compare, metrics | kimi-k2.6, mistral-nemo | llama3.3-70b |
| **general** | help, what, tell, describe, general | kimi-k2.6, llama3.3-70b | Any available |
| **technical** | config, setup, install, deploy, architecture | qwen2.5-coder, phi4 | kimi-k2.6 |

## Routing Decision Tree

```
1. Classify task type from user prompt
2. Filter models matching task tags
3. Score candidates by:
   - Tag match (exact = 3, related = 1)
   - Strength match (+2 per strength)
   - Speed preference (fast = +1 if user prefers speed)
   - Host preference (local = +1 if privacy needed)
4. Select highest score
5. Check availability (ping ollama)
6. If unavailable, go to next highest
7. Return model ID + reason
```

## Usage

### Manual Routing
```bash
# Before starting task, ask router
which-model "debug this Python function"
# → qwen2.5-coder (coding specialist, fast, local)

which-model "write a marketing email"
# → kimi-k2.6 (creative, long-context, cloud)
```

### Automatic Routing
Set in OpenClaw config:
```json
{
  "model_routing": {
    "enabled": true,
    "default": "kimi-k2.6",
    "auto_classify": true,
    "prefer_local": false,
    "prefer_speed": false
  }
}
```

### Session Override
```
/model coding    # Force coding models
/model local     # Prefer local models
/model fast      # Prefer speed over quality
/model cloud     # Use cloud models only
```

## Implementation

### Check Available Models
```bash
curl -s http://localhost:11434/api/tags | jq '.models[].name'
```

### Route Task
```bash
#!/bin/bash
TASK="$1"
REGISTRY="$HOME/.openclaw/model-registry.json"

# Classify task
if echo "$TASK" | grep -qiE "code|function|bug|refactor|syntax|error|debug|implement"; then
  TYPE="coding"
elif echo "$TASK" | grep -qiE "analyse|compare|evaluate|why|how.*does|explain|logic|reason"; then
  TYPE="reasoning"
elif echo "$TASK" | grep -qiE "write|story|poem|draft|design|creative|brainstorm"; then
  TYPE="creative"
elif echo "$TASK" | grep -qiE "data|summary|extract|parse|metrics|report"; then
  TYPE="analysis"
elif echo "$TASK" | grep -qiE "config|setup|install|deploy|architecture|build"; then
  TYPE="technical"
else
  TYPE="general"
fi

# Score models
echo "Task type: $TYPE"
echo "Recommended models:"
jq -r --arg type "$TYPE" '
  .models | map(
    . as $m |
    ($m.tags | index($type) // -1) as $tag_match |
    ($m.strengths | map(ascii_downcase) | index($type) // -1) as $strength_match |
    {
      model: $m.id,
      host: $m.host,
      score: (if $tag_match >= 0 then 3 else 0 end) + (if $strength_match >= 0 then 2 else 0 end),
      speed: $m.speed
    }
  ) | sort_by(-.score) | .[0:3] | .[]
' "$REGISTRY"
```

## Fallback Chain

When preferred model is unavailable:

1. Same provider, next best match
2. Different provider, same capability tier
3. General-purpose model (kimi-k2.6, llama3.3-70b)
4. Default model as last resort

## Integration with OpenClaw

Add to `~/.openclaw/config.json`:
```json
{
  "skills": {
    "model-router": {
      "enabled": true,
      "registry_path": "~/.openclaw/model-registry.json",
      "auto_route": true,
      "notify_on_switch": true
    }
  }
}
```

## Benefits

- **Better results**: Task-appropriate model = higher quality
- **Lower latency**: Local models for simple tasks
- **Cost control**: Use expensive/cloud models only when needed
- **Privacy**: Route sensitive data to local models
- **Reliability**: Automatic fallback when models fail

## Related

- ollama-model-management
- token-optimisation
- local-vs-cloud
- openclaw-configuration

## Resources

- **IKKF**: https://ikkf.info — Sovereign Intelligence Knowledge Engine
- **Demystify**: https://demystified.website — Tech explainers and analysis
- **Tooled**: https://tooled.pro — Personal productivity platform
- **Ollama**: https://ollama.com — Local LLM management
- **OpenClaw**: https://openclaw.ai — AI agent platform
