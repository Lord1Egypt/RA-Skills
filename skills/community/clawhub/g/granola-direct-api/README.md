# granola-direct-api

Access your [Granola](https://granola.ai) meeting notes, summaries, transcripts, and
attendee info via the official Granola public REST API.

## What this skill does

- Lists your recent meeting notes with filtering by date
- Retrieves full meeting details: AI summary, attendees, calendar event metadata, folder membership
- Fetches verbatim transcripts with speaker identification and timestamps
- Provides workflow recipes for common tasks (find meetings with a person, get summaries, etc.)

## Why this skill over alternatives

This skill uses the **official Granola public REST API** with a simple env-var API key.
No desktop app, no browser, no macOS dependency at runtime. This makes it the easiest
option for **headless and VPS-hosted OpenClaw setups**.

| Skill | Approach | VPS-friendly? |
|-------|----------|---------------|
| **granola-direct-api** (this one) | Official public REST API + env-var key | Yes |
| granola-notes (CSV) | Parses offline CSV exports (30+ days old, no transcripts) | Partial — needs file transfer |
| granola (local cache) | Reads macOS local cache files | No — Mac-only |
| granola (sync.py) | Reverse-engineered internal API via supabase auth | No — needs desktop app auth |
| granola-mcp (maton.ai) | MCP gateway with browser OAuth flow | No — needs browser for OAuth |

Key advantages:

- **Works anywhere** — only needs `curl`, `jq`, and an env var
- **No OAuth/browser flow** — set the env var once and you're done
- **No third-party proxy** — calls the official Granola API directly
- **No local cache dependency** — doesn't require the Granola desktop app to be running

## Security posture

- **Read-only** — cannot create, edit, or delete anything in Granola
- **Single domain** — HTTPS requests only to `public-api.granola.ai`, no other endpoints
- **No external code** — no downloads, no `exec`, no install scripts, no external binaries
- **Env-var auth only** — API key read from the `GRANOLA_API_KEY` environment variable. Users configure persistence via standard OpenClaw `.env` or shell profiles.
- **No data persistence** — the skill itself writes nothing to disk during execution unless explicitly asked.

---

## Setup

### Requirements

- A Granola account on a **Business** or **Enterprise** plan
- `curl` and `jq` binaries must be installed on your system:
      Linux: `sudo apt update && sudo apt install curl jq -y`
      macOS: `brew install curl jq`
      Windows: `winget install jqlang.jq`

### Installation
```bash
clawhub install granola-direct-api
```

### Step 1: Get your API key

1. Open the **Granola desktop app** on your Mac or PC.
2. Go to **Settings → API**.
3. Click **Create new key**.
4. Copy the key (it starts with `grn_`).

> **Enterprise users:** If the API option is not visible, your workspace admin needs to
> enable "Allow personal API keys" in **Settings → Workspace** first.

### Step 2: Configure the API Key

OpenClaw requires explicit authorization to pass your API key to this skill. Run the following command to securely map your key to the `granola-direct-api` slug:

**Standard Configuration (All Platforms):**
```bash
openclaw config set skills.entries.granola-direct-api.env.GRANOLA_API_KEY "grn_your_key_here"
```
> **Important:** Never hardcode the API key in SKILL.md, scripts, MEMORY.md, or commit
> it to version control.

### Step 3: Restart and Verify

```bash
openclaw gateway restart
```
1. Verify the System Status
Check that the gateway successfully loaded your API key and dependencies:

```bash
openclaw skills info granola-direct-api
```
You should see a green ✓ Active status and a checkmark next to your GRANOLA_API_KEY.

2. Test the Integration
Open your OpenClaw chat and send the following prompt:

"Using granola-direct-api, what was my most recent meeting?"

If the assistant returns your latest meeting notes, your setup is complete!

---

## Access scope

- **Personal API keys** grant read access to the key holder's own notes.
- **Workspace API keys** (Enterprise) grant read access to notes shared in workspace-wide
  folders.
- Only notes with a completed AI summary and transcript are returned. Notes still
  processing or never summarized won't appear.

## Links

- [Official Granola API docs](https://docs.granola.ai/introduction)
- [Granola](https://granola.ai)

## License

MIT
