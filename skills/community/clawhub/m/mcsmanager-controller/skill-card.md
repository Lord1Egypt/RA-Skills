## Description:

Control and troubleshoot MCSManager-managed Minecraft servers through the MCSManager API and clearly provided host-side context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[szabee13](https://clawhub.ai/user/szabee13)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and server administrators use this skill to inspect, troubleshoot, and control Minecraft servers managed through MCSManager. It supports status checks, log review, console commands, and requested lifecycle actions such as start, stop, restart, or kill when the user provides the required configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can administer a Minecraft server through MCSManager, including state-changing actions such as stop, kill, plugin actions, and console commands.

Mitigation: Review state-changing commands before allowing them unless they were explicitly requested, and prefer read-only status and log checks before making changes.

Risk: MCSManager API credentials can grant control over the configured server instance.

Mitigation: Only provide credentials for servers the agent should administer, keep real config.json files private and untracked, and use intentionally configured local credentials only.

Risk: Incorrect or assumed API endpoints, instance UUIDs, or daemon identifiers could target the wrong server or fail unpredictably.

Mitigation: Require explicit user-provided configuration, confirm the target instance before action, and adapt to the installed MCSManager version when API details differ.

## Reference(s):

- [MCSManager API notes](references/api-notes.md)
- [MCSManager Controller on ClawHub](https://clawhub.ai/szabee13/skills/mcsmanager-controller)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with command snippets, configuration guidance, and concise status or troubleshooting reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May request explicit MCSManager connection details before taking action; uses user-provided or intentionally configured local credentials only.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
