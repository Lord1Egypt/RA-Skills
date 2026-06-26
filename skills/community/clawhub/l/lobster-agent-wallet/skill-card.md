## Description: <br>
Manage a USDC wallet for AI agents on Base, supporting balance checks and x402 payments with configurable network and key settings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chengtang05-hash](https://clawhub.ai/user/chengtang05-hash) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to configure a Base or Base Sepolia USDC wallet, check ETH and USDC balances, and make x402 payments from agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can authorize real USDC payments from server-provided terms without enough user-visible limits or checks. <br>
Mitigation: Install only with a dedicated low-balance or testnet wallet, avoid untrusted payment URLs, and require explicit review of payment details before signing. <br>
Risk: Payment terms may lack enforced checks for recipient, token contract, network, amount, expiry, domain allowlists, or spend limits. <br>
Mitigation: Prefer a version that previews and enforces those constraints before any signature is created. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chengtang05-hash/lobster-agent-wallet) <br>
- [Skill usage documentation](artifact/SKILL.md) <br>
- [Package metadata](artifact/package.json) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Configuration, Guidance] <br>
**Output Format:** [Console text, Markdown usage guidance, and JavaScript CLI/module patterns] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses environment-based wallet configuration; signed x402 payments require a private key and explicit confirmation.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
