## Description:

Network scanning MCP server wrapping nmap that provides structured JSON tools for authorized host discovery, port scanning, service and OS detection, NSE script execution, vulnerability scanning, audit logging, scan persistence, and CIDR scope enforcement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sbmilburn](https://clawhub.ai/user/sbmilburn)

### License/Terms of Use:

MIT

## Use Case:

Developers, security engineers, and authorized auditors use this MCP server to let an AI agent run scoped nmap discovery, port scanning, service fingerprinting, NSE checks, and vulnerability-oriented scans on networks they are permitted to assess.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: High-impact network scanning with weak parameter and scope controls could affect systems outside the intended assessment.

Mitigation: Install only in a dedicated, tightly scoped environment and narrow allowed_cidrs before use.

Risk: Hostname targets may resolve unexpectedly and widen scan scope.

Mitigation: Prefer explicit IP addresses or CIDR ranges for authorized targets.

Risk: The custom scan tool can expose broader nmap behavior than the purpose-built tools.

Mitigation: Use purpose-built scan tools where possible and avoid nmap_custom_scan unless necessary.

Risk: Saved scan output and audit logs may disclose sensitive network inventory and vulnerability information.

Mitigation: Treat persisted scan data as sensitive and restrict access, retention, and sharing.

Risk: Unpinned dependencies can change runtime behavior between installs.

Mitigation: Pin Python dependencies before production deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sbmilburn/skills/nmap-mcp)
- [nmap](https://nmap.org)
- [Model Context Protocol](https://modelcontextprotocol.io)
- [OpenClaw](https://openclaw.ai)
- [mcporter](https://mcporter.dev)

## Skill Output:

**Output Type(s):** [JSON, Text, Files]

**Output Format:** [Structured JSON strings from MCP tools, with persisted scan records as JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires configured allowed CIDRs; scan results and audit logs may contain sensitive network data.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
