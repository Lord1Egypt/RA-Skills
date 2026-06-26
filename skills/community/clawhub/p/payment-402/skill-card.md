## Description: <br>
Access protected APIs and digital resources via the x402 "Payment Required" protocol on Base L2 by automating cryptographic handshakes and USDC micro-payments for pay-per-resource agentic billing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paynodelabs](https://clawhub.ai/user/paynodelabs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to let an agent access x402-protected APIs and digital resources by checking wallet readiness, completing the payment challenge, and returning the protected response. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically spend funds from a local private-key wallet. <br>
Mitigation: Use a dedicated low-balance burner wallet, avoid primary wallet private keys, and require explicit approval or allowlisted budgets before paid requests. <br>
Risk: An agent could pay an unintended or untrusted merchant. <br>
Mitigation: Verify new merchants and confirm that the target URL, resource, and price match the user's objective before making a payment. <br>
Risk: Mainnet use can spend real funds during testing or troubleshooting. <br>
Mitigation: Test on sandbox or testnet endpoints first and move to mainnet only after the flow is verified. <br>


## Reference(s): <br>
- [Sandbox & Testing](references/TESTING.md) <br>
- [PayNode Documentation](https://github.com/PayNodeLabs/paynode-docs) <br>
- [PayNode Hub](https://github.com/PayNodeLabs/paynode-web) <br>
- [ClawHub skill page](https://clawhub.ai/paynodelabs/payment-402) <br>
- [Publisher profile](https://clawhub.ai/user/paynodelabs) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, API Calls, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Bun and CLIENT_PRIVATE_KEY; can initiate blockchain payments through a burner wallet.] <br>

## Skill Version(s): <br>
1.0.1 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
