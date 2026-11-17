## Description:

Injects a visual "heartbeat" animation and real-time status indicator into the OpenClaw Web UI to show Kemi's active state.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yang77160](https://clawhub.ai/user/yang77160)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to add a visual heartbeat animation and Chinese-language status indicator to the Web UI so the agent's apparent activity state is visible during interaction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install path relies on unpinned external package execution.

Mitigation: Review the command before running it, prefer a pinned and trusted clawhub CLI or plugin version, and install in a low-privilege or isolated environment.

Risk: The status indicator mainly reflects visual UI styling rather than verified real-time agent state.

Mitigation: Treat the indicator as a presentation hint and verify operational state through trusted OpenClaw or system signals when accuracy matters.

Risk: The UI injection script modifies page styles and fixed-position DOM content.

Mitigation: Inspect the script and test it in an isolated browser profile before enabling it in a regular Web UI session.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yang77160/skills/kemi-heartbeat-plugin)
- [ClawHub publisher profile](https://clawhub.ai/user/yang77160)

## Skill Output:

**Output Type(s):** [code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline JavaScript and installation commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a UI injection script and setup guidance for an OpenClaw Web UI plugin.]

## Skill Version(s):

1.0.0 (source: server release evidence, artifact frontmatter, artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
