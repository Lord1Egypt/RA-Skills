## Description: <br>
Full Notion API skill - query databases, manage pages, append blocks, and search your entire workspace. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fr3kstyle](https://clawhub.ai/user/fr3kstyle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to search, read, and modify Notion pages, databases, and blocks through a Notion integration token. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A broad Notion integration token may allow the agent to read or modify more workspace content than intended. <br>
Mitigation: Share the Notion integration only with the specific pages or databases needed, and keep NOTION_API_KEY out of chats and logs. <br>
Risk: Create, update, append, and archive commands can change or hide Notion content. <br>
Mitigation: Require human review before running mutating commands against databases, pages, or blocks. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/fr3kstyle/notion-workspace) <br>
- [Notion API endpoint](https://api.notion.com/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown usage guidance with bash commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires NOTION_API_KEY and optionally NOTION_DATABASE_ID.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
