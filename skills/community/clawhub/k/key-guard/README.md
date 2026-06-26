# key-guard

A local MCP server that keeps API keys off Claude's servers.

## Why This Exists

When Claude reads a file containing an API key, the raw key content gets sent to Claude's servers. key-guard prevents this by acting as a local middleman — Claude calls a tool, the tool reads the key and makes the API call locally, and only the result is returned to Claude.

## Approaches

| Approach | How it prevents key exposure | Auto? |
|----------|------------------------------|-------|
| **MCP Server** | Claude calls a local tool; tool reads key, returns only results | ❌ Must @-mention |
| **Hooks** | Intercept file reads before sending to Claude | ✅ Automatic (not yet in CLI) |
| **Skill** | Teaches Claude to always route key ops through MCP | ❌ Prompt-based |

**Best combo:** MCP (local proxy) + Skill (behavioral guardrail)

## Structure

```
key-guard/
├── key-guard.js              # MCP server (run this)
├── .env.example              # Template — copy to .env and fill in keys
├── .env                      # Your actual keys (never share this)
└── .agents/skills/key-guard/ # Copilot skill (tells Claude to use MCP)
    └── SKILL.md
```

## MCP Tools

| Tool | What it does |
|------|-------------|
| `list_keys` | Returns all key **names** from `.env` and shell profiles — never values |
| `validate_key` | Checks if a key exists — never reveals the value |
| `call_api` | Makes authenticated HTTP requests locally — Claude only sees the response |
| `read_file_masked` | Reads a script/config file with key values replaced by `{{KEY_NAME}}` placeholders |
| `write_file_with_keys` | Writes a file, substituting `{{KEY_NAME}}` placeholders with real key values |

## Setup

### 1. Add your keys
```bash
cp .env.example .env
# Edit .env with your real API keys
```

### 2. Register MCP Server
Copy the MCP config to your Copilot CLI config directory:
```bash
cp .agents/mcp-config.json ~/.copilot/mcp-config.json
```

Then edit `~/.copilot/mcp-config.json` and replace `/path/to/key-guard` with the actual path to this repo.

Then replace `/path/to/key-guard` with your actual repo path:
```json
{
  "mcpServers": {
    "key-guard": {
      "command": "node",
      "args": ["/path/to/key-guard/key-guard.js"]
    }
  }
}
```

Restart Copilot CLI and the MCP will be ready.

### 3. (Optional) Install Skill
If you want Claude to auto-use this MCP in a project:
```bash
/skills install /path/to/key-guard/.agents/skills/key-guard
```

