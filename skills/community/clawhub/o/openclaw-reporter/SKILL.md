---
name: openclaw-reporter
description: |
  Opt-in reporter for the OpenClaw global claw heatmap.
  On first use, ASKS the user for consent before registering.
  Heartbeat (platform + model only) is sent only after confirming prior consent
  (i.e. ~/.openclaw/config.json exists from a previous registration).
  Task reports are only sent when the user explicitly mentions completing a task.
  Data collected: user-chosen claw name, OS platform, model name, generic task category.
  Credentials: the server returns an apiKey on registration, which is stored locally
  in ~/.openclaw/config.json and sent as a Bearer token in subsequent requests.
  No file paths, code, tool names, or project-specific data is ever sent.
requirements:
  network: true
  writeFiles:
    - "~/.openclaw/config.json"
  binaries:
    - claw-market
  env:
    - name: CLAUDE_MODEL
      required: false
      description: "Current Claude model identifier. Used to report which model is active. Falls back to 'unknown' if not set."
---

# OpenClaw Reporter

This skill lets you participate in the OpenClaw global claw activity heatmap. It reports **minimal, non-code** activity data to visualize worldwide AI agent usage. Note: as with any HTTPS request, the server can observe your IP address.

## Prerequisites

This skill requires the `claw-market` CLI tool. Install it globally:

```bash
npm install -g @ricardweii/claw-market
```

## How It Works

- **Heartbeat**: Sent once per session, but **only** if `~/.openclaw/config.json` already exists (meaning the user previously consented and registered). There are no automatic hooks — the agent checks for prior consent before sending. No `PostToolUse` or `Stop` hooks are used.
- **Task report**: Sent **only** when the user explicitly mentions completing a task or asks for a report. The agent calls the task API directly — no automated scripts.
- **Registration**: One-time setup requiring explicit user consent (see below).

## Session Start (Consent-Gated)

When this skill is loaded, follow these steps **in order**:

1. Check if `~/.openclaw/config.json` exists:
   ```bash
   test -f ~/.openclaw/config.json && echo "REGISTERED" || echo "NOT_REGISTERED"
   ```
2. **If REGISTERED** (user previously consented): send a heartbeat:
   ```bash
   claw-market heartbeat 2>/dev/null || true
   ```
3. **If NOT_REGISTERED**: do **nothing** automatically. Only proceed with the First-Time Setup below if the user initiates registration or the agent needs to ask.

## Data Disclosure

This skill sends the following data to `https://kymr.top/` (the OpenClaw Market production server; server-side source code is in this repository under `app/api/v1/`):

| Data Field | Example | Purpose |
|---|---|---|
| Claw Name | `CoolClaw42` (user-chosen) | Your display name on the heatmap |
| Platform | `darwin`, `linux` | OS type for heatmap stats |
| Model | `claude-sonnet-4-6` | Model usage stats |
| Task summary | `"Completed a task"` | Generic activity indicator |

**Stored locally:** Registration returns an `apiKey` from the server, saved in `~/.openclaw/config.json` with `chmod 600` (owner-only access). The endpoint URL (`https://kymr.top/`) is hardcoded — not read from the config file — so a modified config cannot redirect telemetry.

**Visible to the server:** Your IP address is visible on every HTTPS request (inherent to any network call). The server uses IP for approximate geolocation on the heatmap — no more precise than city-level.

**Never sent:** system usernames, file paths, code snippets, project names, tool names, tool arguments, tool results, or secrets.

## Configuration

Config is stored at `~/.openclaw/config.json` (permissions `600`). Managed by the `claw-market` CLI tool.

## First-Time Setup (Requires User Consent)

If `~/.openclaw/config.json` does not exist, follow these steps:

### Step 1: Check CLI availability

First, verify `claw-market` is installed:

```bash
which claw-market || echo "NOT_INSTALLED"
```

If not installed, inform the user: "The openclaw-reporter skill requires the claw-market CLI. Install with: `npm install -g @ricardweii/claw-market`"

### Step 2: Ask for consent

Use the AskUserQuestion tool:

- Question: "OpenClaw Reporter wants to register a claw name and send a heartbeat (platform + model only) to https://kymr.top/ when the skill loads. Task reports are only sent when you explicitly mention completing a task. The server will issue an API key stored locally at ~/.openclaw/config.json. No file paths, code, tool names, or project data is sent. Allow?"
- Options: "Yes, register" / "No, skip"

**If the user selects "No, skip":** do NOT register and do NOT ask again in this session. Stop here.

### Step 3: Ask for a claw name

If the user consented, use AskUserQuestion again:

- Question: "Pick a name for your claw on the heatmap! (1-30 chars, letters/numbers/hyphens/underscores only, e.g. CoolClaw, NightCrawler, CodeClaw)"
- Let the user type a custom name via the "Other" option (no preset options needed, but provide a few fun suggestions as options)
- Options: "CoolClaw" / "CodeClaw" / "NightCrawler"

Use whatever the user provides as the claw name.

### Step 4: Register using CLI

After receiving the name, validate and register:

```bash
# Validate claw name: only allow alphanumeric, hyphens, underscores (1-30 chars).
CLAW_NAME="USER_CHOSEN_NAME_HERE"

if ! echo "$CLAW_NAME" | grep -qE '^[A-Za-z0-9_-]{1,30}$'; then
  echo "Error: Claw name must be 1-30 characters, alphanumeric/hyphens/underscores only."
  exit 1
fi

# Register using CLI
claw-market register "$CLAW_NAME"
```

## Task Reporting (Manual Only)

Task reports are **never sent automatically**. Only send a task report when the user explicitly mentions completing a task, finishing work, or asks to report activity.

When triggered, run:

```bash
# Estimate task duration (ask user or use a default)
DURATION_MS=60000  # Default 1 minute, adjust based on actual task time

claw-market task "Completed a task" --duration "$DURATION_MS" || echo "Task report failed (non-blocking)."
```

## Opt-Out / Unregister

To stop all OpenClaw reporting:

```bash
claw-market config clear
```

After deletion, no heartbeats or task reports will be sent. The skill will ask for consent again if re-enabled.

## Behavior Rules

1. **User consent is REQUIRED** before first registration — never register silently
2. If the user declines registration, respect the decision and do not ask again in the same session
3. **Heartbeat is consent-gated** — only sent if `~/.openclaw/config.json` exists (proof of prior consent). There are NO automatic hooks; the agent checks for prior consent before any network call
4. **Task reports are manual only** — only send when the user explicitly mentions completing a task or asks to report
5. If any OpenClaw request fails, continue normally — never interrupt the user's workflow
6. Never include identifying information in task summaries
7. **No system-level modifications**: never write to `~/.claude/settings.json` or any file outside `~/.openclaw/`

## CLI Reference

The `claw-market` CLI provides these commands:

| Command | Description |
|---------|-------------|
| `claw-market register <name>` | Register a new claw |
| `claw-market heartbeat` | Send a heartbeat |
| `claw-market task <summary> -d <ms>` | Report a completed task |
| `claw-market token <input> <output>` | Report token usage |
| `claw-market stats` | Show your token usage statistics |
| `claw-market config show` | Show current configuration |
| `claw-market config path` | Show config file path |
| `claw-market config clear` | Delete configuration (unregister) |

Global options: `--lang <en\|zh>`, `--json`, `--endpoint <url>`

## Token Usage Reporting

Agents can report their token usage to contribute to the global leaderboard.

### When to Report

Report token usage when:
1. The user explicitly asks to report tokens
2. At the end of a significant session (optional, if user has consented)

### How to Get Token Usage

As an AI agent, you can track token usage from the API responses. The usage data includes:
- `input_tokens`: Tokens in your prompts and context (including previous turns)
- `output_tokens`: Tokens in your responses

You can estimate or track cumulative token usage throughout a session.

### CLI Commands

```bash
# Report today's token usage
claw-market token <inputTokens> <outputTokens>

# Report for a specific date
claw-market token <inputTokens> <outputTokens> --date YYYY-MM-DD

# View your token statistics
claw-market stats
```

### Example

If you've used 50,000 input tokens and 12,000 output tokens today:
```bash
claw-market token 50000 12000
```

### Session-End Reporting (Optional)

At the end of a session, you may offer to report token usage:

1. Ask the user: "Would you like me to report today's token usage to the OpenClaw leaderboard?"
2. If yes, report using the token command with your estimated usage
3. If no, continue normally

**Note:** Token reporting is always optional and requires user consent. Never report tokens without asking.
