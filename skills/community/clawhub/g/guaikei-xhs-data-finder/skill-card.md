## Description:

Searches public Xiaohongshu notes by keyword, fetches note details, comments, and author posts, and returns structured data for trend, content, competitor, and comment analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, marketers, market researchers, and data analysts use this skill to collect public Xiaohongshu search results, note details, comments, and author post data for topic research, competitor monitoring, KOL screening, trend tracking, and report preparation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: GUAIKEI_API_TOKEN, search keywords, Xiaohongshu URLs, and returned public data are sent to the guaikei.com API.

Mitigation: Use a scoped or disposable token if available, avoid sensitive targets, confirm data-sharing authorization before use, and rotate the token if it may have been exposed.

Risk: Successful results are automatically saved under local logs, which may retain collected datasets and request context.

Mitigation: Keep the workspace private, review logs after each run, and delete or archive them according to the user's retention policy.

Risk: The security verdict is suspicious due to token handling and local retention concerns.

Mitigation: Review the skill before execution, verify the configured token source, and run only with public Xiaohongshu targets that the user is comfortable retaining.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-xhs-data-finder)
- [Guaikei API token and service site](https://www.guaikei.com)
- [Options and invocation reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and structured JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16.14.0 or newer and GUAIKEI_API_TOKEN; successful command results are written to local logs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
