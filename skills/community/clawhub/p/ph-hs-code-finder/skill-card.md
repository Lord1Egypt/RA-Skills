## Description:

Query Philippines customs HS codes for products exported to the Philippines using product text or image-derived product descriptions and the official Tariff Commission tariff book.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wumaohua233](https://clawhub.ai/user/wumaohua233)

### License/Terms of Use:

MIT-0

## Use Case:

External users, exporters, and trade operations teams use this skill to identify candidate Philippines HS codes for goods and collect the matching tariff-book description, source URL, and PDF page number. Developers and agents can also run the bundled scripts to suggest likely chapters, download chapter PDFs, and search them for product keywords.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: HS-code results are heuristic and may be incorrect for shipment-critical classification decisions.

Mitigation: Verify candidate codes against the official tariff book and consult a customs professional for important shipments.

Risk: The large-file download fallback can retrieve Google Drive PDFs with TLS certificate checking disabled.

Mitigation: Prefer verified official downloads or manually validate downloaded PDFs until the fallback is changed to enforce TLS verification.

Risk: Runtime dependencies such as Playwright and pdfplumber expand the local execution environment.

Mitigation: Install dependencies in an isolated environment and pin versions before operational use.

## Reference(s):

- [Philippines Tariff Commission Tariff Book 2022](https://www.tariffcommission.gov.ph/tariff-book-2022)
- [ClawHub skill page](https://clawhub.ai/wumaohua233/skills/ph-hs-code-finder)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown tables and command-line text, with optional JSON output from the PDF search script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results should include HS code, tariff-book product description, source URL, and PDF page number when available.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
