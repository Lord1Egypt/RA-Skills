## Description:

Guaikei Douyin Discovery helps operators search public Douyin content, fetch creator posts, collect comments, and query real-time hot lists for content planning, competitor analysis, public sentiment monitoring, and trend tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

External operators, marketers, and analysts use this skill to gather structured JSON data from public Douyin search results, creator profiles, comments, and hot lists. It is suited for content planning, competitor review, public sentiment analysis, and trend monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a GUAIKEI_API_TOKEN and evidence.security reports credential-handling concerns.

Mitigation: Use a dedicated, revocable token, avoid sharing it, and rotate it if logs, shell history, or terminal output may have exposed it.

Risk: Requests and query data are sent to www.guaikei.com.

Mitigation: Do not submit private, confidential, or regulated data as search terms or URLs unless the deployment owner has approved that data flow.

Risk: Generated JSON logs may contain query details, result data, or other sensitive operational context.

Mitigation: Store logs in a protected location, limit access, and delete them when they are no longer needed.

Risk: evidence.security says runtime auth-error output may include promotional contact information despite the skill documentation promising neutral errors.

Mitigation: Review error output before deployment and avoid exposing raw authentication errors directly to end users.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/engheng-art/skills/guaikei-douyin-discovery)
- [Readme](readme.md)
- [Options Reference](references/options.md)
- [Changelog](references/changelog.md)
- [Input and Output JSON Schemas](assets/*.schema.json)
- [Guaikei Service Site](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Files, Guidance]

**Output Format:** [JSON on stdout, operational logs on stderr, and JSON log files saved under logs/]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single requests can return up to 10,000 public Douyin records when authorized.]

## Skill Version(s):

1.0.0 (source: package.json, references/changelog.md, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
