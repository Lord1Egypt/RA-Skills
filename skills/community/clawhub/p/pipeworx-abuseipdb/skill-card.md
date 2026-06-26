## Description: <br>
Check, report, and retrieve abuse confidence scores and details for IP addresses using the AbuseIPDB v2 API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[b-gutman](https://clawhub.ai/user/b-gutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security analysts use this skill to configure an agent connection for AbuseIPDB v2 IP reputation checks, abuse reports, and blacklist retrieval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send IP addresses and abuse-report details to external services through a hosted MCP gateway. <br>
Mitigation: Use it only when the Pipeworx gateway is trusted and the user accepts external AbuseIPDB lookups. <br>
Risk: The report_ip action can submit abuse reports to AbuseIPDB. <br>
Mitigation: Require explicit human approval before using report_ip, including review of the IP address and category IDs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/b-gutman/pipeworx-abuseipdb) <br>
- [Publisher profile](https://clawhub.ai/user/b-gutman) <br>
- [Pipeworx AbuseIPDB MCP gateway](https://gateway.pipeworx.io/abuseipdb/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown text with JSON MCP server configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May perform external AbuseIPDB lookups or submit reports through a hosted MCP gateway.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
