## Description:

Scans an agent skill directory before publication for possible API keys, tokens, private keys, personal contact data, and precise coordinates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vlalamoon](https://clawhub.ai/user/vlalamoon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill publishers use this skill before a ClawHub release to run a lightweight local scan for obvious secrets and sensitive personal data in skill files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The checker can miss important secret patterns and incorrectly report that a skill is safe to publish.

Mitigation: Use it as a lightweight helper alongside a mature secret scanner and manual review before publishing.

Risk: Current scanner behavior may provide incomplete coverage for private keys, generic tokens, and coordinates.

Mitigation: Add targeted coverage for those patterns before using the skill as part of a release workflow.

Risk: User-facing output is Chinese-only.

Mitigation: Confirm the intended operators can read the output or add localized messages for the release audience.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vlalamoon/skills/pre-publish-security-check)
- [Publisher profile](https://clawhub.ai/user/vlalamoon)

## Skill Output:

**Output Type(s):** [analysis, shell commands, guidance]

**Output Format:** [Terminal text with remediation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language command output; exits nonzero when potential sensitive information is found.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
