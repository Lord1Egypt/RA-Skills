## Description: <br>
Helps agents and users manage a Kite AI testnet smart wallet through Telegram commands for wallet creation, balance checks, session keys, spending limits, and transfers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nihaovand](https://clawhub.ai/user/nihaovand) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and wallet operators use this skill to run a local Telegram bot that controls a Kite AI testnet wallet. It is suited for testnet wallet operations, smart wallet setup, session key management, spending-limit updates, and transaction commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs a local Telegram bot with a private key that can sign wallet operations. <br>
Mitigation: Use a fresh low-value testnet-only key, keep the bot private or restrict allowed users, and never commit .env files or private keys. <br>
Risk: Chat commands can trigger sends, permission changes, and spending-limit updates with limited access control or confirmation. <br>
Mitigation: Add explicit confirmations and an allowlist before using the bot, and review every command path before connecting funded wallets. <br>
Risk: Repository publishing instructions may encourage pushing local skill files. <br>
Mitigation: Review or remove publishing instructions and confirm secrets are excluded before any repository push. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nihaovand/kite-agent-smart-wallet-permissionless-protocol-v2) <br>
- [Publisher profile](https://clawhub.ai/user/nihaovand) <br>
- [Kite AI website](https://gokite.ai) <br>
- [Kite AI documentation](https://docs.gokite.ai) <br>
- [Kite testnet explorer](https://testnet.kitescan.ai) <br>
- [Kite testnet faucet](https://faucet.gokite.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JavaScript code, shell commands, and environment configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces guidance and runnable local bot code that can sign Kite testnet wallet operations when configured with a private key.] <br>

## Skill Version(s): <br>
2.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
