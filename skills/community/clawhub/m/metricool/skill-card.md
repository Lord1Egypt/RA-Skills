## Description:

Schedule and manage social media posts via Metricool API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[willscott-v2](https://clawhub.ai/user/willscott-v2)

### License/Terms of Use:

MIT

## Use Case:

Developers, operators, and social media teams use this skill to list Metricool brands, schedule posts across connected social platforms, review scheduled posts, and retrieve best-time-to-post analytics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Metricool credentials can allow access to connected brands, scheduled posts, analytics, and post creation.

Mitigation: Use least-privilege Metricool credentials where possible and keep unrelated secrets out of the workspace .env file.

Risk: If blogId is omitted, scripts may auto-select the first available brand.

Mitigation: Specify blogId explicitly when scheduling or reading posts so the intended brand is used.

Risk: Scheduled content can be posted to multiple external social platforms.

Mitigation: Review target platforms, scheduled time, post text, media URL, and platform character limits before running scheduling commands.

## Reference(s):

- [Metricool](https://metricool.com)
- [ClawHub Metricool skill page](https://clawhub.ai/willscott-v2/skills/metricool)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call Metricool API scripts that return console text or JSON and can create scheduled social media posts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
