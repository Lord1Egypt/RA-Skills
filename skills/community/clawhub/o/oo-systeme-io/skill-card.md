## Description:

Systeme.io (systeme.io). Use this skill for ANY Systeme.io request — reading, creating, updating, and deleting data. Whenever a task involves Systeme.io, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and business operators use the skill to read and manage contacts, tags, courses, subscriptions, enrollments, and webhooks in a connected Systeme.io account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may run an unverified remote installer without separate user approval.

Mitigation: Review the CLI dependency and installer, require separate approval before installation, and prefer a verified fixed release.

Risk: Using a connected Systeme.io account entrusts OOMOL with account credentials and business data.

Mitigation: Review the connection, keep confirmations for account changes, and review or disable automatic skill synchronization.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Systeme.io API documentation](https://developer.systeme.io/)
- [Systeme.io](https://systeme.io)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text, Guidance]

**Output Format:** [JSON action payloads and connector responses, with textual guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Write and destructive actions require user confirmation before execution.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
