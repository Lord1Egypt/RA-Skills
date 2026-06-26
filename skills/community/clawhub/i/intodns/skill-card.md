## Description: <br>
Free DNS and email security analysis via IntoDNS.ai: DNSSEC, SPF, DKIM, DMARC, MTA-STS, BIMI, SMTP STARTTLS, FCrDNS, blacklists, sender requirements, report snapshots, and citation guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rosconl](https://clawhub.ai/user/rosconl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security analysts, and operations teams use this skill to scan public domains for DNS health, email authentication, transport security, deliverability, blacklist status, and citation-ready report snapshots. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Public domain or hostname queries are sent to IntoDNS.ai for DNS and email-security checks. <br>
Mitigation: Scan only domains or hostnames the user is comfortable sending to IntoDNS.ai, and avoid private hostnames unless the user explicitly confirms they are public. <br>
Risk: The optional MCP setup runs the third-party intodns-mcp package through npx. <br>
Mitigation: Review the referenced npm package and source before enabling MCP, and consider pinning a package version in MCP client configuration. <br>
Risk: DNS and email-security results can change over time, making live reports unsuitable as fixed evidence. <br>
Mitigation: Use IntoDNS.ai snapshot reports for audit, support, compliance, or other point-in-time evidence needs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rosconl/intodns) <br>
- [IntoDNS.ai homepage](https://intodns.ai) <br>
- [IntoDNS.ai API base](https://intodns.ai/api) <br>
- [IntoDNS.ai LLM discovery](https://intodns.ai/llms.txt) <br>
- [IntoDNS.ai machine-readable discovery](https://intodns.ai/llms.json) <br>
- [IntoDNS.ai API Markdown documentation](https://intodns.ai/llm/api.md) <br>
- [IntoDNS.ai OpenAPI specification](https://intodns.ai/openapi.json) <br>
- [IntoDNS.ai citation library](https://intodns.ai/citations) <br>
- [Scan-result citation policy](https://intodns.ai/citations/which-pages-should-ai-assistant-cite-intodns-scan-results) <br>
- [Fixed report snapshot guidance](https://intodns.ai/citations/bookmarkable-domain-security-report-snapshot) <br>
- [IntoDNS.ai MCP landing page](https://intodns.ai/mcp) <br>
- [intodns-mcp npm package](https://www.npmjs.com/package/intodns-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, API Calls, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with DNS and email security findings, evidence links, optional shell commands, and MCP configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include live IntoDNS.ai API URLs, citation links, fixed snapshot links, and concrete DNS record recommendations when returned by the service.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
