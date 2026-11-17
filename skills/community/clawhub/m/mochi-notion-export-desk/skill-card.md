## Description:

Index an existing Notion Markdown/CSV export with page references, table counts and source hashes. Use for Notion Export Desk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hznetnewpower](https://clawhub.ai/user/hznetnewpower)

### License/Terms of Use:

MIT No Attribution

## Use Case:

External users can provide a Notion Markdown/CSV export ZIP to create a page index, database row and column summaries, a Markdown compilation, and source hash records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports contain copied page content from the selected Notion export.

Mitigation: Keep the source export and generated reports private.

Risk: Workspace path checks do not provide OS-level isolation.

Mitigation: Retain the host sandbox and process only the intended export.

## Reference(s):

- [Notion export help](https://www.notion.com/help/export-your-content)
- [Action contract](references/input.md)
- [ClawHub release](https://clawhub.ai/hznetnewpower/skills/mochi-notion-export-desk)

## Skill Output:

**Output Type(s):** [Files, Markdown, JSON, HTML]

**Output Format:** [Markdown index with JSON and HTML reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include source paths and SHA-256 hashes.]

## Skill Version(s):

1.0.1 (source: release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
