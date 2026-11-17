## Description:

Read social media performance from PostLake: per-post results and normalised cross-platform analytics (impressions, reach, engagement, CTR, follower growth). Use to report on results or decide what to post next.

This skill is ready for commercial/non-commercial use.

## Publisher:

[postlake](https://clawhub.ai/user/postlake)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to query PostLake analytics for individual posts or cross-platform reporting periods, then summarize performance and recommend what to post next.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a bearer API key to query PostLake analytics.

Mitigation: Use a read-only, scoped POSTLAKE_API_KEY when available and avoid granting broader PostLake permissions than analytics reporting requires.

Risk: Analytics may lag because metrics are only as fresh as each social platform reports.

Mitigation: Tell users when recent posts may still be updating and prefer longer reporting windows for decisions that depend on stable trends.

## Reference(s):

- [PostLake analytics skill page](https://clawhub.ai/postlake/skills/postlake-analytics)
- [PostLake API base URL](https://api.postlake.dev)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell command examples and concise analytics summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a user-provided POSTLAKE_API_KEY and reports metrics subject to platform freshness delays.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
