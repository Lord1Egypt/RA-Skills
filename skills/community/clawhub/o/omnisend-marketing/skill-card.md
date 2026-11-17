## Description:

Manage contacts, campaigns, automations, and ecommerce marketing workflows in Omnisend. Use this skill when users want to create or update contacts, run email campaigns, manage automations, and review marketing performance data via the Omnisend API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and marketing operators use this skill to manage Omnisend contacts, campaigns, automations, email/SMS workflows, and performance data through a connected Omnisend account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install and allowlist a third-party credential-bearing plugin with broad business-data write capabilities.

Mitigation: Install only if the user trusts ClawLink with the Omnisend account, review requested Omnisend OAuth scopes, and prefer a pinned or verified plugin version with clear rollback and token revocation steps.

Risk: Campaign sends, SMS sends, destructive actions, and automation triggers can affect customers or marketing operations.

Mitigation: Preview high-impact actions, confirm the target resource and intended effect with the user, and execute only after the preview matches the user's intent.

## Reference(s):

- [Omnisend API Documentation](https://api-docs.omnisend.com/)
- [Omnisend Integrations](https://www.omnisend.com/integrations/)
- [ClawLink OpenClaw Documentation](https://docs.claw-link.dev/openclaw)
- [ClawLink Verification](https://claw-link.dev/verify)
- [ClawHub Skill Page](https://clawhub.ai/hith3sh/skills/omnisend-marketing)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a ClawLink plugin connection to Omnisend; write, send, delete, and automation actions require explicit user confirmation.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
