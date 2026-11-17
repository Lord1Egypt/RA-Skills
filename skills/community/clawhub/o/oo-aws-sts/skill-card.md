## Description:

AWS STS (aws.amazon.com). Use this skill for ANY AWS STS request — reading, creating, and updating data. Whenever a task involves AWS STS, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to request AWS STS operations through an OOMOL-connected account, including assuming a role and obtaining federated temporary credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI setup uses unverified remote code, and startup skill synchronization may make persistent changes to agent skills.

Mitigation: Review and approve setup separately using a trusted, version-pinned distribution. Set OO_SKILLS_SYNC_DISABLED=1 before invoking the CLI if startup skill synchronization is unwanted.

Risk: AWS actions require permissions and may return temporary credentials.

Mitigation: Connect only the AWS permissions needed for the task and treat returned temporary credentials as secrets.

## Reference(s):

- [AWS Security Token Service API Reference](https://docs.aws.amazon.com/STS/latest/APIReference/welcome.html)
- [AWS Identity and Access Management](https://aws.amazon.com/iam/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API calls, JSON, Shell commands, Guidance]

**Output Format:** [JSON action payloads and structured CLI responses, with Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses may contain temporary AWS credentials; treat them as secrets.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
