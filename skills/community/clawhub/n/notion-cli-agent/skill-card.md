## Description: <br>
Provides command-line guidance for agents to access and manage Notion pages, databases, blocks, users, and comments through notion-cli. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[FroeMic](https://clawhub.ai/user/FroeMic) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to configure notion-cli and direct an agent through Notion workspace search, retrieval, creation, update, archive, block, user, and comment workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Notion integration can access any workspace pages or databases shared with it. <br>
Mitigation: Create a dedicated Notion integration and share only the pages or databases needed for the agent task. <br>
Risk: The Notion API key and workspace content could be exposed through careless environment handling or verbose debug logs. <br>
Mitigation: Protect and rotate the API key, and avoid debug logging around sensitive Notion workspace content. <br>
Risk: Update, archive, delete, append, and comment commands can mutate workspace content. <br>
Mitigation: Require explicit confirmation before commands that modify, archive, delete, append to, or comment on Notion content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/FroeMic/notion-cli-agent) <br>
- [notion-cli repository](https://github.com/FroeMic/notion-cli) <br>
- [Notion integrations](https://www.notion.so/profile/integrations) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with command examples and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include JSON, table, or CSV output format guidance for notion-cli commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
