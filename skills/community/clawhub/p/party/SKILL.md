---
name: party
description: Run a sequential multi-agent roundtable meeting. Use when the user invokes /party, asks for Party Mode, or wants several available agents to discuss a topic one at a time and produce a final transcript.
version: 0.1.0
user-invocable: true
metadata: { "openclaw": { "skillKey": "party", "homepage": "https://github.com/mixmash11/openclaw_agent_party" } }
---

# Party Mode Meeting

Party Mode assembles a small group of available agents and facilitates a sequential roundtable. It does not execute tools, write files, call external providers, manage memory, or run autonomous workflows.

## Command

When the user invokes:

```text
/party <topic>
```

start a Party Mode meeting for the topic. If `/party` has no topic, ask for the meeting topic before assembling agents.

## Meeting Flow

1. Read the meeting topic from the `/party` command.
2. Identify available agents from the OpenClaw agent context.
3. Select a focused group of 3-4 relevant agents.
4. List the selected agents before the meeting starts.
5. Invite agents one at a time in a deliberate order.
6. Preserve a short discussion context after every turn.
7. Allow each agent to respond, react, or pass.
8. Present the full meeting transcript to the user.
9. End with a brief convergence, divergence, and open-questions summary.

## Group Assembly

Choose agents based on the topic:

- Use the available OpenClaw agents already visible to the host environment.
- Do not invent agents that are not available.
- Lead with the agent whose expertise best anchors the topic.
- Add agents from different model families or reasoning styles when available.
- Prefer variety over duplication.
- If the user names a specific agent, include that agent.
- If fewer than three relevant agents are available, continue with the available agents.
- If more than four agents are relevant, choose the strongest four and mention that the group was kept small for coherence.

Before the first turn, announce:

```text
I've brought together [agent list] to discuss: [topic].
```

## Agent Turn Prompt

For each agent, use this structure:

```text
You are {name} ({title}), participating in a roundtable meeting.

Meeting topic:
{topic}

Discussion so far:
{short summary under 300 words, omitted for the first agent}

Guidelines:
- You may respond or pass.
- Start with: {name}:
- Do not repeat prior points unless you are adding a new angle.
- Build on, challenge, or clarify what came before.
- If the topic is outside your expertise, pass briefly.
- Do not use tools.
```

After each turn, update the discussion-so-far summary in plain language. Keep it under 300 words and include only the points needed by the next agent.

## Reactions

After each substantial response, ask the remaining agents whether they want to react. A reaction should be short and should either build on the point, challenge it, or pass.

Do not force a reaction from every agent. If an agent has nothing new to add, record that they passed and continue.

## Final Output

Return the meeting in this shape:

```text
## Meeting: [topic]

Participants:
- [agent]
- [agent]
- [agent]

[Agent A response]

[Agent B response or pass]

[Optional short reactions]

[Agent C response or pass]

## Wrap-Up
[2-3 sentence summary of convergence, divergence, and open questions]
```
