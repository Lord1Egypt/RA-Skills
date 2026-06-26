# Modes

Use these exact simple explanations or wording very close to them.

## Mode 1: `多 bot 多 agent`

Big-picture explanation:

- "Each robot has its own assistant brain. They do not interfere with each other."

Tiny example:

- "Your work bot uses the work assistant. Your life bot uses the life assistant."

When to recommend:

- first-time beginners
- users who want the safest setup
- users who want very clear separation

Default recommendation line:

- "If you are new, I recommend this one first. It is the easiest to understand and the hardest to mess up."

## Mode 2: `单 bot 多 agent`

Big-picture explanation:

- "From the outside it looks like one robot, but inside it uses different assistants for different Feishu groups."

Tiny example:

- "In the product group it behaves like the product assistant. In the engineering group it behaves like the engineering assistant."

Important V1 restriction:

- support only group-based routing
- do not offer private-chat routing in V1

When to recommend:

- users who want one unified Feishu bot
- users who are okay with different groups using different assistants

Default recommendation line:

- "This is good if you want one robot entry point, but we will keep it simple and only split by group."

## Mode 3: A2A collaboration

Big-picture explanation:

- "One main assistant takes the task, then asks other assistants to help behind the scenes."

Tiny example:

- "The main assistant receives a report task, then asks a data assistant to gather numbers and a writing assistant to polish the final text."

Warning line:

- "This is an advanced mode. If you are brand new to OpenClaw, do not start here."

When to discuss:

- only if the user explicitly asks for agent-to-agent collaboration
- only if the user wants sub-agents or runtime orchestration

Default advanced recommendation:

- "If you really need collaboration, the safest version is one main assistant replying in Feishu while the other assistants help in the background."

## Experimental mode: same-group public multi-agent replies

Big-picture explanation:

- "Multiple assistants all speak publicly in the same group."

Warning line:

- "This is experimental and not the recommended Feishu path for beginners."

How to describe it:

- "It can look exciting, but it is much easier to make noisy or confusing."
