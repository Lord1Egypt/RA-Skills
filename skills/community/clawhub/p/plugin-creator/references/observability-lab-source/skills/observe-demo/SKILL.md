---
name: observe-demo
description: Built-in Observability Lab demo skill used to verify that a plugin-shipped skill can guide the agent to call its tool correctly.
user-invocable: true
---

# Observe Demo

Use this skill when the user wants to verify that a plugin-shipped skill really loads and that the agent can call the expected tool because of the skill.

## What this skill demonstrates

- the skill is packaged with an OpenClaw plugin
- it automatically gets the `/observe_demo` command entrypoint
- it does not directly map the slash command to a tool
- the agent should read the skill first and then decide to call the tool

## Execution requirements

You must call the `observe_demo_echo` tool first, then produce the final reply from the tool result.

When calling the tool:

- use `observe_demo` for `commandName`
- use `observe-demo` for `skillName`
- use the user's raw text as `command`

## Final reply requirements

The final reply should be short and must include at least:

1. plugin id `observability-lab`
2. skill name `observe-demo`
3. the user's original input
4. a note that the result came from the agent proactively calling the tool under skill guidance
