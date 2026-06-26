## Description: <br>
Notion API for creating and managing pages, databases, blocks, relations, rollups, and multi-workspace profiles via the notioncli CLI tool. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JordanCoin](https://clawhub.ai/user/JordanCoin) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, employees, and agents use this skill to query, create, update, move, delete, and inspect Notion workspace content through the notioncli command-line tool. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify, move, archive, or delete Notion pages, blocks, and database schema. <br>
Mitigation: Require explicit approval before delete, move, schema update, block delete, or other destructive operations. <br>
Risk: The skill depends on a Notion API key and can access any pages or databases shared with that integration. <br>
Mitigation: Use a least-privilege Notion integration, share only required workspace resources, and verify where the API key is stored. <br>
Risk: The skill can upload local files to Notion pages. <br>
Mitigation: Require explicit approval before file uploads and verify both the local file path and destination page. <br>


## Reference(s): <br>
- [ClawHub Notion skill page](https://clawhub.ai/JordanCoin/notioncli) <br>
- [notioncli project homepage](https://github.com/JordanCoin/notioncli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and CLI output formats such as table, CSV, JSON, and YAML] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires NOTION_API_KEY and a Notion integration shared with the target pages or databases.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
