## Description: <br>
审查MCP Server工具实现是否符合接口设计准则。当用户要求review、检查、审查MCP工具定义，或说"check一下工具设计"、"review mcp tools"、"工具设计有没有问题"时使用。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sawzhang](https://clawhub.ai/user/sawzhang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to review MCP Server tool definitions against ten interface design criteria and receive a structured report with scores, top issues, and concrete improvement suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads and searches local MCP-related source files and mock data, so sensitive content in the target project may enter the agent review context. <br>
Mitigation: Run it on specific project folders or exact file paths, and avoid repositories containing secrets or real personal data unless that exposure is acceptable. <br>
Risk: The review can produce incorrect or misleading design guidance for an MCP tool. <br>
Mitigation: Have a developer review the report before applying suggested changes or deploying the reviewed MCP server. <br>


## Reference(s): <br>
- [MCP API Design Guide](artifact/MCP_API_DESIGN_GUIDE.md) <br>
- [Mcp Review on ClawHub](https://clawhub.ai/sawzhang/mcp-review) <br>
- [McDonald's China MCP documentation](https://open.mcd.cn/mcp/doc) <br>
- [McDonald's China MCP Server GitHub](https://github.com/M-China/mcd-mcp-server) <br>
- [Amap MCP Server overview](https://lbs.amap.com/api/mcp-server/summary) <br>
- [Community Amap MCP Server GitHub](https://github.com/sugarforever/amap-mcp-server) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Guidance] <br>
**Output Format:** [Markdown review report with per-tool scoring tables, issue summary, and prioritized recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Chinese-language review output focused on MCP tool interface design.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
