## Description:

Guides agents through installing, verifying, and starting OpenClaw with practical cost and security cautions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dox012](https://clawhub.ai/user/dox012)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to get OpenClaw installation, verification, gateway, and dashboard startup guidance, including reminders about billing and deployment exposure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends global npm installation commands for OpenClaw packages.

Mitigation: Check the npm package page, source repository, publisher, and exact version before installing; avoid sudo for global installs where possible.

Risk: Starting gateway or dashboard services without secure settings could expose them publicly.

Mitigation: Keep services on trusted networks unless access controls, authentication, and other security settings are configured.

Risk: OpenClaw usage can incur API or token costs during agent activity.

Mitigation: Use budget controls, lower-cost models where appropriate, spending limits, and regular billing reviews.

## Reference(s):

- [OpenClaw Documentation](https://docs.openclaw.ai/)
- [OpenClaw Installation Guide](https://docs.openclaw.ai/install)
- [OpenClaw GitHub Repository](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes installation, verification, service startup, cost-awareness, and basic security guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
