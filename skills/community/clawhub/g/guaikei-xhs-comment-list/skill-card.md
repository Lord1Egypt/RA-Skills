## Description:

Retrieves structured public Xiaohongshu data for keyword search, note details, note comments, and creator post lists, with a documented per-request limit of up to 10,000 items.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users, content operators, marketers, and analysts use this skill to retrieve public Xiaohongshu search results, note details, comments, and creator posts for downstream summarization, comparison, reporting, and trend analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Xiaohongshu keywords, URLs, and task parameters are sent to guaikei.com using a GUAIKEI_API_TOKEN.

Mitigation: Use the skill only when that data transfer is authorized, keep the token secret, and rotate it if it appears in logs or shared output.

Risk: Collected social-media data and task results may be written to a local logs/ directory.

Mitigation: Run in a controlled workspace and review, retain, or delete generated logs according to the user's data-handling policy.

Risk: The API token is included in request query parameters to guaikei.com.

Mitigation: Avoid running behind verbose proxy or HTTP request logging, and rotate the token if such logs are exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-xhs-comment-list)
- [Guaikei API token and service site](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Files, Guidance]

**Output Format:** [JSON results and concise Markdown guidance, with optional saved log files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16.14.0+ and GUAIKEI_API_TOKEN; commands may save task results under logs/.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence; artifact metadata reports 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
