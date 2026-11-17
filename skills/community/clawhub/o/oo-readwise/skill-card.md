## Description:

Use the oo CLI to read and manage Readwise books, highlights, and Reader documents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Users can access Readwise books and highlights and manage Reader documents through an existing OOMOL account connection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may run a downloaded installer and introduce broader changes to agent skills without clear user control.

Mitigation: Review the CLI installation and any skills it installs or updates; consider disabling startup synchronization with OO_SKILLS_SYNC_DISABLED.

Risk: Connecting Readwise authorizes OOMOL to access the account, and proposed data changes may affect its contents.

Mitigation: Review each proposed data change and confirm write or destructive actions before running them.

## Reference(s):

- [Readwise](https://readwise.io)
- [Readwise API documentation](https://readwise.io/api_deets)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [CLI commands and JSON action results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions may read or change Readwise data; update_document can overwrite document fields.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
