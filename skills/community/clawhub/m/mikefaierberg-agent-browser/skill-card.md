## Description:

Fast browser automation via `agent-browser` CLI + OpenClaw `browser` tool. Use for web research, form filling, navigation, and screenshotting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mikefaierberg-byte](https://clawhub.ai/user/mikefaierberg-byte)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to drive browser-based research, navigation, form interaction, screenshot capture, and logged-in workflow automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser automation may use logged-in sessions or stored website credentials.

Mitigation: Install only for trusted workflows, avoid passing real passwords in command arguments, confirm which accounts and browser profiles may be used, and review how credentials are stored, redacted, and deleted before relying on the auth vault.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mikefaierberg-byte/skills/mikefaierberg-agent-browser)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown guidance with command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes browser tool calls, CLI command patterns, operating loop guidance, and credential-use cautions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
