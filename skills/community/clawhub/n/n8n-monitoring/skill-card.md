## Description: <br>
Monitor and debug n8n workflow executions via webhook. Provides health checks (GREEN/YELLOW/RED), failure analysis, error debugging, and formatted alerting templates for Telegram or other channels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samirsaci](https://clawhub.ai/user/samirsaci) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to monitor self-hosted n8n workflow health, identify failing workflows, inspect execution errors, and generate concise alert text for operational channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Workflow execution errors and alert payloads may contain tokens, customer data, internal URLs, or stack traces. <br>
Mitigation: Sanitize errors and logs before sending alerts, and avoid including raw execution payloads or sensitive details in Telegram or other notification channels. <br>
Risk: The skill depends on a trusted n8n instance and webhook workflow. <br>
Mitigation: Use HTTPS and authentication where possible, restrict webhook access, and install it only for n8n instances and webhook workflows the user trusts. <br>


## Reference(s): <br>
- [n8n Workflow Template](https://n8n.supply-science.com/workflows/DevOps/AI_Agent_for_Debugging_Workflow_Executions) <br>
- [Video Tutorial](https://youtu.be/oJzNnHIusZs) <br>
- [Original Article](https://towardsdatascience.com/deploy-your-ai-assistant-to-monitor-and-debug-n8n-workflows-using-claude-and-mcp/) <br>
- [MCP Server Reference](https://github.com/samirsaci/mcp-n8n-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON request examples and alert templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operational summaries, health classifications, debugging guidance, and notification templates based on n8n webhook responses.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
