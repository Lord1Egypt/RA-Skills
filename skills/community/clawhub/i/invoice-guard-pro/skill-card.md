## Description: <br>
InvoiceGuard Pro helps agents extract invoice fields, check for duplicate or tampered invoices, and generate invoice compliance reports; tax verification and Feishu export are described as Pro workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yk-global-01](https://clawhub.ai/user/yk-global-01) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Finance, operations, and reimbursement reviewers use this skill to inspect invoice uploads, identify duplicate reimbursement risk, and produce internal compliance reports. Pro workflows describe tax-platform verification and Feishu document or table export, but official verification depends on a real configured tax-verification integration. <br>

### Deployment Geography for Use: <br>
Global, with China-specific invoice formats and tax-verification references. <br>

## Known Risks and Mitigations: <br>
Risk: Invoice metadata may be sent to Feishu or a tax-verification service. <br>
Mitigation: Use only with user approval for external processing, limit shared invoice fields to the minimum needed, and confirm the destination workspace and access controls before export. <br>
Risk: Official tax verification is described in the skill but server security guidance says it should be treated as not implemented until a real integration is provided. <br>
Mitigation: Do not treat generated verification results as official proof unless the publisher provides and configures a working authorized tax-verification integration. <br>
Risk: Generated compliance reports may be mistaken for authoritative tax or audit determinations. <br>
Mitigation: Label reports as internal review aids and require human finance or compliance review before reimbursement, filing, or audit decisions. <br>


## Reference(s): <br>
- [InvoiceGuard Pro on ClawHub](https://clawhub.ai/yk-global-01/invoice-guard-pro) <br>
- [Invoice Types Reference](references/invoice-types.md) <br>
- [Tax Verification API Reference](references/tax-api.md) <br>
- [Compliance Report Template](references/compliance-report.md) <br>
- [Changelog](references/changelog.md) <br>
- [National VAT Invoice Verification Platform](https://inv-veri.chinatax.gov.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, structured text summaries, Python snippets, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include generated compliance-report content and prepared Feishu document or table payload guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
