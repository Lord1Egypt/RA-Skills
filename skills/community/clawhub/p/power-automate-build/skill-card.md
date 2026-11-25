## Description:

Build, scaffold, and deploy Power Automate cloud flows using the FlowStudio MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ninihen1](https://clawhub.ai/user/ninihen1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create, update, deploy, verify, and test Power Automate cloud flow definitions through FlowStudio MCP without opening the Power Automate portal.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An agent using this skill can create or update live Power Automate flows through FlowStudio MCP, which may change running automations or cause external side effects during testing.

Mitigation: Use least-privilege connections, require explicit approval before any test run or trigger change, and verify the final deployed trigger and flow state after testing.

Risk: A temporary schema-free HTTP trigger used for testing can remain on a live flow if testing or rollback fails.

Mitigation: Avoid the temporary HTTP-trigger recipe unless rollback is guaranteed, restore the production trigger immediately after testing, and verify the deployed trigger state.

Risk: Button, Power Apps, or Skills trigger tests may run with missing required inputs as null values.

Mitigation: Pass a complete test body, check warnings from trigger_live_flow, and cancel or retry with full inputs when a required-input warning appears.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ninihen1/skills/power-automate-build)
- [FlowStudio MCP](https://mcp.flowstudio.app)
- [Power Automate workflow definition schema](https://schema.management.azure.com/providers/Microsoft.Logic/schemas/2016-06-01/workflowdefinition.json#)
- [Flow Definition Schema](references/flow-schema.md)
- [Trigger Types](references/trigger-types.md)
- [Common Build Patterns](references/build-patterns.md)
- [Action Patterns: Core](references/action-patterns-core.md)
- [Action Patterns: Data Transforms](references/action-patterns-data.md)
- [Action Patterns: Connectors](references/action-patterns-connectors.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON, Python, and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Power Automate flow definitions and live MCP tool calls that require user approval before execution.]

## Skill Version(s):

1.2.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
