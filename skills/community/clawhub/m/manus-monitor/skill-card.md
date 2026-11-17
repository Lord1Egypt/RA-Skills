## Description:

Create and manage AI agent tasks via Manus API. Manus is an autonomous AI agent that can browse the web, use tools, and deliver complete work products.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tallman2014](https://clawhub.ai/user/tallman2014)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to create Manus agent tasks, poll task status, list and download task outputs, save task IDs, and monitor saved tasks through recurring OpenClaw checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A saved Manus task can automatically create a recurring OpenClaw monitor that runs every minute.

Mitigation: Review the monitor behavior before installing and remove or explicitly control the cron monitor unless recurring polling is intended.

Risk: Repeated Manus API polling and optional Telegram notifications can expose task metadata or sensitive task content.

Mitigation: Avoid sensitive prompts or outputs unless notification settings and recipients are explicitly controlled.

Risk: The skill can download local files from Manus task output URLs.

Mitigation: Inspect downloaded files before opening, sharing, or attaching them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tallman2014/skills/manus-monitor)
- [Manus Homepage](https://manus.im)
- [Manus API Reference](https://open.manus.ai/docs)
- [Manus Documentation](https://manus.im/docs)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with bash commands, JSON API responses, and local file paths for downloaded outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MANUS_API_KEY; saved tasks can trigger recurring status checks and optional Telegram notifications.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
