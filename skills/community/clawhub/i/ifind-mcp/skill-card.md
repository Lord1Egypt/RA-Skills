## Description: <br>
Tonghuashun iFinD financial data MCP skill for querying A-share stock, public fund, macroeconomic, and news information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xingjianliu0417](https://clawhub.ai/user/xingjianliu0417) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and financial-data agents use this skill to configure and call iFinD MCP endpoints for stock summaries, stock screening, fund profile and performance data, macroeconomic indicators, and company news. It is intended for workflows that need authenticated access to iFinD financial data through mcporter. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The iFinD Authorization value is a credential used by the MCP servers. <br>
Mitigation: Treat the Authorization value as a secret, keep ~/.openclaw/mcporter.json private, and rotate the token if it is exposed. <br>
Risk: Financial-data queries may contain confidential research or regulated information. <br>
Mitigation: Avoid sending confidential research or regulated information in queries unless the deployment has approved that use of iFinD. <br>
Risk: The helper script is rough and depends on a local mcporter installation and configuration path. <br>
Mitigation: Review the script and verify the mcporter path, configuration file, and target MCP server before using it in an automated workflow. <br>


## Reference(s): <br>
- [iFinD MCP API Reference](references/API.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/xingjianliu0417/ifind-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup instructions and MCP call patterns; live results depend on valid iFinD authorization and remote MCP service availability.] <br>

## Skill Version(s): <br>
1.3.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
