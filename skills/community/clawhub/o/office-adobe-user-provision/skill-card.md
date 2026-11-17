## Description:

Automates Microsoft 365 (21Vianet) and Adobe Creative Cloud user provisioning and administration through shared CLI and HTTP API workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eggyrooch-blip](https://clawhub.ai/user/eggyrooch-blip)

### License/Terms of Use:

MIT-0

## Use Case:

IT administrators and operations agents use this skill to create, license, inspect, reset, delete, and batch-manage Microsoft 365 (21Vianet) and Adobe Creative Cloud users.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can manage real Microsoft 365 and Adobe accounts, including create, license, reset, delete, and self-test operations.

Mitigation: Install only in a tightly controlled administrator environment and require explicit operator confirmation before reset, delete, or self-test actions.

Risk: The HTTP API exposes account management operations and requires protection before use.

Mitigation: Add authentication before enabling the HTTP API and bind it to localhost unless it is deliberately protected for network access.

Risk: Credential and password handling may expose tenant secrets or initial passwords through environment files or email notification flows.

Mitigation: Remove any bundled or production .env secrets before installation, rotate exposed credentials, and disable plaintext password email or BCC delivery.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/eggyrooch-blip/skills/office-adobe-user-provision)
- [Microsoft 365 China portal](https://portal.partner.microsoftonline.cn)
- [Adobe Creative Cloud](https://creativecloud.adobe.com)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, API calls]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON command/API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May perform account, license, password reset, delete, email notification, and self-test operations against configured Microsoft 365 and Adobe tenants.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
