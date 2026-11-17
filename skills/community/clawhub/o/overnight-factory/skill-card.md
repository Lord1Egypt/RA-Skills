## Description:

Configures an OpenClaw agent to handle support ticket assignments from email or GitHub, dispatch implementation subagents, open pull requests, and notify a human reviewer.

This skill is ready for commercial/non-commercial use.

## Publisher:

[z-team-alpha](https://clawhub.ai/user/z-team-alpha)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and support operations teams use this skill to configure an autonomous ticket-to-PR workflow for support queues while preserving human review before merge.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow asks an unattended AI agent to use persistent credentials, read email, and change GitHub repositories with weak guardrails.

Mitigation: Run it only in a dedicated sandbox with a dedicated mailbox, allowlisted repositories, least-privilege short-lived GitHub credentials, and human approval before pushes, comments, or pull requests.

Risk: The artifact documents plaintext credential storage and permission-skip execution that would be unsafe for real support tickets without additional controls.

Mitigation: Do not use plaintext credential storage or permission-skip mode for production support queues unless compensating controls are in place.

## Reference(s):

- [Cron Job Prompt Template](references/cron-prompt.md)
- [Ticket Pipeline: Subagent Instructions](references/ticket-pipeline.md)
- [Lessons Learned in Production](references/lessons-learned.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown instructions with shell command blocks and prompt templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes credential placeholders, cron setup, dispatch workflow, validation checklist, and debugging guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
