## Description:

Use the oo CLI to read, create, and update Shortcut data through a connected OOMOL account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and project teams use this skill to inspect Shortcut workspace data and create or update stories and epics through their connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup fallback can run downloaded installer code locally without separate approval or integrity verification.

Mitigation: Review the installer, use a reviewed version-pinned CLI, and require approval before local installation or agent-skill changes.

Risk: Using the connected service involves OOMOL handling Shortcut credentials and workspace data, and some actions change Shortcut records.

Mitigation: Assess whether the OOMOL connection is appropriate for the workspace and retain user confirmation for each Shortcut write.

## Reference(s):

- [Shortcut API documentation](https://developer.shortcut.com/api/rest/v3)
- [Shortcut](https://www.shortcut.com)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [Text, API Calls, JSON]

**Output Format:** [Text responses and JSON-formatted Shortcut data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can create or update Shortcut records when the user confirms the proposed write.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
