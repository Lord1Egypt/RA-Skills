## Description:

Deploy and activate a Ko-fi HTTPS webhook receiver, verify live test deliveries, and operate payment tracking with summaries and exports. Use for Ko-fi webhook setup, troubleshooting, and received-payment reporting, not general account editing or publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stanestane](https://clawhub.ai/user/stanestane)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use this skill to configure and verify a Ko-fi payment webhook receiver, then review received-event summaries or exports. It covers payment notifications and local reporting, not historical-payment retrieval or general Ko-fi account management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment flags undeclared tool scope and deployment steps that may involve systemd and sudo.

Mitigation: Review the requested actions and generated deployment files against the target host before applying changes.

Risk: The security assessment is partial and notes one unresolved local path-like reference.

Mitigation: Resolve and inspect the referenced path before relying on the associated instructions.

Risk: Webhook records and private exports can contain supporter names, messages, email addresses, shipping details, and transaction links.

Mitigation: Keep databases and exports private, and use the redacted reports unless private fields are needed.

## Reference(s):

- [Webhook delivery, payload, and scope reference](references/webhooks.md)
- [Deployment and operations guide](references/deployment.md)
- [Ko-fi API and webhook help](https://help.ko-fi.com/hc/en-us/articles/360004162298-Does-Ko-fi-have-an-API-or-webhook)
- [Ko-fi webhook settings](https://ko-fi.com/manage/webhooks?src=sidemenu)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code, Payment reports]

**Output Format:** [Markdown guidance with shell commands, configuration files, and JSON reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports redact supporter details by default; private fields are included only when explicitly requested for export.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
