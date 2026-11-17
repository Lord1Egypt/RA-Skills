# One-Shot Agent Setup Prompt

Copy the block below and paste it into your AI agent (Hermes, Claude Code, etc.). The agent will install the plugin, verify it works, and tell you to restart.

---

## Step 1: Install

Paste this to your AI agent:

```text
Install the hermes-time-awareness plugin for Hermes Agent:

1. Clone and install:
   git clone https://github.com/mfang0126/hermes-time-awareness.git /tmp/hermes-time-awareness
   cd /tmp/hermes-time-awareness && bash scripts/install.sh

2. Verify:
   cd ~/.hermes/plugins/hermes-time-awareness && bash scripts/doctor.sh

3. If all checks pass, restart Hermes:
   hermes gateway restart

Report: installed ✓/✗ · tests ✓/✗ · plugin enabled ✓/✗
```

---

## What happens

The installer will:
- Symlink the plugin into `~/.hermes/plugins/hermes-time-awareness`
- Enable the plugin via `hermes plugins enable`
- Run 13 unit tests
- Verify time context output works

After restart, every LLM turn will include a time block like:
```
[time: 2026-08-29 18:00 AEST +10:00 Sat]
```

When you come back after a break:
```
[time: 2026-08-29 20:30 AEST +10:00 Sat | idle: 2h]
```

No configuration needed — works out of the box.
