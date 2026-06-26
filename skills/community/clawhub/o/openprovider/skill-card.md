## Description: <br>
OpenProvider domain registrar and DNS management skill for domain registration, transfers, renewal, DNS zones and records, SSL certificate orders, nameserver groups, TLD information, WHOIS, customer handles, and reseller operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jpj069](https://clawhub.ai/user/jpj069) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage OpenProvider registrar workflows from an agent, including domain lifecycle actions, DNS record changes, SSL orders, nameserver groups, TLD pricing, and customer handles. It is most appropriate when the agent is expected to operate a real OpenProvider account and present account-impacting changes for human review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent through destructive or costly registrar actions, including domain deletion, transfer, renewal, DNS zone deletion, nameserver changes, and SSL order changes. <br>
Mitigation: Require explicit human confirmation that shows the exact domain, customer handle, DNS zone, nameserver group, certificate order, cost, and service-impact details before any write or delete action. <br>
Risk: The skill requires OpenProvider account credentials and bearer tokens, creating account-level exposure if credentials are over-scoped or mishandled. <br>
Mitigation: Use scoped credentials where possible, provide secrets only through approved secret storage or environment variables, and avoid exposing token values in agent output. <br>
Risk: Incorrect DNS record names can create unintended records such as duplicated apex or subdomain names. <br>
Mitigation: Normalize DNS record names to OpenProvider zone-relative form before writes and read back the zone after changes to verify the final fully qualified record name. <br>
Risk: Nameserver and SSL workflows may need extra review where support is unclear or not fully implemented. <br>
Mitigation: Treat nameserver and SSL changes as high-impact actions and require additional human review before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jpj069/openprovider) <br>
- [OpenProvider authentication and error handling](references/auth.md) <br>
- [OpenProvider domain operations](references/domains.md) <br>
- [OpenProvider DNS zone and record operations](references/dns.md) <br>
- [OpenProvider SSL certificate operations](references/ssl.md) <br>
- [OpenProvider nameserver group operations](references/nameservers.md) <br>
- [OpenProvider TLD information and pricing](references/tlds.md) <br>
- [OpenProvider customer and reseller management](references/customers-resellers.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code, text] <br>
**Output Format:** [Markdown guidance with JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include OpenProvider REST API endpoints, request payloads, environment variable names, and verification steps.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
