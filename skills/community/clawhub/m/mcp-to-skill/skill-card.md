## Description: <br>
Converts MCP servers into standalone skill packages with zero runtime MCP dependency. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JalanChao](https://clawhub.ai/user/JalanChao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to convert an MCP server or pasted MCP tool schema into a ready-to-use standalone skill package. It helps inspect tool schemas, infer equivalent shell commands or helper scripts, separate public configuration from secrets, and register the generated skill with supported agent environments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can inspect or run untrusted MCP server code while discovering tool schemas and source behavior. <br>
Mitigation: Use trusted MCP servers in a clean sandbox and review generated commands before testing or registration. <br>
Risk: Generated skills may include inferred shell commands, helper scripts, and live read-only command tests that were not validated against source code. <br>
Mitigation: Review all inferred commands and skip automatic live tests unless the target, inputs, and side effects are understood. <br>
Risk: The workflow can persist generated agent skills and secrets-related files. <br>
Mitigation: Keep secrets in gitignored secrets.json files, use least-privilege tokens, and manually review generated skill files before registration. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/JalanChao/mcp-to-skill) <br>
- [Publisher profile](https://clawhub.ai/user/JalanChao) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown skill files with JSON configuration, optional helper scripts, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate gitignored secrets templates and registration commands for supported agent frameworks.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
