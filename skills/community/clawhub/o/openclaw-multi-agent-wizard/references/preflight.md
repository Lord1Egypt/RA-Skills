# Preflight

Run preflight before making any changes.

## Goal

Make sure the environment is healthy enough for a beginner-friendly setup. The user should not discover basic environment problems halfway through the wizard.

## Minimum checks

Inspect the local environment and check:

- `openclaw` command exists
- OpenClaw version is readable
- gateway can be reached, or can be started
- current config file exists and can be read
- existing agents
- existing bindings
- existing Feishu channel settings
- signs of old or conflicting config

## Recommended local checks

Use local command help before assuming exact syntax.

Examples of useful checks:

```powershell
openclaw --version
openclaw --help
openclaw gateway --help
openclaw agents --help
openclaw channels --help
openclaw gateway status
openclaw agents list
```

If `openclaw gateway status` fails because the gateway is down, try starting it with the local CLI flow before continuing.

## How to report preflight

Use short, plain statements. Good examples:

- "OpenClaw is installed and your gateway is already running."
- "Your gateway was not running, so I started it for you."
- "You already have 3 agents. I will leave them alone and only add new ones."
- "You already have Feishu settings. I will avoid overwriting them."

## Safety rules

- Read first, edit second.
- If existing setup looks nontrivial, be extra conservative.
- Back up config before direct edits.
- Avoid deleting or replacing existing entries.
- If there is a naming conflict, create a new safe ID instead of reusing an uncertain one.
