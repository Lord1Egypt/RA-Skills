## Description:

Supports enterprise invoice issuance, batch invoicing from ERP or ecommerce orders, invoice previews, authorization handling, and QR-code authorization status workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ningmengyun12366](https://clawhub.ai/user/ningmengyun12366)

### License/Terms of Use:

MIT-0

## Use Case:

Finance and operations users can use this skill to prepare, check, preview, authorize, and issue enterprise invoices from single requests, batches, or supporting business documents. It is intended for invoice workflows that require API-key setup, enterprise tax information, and user review before final issuance.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: API keys and sensitive invoice data may be exposed if they are pasted into chat or passed on command lines.

Mitigation: Use a managed secret store or local protected configuration, avoid sharing API keys in chat, and rotate keys if exposure is suspected.

Risk: The release depends on platform-specific remote invoice-assistant executables that are not included in the ZIP artifact.

Mitigation: Run only in an isolated environment unless the publisher provides signed binaries, pinned checksums, HTTPS-only endpoints, and a clear update process.

Risk: Incorrect invoice data can create financial or tax consequences if issued without review.

Mitigation: Use the skill's preflight checks and invoice preview flow, then require explicit user confirmation before final issuance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ningmengyun12366/skills/invoice-issue)
- [README](README.md)
- [Installation and update guide](invoice-issue-install.md)
- [Task preflight initialization check](references/common/preflight-initialization-check.md)
- [Invoice issuance interface](references/invoice-issue/issue.md)
- [Batch invoice information check](references/invoice-issue/batch-invoice-info-check.md)
- [Invoice authorization extension](references/invoice-issue/invoice-issue-auth-extend.md)
- [Enterprise profile lookup by tax number](references/common/query-enterprise-profile-by-uscc.md)
- [Code mappings](references/common/code-mappings.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command lines, configuration prompts, invoice preview Markdown, and JSON-backed task artifacts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires API-key and enterprise tax setup, preflight checks, preview review, and explicit user confirmation before final invoice issuance.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
