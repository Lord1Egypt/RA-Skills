## Description:

Mint a Crown Race Pass (CROWN) NFT on BNB Chain - the daily crown competition for Binance .ai Agent ID holders. First 500 passes FREE via mint() at value 0; after that mintPaid() at exactly 0.0007 BNB. Max 1 pass per wallet, ever. Use when your human wants a Crown Pass or asks you to mint one, boost points, or settle the daily race.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pokemontownss](https://clawhub.ai/user/pokemontownss)

### License/Terms of Use:

MIT-0

## Use Case:

Wallet owners with a Binance .ai Agent ID use this skill to check eligibility and mint a Crown Race Pass on BNB Chain. Pass holders can also use it to make optional paid boosts or settle the daily race.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Contract legitimacy and deployed behavior have not been independently verified.

Mitigation: Before signing, independently confirm the contract address and simulate the transaction when your wallet supports it.

Risk: Minting and repeatable boosts spend BNB, and race rewards are not guaranteed.

Mitigation: Approve only the exact stated transaction cost, set a spending limit for boosts, and treat competition rewards as uncertain.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/pokemontownss/skills/mint-crown-pass)
- [Crown Race site](https://crownrace.site)
- [Crown Race machine-readable guide](https://crownrace.site/llms.txt)
- [Crown Race mint manifest](https://crownrace.site/mint.json)
- [Sourcify contract record](https://sourcify.dev/#/lookup/0x924B1c9203EBC3EE3D4Fd2Af758B2DBDD3856e0c)

## Skill Output:

**Output Type(s):** [Guidance, API Calls]

**Output Format:** [Markdown with contract call parameters and BNB values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes eligibility preflight checks, lane-specific mint amounts, optional boost tiers, and settle instructions.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
