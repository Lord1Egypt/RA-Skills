## Description: <br>
Pay HTTP 402 payment challenges using tokens via the Tempo CLI and Uniswap Trading API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samledger67-dotcom](https://clawhub.ai/user/samledger67-dotcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to complete paid API calls after an HTTP 402, MPP, or x402 challenge. It guides setup, wallet funding, token swaps, bridging, credential construction, and retrying the paid request after explicit user confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide high-impact crypto payments, approvals, swaps, bridges, signatures, and session actions. <br>
Mitigation: Require a fresh visible user confirmation for each action, including human-readable amount, token, recipient, destination chain, estimated gas, and resource URL before submitting or signing. <br>
Risk: The skill asks agents to work with raw wallet private keys. <br>
Mitigation: Use a dedicated low-balance wallet, avoid main-wallet private keys, keep secrets out of files and logs, and rotate keys if exposure is suspected. <br>
Risk: Installer scripts and npm packages are part of the payment flow. <br>
Mitigation: Verify the Tempo installer and npm package sources before use, and install only in an environment where crypto-payment automation is acceptable. <br>
Risk: Untrusted 402 challenge data or user input could lead to incorrect payment parameters. <br>
Mitigation: Validate addresses, chain IDs, token amounts, and HTTPS URLs before using them, and reject shell metacharacters or malformed challenge bodies. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/samledger67-dotcom/pay-with-any-token) <br>
- [Publisher profile](https://clawhub.ai/user/samledger67-dotcom) <br>
- [Credential Construction](references/credential-construction.md) <br>
- [Trading API Flows](references/trading-api-flows.md) <br>
- [Tempo CLI](https://tempo.xyz) <br>
- [Tempo documentation](https://mainnet.docs.tempo.xyz) <br>
- [MPP documentation](https://mpp.dev) <br>
- [MPP services catalog](https://mpp.dev/api/services) <br>
- [Uniswap developer portal](https://developers.uniswap.org/) <br>
- [Uniswap Trading API](https://trade-api.gateway.uniswap.org/v1) <br>
- [x402 specification](https://github.com/coinbase/x402) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline bash and TypeScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include API request bodies, transaction summaries, and confirmation prompts for payment, signing, approval, swap, and bridge actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter lists 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
