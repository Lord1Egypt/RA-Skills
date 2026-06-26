## Description: <br>
Connect to Meegle via MCP service, support OAuth authentication, and enable querying and managing work items, views, etc. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wadxm](https://clawhub.ai/user/wadxm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to authenticate an agent with Meegle and query, create, modify, or transfer work items and views through the Meegle MCP service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent OAuth credentials are stored at ~/.mcporter/credentials.json. <br>
Mitigation: Prefer browser OAuth, protect the credentials file, avoid logging credential contents, and store credentials only in the designated mcporter location. <br>
Risk: The skill can create, modify, or transfer Meegle work items. <br>
Mitigation: Require the agent to show exact proposed work-item changes and receive user confirmation before executing changes. <br>
Risk: Use depends on the external npm package and trusted Meegle workspace access. <br>
Mitigation: Install only when the npm package and target Meegle workspace access are trusted for the intended environment. <br>


## Reference(s): <br>
- [ClawHub Meegle Connector listing](https://clawhub.ai/wadxm/meegel-connector) <br>
- [@lark-project/meego-mcporter npm package](https://www.npmjs.com/package/@lark-project/meego-mcporter) <br>
- [Meegle OAuth authorization guide](https://meegle.com/b/helpcenter/product/5rifl7a7) <br>
- [Meegle MCP server endpoint](https://meegle.com/mcp_server/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide creation of meegle-config.json and OAuth credential setup; work-item changes should be shown to the user before execution.] <br>

## Skill Version(s): <br>
1.0.9 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
