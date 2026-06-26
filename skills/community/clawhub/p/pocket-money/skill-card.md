## Description: <br>
Give your AI agent crypto wallets on Base for purpose-specific wallet creation, funding requests, balance checks, and budget management using USDC. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[operator-auteng-ai](https://clawhub.ai/user/operator-auteng-ai) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to let an AI agent create and manage small, purpose-specific Base USDC wallets while keeping humans in the loop for funding and spend approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet files are real spending keys stored under .auteng/wallets/; exposed files or a compromised machine can lead to stolen funds. <br>
Mitigation: Protect .auteng/wallets/ like a password store, keep balances low, and fund only purpose-specific wallets. <br>
Risk: An agent with wallet access can propose actions that spend real USDC. <br>
Mitigation: Require explicit human approval for every spend and review or trust the npm package before funding wallets. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/operator-auteng-ai/pocket-money) <br>
- [Source repository](https://github.com/operator-auteng-ai/pocket-money) <br>
- [npm package](https://www.npmjs.com/package/@auteng/pocket-money) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration] <br>
**Output Format:** [Markdown with TypeScript and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide creation of local wallet files under .auteng/wallets/ and requests outbound HTTPS access to Base RPC for balance checks.] <br>

## Skill Version(s): <br>
2.0.0 (source: release evidence and VERSION.txt) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
