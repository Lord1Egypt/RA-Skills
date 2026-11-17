## Description:

Guides agents through paid NetIntel lookups for domain and email checks, web research, content extraction, and other external data using x402 payments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kjgueye](https://clawhub.ai/user/kjgueye)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to check sales leads, investigate domains and IPs, retrieve web content, and find suitable paid lookup endpoints with a wallet-funded budget.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic pay-per-call lookups can spend wallet funds without a separate prompt for each request.

Mitigation: Get explicit approval before paid calls, check the quoted price, and set per-call and session spending limits with a low-balance wallet.

Risk: Unpinned package setup commands may run code with access to a wallet key or funds.

Mitigation: Review and pin package versions before running setup commands, and keep private keys out of conversations and logs.

## Reference(s):

- [NetIntel homepage](https://netintel.dev)
- [NetIntel API reference](https://netintel.dev/openapi.json)
- [ClawHub skill release](https://clawhub.ai/kjgueye/skills/netintel)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration instructions]

**Output Format:** [Markdown with example requests and responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [External lookups may require a paid x402 transaction; responses vary by endpoint.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
