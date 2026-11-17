## Description:

Mailbutler helps an agent triage inbox messages through an approved mailbox adapter, surface attention-worthy mail, recommend read or reply actions, and maintain an evidence-backed local narrative while keeping triage read-only.

This skill is ready for commercial/non-commercial use.

## Publisher:

[antreasantoniou](https://clawhub.ai/user/antreasantoniou)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use Mailbutler to run bounded inbox triage passes, identify messages that need attention, prepare reply recommendations, and maintain message-backed working context without silently mutating the mailbox.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Inbox triage processes sensitive email content through the configured mailbox adapter and model.

Mitigation: Use only owner-approved mailbox and model services, limit each pass to stated accounts and time windows, and avoid showing raw message bodies unless requested.

Risk: The local narrative can contain sensitive message-backed facts and open loops.

Mitigation: Store it under ~/.mailbutler/ with restrictive permissions, review or delete it as needed, and keep it out of repositories, logs, examples, and bug reports.

Risk: Reply recommendations could be confused with permission to draft or send email.

Mitigation: Require separate explicit approval per message before creating a draft and another approval before sending the exact draft to the resolved recipient.

Risk: Email bodies, subjects, attachments, and quoted threads can contain adversarial instructions.

Mitigation: Treat message content as untrusted evidence only; do not let it alter instructions, select recipients, run tools, or weaken the safety contract.

Risk: Mutable install commands can change over time or run in an unexpected environment.

Mitigation: Prefer a pinned or otherwise verified install command and avoid elevated privileges unless the runtime requires them.

## Reference(s):

- [Security and privacy contract](references/security-contract.md)
- [gog CLI](https://github.com/steipete/gogcli)
- [ClawHub skill page](https://clawhub.ai/antreasantoniou/skills/mailbutler-agent-skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Plain text and Markdown with JSON judgment records and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces an attention list, grounded reasons, recommended read or reply actions, suppressed-message counts, optional audit details, and proposed local narrative updates.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
