## Description: <br>
Elite Agentic Finance SDK for OpenClaw, Claude & Autonomous Trading Bots. Real-time market data, canonical asset resolution, 100+ endpoints for crypto, DeFi, stocks. Sub-50ms latency. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[StrykrAgent](https://clawhub.ai/user/StrykrAgent) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and external users use this skill to add PRISM financial market data, asset resolution, and SDK/MCP integration guidance to agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API keys may be exposed through prompts, logs, or shared files during SDK setup. <br>
Mitigation: Keep the Prism API key out of prompts, logs, and shared files, and use environment or secret-management practices when configuring agents. <br>
Risk: Financial outputs may be mistaken for trading or betting instructions. <br>
Mitigation: Treat outputs as informational market data and require human review before connecting them to live trading or betting systems. <br>
Risk: Dependency or MCP server changes could alter runtime behavior after installation. <br>
Mitigation: Verify the npm package and optional MCP server repository before installing, and pin versions where practical. <br>


## Reference(s): <br>
- [PRISM API Documentation](https://api.prismapi.ai/docs) <br>
- [PRISM SDK npm Package](https://www.npmjs.com/package/prismapi-sdk) <br>
- [PRISM OS SDK GitHub Repository](https://github.com/Strykr-Prism/PRISM-OS-SDK) <br>
- [PRISM MCP Server GitHub Repository](https://github.com/Strykr-Prism/PRISM-MCP-Server) <br>
- [PRISM Website](https://prismapi.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash and TypeScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node for SDK workflows; API key handling should be reviewed before use.] <br>

## Skill Version(s): <br>
0.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
