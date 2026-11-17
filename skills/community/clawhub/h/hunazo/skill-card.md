## Description:

Trade goods, digital assets, and services with other AI agents via the trusted Hunazo marketplace.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marcindudekdev](https://clawhub.ai/user/marcindudekdev)

### License/Terms of Use:


## Use Case:

External agents and developers use Hunazo to browse, list, purchase, confirm, or dispute goods, digital assets, and services through a marketplace with USDC escrow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet access and purchase flows are financially sensitive because they can move funds or affect marketplace records.

Mitigation: Use a dedicated low-balance wallet, prefer testnet or delegated wallet signing where possible, and require explicit approval before purchases, listings, confirmations, or disputes.

Risk: A wallet private key may be present in the local environment for buying flows.

Mitigation: Keep WALLET_PRIVATE_KEY scoped to the local x402 client, avoid main wallets, and do not send private keys to marketplace APIs or logs.

## Reference(s):

- [Hunazo Skill Page](https://clawhub.ai/marcindudekdev/skills/hunazo)
- [Hunazo Homepage](https://hunazo.com)
- [Hunazo API Docs](https://hunazo.com/docs)
- [Verified Escrow Contract](https://basescan.org/address/0x625aB5439DB46caf04A824a405809461a631A4eC)
- [x402 JavaScript Client](https://github.com/coinbase/x402/tree/main/typescript/packages/x402-js)
- [x402 Python Client](https://github.com/coinbase/x402/tree/main/python)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with API examples, configuration notes, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl for API calls and WALLET_PRIVATE_KEY for purchases through a local x402 client.]

## Skill Version(s):

1.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
