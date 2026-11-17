## Description:

PropAI Sync helps agents maintain and operate the PropAI Sync monorepo, including BYOK API validation, hosted smoke checks, build gates, Railway deployment checks, and ClawHub publishing steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vishalgojha](https://clawhub.ai/user/vishalgojha)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to run scoped quality checks, build gates, hosted smoke tests, and Railway deployment validation for PropAI Sync releases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Deployment and login workflows may run with insufficient scoping or production credentials.

Mitigation: Review the skill before installing it in environments with Railway or production deployment credentials, require explicit approval before deployment steps, and use staging credentials by default.

Risk: The Railway CLI is invoked through an unpinned executable dependency.

Mitigation: Pin the Railway CLI version before running deployment validation in controlled environments.

Risk: Hosted smoke output can expose a literal API key prefix.

Mitigation: Record only whether an API key was received instead of printing any literal key prefix.

## Reference(s):

- [PropAI Sync ClawHub Skill Page](https://clawhub.ai/vishalgojha/skills/propai-sync)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON smoke-check summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include deployment validation steps and HANDOFF.md status entries.]

## Skill Version(s):

2026.2.28 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
