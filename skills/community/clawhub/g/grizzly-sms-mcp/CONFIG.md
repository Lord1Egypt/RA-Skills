# OpenClaw Configuration for Grizzly SMS Skill

OpenClaw works with **skills only** (no mcpServers). This skill uses the **exec** tool to run scripts that call the Grizzly API.

## Config Location

- **macOS**: `~/.openclaw/openclaw.json`
- **Windows**: `%APPDATA%\.openclaw\openclaw.json`
- **Linux**: `~/.openclaw/openclaw.json`

## Required Configuration

### 1. Load the skill

**Option A — Install from GitHub (recommended):**
```bash
openclaw skills add https://github.com/GrizzlySMS-Git/grizzly-sms-mcp
```

**Option B — Add via extraDirs** (if you cloned manually):
```json5
{
  "skills": {
    "load": {
      "extraDirs": ["/path/to/grizzly-sms-mcp"]
    }
  }
}
```

### 2. Enable skill (API key optional)

**Option A — API key in config** (key is always available):

```json5
{
  "skills": {
    "entries": {
      "grizzly_sms": {
        "enabled": true,
        "env": {
          "GRIZZLY_SMS_API_KEY": "your_api_key_from_grizzlysms_com"
        }
      }
    }
  }
}
```

**Option B — API key in dialog** (agent asks during conversation):

```json5
{
  "skills": {
    "entries": {
      "grizzly_sms": {
        "enabled": true
      }
    }
  }
}
```

When the user asks for something (e.g. "register an Instagram account for Jamaica"), the agent will ask: *Please provide your Grizzly SMS API key*. After the user provides it, the agent passes it via exec env.

## Full Example (merge with your config)

```json5
{
  "skills": {
    "load": {
      "extraDirs": ["/path/to/grizzly-sms-mcp"]
    },
    "entries": {
      "grizzly_sms": {
        "enabled": true
      }
    }
  }
}
```

## Setup Steps

1. Ensure the skill folder is at the path in `extraDirs`
2. (Optional) Add API key in `env` — or let the agent ask for it in the dialog
3. Restart: `npx openclaw gateway restart`

### 3. Enable browser tool (for registration workflow)

To let the agent open a browser and fill registration forms, enable the **browser** tool. Add to `openclaw.json`:

```json5
{
  "browser": {
    "enabled": true,
    "headless": false
  },
  "agents": {
    "list": [
      {
        "id": "main",
        "tools": {
          "alsoAllow": ["agents_list", "exec", "browser"]
        }
      }
    ]
  }
}
```

On Mac, run `openclaw browser install` once to download Chromium. The browser will open visibly (headless: false) so the user can see the registration process.

### 4. Ensure exec tool is available

The agent must use the **exec** tool to run the script. With `tools.profile: "coding"`, exec is usually included. If the agent says it cannot call methods, add:

```json5
{
  "agents": {
    "list": [
      {
        "id": "main",
        "tools": {
          "alsoAllow": ["agents_list", "exec", "browser"]
        }
      }
    ]
  }
}
```

### 5. Allow exec on gateway host

If you get "exec tool was not permitted to run on the gateway host", configure exec to run on the gateway and add approvals.

**Option A — Allowlist (recommended):** Add to `openclaw.json`:

```json5
{
  "tools": {
    "exec": {
      "host": "gateway",
      "security": "allowlist",
      "ask": "on-miss"
    }
  }
}
```

Then create or edit `~/.openclaw/exec-approvals.json` (macOS) and add `node` to the allowlist. Run `which node` to get your path:

```json
{
  "version": 1,
  "defaults": {
    "security": "allowlist",
    "ask": "on-miss",
    "askFallback": "deny"
  },
  "agents": {
    "main": {
      "security": "allowlist",
      "ask": "on-miss",
      "allowlist": [
        { "pattern": "/opt/homebrew/bin/node" },
        { "pattern": "/usr/local/bin/node" }
      ]
    }
  }
}
```

**Option B — Full (dev only, less secure):** If you trust the environment:

```json5
{
  "tools": {
    "exec": {
      "host": "gateway",
      "security": "full",
      "ask": "off"
    }
  }
}
```

Restart after changes: `npx openclaw gateway restart`

## Important

- **No mcpServers** — OpenClaw uses skills + exec only
- **Node.js** — The script requires Node.js on the gateway host
- **Browser tool** — For full registration workflow (open browser, fill forms), enable browser and add it to tools.alsoAllow
- **Grizzly MCP in Docker** — Not used; the skill calls Grizzly API directly via the script
- Get API key: register on [grizzlysms.com](https://grizzlysms.com/), then go to the API section ([grizzlysms.com/docs](https://grizzlysms.com/docs)) and copy the key
