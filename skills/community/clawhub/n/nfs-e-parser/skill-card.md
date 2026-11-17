## Description:

NFS-e Parser extracts structured fields such as CNPJ, prestador, tomador, service value, service code, and ISS from Brazilian São Paulo NFS-e PDFs for bookkeeping, reimbursement batching, and accountant handoff.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tlalvarez](https://clawhub.ai/user/tlalvarez)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agents, and bookkeeping teams use this skill to turn OCR text from São Paulo NFS-e PDFs into structured invoice fields for accounting workflows, reimbursement batches, and accountant handoff. It is intended for Brazilian service invoices and includes validation cues such as CNPJ checks and missing-field warnings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to fetch and run mutable remote parser code without integrity checks.

Mitigation: Review the parser before installation, pin it to a specific commit, and verify a checksum before copying or executing it.

Risk: NFS-e PDFs and extracted OCR text can contain sensitive financial and business data.

Mitigation: Run OCR and parsing in a limited local workspace without unrelated credentials or files; use cloud OCR only with explicit approval and privacy/compliance review.

Risk: The documented validation is scoped to São Paulo NFS-e PDFs and has limited coverage for non-zero retention values.

Mitigation: Review missing-field warnings, validate CNPJ check digits, and manually confirm accounting-critical fields before writing results to a ledger.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tlalvarez/skills/nfs-e-parser)
- [NFS-e extraction methodology](https://auxiliar.ai/solve/nfs-e-extraction/)
- [Referenced parser repository](https://github.com/Tlalvarez/Auxiliar-ai.git)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration instructions, JSON]

**Output Format:** [Markdown guidance with bash and Python snippets; parser output is structured JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The workflow uses local OCR/parsing steps and may emit missing-field or invalid-CNPJ warnings for review before ledger entry.]

## Skill Version(s):

v0.1.1 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
