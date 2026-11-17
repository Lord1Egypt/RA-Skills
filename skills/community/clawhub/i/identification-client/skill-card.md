## Description:

Identifies which client an analyzed accounting document belongs to and, for invoices, determines whether it represents a purchase or sale before the document is filed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[trendex](https://clawhub.ai/user/trendex)

### License/Terms of Use:

MIT-0

## Use Case:

Accounting staff and agents use this skill after document analysis to attach invoices, bank statements, or expense reports to the right client record. It also asks for human review when the client match or invoice direction is ambiguous.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist or alter local client registry data.

Mitigation: Keep backups of clients.json before use and review newly created or changed client records after each run.

Risk: Invoice or expense-report data can lead to client additions or identity attributes that need confirmation.

Mitigation: Treat new client records and SIREN, IBAN, or name updates from accounting documents as requiring human confirmation before downstream use.

Risk: Ambiguous documents may be assigned incorrectly if a human overrides the review flow too quickly.

Mitigation: When needs_review or question is present, ask the accountant the provided question and do not infer the client or purchase-sale direction.

## Reference(s):


## Skill Output:

**Output Type(s):** [JSON, Files, Guidance]

**Output Format:** [JSON object added to the analyzed dossier, with local client registry updates when a confident match or new client is found.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May modify clients.json and create per-client local records; ambiguous cases set needs_review and include a question for the accountant.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
