## Description:

Automates OriginLab Origin Pro through the origin-pro MCP server for worksheets, graphs, publication styling, fitting, LabTalk, and verified figure export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leima-max](https://clawhub.ai/user/leima-max)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and researchers use this skill to automate Origin Pro workflows from an agent, including worksheet creation, scientific plotting, curve fitting, publication figure styling, LabTalk execution, and figure export.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: LabTalk execution can perform powerful Origin operations when prompted.

Mitigation: Use trusted prompts and data, and avoid or disable run_labtalk unless the workflow explicitly requires it.

Risk: Project and worksheet tools can change or clear local Origin work.

Mitigation: Keep backups, confirm before starting a new project, and prefer disposable Origin projects for testing.

Risk: Graph export operations write files to local paths.

Mitigation: Verify export paths before execution and prefer a constrained output directory.

Risk: Origin modal dialogs or cold-start behavior can cause MCP calls to hang or time out.

Mitigation: Start Origin Pro before COM-dependent operations and check for blocking dialogs if a call stalls.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/leima-max/skills/origin-pro-mcp)
- [Security Notes](docs/SECURITY.md)
- [Publication Figure Workflow](skills/publication-figure.md)
- [Project homepage](https://github.com/leima-max/origin-pro-mcp-skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code blocks, MCP tool calls, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include Origin project, worksheet, graph, fitting, styling, LabTalk, and export instructions that act on a local Windows Origin Pro session.]

## Skill Version(s):

0.2.1 (source: server release metadata and pyproject.toml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
