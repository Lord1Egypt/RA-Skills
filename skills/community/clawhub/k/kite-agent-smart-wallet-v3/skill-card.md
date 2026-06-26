## Description: <br>
Kite Agent Smart Wallet V3 lets an agent control a Kite AI testnet wallet through Telegram/OpenClaw commands for wallet creation, balance checks, transfers, session keys, and spending limits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nihaovand](https://clawhub.ai/user/nihaovand) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users operate a Kite AI testnet wallet through Telegram/OpenClaw. They use the skill to create wallets, check balances, send KITE, manage session keys, and set spending limits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Chat commands can exercise powerful wallet authority with weak scoping and disclosure. <br>
Mitigation: Review before installing, restrict who can issue /kite commands, and use only a testnet or low-value wallet key. <br>
Risk: Session keys may grant broad wallet control when added without narrow function permissions. <br>
Mitigation: Avoid adding session keys unless their authority and spending limits are understood and acceptable. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/nihaovand/kite-agent-smart-wallet-v3) <br>
- [Kite testnet RPC endpoint](https://rpc-testnet.gokite.ai) <br>
- [Kite testnet faucet](https://faucet.gokite.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, api calls, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown-formatted command responses and Node.js module exports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Telegram command text, a configured private key, Kite testnet RPC access, and an ethers.js dependency.] <br>

## Skill Version(s): <br>
3.0.2 (source: server release metadata; artifact skill.json and documentation report 3.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
