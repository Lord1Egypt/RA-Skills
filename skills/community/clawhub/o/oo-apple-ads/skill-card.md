## Description:

Apple Ads (ads.apple.com). Use this skill for ANY Apple Ads request — reading, creating, updating, and deleting data. Whenever a task involves Apple Ads, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Advertisers and ad operators use this skill to inspect Apple Ads account data and manage campaigns, ads, keywords, budgets, creatives, and performance through a connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fallback setup executes downloaded CLI installer software whose local effects are not established by the supplied evidence.

Mitigation: Review and approve CLI installation separately before using fallback setup, connect only intended Apple Ads accounts, and retain approval for exact spending changes and deletions.

## Reference(s):

- [Apple Ads Platform API documentation](https://developer.apple.com/documentation/apple-ads-platform-api)
- [Apple Ads](https://ads.apple.com/)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Structured API data with concise natural-language summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Available data depends on connected Apple Ads account permissions and the selected action.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
