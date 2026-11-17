## Description:

Collects KOL, social media, SEO, and advertising signals to help product and operations teams identify candidate AI visual-agent trends and generate Slack-ready reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lygjoey](https://clawhub.ai/user/lygjoey)

### License/Terms of Use:

MIT-0

## Use Case:

Product, operations, and growth teams use this skill to gather multi-channel trend, SEO, and advertising evidence for AI visual product selection and campaign planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles API credentials broadly and may read tokens from shell startup configuration.

Mitigation: Use dedicated, least-privilege API tokens and provide them explicitly in the runtime environment instead of relying on shared shell configuration.

Risk: Reports may surface adult, nudification, or creator-likeness reuse opportunities that are not suitable for product decisions without review.

Mitigation: Filter or remove this content before using the outputs for roadmap, product, or campaign decisions.

Risk: External data sources can incur paid usage or rate limits during full pipeline runs.

Mitigation: Use test mode, result limits, and scheduled runs that match API budgets and source terms.

## Reference(s):

- [Trend Methodology](artifact/TREND_METHODOLOGY.md)
- [Apify API](https://api.apify.com/v2)
- [ClawHub Skill Page](https://clawhub.ai/lygjoey/skills/omni-channel-agent)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration]

**Output Format:** [Slack-formatted text reports, JSON data files, and CLI command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes timestamped reports and channel data files under output/ when the pipeline runs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
