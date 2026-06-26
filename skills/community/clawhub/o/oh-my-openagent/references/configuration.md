## Configuration reference

Config file: `~/.config/opencode/oh-my-opencode.json`

### Top-level structure

```json
{
  "agents": { ... },
  "categories": { ... },
  "hooks": { ... },
  "commands": { ... },
  "mcps": { ... },
  "skills": { ... },
  "background_tasks": { ... },
  "lsp": { ... },
  "experimental": { ... }
}
```

### Agent overrides

Override any of the 11 agents by name (lowercase):

```json
{
  "agents": {
    "sisyphus": {
      "model": "claude-opus-4-6",
      "fallback_models": ["gpt-5.4"],
      "temperature": 0.7,
      "prompt_append": "Additional instructions here."
    },
    "oracle": {
      "model": "gpt-5.4",
      "thinking": true,
      "reasoningEffort": "high"
    },
    "explore": {
      "disable": true
    }
  }
}
```

Agent names: sisyphus, hephaestus, oracle, librarian, explore, multimodal-looker, prometheus, metis, momus, atlas, sisyphus-junior

### Category overrides

Override any of the 8 categories:

```json
{
  "categories": {
    "quick": {
      "model": "gemini-3-flash"
    },
    "ultrabrain": {
      "model": "claude-opus-4-6",
      "thinking": true
    }
  }
}
```

Category names: visual-engineering, ultrabrain, deep, artistry, quick, unspecified-low, unspecified-high, writing

### Hook configuration

Enable, disable, or configure hooks:

```json
{
  "hooks": {
    "hook-name": {
      "enable": true,
      "trigger": "keyword",
      "config": { ... }
    }
  }
}
```

### Background tasks

Control background task behavior:

```json
{
  "background_tasks": {
    "max_concurrent": 5,
    "timeout_ms": 120000
  }
}
```

### LSP configuration

Configure language servers:

```json
{
  "lsp": {
    "typescript": {
      "command": "typescript-language-server",
      "args": ["--stdio"]
    },
    "python": {
      "command": "pylsp"
    }
  }
}
```

### Model ID format

Model IDs must match provider expectations exactly:

- GitHub Copilot uses dots: `claude-sonnet-4.5`, `gpt-4o`
- OmO internal uses hyphens: `claude-opus-4-6`, `gpt-5-4`
- When overriding, use the OmO internal format (hyphens)

### Model resolution order

When an agent needs a model:

1. Check user override in `agents.{name}.model`
2. Use built-in default for that agent
3. Try each provider in priority order (Native → Kimi → Copilot → Venice → Go → Zen → Z.ai)
4. If model unavailable, try `fallback_models` in order
5. If all fail, error

### File locations

| File | Path | Purpose |
|------|------|---------|
| OpenCode config | `~/.config/opencode/opencode.json` | Plugin list, provider settings |
| OmO config | `~/.config/opencode/oh-my-opencode.json` | Agent/category/hook overrides |
| Auth tokens | `~/.local/share/opencode/auth.json` | Provider authentication |
| Skills (user) | `~/.config/opencode/skills/*/SKILL.md` | User-level skills |
| Skills (project) | `.opencode/skills/*/SKILL.md` | Project-level skills |

### Experimental features

```json
{
  "experimental": {
    "hashline": true,
    "parallel_tools": true
  }
}
```

- hashline: Enables hash-anchored edits (LINE#ID content hash system) for more reliable file editing
- parallel_tools: Enables parallel tool execution
