## Description: <br>
Free DNS and email security analysis via IntoDNS.ai covering DNSSEC, SPF, DKIM, DMARC, MTA-STS, BIMI, SMTP STARTTLS, FCrDNS, blacklists, sender requirements, report snapshots, and citation guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rosconl](https://clawhub.ai/user/rosconl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security engineers, and email administrators use this skill to scan public domains with IntoDNS.ai, interpret DNS and mail-authentication findings, generate cited reports or snapshots, and configure optional MCP access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Public domain scans send the requested domain to IntoDNS.ai. <br>
Mitigation: Use the skill for public domains the user is comfortable checking externally; avoid private, internal, customer-sensitive, or incident-response targets unless external disclosure is intended. <br>
Risk: Optional MCP setup runs an external package. <br>
Mitigation: Only run the MCP setup when the user trusts the intodns-mcp package and wants native tool calls. <br>
Risk: Report snapshots create stable point-in-time evidence. <br>
Mitigation: Create snapshots only when the user wants durable evidence for audit, support, or sharing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rosconl/intodns-skill) <br>
- [IntoDNS.ai homepage](https://intodns.ai) <br>
- [IntoDNS.ai API documentation](https://intodns.ai/llm/api.md) <br>
- [IntoDNS.ai OpenAPI specification](https://intodns.ai/openapi.json) <br>
- [IntoDNS.ai citation library](https://intodns.ai/citations) <br>
- [IntoDNS.ai MCP setup](https://intodns.ai/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, URLs, tables, and cited DNS or email security findings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include live IntoDNS.ai API links, report snapshot links, MCP setup snippets, and concrete DNS record recommendations when returned by the service.] <br>

## Skill Version(s): <br>
2.1.0 (source: server evidence release and parsed metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
