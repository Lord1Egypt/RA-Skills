## Description: <br>
An MCP server that wraps nmap with 14 tools for authorized host discovery, port scanning, service and OS detection, NSE script execution, vulnerability scanning, and structured JSON scan results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sbmilburn](https://clawhub.ai/user/sbmilburn) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Security engineers and authorized network auditors use this skill with an MCP-capable agent to run scoped nmap scans, collect structured findings, and retrieve persisted scan results during approved security audits or asset-discovery work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents can run nmap scans with real dual-use network-security impact. <br>
Mitigation: Use only on networks you are authorized to test and narrow config.yaml to the exact approved CIDRs before running scans. <br>
Risk: Audit logs and saved scan JSON may contain sensitive network information. <br>
Mitigation: Protect or periodically delete audit.log and scans/*.json according to the applicable retention policy. <br>
Risk: Granting cap_net_raw to nmap gives the local binary raw-socket capability. <br>
Mitigation: Apply setcap only when required, limit local users who can execute nmap, and review the capability after nmap upgrades. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/sbmilburn/nmap-mcp) <br>
- [Nmap](https://nmap.org) <br>
- [Model Context Protocol](https://modelcontextprotocol.io) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [mcporter](https://mcporter.dev) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON] <br>
**Output Format:** [Structured JSON scan results and Markdown setup guidance with shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scan results are persisted as JSON files by the MCP server; audit log entries are JSON lines.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
