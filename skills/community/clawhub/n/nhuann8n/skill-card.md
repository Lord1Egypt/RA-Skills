## Description: <br>
Notion API for creating and managing pages, databases, and blocks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nhuanlaptrinh](https://clawhub.ai/user/nhuanlaptrinh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to prepare Notion API requests for reading, creating, and updating pages, data sources, and blocks from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Notion integration token can read or change any Notion content shared with that integration. <br>
Mitigation: Use a dedicated Notion integration, share only required pages or data sources, store the token securely, and rotate it if exposed. <br>
Risk: POST and PATCH examples can create or update live Notion content. <br>
Mitigation: Review target IDs and payloads before executing write requests, and test against non-critical pages first. <br>


## Reference(s): <br>
- [Notion API documentation](https://developers.notion.com) <br>
- [Notion integrations](https://notion.so/my-integrations) <br>
- [ClawHub skill page](https://clawhub.ai/nhuanlaptrinh/nhuann8n) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration] <br>
**Output Format:** [Markdown with bash curl commands and JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a NOTION_API_KEY token and access to the target Notion pages or data sources.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
