## Description: <br>
Helps the agent use the one-wallet CLI to manage Ethereum/EVM wallets, send transactions, call contracts, and sign data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Viyozc](https://clawhub.ai/user/Viyozc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to guide terminal workflows for Ethereum/EVM wallet management, balance checks, contract calls, transaction submission, and message or typed-data signing with one-wallet. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide high-impact wallet, signing, token approval, contract write, and transaction workflows. <br>
Mitigation: Require explicit human confirmation before any send, token approval, contract write, or signature. <br>
Risk: Using unverified one-wallet packages or repositories could expose wallet funds or signing authority. <br>
Mitigation: Verify the one-wallet package and repository before installation, and start with testnet or low-value wallets. <br>
Risk: Private keys or wallet passwords could be exposed through chat, shell history, logs, or source-controlled files. <br>
Mitigation: Do not paste real private keys into chat or commands; use a dedicated secret manager or controlled environment variables. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Viyozc/one-wallet) <br>
- [one-wallet repository referenced by the skill artifact](https://github.com/viyozc/one-wallet.git) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON-output conventions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include commands that produce machine-readable JSON when the one-wallet CLI supports --json.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
