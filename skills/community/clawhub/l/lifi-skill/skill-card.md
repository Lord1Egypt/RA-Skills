## Description:

LI.FI Skill helps agents use the LI.FI API to quote and execute same-chain and cross-chain swaps, bridges, contract calls, and transfer status checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fabriziogianni7](https://clawhub.ai/user/fabriziogianni7)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to guide wallet-connected agents through LI.FI route discovery, quote presentation, approval handling, transaction submission, and post-transaction status tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide real wallet transactions, and the release security summary flags weak required safeguards.

Mitigation: Review before installing for real-wallet use, require explicit confirmation before signing or broadcasting, and verify spender, transaction details, and route terms.

Risk: High slippage or broad ERC-20 approvals can create avoidable financial exposure.

Mitigation: Use conservative slippage, avoid unlimited approvals when possible, and confirm approval amounts and spender addresses before execution.

## Reference(s):

- [LI.FI Documentation](https://docs.li.fi/)
- [LI.FI LLM Documentation](https://docs.li.fi/llms.txt)
- [LI.FI OpenAPI Schema](https://gist.githubusercontent.com/kenny-io/7fede47200a757195000bfbe14c5baee/raw/725cf9d4a6920d5b930925b0412d766aa53c701c/lifi-openapi.yaml)
- [ClawHub LI.FI Skill](https://clawhub.ai/fabriziogianni7/skills/lifi-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands, API parameters, transaction details, and block explorer links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires LIFI_API_KEY; quote responses may include transaction request fields for wallet submission.]

## Skill Version(s):

2.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
