## Description:

Nightly Build helps an agent scan recent sessions for friction points, choose one reversible improvement, implement it, and send a morning briefing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joeytbuilds](https://clawhub.ai/user/joeytbuilds)

### License/Terms of Use:

MIT-0

## Use Case:

External ClawHub users use this skill to configure an agent that performs bounded overnight workspace maintenance, prepares low-risk improvements, and reports what changed in the morning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run recurring overnight automation while the user is absent.

Mitigation: Enable it only after setting explicit scan boundaries and adding a simple pause or removal path for the cron job.

Risk: The skill may read broad conversation, memory, and workspace context.

Mitigation: Limit the session and memory sources it may inspect before deployment.

Risk: The skill can prepare or trigger actions involving scripts, aliases, files, and messaging.

Mitigation: Keep outputs local by default, require review before external messages, and prohibit unattended script or alias creation unless separately approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/joeytbuilds/skills/nightly-self-improvement)
- [Publisher profile](https://clawhub.ai/user/joeytbuilds)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a local process document, cron setup guidance, and a morning briefing format.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
