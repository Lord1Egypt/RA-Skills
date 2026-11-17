## Description:

Use the connected 2Chat account to inspect account information and create contacts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to inspect a connected 2Chat account, review usage and webhooks, validate its API key, and create contacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup directs the agent to run downloaded software without a separate approval step.

Mitigation: Review and install the CLI separately, require approval for future software installation, and check its automatic skill synchronization settings.

Risk: OOMOL mediates access to the connected 2Chat account, and the downloaded installers and runtime were not audited.

Mitigation: Understand the account access path before use; rely on the skill's explicit confirmation safeguards for account writes.

## Reference(s):

- [2Chat](https://2chat.co)
- [2Chat API documentation](https://developers.2chat.co/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Guidance, JSON, Shell commands]

**Output Format:** [Structured account data and Markdown guidance with JSON payloads and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Account data depends on the connected 2Chat account; contact creation changes account data after confirmation.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
