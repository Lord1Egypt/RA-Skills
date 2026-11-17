## Description:

Analyze YouTube videos and channels through the KeyAPI REST API using live official docs for video, comment, search, trend, channel, and identifier workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xyzzero](https://clawhub.ai/user/xyzzero)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and content teams use this skill to turn natural-language YouTube research questions into documentation-checked KeyAPI workflows for video, channel, comments, search, trends, and reporting tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: YouTube research inputs are sent to KeyAPI during live workflows.

Mitigation: Install and use the skill only when sending those inputs to KeyAPI is acceptable for the task and organization.

Risk: Authentication helpers can persist KEYAPI_TOKEN in a shell profile.

Mitigation: Prefer a session-only KEYAPI_TOKEN when possible, avoid passing tokens on the command line, and review or remove managed shell-profile entries after use.

Risk: Helper scripts can read user-selected input files and overwrite user-selected output paths.

Mitigation: Avoid file-input flags for sensitive files, use temporary paths for internal analysis, and choose output paths carefully before running file-writing commands.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xyzzero/skills/keyapi-youtube)
- [KeyAPI documentation index](https://docs.keyapi.ai/llms.txt)
- [KeyAPI YouTube documentation](https://docs.keyapi.ai/en/youtube/)
- [KeyAPI authentication documentation](https://docs.keyapi.ai/overview/authentication#bearer-authentication)
- [Global Rules](references/global-rules.md)
- [Scenario Cards](references/scenarios.md)
- [Routing Policy](references/routing-policy.md)
- [Setup And Auth](references/setup-and-auth.md)
- [YouTube Rules](references/youtube-rules.md)
- [YouTube Video Rules](references/youtube-video-rules.md)
- [YouTube Channel Rules](references/youtube-channel-rules.md)
- [YouTube Search And Trends Rules](references/youtube-search-trends-rules.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance, API Calls]

**Output Format:** [Markdown responses with inline shell commands and optional JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May make live KeyAPI REST calls when configured with KEYAPI_TOKEN; large results can be written to a user-selected output file.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
