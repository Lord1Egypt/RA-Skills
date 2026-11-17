## Description:

Manage Google Workspace users, groups, domains, devices, and admin directory data through Google Admin SDK API workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

Workspace administrators and IT operators use this skill to inspect and manage Google Workspace directory resources, including users, groups, organization units, domains, and devices. The skill supports read workflows and confirmed write workflows through a connected Google Workspace admin account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A third-party plugin and hosted service can use administrator OAuth access for high-impact Google Workspace directory changes.

Mitigation: Review before production installation, use a dedicated least-privilege admin account, verify the ClawLink plugin and service provenance, and confirm requested OAuth scopes during connection.

Risk: Administrative write or destructive actions could affect users, groups, organization units, or devices.

Mitigation: Preview and explicitly confirm the target resource and intended effect before create, update, delete, group-membership, 2-step-verification, or organization-unit move operations.

Risk: Compromised or overbroad access may be difficult to notice without monitoring.

Mitigation: Monitor Google Workspace audit logs after deployment and revoke the connected OAuth token if activity looks wrong.

Risk: Sensitive credentials or passwords could be exposed through chat or command-line examples.

Mitigation: Avoid putting real passwords directly into chat or command-line examples; prefer secure account provisioning and rotation processes.

## Reference(s):

- [Google Admin SDK Documentation](https://developers.google.com/admin-sdk)
- [Directory API Reference](https://developers.google.com/admin-sdk/directory/reference/rest)
- [ClawLink Docs](https://docs.claw-link.dev/openclaw)
- [ClawLink Verification](https://claw-link.dev/verify)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance]

**Output Format:** [Markdown with inline shell commands and JSON tool parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes confirmation-oriented guidance for write and destructive Google Workspace admin operations.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
