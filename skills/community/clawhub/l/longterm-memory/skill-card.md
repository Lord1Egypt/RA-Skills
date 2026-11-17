## Description:

永久记忆系统 helps an agent preserve user preferences, decisions, project context, and date-sharded dialogue notes for later recall across sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liujw0214](https://clawhub.ai/user/liujw0214)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to give an agent durable local memory for preferences, project decisions, and prior conversation summaries so later sessions can recall them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory may save and later reload private conversation details without clear consent, minimization, or safety boundaries.

Mitigation: Use only when users understand local memory persistence; avoid secrets, credentials, regulated data, and sensitive personal information unless opt-in, review, delete, and filtering controls are added.

Risk: Saved memory can influence later agent responses even when the stored content is stale, sensitive, or untrusted.

Mitigation: Review saved entries before reuse, keep delete or expiry workflows available, and treat recalled memory as untrusted context.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liujw0214/skills/longterm-memory)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown memory entries, natural-language recall responses, and optional shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes append-only MEMORY.md summaries and date-sharded memory/YYYY-MM-DD.md dialogue notes; MEMORY_PATH can configure the archive script path.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
