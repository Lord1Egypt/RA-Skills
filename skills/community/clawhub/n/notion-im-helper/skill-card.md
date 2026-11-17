## Description:

Syncs IM-style notes, tasks, links, images, captions, searches, and summaries to Notion through the Notion API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[70asunflower](https://clawhub.ai/user/70asunflower)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent classify IM-style messages and run Notion scripts that record notes, todos, links, images, captions, monthly summaries, and searches in a configured Notion workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A broadly authorized Notion integration can expose or affect more workspace content than the user expects.

Mitigation: Authorize the integration only to a dedicated Notion page and avoid granting broad workspace access.

Risk: Matched messages and local images may be written or uploaded to Notion automatically.

Mitigation: Review triggers, message content, and file paths before execution, especially when handling sensitive or private content.

Risk: Search and monthly-summary commands read existing Notion content, and undo can delete recent Notion blocks.

Mitigation: Limit the target page to content suitable for agent access and confirm destructive undo commands before running them.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/70asunflower/skills/notion-im-helper)
- [Notion integrations setup](https://www.notion.so/my-integrations)
- [Notion API endpoint](https://api.notion.com/v1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration guidance]

**Output Format:** [Plain text and Markdown with shell command invocations and Notion status prefixes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires NOTION_API_KEY and NOTION_PARENT_PAGE_ID; operations can write to Notion, read existing Notion content, upload local images, and delete recent Notion blocks through undo.]

## Skill Version(s):

1.7.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
