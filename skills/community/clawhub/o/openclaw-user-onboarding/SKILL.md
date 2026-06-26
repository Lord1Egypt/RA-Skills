---
name: openclaw_user_onboarding
description: Bootstraps new OpenClaw users with guided setup and configurable feature introductions. Auto-triggers on first session if ONBOARDING_PROGRESS.md is missing. Introduces one new OpenClaw capability per day, every few days, or weekly — user's choice. Supports pause, resume, and frequency change via /openclaw-user-onboarding.
metadata: {"openclaw": {"always": true}}
---

# OpenClaw User Onboarding Skill

This skill turns a blank OpenClaw install into a useful, personalized assistant.
It runs silently in the background — one setup conversation, then one short
introduction at your chosen pace — until you've explored the full platform.

---

## Part 1 — Auto-Trigger Logic

At the start of every **interactive** (non-cron, non-background) session:

1. Check whether `ONBOARDING_PROGRESS.md` exists in the workspace.
2. Act based on its status:

| State | Action |
|---|---|
| File missing | Start **Phase 1 — Discovery** immediately as your first reply |
| `status: active` | Ensure the intro cron job exists (create it if missing) — then proceed normally |
| `status: paused` | Do nothing — wait for explicit `/openclaw-user-onboarding` invocation |
| `status: complete` | Do nothing — all features introduced |

Do **not** run auto-trigger logic during cron runs, sub-agent sessions, or
isolated background turns. Check: if `payload.kind` is `agentTurn` from cron,
skip this skill's auto-trigger entirely.

---

## Part 2 — Phase 1: Discovery (first run only)

When `ONBOARDING_PROGRESS.md` is missing, greet the user warmly and ask these
questions **one at a time**, waiting for each answer before the next:

**Q1 — Name**
> "Hi! I'm getting myself set up to be as helpful as possible. What should
> I call you?"

**Q2 — Primary messaging channel**
> "Which app do you use most for messaging? (e.g. iMessage, WhatsApp,
> Telegram, Slack, Discord — or just here in chat)"

**Q3 — Main goal**
> "What's the main thing you're hoping I can help with? For example:
> staying on top of tasks and emails, automating repetitive work, coding
> assistance, or just having a smart assistant available everywhere?"

**Q4 — Timezone**
> "What timezone are you in? I want to schedule check-ins at sensible times."

**Q5 — Introduction frequency**
> "How often would you like me to introduce a new OpenClaw feature?
> - **Daily** — fast track, one feature per day (10 days total)
> - **Every 3 days** — steady pace, done in about a month
> - **Weekly** — relaxed, one feature per week (default)
> - Or tell me any other interval you prefer."

After all five answers, proceed to **Phase 2 — Setup**. Do not ask for
more detail than needed; the user can always tell you more later.

---

## Part 3 — Phase 2: Setup

Perform these steps silently (no need to narrate each one). Announce when done.

### 3a — Resolve the cron expression from Q5

Convert the user's frequency answer into a cron schedule:

| User says | Cron expression | Plain description |
|---|---|---|
| "daily" / "every day" / "1 day" | `0 10 * * *` | Every day at 10am |
| "every 2 days" | `0 10 */2 * *` | Every 2 days at 10am |
| "every 3 days" | `0 10 */3 * *` | Every 3 days at 10am |
| "every N days" | `0 10 */N * *` | Every N days at 10am |
| "weekly" / "every week" / "once a week" | `0 10 * * 0` | Every Sunday at 10am |
| "every N weeks" | `0 10 * * 0/N` | Every N weeks on Sunday |
| "twice a week" | `0 10 * * 1,4` | Monday and Thursday at 10am |
| Custom expression provided | Use as-is | As described by user |

If the user gives an ambiguous or unsupported answer, default to `0 10 * * 0`
(weekly) and tell them.

Store both the cron expression and a human-readable description in
`ONBOARDING_PROGRESS.md`.

### 3b — Write USER.md

Create or update `USER.md` in the workspace:

```markdown
# User Profile

Name: <name from Q1>
Primary channel: <channel from Q2>
Main goal: <goal from Q3>
Timezone: <timezone from Q4>
Onboarding started: <today's date>
```

### 3c — Write SOUL.md (if it doesn't already exist)

Create a starter `SOUL.md` tuned to the user's goal:

```markdown
# Persona

You are a proactive, helpful personal assistant.
Tone: friendly but concise — no filler phrases like "Certainly!" or
"Great question!". Get to the point.

Adapt to the user's stated goal:
- Tasks/email focus: prioritise actionable summaries and follow-up reminders
- Automation focus: suggest cron jobs and skills for repetitive patterns
- Coding focus: be precise, prefer code examples over prose
- General assistant: balanced, warm, practical
```

If `SOUL.md` already exists, do not overwrite it.

### 3d — Write HEARTBEAT.md

Create `HEARTBEAT.md` (overwrite only if it's empty or missing):

```markdown
# Heartbeat checklist

- Scan for anything time-sensitive (messages, reminders, cron alerts).
- If an onboarding feature intro is due soon, surface it gently.
- If nothing needs attention, reply HEARTBEAT_OK.
```

### 3e — Create the feature-intro cron job

Add a cron job using the `cron` tool with the expression from step 3a:

```json
{
  "action": "add",
  "job": {
    "name": "OpenClaw Feature Discovery",
    "schedule": {
      "kind": "cron",
      "expr": "<cron expression from 3a>",
      "tz": "<timezone from Q4>"
    },
    "sessionTarget": "session:openclaw-onboarding",
    "payload": {
      "kind": "agentTurn",
      "message": "Read ONBOARDING_PROGRESS.md from the workspace. If status is 'active', find the next unchecked feature in the curriculum, introduce it in 2–3 plain sentences with one concrete example the user can try right now, then ask if they would like to set it up. Mark the feature as introduced with today's date. If status is 'paused' or 'complete', reply NO_REPLY.",
      "lightContext": false
    },
    "delivery": {
      "mode": "announce",
      "channel": "<primary channel from Q2>",
      "to": "<user's contact on that channel if known>"
    }
  }
}
```

Store the returned `jobId` in `ONBOARDING_PROGRESS.md`.

### 3f — Write ONBOARDING_PROGRESS.md

Create `ONBOARDING_PROGRESS.md` in the workspace:

```markdown
# OpenClaw Onboarding Progress

status: active
started: <today's date>
intro_cron_job_id: <jobId from step 3e>
intro_frequency: <human-readable description, e.g. "daily", "every 3 days", "weekly">
intro_cron_expr: <cron expression, e.g. "0 10 * * *">
primary_channel: <channel>
delivery_target: <user contact>

## Feature Curriculum

- [ ] 1. Heartbeat & HEARTBEAT.md — always-on check-ins without bothering you
- [ ] 2. Cron reminders (main session) — "remind me in 20 minutes"
- [ ] 3. Cron isolated reports — scheduled summaries delivered to your chat
- [ ] 4. Skills — extending the agent with new capabilities
- [ ] 5. Multi-channel routing — same agent, every platform you use
- [ ] 6. Browser automation — agent controls a browser on your behalf
- [ ] 7. Sub-agents — spawn parallel workers for long tasks
- [ ] 8. Multi-agent setup — multiple personas on one gateway
- [ ] 9. Webhooks + Gmail trigger — external events wake the agent
- [ ] 10. MCP servers — connect any external tool to the agent
```

### 3g — Send a friendly completion message

After setup is done, tell the user what was configured, using their actual frequency:

> "You're all set, <name>! I've saved your profile, set up a regular
> heartbeat checklist, and scheduled a short feature introduction for you
> <intro_frequency> at 10am — 10 features total, one at a time.
> Nothing overwhelming. You can pause anytime by saying 'pause onboarding',
> change the pace with 'change onboarding frequency', and pick back up with
> '/openclaw-user-onboarding'. What would you like to do first?"

---

## Part 4 — Phase 3: Feature Introductions

This phase runs automatically via the cron job created in Phase 2 at whatever
frequency the user chose. The cron message instructs the agent to:

1. Read `ONBOARDING_PROGRESS.md`
2. Find the **first unchecked** `[ ]` item in the curriculum
3. Introduce it using the description below (2–3 sentences + one example)
4. Ask: "Would you like to try setting this up now?"
5. Mark the item as done: `- [x] N. Feature Name — introduced <date>`
6. Save the updated file

### Feature Introductions Script

Use these descriptions. Adapt tone to the user's goal from USER.md.

**1. Heartbeat & HEARTBEAT.md**
> "The heartbeat is your agent's idle cycle — every 30 minutes, it quietly
> checks a small file called HEARTBEAT.md for things to keep an eye on.
> I already set one up for you! Try adding a line like
> '- If any tasks are overdue, remind me' and I'll surface it next time."
> Example: edit `HEARTBEAT.md` and add a line — it takes effect immediately.

**2. Cron reminders (main session)**
> "You can ask me to remind you of anything, and I'll schedule it
> automatically. Just say 'remind me in 20 minutes to call the dentist' and
> I'll create a one-shot cron job that injects a nudge into our conversation
> at the right time."
> Example: "Remind me in 1 hour to review the proposal."

**3. Cron isolated reports**
> "Cron jobs can also run fully on their own — I spin up a fresh session,
> do some research or summarising, and deliver the result to your chat.
> Great for daily briefings that arrive before you wake up."
> Example: "Every morning at 7am, summarise my overnight GitHub
> notifications and send it here."

**4. Skills**
> "Skills are small instruction sets that teach me how to use specific
> tools — like controlling a browser, running code, or calling an API.
> You can see what's loaded with 'openclaw skills list', and install new
> ones from ClawHub at clawhub.ai."
> Example: run `openclaw skills list` to see what I can already do.

**5. Multi-channel routing**
> "I can listen and reply on multiple platforms simultaneously — WhatsApp,
> Telegram, Slack, iMessage, and more. Configure each channel once and just
> message me wherever you are."
> Example: set up a second channel so I respond both here and on Telegram.

**6. Browser automation**
> "I have access to a dedicated browser I can control — clicking, filling
> forms, taking screenshots, extracting data from pages. It's isolated from
> your personal browser, so it's safe to hand me credentials for specific tasks."
> Example: "Log into my GitHub, check for new security alerts, and summarise them."

**7. Sub-agents**
> "For long or parallel tasks, I can spawn background workers that run
> independently and report back. Your main conversation stays responsive while
> the work happens in parallel."
> Example: "Research three competing products at the same time and compare them."

**8. Multi-agent setup**
> "You can run multiple fully isolated personas on the same gateway — different
> names, personalities, and channel bindings. Useful for a work vs. personal
> split, or sharing a gateway with someone else."
> Example: add a second agent that handles only your work Slack.

**9. Webhooks + Gmail trigger**
> "External events can wake me directly. Wire a Gmail inbox to the gateway and
> every new email triggers an agent turn, or use a webhook URL to wake me from
> any external service."
> Example: new email arrives → I triage it and surface anything urgent.

**10. MCP servers**
> "MCP (Model Context Protocol) lets me consume tools from any external server —
> databases, APIs, custom business logic. Manage servers with 'openclaw mcp set'
> and I discover their tools automatically at session start."
> Example: connect a local Postgres MCP server so I can query your database directly.

---

## Part 5 — Pause, Resume, and Frequency Change

### Pausing

When the user says "stop onboarding", "pause onboarding", "skip the feature
introductions", or similar:

1. Update `ONBOARDING_PROGRESS.md`: `status: active` → `status: paused`
2. Disable the cron job:
   ```json
   { "action": "update", "jobId": "<intro_cron_job_id>", "patch": { "enabled": false } }
   ```
3. Confirm:
   > "Got it — I've paused the feature introductions. Resume anytime with
   > '/openclaw-user-onboarding' or 'resume onboarding'."

### Resuming

When the user invokes `/openclaw-user-onboarding` or says "resume onboarding":

1. Read `ONBOARDING_PROGRESS.md`:
   - Missing → start Phase 1 (full onboarding from scratch)
   - `status: paused` → re-enable cron, set status to `active`, confirm
   - `status: active` → show progress and next feature
   - `status: complete` → offer a second pass or deeper dive on any topic

2. Re-enable the cron job:
   ```json
   { "action": "update", "jobId": "<intro_cron_job_id>", "patch": { "enabled": true } }
   ```

3. Confirm, including the current frequency:
   > "Welcome back! Resuming from feature N: <feature name>. Intros are set to
   > <intro_frequency>. Anything you'd like to explore now instead of waiting?"

### Changing frequency

When the user says anything like "change onboarding frequency", "make it daily",
"slow down the introductions", "switch to every 3 days", or similar:

1. Ask for (or read from the message) the new frequency.
2. Resolve the new cron expression using the table in step 3a.
3. Update the cron job schedule:
   ```json
   {
     "action": "update",
     "jobId": "<intro_cron_job_id>",
     "patch": {
       "schedule": {
         "kind": "cron",
         "expr": "<new cron expression>",
         "tz": "<timezone from ONBOARDING_PROGRESS.md>"
       }
     }
   }
   ```
4. Update `ONBOARDING_PROGRESS.md`:
   - `intro_frequency: <new human-readable description>`
   - `intro_cron_expr: <new cron expression>`
5. Confirm:
   > "Done — I've switched your feature introductions to <new frequency>.
   > The next one will arrive on <next scheduled date>."

### Marking complete

After the last feature (10. MCP servers) is introduced, update the file:

```
status: complete
completed: <date>
```

Disable the cron job and send a final message:

> "That's the full tour! You've explored all 10 core OpenClaw features.
> I'll keep the heartbeat running as usual. If you want to revisit any
> feature in depth, just ask — or call '/openclaw-user-onboarding' to start a
> deeper second pass."

---

## Installation

Copy this directory into your OpenClaw workspace skills folder:

```bash
cp -r openclaw-onboarding ~/.openclaw/workspace/skills/
```

Start a new session — onboarding begins automatically on the first reply:

```bash
/new
# or
openclaw agent --message "Hello"
```

To share with others, publish to ClawHub:

```bash
clawhub sync --all
```
