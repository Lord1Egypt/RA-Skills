## Description:

Discover pain points, frustrations, and unmet needs on Reddit using the PullPush API without requiring API keys.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yanji84](https://clawhub.ai/user/yanji84)

### License/Terms of Use:

MIT

## Use Case:

External users, founders, product teams, and researchers use this skill to find Reddit complaints, agreement signals, failed solutions, and possible startup opportunities in a chosen domain.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search topics, subreddit selections, and post IDs are sent to the PullPush API.

Mitigation: Avoid confidential business plans, sensitive personal topics, and private client information in query terms or post selections.

Risk: Reddit complaint analysis may reflect anecdotal or unrepresentative demand signals.

Mitigation: Use validationStrength, agreement counts, comment evidence, and independent follow-up validation before making product or investment decisions.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/yanji84/skills/pain-point-finder)
- [PullPush API](https://api.pullpush.io)
- [Subreddit seed lists](references/SUBREDDITS.md)
- [Pain Point Finder implementation notes](docs/pain_point_discovery.md)

## Skill Output:

**Output Type(s):** [JSON, Markdown, Shell commands, Guidance]

**Output Format:** [JSON from CLI commands and Markdown synthesis with structured pain point proposals]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js; sends search topics, subreddit selections, and post IDs to PullPush.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
