## Description: <br>
Helps agents use the Notion API to create, read, update, move, lock, and manage pages, data sources, blocks, and templates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DongkuKim](https://clawhub.ai/user/DongkuKim) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to generate Notion API guidance, request examples, shell commands, and configuration steps for managing Notion workspaces through an integration token. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes examples that can move, lock, update, or erase Notion page content. <br>
Mitigation: Require explicit user confirmation before applying content-changing actions and review generated requests before execution. <br>
Risk: The skill relies on a Notion integration token stored on the local machine. <br>
Mitigation: Protect ~/.config/notion/api_key and share the Notion integration only with pages or data sources it needs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/DongkuKim/notion-2026-01-15) <br>
- [DongkuKim ClawHub profile](https://clawhub.ai/user/DongkuKim) <br>
- [Notion API documentation](https://developers.notion.com) <br>
- [Notion integrations](https://notion.so/my-integrations) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include content-changing Notion API examples that should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
