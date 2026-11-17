## Description:

Helps agents search public Douyin content, retrieve creator posts and comments, and fetch live trending lists for short-video research, competitive analysis, sentiment review, and topic planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to collect structured public Douyin data for content operations, competitor research, viral-topic selection, comment analysis, and trend monitoring. It does not provide publishing, editing, watermark removal, or account-operation services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags unsafe handling of the GUAIKEI_API_TOKEN and recommends review before installation.

Mitigation: Install only when comfortable sending Douyin keywords, URLs, and request metadata to Guaikei; rotate or scope the token where possible and prefer a version that sends credentials through an Authorization header.

Risk: The skill can auto-trigger for broad short-video research requests, which may send unintended queries to the third-party service.

Mitigation: Require explicit user confirmation for Douyin data collection and narrow invocation to clearly stated Douyin research tasks.

Risk: Returned search, comment, and account data may be written to local JSON logs.

Mitigation: Review local log contents, avoid sensitive inputs, and delete or disable logs according to the user's retention requirements.

Risk: Server security evidence reports contradictions between advertised runtime-authentication safeguards and observed behavior.

Mitigation: Review authentication failure paths before deployment and prefer a version that removes runtime promotional contact messages.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-douyin-trending-for-hotspot-tracking)
- [Guaikei token and support site](https://www.guaikei.com)
- [Complete option reference](references/options.md)
- [Changelog](references/changelog.md)
- [Input and output JSON schemas](assets/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON, Files, Guidance]

**Output Format:** [Markdown guidance with shell commands; command execution returns structured JSON and local JSON log files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js >= 16.14.0 and GUAIKEI_API_TOKEN; successful CLI commands write pure JSON to stdout and may save result logs under logs/.]

## Skill Version(s):

1.0.0 (source: SKILL.md metadata, package.json, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
