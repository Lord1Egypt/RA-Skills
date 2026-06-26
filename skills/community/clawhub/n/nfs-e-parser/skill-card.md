## Description: <br>
NFS-e field extractor for Brazilian agents that extracts CNPJ, prestador, tomador, service value, service code, and ISS fields from Sao Paulo NFS-e invoices for bookkeeping, reimbursement batching, and accountant handoff. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tlalvarez](https://clawhub.ai/user/tlalvarez) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to extract structured fields from Sao Paulo Brazilian NFS-e PDFs for bookkeeping, reimbursement batching, accountant handoff, CNPJ validation, and ISS reconciliation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow downloads parser code from GitHub at use time. <br>
Mitigation: Inspect the downloaded parser, pin the repository to a known commit, and run it in a virtual environment before processing invoices. <br>
Risk: Financial invoice fields can be misread or incomplete after OCR and parsing. <br>
Mitigation: Process only intended invoice PDFs and manually verify important accounting fields, CNPJ validation warnings, and missing-field warnings before ledger or reimbursement use. <br>
Risk: OCR text may contain sensitive invoice data. <br>
Mitigation: Keep processing local and delete temporary OCR text after use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tlalvarez/nfs-e-parser) <br>
- [NFS-e extraction methodology](https://auxiliar.ai/solve/nfs-e-extraction/) <br>
- [Parser source referenced by skill](https://github.com/Tlalvarez/Auxiliar-ai.git) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, Python code examples, and JSON output shape examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local workflow guidance for OCR, parser setup, field extraction, validation warnings, and invoice summary generation.] <br>

## Skill Version(s): <br>
v0.1.1 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
