---
name: one-person-company-os
description: Build and advance a visual operating cockpit for an AI-native one-person company inside Hermes Agent.
---

# One Person Company OS For Hermes Agent

Use this skill when the user wants Hermes to help run a one-person AI company with memory, tools, and repeatable operating discipline.

The visible loop is:

`promise -> buyer -> product capability -> delivery -> cash -> learning -> asset`

## Hermes-Specific Rules

- Load prior memory only as context; do not let self-improvement overwrite this core skill automatically.
- Propose skill improvements as patches and require founder approval before saving them.
- Prefer the MCP adapter for file-writing actions.
- Keep all persistent company files inside the founder-approved workspace.
- Record durable lessons in the generated workspace's collaboration memory, not in hidden global memory only.

## First Run

Clarify:

- sellable promise
- first buyer
- core problem
- current primary goal
- current bottleneck
- primary arena
- shortest action today
- approved workspace path

Then call the MCP `init_business` tool if configured.

## Safety

- Dangerous commands require approval.
- Pricing, launch claims, legal statements, budget changes, and customer-facing risk require founder approval.
- AI images are optional creative assets and must not carry exact operating numbers.
