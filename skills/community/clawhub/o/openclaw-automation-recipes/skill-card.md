## Description:

OpenClaw automation recipes provides 10 practical automation scenarios for productivity tool enthusiasts and automation beginners.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yang1002378395-cmyk](https://clawhub.ai/user/yang1002378395-cmyk)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and automation beginners use this skill to adapt ready-made OpenClaw recipes for scheduled summaries, message routing, notifications, content publishing, backups, and monitoring workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recipes can automatically send messages, email replies, or public posts without built-in approval steps.

Mitigation: Review each recipe before enabling it and add approval or draft steps for email replies, notifications, and public posts.

Risk: Examples can upload, back up, or store data without specifying encryption, access controls, or retention.

Mitigation: Verify S3 bucket and database destinations, avoid sensitive data unless safeguards are defined, and configure encryption, access controls, and retention.

Risk: Broad schedules and keyword matches can trigger unwanted automation activity.

Mitigation: Limit schedules and keyword matches to the intended scope and test recipes before continuous operation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yang1002378395-cmyk/skills/openclaw-automation-recipes)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Shell commands, Guidance]

**Output Format:** [Markdown with YAML configuration examples and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recipes require user-specific review and customization before enabling automations.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
