## Description:

Summarizes deterministic changes in price and key BSR fields from saved Amazon product snapshots and notes the sampling times.

This skill is ready for commercial/non-commercial use.

## Publisher:

[funewa](https://clawhub.ai/user/funewa)

### License/Terms of Use:

MIT-0

## Use Case:

Amazon sellers and product researchers use this skill to review changes in price and key Best Sellers Rank fields across saved product snapshots.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags unrelated spending controls and paid services in this snapshot, along with conflicting information about recurring costs.

Mitigation: Use a corrected watch-only package before connecting an ARI key; verify recurring refresh prices and require confirmation before spending credits.

## Reference(s):

- [Watch workflow](references/watch-workflow.md)
- [Watch reference](references/reference.md)
- [ARI operations workspace](https://ari.funewa.com/zh/operations)
- [ClawHub release page](https://clawhub.ai/funewa/skills/price-bsr-track)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Markdown snapshot summary with sampling times and price/BSR change fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Snapshot-based; does not provide real-time prices or ranks, sales estimates, or predictions.]

## Skill Version(s):

1.5.3 (source: server release metadata, artifact _meta.json, artifact CHANGELOG.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
