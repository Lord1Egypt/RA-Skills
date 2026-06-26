## Description: <br>
moonfun_sdk helps developers create AI-generated meme tokens on Binance Smart Chain and run experimental buy and sell workflows through the MoonnFun platform. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[moonnfunOfficial](https://clawhub.ai/user/moonnfunOfficial) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers use this skill to install and use a Python SDK for creating BSC meme tokens with AI-generated images, checking balances, and optionally testing token trading flows. It is intended for wallet-backed blockchain workflows where users review transactions and configure endpoints before use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet-backed token creation and trading can spend real BNB or tokens. <br>
Mitigation: Use a dedicated low-balance wallet and review transactions before calling create_meme, buy_token, or sell_token. <br>
Risk: The default image-generation endpoint uses HTTP, and prompts, images, token metadata, wallet addresses, and signatures are shared with external services. <br>
Mitigation: Configure an HTTPS or self-hosted image API where possible and treat submitted prompts, images, metadata, addresses, and signatures as external-service data. <br>
Risk: Experimental trading may submit trades with min_received set to 0 when quote failures occur. <br>
Mitigation: Use small amounts, avoid low-liquidity trades unless intentionally testing, and inspect slippage and transaction details before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/moonnfunOfficial/moonfunsdk) <br>
- [Publisher profile](https://clawhub.ai/user/moonnfunOfficial) <br>
- [Artifact README](artifact/README.md) <br>
- [SDK README](artifact/python/README.md) <br>
- [Security guide](artifact/python/SECURITY.md) <br>
- [Changelog](artifact/python/CHANGELOG.md) <br>
- [MoonnFun platform](https://moonn.fun) <br>
- [BSC explorer](https://bscscan.com) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration] <br>
**Output Format:** [Markdown with Python and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes SDK usage examples, installation commands, endpoint configuration, and wallet safety guidance.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata, setup.py, changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
