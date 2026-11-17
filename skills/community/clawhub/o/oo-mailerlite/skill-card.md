## Description:

MailerLite (mailerlite.com). Use this skill for ANY MailerLite request — reading, creating, updating, and deleting data. Whenever a task involves MailerLite, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use the skill to read and manage MailerLite subscribers, groups, and fields through their connected account. It guides the agent to inspect each action's schema and obtain confirmation before writes or destructive changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: If the oo CLI dependency is missing, a fallback may execute an unverified online installer without separate approval.

Mitigation: Install a verified oo release yourself and require approval before running any fallback installer.

Risk: The connector acts through the user's connected MailerLite account.

Mitigation: Review the OOMOL connection trust relationship and retain the skill's confirmation requirements for write and deletion actions.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [MailerLite API documentation](https://developers.mailerlite.com/docs/)

## Skill Output:

**Output Type(s):** [API calls, JSON, Guidance]

**Output Format:** [JSON action results with concise natural-language summaries and guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can read, create, update, and delete MailerLite data; the skill requires confirmation before write and destructive actions.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
