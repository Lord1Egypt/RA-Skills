## Description: <br>
Manage monday.com boards, items, columns, groups, updates, and workflows via MCP server (preferred) and GraphQL API (fallback). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[regevguym](https://clawhub.ai/user/regevguym) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agents use this skill to manage monday.com project, CRM, workflow, and reporting resources through the official MCP server or direct GraphQL API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents to access and modify broad monday.com business data. <br>
Mitigation: Install only for intended monday.com use, use a least-privilege token, and verify board access before operations. <br>
Risk: Destructive or bulk actions could delete or alter boards, items, groups, or workflows. <br>
Mitigation: Require explicit user confirmation for destructive or bulk changes and summarize what will change before execution. <br>
Risk: The MCP configuration uses an unpinned package reference in the artifact. <br>
Mitigation: Pin or review the monday.com MCP package before installation instead of relying on an @latest install. <br>
Risk: The artifact encourages retaining board and item names, URLs, and context in persistent memory. <br>
Mitigation: Disable or limit persistent memory for monday.com resource details unless users knowingly opt in. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/regevguym/monday-com) <br>
- [monday.com Developer Docs](https://developer.monday.com) <br>
- [monday.com API Reference](https://developer.monday.com/api-reference) <br>
- [monday.com MCP Server](https://github.com/mondaycom/mcp) <br>
- [GraphQL API Examples](references/graphql-examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown guidance with JSON, GraphQL, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce monday.com MCP configuration, GraphQL requests, direct resource URLs, summaries, and operational next steps.] <br>

## Skill Version(s): <br>
1.3.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
