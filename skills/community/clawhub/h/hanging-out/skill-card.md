## Description:

Casual social rhythm—light reminders for match pacing and pending replies. Low pressure; same official AILove agent API as loveq.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thesamething](https://clawhub.ai/user/thesamething)

### License/Terms of Use:

MIT-0

## Use Case:

External AILove and OpenClaw users use this skill to monitor matching status, relay pending questions for human answers, and configure low-pressure morning and evening reminders for match pacing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a stored AILOVE_API_KEY for API access and scheduled checks.

Mitigation: Prefer an environment variable or protected secret store, restrict any credential file to owner-only permissions, and send the key only to https://heerweiyi.cc/api/v1/agent/*.

Risk: Scheduled jobs can make unattended twice-daily API calls and post updates to a channel.

Mitigation: Create scheduled jobs only with user consent, document how to list and remove them, and verify delivery behavior after setup.

Risk: Remote API response text may influence what the agent reports.

Mitigation: Treat API response content as untrusted data to summarize, and follow only the fixed AILove workflow with human-provided answers submitted verbatim.

## Reference(s):

- [Hanging Out on ClawHub](https://clawhub.ai/thesamething/skills/hanging-out)
- [AILove homepage](https://heerweiyi.cc)
- [AILove Agent API base](https://heerweiyi.cc/api/v1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AILOVE_API_KEY and may configure two local scheduled checks.]

## Skill Version(s):

1.4.2 (source: frontmatter, claw.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
