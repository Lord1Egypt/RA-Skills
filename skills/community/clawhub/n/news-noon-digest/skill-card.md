## Description:

Generates a Chinese noon news digest with global, technology, and finance sections and supports scheduled posting to Feishu and QQ.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cp3d1455926-svg](https://clawhub.ai/user/cp3d1455926-svg)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to configure a scheduled Chinese noon digest and send it to workplace messaging channels. It is aimed at users who want recurring summaries of global, technology, and finance headlines through OpenClaw cron and Feishu webhook configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The digest may present hardcoded sample text as current fetched news.

Mitigation: Review and replace the fetching behavior before using it for real automated news delivery; label output clearly if it remains sample content.

Risk: Scheduled external posting can distribute stale or inaccurate content through configured messaging channels.

Mitigation: Test manually before enabling cron, restrict webhook access, and monitor scheduled posts until the news source behavior is verified.

Risk: QQ delivery is claimed by the artifact but appears unimplemented in the security evidence.

Mitigation: Treat QQ posting as unavailable until the delivery path is implemented and tested.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cp3d1455926-svg/skills/news-noon-digest)
- [World Monitor](https://www.worldmonitor.app/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Chinese digest text with setup commands and environment-variable configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May post text messages through a Feishu webhook; QQ delivery is claimed, but security evidence says it appears unimplemented.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
