## Description: <br>
Predict pump.fun token graduations (YES/NO) on Solana mainnet via PumpMarket parimutuel betting markets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[notKing0](https://clawhub.ai/user/notKing0) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to inspect PumpMarket markets, construct Solana mainnet transactions, and place or claim YES/NO bets on pump.fun token graduation outcomes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to sign Solana mainnet transactions that spend real SOL. <br>
Mitigation: Use a dedicated low-balance wallet, require explicit approval before signing, and enforce a strict SOL cap for each transaction. <br>
Risk: Wallet private keys may be exposed if loaded carelessly for automated signing. <br>
Mitigation: Never hardcode private keys; use environment variables, encrypted keyfiles, or a secrets manager with restricted access. <br>
Risk: Transactions may execute against live PumpMarket markets before the operator understands the outcome and fee mechanics. <br>
Mitigation: Run the documented dry-run simulation first, verify market data immediately before signing, and start with the minimum practical balance. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/notKing0/pmt-skill) <br>
- [PumpMarket Homepage](https://pumpmarket.fun) <br>
- [PumpMarket Program IDL](https://pumpmarket.fun/skill.json) <br>
- [PumpMarket API](https://pumpbet-mainnet.up.railway.app) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with TypeScript, JSON, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes mainnet API, WebSocket, wallet, transaction-construction, simulation, and claim workflow guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
