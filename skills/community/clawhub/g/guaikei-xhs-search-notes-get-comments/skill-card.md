## Description:

Provides structured public Xiaohongshu data for note search, note details, creator post monitoring, and comment retrieval to support content planning, competitor monitoring, KOL screening, and comment insights.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users, content operators, marketers, and analysts use this skill to retrieve structured public Xiaohongshu notes, creator posts, note details, and comments for trend research, campaign planning, competitive analysis, and report preparation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API credentials and submitted keywords or URLs are sent to guaikei.com, and the security evidence notes credentials are placed in URL query strings.

Mitigation: Use a least-privilege GUAIKEI_API_TOKEN, avoid sensitive or regulated research targets unless authorized, and rotate the token if it may have appeared in logs or infrastructure traces.

Risk: Retrieved Xiaohongshu data and source URLs are automatically saved as plaintext files in the local logs directory.

Mitigation: Run the skill only in workspaces where plaintext logs are acceptable, restrict workspace access, and clean the logs directory when the task is complete.

Risk: The security verdict is suspicious and calls for review before installation.

Mitigation: Review and scan the artifact before deployment, then approve use only for authorized public-data collection workflows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/engheng-art/skills/guaikei-xhs-search-notes-get-comments)
- [Guaikei API Service](https://www.guaikei.com)
- [Options Reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON results with status, request metadata, execution metadata, and retrieved Xiaohongshu records; guidance may include Markdown and shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16.14.0 or newer and GUAIKEI_API_TOKEN; command results are also saved to local logs.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata and changelog report 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
