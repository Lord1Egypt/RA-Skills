## Description:

Use the oo CLI through OOMOL to read, create, update, and delete data in Grist.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People and teams using Grist can inspect documents, tables, columns, and records, and add, update, or delete records through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute remote code and make broader changes to agent configuration or installed skills without clearly explaining or seeking approval.

Mitigation: Review the CLI installer before setup, prefer a reviewed and versioned installation, and disable unwanted automatic skill synchronization.

Risk: Grist requests pass through OOMOL, and write or deletion actions can change user data.

Mitigation: Connect only the Grist resources needed and confirm the exact targets and effects before write or deletion actions.

## Reference(s):

- [Grist](https://www.getgrist.com)
- [Grist API documentation](https://support.getgrist.com/api/)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Grist data and metadata, Guidance]

**Output Format:** [CLI commands with JSON action payloads and connector responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an installed, authenticated oo CLI and a connected Grist account; write and deletion actions require confirmation of the exact effect.]

## Skill Version(s):

1.0.5 (source: frontmatter and server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
