## Description: <br>
Complete authentication guide for Orderly Network - EIP-712 wallet signatures for EVM accounts, Ed25519 message signing for Solana accounts, and Ed25519 signatures for API requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Tarnadas](https://clawhub.ai/user/Tarnadas) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill as an Orderly Network authentication reference for setting up accounts, API keys, trading bot requests, WebSocket authentication, and key management across EVM and Solana wallets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Example code logs generated private keys and could expose credentials if copied into real applications. <br>
Mitigation: Remove private-key logging, store keys in a secret manager or protected environment, and keep generated credentials out of application logs. <br>
Risk: Trading, withdrawal, transfer, and key-management examples can affect live accounts if used without review. <br>
Mitigation: Test on testnet first, use least-privilege key scopes, and require explicit user confirmation before withdrawals, transfers, or live trading. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Tarnadas/orderly-api-authentication) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, configuration] <br>
**Output Format:** [Markdown with TypeScript examples, endpoint references, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance for authentication flows; examples require review and adaptation before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
