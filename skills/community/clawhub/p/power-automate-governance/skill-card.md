## Description:

Govern Power Automate flows and Power Apps at scale using the FlowStudio MCP cached store to classify flows, detect orphaned resources, audit connector usage, enforce compliance standards, manage notification rules, and compute governance scores.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ninihen1](https://clawhub.ai/user/ninihen1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, administrators, and platform governance teams use this skill to review and classify Power Automate flows and Power Apps, identify orphaned resources, audit connector usage, manage notification rules, and produce governance reports through FlowStudio MCP.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Some workflows can stop live Power Automate flows or change governance metadata in bulk.

Mitigation: Confirm target flows, business owners, rollback plan, and notification recipients before allowing stop, migration, or bulk-update actions.

Risk: Governance metadata updates affect the FlowStudio cache and may not change actual Power Automate ownership or portal-visible settings.

Mitigation: Tell users when Power Platform admin center or PowerShell action is required for actual ownership transfer, app reassignment, or deletion.

Risk: The FlowStudio security field contains structured data that can be overwritten by an unsafe plain-text update.

Mitigation: Use tags such as #security-reviewed for review status and avoid overwriting the structured security field.

Risk: Large tenant audits can require many per-flow detail calls.

Mitigation: Prefer list-level metrics and scope expensive connector or security audits to monitored flows unless the user confirms a broader scan.

## Reference(s):

- [FlowStudio MCP](https://mcp.flowstudio.app)
- [FlowStudio MCP Pricing](https://mcp.flowstudio.app/pricing)
- [ClawHub Skill Page](https://clawhub.ai/ninihen1/skills/power-automate-governance)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with structured findings, workflow steps, tool-call guidance, and optional code or shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend metadata updates, flow state changes, notification changes, solution migration steps, or governance reports for user confirmation.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
