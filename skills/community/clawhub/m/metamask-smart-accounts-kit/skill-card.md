## Description: <br>
Provides Web3 development guidance for MetaMask Smart Accounts Kit, including ERC-4337 smart accounts, user operations, signers, paymasters, delegations, advanced permissions, and Viem integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AyushBherwani1998](https://clawhub.ai/user/AyushBherwani1998) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to build dApps with MetaMask smart accounts, gas abstraction, delegation flows, and ERC-7715 advanced permissions. It helps agents answer implementation questions and draft code, configuration, and command examples for smart-account workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated wallet or smart-account code can move assets or authorize future transactions if chain IDs, recipients, token amounts, expiry times, caveats, or delegation scopes are wrong. <br>
Mitigation: Use testnets first and verify all transaction, permission, and delegation parameters before running code with real accounts or funds. <br>
Risk: Private keys, signer credentials, or wallet secrets may be exposed if inserted into source code, prompts, logs, or client-side applications. <br>
Mitigation: Keep private keys and credentials out of prompts, logs, repositories, and browser code; use secure key management and environment-specific secret handling. <br>


## Reference(s): <br>
- [MetaMask Smart Accounts Kit Documentation](https://docs.metamask.io/smart-accounts-kit) <br>
- [MetaMask Flask](https://metamask.io/flask) <br>
- [Smart Accounts Reference](references/smart-accounts.md) <br>
- [Delegations Reference](references/delegations.md) <br>
- [Advanced Permissions Reference](references/advanced-permissions.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with TypeScript and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include wallet, chain, contract, permission, delegation, bundler, and paymaster values that must be verified before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
