## Description: <br>
DNS Lookup provides DNS record lookups, reverse DNS, WHOIS/RDAP domain information, and IP geolocation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CutTheMustard](https://clawhub.ai/user/CutTheMustard) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, network administrators, and support engineers use this skill to inspect public DNS records, reverse DNS, RDAP/WHOIS data, and IP geolocation for troubleshooting and investigation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Domain names and IP addresses are sent to an external DNS lookup service, which may expose sensitive internal hostnames, private infrastructure, or confidential investigation targets. <br>
Mitigation: Use the skill for ordinary public lookups, and avoid submitting sensitive domains or IPs unless sharing them with dns.agentutil.net is acceptable. <br>


## Reference(s): <br>
- [DNS Lookup on ClawHub](https://clawhub.ai/CutTheMustard/lookup-dns) <br>
- [DNS Lookup service homepage](https://dns.agentutil.net) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include DNS records, reverse DNS names, RDAP/WHOIS fields, IP geolocation details, request IDs, and service metadata.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
