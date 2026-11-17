## Description:

Monitor PopMart product restock status across multiple channels including WeChat Mini Programs, Taobao, JD.com, and Tmall.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iiustrator](https://clawhub.ai/user/iiustrator)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to configure PopMart product watch lists, run stock checks across supported commerce channels, and receive restock notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security summary says the skill overstates implemented capabilities and should be treated as an incomplete prototype.

Mitigation: Review the implementation before installing or relying on alerts, and confirm platform handlers are complete for the channels being monitored.

Risk: The server security guidance warns against placing real API secrets or webhook tokens in workspace JSON without understanding file visibility.

Mitigation: Keep secrets out of shared configuration files and use a controlled secret-management approach before enabling live notifications.

Risk: The server security guidance cautions against cron or long-running checks until the implementation is fixed and destinations are constrained.

Mitigation: Do not enable persistent monitoring until network destinations, notification endpoints, rate limits, and removal instructions have been reviewed.

## Reference(s):

- [PopMart Stock Monitor Setup Guide](references/SETUP_GUIDE.md)
- [OpenClaw Integration Guide](references/OPENCLAW_INTEGRATION.md)
- [Example Configuration](references/example_config.json)
- [Taobao Open Platform](https://open.taobao.com/)
- [JD Open Platform](https://jos.jd.com/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON configuration examples, bash commands, and Python script usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce monitoring configuration, execution commands, and restock notification payloads.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
