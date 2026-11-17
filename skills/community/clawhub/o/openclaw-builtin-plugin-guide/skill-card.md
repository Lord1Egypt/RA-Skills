## Description:

This skill helps Chinese-speaking OpenClaw users list bundled plugins, view enabled or disabled plugin status, and inspect individual plugin details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[henryczq](https://clawhub.ai/user/henryczq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to understand OpenClaw built-in plugins, check which plugins are enabled or disabled in the current environment, and inspect details for a named plugin.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can reveal local OpenClaw plugin inventory, enabled or disabled status, capabilities, and documentation excerpts to the agent.

Mitigation: Use it only in workspaces where the agent is allowed to inspect local OpenClaw plugin configuration and avoid sharing generated inventory outside authorized contexts.

Risk: Plugin status and inspection commands depend on the locally installed OpenClaw CLI and current workspace state.

Mitigation: Confirm the `openclaw` and `python` binaries are available before relying on status or inspection output.

## Reference(s):

- [OpenClaw built-in plugin reference](artifact/references/builtin-plugins.md)
- [ClawHub skill page](https://clawhub.ai/henryczq/skills/openclaw-builtin-plugin-guide)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local OpenClaw plugin inventory, status, capability, and documentation excerpts.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
