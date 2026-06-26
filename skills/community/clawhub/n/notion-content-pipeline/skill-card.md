## Description: <br>
Two-way markdown to Notion sync for blog and content workflows, including local draft push and pull, content pipeline database management, status tracking, and batch or per-file operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nissan](https://clawhub.ai/user/nissan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content operators use this skill to move blog drafts between local Markdown files and Notion, create or manage a content pipeline database, and advance posts through review workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a sensitive Notion integration token. <br>
Mitigation: Use a least-privilege Notion integration, share only the required pages or databases with it, and manage the token with your own secure secret-handling process. <br>
Risk: Normal workflows can overwrite local drafts, archive Notion pages, update workflow status, and modify the local sync map. <br>
Mitigation: Keep drafts under version control or backed up, run the advance workflow with --dry-run first, and confirm the target file and Notion page mapping before push or pull operations. <br>
Risk: The advance workflow can run a sibling fact-checker if present and may otherwise skip that step. <br>
Mitigation: Verify the fact-checker behavior before relying on it, review generated reports, or use --skip-factcheck when that dependency is not trusted or not available. <br>


## Reference(s): <br>
- [Notion API Notes](references/api_notes.md) <br>
- [ClawHub release page](https://clawhub.ai/nissan/notion-content-pipeline) <br>
- [Notion integration setup](https://www.notion.so/my-integrations) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, API calls, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands and Python script usage; scripts can create or update local Markdown, JSON sync maps, diffs, reports, and Notion pages.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and a NOTION_API_KEY; outbound network access is used for Notion API calls.] <br>

## Skill Version(s): <br>
1.0.3 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
