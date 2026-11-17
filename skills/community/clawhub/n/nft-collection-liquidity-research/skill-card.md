## Description:

Compares observed OpenSea collection depth, bids and asks, activity, holders, and traits through Crawlora for a source-attributed liquidity snapshot.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

NFT researchers and developers use this skill to compare observed collection liquidity, marketplace activity, and holder and trait data while tracking identity, currency, timing, and coverage gaps. It supports research snapshots, not trading decisions or transactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Collection queries are sent to Crawlora using a Crawlora API key.

Mitigation: Use a scoped key, keep it private, and share only collection searches and slugs you are comfortable sending to Crawlora.

Risk: A liquidity snapshot can have incomplete coverage or omit conditions needed to execute an offer.

Mitigation: Preserve source, currency, timing, and coverage gaps; do not treat observed quotes as fillable orders or use the snapshot to make trades.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/crawlora-org/skills/nft-collection-liquidity-research)
- [Crawlora endpoint reference](reference/endpoints.md)
- [Crawlora API](https://api.crawlora.net/api/v1)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown research snapshot with source attribution and coverage ledger]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves collection and contract identity, quote currencies, observation times, and incomplete coverage.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
