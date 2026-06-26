## Description: <br>
iautopay helps agents and developers purchase and manage iAutoPay Fact API keys using USDC payments on Base Sepolia. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[newblock](https://clawhub.ai/user/newblock) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external agents use this skill to inspect iAutoPay pricing, create EIP-3009 payment signatures, buy API keys for 1, 7, or 30 days, and check account or key status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill documents broad payment actions, including stablecoin transfers and API-key purchases that require wallet signatures. <br>
Mitigation: Use a dedicated test wallet and verify every recipient, amount, token contract, chain, and signature expiry before signing. <br>
Risk: The security summary notes bearer API keys are sent to plain HTTP user-management URLs. <br>
Mitigation: Do not send real API keys to the documented HTTP user-management URLs unless the publisher provides a trusted secure transport. <br>
Risk: The security guidance flags the generic transfer endpoint as sensitive because it can move funds. <br>
Mitigation: Avoid the generic transfer endpoint unless the user explicitly intends to transfer funds and has confirmed all payment details. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/newblock/iautopay) <br>
- [newblock publisher profile](https://clawhub.ai/user/newblock) <br>
- [iAutoPay Fact API server information](https://apipaymcp.okart.fun/info) <br>
- [iAutoPay API key purchase endpoint](https://apipaymcp.okart.fun/v1/buy-apikey) <br>
- [iAutoPay user account endpoint](http://ipaynapi.gpuart.cn/user/me) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown with inline bash, JSON, Python, and TypeScript snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
0.1.1 (source: evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
