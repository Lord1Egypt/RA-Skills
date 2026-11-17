## Description:

Use GitHub Copilot as your OpenClaw coding agent via the built-in copilot-bridge.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yanglinzhen](https://clawhub.ai/user/yanglinzhen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure GitHub Copilot as the OpenClaw default coding model, diagnose model availability, auth, alias, and session issues, and get exact OpenClaw commands for setup or activation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The activation flow can change the OpenClaw default model to GitHub Copilot.

Mitigation: Review the current model status and the target model before running activation commands.

Risk: Alias repair can add or update the copilot-auto alias.

Mitigation: Use alias changes only when desired and review the exact alias mapping before using --ensure-alias.

Risk: GitHub Copilot login may require an interactive device-code or browser step.

Mitigation: Run login only in a trusted interactive terminal and use the official OpenClaw GitHub Copilot auth flow.

## Reference(s):

- [OpenClaw CLI Models Documentation](https://docs.openclaw.ai/cli/models)
- [ClawHub Skill Page](https://clawhub.ai/yanglinzhen/skills/openclaw-github-copilot)
- [Setup Guide](references/setup-guide.md)
- [Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend interactive GitHub Copilot login and OpenClaw default model changes.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
