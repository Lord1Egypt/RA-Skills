## Description:

Sage Sales Management (forcemanager.com). Use this skill for ANY Sage Sales Management request — reading, creating, updating, and deleting data. Whenever a task involves Sage Sales Management, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Sales teams use this skill to read Sage Sales Management accounts, contacts, and opportunities, and to create, update, or delete those records through a connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup uses remote installer scripts whose release integrity is unverified, and automatic skill synchronization may change installed agent skills.

Mitigation: Install a verified CLI release yourself, review its setup and synchronization behavior, and decide whether to allow automatic skill synchronization.

Risk: The connected service can expose CRM records and permit creates, updates, and deletions, while the backend permission scope is unverified.

Mitigation: Review the OOMOL connection scopes before use, retain approval for changes, and confirm the target and effect before deleting records.

## Reference(s):

- [Sage Sales Management](https://www.forcemanager.com/)
- [Sage Sales Management API documentation](https://developer.forcemanager.com/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [ClawHub release](https://clawhub.ai/oomol/skills/oo-sage-sales-management)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON request payloads and Sage Sales Management records, with concise action guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions can read, create, update, or delete CRM records; writes and deletions require user approval.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
