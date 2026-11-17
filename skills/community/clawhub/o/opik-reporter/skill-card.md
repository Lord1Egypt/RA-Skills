## Description:

Opik observability reporter - fetches traces, analyzes usage, costs, and errors, then sends reports to Discord.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunnyhot](https://clawhub.ai/user/sunnyhot)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to generate recurring or manual Opik observability reports about trace activity, token usage, costs, errors, and Discord delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hardcoded Opik API key and Discord destination could expose credentials or send reports to an unintended channel.

Mitigation: Rotate the exposed key if real, replace it with a user-supplied secret, and require users to choose the Discord target before running the skill.

Risk: Recurring automatic sends can post monitoring reports without a local review step.

Mitigation: Add a dry-run or local-only mode and verify the schedule, workspace, project, and destination before enabling cron delivery.

Risk: The current artifact behavior includes mock usage, cost, tool-call, and error figures.

Mitigation: Clearly label mock output or implement live Opik data collection before using the reports for operational decisions.

## Reference(s):

- [Opik](https://www.comet.com/opik/)
- [Opik API](https://www.comet.com/opik/api)
- [Opik Reporter on ClawHub](https://clawhub.ai/sunnyhot/skills/opik-reporter)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report text with shell command and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may be truncated for Discord delivery; the current artifact behavior includes mock observability figures.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, package.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
