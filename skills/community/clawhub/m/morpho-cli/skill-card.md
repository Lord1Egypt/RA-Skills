## Description:

Interact with the Morpho lending protocol via CLI to query vaults, markets, positions, balances, and health, and to prepare or simulate unsigned transactions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jinmel](https://clawhub.ai/user/jinmel)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to inspect Morpho protocol state on Base and Ethereum and prepare unsigned DeFi transaction payloads with simulation results for user review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs an unpinned npm CLI while preparing DeFi transaction payloads.

Mitigation: Use only a pinned, reviewed version of the Morpho CLI or a locked local install, and run it with minimal filesystem and environment access.

Risk: Prepared transactions may contain incorrect chain IDs, contract addresses, approval spenders, amounts, warnings, or simulation results.

Mitigation: Independently verify chain IDs, contract addresses, approval spenders, amounts, warnings, and simulation results before signing anything in a wallet.

Risk: Sensitive wallet material or unrelated credentials could be exposed to the agent environment.

Mitigation: Do not expose private keys or unnecessary credentials to the agent environment.

## Reference(s):

- [Read Command Response Schemas](artifact/references/read.md)
- [Write Command Response Schemas](artifact/references/write.md)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Markdown with inline bash commands and JSON summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands output JSON to stdout; transaction payloads are unsigned and should be independently verified before signing.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
