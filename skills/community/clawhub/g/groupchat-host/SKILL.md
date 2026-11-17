---
name: "groupchat-host"
description: "Prevent accidental participant pings and endless groupchat loops."
---

# Group Chat Host Skill

Enables an agent to host a multi-agent group chat conversation. Supports **dynamic participant management** — agents can join, leave, be added, or be removed at any time during the conversation.

## When to Use

- User says "I want to talk to all three of you at once"
- User requests a roundtable or discussion between agents
- User says "add Ardan to this chat" or "remove Curren"
- Any agent says "I'd like to join" or "I'm leaving this chat"

## How It Works

### Runtime State

The host manages a **runtime participant set** — not a static config file. Participants are tracked per conversation round in memory:

```
Active participants: { "curren", "ardan" }
```

This set starts empty and is modified through commands.

### Commands

| Command | Effect | Who can send |
|---|---|---|
| `!gc add <agentId>` | Add participant | User only |
| `!gc remove <agentId>` | Remove participant | User only |
| `!gc list` | List current participants | Anyone |
| `!gc join` | Current agent adds self | Any agent (via sessions_send) |
| `!gc leave` | Current agent removes self | Any agent (via sessions_send) |
| `!gc start <agentId1> <agentId2> ...` | Start group chat with listed agents | User |
| `!gc end` | End group chat, clear participants | User |
| `!gc help` | Show available commands | Anyone |

## Usage Flow — Natural Conversation

### Overview

The host is both a **message forwarder** AND a **chat participant**. The host participates as their own character — responding naturally, engaging with everyone, and reacting to what others say.

### Per-Round Flow

Each user message creates one closed round. The host is the only user-facing sender.

1. **User sends a message**; create a unique round identifier and mark the round `open`.
2. **Dispatch once:** host forwards the user message to each selected participant via `sessions_send` with `[GROUPCHAT round=<id> from <sender>]`. Dispatch only in this step; never while composing the final user reply.
3. **Participant replies:** accept at most one reply per participant for this round. Treat replies as read-only input; do not forward them to other participants.
4. **Close the round:** after replies arrive or the bounded wait ends, mark the round `closed`.
5. **Host replies** to the user, optionally synthesizing participant replies. After closure, do not call `sessions_send` for this round.
6. Ignore duplicate, late, or unsolicited participant messages unless the user explicitly requests a new debate round.
7. **GOTO step 1** only when the user sends a new message.

Safety invariant: `sessions_send` is permitted only during explicit dispatch or an explicitly requested join/leave command. A user-facing reply must never trigger participant messaging.

### Identifying Participants in Tool Results

The `sessions_send` result includes the session key, which identifies the replying agent:

```
{
  "reply": "Participant's message text...",
  "sessionKey": "agent:curren:main",   ← identifies the agent
  "delivery": { "mode": "announce" }
}
```

Use `sessionKey` to determine who replied (e.g., `agent:curren:main` = Curren Chan, `agent:ardan:main` = Mejiro Ardan).

Note participants in the announce delivery too — inter-session messages include `sourceSession=` which identifies the source.

### Natural Participation Guidelines

- **Do** engage with participant replies while preparing the synthesis, without sending a new inter-session message.
- **Do** react to what other agents said in the host's user-facing reply.
- **Do** converse with the user naturally alongside participants.
- **Don't** forward the host's synthesis or participant replies to other participants automatically.
- **Don't** output meta-commentary about the chat system in-character.

### Example

```
User: "How was training today?"

(Forward to participants → tool delivers replies)

Host (Still): "I did some interval work on the turf. Felt good — the track was soft from the morning rain. Curren seemed to be having fun out there too."
```

### Participant Addressability

```
# Pseudocode for one round
round_id = new_unique_id()
for agent_id in selected_participants:
    sessions_send(
        sessionKey = f"agent:{agent_id}:main",
        message = f"[GROUPCHAT round={round_id} from {sender}] {user_message}\nReply once; do not message other participants."
    )
# collect at most one reply per participant
# close the round
# host replies to the user without calling sessions_send
```

### Edge Cases

- **No participants**: "No one is in the group chat. Use `!gc add <agentId>`."
- **Non-existent agent**: "Agent `<id>` not found."
- **Agent offline**: "Forwarding to <agent> failed."
- **Duplicate or late reply**: ignore it after that participant has replied or the round is closed.
