## Description:

Provides Xiaohongshu (小红书/RedNote) public-data retrieval for content research, including keyword search, note details, comments, and creator post collections.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

Content creators, marketing teams, market analysts, and creator-operations teams use this skill to collect public Xiaohongshu posts, note details, comments, and creator post sets for topic research, competitive monitoring, trend analysis, and KOL screening.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Xiaohongshu keywords, links, limits, and fetched public-content requests to Guaikei using GUAIKEI_API_TOKEN.

Mitigation: Install only when this data sharing is acceptable for the intended use; keep the token out of shared logs and rotate it if exposure is suspected.

Risk: CLI runs save structured result logs that may contain research inputs, Xiaohongshu URLs, and fetched public-content data.

Mitigation: Treat generated logs as sensitive, avoid shared workspaces for sensitive research, and review or delete logs after use.

## Reference(s):

- [Guaikei documentation and API access](https://www.guaikei.com)
- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-xhs-search-detail-comment-creator)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance, JSON, files]

**Output Format:** [Markdown guidance with Node.js command examples; CLI stdout and saved logs contain structured JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16.14.0+ and GUAIKEI_API_TOKEN; documented result limits are up to 10000 records per request.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata; artifact metadata and package.json report 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
