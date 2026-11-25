## Description:

Provides AI agents with bounded PocketSlip funds on Base through a Slip URL, with spend controls and payment tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[naraprotocol](https://clawhub.ai/user/naraprotocol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to provision bounded funds for Base payments, human and batch payouts, payment verification, refunds of unclaimed funds, and referral withdrawals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan flagged an unpinned MCP command and had partial coverage because some references could not be resolved.

Mitigation: Review the install command and confirm it is pinned to the intended package version; assess the unresolved references before installation.

## Reference(s):

- [CryptoSLIP PocketSlip setup](https://slip.naraprotocol.io)
- [CryptoSLIP alternative access](https://cryptoslip.eth.limo)
- [ClawHub release page](https://clawhub.ai/naraprotocol/skills/mcp)

## Skill Output:

**Output Type(s):** [Text, JSON, CSV, HTML, Payment links, Guidance]

**Output Format:** [Structured payment status and receipts in JSON, CSV, or printable HTML, plus payment links and text guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tool calls can initiate Base Mainnet payments; the skill describes configurable spend limits, rate limits, and destination controls.]

## Skill Version(s):

0.1.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
