## Description: <br>
Notion API for creating and managing pages, databases, and blocks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qfish](https://clawhub.ai/user/qfish) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to issue Notion API requests for creating, reading, updating, and querying pages, data sources, and blocks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a Notion integration token that can access shared workspace content. <br>
Mitigation: Use a dedicated Notion integration, share only the pages or data sources the agent should access, and keep the local API key file private. <br>
Risk: Create, update, and add-block examples can modify Notion workspace content. <br>
Mitigation: Review write requests before running them, especially page creation, property updates, and block append operations. <br>


## Reference(s): <br>
- [Notion API documentation](https://developers.notion.com) <br>
- [Notion integrations](https://notion.so/my-integrations) <br>
- [ClawHub skill page](https://clawhub.ai/qfish/notion-test) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local Notion API key file and emits curl request patterns for Notion API operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
