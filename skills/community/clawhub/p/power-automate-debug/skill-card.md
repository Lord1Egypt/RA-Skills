## Description:

Debug failing Power Automate cloud flows using the FlowStudio MCP server by inspecting action-level inputs and outputs to identify root causes beyond top-level Graph API status codes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ninihen1](https://clawhub.ai/user/ninihen1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation engineers use this skill to diagnose and repair failing Microsoft Power Automate cloud flows through FlowStudio MCP diagnostics. It helps trace failed runs, inspect action inputs and outputs, identify connector or expression failures, apply fixes, and verify them by resubmitting prior runs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to update, resubmit, or trigger live Power Automate flows.

Mitigation: Require explicit human approval before any flow update, resubmit, or trigger action, especially for production flows.

Risk: Resubmitting or triggering flows can duplicate side effects such as emails, writes, approvals, or downstream API calls.

Mitigation: Review the target flow's downstream actions before replaying a run and use controlled test payloads or non-production environments when possible.

Risk: Run inputs and outputs may contain tokens, business records, or other sensitive data.

Mitigation: Redact secrets and sensitive payload fields before placing diagnostic details into prompts, logs, or shared summaries.

## Reference(s):

- [Power Automate Debug Skill Page](https://clawhub.ai/ninihen1/skills/power-automate-debug)
- [FlowStudio MCP](https://mcp.flowstudio.app)
- [Common Power Automate Errors](references/common-errors.md)
- [FlowStudio MCP Debug Workflow](references/debug-workflow.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with Python examples, diagnostic decision trees, and Power Automate configuration recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require access to a FlowStudio MCP server with a valid JWT and a FlowStudio MCP subscription.]

## Skill Version(s):

1.2.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
