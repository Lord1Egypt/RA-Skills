## Description:

Helps administer Google Workspace users, groups, organizational units, roles, and domains through an authorized Maton connection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Google Workspace administrators use this skill to inspect and manage directory resources and, when explicitly approved, automate administrative actions through scheduled or external events.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Administrative changes can remove accounts or data, alter access, or affect organization-wide settings.

Mitigation: Use a least-privileged admin account, verify the target, and obtain explicit approval for every write after showing its method, endpoint, target, and consequences.

Risk: Broad triggers or third-party destinations can repeatedly disclose sensitive event data.

Mitigation: Avoid broad triggers and third-party destinations unless explicitly needed; narrowly scope events and share only necessary fields.

Risk: Persistent administrative connections can retain access beyond the task.

Mitigation: Restrict OAuth scopes to the task and revoke Maton and Google connections when the work is complete.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/byungkyu/skills/google-workspace-admin)
- [Maton homepage](https://maton.ai)
- [Maton documentation](https://docs.maton.ai)
- [Google Admin SDK overview](https://developers.google.com/admin-sdk)
- [Google Directory API reference](https://developers.google.com/admin-sdk/directory/reference/rest/v1/users)
- [Time trigger reference](references/time/triggers.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code]

**Output Format:** [Markdown with CLI examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only operations by default; administrative writes require explicit user approval. API results may include personal data.]

## Skill Version(s):

1.2.10 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
