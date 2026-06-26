## Description: <br>
LobPay helps agents retrieve checkout details, execute X402-based purchases on Base, view purchase history, and submit merchant feedback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[web3senior](https://clawhub.ai/user/web3senior) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent operators use LobPay to configure a wallet-backed commerce agent that can inspect products, make purchases through LobPay API endpoints, record transaction history, and submit merchant ratings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet private keys and API keys are stored locally in ~/.lobpay/config.json and can be supplied on the command line during registration. <br>
Mitigation: Use a dedicated low-balance or testnet wallet, avoid passing long-lived private keys on the command line, and protect or delete ~/.lobpay/config.json after use. <br>
Risk: buy.js and purchase.js can execute blockchain-backed purchases without enough built-in confirmation safeguards. <br>
Mitigation: Manually confirm the merchant, amount, token, network, quantity, and product before running purchase commands. <br>
Risk: The configured LOBPAY_API_URL controls the checkout and purchase endpoints used by the scripts. <br>
Mitigation: Verify LOBPAY_API_URL before every use and only send API keys or payment headers to trusted LobPay endpoints. <br>


## Reference(s): <br>
- [LobPay Skill Page](https://clawhub.ai/web3senior/lobpay) <br>
- [LobPay API Reference](references/api.md) <br>
- [Database Schemas](references/schemas.md) <br>
- [X402 Protocol Integration](references/x402.md) <br>
- [X402 Spec](https://github.com/coinbase/x402) <br>
- [Base Docs](https://docs.base.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide API calls and local file updates performed by LobPay scripts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and scripts/package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
