# Routing Modes Reference

Use this reference when selecting routing strategy for a new OpenClaw agent.

Scope of this skill: Feishu channel only.

## 1) `routing-mode=account`

Use when each agent maps to a dedicated bot/account.

Expected binding shape:

```json
{
  "agentId": "coding",
  "match": {
    "channel": "feishu",
    "accountId": "coding"
  }
}
```

Required `session.dmScope`: `per-account-channel-peer`

Account config location:
- `channels.feishu.accounts.<accountId>`

Typical fields:
- `appId`
- `appSecret`
- `botName`

## 2) `routing-mode=peer`

Use when one bot serves multiple groups/users, and route by peer id.

Expected binding shape:

```json
{
  "agentId": "dev-agent",
  "match": {
    "channel": "feishu",
    "peer": {
      "kind": "group",
      "id": "oc_dev_group_xxx"
    }
  }
}
```

Required `session.dmScope`: `per-account-channel-peer`

Optional narrowing:
- include `accountId` in `match` if the channel has multiple accounts.

## Route Conflict Rule

Reject creation when the same route is already bound to another agent:
- same `channel`
- same `accountId` (or both missing)
- same `peer.kind` + `peer.id` (or both missing)

Resolve by changing `accountId` or `peer.id`, or by removing the old conflicting binding first.
