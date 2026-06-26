## Description: <br>
Notion API for creating and managing pages, databases, blocks and enhanced markdown. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fental](https://clawhub.ai/user/fental) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to call the Notion API for creating, reading, updating, and querying pages, data sources, blocks, and Markdown page content in Notion workspaces shared with the integration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read Notion pages, databases, and optional transcript content shared with the integration. <br>
Mitigation: Use a dedicated least-privileged Notion integration and share only the pages or databases needed for the task. <br>
Risk: The setup stores the Notion API key in a plaintext local file. <br>
Mitigation: Protect or avoid the plaintext API-key file and limit access to the account or environment where it is stored. <br>
Risk: Page updates, content replacement, and deletion-enabling options can change or remove sensitive Notion content. <br>
Mitigation: Review operations that update, replace, or fetch sensitive content before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fental/notion-enhanced-markdown) <br>
- [Notion developer documentation](https://developers.notion.com) <br>
- [Notion integration setup](https://notion.so/my-integrations) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, Configuration, Markdown, Guidance] <br>
**Output Format:** [Markdown with cURL examples, JSON request bodies, and configuration instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires NOTION_API_KEY and a Notion integration shared with the target pages or databases.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
