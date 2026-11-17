## Description:

Fast Note Sync (github.com). Use this skill for ANY Fast Note Sync request — reading, creating, updating, and deleting data. Whenever a task involves Fast Note Sync, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill through an OOMOL-connected account to find, read, create, and manage Fast Note Sync notes, vaults, and attachments. It also guides setup and requires approval for actions that change or delete data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup directs the agent to run downloaded installer code without explicit approval, and the installer implementation is unverified.

Mitigation: Review the CLI installation separately, require approval before running downloaded installers, and check its automatic bundled-skill installation behavior.

Risk: Connecting an account permits access to private notes, while note and vault actions can change or remove user data.

Mitigation: Retain the documented approval requirements for changes and deletions.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Fast Note Sync service](https://github.com/haierkeys/fast-note-sync-service)
- [Fast Note Sync REST API documentation](https://github.com/haierkeys/fast-note-sync-service/blob/master/docs/REST_API.md)

## Skill Output:

**Output Type(s):** [API Calls, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell command examples and connector action results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read actions return note, vault, or attachment data; changes and deletions require user approval.]

## Skill Version(s):

1.0.5 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
