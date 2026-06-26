## Description: <br>
Invoice Guard helps agents extract invoice fields, check for duplicate or suspicious invoices, verify invoice status, and generate invoice compliance reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qiji0802](https://clawhub.ai/user/qiji0802) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Finance, operations, and audit teams use this skill through an agent to review uploaded Chinese invoices for duplicate reimbursement, suspicious status, and report-ready compliance summaries before reimbursement or audit workflows. <br>

### Deployment Geography for Use: <br>
Global, with China-specific invoice and tax-verification workflows. <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive invoice and company tax data, and its workflow can involve OCR uploads, tax-platform checks, Feishu document creation, and Bitable exports. <br>
Mitigation: Require explicit user approval before any upload, verification call, document creation, or export; use least-privilege Feishu credentials; and confirm document sharing settings before publishing or sharing results. <br>
Risk: Security review flagged that capability claims around image similarity and official verification may be more confident than the tested implementation supports. <br>
Mitigation: Treat duplicate and verification results as decision support, require human review against source invoices and official records, and avoid relying on image-similarity or official-verification claims until they are corrected and tested. <br>
Risk: Generated compliance reports may be used in reimbursement or audit decisions even when source invoices are incomplete, unclear, or externally unverified. <br>
Mitigation: Keep reports as internal review artifacts, preserve traceability to source invoices, and require finance or tax reviewers to confirm exceptions before reimbursement or filing decisions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/qiji0802/invoice-guard) <br>
- [README](README.md) <br>
- [Invoice Types Reference](references/invoice-types.md) <br>
- [Tax Verification Reference](references/tax-api.md) <br>
- [Compliance Report Template](references/compliance-report.md) <br>
- [Changelog](references/changelog.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, structured invoice records, Python snippets, shell commands, and Feishu-ready document or table payload guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May prepare Feishu document Markdown and Bitable records; tax verification and cloud exports require explicit user approval.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
