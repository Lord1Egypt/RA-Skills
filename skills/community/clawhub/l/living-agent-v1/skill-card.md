## Description:

Living Agent configures an OpenClaw agent to run persistent autonomous reflection, exploration, memory updates, schedule management, and optional user reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linsongrong](https://clawhub.ai/user/linsongrong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users can use this skill to make an agent proactively reflect on recent conversations, manage a thinking queue, append memory notes, schedule periodic exploration, and report selected findings to the user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent autonomous operation can review conversations, write long-term memory files, and change scheduled jobs after installation.

Mitigation: Install only in a deliberate workspace, review every payload before enabling it, and keep cron jobs disabled until the user understands how to stop and delete them.

Risk: Conversation history and memory writes may retain sensitive or stale user context.

Mitigation: Set retention and cleanup rules for memory files, and periodically review generated notes before relying on or preserving them.

Risk: Configured messaging can send proactive reports to a Telegram or other user target.

Mitigation: Configure the messaging target explicitly or remove messaging behavior before enabling scheduled exploration.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/linsongrong/skills/living-agent-v1)
- [OpenClaw skills repository referenced by the artifact](https://github.com/openclaw/skills)
- [Heartbeat-Like-A-Man repository referenced by the artifact](https://github.com/loryoncloud/Heartbeat-Like-A-Man)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with shell commands and JSON configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May append memory files, update thinking queue and state JSON, manage cron jobs, search topics, and send configured user messages.]

## Skill Version(s):

1.1.1 (source: frontmatter, changelog, ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
