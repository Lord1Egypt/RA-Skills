## Description: <br>
Scaffolds a new MCP server from a one-line description. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[njengah](https://clawhub.ai/user/njengah) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to scaffold a complete TypeScript MCP server project from a short description, including tools, transport setup, Claude Code configuration, environment documentation, and README content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated MCP configuration can include placeholder absolute paths or environment values that are unsafe to use as-is. <br>
Mitigation: Review the generated MCP config and replace placeholder paths and environment values before running the scaffold. <br>
Risk: Generated MCP server code may not match the security needs of the target integration. <br>
Mitigation: Audit the generated server code before execution and avoid placing real secrets in examples or generated documentation. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/njengah/mcp-scaffolder) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown containing scaffolded file contents, JSON configuration snippets, and setup instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated code and configuration should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
