## Description:

Retrieves public Xiaohongshu data for note search, note details, comments, and creator public posts, returning structured results for content, competitor, KOL, and sentiment analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

External users, content creators, brand marketers, data analysts, and operators use this skill to collect public Xiaohongshu search results, note details, comments, and creator posts for planning, market research, competitor monitoring, KOL screening, and sentiment analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Commands send Xiaohongshu keywords, note or profile URLs, limits, and GUAIKEI_API_TOKEN to www.guaikei.com.

Mitigation: Use the skill only when that external data transfer is acceptable, keep the token out of shared logs and prompts, and rotate the token if it may have been exposed.

Risk: Successful runs save retrieved result data under the local logs directory.

Mitigation: Review, secure, or clean saved log files after use, especially when collected content may be sensitive for the user's workflow.

Risk: The server security verdict is suspicious because credential handling and saved results need review before installation.

Mitigation: Review the security summary and guidance before deployment, and restrict use to public Xiaohongshu data with appropriate authorization.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/engheng-art/skills/guaikei-xhs-note-detail)
- [Guaikei API service](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance, Files]

**Output Format:** [JSON stdout from Node.js CLI commands, with brief human-facing status or guidance and saved JSON logs after successful runs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN; supports keyword, note URL, profile URL, content type, sort, time range, and limit parameters.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata, package.json, constants.js, and changelog report 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
