## Description: <br>
Enables OpenClaw MCP support and guides agents through adding the engine_mcp_server configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rxjhfmf](https://clawhub.ai/user/rxjhfmf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to enable MCP and configure a remote Finance Engine MCP server for quantitative strategy backtesting and financial analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill publishes a hardcoded authorization value for a remote financial MCP service. <br>
Mitigation: Replace the embedded Authorization value with a scoped credential before use and avoid committing MCP configuration files. <br>
Risk: The remote MCP service may receive strategy, market, or financial-analysis data. <br>
Mitigation: Send data only when the service operator and retention practices are trusted for the intended use case. <br>
Risk: Credential and data risks are under-disclosed by the skill text. <br>
Mitigation: Review the security guidance before installation and document any organization-specific handling requirements. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rxjhfmf/openclaw-engine-mcp-setup) <br>
- [engine_mcp_server endpoint](https://mcp.hzyotoy.com/engine/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, code] <br>
**Output Format:** [Markdown with YAML and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes MCP server configuration examples and sample JSON-RPC tool calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
