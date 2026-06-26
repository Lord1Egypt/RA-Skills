## Description: <br>
한국형 견적서/세금계산서 자동 생성 (사업자등록번호, 부가세 자동 계산) <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mupengi-bot](https://clawhub.ai/user/mupengi-bot) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Employees, external service providers, and small-business operators use this skill to create Korean quote and tax invoice files, manage client and item data, and calculate supply amount, VAT, and totals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Crafted client names or path-like segments could affect where generated files are written. <br>
Mitigation: Use trusted client data only and avoid slashes or dot-dot path segments in client names. <br>
Risk: HTML or script-like text in invoice notes, item names, or client fields could affect the local browser when generated HTML is opened or converted. <br>
Mitigation: Do not enter HTML or script-like content in notes, item fields, or client fields. <br>
Risk: Local business, client, and invoice data may contain sensitive commercial or tax information. <br>
Mitigation: Keep the local data directory private and confirm generated tax invoice details before sharing files. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/mupengi-bot/korean-invoice) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; generated invoice outputs are HTML and PDF files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated files are written under an output directory using date, document type, and client name in the filename.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
