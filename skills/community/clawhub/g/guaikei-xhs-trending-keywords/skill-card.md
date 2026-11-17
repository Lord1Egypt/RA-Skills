## Description:

Retrieves public Xiaohongshu data for keyword search, note details, comments, and creator posts as structured JSON for trend research, competitor analysis, KOL screening, and comment analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External content creators, brand marketers, market analysts, and agent developers use this skill to collect public Xiaohongshu keyword results, note details, comments, and creator-post data for content planning, competitor monitoring, KOL screening, and trend analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary says the skill sends the API token in URL query strings.

Mitigation: Use a dedicated token, avoid exposing command output or network logs, and prefer an updated version that sends credentials in an Authorization header.

Risk: The security summary says returned data and tokenized Xiaohongshu links are automatically saved under a local logs directory.

Mitigation: Avoid shared or synced workspaces for sensitive research and delete generated logs when finished.

Risk: The skill is designed for public Xiaohongshu data retrieval and not private, hidden, login-only, publishing, liking, or account-interaction workflows.

Mitigation: Confirm the user request is limited to public data collection and verify authorization before redistributing collected data.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/engheng-art/skills/guaikei-xhs-trending-keywords)
- [Guaikei API access page](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON]

**Output Format:** [JSON data with concise Markdown guidance and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16.14.0+ and GUAIKEI_API_TOKEN; task results are saved under a local logs directory.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence; artifact metadata reports 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
