## Description:

Collects public Xiaohongshu/RedNote notes, note details, comments, and creator posts through command-line workflows for downstream content, market, and social media analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

External users, marketers, content creators, and analysts use this skill to retrieve public Xiaohongshu content for topic research, competitor monitoring, KOL screening, comment insight, and trend analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Xiaohongshu queries, URLs, and collected data are sent to Guaikei using GUAIKEI_API_TOKEN.

Mitigation: Use the skill only when that data sharing is authorized, and do not use it for private, hidden, or login-gated content.

Risk: Generated logs may contain xsec_token URLs and collected data.

Mitigation: Keep logs private, avoid committing or sharing the logs directory, and rotate the API token if request URLs or logs are exposed.

Risk: GUAIKEI_API_TOKEN exposure could allow unauthorized API use.

Mitigation: Store the token in an environment variable or secret manager, avoid embedding it in prompts or source files, and rotate it after suspected exposure.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-xhs-note-and-comment)
- [Publisher profile](https://clawhub.ai/user/engheng-art)
- [Guaikei service website](https://www.guaikei.com)
- [Parameter and calling options](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [shell commands, configuration, JSON, guidance]

**Output Format:** [Markdown guidance with inline shell commands; executed commands return structured JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16.14.0+ and GUAIKEI_API_TOKEN; task results may be saved under logs/.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter and package.json report 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
