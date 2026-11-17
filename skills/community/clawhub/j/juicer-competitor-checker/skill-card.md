## Description:

Compare a brand's social media with its competitors using Juicer. Finds each competitor's verified accounts on Instagram, TikTok, X, YouTube, LinkedIn, Facebook and Bluesky, then reports followers, posting frequency, top posts and hashtags side by side, with a short "what to copy" list.

This skill is ready for commercial/non-commercial use.

## Publisher:

[juicer](https://clawhub.ai/user/juicer)

### License/Terms of Use:

MIT-0

## Use Case:

Brand and marketing teams use the skill to compare their public social media accounts with up to four competitors. It summarizes recent posting and engagement patterns and suggests three ideas to try based on the returned posts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Juicer profile and post lookups consume credits, including account discovery.

Mitigation: Check the credit balance, share the estimated lookup cost, and confirm the accounts before running lookups.

Risk: A similar-looking account could be attributed to the wrong brand.

Mitigation: Verify each profile against its description, display name, or website URL; leave unclear accounts unreported.

Risk: Recurring scheduled comparisons can continue to consume credits.

Mitigation: Keep repeat runs optional and agree on the cadence before scheduling them.

## Reference(s):

- [Juicer MCP Server documentation](https://developers.juicer.io/mcp-server)
- [Juicer developer portal](https://www.juicer.io/developer)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown comparison report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses public account profiles and a recent post sample; missing data is reported as n/a.]

## Skill Version(s):

1.0.1 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
