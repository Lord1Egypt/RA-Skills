## Description: <br>
Universal adapter diagnostics for Model Context Protocol (MCP) that detects connection issues between agents and external tools and provides deep-trace debugging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tmstudio667-commits](https://clawhub.ai/user/tmstudio667-commits) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to diagnose MCP server connectivity, inspect protocol handshakes and latency, and recover from local MCP adapter failures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may inspect all configured MCP targets during broad diagnostics. <br>
Mitigation: Prefer explicit server names or dry-run style requests, and avoid sensitive or production-linked integrations unless the diagnostic scope has been reviewed. <br>
Risk: Automatic repair behavior may restart crashed MCP servers or change local adapter state. <br>
Mitigation: Review what will be restarted or changed before enabling automatic fixes, especially for production or sensitive integrations. <br>


## Reference(s): <br>
- [OpenClaw MCP Debugger on ClawHub](https://clawhub.ai/tmstudio667-commits/openclaw-mcp-debugger) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Guidance, Shell commands] <br>
**Output Format:** [Markdown diagnostics with command suggestions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include MCP health checks, latency audit notes, and repair guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
