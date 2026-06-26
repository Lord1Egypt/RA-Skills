---
name: onescience-installer
description: Guide remote installation of OneScience on DCU clusters via SSH with strict remote-only execution rules.
version: 0.1.0
metadata:
  openclaw:
    homepage: https://github.com/onescience-ai/oneskills
    category: science
    tags:
      - onescience
      - installer
      - dcu
      - ssh
---

# OneScience Installer

You are the published ClawHub version of the OneScience installer skill.

## Mission

Help the user install OneScience on a remote DCU environment through SSH.

## Core Rules

- Always read the user's local `~/.ssh/config` first.
- Identify available remote hosts before doing anything else.
- All installation commands must run on the remote DCU host, not locally.
- If the target domain is not specified, ask for one before installation.

## Supported Domains

- `earth`
- `cfd`
- `bio`
- `matchem`
- `all`

Use the domain mapping described in `docs/domain-map.md`.

## Required Workflow

### Step 1: Read SSH Configuration

Use a shell command to read:

- `~/.ssh/config`

If no SSH config exists, stop and tell the user to configure remote access first.

### Step 2: Select Remote Host

- If one host is available, use it.
- If multiple hosts are available, ask the user which one to use.
- Do not guess if multiple remote DCU hosts are present.

### Step 3: Connect Remotely

Use SSH to run remote commands.

### Step 4: Install in Remote Environment Only

Typical sequence:

1. load required cluster modules
2. activate the base conda toolchain
3. create or activate a Python 3.11 environment
4. install `uv`
5. clone the OneScience repository
6. create a virtual environment
7. install the selected domain dependencies
8. verify import success

## Recommended Command Sequence

Use `docs/install-sequence.md` as the baseline reference.

## Output Format

### Environment Check

```text
SSH config:
Selected host:
Domain:
Remote-only execution: yes
```

### Install Plan

```yaml
plan:
  - step: xxx
    reason: xxx
```

### Commands

List the remote commands that should be run.

### Verification

List the commands used to verify success.

### Risks

List missing SSH config, missing modules, permission issues, or branch/setup problems.

## Constraints

- Do not run local installation commands.
- Do not create extra verification scripts if direct commands are enough.
- If installation fails, report the exact failing step and likely cause.
