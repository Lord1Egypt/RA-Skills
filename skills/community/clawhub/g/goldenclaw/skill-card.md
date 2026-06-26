## Description: <br>
Golden Claw helps OpenClaw agents manage GoldenClaw (GCLAW) on Solana, including wallet creation, faucet claims, balance checks, token transfers, and transaction history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[GoldenClawOrg](https://clawhub.ai/user/GoldenClawOrg) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External OpenClaw users and developers use this skill to operate a GCLAW wallet, claim tokens from the GoldenClaw faucet, inspect balances and history, and send GCLAW or SOL through Solana transactions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can move real Solana assets and was flagged by ClawHub security as requiring review. <br>
Mitigation: Install only if the GoldenClawOrg publisher is trusted, use a low-value dedicated wallet, and review transaction details before sending GCLAW or SOL. <br>
Risk: The skill auto-runs npm install at startup when dependencies are missing. <br>
Mitigation: Install dependencies in a controlled environment before use instead of relying on runtime installation. <br>
Risk: Wallet recovery and setup involve a BIP39 seed phrase. <br>
Mitigation: Avoid pasting valuable seed phrases into agent or shell contexts; prefer a dedicated wallet and keep backups outside the agent session. <br>
Risk: The donation command sends SOL to a configured project treasury address. <br>
Mitigation: Verify the donation address and amount before confirming any SOL transfer. <br>


## Reference(s): <br>
- [GoldenClaw Skill Page](https://clawhub.ai/GoldenClawOrg/goldenclaw) <br>
- [GoldenClaw Website and Faucet](https://goldenclaw.org) <br>
- [GCLAW Token on Solscan](https://solscan.io/token/8fUqKCgQ2PHcYRnce9EPCeMKSaxd14t7323qbXnSJr4z) <br>
- [GoldenClaw X Profile](https://x.com/GClaw68175) <br>
- [GoldenClaw Community](https://moltbook.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown-style command responses and status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Solana addresses, balances, transaction signatures, faucet status, wallet recovery guidance, and spending-limit messages.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact metadata reports 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
