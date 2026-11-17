## Description:

Controls a Minecraft bot through the Mindcraft HTTP API without a built-in LLM, guiding external agents through status reads, action schema lookup, action execution, and task orchestration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[songjc0511](https://clawhub.ai/user/songjc0511)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation engineers use this skill to operate a local Mindcraft or Minecraft bot from OpenClaw or another external controller through REST API calls. It helps them discover connected agents, inspect action schemas, execute actions, verify state changes, and recover from failed or stuck actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automated actions can affect a local Minecraft world or a shared world connected to the Mindcraft bot.

Mitigation: Use the skill first in a private or local world, confirm the API binding, and review planned actions before allowing automation in shared worlds.

Risk: Incorrect parameters or long action chains can leave the bot in an unexpected state.

Mitigation: Fetch the action schema before execution, run actions in small steps, read state after each action, and use the stop command before recovery actions when needed.

## Reference(s):

- [OpenClaw Call Reference](artifact/reference.md)
- [Call Examples](artifact/examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with REST API endpoints, JSON payloads, PowerShell commands, and Python code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommends recording request and response payloads plus before-and-after state snapshots for each action.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
