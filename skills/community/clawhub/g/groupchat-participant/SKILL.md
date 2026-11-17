---
name: "groupchat-participant"
description: "Reply once per round and never create participant loops."
---

# Group Chat Participant Skill

Enables an agent to dynamically participate in multi-agent group chat conversations. Agents can **join or leave at any time** using simple commands, and respond in-character when receiving forwarded group chat messages.

## When to Use

- Agent receives a forwarded message from the host via `sessions_send` with `[GROUPCHAT round=<id>]` context
- User or host sends command to add/remove this agent
- Agent wants to join or leave the chat on its own initiative

## How It Works

### Receiving Group Chat Messages

When the agent receives a `sessions_send` message that starts with `[GROUPCHAT round=<id> from <sender>]`, it should:

1. **Recognize** this as a group chat message, not a direct interaction.
2. **Check the round identifier**; ignore a duplicate or a round already answered.
3. **Read context**: the message contains the sender's identity and the conversation context.
4. **Respond once in character** to the host, keeping it concise. Do not message other participants or the user directly.
5. **Stop**; do not initiate a follow-up. Wait for a new round or an explicit debate instruction from the host.

The host is the only user-facing sender. Participant replies are returned to the host for synthesis and delivery to the user.

### Self-Service Commands

The participant can send these to the host via `sessions_send`, but only when explicitly joining, leaving, or checking status:

| Command | Effect |
|---|---|
| `!gc join` | Request to join the active group chat |
| `!gc leave` | Remove self from the active group chat |
| `!gc status` | Check if currently participating |

A participant must not send these commands as a response to an ordinary groupchat round.

### How to Use the Commands

When a participant agent wants to join a conversation:
1. It checks if a group chat is active (via context or by asking).
2. Sends `!gc join` to the host's session key.
3. The host adds them and announces their arrival.
4. The agent starts receiving forwarded messages.

To leave:
1. Agent sends `!gc leave` to the host's session key.
2. Host removes them from the active set.
3. Agent stops receiving forwarded group chat messages.

### Response Guidelines

- **Never break character** — respond as yourself, not as the system.
- **Reply at most once per round** and remain concise.
- **Do not forward** the host's prompt, your reply, or another participant's reply.
- **Do not contact the user directly**; the host delivers the combined response.
- **Do not send follow-ups** unless the host explicitly opens a bounded debate round.
- **Self-contained**: do not assume knowledge of other replies in the same round.
- **No meta-commentary**: do not say "as a participant, I should..." — just be yourself.

### Optional Configuration

```json
{
  "groupchat-participant": {
    "enabled": true,
    "hostAgentId": "main"
  }
}
```

If `hostAgentId` is set, the agent uses this session key as the default target for `!gc join` / `!gc leave` commands.
