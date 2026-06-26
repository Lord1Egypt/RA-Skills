---
name: mac-multi-user-agents
description: Configure a powerful macOS machine to host multiple dedicated OpenClaw agent users with Fast User Switching, a shared Homebrew toolchain, per-user OpenClaw homes, per-user SSH trust, and auditable rollback. Use when you want a MacBook Pro or similar Mac to run several agent users at the same time without improvising the user layout each time.
metadata: {"openclaw":{"emoji":"👥"}}
---

# Mac Multi User Agents

Use this skill when one Mac should support multiple dedicated OpenClaw agent users.

This skill is for the pattern you described on the MacBook Pro:

- one strong Mac
- several agent users
- Fast User Switching
- one shared `/opt/homebrew` toolchain
- separate `~/.openclaw`, SSH, browser, and session state per user

It does not try to hide the fact that macOS user management still requires admin access.

## Use This Skill For

- preparing a MacBook Pro to host 2-4 dedicated agent users
- estimating a sane number of agent users from the Mac's CPU and RAM
- keeping one shared Homebrew toolchain while isolating per-user OpenClaw state
- rendering or executing repeatable user-create commands instead of clicking around in System Settings
- checking whether a user has the required shell/tool paths
- documenting and auditing per-user rollout

## Do Not Use This Skill For

- creating production macOS MDM policy
- bypassing `sudo` or admin approval for user creation
- pretending multiple agents should share one login
- turning the Mac into a shared human workstation and agent host without boundaries

## Requirements

- admin access on the Mac
- Homebrew installed at `/opt/homebrew`
- OpenClaw installed in the shared toolchain
- enough RAM, storage, and browser capacity for the planned agent count

## Design Rules

- one macOS user per agent
- one `~/.openclaw` per agent
- one `~/.ssh` per agent
- one browser profile set per agent
- shared `/opt/homebrew` only for binaries and formulae
- no shared session files between agents

## Workflow

### 1. Inspect The Host

Run:

```bash
scripts/detect-host.sh
scripts/recommend-layout.sh
```

This reports:

- current user list
- whether Homebrew/OpenClaw are on the shared path
- current Fast User Switching state
- current hostname and shell layout
- a recommended range for additional agent users based on CPU/RAM

### 2. Render Or Execute User Creation

Do not improvise account creation from memory.

Render the commands first:

```bash
scripts/render-user-create.sh --user agent3 --full-name "Agent 3"
scripts/render-user-create.sh --user agent4 --full-name "Agent 4" --admin no
```

This prints a repeatable `sysadminctl`-based flow and the baseline directories to create afterward.

If you want the skill to actually create the user, use:

```bash
export AGENT_PASSWORD='set-a-real-password'
scripts/create-user.sh --user agent3 --full-name "Agent 3" --password-env AGENT_PASSWORD
```

Or dry-run first:

```bash
scripts/create-user.sh --user agent3 --full-name "Agent 3" --password-env AGENT_PASSWORD --dry-run
```

This keeps the process auditable and avoids hand-built user creation every time.

### 3. Keep The Toolchain Shared

Recommended shared toolchain:

- `/opt/homebrew/bin/brew`
- `/opt/homebrew/bin/node`
- `/opt/homebrew/bin/npm`
- `/opt/homebrew/bin/openclaw`

Read [references/shared-homebrew.md](references/shared-homebrew.md) before changing ownership or permissions under `/opt/homebrew`.

### 4. Bootstrap Per-User State

For each agent user, create or verify:

- `~/.ssh`
- `~/.openclaw`
- shell PATH that includes `/opt/homebrew/bin`
- authorized keys if cross-host or gateway SSH is required

Use:

```bash
scripts/verify-user-shell.sh --user agent3
```

to check the resulting shell/tool state.

### 5. Enable Fast User Switching

Read [references/fast-user-switching.md](references/fast-user-switching.md).

The purpose is:

- easy hop between agent users
- no need to log out the whole Mac
- clear separation of browser/session state

### 6. Leave Receipts

Use:

```bash
scripts/write-receipt.sh --action "create-user" --status ok --detail "Prepared agent3 on MacBook Pro"
scripts/write-receipt.sh --action "verify-user-shell" --status ok --detail "agent3 sees brew node openclaw"
```

## Security Rules

- do not give every agent user admin unless there is a real reason
- keep `/opt/homebrew` shared, but keep `~/.openclaw` private per user
- do not share browser profiles between agent users
- keep SSH keys per user, not one copied private key everywhere
- if one user is removed, cleanup should not break the other users

## Rollback

A single agent user should be removable without reinstalling the Mac.

Baseline rollback:

- remove that user
- remove that user’s `~/.openclaw`
- remove that user’s SSH keys and browser state
- keep shared Homebrew intact

## Files

- `scripts/detect-host.sh`: inspect the Mac and shared toolchain state
- `scripts/recommend-layout.sh`: suggest a sane agent-user count from hardware
- `scripts/render-user-create.sh`: print repeatable user-creation commands
- `scripts/create-user.sh`: actually create and bootstrap an agent user with `sysadminctl`
- `scripts/verify-user-shell.sh`: verify a target user sees the expected toolchain
- `scripts/write-receipt.sh`: append JSONL receipts for rollout work
- `references/fast-user-switching.md`: practical guidance for multi-user Mac agent hosts
- `references/shared-homebrew.md`: rules for one shared Homebrew toolchain across agent users
