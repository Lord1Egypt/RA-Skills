## Description: <br>
Creates and manages invoices as JSON files on GitHub with sequential numbering, preview, and upload. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kleberbaum](https://clawhub.ai/user/kleberbaum) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, operators, and small-business users use this skill to create invoice or offer JSON records, preview calculated totals, list existing invoices, and upload confirmed records to a private GitHub repository. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can write sensitive invoice, customer, VAT, bank, pricing, and line-item data to a GitHub repository. <br>
Mitigation: Use a dedicated private invoice repository and a fine-grained GitHub token limited to that repository. <br>
Risk: Short confirmations such as OK or Ja may approve persistence of invoice data and downstream PDF or email automation. <br>
Mitigation: Review each preview carefully before confirming upload, especially when the target repository has automated invoice delivery. <br>
Risk: The skill requires command execution and network access through curl, python3, and base64. <br>
Mitigation: Deploy only in an environment where script execution and the configured GitHub token are acceptable for invoice handling. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kleberbaum/netsnek-invoice) <br>
- [README](artifact/README.md) <br>
- [Skill Instructions](artifact/SKILL.md) <br>
- [Manifest](artifact/claw.json) <br>
- [Basic Invoice Creation Example](artifact/examples/basic.md) <br>
- [Invoice Commands Example](artifact/examples/commands.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown conversation text with shell command execution and generated invoice JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Telegram-compatible preview text and stores invoice or offer records as JSON files.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter, manifest, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
