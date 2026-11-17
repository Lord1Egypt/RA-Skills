## Description:

Retrieves structured JSON for public Xiaohongshu keyword searches, note details, note comments, and creator post lists through the Guaikei API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users, marketers, content operators, analysts, and developers use this skill to collect public Xiaohongshu data for content research, competitive monitoring, KOL review, trend analysis, and comment insight workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries, note/profile URLs, and GUAIKEI_API_TOKEN are sent to the third-party Guaikei service.

Mitigation: Use the skill only when that data sharing is acceptable, avoid sensitive inputs, and rotate or restrict the API token where possible.

Risk: Fetched results are saved locally by default and may contain sensitive business research or user-generated content.

Mitigation: Treat generated logs as sensitive, limit access to them, and delete them when they are no longer needed.

Risk: The skill only supports public Xiaohongshu data and may return empty or error results for private, deleted, inaccessible, or mismatched links.

Mitigation: Confirm inputs are public and of the expected type, handle status and error_code fields explicitly, and do not fabricate conclusions from empty results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-xhs-tool)
- [Guaikei API service](https://www.guaikei.com)
- [Options and invocation guide](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Files, Guidance]

**Output Format:** [Markdown guidance with inline shell commands; command execution returns structured JSON and may write local log files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16.14.0+ and GUAIKEI_API_TOKEN; each request can return up to 10000 items according to artifact documentation.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact metadata reports 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
