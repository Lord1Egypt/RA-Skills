## Description: <br>
x402 payment protocol for AI agents. Enables autonomous micropayments using HTTP 402 status codes and stablecoins. Use when you need to pay for API access, accept payments for your services, or interact with x402-enabled endpoints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Neckr0ik](https://clawhub.ai/user/Neckr0ik) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent builders use this skill to inspect x402-enabled endpoints, draft payment or payment-acceptance workflows, and configure agent-facing payment commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill presents as a real autonomous payment tool while the security review says the implementation mostly simulates payments. <br>
Mitigation: Use it only for testing or code review; do not rely on it for real settlement, account balances, payment enforcement, or production API access until verified payment behavior is clearly implemented or labeled. <br>
Risk: Wallet secrets and local payment records may be handled with weak guidance. <br>
Mitigation: Do not enter a funded wallet private key; use isolated test wallets and review local configuration and history files before any use. <br>
Risk: Autonomous payment workflows can create unintended spending exposure. <br>
Mitigation: Require human approval, dry runs, low spending limits, and endpoint verification before any live payment workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Neckr0ik/neckr0ik-x402-payments) <br>
- [Publisher profile](https://clawhub.ai/user/Neckr0ik) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, Python examples, and configuration instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose command-line payment, server, balance, history, and wallet-configuration workflows for review before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
