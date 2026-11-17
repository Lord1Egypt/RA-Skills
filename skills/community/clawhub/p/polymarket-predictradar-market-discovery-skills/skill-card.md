## Description:

Polymarket hot market rankings and new market discovery for trending markets, newly listed high-momentum markets, and active markets by category.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cnica](https://clawhub.ai/user/cnica)

### License/Terms of Use:

MIT-0

## Use Case:

External users and market researchers use this skill to discover Polymarket markets by recent trading activity, new-market momentum, and category. It returns live market discovery summaries for user-facing analysis, not financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run broad market and wallet-profile analyses that may expose or overemphasize public wallet-position patterns.

Mitigation: Review prompts and outputs before use, limit analysis to the user's requested market-discovery task, and avoid presenting smart-money labels as investment recommendations.

Risk: The skill is instructed to hide specific data-provider details while adding PredicTradar branding, which can reduce transparency.

Mitigation: Disclose material data-source limitations to users when they affect interpretation, especially for incomplete trade windows, unavailable enrichment, or stale query results.

Risk: Users may misread market discovery output as financial advice.

Mitigation: Frame results as informational market discovery and include that prices, volumes, trader counts, and rankings are snapshots from available data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cnica/skills/polymarket-predictradar-market-discovery-skills)
- [Publisher profile](https://clawhub.ai/user/cnica)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown market summaries with clickable links and concise ranked tables or lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses live query results for prices, volume, trader counts, categories, and end dates; output should not fabricate unavailable fields.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
