## Description:

Edit and search notes and tasks, filter tags and due dates, and export Markdown and CSV. Use for Quick Notes and Tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hznetnewpower](https://clawhub.ai/user/hznetnewpower)

### License/Terms of Use:

MIT No Attribution

## Use Case:

People using OpenClaw can capture and manage notes, tasks, and ideas in the active agent workspace, search and filter records, and export selected records as Markdown or CSV.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Notes, prior versions, and exports remain in the workspace in plaintext, and archiving does not erase them.

Mitigation: Use the intended workspace with appropriate access controls; remove retained files separately when they should be deleted.

Risk: Installing through a floating ClawHub version may select a different release over time.

Mitigation: Pin the ClawHub installer to the reviewed version.

## Reference(s):

- [Quick Notes and Tasks on ClawHub](https://clawhub.ai/hznetnewpower/skills/mochi-quick-notes)
- [Input contract](references/input.md)
- [MochiLab](https://mochilab.bz)

## Skill Output:

**Output Type(s):** [Text, Markdown files, CSV files]

**Output Format:** [Conversational text, Markdown (.md), and CSV (.csv)]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Exports include workspace-relative paths and SHA-256 receipts; records and previous exports are retained in the active workspace.]

## Skill Version(s):

1.1.1 (source: frontmatter, server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
