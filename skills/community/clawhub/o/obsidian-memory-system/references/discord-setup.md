# Discord Workspace Setup

Complete guide to setting up a Discord server as your OpenClaw workspace. Discord replaces WhatsApp as the primary communication channel with significant upgrades: streaming responses, voice channels, interactive components, thread-bound coding sessions, per-project channel isolation, custom emoji status reactions, and animated server identity.

## Why Discord Over WhatsApp

| Feature | WhatsApp | Discord |
|---------|----------|---------|
| Streaming responses | ❌ | ✅ See text as it generates |
| Voice conversations | ❌ | ✅ Real-time STT → LLM → TTS |
| Interactive buttons | ❌ | ✅ Approve/reject, dropdowns, forms |
| Channel separation | ❌ One chat | ✅ Per-project channels |
| Thread-bound coding | ❌ | ✅ Codex/Claude Code in threads |
| Reactions | ❌ | ✅ Custom emoji ack + status reactions |
| Message search | Basic | ✅ Full-text across channels |
| Polls | ❌ | ✅ Native polls |
| Pins | ❌ | ✅ Pin important messages |
| File size limit | 16MB | 25MB (50MB with boost/Nitro) |
| Custom emoji | ❌ | ✅ Agent-themed emoji for personality |
| Stickers | ❌ | ✅ Animated APNG stickers for rituals |
| Auto-presence | ❌ | ✅ Bot status shows health state |
| Components v2 | ❌ | ✅ Rich UI containers, galleries |

## Server Architecture

### Recommended Channel Layout

```
🏠 Home
  #general          — Casual chat, quick questions (daily driver)
  #tasks            — Task tracking, reminders, todos
  #coding           — General coding, debugging, code review

🔊 Voice
  🎙 General        — Voice conversations with the agent

🏥 [Your Org]       — Organization-specific channels
  #project-a        — Project A work
  #project-b        — Project B work
  #project-c        — Project C work

🤖 Agents
  #agents           — Subagent/ACP coding sessions (threads spawn here)

📋 Ops
  #logs             — Deployment logs, alerts
  #cron             — Cron job output, scheduled tasks

🧪 Research
  #research         — Deep research, analysis tasks
```

**Key principle:** Each channel = isolated session with its own context. When you ask about Project A in #project-a, the agent doesn't waste tokens loading Project B context.

### Channel Topics as Context Pointers

Set channel topics to include vault pointers so the agent knows where to find project docs:

```
Project A digital signage | vault: 20-projects/project-a/ | repo: user/project-a | admin: port 3001
```

This gives the agent routing context without loading full project docs every message.

## OpenClaw Discord Configuration

### Minimum Config (gets you working)

```json5
{
  "channels": {
    "discord": {
      "enabled": true,
      "token": "YOUR_BOT_TOKEN",
      "dmPolicy": "allowlist",
      "allowFrom": ["YOUR_DISCORD_USER_ID"],
      "groupPolicy": "allowlist",
      "guilds": {
        "YOUR_GUILD_ID": {
          "requireMention": false,
          "users": ["YOUR_DISCORD_USER_ID"]
        }
      }
    }
  },
  "tools": {
    "profile": "full",
    "exec": {
      "security": "full",
      "ask": "off"
    }
  }
}
```

**⚠️ Common mistake:** Without the `guilds` block, the bot only responds to DMs. Guild channels need explicit allowlisting. This is the #1 reason bots don't respond in servers.

### Full Production Config

```json5
{
  "channels": {
    "discord": {
      "enabled": true,
      "token": "YOUR_BOT_TOKEN",

      // --- Access Control ---
      "groupPolicy": "allowlist",
      "dmPolicy": "allowlist",
      "allowFrom": ["YOUR_DISCORD_USER_ID"],
      "guilds": {
        "YOUR_GUILD_ID": {
          "requireMention": false,
          "users": ["YOUR_DISCORD_USER_ID"]
        }
      },

      // --- Response Behavior ---
      "streaming": "partial",        // See responses as they generate
      "replyToMode": "first",        // Agent replies to your message
      "historyLimit": 30,            // Messages loaded for context

      // --- Thread Bindings (for subagents/ACP) ---
      "threadBindings": {
        "enabled": true,
        "spawnSubagentSessions": true,
        "spawnAcpSessions": true
      },

      // --- Visual Acknowledgment ---
      // Simple emoji:
      "ackReaction": "🦅",
      // Or custom animated emoji (upload to server first):
      // "ackReaction": "your_emoji_name:EMOJI_ID",

      // --- Status Reactions (per-phase custom emoji) ---
      // These show what the agent is doing in real-time via reactions.
      // Upload custom emoji to your server, then reference by name:id.
      // "statusReactions": {
      //   "emojis": {
      //     "thinking": "a_scroll:EMOJI_ID",
      //     "tool": "a_torch:EMOJI_ID",
      //     "coding": "a_coding:EMOJI_ID",
      //     "web": "a_spider:EMOJI_ID",
      //     "done": "dcc_yes:EMOJI_ID",
      //     "error": "a_skull:EMOJI_ID",
      //     "stallSoft": "a_hourglass:EMOJI_ID",
      //     "stallHard": "a_bomb:EMOJI_ID",
      //     "compacting": "a_cauldron:EMOJI_ID"
      //   }
      // },

      // --- Auto Presence (bot status) ---
      "autoPresence": {
        "enabled": true,
        "healthyText": "Watching the crawl",
        "degradedText": "Recovering...",
        "exhaustedText": "Token budget hit — {reason}"
      },

      // --- UI Customization ---
      "ui": {
        "components": {
          "accentColor": "#1a1a2e"   // Dark theme accent for components v2
        }
      },

      // --- Voice (STT → LLM → TTS) ---
      "voice": {
        "enabled": false,            // Set true when upstream bugs are fixed
        "tts": {
          "provider": "openai",
          "providers": {
            "openai": {
              "voice": "onyx"        // Options: alloy, echo, fable, onyx, nova, shimmer
            }
          }
        },
        "autoJoin": [],              // Channel IDs to auto-join on startup
        "daveEncryption": false      // Keep false — DAVE E2EE breaks receive in current versions
      }
    }
  },

  // --- Tool permissions ---
  "tools": {
    "profile": "full",
    "exec": {
      "security": "full",
      "ask": "off"
    }
  },

  // --- Reaction scope ---
  "messages": {
    "ackReactionScope": "all"        // React to all messages, not just first
  },

  // --- Commands ---
  "commands": {
    "native": "auto",
    "nativeSkills": "auto",
    "restart": true
  },

  // --- Session thread bindings (top-level) ---
  "session": {
    "threadBindings": {
      "enabled": true
    }
  }
}
```

### Config Reference

| Setting | Value | Purpose |
|---------|-------|---------|
| `streaming: "partial"` | Progressive output | See responses as they generate |
| `replyToMode: "first"` | Reply threading | Agent replies to your message, not channel |
| `requireMention: false` | No @mention needed | Just type naturally in guild channels |
| `historyLimit: 30` | Context window | Messages loaded for context per channel |
| `threadBindings.enabled` | Thread isolation | Subagents get their own Discord threads |
| `spawnSubagentSessions` | Auto-thread coding | Codex/Claude Code spawn in threads |
| `spawnAcpSessions` | ACP thread binding | ACP harness sessions get threads |
| `ackReaction` | Visual confirmation | Emoji reacted on message receipt |
| `ackReactionScope: "all"` | Scope | React to every message (vs just first) |
| `autoPresence.enabled` | Bot status | Shows health in member list sidebar |
| `voice.daveEncryption` | Keep false | DAVE E2EE breaks voice receive (known bug) |
| `tools.profile: "full"` | Full tool access | Agent can use all tools without asking |
| `exec.security: "full"` | No sandbox | Agent executes commands directly |
| `exec.ask: "off"` | No confirmation | Agent doesn't ask before running commands |

## Custom Emoji & Status Reactions

### Why Custom Emoji?

Instead of generic ✅❌⏳ reactions, custom emoji give your agent personality. When the agent is thinking, searching, coding, or done — you see themed animated reactions that tell you exactly what phase it's in.

### Status Reaction Phases

| Phase | Emoji | When |
|-------|-------|------|
| `thinking` | 📜 scroll animation | LLM is generating a response |
| `tool` | 🔥 torch animation | Executing a tool call |
| `coding` | 💻 coding animation | Running code/exec |
| `web` | 🕷 spider animation | Web search/fetch |
| `done` | ✅ checkmark | Response complete |
| `error` | 💀 skull animation | Error occurred |
| `stallSoft` | ⏳ hourglass animation | Soft stall (taking a while) |
| `stallHard` | 💣 bomb animation | Hard stall (very slow) |
| `compacting` | 🧪 cauldron animation | Context compaction running |

### Setting Up Custom Emoji

1. **Create/generate your emoji** — Use AI image generation, pixel art tools, or commission them. Animated GIF emoji: max 256KB, any square size (Discord resizes). Static: PNG, max 256KB.

2. **Upload to your server** — Server Settings → Emoji → Upload. Name them consistently (e.g., `a_scroll`, `a_torch`, `dcc_yes` — `a_` prefix is common for animated).

3. **Get emoji IDs** — Use the `emoji-list` action:
```json
{ "action": "emoji-list", "channel": "discord", "guildId": "YOUR_GUILD_ID" }
```

4. **Add to config** — Format: `emoji_name:emoji_id`
```json5
"statusReactions": {
  "emojis": {
    "thinking": "a_scroll:1234567890",
    "tool": "a_torch:1234567891",
    "done": "checkmark:1234567892"
  }
}
```

### Stickers for Rituals

Discord stickers (animated APNG, max 512KB, 320×320) are great for daily rituals:
- **Good morning sticker** → Agent reads yesterday's journal and gives a morning briefing
- **Goodnight sticker** → Agent wraps up, updates memory, ends session

Define sticker conventions in `SOUL.md` so the agent recognizes them:
```markdown
### Sticker Conventions
- **wakeup_sticker** = Good morning. Read notes, give briefing.
- **sleep_sticker** = Goodnight. Wrap up, update memory.
```

Note: OpenClaw receives stickers as `<media:sticker>` with the image attached but **no sticker name/ID metadata**. The agent must identify stickers by visual content.

## Interactive Components

### Buttons
```json5
{
  "components": {
    "reusable": true,
    "blocks": [{
      "type": "actions",
      "buttons": [
        { "label": "✅ Approve", "style": "success" },
        { "label": "❌ Reject", "style": "danger" },
        { "label": "📋 Details", "style": "secondary" }
      ]
    }]
  }
}
```

### Select Menus
```json5
{
  "type": "actions",
  "select": {
    "type": "string",
    "placeholder": "Pick a project...",
    "options": [
      { "label": "Project A", "value": "a" },
      { "label": "Project B", "value": "b" }
    ]
  }
}
```

### Forms (Modal Dialogs)
```json5
{
  "components": {
    "modal": {
      "title": "Bug Report",
      "triggerLabel": "Report Bug",
      "fields": [
        { "type": "text", "label": "Summary", "style": "short", "required": true },
        { "type": "text", "label": "Steps to Reproduce", "style": "paragraph" }
      ]
    }
  }
}
```

**Important:** Block type must be `actions` (not `buttons`) — this is a common mistake.

## Voice Channels

Real-time voice: your voice → Whisper STT → LLM → OpenAI TTS → your speakers.

**Setup:**
1. Create a voice channel in your server
2. Enable voice in config (see above)
3. Bot needs Connect + Speak permissions
4. Use `/vc join` in the voice channel

**Voice options:** alloy, echo, fable, onyx, nova, shimmer (OpenAI TTS).

**Cost:** ~$0.015 per response for TTS. STT is minimal (Whisper).

**Known issue (as of 2026.4.5):** @discordjs/voice 0.19.x has a DAVE E2EE bug that breaks incoming audio (STT). TTS output works. Keep `daveEncryption: false` and `voice.enabled: false` until upstream ships a fix. Track: GitHub #24825.

## Thread-Bound Coding Sessions

When spawning Codex, Claude Code, or other ACP agents, they get their own Discord thread. Full conversation history preserved, isolated from the main channel.

**Requires:**
- `threadBindings.enabled: true` (both in `channels.discord` and top-level `session`)
- `spawnSubagentSessions: true`
- `spawnAcpSessions: true`

**How it works:** User asks agent to "run Codex on this task" → agent spawns ACP session → Discord thread created automatically → all Codex output appears in the thread → main channel stays clean.

## Memory Integration with Discord

### Memory Sync for Search

OpenClaw's memory indexer (`memorySearch`) indexes `MEMORY.md` and `memory/*.md` from the workspace root. 

**⚠️ Symlink limitation:** The memory indexer uses `lstat` and explicitly skips symlinks. If your `memory/` directory is a symlink to `vault/10-journal/`, indexing will find 0 files. 

**Workaround:** Use a sync script instead of symlinks:

```bash
#!/bin/bash
# scripts/sync-memory.sh
WORKSPACE="/root/clawd"
rsync -a --delete "$WORKSPACE/vault/10-journal/" "$WORKSPACE/memory/"
cp -u "$WORKSPACE/vault/00-brain/MEMORY.md" "$WORKSPACE/MEMORY.md"
rm -rf "$WORKSPACE/memory/.dreams" 2>/dev/null
```

Run via system cron every 30 minutes (matching heartbeat cadence):
```bash
*/30 * * * * /root/clawd/scripts/sync-memory.sh >/dev/null 2>&1
```

### Dreaming (Automatic Memory Promotion)

OpenClaw's Dreaming system automatically promotes important recurring information from short-term recall to `MEMORY.md`. It runs in three phases:

1. **Light Sleep** — Ingests signals from `memory_search` usage
2. **REM Sleep** — Reflects on patterns and themes
3. **Deep Sleep** — Scores candidates and promotes to MEMORY.md

**Enable dreaming:**
```json5
{
  "plugins": {
    "entries": {
      "memory-core": {
        "config": {
          "dreaming": {
            "enabled": true,
            "frequency": "0 8 * * *"  // 3 AM your timezone if server is UTC+5
          }
        }
      }
    }
  }
}
```

With dreaming enabled, the heartbeat no longer needs to manually update MEMORY.md — dreaming handles promotion automatically based on what information is actually recalled and used across sessions.

## Heartbeat with Discord

Configure `HEARTBEAT.md` for Discord-aware periodic maintenance:

```markdown
# HEARTBEAT.md

## Rule: Only act if there was interaction in the last 30 minutes.
Check the conversation history — if there are NO user messages from the last 30 minutes, reply HEARTBEAT_OK immediately.

## If there WAS recent interaction:

### Update Journal
1. **Journal** — Append to `vault/10-journal/YYYY-MM-DD.md`
2. **Project docs** — Update if significant project changes happened
3. **Core files** — Update TOOLS.md if infrastructure changed
4. **Memory promotion is handled by Dreaming** — do NOT manually update MEMORY.md
5. Reply HEARTBEAT_OK when done
```

## Discord Bot Setup (Prerequisites)

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a New Application → name it
3. Go to Bot → create bot, copy token
4. Enable these **Privileged Intents:**
   - ✅ Message Content Intent
   - ✅ Server Members Intent
   - ✅ Presence Intent (for autoPresence)
5. Go to OAuth2 → URL Generator:
   - Scopes: `bot`, `applications.commands`
   - Permissions: Administrator (simplest), or fine-tune:
     - Send Messages, Read Messages, Read Message History
     - Connect, Speak (voice)
     - Manage Threads, Create Public Threads
     - Add Reactions, Use External Emojis, Use External Stickers
     - Attach Files, Embed Links
     - Manage Messages (for edit/delete)
6. Copy the invite URL → open in browser → add to your server
7. Add the bot token to your OpenClaw config

## Migration from WhatsApp

1. Set up Discord server with the channel architecture above
2. Configure OpenClaw with the full production config
3. Update `USER.md` to list Discord as primary channel
4. Update `AGENTS.md` trust anchor with your Discord user ID
5. Keep WhatsApp config as fallback if desired
6. Test: send a message in #general — agent should respond without @mention

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Bot responds in DMs but not guild channels | Missing `guilds` block in config | Add `guilds.GUILD_ID` with user allowlist |
| "This channel is not allowed" | `groupPolicy: "allowlist"` without guild entry | Add your guild ID to `guilds` |
| Bot ignores messages | `requireMention: true` (default) | Set `requireMention: false` in guild config |
| Bot asks permission for everything | Missing `tools.exec` config | Add `tools.profile: "full"`, `exec.security: "full"`, `exec.ask: "off"` |
| Custom emoji reactions fail | Wrong emoji format | Use `name:id` format, get ID from `emoji-list` action |
| Voice: bot joins but can't hear you | DAVE E2EE bug | Set `daveEncryption: false`, wait for upstream fix |
| Memory search returns 0 results | `memory/` is a symlink | Use sync script instead (see Memory Integration section) |
| Stickers not recognized | No metadata sent | Agent must identify by visual content, define conventions in SOUL.md |
