---
name: openclaw-msg-delivery-guide
description: Ensure later replies actually reach the user in OpenClaw. Use when the user asks for reminders, scheduled checks, follow-up notifications, completion updates, recurring monitoring, or any task where execution and user-visible delivery happen in different steps. Default to cron for scheduled or notification-critical tasks, use subagent completion for background-result handoff, use direct reply when finishing now, and avoid heartbeat unless the user explicitly wants a soft, low-precision follow-up.
metadata:
  openclaw:
    requires:
      bins: ["openclaw"]
      config: ["~/.openclaw/cron/jobs.json"]
      note: "This skill may inspect and modify local OpenClaw cron configuration, run openclaw cron commands, manually trigger jobs for verification, and send test notifications while validating delivery behavior against the local scheduler store."
---

# OpenClaw Message Delivery Guide

## Core problem

Prevent this failure mode:

- work starts
- the agent promises a later reply
- no real delivery path is bound
- the user never receives the result

Treat **execution** and **delivery** as separate things.
Starting work is not the same as binding a later user-visible message.

## Core rules

### Rule 1: never promise a later reply without a delivery path

Before saying things like:

- "reply in 5 minutes"
- "watch this task and tell me if there is progress"
- "send it later"
- "check this every hour and notify me"

be able to answer all 3:

1. What event counts as completion or reportable progress?
2. Who sends the later message?
3. Which mechanism actually delivers it?

If any answer is unclear, resolve the delivery path first: choose the mechanism, bind the target, and only then promise the follow-up.

### Rule 2: choose mechanism by delivery need

Default map:

- **Direct reply**: result will be sent now
- **Cron**: exact time or repeated schedule; notification matters
- **Subagent**: background task that should report back when finished
- **Heartbeat**: soft, low-precision check-in only; avoid by default and use only when the user explicitly accepts a soft follow-up
- **`message` send**: visible result already sent by tool

### Rule 3: scheduled + notify => cron

For anything like:

- "reply in 5 minutes"
- "remind me in 20 minutes"
- "check this every hour and notify me if it changes"
- "send a report every day at 9"

prefer:

- **one-shot cron** with `--at` for a single future reply
- **recurring cron** with `--cron` for repeated checks
- **`--session isolated`** when the run should execute independently and deliver its own result
- explicit delivery fields derived from current session metadata

Do not default to cron main-session runs unless the user explicitly wants main-session / heartbeat-style behavior.

### Rule 4: background exec does not imply notification

Starting `exec` / `process` / a long-running task only means work has started.
It does **not** mean the user will later receive an update.
If the user expects a later message, bind a real follow-up path.

## Key examples

### 1. "reply in 5 minutes"

Use **one-shot cron**, not heartbeat.

```bash
openclaw cron add \
  --name "Reply in 5 minutes" \
  --at "5m" \
  --session isolated \
  --message "Reply to the user with the requested follow-up. If nothing meaningful changed, say that clearly." \
  --announce \
  --channel <channel> \
  --to <destination>
```

### 2. "run this in the background and tell me when it is done"

Use **subagent** when the main need is background execution plus completion report.

Required behavior:

- start the task
- tell the user the task has started
- when the subagent completion announce is handed back to the requester session, deliver that result to the user immediately

### 3. "check this site every hour and notify me if it changes"

Use **recurring cron isolated + explicit delivery**.

```bash
openclaw cron add \
  --name "Hourly site check" \
  --cron "0 * * * *" \
  --session isolated \
  --message "Check the target site. Notify only when there is a real change; otherwise stay silent." \
  --announce \
  --channel <channel> \
  --to <destination>
```

### 4. visible result already sent via `message`

If the user-visible result has already been delivered via `message(action=send)`, do not send a duplicate normal reply; return only:

`NO_REPLY`

## Bad cases

- Promise a later reply without naming the delivery path
- Use heartbeat for exact reminders or required notifications
- Start background `exec` and assume completion will surface automatically
- Create cron jobs without explicit delivery when the user expects a visible notification
- Bind only a final completion path when the user actually asked for progress updates

## Test and verification

### Cron

After add/edit:

1. confirm the job exists in `openclaw cron list`
2. verify stored fields in `~/.openclaw/cron/jobs.json`
3. run the job once manually
4. confirm the notification reached the intended chat

For recurring jobs, do not rely on the schedule before doing this manual trigger once.

Verify at least:

- schedule kind (`at` vs `cron`)
- session target
- payload message
- delivery mode
- delivery channel
- delivery target

Do not require model verification here; use the default model unless the user explicitly asked for a model override.

When changing a cron job, do not trust CLI output alone; verify the stored job.

### Background-task follow-up

Verify:

1. the task actually started
2. the user knows whether the current turn already delivered a result or not
3. the completion path is explicit

## Extra guidance

### Progress mode

For long-running work, classify the expected update style before promising follow-up:

- **result-only**
- **stage updates**
- **fixed-interval updates**

### Silent-if-no-change

For recurring checks, prefer:

- notify on real change
- otherwise stay silent

### Current-chat delivery

When the result should come back to the same chat, derive delivery target from current session metadata instead of hardcoding user-specific identifiers.
