# A2A Collaboration Mode

Use this file when the user asks for agent-to-agent collaboration, sub-agents, or "多个 agent 一起完成同一个任务".

## Beginner explanation

Use one short explanation:

- "On the outside, one main assistant still replies to you. Behind the scenes, it can ask other assistants to help."

## Tiny example

- "The main assistant receives a weekly report task, then asks a data assistant to gather numbers and a writing assistant to polish the final answer."

## Default design rule

For Feishu, the recommended A2A pattern is:

- one main agent talks to the group
- worker agents help in the background
- the main agent sends the final reply

This is the recommended default because it is clearer, quieter, and easier to control.

## Recommended structure

### Main agent

The main agent should:

- receive the user message
- decide whether collaboration is needed
- call worker agents when useful
- merge the results
- send the final reply

### Worker agents

Worker agents should:

- specialize in one kind of work
- return focused results
- avoid acting like public-facing bots
- use a short, role-shaped starter persona when the name is obvious
- get the full starter profile files so their role, memory, tools, and collaboration boundaries are clear

## Good beginner scenarios

Use this mode for tasks like:

- weekly reports
- project review summaries
- product plus engineering discussions
- data collection plus writing tasks
- one main assistant coordinating specialist assistants

## What not to promise

Do not imply that multiple agents will all speak publicly in the same Feishu group by default.

Do not frame public same-group multi-agent chatter as the normal path.

## Experimental boundary

Treat this as experimental and not the default skill path:

- multiple agents publicly replying in the same Feishu group

If the user asks for it, explain:

- "OpenClaw does have advanced multi-agent and broadcast-style capabilities, but for Feishu the safer recommended setup is still one main public agent plus background helpers."

## Suggested setup flow

When the user insists on A2A mode, keep the flow simple:

1. choose the main agent
2. choose one or two worker agents
3. define each worker's role in plain language
4. explain that only the main agent will reply in Feishu
5. create a skeleton plan or lightweight conventions

## Suggested plain-language role prompts

Main agent:

- "You talk to the user directly and coordinate the other assistants when needed."

Data worker:

- "You help gather numbers, facts, and structured findings for the main assistant."

Writing worker:

- "You help improve clarity, structure, and wording for the main assistant."

Project worker:

- "You help track progress, organize owners, and keep next steps clear for the main assistant."

Research worker:

- "You help collect background information, compare findings, and return concise notes for the main assistant."

Technical worker:

- "You help with technical checks, implementation details, and debugging input for the main assistant."
