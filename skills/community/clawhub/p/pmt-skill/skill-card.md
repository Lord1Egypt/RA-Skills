## Description:

Predict pump.fun token graduations (YES/NO) on Solana mainnet via PumpMarket parimutuel betting markets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[notking0](https://clawhub.ai/user/notking0)

### License/Terms of Use:


## Use Case:

External developers and agents use this skill to inspect PumpMarket markets, construct Solana mainnet transactions, and place or manage YES/NO bets on pump.fun token graduation outcomes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can help an agent spend real SOL on Solana mainnet betting markets.

Mitigation: Use a dedicated wallet with limited funds and require explicit approval before every createMarket or placeBet transaction.

Risk: The security evidence flags a privileged emergency withdrawal path that users should review before depositing meaningful funds.

Mitigation: Review the program's emergency withdrawal behavior and keep funds limited until the risk is acceptable.

Risk: Dependency or transaction behavior may differ from expectations during live mainnet use.

Mitigation: Pin dependencies and simulate transactions before submitting them on mainnet.

## Reference(s):

- [PumpMarket homepage](https://pumpmarket.fun)
- [PumpMarket IDL](https://pumpmarket.fun/skill.json)
- [PumpMarket mainnet API](https://pumpbet-mainnet.up.railway.app)
- [ClawHub skill page](https://clawhub.ai/notking0/skills/pmt-skill)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration]

**Output Format:** [Markdown with inline TypeScript and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides API, WebSocket, Solana transaction, wallet setup, and dry-run simulation guidance for PumpMarket.]

## Skill Version(s):

1.0.0 (source: frontmatter and server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
