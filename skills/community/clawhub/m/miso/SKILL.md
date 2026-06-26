# Mission Control - MISO

## Overview
**MISO** is a Telegram-native mission control for OpenClaw multi-agent workflows.
It standardizes visibility for parallel work so operators can track progress from the chat list.

## State model
`INIT` → `RUNNING` → `PARTIAL` → `AWAITING APPROVAL` → `COMPLETE` (+ `ERROR`)

State reactions:
- `🔥` : INIT / RUNNING / PARTIAL
- `👀` : AWAITING APPROVAL
- `🎉` : COMPLETE
- `❌` : ERROR

## Message format (required)
Use plain text, no code blocks.

- Left aligned
- Keep this frame:
  - `🤖 MISSION CONTROL`
  - `——————————————`
  - `🌸 powered by miyabi`

Template:

🤖 MISSION CONTROL
——————————————
📋 {mission}
⏱ {elapsed} ∣ 🧩 {done}/{total} agents ∣ {state}
- Issue: #{issue-number}
- Owner: SHUNSUKE AI
- Goal: {goal}

↳ {agent-a}: {status-a}
↳ {agent-b}: {status-b}
↳ {agent-c}: {status-c}

- Next: {next action}
——————————————
🌸 powered by miyabi

## Commands
Comment on Issue with:
- `/agent analyze`
- `/agent execute`
- `/agent review`
- `/agent status`
- `/task-start`
- `/task-plan`
- `/task-close`

## /task-start
/task-start
- Owner: SHUNSUKE AI
- Issue/Context: #<issue-number>
- Goal: <one-sentence objective>
- Scope: <files/areas>
- Completion Criteria: <what defines done>
- Risk: <none|low|medium|high>

## /task-plan
/task-plan
Execution plan:
- issue-analysis
- agent-execution (or agent-teams / ai-triad)
- git-workflow
- debugging-troubleshooting

## /task-close
/task-close
- Implemented: <summary>
- Validation: <tests/checks passed>
- Changes: <files changed>
- Risks / next steps: <follow-up>
- Notify: pushcut / telegram-buttons

## Reproducibility rules
1. Same header/footer for all missions.
2. Keep state and status updates deterministic.
3. Include `Issue`, `Goal`, `Status`, `Next action` every update.
4. For approvals, use explicit AWAITING state and user action.
5. On completion/error, close each mission with state summary and artifacts.
