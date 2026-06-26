---
name: phone-call-agent
description: "AI voice call agent — make outbound calls, generate browser call links, accept inbound calls, and retrieve full transcripts + summaries when calls end. Supports Chinese and English. Self-hosted with Docker."
license: MIT-0
metadata:
  github: https://github.com/Littlesheepxy/phone-call-agent
compatibility:
  - claude-3-5-sonnet
  - claude-3-opus
argument-hint: "make a call to +8613800138000 to follow up on Q1 contract"
---

# Phone Call Agent

An open-source, self-hosted AI voice call agent. Give it a phone number and a task — it calls the person, has a natural conversation, and returns the full transcript and outcome back to you.

Works in two modes:
- **Outbound** — agent dials a real phone number via SIP, or generates a browser call link
- **Inbound** — agent answers incoming calls from your SIP trunk

---

## Quick Start

```bash
git clone https://github.com/Littlesheepxy/phone-call-agent
cd phone-call-agent
cp .env.example .env
# Fill in .env with your API keys (see Configuration below)
docker compose up
```

Services started:
| Service | URL | Purpose |
|---------|-----|---------|
| Backend API | http://localhost:8001 | FastAPI + MCP server |
| Web UI | http://localhost:3000 | Dashboard + share-link landing page |
| LiveKit | ws://localhost:7880 | WebRTC media server |

### Public URL (needed for share links to work on other devices)

```bash
# No account needed — temporary URL, good for testing:
docker compose --profile quick-tunnel up quick-tunnel

# Permanent URL (free Cloudflare account):
# Set CLOUDFLARE_TOKEN= in .env, then:
docker compose --profile tunnel up tunnel
```

---

## Configuration (.env)

```env
# LiveKit (included in docker compose — defaults work out of the box)
LIVEKIT_URL=ws://localhost:7880
LIVEKIT_API_KEY=devkey
LIVEKIT_API_SECRET=secret

# LLM — pick one
LLM_PROVIDER=openai
LLM_API_KEY=sk-...
LLM_MODEL=gpt-4o-mini

# STT (speech-to-text)
ASR_PROVIDER=openai_whisper   # or: volcengine (lower latency for Chinese)

# TTS (text-to-speech)
TTS_PROVIDER=openai           # or: volcengine
TTS_VOICE=alloy

# Volcengine / Doubao (recommended for Chinese — lower latency, better quality)
VOLCENGINE_LLM_API_KEY=...
VOLCENGINE_LLM_MODEL=doubao-pro-32k-241215
VOLCENGINE_ASR_APP_ID=...
VOLCENGINE_ASR_TOKEN=...
VOLCENGINE_TTS_APP_ID=...
VOLCENGINE_TTS_TOKEN=...

# SIP trunk (only needed for real outbound phone calls)
SIP_OUTBOUND_TRUNK_ID=...     # LiveKit SIP trunk ID

# Optional: called with transcript + summary JSON when each call ends
WEBHOOK_URL=https://your-app.com/call-webhook

# Public base URL for share links (set to your tunnel/domain)
PUBLIC_URL=https://your-tunnel.trycloudflare.com
```

---

## How Share Links Work

The core workflow: **Claude generates a browser call link → sends it to anyone → they click and talk to the AI → Claude gets the transcript back.**

```
Claude (via MCP)
  │
  ├── create_share_link("follow_up", mode="outbound")
  │     └── returns: https://abc123.trycloudflare.com/call/web-xxx?token=...
  │
  │   [you send this URL to the person you want to call]
  │
  ├── Person opens link in any browser (phone, laptop — no app needed)
  │     └── WebRTC audio call starts instantly
  │
  └── get_call_result(room_name, wait_seconds=300)
        └── returns transcript + summary the moment they hang up
```

### Step 1 — Start the tunnel so the link works for others

By default the link points to `localhost` — only works on your machine. To make it work for anyone:

```bash
# Option A: No account needed (temporary URL, good for demos)
docker compose --profile quick-tunnel up quick-tunnel
# Prints something like: https://abc123.trycloudflare.com

# Option B: Permanent URL (free Cloudflare account)
# 1. Get a tunnel token at dash.cloudflare.com → Zero Trust → Tunnels
# 2. Add to .env:  CLOUDFLARE_TOKEN=your-token-here
# 3. Run:
docker compose --profile tunnel up tunnel
```

### Step 2 — Set PUBLIC_URL in .env

```env
PUBLIC_URL=https://abc123.trycloudflare.com
```

Restart the backend so it uses the new URL:
```bash
docker compose restart agent
```

### Step 3 — Ask Claude to make a call

```
You: "帮我跟进一下张三的Q1合同签署"

Claude:
  → create_share_link("follow_up", mode="outbound")
  → "请点击此链接，AI 会主动跟进合同事宜：https://abc123.trycloudflare.com/call/web-xxx?token=..."
  → [waits for the call to end]
  → "张三确认将于本周五提交合同。"
```

The person receiving the link just opens it in a browser — no app, no phone number, no account needed.

---

## MCP Server Setup

After `docker compose up`, connect the MCP server to Claude Desktop:

**`~/Library/Application Support/Claude/claude_desktop_config.json`** (macOS):
```json
{
  "mcpServers": {
    "phone-call-agent": {
      "command": "python",
      "args": ["-m", "backend.mcp_server"],
      "cwd": "/path/to/phone-call-agent",
      "env": {
        "AGENT_API_URL": "http://localhost:8001"
      }
    }
  }
}
```

Install the MCP dependency first:
```bash
cd phone-call-agent && pip install mcp>=1.0.0
```

---

## MCP Tools

Once connected, Claude has access to these tools:

### `list_skills`
List all available call skills (loaded from `skills/*.md`).

```
→ follow_up: 跟进待处理事项 (outbound)
→ appointment_reminder: 提醒联系人即将到来的预约 (outbound)
→ customer_survey: 服务后进行简短满意度调查 (outbound)
```

### `create_share_link(skill_id, mode?)`
Generate a browser-based call URL — no phone number needed.
- `mode: "outbound"` → AI speaks first (agent initiates the conversation)
- `mode: "inbound"` → user speaks first (agent waits and responds)
- Default: use the skill's own mode setting

Returns `share_url`, `room_name`, `mode`, `expires_in`.

### `make_voice_call(to, skill_id, context)`
Dial a real phone number via SIP. Requires `SIP_OUTBOUND_TRUNK_ID` in `.env`.
- `to`: E.164 phone number e.g. `"+8613800138000"`
- `context`: fills `{{variable}}` placeholders in the skill's system prompt

### `get_call_result(room_name, wait_seconds?)`
Retrieve the transcript and summary of a completed call.
- `wait_seconds`: long-poll up to 300 seconds — returns the moment the call ends
- Returns: `transcript[]`, `summary.outcome`, `summary.summary`, `summary.sentiment`

### `get_skill(skill_id)`
Get a skill's details including context variables.

### `check_pending_inbound` / `accept_inbound_call(room_name, skill_id)`
Handle incoming SIP calls — list pending calls and accept them with a chosen skill.

---

## Skills

Skills are Markdown files in `skills/` — YAML frontmatter + LLM system prompt:

```markdown
---
name: my_skill
description: 简短描述
language: zh          # zh | en | auto
mode: outbound        # outbound | inbound | both
max_duration: 300
context_variables:
  - contact_name
  - topic
---
你是 Relay，一个 AI 助理。联系人：{{contact_name}}。话题：{{topic}}。
```

No code changes needed. Add a file → restart → immediately available via MCP.

---

## Typical Agent Workflow

```
User: "帮我跟进一下张三的Q1合同签署"

Claude:
  1. list_skills() → 找到 follow_up
  2. create_share_link("follow_up", mode="outbound")
     → share_url: https://your-tunnel.../call/web-xxx?token=...
  3. 把链接发给用户：
     "请点击此链接，AI 会主动跟进您的合同事宜：[链接]"
  4. get_call_result(room_name, wait_seconds=300)
     → 通话结束后立即返回
  5. 总结并回复：
     "张三确认将于本周五提交合同。通话时长 2 分 18 秒。"
```

---

## Architecture

```
User prompt
    │
    ▼
Claude (MCP client)
    │  tools: create_share_link / get_call_result
    ▼
phone-call-agent backend (FastAPI :8001)
    │
    ├── LiveKit room (WebRTC)
    │       ├── AI agent (Pipecat pipeline)
    │       │       ├── VAD (Silero)
    │       │       ├── STT (Whisper / Volcengine)
    │       │       ├── LLM (GPT-4o / Doubao)
    │       │       └── TTS (OpenAI / Volcengine)
    │       └── User (browser via share link, or SIP phone)
    │
    └── Results stored → GET /calls/{room}/result
```

---

## Supported Providers

| Component | Options |
|-----------|---------|
| LLM | OpenAI (gpt-4o, gpt-4o-mini), Volcengine Doubao, any OpenAI-compatible |
| STT | OpenAI Whisper, Volcengine ASR (recommended for Chinese) |
| TTS | OpenAI TTS, Volcengine TTS (recommended for Chinese) |
| Phone | Any LiveKit SIP trunk provider |
| WebRTC | LiveKit (self-hosted, included in docker compose) |
