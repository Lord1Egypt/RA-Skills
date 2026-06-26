## Description: <br>
Create and list Notion tasks in a single database via Notion API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luciorenovato](https://clawhub.ai/user/luciorenovato) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Notion users and assistants configured with a Notion integration use this skill to add tasks, list today's tasks, search task text, and resolve task database aliases from chat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Notion integration token that can access configured databases. <br>
Mitigation: Share the Notion integration only with intended task databases, keep NOTION_DATABASE_MAP limited, and rotate or revoke the token if exposed. <br>
Risk: Task text, dates, times, and locations are sent to Notion and stored in configured databases. <br>
Mitigation: Avoid capturing secrets or highly sensitive information as task content, and review entries before relying on them. <br>


## Reference(s): <br>
- [Notion API endpoint](https://api.notion.com/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration] <br>
**Output Format:** [Plain text and JSON returned from shell command execution] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires NOTION_TOKEN and either NOTION_DATABASE_MAP or NOTION_DATABASE_ID.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
