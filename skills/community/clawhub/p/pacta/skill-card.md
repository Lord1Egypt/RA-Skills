## Description:

Pacta is a deprecated and permanently deactivated escrow skill whose runtime exits immediately instead of performing Pacta V1 blockchain actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[amenizm](https://clawhub.ai/user/amenizm)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can inspect this release as a deactivated Pacta V1 escrow skill. It should not be used for escrow, token approval, agreement delivery, contract recovery, or other Pacta V1 actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Deprecated manifest command names may make the skill appear to support Pacta V1 escrow, token approval, agreement, or delivery workflows.

Mitigation: Treat the command names as obsolete compatibility metadata and do not rely on this skill for escrow, token approval, contract recovery, or related workflows.

Risk: Users may attempt to bypass the disabled interface and interact manually with Pacta V1 contracts while funds are frozen or contracts are under review.

Mitigation: Do not attempt manual Pacta V1 contract interactions through this skill; the release is intentionally nonfunctional and exits immediately.

## Reference(s):

- [ClawHub Pacta Skill Page](https://clawhub.ai/amenizm/skills/pacta)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text terminal output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The runtime exits with a fatal error and does not execute Pacta V1 actions.]

## Skill Version(s):

1.0.2 (source: frontmatter, manifest, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
