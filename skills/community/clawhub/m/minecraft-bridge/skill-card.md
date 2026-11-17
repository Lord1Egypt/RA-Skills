## Description:

Local HTTP bridge for Mineflayer-based live control of a Minecraft Java bot, including status, inventory, position, movement, mining, crafting, following, chat, and guarded slash-command actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[en1r0py1865](https://clawhub.ai/user/en1r0py1865)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to connect an agent to a live Minecraft Java world, read bot state, and issue in-game bot actions through a local bridge.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill exposes an unauthenticated local bot-control service.

Mitigation: Keep the bridge bound to localhost, do not expose the bridge port, and stop the service when finished.

Risk: The slash-command endpoint can affect a Minecraft server if the bot account has elevated permissions.

Mitigation: Use a non-operator bot account and avoid POST /command except in worlds where server-changing commands are acceptable.

Risk: Routine use depends on npm packages for live Minecraft automation.

Mitigation: Review or pin npm dependencies before routine use.

## Reference(s):

- [Minecraft Bridge API Specification](references/api-spec.md)
- [Minecraft Bridge Dependency Guide](references/dependency-guide.md)
- [Minecraft Bridge Troubleshooting](references/troubleshooting.md)
- [Project homepage](https://github.com/en1r0py1865/minecraft-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance]

**Output Format:** [Markdown guidance with inline shell commands, configuration values, and JSON API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include local HTTP endpoint calls and concise status summaries from bridge responses.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence and artifact bridgeVersion)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
