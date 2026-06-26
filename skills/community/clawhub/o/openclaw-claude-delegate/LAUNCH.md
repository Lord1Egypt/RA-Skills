# OpenClaw Claude Delegate Launch Pack

## Core positioning

**Give Claude back to OpenClaw.**

OpenClaw Claude Delegate gives any OpenClaw agent a locally authenticated Claude Code worker lane, with dispatch, poll, result, resume, and an optional non-root `bypassPermissions` path.

## One-line pitch

Claude was cut out of OpenClaw, this puts it back.

## Short description

Give Claude back to OpenClaw through a local Claude Code delegation lane with monitoring, resume, and an optional non-root `bypassPermissions` worker path.

## Medium description

Third-party harnesses do not reliably get Claude subscription access. OpenClaw Claude Delegate fixes that by giving any OpenClaw agent a stable local lane into Claude Code, with monitoring, resume, bounded workdirs, and an optional non-root `bypassPermissions` runner.

## Why it matters

- Claude subscription access should not be stranded outside your agent stack.
- ACP and third-party harnesses are not the same as a real local Claude worker lane.
- This gives OpenClaw operators a boring, reliable way to use Claude again.
- It installs fast and gives you a simple `claude-delegate` command to remember.

## Install CTAs

### OpenClaw-native

```bash
openclaw skills install openclaw-claude-delegate
```

### One-line installer

```bash
curl -fsSL https://raw.githubusercontent.com/StoicEnso/openclaw-claude-delegate/v0.2.6/install.sh | bash -s -- --version v0.2.6
```

## GitHub repo description

Lets any OpenClaw agent delegate into a locally authenticated Claude Code subscription lane, including a non-root bypassPermissions worker path.

## ClawHub listing copy

### Name
OpenClaw Claude Delegate

### Slug
openclaw-claude-delegate

### Summary
Give Claude back to OpenClaw through a local Claude Code delegation lane with monitoring, resume, and an optional non-root `bypassPermissions` worker path.

### Suggested tags
latest,openclaw,claude-code,delegation,automation,local-worker,bypasspermissions

### Changelog for v0.2.6
- fixed installer defaults to use modern `~/.agents/skills/claude-delegate` skill discovery
- made `setup.sh` use the same runner/OAuth environment as the real wrapper, avoiding false auth failures
- added adaptive runner detection: root+`/home/ccbot` uses `ccbot`, otherwise current-user Claude works out of the box
- added optional `--smoke` install flag for a live end-to-end scratch dispatch test
- forwarded `CLAUDE_CODE_OAUTH_TOKEN` into runner executions and normalized Claude model aliases

## X post

Claude got cut out of OpenClaw.

So I built **OpenClaw Claude Delegate**.

It gives any OpenClaw agent a real local Claude Code worker lane with:
- dispatch, poll, result, resume
- bounded workdirs
- optional non-root `bypassPermissions`

Install:
`openclaw skills install openclaw-claude-delegate`

Repo:
https://github.com/StoicEnso/openclaw-claude-delegate

## X thread

### Post 1
Claude got cut out of OpenClaw.

That sucked.

So I built **OpenClaw Claude Delegate** to put it back.

### Post 2
The problem:
- third-party harnesses do not reliably get Claude subscription access
- ACP is not the same thing as a real local Claude worker lane
- people still want Claude-quality work inside OpenClaw

### Post 3
What this gives you:
- a local Claude Code delegation lane
- dispatch, poll, result, and resume
- bounded workdirs
- optional non-root `bypassPermissions`
- cleaner separation from ACP/chat-thread flows

### Post 4
Fast install:
`openclaw skills install openclaw-claude-delegate`

Or:
`curl -fsSL https://raw.githubusercontent.com/StoicEnso/openclaw-claude-delegate/v0.2.6/install.sh | bash -s -- --version v0.2.6`

### Post 5
Repo:
https://github.com/StoicEnso/openclaw-claude-delegate

If Claude being cut out of your OpenClaw workflows annoyed you too, give it a star.

## Discord / ClawHub / forum post

**OpenClaw Claude Delegate: give Claude back to OpenClaw**

If you want Claude Code inside OpenClaw again, this is the clean local lane.

It gives you:
- dispatch, poll, result, and resume
- profile-based workdir scoping
- optional non-root `bypassPermissions`
- cleaner separation from ACP/chat-thread flows

Install:
- `openclaw skills install openclaw-claude-delegate`
- `curl -fsSL https://raw.githubusercontent.com/StoicEnso/openclaw-claude-delegate/v0.2.6/install.sh | bash -s -- --version v0.2.6`

Repo:
https://github.com/StoicEnso/openclaw-claude-delegate

## Hacker News style title ideas

- Show HN: OpenClaw Claude Delegate, a local Claude Code lane for OpenClaw agents
- Show HN: Give Claude back to OpenClaw
- Show HN: A local Claude Code delegation lane for OpenClaw
