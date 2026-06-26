## Description: <br>
Complete GoDaddy API skill with shell scripts + MCP server for domains, DNS, certificates, shoppers, subscriptions, agreements, countries, and aftermarket listings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[solarx56](https://clawhub.ai/user/solarx56) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to manage GoDaddy account resources through shell scripts or an MCP server, including domains, DNS records, certificates, shoppers, subscriptions, agreements, countries, and aftermarket listings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The MCP server can let an agent make costly or destructive GoDaddy account changes without built-in approval checks. <br>
Mitigation: Use OTE/test credentials first and connect the MCP server only in environments with separate human approval or other controls for purchases, deletions, DNS replacement, certificate revocation, and cancellations. <br>
Risk: Production GoDaddy credentials can authorize domain, DNS, certificate, shopper, and subscription changes. <br>
Mitigation: Store credentials securely, avoid shell startup files for sensitive production secrets, and do not paste credential debug output into logs or chats. <br>
Risk: DNS replacement, domain cancellation, certificate revocation, and subscription cancellation can interrupt live services or be difficult to reverse. <br>
Mitigation: Back up current DNS records, validate payloads, test workflows in OTE when possible, and review the artifact safety checklist before high-impact operations. <br>


## Reference(s): <br>
- [GoDaddy API Documentation](https://developer.godaddy.com/doc) <br>
- [GoDaddy API Keys](https://developer.godaddy.com/keys) <br>
- [Authentication & Environment Setup](references/auth-and-env.md) <br>
- [GoDaddy API Endpoints Reference](references/endpoints.md) <br>
- [Request Body Schemas](references/request-bodies.md) <br>
- [Error Handling](references/error-handling.md) <br>
- [Safety Playbook](references/safety-playbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON payload examples, and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires bash, curl, jq, node, npm, and GoDaddy API credentials in GODADDY_API_BASE_URL, GODADDY_API_KEY, and GODADDY_API_SECRET.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
