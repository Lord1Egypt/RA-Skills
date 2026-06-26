---
name: gpu-cli
description: Safely run local `gpu` commands via a guarded wrapper (`runner.sh`) with preflight checks and budget/time caps.
argument-hint: runner.sh gpu [subcommand] [flags]
allowed-tools: Bash(runner.sh*), Read
---

# GPU CLI Skill (Stable)

Use this skill to run the local `gpu` binary from your agent. It only allows invoking the bundled `runner.sh` (which internally calls `gpu`) and read-only file access.

What it does
- Runs `gpu` commands you specify (e.g., `runner.sh gpu status --json`, `runner.sh gpu run python train.py`).
- Recommends a preflight: `gpu doctor --json` then `gpu status --json`.
- Streams results back to chat; use `--json` for structured outputs.

Safety & scope
- Allowed tools: `Bash(runner.sh*)`, `Read`. No network access requested by the skill; `gpu` handles its own networking.
- Avoid chaining or redirection; provide a single `runner.sh gpu …` command.
- You pay your provider directly; this may start paid pods.

Quick prompts
- "Run `runner.sh gpu status --json` and summarize pod state".
- "Run `runner.sh gpu doctor --json` and summarize failures".
- See `templates/prompts.md` for more examples.

Security
- Input sanitization: character blocklist (`; & | \` ( ) > < $ { }` + newlines) plus subcommand allowlist. Commands are executed via direct `gpu` binary invocation — no shell re-evaluation (`bash -c` / `eval`).
- See `SECURITY.md` for the full threat model, permission rationale, and version history.

Notes
- For image/video/LLM work, ask the agent to include appropriate flags (e.g., `--gpu-type "RTX 4090"`, `-p 8000:8000`, or `--rebuild`).
