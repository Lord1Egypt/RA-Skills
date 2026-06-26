## Description: <br>
Notion API for creating and managing pages, databases, and blocks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nidhov01](https://clawhub.ai/user/nidhov01) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and workspace operators use this skill to create, read, update, and query Notion pages, data sources, and blocks through the Notion API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a Notion API key that can read or modify content shared with the integration. <br>
Mitigation: Use a dedicated Notion integration and share only the pages or data sources required for the task. <br>
Risk: A stored API key could be exposed through permissive file permissions, commits, or logs. <br>
Mitigation: Restrict permissions on the key file and avoid committing or logging the key. <br>
Risk: Write requests can change Notion pages, data sources, or blocks. <br>
Mitigation: Review proposed write requests before running them. <br>


## Reference(s): <br>
- [Notion API documentation](https://developers.notion.com) <br>
- [Notion integration setup](https://notion.so/my-integrations) <br>
- [ClawHub skill page](https://clawhub.ai/nidhov01/nidhov01-notion) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/nidhov01) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Notion API guidance and curl examples for agent-mediated page, data source, and block operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
