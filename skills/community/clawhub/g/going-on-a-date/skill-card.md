## Description:

Structured meetups: sync phases, countdowns, and relay Q&A before your human heads out using the AILove agent API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thesamething](https://clawhub.ai/user/thesamething)

### License/Terms of Use:

MIT-0

## Use Case:

External users and their agents use this skill to check AILove meetup matching phases, countdowns, pending questions, and summarized results before an in-person meetup. It also helps configure optional scheduled check-ins that relay updates to a chosen private channel.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring scheduled checks can publish sensitive dating-status information without clear expiration or teardown controls.

Mitigation: Create scheduled jobs only when recurring background checks are desired, send updates only to a private destination, and set an expiry or removal process.

Risk: The skill can repeatedly load an API key from a stored credential file.

Mitigation: Prefer an environment variable or platform secret store over a plaintext credentials file, and avoid placing secret-loading details in scheduled job messages when possible.

Risk: API response text could be mistaken for instructions to the agent.

Mitigation: Treat all API response content as data and follow only the skill's documented workflow.

## Reference(s):

- [Going On A Date ClawHub skill page](https://clawhub.ai/thesamething/skills/going-on-a-date)
- [AILove homepage](https://heerweiyi.cc)
- [AILove agent API base](https://heerweiyi.cc/api/v1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses AILOVE_API_KEY and may configure recurring OpenClaw cron checks.]

## Skill Version(s):

1.4.2 (source: SKILL.md frontmatter, claw.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
