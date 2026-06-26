## Description: <br>
Notion CLI for creating and managing pages, databases, and blocks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[willykinfoussia](https://clawhub.ai/user/willykinfoussia) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external users use this skill to search, read, create, update, and query Notion pages, databases, and blocks through notion-cli and direct Notion API examples. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and modify Notion content shared with the integration token. <br>
Mitigation: Use a dedicated least-privilege Notion integration and share only the pages or databases the agent needs. <br>
Risk: Create and update actions can change live Notion workspace data. <br>
Mitigation: Review proposed create, patch, and database query actions before execution. <br>
Risk: The local Notion token file can expose workspace access if mishandled. <br>
Mitigation: Store the token with restrictive local permissions and avoid sharing it in prompts, logs, or generated files. <br>
Risk: The workflow depends on an external npm package. <br>
Mitigation: Verify the npm package source and version before installation. <br>


## Reference(s): <br>
- [ClawHub release](https://clawhub.ai/willykinfoussia/notion-cli) <br>
- [notion-cli GitHub repository](https://github.com/litencatt/notion-cli) <br>
- [Notion API documentation](https://developers.notion.com) <br>
- [Create a Notion integration](https://notion.so/my-integrations) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, configuration guidance, JSON examples] <br>
**Output Format:** [Markdown with inline shell commands, curl examples, and JSON payload snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires NOTION_TOKEN and may produce Notion CLI output in table, csv, json, yaml, or raw JSON formats.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata; release changelog text states Version 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
