## Description:

Open Humancy delegates real-world tasks to human workers through the OpenHumancy API, including worker search, task creation, chat, file upload, webhooks, transactions, and TON-based payments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openhumancy](https://clawhub.ai/user/openhumancy)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to hire human workers for physical actions, field verification, photography, deliveries, mystery shopping, data collection, and other tasks that require a person. It also supports managing worker applications, chats, task status, webhooks, transactions, refunds, and payment release.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create tasks, release payments, issue refunds, assign workers, and manage transactions involving real money.

Mitigation: Require explicit user confirmation before any payment, refund, task assignment, or task completion action.

Risk: The skill requires an OpenHumancy API key and may expose account balance, task, worker, or transaction information through API calls.

Mitigation: Use a narrowly scoped API key when available and avoid disclosing credentials, internal documents, access details, personal addresses, or other sensitive information.

Risk: The artifact recommends installing an MCP package using an unpinned @latest version.

Mitigation: Pin and verify the MCP package version before use, or avoid the MCP setup when package provenance cannot be validated.

Risk: Real-world worker tasks can involve privacy-sensitive locations, photos, deliveries, or field verification.

Mitigation: Review task descriptions and file uploads before submission to minimize personal data and confirm that the requested work is appropriate.

## Reference(s):

- [OpenHumancy API Base URL](https://app.openhumancy.com/api)
- [Open Humancy ClawHub Skill Page](https://clawhub.ai/openhumancy/skills/openhumancy)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Configuration instructions, Guidance, Text]

**Output Format:** [Markdown with API endpoint details, JSON examples, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include task lifecycle guidance, API request bodies, webhook configuration details, and MCP server setup instructions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
