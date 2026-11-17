## Description:

Searches public Xiaohongshu notes, retrieves note details and comments, and fetches public creator posts for structured content, competitor, KOL, and trend analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users, content creators, marketers, and analysts use this skill to collect public Xiaohongshu note, comment, and creator-post data for topic research, competitor monitoring, KOL screening, and comment insight workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Xiaohongshu URLs, search keywords, limits, and GUAIKEI_API_TOKEN to Guaikei's API.

Mitigation: Install only when this data sharing is acceptable, keep the token restricted to this use, and rotate it if exposure is suspected.

Risk: Generated logs may contain collected content, request details, or other sensitive workflow data.

Mitigation: Treat the logs directory as sensitive, review file retention practices, and delete old result files when they are no longer needed.

Risk: Authentication is passed through request parameters according to the artifact behavior and ClawHub security guidance.

Mitigation: Prefer a publisher update that moves authentication out of query parameters before broad or low-friction deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-xhs-find-notes)
- [Guaikei API support site](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and structured JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and GUAIKEI_API_TOKEN; command results are saved under logs/ by the artifact.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
