# Proof of Work — Automated Completion Verification for AI Agents

Use this skill to verify that your AI agents actually completed what they claimed, not just that they said they did.

## What This Skill Does

Runs automated verification checks after agent task completion:
- Did the expected output file exist and contain valid content?
- Did the expected system state change actually happen?
- Did the agent log a completion that matches what was assigned?

Catches the most common AI agent failure mode: the confident-sounding completion that didn't actually do anything.

## When to Use

- Any time an agent reports TASK_COMPLETE on critical work
- Before promoting an agent from "draft and review" to "act autonomously"
- When debugging why something that "was done" isn't actually done
- As a gate before downstream work depends on a previous agent's output

## How It Works

A shell script that runs after agent task completion. Checks:

1. **File existence** — Did the expected output path get created?
2. **Content validation** — Does the file contain expected markers (non-empty, valid JSON, expected keywords)?
3. **State checks** — Did the expected system state change? (process running, port listening, DB record created)
4. **Log correlation** — Does the activity_log entry for this task show TASK_COMPLETE (not TASK_BLOCKED or silence)?

Returns exit code 0 on pass, 1 on fail. Integrates with any CI/cron pipeline.

## Installation

```bash
chmod +x install.sh && ./install.sh
```

## Usage

```bash
# Verify a file output
./proof-of-work.sh --check-file /path/to/expected/output.md

# Verify a process is running
./proof-of-work.sh --check-process "queue-manager"

# Verify a DB record exists
./proof-of-work.sh --check-db ~/.agentops/agentops.db --query "SELECT count(*) FROM queue_items WHERE status='done' AND id=42" --expected 1

# Full verification suite
./proof-of-work.sh --config verification.json
```

## Sample Verification Config

```json
{
  "task_id": 42,
  "checks": [
    {"type": "file", "path": "~/.agentops/output/report.md", "min_size": 100},
    {"type": "db", "db": "~/.agentops/agentops.db", "query": "SELECT status FROM queue_items WHERE id=42", "expected": "done"},
    {"type": "log", "event_type": "TASK_COMPLETE", "agent_id": "buzz"}
  ]
}
```

## Part of Trust AI Suite

Proof of Work is the verification layer of the Trust AI Suite:

- **Accountable AI** — Governance & accountability
- **Proof of Work** (this) — Verify agents completed tasks
- **AgentOps Tracker** — Full operational visibility ($49)
- **Total Recall** — Forensic memory search ($69)
- **Anticipation** — Predict what you need before you ask ($39)

→ Full suite: [Trust AI Stack on ClawMart](https://www.shopclawmart.com)
