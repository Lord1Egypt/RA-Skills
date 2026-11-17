## Description:

Purchase API keys from the iAutoPay Fact API using USDC on Base Sepolia, then check account, usage, pricing, and API key information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[newblock](https://clawhub.ai/user/newblock)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to buy time-limited API keys with Base Sepolia USDC payments and inspect related user account, API key, pricing, and usage data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet payments and API keys are handled by the workflow, and the security verdict flags the release as suspicious.

Mitigation: Review carefully before installation and use only a dedicated low-balance testnet wallet.

Risk: Authenticated user-management examples send bearer API keys to an HTTP endpoint.

Mitigation: Do not send bearer API keys over HTTP; verify HTTPS support before using authenticated endpoints.

Risk: Payment signing can transfer funds to the wrong recipient, token contract, chain, amount, or expiry if values are not checked.

Mitigation: Confirm the exact chain, token contract, recipient, amount, and signature expiry before signing.

Risk: The documented transfer endpoint can send stablecoin to arbitrary addresses.

Mitigation: Avoid the arbitrary transfer endpoint unless it is intentionally required and all transfer details have been independently confirmed.

Risk: Wallet-signing examples install runtime dependencies before execution.

Mitigation: Pin dependencies before running the Python or TypeScript wallet-signing examples.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/newblock/skills/iautopay)
- [iAutoPay Fact API](https://apipaymcp.okart.fun)
- [iAutoPay Fact API Info Endpoint](https://apipaymcp.okart.fun/info)
- [iAutoPay User Management API](http://ipaynapi.gpuart.cn)
- [Base Sepolia RPC](https://sepolia.base.org)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration]

**Output Format:** [Markdown with bash, Python, TypeScript, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include wallet-signing steps, API request examples, endpoint responses, and environment-variable guidance.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
