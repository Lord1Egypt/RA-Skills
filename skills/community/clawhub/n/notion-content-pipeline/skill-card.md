## Description:

Two-way Markdown and Notion sync for blog and content workflows, including local draft push/pull, tracked page mappings, and content pipeline database management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nissan](https://clawhub.ai/user/nissan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operators use this skill to move Markdown drafts between local files and Notion, keep a sync map of page IDs, and advance blog content through review-oriented pipeline statuses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Notion integration token that can create, edit, archive, and query pages in shared workspaces.

Mitigation: Use a least-privilege Notion integration, share only the intended parent page or database, protect the token, and configure parent page and database IDs explicitly before use.

Risk: Push and pipeline advance flows can archive existing Notion pages, overwrite local Markdown from Notion pulls, and mutate pipeline status fields.

Mitigation: Review backups and sync-map entries before pull, push overwrite, or pipeline advance; pull before pushing when Notion edits may exist; use no-overwrite behavior when preserving an existing page matters.

Risk: Dry-run mode should not be treated as a full no-execution sandbox because the workflow still initializes configuration and may inspect pipeline state.

Mitigation: Run dry-run only with intentionally scoped credentials and workspace IDs, and use separate test pages or databases for validation.

Risk: The pipeline advance workflow can execute a sibling fact-checker script outside this package when that script exists.

Mitigation: Remove, review, or pin the sibling fact-checker dependency before routine use, and skip fact-checking when the external script has not been approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nissan/skills/notion-content-pipeline)
- [Publisher profile](https://clawhub.ai/user/nissan)
- [Notion API Notes](references/api_notes.md)
- [Notion API](https://api.notion.com/v1)
- [Notion integrations](https://www.notion.so/my-integrations)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, environment variable examples, and generated local report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local Markdown files, sync-map JSON, humanizer diff reports, fact-check reports, Notion pages, and Notion database status fields.]

## Skill Version(s):

1.0.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
