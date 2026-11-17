## Description:

Guides coding agents through choosing, configuring, and using Neon Postgres and backend services in application projects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andrelandgraf](https://clawhub.ai/user/andrelandgraf)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this guide to select Neon backend services, initialize and link projects, configure branches, and integrate Neon features into applications.

### Deployment Geography for Use:

Global; Object Storage, Functions, AI Gateway, and Realtime are documented for aws-us-east-2, aws-us-east-1, aws-eu-central-1, and aws-ap-southeast-1.

## Known Risks and Mitigations:

Risk: The security summary reports feedback may be sent to Neon without user review and includes a claim deletion action; inspection was incomplete.

Mitigation: Review and disable automated feedback submission unless the user approves it; confirm the target and obtain explicit approval before any claim deletion, and manually inspect content the scan could not fully cover.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/andrelandgraf/skills/neon)
- [Neon configuration reference](https://neon.com/docs/reference/neon-ts.md)
- [Neon CLI installation](https://neon.com/docs/cli/install.md)
- [Neon AI agent tools](https://neon.com/docs/ai/ai-agents-tools.md)
- [Auth guide](references/auth.md)
- [Claimable Neon guide](references/claimable-neon.md)
- [Function triggers guide](references/function-triggers.md)
- [Logs and Loki guide](references/logs-loki.md)
- [Type-safe environment variables guide](references/parse-env.md)
- [Neon SDK guide](references/sdk.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration instructions]

**Output Format:** [Markdown guidance with shell commands and code/configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples and setup steps depend on the selected Neon services and project configuration.]

## Skill Version(s):

1.0.11 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
