## Description: <br>
IP geolocation lookup via MCP for IP location, ASN, country, city, domain-to-IP, and batch IP lookup requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marc-chen](https://clawhub.ai/user/marc-chen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and support teams use this skill to look up public IP geolocation and ASN details, including batch IP checks and domain-to-IP geolocation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Public IP addresses and domain-resolved public IPs are sent to an external MCP service. <br>
Mitigation: Use the skill for public IP and public domain geolocation, and avoid sensitive internal infrastructure details unless external disclosure is acceptable. <br>
Risk: Private or reserved IP addresses can expose internal network details if queried externally. <br>
Mitigation: Keep the documented and script-level private/reserved IP blocking in place before external lookup. <br>


## Reference(s): <br>
- [MCP API Reference](references/api.md) <br>
- [MCP GeoIP endpoint](https://ip.api4claw.com/mcp) <br>
- [ClawHub release page](https://clawhub.ai/marc-chen/ip-geo-location-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, API Calls] <br>
**Output Format:** [Concise text or Markdown tables, with JSON returned by helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns IP, country, country code, province or state, city, ASN, ASN organization, or explicit validation/error status.] <br>

## Skill Version(s): <br>
0.1.3 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
