## Description:

Guides developers through Huifu payment, balance, delayed transaction, account, payout, settlement, checkout, and notification integrations and troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huifu](https://clawhub.ai/user/huifu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to select and implement Huifu payment and payout APIs, troubleshoot integrations, and handle SDK, request, notification, and transaction status details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports disabled TLS checks.

Mitigation: Keep certificate-chain and hostname verification enabled; review the selected SDK and deployment configuration before live requests.

Risk: Sensitive information handling may expose credentials in source code or logs.

Mitigation: Keep keys in server-side secret storage, disable SDK debug logging before initialization, redact logs, and keep credentials out of frontends and repositories.

Risk: Security analysis is incomplete for some referenced content.

Mitigation: Review unresolved or parser-limited references and confirm applicable API and SDK details against official Huifu documentation before production use.

## Reference(s):

- [Payment integration overview](references/shared-overview.md)
- [Server SDK matrix and transport guidance](references/shared-server-sdk-matrix.md)
- [Payment notification handling](references/shared-async-notify.md)
- [Credential use and storage boundaries](references/shared-credential-boundary.md)
- [Huifu official API documentation](https://paas.huifu.com/partners/api/doc/)
- [Huifu developer integration guide](https://paas.huifu.com/open/service/develop/#/)

## Skill Output:

**Output Type(s):** [Guidance, Code, Configuration, Shell commands, API request examples]

**Output Format:** [Markdown with explanations, tables, and inline code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include language-specific integration examples and configuration placeholders.]

## Skill Version(s):

1.6.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
