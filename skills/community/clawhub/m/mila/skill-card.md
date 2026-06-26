## Description: <br>
Create, read, update, and delete documents, spreadsheets, and slide presentations in Mila via the REST API or MCP tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freddyjd](https://clawhub.ai/user/freddyjd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to manage Mila documents, spreadsheets, slide decks, and collaborative workspaces through documented REST API calls or MCP tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to create, update, replace, or delete Mila documents, sheets, slides, and workspace content. <br>
Mitigation: Use a dedicated least-privilege API key, prefer read-only scopes unless writes are needed, and require confirmation of the exact title, ID, and workspace before any update, replacement, or delete action. <br>
Risk: Mila API keys are credentials that grant access according to their scopes. <br>
Mitigation: Keep MCP client configuration files private and avoid exposing API keys in shared prompts, logs, or repositories. <br>


## Reference(s): <br>
- [Mila homepage](https://mila.gg) <br>
- [Mila API documentation](https://mila.gg/docs) <br>
- [Mila MCP integration guide](https://mila.gg/mcp) <br>
- [Documents reference](references/DOCUMENTS.md) <br>
- [Sheets reference](references/SHEETS.md) <br>
- [Slides reference](references/SLIDES.md) <br>
- [Servers reference](references/SERVERS.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline JSON and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include REST API examples, MCP tool names, and client configuration snippets.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
