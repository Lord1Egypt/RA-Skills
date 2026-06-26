# MCP Configuration Guide

> OpenCode MCP (Model Context Protocol) integration configuration reference

---

## Contents

- [Configuration Levels](#configuration-levels)
- [Security Considerations](#security-considerations)
- [Global MCP Configuration](#global-mcp-configuration)
  - [Playwright MCP](#playwright-mcp-ui-automation-testing)
  - [Context7 MCP](#context7-mcp-context-management)
- [Project-level MCP Configuration](#project-level-mcp-configuration)
  - [Supabase MCP](#supabase-mcp-database)
- [Complete Configuration Example](#complete-configuration-example)
- [Running Constraints](#running-constraints)
- [Adding New MCP](#adding-new-mcp)
- [Troubleshooting](#troubleshooting)

---

## Configuration Levels

| Level | Location | Purpose | Example |
|-------|----------|---------|---------|
| Global | `~/.config/opencode/opencode.json` | Common tools | Playwright, Context7 |
| Project | `<project>/.opencode/opencode.json` | Project-specific tools | Supabase |

---

## Security Considerations

### ⚠️ Remote Code Execution Risk

MCP servers run as separate processes. Different configuration methods have different security profiles:

| Method | Risk Level | Description |
|--------|------------|-------------|
| **Global Install** | Low | Code verified once, runs locally |
| **npx** | Medium | Downloads remote code each run |

### ✅ Recommended: Global Install Only

**Why**: Verifies package integrity once, no repeated downloads, no network dependency at runtime.

**Steps:**
```bash
# 1. Verify package
npm view <package-name>

# 2. Install globally
npm install -g <package-name>

# 3. Configure with binary name
"command": ["<binary-name>"]
```

---

## Global MCP Configuration

### Playwright MCP (UI Testing)

**Package**: `playwright-mcp-server` (search npm for current package name)

```bash
npm install -g playwright-mcp-server
```

```json
{
  "mcp": {
    "playwright": {
      "type": "local",
      "command": ["playwright-mcp-server"]
    }
  }
}
```

**Purpose:**
- UI automation testing
- Page interaction simulation
- Screenshot comparison

**Tool chain:**
| Tool | Purpose |
|------|---------|
| `browser snapshot` | Get page state |
| `browser act` | Click/input operations |
| `browser screenshot` | Screenshot comparison |

---

### Context7 MCP (Context Management)

**Package**: `context7-mcp` (search npm for current package name)

```bash
npm install -g context7-mcp
```

```json
{
  "mcp": {
    "context7": {
      "type": "local",
      "command": ["context7-mcp"],
      "environment": {
        "CONTEXT7_API_KEY": "<your-api-key>",
        "DEFAULT_MINIMUM_TOKENS": "10000"
      }
    }
  }
}
```

**Purpose:**
- Long-term context storage
- Cross-session memory

**Get API Key:** https://upstash.com

---

## Project-level MCP Configuration

### Supabase MCP (Database)

**Package**: `mcp-server-supabase` (search npm for current package name)

```bash
npm install -g mcp-server-supabase
```

**Config file:** `<project>/.opencode/opencode.json`

```json
{
  "mcp": {
    "supabase": {
      "type": "local",
      "command": ["mcp-server-supabase"],
      "environment": {
        "SUPABASE_URL": "<your-project-url>",
        "SUPABASE_ANON_KEY": "<your-anon-key>"
      }
    }
  }
}
```

**Purpose:**
- Database operations
- Schema migrations
- Data queries

**Tool chain:**
| Tool | Purpose |
|------|---------|
| `supabase_apply_migration` | Create/modify tables |
| `supabase_execute_sql` | Execute SQL queries |
| `supabase_list_tables` | List tables |
| `supabase_get_advisors` | Security recommendations |

**⚠️ Running constraint:** Must start OpenCode in project root directory.

---

## Complete Configuration Example

### Global Config (~/.config/opencode/opencode.json)

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "playwright": {
      "type": "local",
      "command": ["playwright-mcp-server"]
    },
    "context7": {
      "type": "local",
      "command": ["context7-mcp"],
      "environment": {
        "CONTEXT7_API_KEY": "<your-api-key>"
      }
    }
  }
}
```

### Project Config (<project>/.opencode/opencode.json)

```json
{
  "mcp": {
    "supabase": {
      "type": "local",
      "command": ["mcp-server-supabase"],
      "environment": {
        "SUPABASE_URL": "https://xxx.supabase.co",
        "SUPABASE_ANON_KEY": "eyJ..."
      }
    }
  }
}
```

---

## Running Constraints

### ⚠️ Must run in project root directory

```bash
cd /path/to/project
opencode run -m <model> -- "task"
```

OpenCode looks for `.opencode/opencode.json` from current working directory.

---

## Adding New MCP

1. Search npm for MCP server package
2. Verify package: `npm view <package>`
3. Install globally: `npm install -g <package>`
4. Add to config file with binary name
5. Set required environment variables
6. Restart OpenCode or start new session

---

## Troubleshooting

### MCP not loading

**Check:**
1. Config file path correct?
2. JSON format valid?
3. Environment variables set?
4. Running in project root?
5. MCP binary installed globally?

### Debug MCP

```bash
opencode mcp list
opencode mcp debug <name>
which playwright-mcp-server
```

---

*Configuration Guide v1.4 - 2026-04-05*