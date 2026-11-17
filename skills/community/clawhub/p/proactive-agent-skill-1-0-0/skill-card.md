## Description:

Transform AI agents from task-followers into proactive partners that anticipate needs and continuously improve. Includes WAL Protocol, Working Buffer, Autonomous Crons, and battle-tested patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flychicks](https://clawhub.ai/user/flychicks)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to add cross-session memory, working buffers, scheduled checks, and proactive automation patterns to AI agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cross-session memory and working buffers can retain secrets, private messages, regulated data, or full transcripts.

Mitigation: Configure memory capture and retention to exclude sensitive data, define removal processes, and review stored content before deployment.

Risk: Email, calendar, and other private-source checks can run without enough consent or scoping.

Mitigation: Enable private-source checks only after each account, access scope, schedule, and permitted task is explicitly approved.

Risk: Recurring automation can affect files or workflows beyond the intended boundary.

Mitigation: Define each cron task, writable path, retention period, and rollback or disable procedure before enabling automation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/flychicks/skills/proactive-agent-skill-1-0-0)
- [LobeHub Skill Page](https://lobehub.com/skills/openclaw-skills-proactive-agent)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may include file templates, cron examples, memory structures, and operational practices.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
