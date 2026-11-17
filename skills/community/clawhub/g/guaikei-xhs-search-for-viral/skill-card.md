## Description:

Provides structured retrieval of Xiaohongshu public data for viral note search, note details, comment analysis, and creator post monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, marketers, operators, and analysts use this skill to collect Xiaohongshu public-data signals for topic research, competitor monitoring, KOL review, comment insight, and marketing retrospectives. It retrieves data for downstream analysis and does not replace strategy judgment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Xiaohongshu keywords, note or profile URLs, retrieved content, and the Guaikei API token to the Guaikei service.

Mitigation: Use it only when that data sharing is acceptable, prefer a narrowly scoped token when available, and avoid sensitive research in shared workspaces.

Risk: The security summary notes credentials are sent in URL query strings.

Mitigation: Protect shell history, terminal output, proxy logs, and other request logs that may capture URLs, and rotate the token if exposure is suspected.

Risk: Retrieved data and access-bearing Xiaohongshu URLs are saved automatically to a local logs directory.

Mitigation: Restrict access to the logs directory and delete or archive generated result files according to the user's data-retention policy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-xhs-search-for-viral)
- [Publisher profile](https://clawhub.ai/user/engheng-art)
- [Guaikei API service](https://www.guaikei.com)
- [Options reference](artifact/references/options.md)
- [Changelog](artifact/references/changelog.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Structured JSON results with concise Markdown guidance and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN and writes retrieved task results to local JSON files under logs/.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
