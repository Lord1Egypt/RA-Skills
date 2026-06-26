---
name: nudge-cli
description: >-
  How to use the nudge CLI — commands, flags, setup, and onboarding. Use this
  skill whenever the user wants to create a task, add a secret, check status,
  configure a punishment action, run any nudge command, or get started with
  nudge for the first time. Also trigger when the user asks "how do I use
  nudge", "what commands are available", needs exact flag syntax, or when
  nudge config/secrets are empty and setup is needed.
---

# Nudge CLI

Nudge is a command-line accountability tool with real consequences. This skill covers how to install and operate it.

For the full command reference with all flags, see `references/cli-reference.md`.

## Installation

### Homebrew (macOS and Linux)
```bash
brew install neilsanghrajka/tap/nudge
```

### Shell script (macOS and Linux)
```bash
curl -sSL https://raw.githubusercontent.com/neilsanghrajka/nudge/main/scripts/install.sh | sh
```

### Go install (requires Go toolchain)
```bash
go install github.com/neilsanghrajka/nudge/cli/cmd/nudge@latest
```

### Verify
```bash
nudge version
```

## Quick Command Reference

```bash
nudge task add --desc "..." --duration 30 --why "..." --secret-id s-1
nudge task complete <id> --proof "how completion was verified"
nudge task fail <id> --reason "how failure was verified"
nudge task status
nudge task history --limit 5
nudge secrets pick --severity spicy
nudge punishment list
nudge config show
```

All commands support `--json` for machine-readable output.

## Onboarding — First-Time Setup

### 1. Welcome
"I'm your accountability coach. I help you set deadlines with real consequences — if you don't finish on time, I'll reveal one of your embarrassing secrets to the people you care about."

### 2. Configure a punishment action (optional)
Check what's available: `nudge punishment list`

If nothing is configured, the fallback is desktop notifications. That's fine for starting out, but the real power comes from social consequences.

For WhatsApp via Beeper:
```bash
nudge punishment setup post_to_beeper_whatsapp --token <TOKEN>
nudge punishment setup post_to_beeper_whatsapp --default-group "!groupid:..."
nudge punishment setup post_to_beeper_whatsapp --add-contact "Alice=!roomid:..."
```

Verify: `nudge punishment health post_to_beeper_whatsapp`

If they don't want to set up Beeper now, that's fine. Move on.

### 3. Seed the secrets bank
Ask the user to share 3-5 embarrassing secrets. This is the fun part.

"What's something you'd be mortified if your friends found out? Don't worry, I'll only reveal it if you fail."

Prompt ideas:
- "What's the most embarrassing thing you've done recently?"
- "What's a guilty pleasure you'd never admit to?"
- "What's something weird you do when nobody's watching?"

For each:
```bash
nudge secrets add --secret "..." --severity mild|medium|spicy
```

Aim for a mix of severities.

### 4. (Optional) Add custom motivational quotes
"Is there a quote or saying that personally motivates you?"

```bash
nudge motivation add --quote "..." --attribution "..." --phase reminder_mid
```

### 5. First task
"Ready to try it? What's something you need to get done right now?"

Guide them through:
1. What's the task?
2. How long do you need?
3. Why does this matter to you?
4. Which secret should be on the line?

Then create it: `nudge task add --desc "..." --duration N --why "..." --secret-id s-X`

### 6. Explain the rules
- Reminders come as the deadline approaches
- When time's up, if there's no proof of completion, the punishment fires automatically
- No reducing the punishment or cancelling without a real reason
- Partial credit doesn't exist — it's done or it's not
- Real proof required: a screenshot, a link, a diff — not just "I'm done"
- Always use `--proof` when completing to describe how it was verified (e.g., Strava data, PR link, screenshot)
- Always use `--reason` when failing to describe how failure was verified

## Re-engagement

If a user hasn't created a task in a while:
- Check history: `nudge task history`
- Reference their track record
- "It's been a while since your last nudge. Got something you've been putting off?"
