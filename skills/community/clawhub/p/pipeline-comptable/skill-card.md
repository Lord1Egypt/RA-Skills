## Description:

Pipeline comptable orchestrates incoming accounting documents from email or inbox through sorting, analysis, client identification, filing, and payment reconciliation, returning one consolidated report with accountant-facing questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[trendex](https://clawhub.ai/user/trendex)

### License/Terms of Use:

MIT-0

## Use Case:

Accounting teams and their agents use this skill to process batches of incoming invoices, bank statements, and expense receipts end to end while preserving accountant review for ambiguous client identification or filing decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes sensitive financial documents and can file or reconcile accounting records in ways that may affect business records.

Mitigation: Require explicit user review before filing or reconciling documents, and run the skill with access only to the intended inbox and client folders.

Risk: The workflow executes sibling local component scripts, so spoofed or unverified components could change processing outcomes.

Mitigation: Install only in a trusted, locked-down OpenClaw skills directory, pin or verify the sibling component scripts, and use a dedicated low-privilege account.

Risk: The included convenience runner uses fixed root-owned workspace paths and is not suitable as-is for routine execution.

Mitigation: Avoid using run_pipeline.py as written and do not run the workflow as root.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [JSON report plus readable text summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces consolidated per-document status, filing outcomes, payment-reconciliation summary, and questions that require accountant review.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
