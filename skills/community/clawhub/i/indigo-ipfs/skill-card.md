## Description:

Store and retrieve data on IPFS and query collector UTXOs for the Indigo Protocol.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adacapo21](https://clawhub.ai/user/adacapo21)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Indigo Protocol users use this skill to store or retrieve text content on IPFS and inspect collector UTXOs that hold accumulated protocol fees on Cardano.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Plaintext content stored on IPFS can be durable and potentially public, including wallet-linked financial snapshots.

Mitigation: Use the skill only for content intended for durable storage; redact or encrypt seed phrases, private keys, API keys, personal data, confidential proposals, and wallet-linked financial snapshots before storage.

Risk: Collector UTXO summaries can expose wallet-linked protocol fee information if copied into public records.

Mitigation: Review generated summaries before sharing and remove sensitive addresses, transaction details, or financial context that should not be public.

## Reference(s):

- [MCP Tools Reference](artifact/references/mcp-tools.md)
- [Concepts - IPFS & Collector](artifact/references/concepts.md)
- [ClawHub skill page](https://clawhub.ai/adacapo21/skills/indigo-ipfs)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown with tool-call guidance and plain-text returned content, CIDs, and UTXO summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return durable IPFS content identifiers and wallet-linked collector UTXO data.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
