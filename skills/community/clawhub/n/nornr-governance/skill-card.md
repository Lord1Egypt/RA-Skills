## Description: <br>
NORNR MCP Control adds an approval and audit layer before consequential MCP or OpenClaw actions so agents can proceed, queue, or block work before spend or vendor-side execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Onechan](https://clawhub.ai/user/Onechan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations teams use this skill to run NORNR checks before paid, vendor-side, or policy-sensitive OpenClaw and MCP actions. It helps route approval-required or blocked actions to named review while preserving audit and finance records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is used around paid or policy-sensitive actions, so a broad or reused NORNR API key could increase approval and audit exposure. <br>
Mitigation: Use a dedicated least-privilege NORNR API key with only the scopes needed for the selected command set. <br>
Risk: Autonomous workflows could continue after approval-required, queued, blocked, anomalous, or review-required responses if client routing is misconfigured. <br>
Mitigation: Verify that agents treat those responses as stop states and require a named human operator before continuing. <br>
Risk: Governance behavior depends on the pinned nornr-agentpay dependency used by the local bridge. <br>
Mitigation: Review the pinned nornr-agentpay release before production use, especially in finance-sensitive workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Onechan/nornr-governance) <br>
- [Artifact-stated NORNR MCP package repo](https://github.com/NORNR/nornr-mcp-control) <br>
- [Artifact-stated NORNR Python SDK repo](https://github.com/NORNR/sdk-py) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Text] <br>
**Output Format:** [Markdown guidance with shell commands and CLI-mediated NORNR responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires NORNR_API_KEY and the pinned nornr-agentpay dependency.] <br>

## Skill Version(s): <br>
0.1.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
