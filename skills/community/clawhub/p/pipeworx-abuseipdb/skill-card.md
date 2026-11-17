## Description:

Check, report, and retrieve abuse confidence scores and details for IP addresses using the AbuseIPDB v2 API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[b-gutman](https://clawhub.ai/user/b-gutman)

### License/Terms of Use:

MIT-0

## Use Case:

Security analysts and incident response teams use this skill to check IP reputation, submit abuse reports, and retrieve AbuseIPDB blacklist information from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: IP lookups and reports may contain sensitive operational, personal, or investigation data routed through a third-party MCP gateway.

Mitigation: Review the gateway operator and avoid sending sensitive data unless the operator and data handling are acceptable for the use case.

Risk: The report_ip capability can submit external abuse reports.

Mitigation: Require explicit user confirmation before sending any abuse report.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/b-gutman/skills/pipeworx-abuseipdb)
- [AbuseIPDB v2 API endpoint](https://api.abuseipdb.com/api/v2)
- [Pipeworx AbuseIPDB MCP gateway](https://gateway.pipeworx.io/abuseipdb/mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration]

**Output Format:** [Markdown or text responses with JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include IP reputation details, abuse confidence scores, ISP information, blacklist entries, and abuse report submission guidance.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
