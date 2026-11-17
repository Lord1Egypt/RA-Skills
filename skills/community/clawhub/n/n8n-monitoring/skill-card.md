## Description:

Monitor and debug n8n workflow executions via webhook with health checks, failure analysis, error debugging, and formatted alerting templates for Telegram or other channels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samirsaci](https://clawhub.ai/user/samirsaci)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to monitor self-hosted n8n workflow health, identify failing workflows, inspect failed nodes and errors, and generate concise alerts for operational follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to import an external n8n workflow and provide n8n API credentials.

Mitigation: Review the imported workflow before activating it and use a dedicated read-only n8n service account.

Risk: The monitoring webhook can expose workflow execution details if it is reachable without strong access controls.

Mitigation: Protect the webhook with strong authentication or private-network controls.

Risk: Workflow names, node details, and error messages may contain sensitive operational data.

Mitigation: Sanitize workflow details before sending them to Telegram, logs, or other notification channels.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/samirsaci/skills/n8n-monitoring)
- [n8n workflow template](https://n8n.supply-science.com/workflows/DevOps/AI_Agent_for_Debugging_Workflow_Executions)
- [Video tutorial](https://youtu.be/oJzNnHIusZs)
- [Original article](https://towardsdatascience.com/deploy-your-ai-assistant-to-monitor-and-debug-n8n-workflows-using-claude-and-mcp/)
- [MCP server reference](https://github.com/samirsaci/mcp-n8n-monitor)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with JSON request examples, shell commands, configuration snippets, and alert templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces health summaries, workflow failure analysis, error-debugging guidance, and Telegram-style alert text from webhook responses.]

## Skill Version(s):

1.0.0 (source: server release metadata and submission metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
