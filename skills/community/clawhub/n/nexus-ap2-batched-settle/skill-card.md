## Description:

Atomically settle up to 20 AI agent payments in a single XRPL Batch transaction using AP2 mandates and XLS-56 Batch on XRP Ledger.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cyberforexblockchain](https://clawhub.ai/user/cyberforexblockchain)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent builders use this skill to create AP2 payment mandates, build unsigned XRPL payment or batch transactions, and verify broadcast settlement proofs while keeping wallet signing outside the service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The remote service constructs unsigned wallet transactions for payments, including batched payments.

Mitigation: Manually inspect decoded transaction fields before signing, including destination, amount, currency, issuer, fee, network, memo, and every inner payment in a batch.

Risk: Sandbox signatures and unclear sandbox/mainnet separation can create production-funds exposure if reused without controls.

Mitigation: Use production funds only with real signatures, a clearly isolated sandbox/mainnet boundary, and wallet-side spending or network limits.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cyberforexblockchain/skills/nexus-ap2-batched-settle)
- [AP2 Specification](https://ap2-protocol.org/)
- [XRPL Batch Transactions](https://xrpl.org/docs/concepts/transactions/batch-transactions)
- [AP2 Config Endpoint](https://ai-service-hub-15.emergent.host/api/ap2/config)
- [XRPL Config Endpoint](https://ai-service-hub-15.emergent.host/api/xrpl/config)
- [A2A Agent Card](https://ai-service-hub-15.emergent.host/.well-known/agent.json)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON request and response examples plus shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces mandate identifiers, unsigned XRPL transaction JSON, and settlement or verification instructions for local wallet signing and broadcast.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
