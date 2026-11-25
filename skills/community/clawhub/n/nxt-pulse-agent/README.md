# NXT Pulse Agent v0.6.0

> **Proactive, energy-aware task management for OpenClaw agents — local-only, consent-first.**

NXT bridges the gap between reactive chat and proactive partnership. It estimates your task capacity from recent conversation and adapts its tone so the right tasks get proposed at the right time — preventing burnout and decision paralysis without ever phoning home.

## ✨ New in v0.6.0

- **Hard consent gate**: NXT Pulse is fully inert until you explicitly opt in. `/pulse forget` revokes everything.
- **Privacy-first defaults**: `CONTEXT_SOURCES` empty by default, bounded message window, redacted logs with a 500-entry cap — or no log at all with `LOG_HISTORY: false`.
- **Anti-nag backoff**: ignore two nudges in a row and NXT Pulse automatically doubles its cooldown — silence is respected, not re-litigated.
- **Unknown state + hysteresis**: no more over-confident readings — weak evidence means no nudge, and state can't flip on a single message.
- **Full command surface**: `/pulse privacy`, `/pulse forget`, `/pulse off`, `/pulse now`, `/pulse help`, `/pulse sensitivity`.
- **Quiet hours**: no nudges between `22:00–08:00` local by default.
- **Prompt-only architecture**: no runtime scripts; all side effects are documented and inspectable.
- **`SECURITY.md`**: threat model, data disclosure table, and a remediation map for every v0.5.0 audit finding.
- **`TESTING.md`**: pre-release acceptance matrix covering consent, injection, and privacy scenarios.

> **⬆️ Upgrading from 0.5.0?** NXT Pulse now asks for consent on first use — that's expected. Run `/pulse privacy` to review what it reads and writes, then accept. Your old state file is migrated, not discarded.

## 📦 Installation

```bash
openclaw skills install @adnxone/nxt-pulse-agent
```

Update later with:

```bash
openclaw skills update @adnxone/nxt-pulse-agent
```

## 🚦 Consent

On first use NXT Pulse shows its privacy summary and asks for opt-in. Until you accept, it does **nothing**: no nudges, no analysis, no file reads. Everything stays on your device — see [`SECURITY.md`](SECURITY.md) for the full disclosure table.

## ⚙️ Configuration

Add a `config` object to your skill entry in `openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "nxt-pulse-agent": {
        "enabled": true,
        "config": {
          "PULSE_SENSITIVITY": 3,
          "MAX_CONTEXT_CHARS": 5000,
          "PULSE_COOLDOWN": "4h",
          "DOWNTIME_KEYWORDS": [],
          "CONTEXT_SOURCES": ["notes/daily-journal.md"],
          "SCOPE": "dm",
          "MAX_MESSAGES_SCANNED": 10,
          "PULSE_LANGUAGES": "auto",
          "QUIET_HOURS": "22:00-08:00",
          "LOG_HISTORY": true
        }
      }
    }
  }
}
```

| Setting | Description | Default |
|---------|-------------|---------|
| `PULSE_SENSITIVITY` | 1–5 confidence threshold for nudging (1 = conservative, 5 = sensitive). | `3` |
| `MAX_CONTEXT_CHARS` | Total character budget for `CONTEXT_SOURCES` per pulse. | `5000` |
| `PULSE_COOLDOWN` | Minimum time between proactive nudges (e.g. `30m`, `4h`). | `4h` |
| `DOWNTIME_KEYWORDS` | Optional language-specific hard-triggers for Recovery Mode. | `[]` |
| `CONTEXT_SOURCES` | Opt-in files (relative paths only) consulted during a pulse. **Read rules are enforced — see SKILL.md.** | `[]` |
| `SCOPE` | `dm` or `group`. Group analysis stays off unless `group`. | `dm` |
| `MAX_MESSAGES_SCANNED` | Max messages read per pulse, current session only. | `10` |
| `PULSE_LANGUAGES` | `"auto"` follows your writing language; or a list like `["en"]`. | `"auto"` |
| `QUIET_HOURS` | Local-time window with no nudges; `""` disables. | `22:00-08:00` |
| `LOG_HISTORY` | `false` disables `pulse-history.jsonl` entirely (state/flags still persist). | `true` |

## 🕹 Commands

| Command | What it does |
|---|---|
| `/pulse` | State (🟢 🟡 🔴 ⚪), confidence, reasoning, next nudge time. |
| `/pulse set green\|yellow\|red [why]` | Manual override with optional reason. |
| `/pulse quiet [duration]` | Mute nudges (`30m`, `2h`, or until tomorrow). |
| `/pulse on` / `/pulse off` | Global kill switch. |
| `/pulse now` | Ask for a nudge right now (the only cooldown bypass). |
| `/pulse forget` | Revoke consent and delete all local state. |
| `/pulse privacy` | Live disclosure of reads/writes/retention. |
| `/pulse sensitivity 1-5` | Tune sensitivity live. |
| `/pulse help` | Command reference. |

## 🛠 How it works

NXT Pulse runs a **Pulse Audit**: consent → mute/cooldown checks → bounded message window (last 10 messages, current session) → state estimate with hysteresis → opt-in context read → decision. If evidence is weak, the state is `⚪ Unknown` and nothing is sent.

**Anti-nag backoff**: if you ignore two nudges in a row, NXT Pulse doubles its cooldown and tells you once ("I'll dial back — next check in 8h"). Any `/pulse` command resets it.

If you say "I've had a long day" twice in a row, the state moves to `🔴 Low` and the agent shifts from task framing to the Downtime Protocol — hydration, breaks, zero work demands.

## 🔒 Privacy at a glance

- **Local only**: state in `memory/pulse-state.json`, audit trail in `memory/pulse-history.jsonl` (capped at 500 entries, redacted to reason codes — or nothing at all with `LOG_HISTORY: false`). Nothing is transmitted.
- **Opt-in files**: `CONTEXT_SOURCES` is empty until you add paths; sensitive patterns are rejected; content is never quoted into nudges or logs.
- **Bounded**: last 10 messages per pulse, 5,000 context characters, one nudge per cooldown window.
- **Reversible**: `/pulse forget` deletes everything.


## ❓ Troubleshooting

- **NXT Pulse never nudges**: check `/pulse` — you may be in quiet hours, quiet mode, `/pulse off`, or below the confidence threshold.
- **Wrong reading**: `/pulse set yellow "busy but not tired"` teaches it; corrections always win.
- **Want it gone**: `/pulse forget` then `openclaw skills update` / uninstall.

---

Developed by **adnXone** (@adnxone).
[GitHub](https://github.com/adnxone/nxt-pulse-agent) | [ClawHub](https://clawhub.ai/adnxone/skills/nxt-pulse-agent) 
