## Description: <br>
Integrates agents with Notion workspaces to read pages, query databases, create entries, update properties, append content, and search explicitly shared pages or databases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Moikapy](https://clawhub.ai/user/Moikapy) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, teams, content creators, researchers, and operators use this skill to let an agent manage Notion-backed knowledge bases, content pipelines, project trackers, CRMs, and collaborative documentation. It is appropriate when the user has shared specific Notion pages or databases with a dedicated integration token. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A configured integration token can allow the agent to read or modify Notion pages and databases shared with that integration. <br>
Mitigation: Use a dedicated Notion integration, share only the minimum required pages or databases, and periodically review shared connections. <br>
Risk: The NOTION_TOKEN credential could be exposed if stored in source control or overly broad local files. <br>
Mitigation: Keep NOTION_TOKEN out of source control, store it in local environment configuration with restrictive permissions, and rotate the token if exposure is suspected. <br>
Risk: Automation can change customer, project, or business records incorrectly if commands are run without review. <br>
Mitigation: Require human review before automation updates sensitive records or appends business-critical content. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Moikapy/openclaw-notion-skill) <br>
- [Notion integration setup](https://www.notion.so/my-integrations) <br>
- [Notion API documentation](https://developers.notion.com) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, TypeScript examples, JSON property payloads, and setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May execute Notion API operations through local CLI commands when the agent has a configured NOTION_TOKEN and user-shared Notion pages or databases.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata, SKILL.md frontmatter, package.json, skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
