## Description:

Provides a documentation-only reference process for converting GitHub projects into OpenClaw skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jijinbao-code](https://clawhub.ai/user/jijinbao-code)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill authors use this reference guide to evaluate GitHub projects, plan OpenClaw skill structure, handle dependencies, and check safety and licensing considerations before manually creating a skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Converted third-party GitHub projects may include secrets, keys, or environment files if users package source material without review.

Mitigation: Review the source project before packaging and exclude .env files, keys, certificates, credentials, secrets, node_modules, and version-control directories.

Risk: Converted projects may carry license or dependency obligations that are not obvious from the reference guide alone.

Mitigation: Verify the source project's license, dependency trustworthiness, and dependency conflicts before creating or releasing a derived skill.

## Reference(s):

- [Github To Skill listing](https://clawhub.ai/jijinbao-code/skills/github-to-skill)
- [OpenClaw Skill Specification](https://agentskills.io/specification)
- [OpenClaw documentation](https://docs.openclaw.ai)
- [ClawHub skill marketplace](https://clawhub.ai)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration]

**Output Format:** [Markdown reference guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only; no executable code or automated runtime behavior is included.]

## Skill Version(s):

2.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
