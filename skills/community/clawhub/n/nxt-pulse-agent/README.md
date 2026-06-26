# NXT Pulse Agent (NXT) v0.5.0

> **Proactive energy-aware task management for OpenClaw agents.**

NXT bridges the gap between reactive chat and proactive partnership. It monitors your state and energy levels to ensure the right tasks are proposed at the right time, preventing burnout and decision paralysis.

## ✨ New in v0.5.0
- **`/pulse` Command**: Full transparency into the agent's "mind".
- **Manual Overrides**: Correct the agent if it misreads your vibe.
- **Token Efficiency**: New context guardrails (`MAX_CONTEXT_CHARS`) for power users.
- **Sensitivity Tuning**: Adjustable `PULSE_SENSITIVITY`.

## 📦 Installation

```bash
clawhub install nxt-pulse-agent
```

## ⚙️ Configuration

To configure NXT Pulse Agent, add a `config` object to your skill entry in `openclaw.json`:

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
          "CONTEXT_SOURCES": ["memory/daily-jurnal.md", "logs/activity.log"]
        }
      }
    }
  }
}
```

| Setting | Description | Default |
|---------|-------------|---------|
| `PULSE_SENSITIVITY` | 1-5 scale for energy state triggers (1=conservative, 5=sensitive). | `3` |
| `MAX_CONTEXT_CHARS` | Character limit for reading external context sources per pulse. | `5000` |
| `PULSE_COOLDOWN` | Minimum time duration between proactive nudges (e.g. 1h, 4h). | `4h` |
| `DOWNTIME_KEYWORDS` | Optional manual triggers. Note: Semantic detection works in any language by default. | `[]` |
| `SCOPE` | Interaction scope: `dm` or `group`. | `dm` |

## 🕹 Commands

- **/pulse**: Check current state.
- **/pulse set [green/yellow/red]**: Manual override.
- **/pulse quiet [time]**: Mute proactive nudges (e.g., `1h`).

## 🛠 How it Works

NXT uses **Semantic Pulse Checks**. It reads the "vibe" of recent messages. If you say "I've had a long day," the agent updates your state to `🔴 Low` and shifts from "Productivity Mode" to "Downtime Protocol."

---
Developed by **adnXone** (@adnxone). 
[GitHub](https://github.com/adnXone/nxt-pulse-agent) | [ClawHub](https://clawhub.ai/nxt-pulse-agent)
