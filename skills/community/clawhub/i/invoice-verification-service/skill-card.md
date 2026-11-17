## Description:

Use the local invoice service script to initialize app keys, query quota and packages, verify invoice text or images, batch-verify local folders, and create or query recharge orders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fenghaozhe-git](https://clawhub.ai/user/fenghaozhe-git)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and external users can use this skill to run a Node.js helper for invoice quota checks, package lookup, invoice verification, batch image verification, and recharge order management against a configured invoice API backend.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Invoice text, invoice images, extracted invoice fields, API keys, and account or order data may be sent to the configured backend.

Mitigation: Install only when the backend is trusted and configure an HTTPS endpoint before processing sensitive invoices.

Risk: Implicit or ambiguous invocation could submit invoice data or create backend requests unexpectedly.

Mitigation: Use explicit user confirmation for verification and payment-related actions, especially before creating recharge orders.

Risk: Batch verification uploads images from local folders and writes JSON result files beside the source directory.

Mitigation: Review the target folder before upload and handle generated result files as sensitive invoice records.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/fenghaozhe-git/skills/invoice-verification-service)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, API Calls, JSON, Files, Guidance]

**Output Format:** [JSON responses and Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Batch directory verification can write per-image JSON files and a summary.json file next to the source directory.]

## Skill Version(s):

0.4.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
