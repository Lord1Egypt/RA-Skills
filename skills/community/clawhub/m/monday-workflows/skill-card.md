## Description:

Manage Monday.com workspaces, boards, items, teams, and documents. Create projects, manage tasks and columns, handle team permissions, automate workflows with webhooks, and track portfolio-level analytics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and workspace administrators use this skill to inspect and manage Monday.com boards, workspaces, items, teams, documents, automations, webhooks, and portfolio data through an agent connected to their Monday.com account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install and globally enable an unpinned third-party plugin that handles OAuth-backed Monday.com business data.

Mitigation: Review the ClawLink plugin and publisher before installation, and only enable it in environments where that publisher and integration are trusted.

Risk: The connected integration can perform write and delete operations against Monday.com workspaces, boards, items, users, teams, webhooks, and related objects.

Mitigation: Use a least-privilege Monday.com account where possible and confirm every write or delete preview, including the target resource and intended effect, before execution.

Risk: Enabling the plugin persists in OpenClaw configuration until it is removed.

Mitigation: Periodically review enabled OpenClaw tools and remove the plugin when Monday.com access is no longer needed.

## Reference(s):

- [Monday.com API Documentation](https://developer.monday.com/api-reference/)
- [Monday.com GraphQL API](https://api.monday.com/v2)
- [ClawLink Docs](https://docs.claw-link.dev/openclaw)
- [ClawLink Verification](https://claw-link.dev/verify)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API calls]

**Output Format:** [Markdown with inline bash commands and JSON tool parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce read results, write previews, and confirmed Monday.com actions through the connected ClawLink integration.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
