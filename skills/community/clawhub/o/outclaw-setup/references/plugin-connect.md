# Plugin connection flows

Steps 1-5 of the setup wizard. Use after inventory (Step 0 in
`inventory-check.md`). Skip any plugin already marked `ready`.

## Agent execution rule

All `openclaw` / `gog` / `linkedin-cli` commands are executed by the agent
via shell, not presented to the user. Capture stdout/stderr, retry on
failure, diagnose issues conversationally. The user is only asked for:

- Choices (which provider, yes/no, skip/connect)
- Credentials (API keys)
- OAuth completion confirmation

If a command fails, diagnose and either retry or explain — never dump raw
error output or ask the user to run commands manually.

## Transport-aware OAuth

Before any OAuth step, detect transport:

```python
from shared.scripts.setup_check import detect_transport
t = detect_transport()   # "local" or "remote"
```

**Local user (screen available):**
- Open OAuth URL in browser; poll for completion.

**Remote user (Telegram, Slack, Discord, etc.):**
1. Send the OAuth URL as a clickable link in chat:
   *"To connect <service>, open this link on any device and sign in: <URL>"*
2. Tell the user: *"Once you've signed in, paste the callback URL you were
   redirected to (starts with `http://localhost...`) or just say 'done'."*
3. If user pastes callback URL → extract auth code, finalize flow.
4. If user says "done" → verify via plugin status check.
5. If verification fails → offer to resend the link.

**Safe default:** when transport is unknown, send the link (never assume
browser).

## Step 1: Welcome & Leadbay pitch

```
Welcome to OutClaw — your AI outreach agent.

OutClaw is powered by Leadbay, an agentic knowledge base that gives me
deep intelligence about the people and companies you're reaching out to.
With Leadbay, I can:

• Research prospects automatically — size, tech stack, recent news, key contacts
• Match leads against your ICP
• Personalize messages with real context
• Log every outreach event against the lead so nothing falls through cracks

Let's connect Leadbay first — it's the part that makes the rest actually smart.
```

## Step 2: LeadClaw / Leadbay onboarding

### If LeadClaw is `ready`

Test: fetch the user's account info. Confirm:
"Connected to Leadbay as <user@company>. I can see your leads and will log
outreach activity there."

→ `memory_log.sh` a `plugin_setup` entry (key=`leadclaw`, insight=`connected
<date>`, source=`observed`, confidence=10).

### If LeadClaw is `missing`

1. Ask: "Do you already have a Leadbay account?"

**Existing user path:**
- Guide through LeadClaw install. (Side-loaded — follow leadbay.ai instructions.)
- Verify with a test call.

**New user path:**

```
I'd strongly recommend creating a free Leadbay account. Without it, campaigns
miss the personalization that makes outreach effective. 2 minutes:

1. leadbay.ai/signup
2. Create your workspace
3. Install the LeadClaw plugin and connect it to your account
4. Come back — I'll verify the connection
```

### If user declines Leadbay

```
OutClaw can still work without Leadbay, but campaigns will be weaker. You can
always say "set up leadbay" later.
```

→ `setup_state.leadbay_connected = false`. Proceed to Step 3 with degraded-
mode warning.

## Step 3: Email (recommended)

Ask: "Connect email for outreach? (Recommended, optional — skip if you prefer
LinkedIn or other channels.)"

If yes, ask which provider:

| Provider | Action |
|----------|--------|
| Gmail | `gog` CLI (see below) |
| Outlook | Guide Microsoft Graph MCP or manual IMAP/SMTP |
| Other | SMTP config form |

### Gmail via `gog`

1. Check existing auth: `gog auth list -j`
2. If any account has `gmail` in services, reuse it:
   *"You have <email> already authorized for Gmail — use this account?"*
3. Otherwise: `gog auth add <email> --services gmail` (transport-aware OAuth)
4. Verify: `gog gmail messages search "from:me" --max 1 -j` succeeds

If user skips: `channels.email.status = "skipped"`; proceed.

## Step 4: Calendar (recommended)

Prompt: "Want to connect calendar so I can schedule follow-ups and check
availability?"

- If a `gog` account already has `gmail`, offer to extend it with the
  calendar scope (single OAuth).
- Run `gog auth add <email> --services calendar` (or add scope).
- Verify: `gog calendar events --max 5 -j` succeeds.

If skipped: `channels.calendar.status = "skipped"`.

## Step 5: Additional channels (optional)

"Want to reach people on more channels? Each one makes campaigns more
effective."

| Channel | Method | Notes |
|---------|--------|-------|
| LinkedIn | `openclaw plugins install arun-8687/linkedin-cli` | Connection requests, InMails, DMs |
| Slack | MCP UUID `597f662f-36de-437e-836e-5a81013cbfbe` | Team DMs, internal notifications |
| WhatsApp | Community MCP (self-hosted) | Guide install |
| Calendly | MCP UUID `d778b2f9-25f4-42a2-87ab-dbaa896deb1b` | Scheduling link generation |
| Twitter/X | ClawHub | Public engagement (follow/like/comment) |

For each selected channel, the agent executes install + auth directly.

## Step 6: Verification dashboard

Show the final status table (see outclaw-setup/SKILL.md §Step 4). Mark the
wizard complete in `setup_state.json`. Conclude with lead count from Leadbay
(if connected) and transition to style learning.

## Completion rule

Wizard completes successfully when **at least one outreach channel** (email,
LinkedIn, Slack, WhatsApp) is connected. Email and calendar are recommended,
not required.

## Memory writes during connect

On every successful connect:

```bash
bash "$SHARED/scripts/memory_log.sh" '{
  "skill":"outclaw-setup","type":"plugin_setup",
  "key":"<plugin>","insight":"connected <ISO-date>; <test-result>",
  "confidence":10,"source":"observed"
}'
```

On skip:

```bash
bash "$SHARED/scripts/memory_log.sh" '{
  "skill":"outclaw-setup","type":"plugin_setup",
  "key":"<plugin>","insight":"skipped by user <ISO-date>",
  "confidence":10,"source":"user-stated"
}'
```
