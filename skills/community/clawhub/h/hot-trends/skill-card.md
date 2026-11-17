## Description:

Fetches real public trending data from Baidu Hot Search, Toutiao Hot Board, and GitHub Trending for demand discovery, trend analysis, and market insight.

This skill is ready for commercial/non-commercial use.

## Publisher:

[embracex1998](https://clawhub.ai/user/embracex1998)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and market analysts use this skill to collect current public trend lists and filter them by platform, programming language, or keyword for opportunity discovery and market monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes outbound requests to public Baidu, Toutiao, and GitHub endpoints.

Mitigation: Use it only in environments where those network requests are allowed, and narrow trigger phrases if agents auto-load skills aggressively.

Risk: Trend data and third-party page structures can change or become unavailable.

Mitigation: Treat results as time-sensitive public signals and rerun the skill or verify important findings against the source sites before acting on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/embracex1998/skills/hot-trends)
- [Publisher profile](https://clawhub.ai/user/embracex1998)
- [Baidu Hot Search endpoint](https://top.baidu.com/api/board?platform=wise&tab=realtime&offset=0&limit=30)
- [Toutiao hot board endpoint](https://www.toutiao.com/hot-event/hot-board/?origin=toutiao_pc)
- [GitHub Trending](https://github.com/trending)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Plain text trend listings with ranks, titles, heat indicators, optional language labels, and short repository descriptions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output depends on live public websites and may vary by time, network availability, keyword filter, platform, and GitHub language option.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
