# Command Branches

Use these command branches as the practical backbone of the wizard. Prefer the simplest official path first.

## Local version note

The current local environment reported:

- `OpenClaw 2026.4.2`

The command examples below are aligned with the current official docs and should be treated as the preferred path. Still inspect local help when a command seems unavailable or behaves differently.

## Preflight commands

Good first checks:

```bash
openclaw --version
openclaw gateway status
openclaw agents list
openclaw logs --follow
```

If the gateway is not running:

```bash
openclaw gateway start
openclaw gateway status
```

If startup still looks wrong:

```bash
openclaw doctor
openclaw gateway restart
```

## Agent creation branch

Preferred official commands from the docs:

```bash
openclaw agents list
openclaw agents add work --workspace ~/.openclaw/workspace-work
openclaw agents bindings
openclaw agents delete work
```

Wizard behavior:

1. choose a safe agent ID
2. create the agent with an explicit workspace when possible
3. verify with `openclaw agents list`

### Identity branch

If you created `IDENTITY.md` in the workspace as part of the starter profile bundle, use the official identity flow:

```bash
openclaw agents set-identity --workspace ~/.openclaw/workspace --from-identity
```

If that flow is not convenient, use explicit fields:

```bash
openclaw agents set-identity --agent main --name "OpenClaw"
```

Recommended starter profile bundle in each new workspace:

- `IDENTITY.md`
- `SOUL.md`
- `AGENTS.md`
- `MEMORY.md`
- `TOOLS.md`
- `USER.md`

## Feishu channel branch

The official Feishu page recommends this as the main beginner path:

```bash
openclaw channels add
```

Wizard behavior:

1. ask the user to create the Feishu app
2. collect `App ID` and `App Secret`
3. use the official channel add flow when possible
4. verify with gateway status and logs

Useful follow-up commands:

```bash
openclaw gateway status
openclaw gateway restart
openclaw logs --follow
```

## Feishu config branch

If the CLI flow cannot express the needed account layout, patch config minimally.

The official docs show a shape like:

```json
{
  "channels": {
    "feishu": {
      "enabled": true,
      "dmPolicy": "pairing",
      "accounts": {
        "main": {
          "appId": "cli_xxx",
          "appSecret": "xxx",
          "botName": "My AI assistant"
        }
      }
    }
  }
}
```

For multiple accounts, the docs show:

```json
{
  "channels": {
    "feishu": {
      "defaultAccount": "main",
      "accounts": {
        "main": {
          "appId": "cli_xxx",
          "appSecret": "xxx",
          "botName": "Primary bot"
        },
        "backup": {
          "appId": "cli_yyy",
          "appSecret": "yyy",
          "botName": "Backup bot",
          "enabled": false
        }
      }
    }
  }
}
```

Use this shape as the safe fallback for `多 bot 多 agent`.

## Binding branch

Official docs for agent bindings show examples like:

```bash
openclaw agents bindings
openclaw agents bind --agent work --bind telegram:ops
openclaw agents unbind --agent work --bind telegram:ops
```

For the beginner wizard:

- use CLI bindings where they clearly fit
- use minimal config patching when peer-level Feishu routing is required

## Single-bot multi-agent branch

V1 supports only Feishu group routing.

The official Feishu docs show bindings like:

```json
{
  "bindings": [
    {
      "agentId": "clawd-xi",
      "match": {
        "channel": "feishu",
        "peer": { "kind": "group", "id": "oc_zzz" }
      }
    }
  ]
}
```

The docs also say Feishu group IDs look like `oc_xxx`, and the recommended lookup method is:

1. start the gateway
2. @mention the bot in the group
3. run `openclaw logs --follow`
4. look for `chat_id`

Wizard behavior:

- ask the user to send a test message in each target group
- inspect local logs yourself
- identify the `oc_xxx` group IDs
- patch only the new needed peer bindings

## Gateway restart branch

Use official commands:

```bash
openclaw gateway status
openclaw gateway restart
openclaw logs --follow
```

Prefer `openclaw gateway restart` over killing processes manually.

## Verification branch

After setup, run a small verification sweep:

```bash
openclaw gateway status
openclaw agents list
openclaw logs --follow
```

If the user says the bot does not reply:

- confirm the app was published
- confirm the bot is in the target group
- confirm the group sent a fresh message
- inspect logs for `chat_id`, Feishu inbound events, and reply attempts

## Pairing and IDs

The official Feishu docs note:

- group IDs look like `oc_xxx`
- user IDs look like `ou_xxx`

To inspect user IDs in DM flows:

```bash
openclaw pairing list feishu
```

In V1, keep this mainly for troubleshooting and for explaining advanced private-chat routing, not for the main setup path.

## A2A collaboration branch

For advanced A2A use cases, prefer:

- `sessions_spawn`
- `sub-agents`
- `sessions_send`

Recommended practical rule for Feishu:

- let one main agent remain the public speaker
- use worker agents only for background collaboration

Do not default to many agents publicly replying in the same Feishu group.
