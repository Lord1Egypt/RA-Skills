## Description:

Manage Happy Scribe transcriptions, orders, and exports, including reading, creating, updating, and deleting data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People working with a connected Happy Scribe account use this skill to retrieve and manage transcription data, submit transcription or translation orders, and create exports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup uses remote CLI installers whose behavior and connector implementations have not been verified.

Mitigation: Review and verify the specific oo CLI release before allowing setup.

Risk: The CLI may make persistent skill synchronization changes beyond the documented Happy Scribe actions.

Mitigation: Consider setting OO_SKILLS_SYNC_DISABLED=1 before invoking the CLI.

Risk: Orders, updates, and deletions can change Happy Scribe data.

Mitigation: Retain confirmation for orders, updates, and deletions.

## Reference(s):

- [Happy Scribe API documentation](https://dev.happyscribe.com/sections/general/)
- [Happy Scribe](https://www.happyscribe.com/)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Text, Guidance]

**Output Format:** [Structured JSON results with concise text summaries and guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the connected Happy Scribe account and selected action.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
