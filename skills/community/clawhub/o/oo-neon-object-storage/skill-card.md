## Description:

Operate Neon Object Storage through an OOMOL-connected account to inspect buckets and objects, upload and download content, and manage stored data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect Neon Object Storage buckets and objects, upload or download content, and manage storage through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fallback setup may run downloaded code without a separate approval step.

Mitigation: Install and review the oo CLI separately before use; check exact targets and effects before approving storage writes or deletions.

## Reference(s):

- [Neon Object Storage](https://neon.com)
- [Neon API documentation](https://api-docs.neon.tech/reference/getting-started-with-neon-api)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON]

**Output Format:** [Markdown with shell command examples and JSON payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May involve changes to connected storage data.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
