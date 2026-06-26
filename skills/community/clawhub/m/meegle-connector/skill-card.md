## Description: <br>
Connect to Meegle via MCP service, support OAuth authentication, and enable querying and managing work items, views, etc. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wadxm](https://clawhub.ai/user/wadxm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams use this skill to connect an agent to Meegle so it can query to-dos, views, and work item information and help create, modify, or transfer work items after user confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on OAuth credentials stored at ~/.mcporter/credentials.json. <br>
Mitigation: Use browser OAuth when possible, protect the credentials file, and do not log or store credential contents outside ~/.mcporter/. <br>
Risk: The skill can help create, modify, or transfer Meegle work items through an npm MCP tool. <br>
Mitigation: Require explicit user confirmation before any create, modify, or transfer action. <br>
Risk: Runtime behavior depends on the external @lark-project/meego-mcporter npm package and Meegle MCP service. <br>
Mitigation: Install only when those dependencies are trusted and available in the target environment. <br>


## Reference(s): <br>
- [@lark-project/meego-mcporter npm package](https://www.npmjs.com/package/@lark-project/meego-mcporter) <br>
- [Meegle OAuth help article](https://meegle.com/b/helpcenter/product/5rifl7a7) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Text] <br>
**Output Format:** [Markdown with inline bash commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce instructions for OAuth setup and Meegle MCP tool calls; credential handling requires user confirmation.] <br>

## Skill Version(s): <br>
1.0.9 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
