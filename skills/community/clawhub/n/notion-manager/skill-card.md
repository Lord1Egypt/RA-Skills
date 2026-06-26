## Description: <br>
Production-ready Notion API client for SaaS workflows. Create/read/update pages, query data sources, append blocks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tomas-mikula](https://clawhub.ai/user/tomas-mikula) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and SaaS operators use this skill to search Notion, read and update pages, query or create data sources, and append blocks through the Notion API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access and modify selected Notion workspace resources through a provided Notion integration token. <br>
Mitigation: Use a least-privilege Notion integration, connect only required pages or data sources, and confirm write, undo, or delete-style actions before execution. <br>


## Reference(s): <br>
- [ClawHub Notion Manager release](https://clawhub.ai/tomas-mikula/notion-manager) <br>
- [Publisher profile](https://clawhub.ai/user/tomas-mikula) <br>
- [Publisher website](https://FrontendAccelerator.com) <br>
- [Notion API endpoint](https://api.notion.com/v1) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Guidance] <br>
**Output Format:** [JSON status object with data, metadata, and error fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Notion API key and operation-specific parameters.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
