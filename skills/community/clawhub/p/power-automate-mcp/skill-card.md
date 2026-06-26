## Description: <br>
Foundation skill for connecting agents to Power Automate through FlowStudio MCP, covering authentication setup, reusable Python and Node.js helpers, tool discovery, and oversized-response handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ninihen1](https://clawhub.ai/user/ninihen1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to set up FlowStudio MCP access for Power Automate, discover relevant tools, and prepare an agent to inspect, modify, debug, monitor, or govern flows through companion workflow skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a sensitive FlowStudio MCP token that can give an agent access to Power Automate resources. <br>
Mitigation: Use least-privileged credentials, keep FLOWSTUDIO_MCP_TOKEN out of prompts and logs, and rotate or revoke the token when access is no longer needed. <br>
Risk: Live flow operations can create, update, start, stop, cancel, resubmit, or trigger Power Automate flows. <br>
Mitigation: Require explicit confirmation before any state-changing or live-run action, and verify the target environment and flow identifiers before execution. <br>
Risk: Large MCP responses and temporary spill files may contain tenant, flow, run, connector, or payload data. <br>
Mitigation: Treat spill files as sensitive, parse only the fields needed for the task, and summarize results rather than returning raw JSON unless explicitly required. <br>


## Reference(s): <br>
- [Power Automate Mcp on ClawHub](https://clawhub.ai/ninihen1/power-automate-mcp) <br>
- [FlowStudio MCP](https://mcp.flowstudio.app) <br>
- [MCP Bootstrap Quick Reference](artifact/references/MCP-BOOTSTRAP.md) <br>
- [FlowStudio MCP Tool Response Catalog](artifact/references/tool-reference.md) <br>
- [FlowStudio MCP Connection References](artifact/references/connection-references.md) <br>
- [FlowStudio MCP Action Types Reference](artifact/references/action-types.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown with Python, Node.js, JSON, and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference FlowStudio MCP tool schemas and large spill files; summarize sensitive or oversized outputs instead of echoing raw payloads.] <br>

## Skill Version(s): <br>
1.2.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
