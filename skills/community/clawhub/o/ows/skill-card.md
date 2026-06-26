## Description: <br>
Enables agents to use a pre-installed OWS CLI for local multi-chain wallet management, balance checks, transaction signing, x402 payments, funding, and policy-aware wallet operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rhlsthrm](https://clawhub.ai/user/rhlsthrm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to operate a local OWS wallet for balance checks, signing, x402 API payments, and wallet policy control. It is intended for environments where the user has already installed and independently verified the OWS CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables spend-capable signing and payment commands without explicit per-transaction confirmation safeguards. <br>
Mitigation: Require manual review of wallet, chain, destination, amount, URL, and decoded transaction or message details before any signing or payment command. <br>
Risk: Using the skill with a production or high-balance wallet can expose funds to mistaken or unauthorized actions. <br>
Mitigation: Use a dedicated low-balance wallet, configure spending limits and chain allowlists, and keep high-value wallets outside agent workflows. <br>
Risk: The skill depends on a local OWS CLI that the skill does not install or verify. <br>
Mitigation: Install and verify the OWS CLI separately, and do not allow the agent to install or update OWS packages. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rhlsthrm/ows) <br>
- [Open Wallet Standard documentation](https://openwallet.sh) <br>
- [Open Wallet Standard core repository](https://github.com/open-wallet-standard/core) <br>
- [OWS npm package](https://www.npmjs.com/package/@open-wallet-standard/core) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash and TypeScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-preinstalled OWS CLI; signing and payment commands should be manually reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.3 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
