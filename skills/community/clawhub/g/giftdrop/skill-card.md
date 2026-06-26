## Description: <br>
Send, manage, and claim Solana crypto red packets via the GiftDrop API using wallet-authenticated requests and customizable gift parameters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tiancookie](https://clawhub.ai/user/tiancookie) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use GiftDrop to register wallet-authenticated API keys, create funded Solana gift drops, check their status, list owned drops, and claim available gifts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can lead agents to handle wallet keys and broadcast real Solana transfers. <br>
Mitigation: Use only a dedicated low-balance wallet, never a primary wallet or seed phrase, and require manual approval before any transaction is broadcast. <br>
Risk: Funds can be lost if the domain, host wallet, network, token mint, amount, fees, or service trustworthiness are wrong. <br>
Mitigation: Verify the GiftDrop domain, host wallet, network, token mint, amount, fees, and service trustworthiness before signing anything. <br>


## Reference(s): <br>
- [GiftDrop ClawHub Release](https://clawhub.ai/tiancookie/giftdrop) <br>
- [GiftDrop API Base URL](https://giftdrop.fun/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with curl commands, JSON request and response examples, and Python workflow code] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Solana wallet keypair and GiftDrop API key; operations may sign and broadcast real Solana transactions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
