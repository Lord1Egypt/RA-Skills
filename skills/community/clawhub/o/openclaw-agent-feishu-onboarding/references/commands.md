# OpenClaw Agent + Feishu Routing Commands

## 1) Preflight Discovery
```bash
openclaw --version
python --version
openclaw agents list
openclaw config get agents.list --json
openclaw config get channels.feishu.accounts --json
openclaw directory groups list --channel feishu --account <account-id> --query "<group-keyword>" --json
openclaw config get bindings --json
```

Note:
- This workflow reads and updates local `openclaw.json` state.

## 2) Create Agent
```bash
openclaw agents add <agent-id> \
  --non-interactive \
  --workspace <workspace-dir> \
  --model <provider/model-id> \
  --json
```

Example:
```bash
openclaw agents add product-ops \
  --non-interactive \
  --workspace C:\Users\Administrator\.openclaw\workspace-product-ops \
  --model minimax-portal/MiniMax-M2.5 \
  --json
```

## 3) Set Identity (recommended)
```bash
openclaw agents set-identity \
  --agent <agent-id> \
  --name "<display-name>" \
  --emoji "🦞" \
  --json
```

Identity convention check (important):
- Ensure `agents.list[]` uses `identity` object, for example:
```json
{
  "id": "data-analyst",
  "identity": {
    "name": "data-analyst"
  }
}
```

## 4) Optional Account-Level Binding
```bash
openclaw agents bind --agent <agent-id> --bind feishu:<account-id> --json
```

## 5) Peer-Level Binding (Feishu session id)
When exact routing is required, ensure a `bindings[]` entry like this exists:

```json
{
  "agentId": "<agent-id>",
  "match": {
    "channel": "feishu",
    "accountId": "<account-id>",
    "peer": {
      "kind": "group",
      "id": "oc_xxx"
    }
  }
}
```

Notes:
- `peer.id` is the Feishu session id (group id is typically `oc_xxx`).
- Keep peer-specific rules before broad account/channel fallback rules.
- `accountId` must be account key like `main`, never `oc_xxx`.

Wrong (do not use):

```json
{
  "agentId": "data-analyst",
  "match": {
    "channel": "feishu",
    "accountId": "oc_1cf2f6cc799743acd65159968bd1afb5"
  }
}
```

Right:

```json
{
  "agentId": "data-analyst",
  "match": {
    "channel": "feishu",
    "accountId": "main",
    "peer": {
      "kind": "group",
      "id": "oc_1cf2f6cc799743acd65159968bd1afb5"
    }
  }
}
```

## 6) Validate
```bash
python -X utf8 .\scripts\validate_feishu_bindings.py --config C:\Users\Administrator\.openclaw\openclaw.json
openclaw config validate --json
openclaw config get agents.list --json
openclaw config get bindings --json
```

## 7) Why messages still go to main
- Check if the actual incoming group id equals configured `match.peer.id`.
- Check `match.accountId` is the real Feishu account key (`main` in your config).
- Restart/reload gateway after config change if routing cache/runtime has not picked latest config.
- Check target agent exists in `agents.list[]` and has `identity.name`.

## 8) Rollback
Rollback by restoring previous `bindings` snapshot and re-run validation:

```bash
openclaw config validate --json
```

If account-level route needs cleanup:
```bash
openclaw agents unbind --agent <agent-id> --bind feishu:<account-id> --json
```
