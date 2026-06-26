# Routing Basics

This file defines the only two V1 routing patterns that should be configured automatically.

## Pattern A: `多 bot 多 agent`

Meaning:

- one Feishu bot account per agent
- one clean mapping from that bot account to that agent

Explain it simply:

- "Each robot talks to exactly one assistant."

Preferred implementation strategy:

1. create or confirm each agent
2. create or confirm each Feishu account
3. bind each Feishu account to exactly one agent
4. verify the mapping

For beginners with many bots:

5. finish one bot end-to-end before configuring the next bot

Best for:

- beginners
- clear separation
- minimal confusion

Simple explanation for the user:

- "Robot A always talks to Assistant A. Robot B always talks to Assistant B."

## Pattern B: `单 bot 多 agent`

Meaning:

- one Feishu bot
- multiple agents behind it
- split only by group chat in V1

Explain it simply:

- "One robot, different assistant brains in different Feishu groups."

Preferred implementation strategy:

1. create or confirm the shared Feishu bot
2. add the bot to each target Feishu group
3. ask the user to send a message in each group
4. inspect local logs or OpenClaw state to identify the groups
5. bind each group target to one agent
6. verify each binding

Simple explanation for the user:

- "The same robot stays in multiple groups, but each group is handled by its own assistant."

For high success in V1:

- start with one group first
- verify that group works
- only then add the next group

## Important V1 restriction

Do not auto-configure private-chat routing.

If the user asks for private-chat routing:

- say it is an advanced option
- explain that V1 only supports group-based routing for simplicity and reliability

Suggested wording:

- "Private-chat splitting is possible in OpenClaw, but it is easier to get wrong. This first version only supports splitting by group."

## Editing rules

- Prefer official OpenClaw CLI commands.
- If exact CLI coverage is missing, patch config minimally.
- Preserve existing bindings whenever possible.
- Never replace unrelated bindings.
