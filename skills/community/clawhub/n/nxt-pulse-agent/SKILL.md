---
name: nxt-pulse-agent
description: "An adaptive proactive agent skill that manages user energy levels and task prioritization using semantic pulse checks."
version: 0.5.0
---

# Next Pulse Agent (NXT) v0.5.0

NXT transforms your agent from a reactive chat-bot into a proactive partner. It adapts its proactivity based on your inferred energy levels, ensuring it's helpful when you're peaking and supportive when you're recharging.

## 🌟 Key Features

- **Semantic Energy Detection**: Infers energy levels (🟢 High, 🟡 Medium, 🔴 Low) from recent interactions.
- **Adaptive Proactivity**: Shifts between "Deep Work", "Micro-Steps", and "Downtime Protocol".
- **Transparency Command (`/pulse`)**: Users can check the agent's current perception of their state and manually override it.
- **Context Guardrails**: Automatically limits external file scanning to the most recent/relevant snippets to save tokens and prevent context overflow.
- **Smart Cooldowns**: Syncs with OpenClaw's heartbeat to minimize noise.

## 🛠 Configuration

The agent reads these values from the skill's configuration entry in `openclaw.json` (`skills.entries.nxt-pulse-agent.config`).

- `PULSE_SENSITIVITY`: Integer (1-5). 1 is conservative, 5 is highly sensitive to language cues. (Default: `3`)
- `MAX_CONTEXT_CHARS`: Integer. Maximum characters to read from `CONTEXT_SOURCES` per pulse to keep tokens low. (Default: `5000`)
- `PULSE_COOLDOWN`: Duration string (e.g., `30m`, `4h`). Minimum time between proactivity triggers.
- `DOWNTIME_KEYWORDS`: Array of strings (Optional). Manual "hard-triggers" to force Recovery Mode. Note: The agent's **Semantic Detection** automatically identifies downtime needs in any language based on context, even without keywords.
- `CONTEXT_SOURCES`: Array of strings. Relative paths to files that provide user state (e.g., journals, medical logs).
- `SCOPE`: `dm` (default) or `group`. Limits proactive triggers to specific conversation types.

## 🚀 Commands

- `/pulse`: Shows current energy level, reasoning, and upcoming tasks.
- `/pulse set [green|yellow|red]`: Manually override your energy state.
- `/pulse quiet [duration]`: Mutes proactive nudges for a specific time (e.g., `2h`).

## 🚀 Workflow

### 1. The Pulse Audit
When triggered, the agent performs a **Resource-Safe Audit**:
1. **State Check**: Evaluates capacity using `MAX_CONTEXT_CHARS` from sources.
2. **Sentiment Alignment**: Adjusts based on `PULSE_SENSITIVITY`.
3. **Command Check**: Looks for any active `/pulse quiet` timers.

### 2. Interaction Modes
- **🟢 High Energy**: Focuses on the top 1-2 priority tasks from TODOs.
- **🟡 Medium Energy**: Proposes 5-10 minute "Quick Wins".
- **🔴 Low Energy**: Triggers **Downtime Protocol**. No work demands. Only recovery suggestions (hydration, breaks).

---
Part of the OpenClaw community ecosystem. Built for performance, tuned for human limits.
