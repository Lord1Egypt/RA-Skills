## Description:

Query and manage INDY token staking positions on Indigo Protocol.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adacapo21](https://clawhub.ai/user/adacapo21)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to inspect INDY staking information, review staking positions, and prepare unsigned transactions to open, adjust, close, or distribute rewards for Indigo Protocol staking positions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security evidence marks the release suspicious because transaction instructions are inconsistent enough to require careful review before use with real funds.

Mitigation: Manually verify every generated transaction in a trusted wallet or transaction inspector before signing.

Risk: Staking actions can affect locked INDY, accrued ADA rewards, transaction fees, and governance voting power.

Mitigation: Confirm the caller address, staking UTxO transaction hash and output index, all outputs, fees, and INDY amounts in whole tokens and smallest units before signing.

Risk: Owner-address queries can expose wallet-linked staking information.

Mitigation: Avoid querying wallet-linked owner addresses without the address holder's consent.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/adacapo21/skills/indigo-staking)
- [Publisher Profile](https://clawhub.ai/user/adacapo21)
- [Staking MCP Tools Reference](references/mcp-tools.md)
- [Staking Concepts](references/concepts.md)

## Skill Output:

**Output Type(s):** [text, markdown, API Calls, Configuration instructions, guidance]

**Output Format:** [Markdown with MCP tool call examples and JSON transaction responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Write operations return unsigned Cardano transaction CBOR that must be reviewed, signed, and submitted outside the skill.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
