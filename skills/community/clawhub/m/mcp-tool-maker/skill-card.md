## Description:

Generates MCP tool registration code from top-level functions in Python source files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[534422530](https://clawhub.ai/user/534422530)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to scan Python files, identify callable top-level functions, and generate MCP-compatible wrapper code for local server integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated wrappers can expose broad local Python functions as MCP tools.

Mitigation: Review generated code and approve each wrapped function before adding it to an MCP server.

Risk: Untrusted source files or manipulated module names can influence generated Python imports and wrapper behavior.

Mitigation: Use trusted source files with simple valid module names and scan generated output before execution.

Risk: Writing generated output over an existing server file can replace or weaken server behavior.

Mitigation: Write to a new review file first and merge changes manually after inspection.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/534422530/skills/mcp-tool-maker)
- [Bilibili MCP and tool-use reference](https://www.bilibili.com/video/BV1vhV36ZEFu)
- [Bilibili MCP agent reference](https://www.bilibili.com/video/BV1aQPrzYEhJ)

## Skill Output:

**Output Type(s):** [Text, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with Python code and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write generated MCP wrapper code to a Python file when an output path is provided.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
