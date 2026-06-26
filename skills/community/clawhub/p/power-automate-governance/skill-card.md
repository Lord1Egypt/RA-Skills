## Description: <br>
Govern Power Automate flows and Power Apps at scale using the FlowStudio MCP cached store by classifying flows, detecting orphaned resources, auditing connector usage, enforcing compliance standards, managing notification rules, and computing governance scores. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ninihen1](https://clawhub.ai/user/ninihen1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Power Platform administrators and governance teams use this skill to review tenant-wide Power Automate and Power Apps metadata, classify flows, identify compliance gaps and orphaned resources, and prepare controlled governance updates through FlowStudio MCP. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent through governance workflows that stop flows, migrate flows into solutions, or change notification and monitoring metadata. <br>
Mitigation: Before making changes, require the agent to list the tenant, environment, flows, intended updates, and request explicit approval. <br>
Risk: FlowStudio store updates may change governance contacts, tags, monitoring settings, or notification recipients in cached metadata. <br>
Mitigation: Confirm the target environment and flow IDs before each write and review the proposed values for ownership, support, monitoring, and notification fields. <br>


## Reference(s): <br>
- [FlowStudio MCP](https://mcp.flowstudio.app) <br>
- [ClawHub skill page](https://clawhub.ai/ninihen1/power-automate-governance) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with tool-call plans, audit summaries, and configuration values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FLOWSTUDIO_MCP_TOKEN and FlowStudio for Teams or MCP Pro+ access for store tool workflows.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
