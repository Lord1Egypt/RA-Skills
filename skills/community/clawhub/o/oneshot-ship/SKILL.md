---
name: oneshot-ship
description: Ship code with oneshot CLI. One command that plans, executes, reviews, and opens a PR. Runs over SSH or locally. Use when the user wants to ship code changes, automate PRs, or run a coding pipeline with Codex or Claude.
license: MIT
metadata:
  author: ADWilkinson
  version: "1.2.3"
  repository: "https://github.com/ADWilkinson/oneshot-cli"
compatibility: Requires Bun, GitHub CLI, and either Codex CLI or Claude Code CLI. SSH access to a server optional (can run locally with --local)
---

# oneshot CLI

Ship code with a single command. oneshot is an agentic software workflow runtime: repo + task in, isolated agent run out, reviewed PR ready. It runs with one selected fallback provider, or with invisible adaptive routing when `routing.enabled` is true. The router chooses Codex or Claude plus reasoning effort, while each provider stays on its configured frontier model. Works over SSH to a remote server or locally with `--local`.

## When to use this skill

- User wants to ship a code change to a repository without manual coding
- User wants to automate the plan/implement/review/PR workflow
- User mentions "oneshot" or wants to delegate a coding task
- User wants to run a task on a remote server or locally

## Installation

```bash
bun install -g oneshot-ship
```

## Setup

Run `oneshot init` to configure SSH host, workspace path, API keys, and model preferences. Config is saved to `~/.oneshot/config.json`.

Repos on the server should live as `<org>/<repo>` under the workspace path:

```
~/projects/
  my-org/my-app/
  my-org/my-api/
```

### Server prerequisites

- [Bun](https://bun.sh)
- Either [Codex CLI](https://github.com/openai/codex) or [Claude Code CLI](https://docs.anthropic.com/en/docs/claude-code)
- [GitHub CLI](https://cli.github.com) (authenticated)
- `OPENAI_API_KEY` for Codex mode, or `ANTHROPIC_API_KEY` for Claude mode

## Usage

```bash
oneshot <repo> "<task>"                 # ship a task
oneshot <repo> <linear-url>            # ship from a Linear ticket
oneshot <repo> "<task>" --bg           # fire and forget
oneshot <repo> "<task>" --local        # run locally, no SSH
oneshot <repo> "<task>" --mode deep    # skip classification and force deep mode
oneshot <repo> "<task>" --workflow ship # apply a workflow preset
oneshot <repo> "<task>" --deep-review  # force exhaustive review
oneshot <repo> "<task>" --model gpt-5.5 # override configured plan/PR model
oneshot <repo> "<task>" --branch dev   # target a different branch
oneshot <repo> "<task>" --base-path /srv/workspaces  # override repo root for this run
oneshot <repo> "<task>" --worktree-root /tmp/agents   # override temp worktree root
oneshot route "fix failing CI and publish" --json # inspect invisible route
oneshot <repo> --dry-run               # validate only
oneshot init                           # configure
oneshot stats                          # recent runs + timing
oneshot runs                           # durable run ledger
oneshot runs --json --limit 10         # list runs for automation
oneshot status <run-id|events-file> --json  # inspect one run
oneshot eval --json                    # summarize outcomes
oneshot workflow list                  # inspect workflow presets
oneshot workflow show fix-ci --json    # inspect one workflow preset
oneshot policy init                    # create .oneshot/policy.json
oneshot policy init --path ./repo      # write policy in another directory
oneshot mcp serve                      # expose MCP tools over stdio
oneshot doctor                         # package, tool, SSH, and event health
oneshot doctor --repo zkp2p/pay        # health plus checkout existence
```

## Pipeline

1. **Validate**: checks the repo exists, fetches latest from origin
2. **Worktree**: creates a temp git worktree from the target base branch
3. **Route**: oneshot's adaptive router chooses provider, reasoning effort, context shape, execution style, verification profile, and `fast`/`deep` mode
4. **Plan**: routed agent reads the codebase plus `AGENTS.md`/`CLAUDE.md` instructions, package scripts, policy packs, and relevant docs, then outputs an implementation plan
5. **Execute**: routed agent implements the plan. If it times out with partial changes, the pipeline continues
6. **Draft PR**: configurable agent creates a branch, commits, and writes PR metadata; the runtime pushes and opens or updates the draft PR
7. **Review**: configurable agent reviews the diff across correctness, compatibility, runtime contracts, policy, security, docs quality, and simplicity. Confirmed issues are fixed directly
8. **Finalize**: runtime pushes review fixes and marks the PR ready, or preserves the draft if review fails/times out

Every run writes JSONL events to `/tmp/oneshot-<runId>.events.jsonl` and mirrors them into `~/.oneshot/runs/<runId>.events.jsonl`. Worktrees are cleaned up after successful runs and preserved on failure for recovery.

## Configuration

`~/.oneshot/config.json`:

```json
{
  "host": "user@100.x.x.x",
  "basePath": "~/projects",
  "provider": "codex",
  "routing": { "enabled": true },
  "linearApiKey": "lin_api_...",
  "claude": { "model": "opus", "timeoutMinutes": 180 },
  "codex": {
    "model": "gpt-5.5",
    "reasoningEffort": "xhigh",
    "reviewModel": "gpt-5.5",
    "reviewReasoningEffort": "xhigh",
    "timeoutMinutes": 180
  },
  "phases": {
    "classify": { "model": "gpt-5.5", "reasoningEffort": "medium" },
    "plan": { "model": "gpt-5.5", "reasoningEffort": "xhigh" },
    "execute": { "model": "gpt-5.5", "reasoningEffort": "xhigh" },
    "review": { "model": "gpt-5.5", "reasoningEffort": "xhigh" },
    "deepReview": { "model": "gpt-5.5", "reasoningEffort": "xhigh" },
    "pr": { "model": "gpt-5.5", "reasoningEffort": "high" }
  },
  "stepTimeouts": {
    "planMinutes": 20,
    "executeMinutes": 60,
    "reviewMinutes": 20,
    "deepReviewMinutes": 20,
    "prMinutes": 20
  }
}
```

Only `host` is required for SSH runs. Local mode works without a config file.
Remote SSH runs stream the active oneshot config to the server for that run, so `basePath`, provider defaults, timeout settings, and configured Linear credentials stay aligned even if the server does not have its own oneshot config file.

## Flags

| Flag | Short | Description |
|------|-------|-------------|
| `--model` | `-m` | Override configured plan/PR model |
| `--branch` | `-b` | Base branch (default: main) |
| `--base-path` | | Override the workspace path used to locate the repo |
| `--worktree-root` | | Override where temporary git worktrees are created |
| `--mode` | | Skip classification and force `fast` or `deep` mode |
| `--workflow` | | Apply a workflow preset: `ship`, `review`, `fix-ci`, `research`, `docs`, or `swarm-review` |
| `--deep-review` | | Force exhaustive review mode |
| `--local` | | Run locally instead of over SSH |
| `--bg` | | Run in background, return PID + log path |
| `--dry-run` | `-d` | Validate only |
| `--events-file` | | Mirror JSONL events to an additional file |
| `--repo` | | With `doctor`, verify a specific `owner/repo` checkout exists |
| `--provider` | | With `route`, choose the fallback provider (`codex` or `claude`) |
| `--help` | `-h` | Help |
| `--version` | `-v` | Version |

## Customization

- Put an `AGENTS.md` or `CLAUDE.md` in any repo root. oneshot passes the instruction snapshot to the configured agents, and the prompts ask agents to inspect relevant local instruction files directly
- Choose `provider: "codex"` or `provider: "claude"` as the fallback. Set `routing.enabled: true` when oneshot's adaptive router should silently pick Codex or Claude per task
- Configure `claude.model` and `codex.model` as the frontier models for each provider. Adaptive routing varies effort and provider, not model class
- Configure `phases.classify`, `phases.plan`, `phases.execute`, `phases.review`, `phases.deepReview`, and `phases.pr` for model and reasoning defaults when routing is disabled
- Edit `prompts/plan.txt`, `execute.txt`, `review.txt`, `pr.txt` to change pipeline behavior
- Use `oneshot policy init` to add `.oneshot/policy.json` with protected paths, required checks, approval-sensitive keywords, and secret-pattern gates
- Use `oneshot mcp serve` when another agent should call oneshot through tools instead of shelling out ad hoc
- For dense specs, explainers, review maps, incident reports, design sheets, or one-off editors, oneshot can create a self-contained HTML artifact instead of a long markdown wall. Durable artifacts belong in `docs/artifacts/`; throwaway local artifacts belong in `/tmp/oneshot-html-artifacts/`.

## Tips

- Use `--bg` to fire and forget long tasks
- Linear integration moves tickets to "In Review" and comments the PR URL
- Per-step timeouts prevent runaway processes (plan 20m, execute 60m, review 20m, PR 20m)
- Worktree isolation means your main branch is never touched
- Task classification picks `fast` or `deep` mode automatically. Use `--deep-review` to force deep
- Duration estimates come from historical runs per repo (`~/.oneshot/history.json`)
- Durable run events live in `~/.oneshot/runs`; use `oneshot runs`, `oneshot status`, and `oneshot eval` for recovery and feedback loops
- Repo slugs must be exact `owner/repo` values. Nested paths and `..` are rejected before dispatch
- `doctor` compares the running CLI version with the npm registry, checks config, required CLIs, recent event files, SSH reachability, and can verify a specific checkout with `--repo`
- `oneshot mcp serve` exposes tools for running tasks, listing runs, reading status, initializing policy, listing workflows, and summarizing eval outcomes
