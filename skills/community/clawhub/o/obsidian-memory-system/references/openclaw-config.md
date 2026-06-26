# OpenClaw Configuration

## Full Production Config (openclaw.json)

This is the complete configuration for an OpenClaw agent with Obsidian vault memory, Discord workspace, semantic search, dreaming, and full tool access.

```json5
{
  // --- Agent Defaults ---
  "agents": {
    "defaults": {
      "workspace": "/root/clawd",
      "memorySearch": {
        "enabled": true,
        "sources": ["memory"],
        "provider": "openai"       // Requires OPENAI_API_KEY in ~/.openclaw/.env
      },
      "compaction": {
        "mode": "safeguard"        // Preserves context during compaction
      },
      "maxConcurrent": 4,
      "subagents": {
        "maxConcurrent": 8,
        "model": "anthropic/claude-sonnet-4-6",
        "thinking": "low",
        "runTimeoutSeconds": 1200   // 20 min timeout for subagents
      }
    }
  },

  // --- Tool Permissions ---
  "tools": {
    "profile": "full",             // Full tool access
    "exec": {
      "security": "full",          // No sandbox restrictions
      "ask": "off"                 // No confirmation prompts
    },
    "media": {
      "audio": {
        "enabled": true,
        "maxBytes": 26214400,      // 25MB
        "models": [{
          "provider": "openai",
          "model": "gpt-4o-mini-transcribe"
        }]
      }
    }
  },

  // --- Messages & Reactions ---
  "messages": {
    "ackReactionScope": "all"      // React to every message
    // Custom status reactions — see discord-setup.md
  },

  // --- Commands ---
  "commands": {
    "native": "auto",
    "nativeSkills": "auto",
    "restart": true
  },

  // --- Discord Channel ---
  // Full config in references/discord-setup.md
  "channels": {
    "discord": {
      "enabled": true,
      "token": "YOUR_BOT_TOKEN",
      "groupPolicy": "allowlist",
      "dmPolicy": "allowlist",
      "allowFrom": ["YOUR_DISCORD_USER_ID"],
      "guilds": {
        "YOUR_GUILD_ID": {
          "requireMention": false,
          "users": ["YOUR_DISCORD_USER_ID"]
        }
      },
      "streaming": "partial",
      "replyToMode": "first",
      "historyLimit": 30,
      "threadBindings": {
        "enabled": true,
        "spawnSubagentSessions": true,
        "spawnAcpSessions": true
      },
      "ackReaction": "🦅",
      "autoPresence": {
        "enabled": true,
        "healthyText": "Online",
        "degradedText": "Recovering...",
        "exhaustedText": "Token budget hit — {reason}"
      }
    }
  },

  // --- Gateway ---
  "gateway": {
    "port": 18789,
    "mode": "local",
    "bind": "loopback",
    "auth": {
      "mode": "token",
      "token": "GENERATE_A_RANDOM_TOKEN"
    }
  },

  // --- Plugins ---
  "plugins": {
    "entries": {
      "memory-core": {
        "config": {
          "dreaming": {
            "enabled": true,
            "frequency": "0 8 * * *"   // Adjust for your timezone
          }
        }
      }
    }
  },

  // --- Session ---
  "session": {
    "threadBindings": {
      "enabled": true
    }
  }
}
```

## Environment Variables (~/.openclaw/.env)

```bash
OPENAI_API_KEY=sk-...          # Required for memory search embeddings + audio transcription
GEMINI_API_KEY=AIzaSy...       # Optional: for image/video/music generation
```

## Project Context Auto-Loading

OpenClaw automatically discovers and loads these files from the workspace root:

| File | Purpose | Loaded When |
|------|---------|-------------|
| `SOUL.md` | Agent personality | Every session |
| `USER.md` | Human context | Every session |
| `AGENTS.md` | Workflow rules | Every session |
| `TOOLS.md` | Infrastructure | Every session |
| `MEMORY.md` | Long-term memory | Every session (main/DM only) |
| `IDENTITY.md` | Extended character | Every session |
| `HEARTBEAT.md` | Periodic tasks | On heartbeat polls |
| `BOOTSTRAP.md` | First-run setup | First session only |

## Memory Search

`memory_search` indexes `MEMORY.md` and `memory/*.md` from the workspace root.

**⚠️ Symlink limitation:** The indexer skips symlinks (both directory and file level). If `memory/` is a symlink to `vault/10-journal/`, indexing finds 0 files.

**Fix:** Use real file copies with a sync script. See `references/discord-setup.md` → Memory Integration section.

## Dreaming (Memory Promotion)

Dreaming automatically promotes frequently-recalled information to MEMORY.md:

1. Enable in config (see `plugins.entries.memory-core.config.dreaming`)
2. The recall store (`memory/.dreams/short-term-recall.json`) populates from `memory_search` usage
3. After enough recalls (default: 3+ recalls, 3+ unique queries), Deep phase promotes to MEMORY.md
4. First meaningful dreaming happens after a few days of normal search usage

## Key Settings Explained

| Setting | Purpose |
|---------|---------|
| `compaction.mode: "safeguard"` | Preserves conversation context during token limit management |
| `tools.profile: "full"` | Agent has access to all available tools |
| `exec.security: "full"` | Commands run without sandboxing |
| `exec.ask: "off"` | Agent doesn't ask before executing commands |
| `subagents.model` | Model used for delegated work (cheaper than orchestrator) |
| `subagents.runTimeoutSeconds` | Max time for a subagent task |
| `ackReactionScope: "all"` | Visual confirmation on every incoming message |
| `streaming: "partial"` | See responses as they generate |
| `dreaming.frequency` | Cron schedule for memory consolidation sweeps |

## Apply Config

After editing `~/.openclaw/openclaw.json`:

```bash
# Restart gateway to pick up changes
openclaw gateway restart

# Or send SIGUSR1 for graceful reload
kill -USR1 $(pgrep -f openclaw-gateway)
```
