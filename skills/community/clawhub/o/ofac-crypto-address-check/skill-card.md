## Description:

Screens unfamiliar crypto wallet addresses against public US Treasury OFAC SDN data with a free, no-auth exact-match check, including when a user asks whether an address is sanctioned, blacklisted, or OFAC-listed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[a0971025732-netizen](https://clawhub.ai/user/a0971025732-netizen)

### License/Terms of Use:

MIT-0

## Use Case:

Crypto users and agents can screen an unfamiliar counterparty's wallet address before sending, receiving, or swapping, or when asked whether an address is OFAC-listed. Treat the result as an exact-match lookup against the published list, not as a determination that an address is safe.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Finch receives queried wallet addresses, and their association with the user may be sensitive.

Mitigation: Consider that sensitivity before screening and explain that the address is sent to Finch when relevant.

Risk: An exact-match non-match does not prove that an address is safe.

Mitigation: State the list publish date and the limits of the lookup; do not present a non-match as transaction approval.

Risk: Optional MistTrack tracing may require payment.

Mitigation: Offer tracing as an option and obtain the user's approval before running any paid trace.

## Reference(s):

- [OFAC Crypto Address Check on ClawHub](https://clawhub.ai/a0971025732-netizen/skills/ofac-crypto-address-check)
- [Finch sanctions check service](https://finch-agent-catalog.finch-catalog-mcp.workers.dev/mcp)

## Skill Output:

**Output Type(s):** [Guidance, Text]

**Output Format:** [Concise user-facing text with match status, relevant sanctioned-party and program details, and the list publish date when available.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Exact-match screening against public SDN digital-currency address data; a non-match does not establish safety.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
