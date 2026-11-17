## Description:

Gets GitHub trending projects for daily, weekly, or monthly periods, visits each repository to understand its functionality, and returns Chinese-language summaries with descriptions, statistics, and README-derived details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhuxiaoke27](https://clawhub.ai/user/zhuxiaoke27)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and engineers use this skill to inspect current GitHub trending repositories, compare trend periods, filter by programming language, and generate weekly or monthly trend reports in Chinese.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill accesses public GitHub trending and repository pages, so results can change over time or be unavailable due to network errors.

Mitigation: Treat generated trend reports as point-in-time summaries and preserve the artifact's fallback behavior for skipped or unavailable repository details.

Risk: Optional caching may store public GitHub trending results when the agent chooses to use the cache strategy.

Mitigation: Keep cached data limited to public trending results and refresh or discard cached files when current trend accuracy matters.

Risk: The artifact requires Chinese output, which may not match every user's preferred language.

Mitigation: Set user expectations that the normal response format is Chinese Markdown unless the deployment intentionally adapts the output language.

## Reference(s):

- [GitHub Trending](https://github.com/trending)
- [ClawHub Skill Page](https://clawhub.ai/zhuxiaoke27/skills/github-trending-analysis)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Chinese Markdown reports with repository links, project statistics, README-derived summaries, comparisons, and trend insights.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default output covers the top 10 repositories; artifact evidence describes optional period, limit, language, compare, and report modes.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
