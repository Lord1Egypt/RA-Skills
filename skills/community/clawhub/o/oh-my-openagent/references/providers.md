## Provider setup and model routing

### Provider priority chain

OmO resolves models through providers in this order:

1. **Native** — Built-in to OpenCode
2. **Kimi for Coding** — Kimi API
3. **GitHub Copilot** — OAuth-based, free with GitHub account
4. **Venice** — Venice AI API
5. **OpenCode Go** — OpenCode's own routing
6. **OpenCode Zen** — OpenCode's Zen tier
7. **Z.ai Coding Plan** — Z.ai API

When a model is requested, OmO tries each provider in order until one can serve it.

### Authentication methods

| Provider | Auth Method | Setup |
|----------|-------------|-------|
| GitHub Copilot | OAuth | `opencode auth login --provider copilot` |
| Google | OAuth | `opencode auth login --provider google` |
| OpenCode Zen | API key | Add key in `~/.local/share/opencode/auth.json` |
| AIHubMix | API key | Add key in auth.json |

Auth tokens stored in: `~/.local/share/opencode/auth.json`

### Model families

#### Claude-like models
- claude-opus-4-6 (highest capability)
- claude-sonnet-4-6 (balanced)
- claude-haiku-4-5 (fast/cheap)

#### GPT models
- gpt-5.4 (highest reasoning)
- gpt-5.3-codex (code-optimized)
- gpt-5-nano (fast/cheap)

#### Gemini models
- gemini-3.1-pro (high capability)
- gemini-3-flash (fast/cheap)

#### Speed-focused models
- grok-code-fast-1 (very fast)
- minimax-m2.5-free (free tier)

### Model ID conventions

- OmO internal format uses hyphens: `claude-opus-4-6`
- GitHub Copilot uses dots: `claude-sonnet-4.5`
- Always use hyphens in `oh-my-opencode.json`
- OmO handles translation to provider format

### Adding third-party models

If a model is available through a configured provider (e.g., AIHubMix), you can use it by specifying the provider prefix:

```json
{
  "agents": {
    "librarian": {
      "model": "aihubmix/coding-glm-4.7-free"
    }
  }
}
```

### Checking available models

Models available to you depend on which providers are authenticated. Check:

1. Auth status: Look at `~/.local/share/opencode/auth.json`
2. Provider models: Each provider exposes different model lists
3. Free models: Some models are free (e.g., `minimax-m2.5-free`, `aihubmix/coding-glm-4.7-free`)

### Model selection per agent

Each agent has a default model optimized for its role:

| Agent Role | Needs | Default Choice |
|-----------|-------|----------------|
| Orchestrator (Sisyphus) | Broad reasoning + tool use | claude-opus-4-6 |
| Deep worker (Hephaestus) | Code generation + large context | gpt-5.3-codex |
| Consultant (Oracle) | Deep reasoning | gpt-5.4 |
| Search (Librarian) | Fast, large context | gemini-3-flash |
| Grep (Explore) | Very fast, cheap | grok-code-fast-1 |
| Vision (Multimodal-Looker) | Image understanding | gpt-5.3-codex |

Override any of these in config if your provider setup differs.
