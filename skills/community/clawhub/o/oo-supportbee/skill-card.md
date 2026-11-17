## Description:

Use this skill to read, create, update, and delete SupportBee data through your connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Support teams and account operators use this skill to find and manage tickets, replies, comments, labels, users, and teams in SupportBee.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fallback setup may execute changing remote code without clearly limiting or approving local changes; the downloaded installers could not be inspected, so their exact local effects are uncertain.

Mitigation: Use a separately approved, verified oo CLI release, and review its automatic skill synchronization and local effects before running setup.

## Reference(s):

- [SupportBee API documentation](https://supportbee.com/docs/api/api)
- [SupportBee](https://supportbee.com)
- [oo CLI project page](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [Structured SupportBee data with concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses may contain customer support ticket and user data.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
