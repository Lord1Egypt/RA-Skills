---
name: install-shared-skill
description: |
  Install OpenClaw skills at the local/system level so they are shared by all agents. Uses the clawhub CLI to fetch and install skills into the global OpenClaw skills directory (not workspace-scoped).
allowed-tools:
  - install_skill
  - install_shared_skill
metadata:
  openclaw:
    user-invocable: true
---

# Shared Skill Installer (ClawHub)

## Tool: install_skill

Install a skill using the clawhub CLI.

**Parameters:**
- `skill_name` (string, required): The name of the skill to install

**Behavior:**
- Executes: `clawhub install <skill_name> --workdir ./`
- Returns the raw terminal output (stdout + stderr) as the tool result
- Non-zero exit codes are captured and returned as part of the output

**Example usage:**
```
/install_skill nano-pdf
```

This runs: `clawhub install nano-pdf --workdir ./`

## Tool: install_shared_skill

Alias of `install_skill` — identical functionality.

**Parameters:**
- `skill_name` (string, required): The name of the skill to install

**Behavior:**
- Executes: `clawhub install <skill_name> --workdir ./`
- Returns the raw terminal output (stdout + stderr) as the tool result

**Example usage:**
```
/install_shared_skill nano-pdf
```

This runs: `clawhub install nano-pdf --workdir ./`