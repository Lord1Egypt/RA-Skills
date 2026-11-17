## Description:

Foundation skill for Power Automate via FlowStudio MCP that covers auth setup, reusable Python and Node.js MCP helpers, tool discovery, and oversized-response handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ninihen1](https://clawhub.ai/user/ninihen1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation teams use this skill to connect an agent to a FlowStudio MCP server for Power Automate and prepare reliable auth, tool discovery, response parsing, and handoff to specialized build, debug, monitoring, or governance workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent access to FlowStudio MCP can expose or change Power Automate environments according to the permissions behind the configured token.

Mitigation: Use an account whose Power Platform permissions match the intended task and review proposed flow changes or run-control actions before execution.

Risk: JWT/API keys are sensitive credentials that may be exposed through logs, transcripts, or copied examples.

Mitigation: Keep tokens out of shared transcripts and logs, pass them only through the required x-api-key header, and rotate them if exposed.

Risk: Large flow, connector, or run-output responses may include tenant data and can overwhelm an agent context.

Mitigation: Parse spilled responses, extract only the fields needed for the task, and summarize results instead of echoing raw JSON.

## Reference(s):

- [MCP Bootstrap](references/MCP-BOOTSTRAP.md)
- [FlowStudio MCP Tool Response Catalog](references/tool-reference.md)
- [FlowStudio MCP Action Types Reference](references/action-types.md)
- [FlowStudio MCP Connection References](references/connection-references.md)
- [FlowStudio MCP](https://mcp.flowstudio.app)
- [ClawHub Skill Page](https://clawhub.ai/ninihen1/skills/power-automate-mcp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python, JavaScript, JSON, and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a FlowStudio MCP subscription or compatible Power Automate MCP server; outputs should avoid exposing JWT/API keys or large raw tool responses.]

## Skill Version(s):

1.2.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
