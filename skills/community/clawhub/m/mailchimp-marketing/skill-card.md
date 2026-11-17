## Description:

Manage Mailchimp audiences, campaigns, automations, e-commerce, and analytics. Create and send email campaigns, manage subscribers, configure automations, handle e-commerce stores, and track performance with detailed reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to operate Mailchimp marketing workflows from an agent, including audience management, campaign creation and sending, automations, e-commerce objects, and reporting. It is intended for connected Mailchimp accounts where the user can review and approve write actions before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawLink receives OAuth access for the connected Mailchimp account.

Mitigation: Install only if the user trusts ClawLink, review the Mailchimp account before authorization, and revoke the connection when it is no longer needed.

Risk: The integration exposes broad Mailchimp write actions, including campaign sends and changes to audiences, subscribers, templates, stores, webhooks, and automations.

Mitigation: Require explicit confirmation for write operations, including the target resource and intended effect, before calling the tool.

Risk: Destructive or high-impact operations can permanently delete or alter marketing assets and subscriber data.

Mitigation: Preview unfamiliar or high-impact tools first, prefer read/list/get operations to reduce ambiguity, and confirm destructive actions separately.

## Reference(s):

- [Mailchimp Marketing API Documentation](https://mailchimp.com/developer/marketing/api/)
- [Mailchimp Marketing API Guide](https://mailchimp.com/developer/marketing/docs/)
- [ClawLink OpenClaw Documentation](https://docs.claw-link.dev/openclaw)
- [ClawLink Verification](https://claw-link.dev/verify)
- [ClawHub Skill Page](https://clawhub.ai/hith3sh/skills/mailchimp-marketing)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON tool parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the connected ClawLink Mailchimp integration and returns tool results from the user's authorized Mailchimp account.]

## Skill Version(s):

1.0.6 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
