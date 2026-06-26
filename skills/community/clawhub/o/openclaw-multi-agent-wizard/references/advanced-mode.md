# Advanced Mode

This mode is explanation-first, warning-first.

## One-line explanation

- "A main assistant takes the task and can call other assistants to help during the run."

## Tiny example

- "The main assistant receives a weekly report task, then asks a data assistant and a writing assistant to help."

## Warning

Always include this or very similar wording:

- "This is an advanced setup. If you are still learning OpenClaw multi-agent basics, do not start here."

## What counts as advanced mode

- `sub-agents`
- `sessions_spawn`
- `sessions_send`
- agent-to-agent runtime collaboration
- broadcast-style multi-agent responses

## V1 behavior

For beginners:

- explain briefly
- recommend against enabling it now
- offer to come back later after the user understands the basic modes

If the user insists:

- prefer one main public agent plus background worker agents
- provide a skeleton plan or checklist
- avoid automatic configuration unless the user explicitly accepts the risk

## Things not to do in V1

- do not silently enable orchestration
- do not rewrite large config sections for orchestration
- do not mix advanced orchestration into a beginner wizard without clear consent
- do not treat "multiple public agents replying in the same Feishu group" as the default path
