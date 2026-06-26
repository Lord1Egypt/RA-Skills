# OpenClaw Dashboard Guide

Your dashboard has two modes. Start with Simple. Graduate to Advanced when you're ready.

---

# 🟢 SIMPLE MODE — "I Just Want It To Work"

You need exactly 4 pages. Ignore everything else.

## Page 1: Chat (left sidebar → Chat)
**This is home.** Type messages, get responses. That's it.
- Bottom bar: type your message, hit Enter to send
- "New session" button (bottom right): starts a fresh conversation
- "Queue" button: sends message even if agent is busy (it'll read it next)
- **Paste or drag images** into the chat box to share them with your agent
- "Stop" button: appears when agent is thinking — cancels current response
- Top right dropdown (`agent:main:main`): leave this alone unless you have multiple agents

## Page 2: Agents (left sidebar → Agent → Agents)
**This is where your agent lives.**
- Click your agent name (probably "main")
- **Overview tab**: See your agent's name, model, and emoji
- **Model Selection**: Change which AI model your agent uses (dropdown)
- Click **Save** after changes, then **Reload Config**

**First time setup:**
1. Click your agent
2. Check that "Identity Name" shows your agent's name from IDENTITY.md
3. Make sure "Primary Model" is set to what you want (e.g., Claude Sonnet 4.5)
4. That's it

## Page 3: Cron Jobs (left sidebar → Control → Cron Jobs)
**Reminders and scheduled tasks.**
- **Scheduler box**: Shows if cron is enabled and how many jobs exist
- **New Job form** (right side): Create reminders
  - Name: what to call it
  - Schedule: "Every" for recurring, pick a time
  - Agent message: what the reminder says
  - Click **Add job**
- **Jobs list** (bottom): All your scheduled tasks. Each has enable/disable/delete

**Quick reminder recipe:**
1. Name: "Morning check-in"
2. Schedule: Every → 30 → Minutes
3. Session: Main
4. Payload: System event
5. Message: "Check email and calendar"
6. Click Add job → done

## Page 4: Usage (left sidebar → Control → Usage)
**Watch your money.**
- Click **Refresh** to load data
- Toggle between **Tokens** and **Cost** views
- Use **Today / 7d / 30d** buttons to change time range
- "Activity by Time" shows when you're burning tokens
- "Daily Usage" shows spend per day

**Check this weekly.** If costs are climbing, you're probably using a more expensive model than you need.

---

## Simple Mode — That's It! 🎉

4 pages. Chat, Agents, Cron Jobs, Usage. Everything else is optional.

Your agent handles the rest through conversation:
- "Set a reminder for tomorrow at 9am" → agent uses cron
- "What model are you using?" → agent tells you
- "Switch to a cheaper model" → agent can do this
- "How much have I spent today?" → agent checks

**You don't need the other pages until you want them.**

---

# 🔵 ADVANCED MODE — "Show Me Everything"

When you're comfortable with Simple Mode and want more control.

## Control Section

### Overview
Gateway health dashboard. Shows:
- **Gateway Access**: WebSocket URL, token (for remote connections)
- **Snapshot**: Connection status, uptime, last channel refresh
- **Instances/Sessions/Cron**: Quick counts
- **Notes**: Tips for Tailscale serve, session hygiene, cron reminders

*When to use:* Troubleshooting connection issues or checking if everything's running.

### Channels
Connect messaging platforms:
- **WhatsApp**: Show QR code → scan with phone → linked
- **Discord**: Configure bot token, manage guild/channel permissions
- **Telegram**: Add bot token, set allowed users
- **Signal/iMessage/Slack**: Additional platforms if configured

Each channel shows: Configured / Linked / Running / Connected status.

*When to use:* Setting up or troubleshooting messaging connections.

### Instances
Shows all connected clients sending presence beacons. Displays:
- Instance name and tags (OS, architecture)
- Last activity time
- Connection reason

*When to use:* Checking if your gateway is reachable from other devices.

### Sessions
All active conversation sessions with:
- Session key and label
- Kind (direct/group)
- Token count (current / max)
- Per-session overrides for: Thinking, Verbose, Reasoning
- Delete button for cleanup

*When to use:* Managing token usage per conversation, cleaning up old sessions, or setting per-session model overrides.

## Agent Section

### Agents (expanded)
Beyond the Overview tab from Simple Mode:
- **Files tab**: View workspace files
- **Tools tab**: See available tools and their status
- **Skills tab**: Agent-specific skill configuration
- **Channels tab**: Per-agent channel routing
- **Cron Jobs tab**: Agent-specific scheduled tasks

### Skills
All installed skills (workspace + built-in):
- **Workspace Skills**: Skills you've installed in your workspace
- **Built-in Skills**: Bundled with OpenClaw (weather, ClawHub, etc.)
- Search/filter to find specific skills
- Click to expand and configure (API keys, enable/disable)

*When to use:* Installing new capabilities or configuring skill-specific API keys.

### Nodes
Device pairing and command execution control:
- **Exec Approvals**: Security settings for command execution
  - Target: Gateway vs Host
  - Security Mode: Deny / Allow
  - Ask Mode: On miss / Always
  - Ask Fallback: What to do when UI can't prompt
- **Exec Node Binding**: Pin agents to specific nodes
- **Devices**: Paired devices, tokens, rotate/revoke
- **Nodes**: Live paired devices

*When to use:* Pairing your phone, controlling what commands the agent can run, or managing device access.

## Settings Section

### Config
The full configuration editor. Two views:
- **Form view**: Visual editor with dropdowns and toggles
- **Raw view**: Direct JSON5 editing

**Top bar buttons:**
- **Reload**: Refresh config from disk (undo unsaved changes)
- **Save**: Write changes to disk (saved but NOT active yet)
- **Apply**: Save AND restart — this is how changes take effect
- **Update**: Check for OpenClaw updates

**The settings sidebar has 14+ categories.** Here's every single one explained in plain English, with honest advice on what to touch:

---

#### ✅ Environment — "Your API keychain"
Where you put API keys and environment variables. **This is likely the first thing you configure.**

What to do: Add your `ANTHROPIC_API_KEY` (or whichever AI provider you use). Leave everything else alone.

What to skip: Shell environment passthrough, custom env file paths.

---

#### 🟡 Updates — "Auto-update settings"
Controls how OpenClaw updates itself. Like auto-update on your phone.

What to do: Leave on "stable." Only switch to "beta" or "dev" if you like living dangerously.

---

#### ✅ Agents — "The brain settings"
The most important settings page. Controls which AI your agent uses and how it behaves.

**Key things to look for:**
- **Primary model** — which AI model (e.g., Claude Sonnet 4.5)
- **Fallbacks** — backup models if primary fails
- **Heartbeat** — how often your agent checks in (30 minutes is good)
- **Thinking default** — how deeply the agent thinks (low is fine for most things)
- **Timeout** — how long before giving up on a response

What to do: Make sure your model is set. Set heartbeat to 30m. Leave the rest.

What to skip: Multi-agent configs, sandbox settings, advanced model overrides.

---

#### 🟡 Authentication — "Login credentials for AI services"
How your agent authenticates with AI providers. Usually already set up by the wizard.

What to do: Nothing, unless you're adding a second AI provider.

What to skip: OAuth internals, priority ordering, API modes.

---

#### ✅ Channels — "Messaging platform connections"
Connect WhatsApp, Discord, Telegram, Slack, Signal, etc. Each platform has its own section with on/off, credentials, and who's allowed to message.

What to do: Configure whichever platform you use. The dashboard Channels page (separate from Config) is usually easier for this.

What to skip: Network/proxy settings, retry policies, webhook configs.

---

#### 🟡 Messages — "How responses look"
Controls response formatting — prefixes, acknowledgment reactions, typing indicators, message chunking.

What to do: Leave defaults. Come back if you want a custom ack emoji (the 👀 that appears when your agent starts thinking).

---

#### 🟡 Commands — "Slash command settings"
Controls which `/commands` work and who can use them.

What to do: Leave defaults (they're safe). Consider enabling `/config` if you want to change settings from chat.

⚠️ **Don't enable `/bash`** unless you understand it lets your agent run ANY command on the server.

---

#### 🔴 Hooks — "Email & webhook integrations"
Lets external services (like Gmail) trigger your agent. Advanced feature.

What to do: Skip entirely for now. Come back when you want email notifications.

---

#### 🟡 Skills — "Plugin management"
Controls how skills (add-on capabilities) load and where they live.

What to do: Leave defaults. Use the Skills page in the dashboard to manage skills visually instead.

---

#### ✅ Tools — "Security & permissions"
Controls what your agent can DO — run commands, browse the web, access files.

**Key things to look for:**
- **Exec settings** — command execution sandbox mode
- **Elevated permissions** — who can run privileged commands
- **Web/search settings** — add Brave Search API key here for web search

What to do: Review security settings so you know what's allowed. Add search API key if you want web search.

⚠️ **Be careful** with elevated permissions. Don't open these up without understanding what they allow.

---

#### 🟡 Gateway — "The engine room"
Server settings — port, authentication, networking. Usually already configured by the setup wizard.

What to do: Leave alone unless you need remote access or Tailscale integration.

**Never change** `bind` or `auth.mode` unless you understand network security.

---

#### 🔴 Setup Wizard — "Internal bookkeeping"
Records what setup steps you've completed. **Never edit manually.**

---

#### 🔴 Meta — "Configuration metadata"
Internal metadata fields. No user-facing impact. **Skip.**

---

#### 🔴 Diagnostics — "Developer mode"
Debug flags, cache tracing, OpenTelemetry. Only useful if something is broken and you're getting help on Discord.

What to do: Never touch this unless someone helping you asks you to enable something specific.

---

**Summary: You need 3 categories (Environment, Agents, Channels). Tools is worth reviewing for security. Everything else can wait.**

### Debug
For troubleshooting only:
- **Snapshots**: Raw gateway state JSON (status, health, heartbeat data)
- **Manual RPC**: Send raw gateway method calls (e.g., `system-presence`)
- Health shows all channel states, uptime, errors

*When to use:* Something's broken and you need to see what the gateway sees.

### Logs
System log viewer. Shows gateway events, errors, and activity.

*When to use:* Diagnosing errors or checking what happened.

## Resources Section

### Docs
Link to OpenClaw documentation. Opens in browser.

---

# 🎯 Setup Order (First Time)

**Day 1 — Get talking:**
1. **Config → Environment**: Add your API key (e.g., `ANTHROPIC_API_KEY`)
2. **Agents**: Verify model is set correctly
3. **Chat**: Say hello. It works.

**Day 2 — Get connected:**
4. **Channels**: Connect Discord/WhatsApp/Telegram (whichever you use)
5. **Config → Tools**: Review security settings

**Day 3 — Get proactive:**
6. **Cron Jobs**: Set up your first heartbeat (every 30-60 min)
7. **Usage**: Check your first day's spend

**Week 2 — Get comfortable:**
8. Explore Agents → Skills, Tools tabs
9. Try Config → Messages for custom formatting
10. Set up additional channels

**When ready — Go advanced:**
11. Nodes for device pairing
12. Hooks for email/webhook integration
13. Debug for troubleshooting

---

# ⌨️ Useful Shortcuts (in Chat)

These work in the chat message box:

### Everyday Commands
| Command | What It Does |
|---------|-------------|
| `/help` | Show all available commands |
| `/new` or `/reset` | Start fresh session (clears conversation) |
| `/stop` | Cancel current agent response |
| `/status` | Show current session info |
| `/model <alias>` | Switch AI model (e.g., `/model opus`) |
| `/model list` | Show all available models with numbers to pick |
| `/compact` | Compress conversation history (saves tokens = saves money) |
| `/usage cost` | Show how much you've spent this session |
| `/context` | Show what files/tools are loaded and how much space they use |

### Thinking & Output
| Command | What It Does |
|---------|-------------|
| `/think <level>` | Set thinking depth: off, low, medium, high (deeper = smarter but slower) |
| `/reasoning` | Toggle reasoning visibility on/off |
| `/verbose` | Toggle verbose output |

### Background Tasks
| Command | What It Does |
|---------|-------------|
| `/subagents list` | Show all background tasks |
| `/subagents stop <id>` | Stop a specific background task |
| `/subagents log <id>` | View what a background task did |

### Advanced (skip these until you need them)
| Command | What It Does |
|---------|-------------|
| `/elevated` | Toggle elevated permissions |
| `/send on\|off` | Toggle outbound messaging |
| `/activation mention\|always` | Group chat: respond to mentions only, or everything |
| `/skill <name>` | Run a specific skill |

---

*Start simple. Add complexity only when you need it. The UI has everything — you don't have to use everything.*
