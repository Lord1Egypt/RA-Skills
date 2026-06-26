## Description: <br>
Inscribe content on Bitcoin via the Ordiscan API and pay per request with USDC on Base using the x402 protocol. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[t4t5](https://clawhub.ai/user/t4t5) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to query Ordinals data or prepare paid Ordiscan API requests that inscribe text, files, or other content on Bitcoin. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The default signing script can sign real USDC payments from an Ethereum private key without a built-in spending cap or confirmation step. <br>
Mitigation: Use a dedicated, low-balance wallet, review the 402 price, recipient, and destination before signing, and prefer flows with explicit maximum amounts. <br>
Risk: Inscription content is sent to Ordiscan and can become permanently public on Bitcoin. <br>
Mitigation: Avoid inscribing private, sensitive, copyrighted, or regulated content and confirm the intended recipient Bitcoin address before submitting. <br>


## Reference(s): <br>
- [Ordiscan API Documentation](https://ordiscan.com/docs/api) <br>
- [Ordiscan API Markdown Documentation](https://ordiscan.com/docs/api.md) <br>
- [ClawHub Ordiscan Release](https://clawhub.ai/t4t5/ordiscan) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown with inline bash commands and JSON request or response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node or awal, X402_PRIVATE_KEY, and optionally ~/.evm-wallet.json.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
