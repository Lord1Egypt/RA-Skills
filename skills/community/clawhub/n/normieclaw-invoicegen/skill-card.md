## Description:

InvoiceGen helps users create, track, and render branded PDF invoices from conversational requests with client management, line items, payment terms, and payment tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nollio](https://clawhub.ai/user/nollio)

### License/Terms of Use:

MIT

## Use Case:

Freelancers, small businesses, and their agents use InvoiceGen to draft invoices, manage client and business profile data, calculate totals, render local PDF invoices, and prepare client email copy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PDF rendering can process unescaped invoice data in a browser, which weakens the local and private handling claim.

Mitigation: Escape invoice fields before HTML insertion, block browser network access during rendering, avoid remote logo URLs, and review generated HTML before using the package with sensitive invoices.

Risk: Invoice records can include sensitive payment details, tax IDs, and client financial data.

Mitigation: Store only necessary details, prefer payment links or references over full account numbers, restrict invoice file permissions, and avoid committing invoice data.

Risk: The Playwright browser dependency can change rendering or security behavior if installed without version control.

Mitigation: Install Playwright in a virtual environment with pinned versions and review dependency updates before production use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nollio/skills/normieclaw-invoicegen)
- [README](artifact/README.md)
- [Security Guidance](artifact/SECURITY.md)
- [Agent Workflow](artifact/SKILL.md)
- [Dashboard Kit Specification](artifact/dashboard-kit/DASHBOARD-SPEC.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown invoice drafts and email copy, JSON invoice records, generated HTML, PDF files, and shell commands for local PDF rendering.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Asks for confirmation before PDF generation and writes invoice data under the local invoices directory.]

## Skill Version(s):

1.0.3 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
