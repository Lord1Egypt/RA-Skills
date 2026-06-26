## Description: <br>
Use when the user wants to connect to, test, or use the McDonalds service at mcp.mcd.cn, including checking authentication, probing MCP endpoints, listing tools, or calling McDonalds MCP tools through a reusable local CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1052666](https://clawhub.ai/user/1052666) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to test connectivity and authentication for the McDonalds MCP service, list available tools, and invoke selected tools through a local Python CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A live McDonalds MCP token can be used to create orders or change account data without clear built-in confirmation safeguards. <br>
Mitigation: Require explicit user confirmation before order creation, coupon binding, points redemption, or address changes, and review every tool name and JSON argument before execution. <br>
Risk: Terminal output and saved JSON reports may contain sensitive account data. <br>
Mitigation: Treat command output and report files as sensitive, avoid sharing them, and remove reports when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/1052666/mcdonalds-skill) <br>
- [McDonalds MCP service endpoint](https://mcp.mcd.cn) <br>
- [McDonalds MCP token portal](https://open.mcd.cn/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, JSON, API calls, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can save smoke-test reports as JSON files; uses bearer-token authentication.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
