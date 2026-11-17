## Description:

OpenProvider domain registrar and DNS management guidance for registering, renewing, transferring, deleting, and restoring domains; managing DNS records, SSL orders, nameservers, TLD data, customers, resellers, WHOIS, EPP codes, and pricing through the OpenProvider REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jpj069](https://clawhub.ai/user/jpj069)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to draft OpenProvider API calls and operational steps for domain lifecycle, DNS, SSL, nameserver, TLD, customer, and reseller management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OpenProvider credentials, bearer tokens, EPP codes, customer data, and other sensitive values can be exposed in shell history, CI logs, or chat transcripts.

Mitigation: Use a narrowly scoped OpenProvider identity, avoid running authentication curl examples in logged shells or CI, and redact passwords, tokens, EPP codes, and PII before sharing output.

Risk: Registrar, DNS, SSL, and customer operations can change availability, ownership, billing, or live traffic for real domains.

Mitigation: Require fresh explicit confirmation that names the exact domain, DNS zone, customer handle, SSL order, action, and cost before delete, transfer, purchase, renewal, restore, or DNS-changing operations.

Risk: Incorrect DNS record naming can create unintended records such as duplicated zone suffixes.

Mitigation: Normalize DNS record names to OpenProvider zone-relative form, use an empty string for apex writes, and read back zone records to verify the final FQDN.

## Reference(s):

- [OpenProvider Skill Page](https://clawhub.ai/jpj069/skills/openprovider)
- [Authentication and Error Handling](references/auth.md)
- [Domain Operations](references/domains.md)
- [DNS Zone and Record Management](references/dns.md)
- [SSL Certificate Operations](references/ssl.md)
- [Nameserver Management](references/nameservers.md)
- [TLD Information and Pricing](references/tlds.md)
- [Customer and Reseller Management](references/customers-resellers.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration guidance, API calls]

**Output Format:** [Markdown with inline JSON and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include OpenProvider endpoint paths, request payloads, DNS record values, customer handles, domain names, and operational checklists.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
