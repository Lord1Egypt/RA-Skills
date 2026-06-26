## Description: <br>
Control OriginLab Origin Pro through the origin-pro MCP server for worksheets, graphs, publication styling, fitting, LabTalk, and verified figure export. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leima-max](https://clawhub.ai/user/leima-max) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and researchers use this skill to automate Origin Pro workflows through a local MCP server, including worksheet operations, scientific plotting, curve fitting, LabTalk execution, and figure export. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad unsandboxed control over a running Origin Pro session and local project/files. <br>
Mitigation: Install only from a trusted publisher, keep important Origin projects saved or backed up, and avoid use with untrusted prompts, labels, names, or paths. <br>
Risk: Raw LabTalk execution, project creation, project load/save, imports, and exports can change the current Origin session or overwrite local files. <br>
Mitigation: Require explicit confirmation before LabTalk, new_project, project load/save, imports, or exports over existing files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/leima-max/origin-pro-mcp) <br>
- [Security notes](docs/SECURITY.md) <br>
- [Publication figure workflow](skills/publication-figure.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON configuration snippets, MCP tool calls, and generated Origin project or figure files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Windows, Windows Python, Origin Pro 2020 or newer, and the local origin-pro MCP server.] <br>

## Skill Version(s): <br>
0.2.1 (source: server release evidence and pyproject.toml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
