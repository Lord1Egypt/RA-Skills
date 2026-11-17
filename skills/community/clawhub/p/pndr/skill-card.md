## Description:

Personal productivity app with Ideas/Tasks, Journal, Habits, Package tracking, Lists, and more via MCP

This skill is ready for commercial/non-commercial use.

## Publisher:

[dgershman](https://clawhub.ai/user/dgershman)

### License/Terms of Use:


## Use Case:

External Pndr users and developers use this skill to connect an MCP-capable assistant to their Pndr account for natural-language task, journal, habit, list, package, tag, comment, attachment, and analytics workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill connects an assistant to private Pndr productivity data and may expose tasks, journals, habits, lists, packages, comments, attachments, and analytics to the assistant.

Mitigation: Install only when the assistant is allowed to access that account data, and prefer read-only access when full modification is not required.

Risk: Pro accounts can allow broad write and delete actions across Pndr records.

Mitigation: Confirm destructive or bulk-change requests before allowing the assistant to complete, archive, modify, or delete records.

Risk: The setup uses a client secret and a long-lived bearer token that could grant account access if exposed.

Mitigation: Treat credentials like passwords, keep them out of logs, screenshots, and committed config files, and rotate or revoke them if exposed.

## Reference(s):

- [Pndr](https://pndr.io)
- [Pndr Documentation](https://pndr.io/docs)
- [Pndr Source Code](https://github.com/Dgershman/pndr)
- [Pndr Issues](https://github.com/Dgershman/pndr/issues)
- [ClawHub Pndr Skill](https://clawhub.ai/dgershman/skills/pndr)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Pndr account, OAuth client credentials, a bearer token, and an MCP-capable client such as mcporter.]

## Skill Version(s):

1.0.20260202 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
