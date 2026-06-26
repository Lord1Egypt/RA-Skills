## Description: <br>
Sync IM messages to Notion via Notion API. Supports 7 content types, 4 formats, 2 metadata types. Append-only to a single Notion page. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[70asunflower](https://clawhub.ai/user/70asunflower) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to capture IM-style notes, diary entries, tasks, links, quotes, images, and summaries into a configured Notion page through the Notion API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Notion API token and page ID, which can grant access beyond a single intended workflow if the integration is over-scoped. <br>
Mitigation: Use a dedicated Notion integration restricted to the intended page and store credentials only in the configured environment variables. <br>
Risk: The skill can save, search, upload, and delete Notion content more broadly than its append-only summary suggests. <br>
Mitigation: Review commands before execution, prefer explicit trigger prefixes, and verify the configured Notion page before first use. <br>
Risk: Local image paths are uploaded to Notion servers when image handling is invoked. <br>
Mitigation: Avoid local file paths unless the file is intended to be uploaded to Notion. <br>
Risk: The undo command can delete the last batch of blocks or the last single block without an extra confirmation step. <br>
Mitigation: Treat undo as destructive and use it only after confirming the target content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/70asunflower/notion-im-helper) <br>
- [Publisher profile](https://clawhub.ai/user/70asunflower) <br>
- [Notion integrations](https://www.notion.so/my-integrations) <br>
- [Notion API endpoint](https://api.notion.com/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text status messages and Markdown guidance with shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses standardized OK, ERROR, and INFO status prefixes from helper scripts.] <br>

## Skill Version(s): <br>
1.7.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
