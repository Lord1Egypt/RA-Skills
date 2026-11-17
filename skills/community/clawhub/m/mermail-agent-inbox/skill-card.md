## Description:

Provision or reuse a service-scoped Mermail mailbox, then safely find and inspect an expected verification, sign-in, onboarding, receipt, or order-status email for an active third-party workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mermail](https://clawhub.ai/user/mermail)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill when a workflow needs a controlled mailbox identity and one expected verification, sign-in, onboarding, receipt, or order-status email. It supports mailbox reuse or provisioning, bounded polling, safe message validation, and protected extraction of task-required OTPs or HTTPS links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The packaged MCP connection uses the broader Mermail endpoint while the skill's security design recommends a dedicated agent-inbox profile or host-side allowlist.

Mitigation: Configure the dedicated agent-inbox MCP profile when available, or enforce a host-side allowlist limited to mailbox discovery, bounded polling, message reads, and context reads before using sensitive verification mail.

Risk: Inbound email, OTPs, magic links, and attachments may contain untrusted or sensitive content.

Mitigation: Use metadata-only candidate discovery, require exact expected-message validation, inspect only scan-clean bounded content, keep extracted secrets in protected task-local context, and require fresh confirmation before using a code or link.

## Reference(s):

- [Mermail Agent Inbox documentation](https://docs.mermail.app/ai/skills)
- [ClawHub skill page](https://clawhub.ai/mermail/skills/mermail-agent-inbox)
- [Agent-inbox tool map](references/tools.md)
- [Agent-inbox security boundary](references/security.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, API calls, shell commands]

**Output Format:** [Markdown guidance with structured status summaries and bounded command or tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces mailbox-resolution summaries, polling states, protected OTP or link extraction, and handoff guidance; requires MERMAIL_API_KEY for Mermail access.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
