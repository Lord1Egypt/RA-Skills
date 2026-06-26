## Description: <br>
Manage domains and DNS via the Porkbun API v3, including domain listing, availability checks, DNS records, nameservers, URL forwarding, SSL retrieval, pricing, and auto-renew settings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[danielgrobelny](https://clawhub.ai/user/danielgrobelny) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and domain administrators use this skill to manage Porkbun-hosted domains and DNS records from an agent session with explicit API credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make high-impact DNS and domain changes, including deleting DNS records, changing nameservers, forwarding domains, and toggling auto-renew. <br>
Mitigation: Require explicit user confirmation before delete, nameserver, forwarding, or auto-renew operations, and restrict credentials to Porkbun accounts where this level of authority is acceptable. <br>
Risk: The credential loader reads a workspace .env file in an unsafe way. <br>
Mitigation: Avoid shared or untrusted workspace .env files until the loader parses keys without eval; prefer trusted environment variables for credentials. <br>


## Reference(s): <br>
- [Porkbun API key management](https://porkbun.com/account/api) <br>
- [Porkbun API v3 base endpoint](https://api.porkbun.com/api/json/v3) <br>
- [ClawHub skill page](https://clawhub.ai/danielgrobelny/porkbun-domains) <br>
- [Publisher profile](https://clawhub.ai/user/danielgrobelny) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PORKBUN_API_KEY and PORKBUN_SECRET_KEY for authenticated operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
