## Description:

Helps agents resolve Talvio Dot Robot NFTs in DOTFIELD on BNB Chain through free or paid minting paths and post-seal $DOT claims.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pokemontownss](https://clawhub.ai/user/pokemontownss)

### License/Terms of Use:

MIT-0

## Use Case:

External users can ask an agent to resolve a Talvio Dot Robot NFT in DOTFIELD or discharge an eligible unit to claim $DOT. The skill provides the checks and transaction details for BNB Chain.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Minting or discharge transactions can spend BNB and interact with on-chain assets.

Mitigation: Before signing, confirm the requested action, BNB Chain network, contract address, transaction value, and current eligibility with the human.

Risk: Daily quotas, eligibility, and the paid mint price depend on live contract state.

Mitigation: Read the current contract state and calculate the exact required value immediately before submitting; stop if a pre-check fails.

## Reference(s):

- [TalvioGenerate DOTFIELD site](https://talviogenerate.com)
- [Mint reference](https://talviogenerate.com/mint.json)
- [Agent reference](https://talviogenerate.com/agent.json)
- [LLM reference](https://talviogenerate.com/llms.txt)

## Skill Output:

**Output Type(s):** [Guidance, Transaction instructions]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes BNB Chain contract addresses, function selectors, and transaction values.]

## Skill Version(s):

1.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
