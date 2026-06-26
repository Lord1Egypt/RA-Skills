## Description: <br>
Create agent skills for Microsoft technologies using Learn MCP tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TianqiZhang](https://clawhub.ai/user/TianqiZhang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to create agent skills for Microsoft technologies such as Azure, .NET, Microsoft 365, VS Code, and Bicep. It guides investigation with Microsoft Learn resources, then helps generate hybrid skills that keep essential knowledge local while supporting deeper documentation lookup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional CLI fallback commands may invoke npx or a global npm install. <br>
Mitigation: Prefer the Microsoft Learn MCP server when available, and explicitly approve any npx or global npm install before running it. <br>
Risk: Generated skills and sample code may contain incomplete or outdated Microsoft technology guidance. <br>
Mitigation: Review generated skills and sample code against Microsoft Learn documentation before enabling or running them. <br>


## Reference(s): <br>
- [Microsoft Learn MCP Server](https://learn.microsoft.com/api/mcp) <br>
- [Skill Templates](references/skill-templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown skill files with code blocks and CLI/tool lookup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include generated skill structure, local reference guidance, sample code patterns, and optional Microsoft Learn CLI commands.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
