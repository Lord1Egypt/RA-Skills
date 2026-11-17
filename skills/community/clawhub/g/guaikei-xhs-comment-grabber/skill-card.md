## Description:

Retrieves public Xiaohongshu creator posts, note details, comments, and interaction metrics so agents can support KOL screening, competitive research, trend monitoring, and comment analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users, marketers, content operators, and analysts use this skill to collect public Xiaohongshu search results, post details, creator posts, and comments for downstream summaries, comparisons, reports, and campaign decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Xiaohongshu keywords or URLs, returned public social data, and the required GUAIKEI_API_TOKEN to guaikei.com.

Mitigation: Use the skill only when that data sharing is acceptable, prefer a scoped or disposable token when available, and rotate any token already used with this release.

Risk: Fetched public comments or business research results may be written to local logs.

Mitigation: Review the local logs directory after use and delete retained results when they contain sensitive research or comments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-xhs-comment-grabber)
- [GuaiKei API and token site](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with shell commands and structured JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16.14.0 or newer and a GUAIKEI_API_TOKEN for API-backed commands.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata reports 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
