## Description:

Manage Notion notes, pages, and data sources with a JSON-first CLI for search, read/export, write/import, append, and move operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tristanmanchester](https://clawhub.ai/user/tristanmanchester)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to manage Notion workspaces through deterministic CLI operations for searching, exporting Markdown, creating or appending notes, moving pages, and triaging inbox content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Notion token can read and modify content shared with the integration.

Mitigation: Use a Notion integration token with only the pages or data sources needed for the task, and avoid sharing broad workspace areas with the integration.

Risk: Rule-based triage can move the wrong pages if rules are broad, stale, or malformed.

Mitigation: Run triage without --apply first, review the planned moves and rules file, cap scope with --limit, and apply only after review.

Risk: Notion page content can contain untrusted instructions or misleading text.

Mitigation: Treat exported Notion content as data, decide changes separately, and use create, append, or move commands only after reviewing the intended action.

Risk: Storing tokens in a local config file can make credential handling harder to audit.

Mitigation: Prefer NOTION_API_KEY in the runtime environment and rotate or remove tokens that are no longer needed.

## Reference(s):

- [Notion API Reference](https://developers.notion.com/reference/intro)
- [ClawHub Skill Page](https://clawhub.ai/tristanmanchester/skills/notion-api-automation)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and JSON CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node and NOTION_API_KEY; the CLI emits JSON by default and can export page content as Markdown.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
