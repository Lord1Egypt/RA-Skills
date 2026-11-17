## Description:

Use this skill for Retable requests to read, create, update, and delete data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use the skill to manage Retable workspaces, tables, and rows through an OOMOL-connected account, including reading, creating, updating, and deleting data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may run downloaded code and introduce additional agent skills; the remote installer payload was unavailable for review, so its full local effects are uncertain.

Mitigation: Review the CLI installation before setup, disable startup skill synchronization with OO_SKILLS_SYNC_DISABLED=1 if it is not needed, use narrowly scoped Retable access, and retain approval gates for writes and deletions.

## Reference(s):

- [Retable API documentation](https://docs.retable.io/retable-user-guide/retable-api/api)
- [Retable homepage](https://www.retable.io)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Text]

**Output Format:** [Shell commands with JSON input and JSON responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read actions return data; write actions change Retable state and deletions remove data.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
