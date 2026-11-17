## Description:

发票查验技能。按票面信息或上传文件查验发票真伪，返回完整票面信息。适用于验证发票真实性的场景。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zxt](https://clawhub.ai/user/zxt)

### License/Terms of Use:

MIT-0

## Use Case:

External users and business operators use this skill to verify invoice authenticity from invoice fields or uploaded invoice files, retrieve complete invoice details, and query prior verification records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Invoice files and invoice metadata may contain sensitive business, tax, or personal information and are sent to skill.quandianfapiao.com for verification.

Mitigation: Install and use the skill only after confirming that this external service is acceptable for the data being checked, and avoid submitting invoices that exceed the user's data-sharing policy.

Risk: The skill asks users to provide an API key in chat and includes instructions that may persist the key in plaintext shell startup files.

Mitigation: Use a temporary environment variable, a secret manager, or a restricted throwaway key instead of pasting production credentials into chat or storing them permanently; rotate any key that may have been exposed.

Risk: Invoice authenticity and record outputs depend on responses from the remote service and the user's account authorization.

Mitigation: Review non-200 status messages before acting on results, and confirm important tax or compliance decisions against authoritative records.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zxt/skills/invoice-verify)
- [中兴通简税Skill平台](https://skill.quandianfapiao.com/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Human-readable invoice verification results, record summaries, status messages, and command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include invoice metadata returned by the external service; file verification supports pdf, ofd, xml, jpg, and png files up to 10MB.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
