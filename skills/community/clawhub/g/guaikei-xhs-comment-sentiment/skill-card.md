## Description:

Returns structured JSON for public Xiaohongshu content, note details, comments, and creator posts so agents can support topic research, sentiment review, competitive monitoring, and trend analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External analysts, marketers, content operators, and agents use this skill to collect public Xiaohongshu search results, note details, comments, and creator posts for topic planning, comment sentiment review, competitor monitoring, and trend analysis. It provides source data for analysis and reporting rather than final report layout.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Xiaohongshu keywords, links, and the Guaikei API token are sent to guaikei.com.

Mitigation: Install only when that data sharing is acceptable, use a scoped and revocable token, and rotate the token if URLs or requests may have been exposed.

Risk: Generated result files may persist public-content queries, links, and returned data in a local logs directory.

Mitigation: Protect the logs directory, limit access to generated files, and delete logs when they are no longer needed.

Risk: The skill is intended for public Xiaohongshu data collection and may be inappropriate for private, unauthorized, or restricted data use.

Mitigation: Use it only for public or authorized data and avoid requests involving private, hidden, login-only, or unauthorized content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-xhs-comment-sentiment)
- [Guaikei API service](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Structured JSON from CLI stdout, with concise Markdown guidance and command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands require Node.js 16.14.0 or newer and the GUAIKEI_API_TOKEN environment variable; results may also be saved under a local logs directory.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata reports 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
