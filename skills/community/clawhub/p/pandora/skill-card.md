## Description:

Pandora namespace for Netsnek e.U. secrets and configuration management vault. Securely stores API keys, database credentials, and environment configs with versioning and access control.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kleberbaum](https://clawhub.ai/user/kleberbaum)

### License/Terms of Use:

MIT

## Use Case:

Developers and operations teams use Pandora for proposed secrets and configuration management workflows such as storing, rotating, and listing credential keys.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release presents itself as a secure secrets vault, but evidence.security says the artifacts only include a placeholder command script and may make users believe secrets were stored or rotated when no vault action occurred.

Mitigation: Review carefully before installing and do not use this skill for real secrets unless the publisher implements real storage, encryption, listing, and rotation behavior with clear failures.

Risk: The documented command-line example could expose a secret value in shell history or process logs.

Mitigation: Avoid passing real secrets directly on the command line; require safe prompt-based or stdin input before handling production credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kleberbaum/skills/pandora)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The artifact declares Linux support and exec permission.]

## Skill Version(s):

0.1.0 (source: SKILL.md frontmatter, claw.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
