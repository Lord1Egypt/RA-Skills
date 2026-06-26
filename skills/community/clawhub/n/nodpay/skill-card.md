## Description: <br>
Propose on-chain payments from a shared wallet. Use when user asks to send crypto, make a payment, or create a shared wallet. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xhyumiracle](https://clawhub.ai/user/xhyumiracle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use NodPay to set up a shared crypto wallet, generate an agent signing key, and propose on-chain payments that require human approval before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill participates in crypto payment proposal workflows and can prepare proposals with incorrect chain, recipient, amount, or nonce values. <br>
Mitigation: Require personal review of every approval link, chain, recipient, amount, and nonce before signing or approving a transaction. <br>
Risk: The agent signing key is stored locally in ~/.nodpay/.env and could authorize proposals if exposed. <br>
Mitigation: Protect ~/.nodpay/.env like a wallet credential, keep restrictive file permissions, and avoid sharing the key or wallet files. <br>
Risk: The workflow depends on the third-party nodpay npm package, nodpay.ai service, and public RPC endpoints. <br>
Mitigation: Verify the installed nodpay package and source before use, and confirm the official nodpay.ai domain when creating wallets or reviewing approvals. <br>


## Reference(s): <br>
- [NodPay homepage](https://nodpay.ai) <br>
- [NodPay CLI source](https://github.com/xhyumiracle/nodpay-cli) <br>
- [Safe multisig infrastructure](https://safe.global) <br>
- [ClawHub skill page](https://clawhub.ai/xhyumiracle/nodpay) <br>
- [Publisher profile](https://clawhub.ai/user/xhyumiracle) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, json] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces payment proposal guidance and CLI commands; the CLI may return JSON containing approval URLs, nonce data, transaction lists, and gas estimates.] <br>

## Skill Version(s): <br>
0.2.33 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
