## Description: <br>
Notion integration - Manage pages, databases, and content in Notion <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lukaizj](https://clawhub.ai/user/lukaizj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to search Notion, query databases, and create or update Notion pages through a configured integration token. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a Notion API key that can access shared pages and databases and can create pages. <br>
Mitigation: Use a least-privilege Notion integration, share only the pages or databases needed, and confirm the destination and content before asking the agent to create pages. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/lukaizj/lukaizj-notion) <br>
- [Project homepage](https://github.com/lukaizj/notion-integration-skill) <br>
- [Notion integrations setup](https://www.notion.so/my-integrations) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Text] <br>
**Output Format:** [JSON-like tool results and Notion content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires NOTION_API_KEY and access to shared Notion pages or databases.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and claw.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
