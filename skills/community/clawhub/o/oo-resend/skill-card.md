## Description:

Use the Resend connector through the oo CLI to read email, send messages, retrieve attachments, and manage scheduled delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and email operators use this skill to inspect sent and received email, retrieve attachments, send messages, and manage scheduled delivery through a connected Resend account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI setup runs downloaded software that may install additional agent skills; the installer contents and exact installed release are unverified.

Mitigation: Review and approve CLI setup separately. If startup skill-directory writes are unwanted, set OO_SKILLS_SYNC_DISABLED=1 before running the CLI.

Risk: Sending email, changing scheduled delivery, and canceling scheduled email can affect communications or delivery state.

Mitigation: Confirm the exact payload and effect before send or update actions, and confirm the target before cancellation.

Risk: Using the connected account exposes email data and attachments to the connector provider.

Mitigation: Use only a trusted OOMOL connection and review access to email content and attachments.

## Reference(s):

- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [Resend](https://resend.com)
- [Resend API documentation](https://resend.com/docs/api-reference/introduction)

## Skill Output:

**Output Type(s):** [Guidance, API calls, Shell commands]

**Output Format:** [Markdown guidance with inline shell commands and JSON payload examples; connector results are returned as JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions that send, update, or cancel messages require user confirmation.]

## Skill Version(s):

1.0.7 (source: frontmatter; server release 1.0.7)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
