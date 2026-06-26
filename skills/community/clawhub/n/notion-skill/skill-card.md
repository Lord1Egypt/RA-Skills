## Description: <br>
Work with Notion pages and databases via the official Notion API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Dimagious](https://clawhub.ai/user/Dimagious) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to read, create, append to, query, and update Notion pages and databases through a trusted local Notion CLI backed by the official Notion API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A compromised or untrusted local Notion CLI could misuse the Notion API token or perform unintended API actions. <br>
Mitigation: Install only a trusted Notion CLI and verify the tool source before use. <br>
Risk: The NOTION_API_KEY grants access to every page or database shared with the integration. <br>
Mitigation: Use a dedicated Notion integration, treat the token as a secret, and share only the specific pages or databases required for the task. <br>
Risk: Write operations or database schema changes could alter Notion content in unintended ways. <br>
Mitigation: Review write operations before execution, inspect schema diffs, and require explicit confirmation before applying schema changes. <br>


## Reference(s): <br>
- [Notion API Documentation](https://developers.notion.com) <br>
- [Notion Integrations](https://www.notion.so/my-integrations) <br>
- [ClawHub Notion Skill](https://clawhub.ai/Dimagious/notion-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON arguments] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires NOTION_API_KEY and a trusted local Notion CLI; Notion API visibility is limited to pages and databases shared with the integration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
