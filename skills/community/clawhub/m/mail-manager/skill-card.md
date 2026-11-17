## Description:

Manages an agent mailbox by checking mail status and content, maintaining contacts, sending new-mail reminders, and guiding send, reply, forward, and delete workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hechunxian](https://clawhub.ai/user/hechunxian)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to let an agent monitor mailbox state, summarize incoming messages, maintain contacts, and perform mail actions with the configured agent-mail tooling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Emails from user aliases can trigger agent actions and automatic replies without normal confirmation.

Mitigation: Require in-session confirmation before email-originated actions with side effects or automatic replies, or remove the alias-based full-authorization rule before deployment.

Risk: The skill manages mailbox data and local mail logs.

Mitigation: Install only when the agent is intended to manage this mailbox, and review local log retention and access controls before use.

Risk: Email attachments may be untrusted.

Mitigation: Keep attachment handling read-only unless the user explicitly authorizes processing, and do not execute or unpack attachments by default.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hechunxian/skills/mail-manager)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown instructions with tool-name and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes mailbox action workflows, confirmation rules, contact and mail-state file guidance, and attachment-handling guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
