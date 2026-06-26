## Description: <br>
Real-time cryptocurrency prices, network fee estimates, and Lightning Network statistics via L402 API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[haveblue997](https://clawhub.ai/user/haveblue997) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this MCP skill to retrieve crypto market prices, estimate transaction fees, and check Lightning Network health for portfolio monitoring, fee planning, and market-data workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Package, tool-name, and environment-variable mismatches could cause agents to install or configure a different package than intended. <br>
Mitigation: Verify the intended npm package name before installation, pin the npx package version when possible, and use the environment variable expected by the runtime. <br>
Risk: API requests may be metered through L402 micropayments. <br>
Mitigation: Review pricing and usage expectations before enabling the skill in workflows that can make repeated requests. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/haveblue997/mcp-crypto-data) <br>
- [Blue-Trianon-Ventures GitHub profile](https://github.com/Blue-Trianon-Ventures) <br>
- [NautDev API base URL](https://api.nautdev.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, API Calls, configuration] <br>
**Output Format:** [MCP tool responses containing JSON-formatted text, plus MCP server configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides price lookup by coin identifier and parameterless fee and Lightning Network statistics tools.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, SKILL.md frontmatter, and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
