## Description:

Autonomous session scribe that reads today's OpenClaw session logs, extracts decisions, preferences, framework sentences, and project updates, then writes a structured daily memory file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[billc8128](https://clawhub.ai/user/billc8128)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use Scribe to consolidate daily agent-session history into durable memory notes. It supports manual runs and scheduled cron-based memory extraction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Session messages are processed by OpenRouter and may contain confidential, personal, or credential-like content.

Mitigation: Use only in workspaces approved for external LLM processing, and add redaction or review controls before processing sensitive sessions.

Risk: Extracted preferences, decisions, and project updates are persisted into local memory and may be inaccurate or overly broad.

Mitigation: Review generated memory files before relying on them for future agent behavior, and keep retention scoped to the user's needs.

Risk: A scheduled job can repeatedly process new session logs without per-run approval.

Mitigation: Keep the cron job disabled until reviewed, scope the session directory and day range, and provide an easy way to disable the schedule.

## Reference(s):

- [Cron Setup for Scribe](references/cron-setup.md)
- [Signal Classification Guide](references/signal-guide.md)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Configuration]

**Output Format:** [Structured Markdown memory files and setup commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes memory/YYYY-MM-DD.md and can optionally append to MEMORY.md.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
