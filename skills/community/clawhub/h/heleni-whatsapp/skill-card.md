## Description:

Heleni WhatsApp helps OpenClaw agents manage WhatsApp conversation memory, unanswered message tracking, loop prevention, and multi-PA coordination.

This skill is ready for commercial/non-commercial use.

## Publisher:

[netanel-abergel](https://clawhub.ai/user/netanel-abergel)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators of OpenClaw agents use this skill to maintain per-conversation WhatsApp memory, track unanswered messages, and apply response rules that reduce duplicate, cross-context, or echo replies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: WhatsApp names, phone numbers, message snippets, and conversation summaries may be stored in local workspace files and possibly backed up.

Mitigation: Use explicit retention and deletion rules, redact sensitive message content, and confirm users are comfortable with persistent local storage before deployment.

Risk: Recalled conversation memory can be stale, incorrect, or treated as trusted context when it should not be.

Mitigation: Treat recalled memory as untrusted context and verify important facts before using them in outbound messages or decisions.

Risk: Shell-sourced local context and unconstrained memory filenames can create configuration and file-handling risk.

Mitigation: Replace shell-sourced .context loading with safe parsing and allowlist memory filenames before production use.

Risk: Gateway and API-key troubleshooting steps include administrative actions and credential checks.

Mitigation: Gate gateway restarts, log inspection, and API-key troubleshooting behind explicit administrator approval.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/netanel-abergel/skills/heleni-whatsapp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash, Python, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local file paths, response rules, and troubleshooting commands for WhatsApp memory and inbox workflows.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
