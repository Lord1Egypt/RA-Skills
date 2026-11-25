## Description:

Detect and protect against MEV attacks on Base L2 including sandwich attacks, frontrunning, and backrunning. Analyzes confirmed transactions from recent blocks for sandwich patterns, simulates attack profitability, and suggests protection strategies. Use when an agent needs to assess MEV risk on a Base L2 transaction or understand MEV risks on Base L2.

This skill is ready for commercial/non-commercial use.

## Publisher:

[manteclaw](https://clawhub.ai/user/manteclaw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use the skill to review confirmed Base transactions for possible MEV patterns and to explore basic sandwich-risk estimates. Its findings can inform protection choices before a separate transaction workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment is benign with medium confidence, but coverage is partial and does not guarantee zero risk.

Mitigation: Review the skill before installation and treat the scan verdict as limited evidence rather than a guarantee.

Risk: The skill sends transaction hashes or block numbers to its configured Base RPC endpoint, so endpoint trust and network use matter.

Mitigation: Use a trusted HTTPS RPC endpoint and consider whether sending those query values to it fits your needs.

## Reference(s):

- [MEV Patterns on Base L2](references/mev-patterns.md)
- [Flashbots Protect RPC](https://rpc.flashbots.net)
- [MEV Blocker RPC](https://rpc.mevblocker.io)
- [Merkle RPC](https://rpc.merkle.io)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Guidance]

**Output Format:** [Human-readable transaction analysis by default, or JSON when requested; simulation results are summarized as text or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Heuristic, read-only analysis of confirmed transactions; the sandwich simulation is a simple arithmetic estimate. Scores are guidance, not a guarantee.]

## Skill Version(s):

1.0.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
