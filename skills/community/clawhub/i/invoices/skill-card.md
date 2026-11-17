## Description:

Files, checks, and audits received invoices using OCR and e-invoice XML, duplicate and fraud checks, VAT deduction support, and a searchable local archive.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

External users and business operators use this skill to file received invoices, validate supplier and tax details, track payments and disputes, prepare VAT or accountant-facing summaries, and search a local invoice archive.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill maintains a persistent local invoice archive and accounting memory under ~/Clawic/data/.

Mitigation: Install only when that local storage behavior is desired, and review generated archive entries and memory updates before relying on them.

Risk: VAT summaries, supplier changes, generated filings, and recurring due outputs can affect tax, payment, or accountant-facing decisions.

Mitigation: Review those outputs before use and route tax-sensitive or payment-sensitive decisions to the appropriate accountant, tax adviser, or approval process.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/invoices)
- [Clawic skill page](https://clawic.com/skills/invoices)
- [SKILL.md](artifact/SKILL.md)
- [Capture workflow](artifact/capture.md)
- [Extraction workflow](artifact/extraction.md)
- [Validation workflow](artifact/validation.md)
- [Filing workflow](artifact/filing.md)
- [VAT and deductibility workflow](artifact/vat.md)
- [Period close workflow](artifact/period-close.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance and local plain-text accounting records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local invoice archive entries, ledger rows, VAT summaries, filing guidance, dispute notes, supplier memory, and accountant handoff material.]

## Skill Version(s):

1.0.3 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
