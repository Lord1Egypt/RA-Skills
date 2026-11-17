## Description:

NZ tax assistant for sole traders that processes receipt photos into IRD-ready GST reports, tracks sales income for GST Box 5, calculates IR3 annual income tax, provisional tax, asset depreciation, and exports to Xero CSV.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maxazure](https://clawhub.ai/user/maxazure)

### License/Terms of Use:

MIT-0

## Use Case:

External users, especially New Zealand sole traders, builders, and contractors, use this skill to capture receipts, track business income and assets, prepare GST and IR3 summaries, calculate provisional tax, and generate accountant- or filing-ready exports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive tax and business records are stored in local plaintext files.

Mitigation: Install only when local plaintext storage is acceptable, review file permissions, and maintain backups for the ~/.openclaw/data/kiwi-receipts/ directory.

Risk: Tax calculations or filing summaries may be incorrect or become stale as tax rules change.

Mitigation: Validate GST, IR3, provisional tax, and depreciation outputs with an accountant or authoritative IRD guidance before filing.

Risk: Generated XLSX and CSV exports have spreadsheet safety gaps until text sanitization is fixed.

Mitigation: Use caution when opening generated spreadsheet files and review exported cell values before sharing or importing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/maxazure/skills/kiwi-receipts)
- [NZ GST Compliance Reference for Receipt Processing](artifact/references/nz-gst-guide.md)
- [NZ Income Tax Reference -- Sole Traders](artifact/references/nz-income-tax-guide.md)
- [NZ IRD Depreciation Rates for Construction/Builder Assets](artifact/references/nz-depreciation-rates.md)
- [IRD GST](https://www.ird.govt.nz/gst)
- [IRD Taxable supply information for GST](https://www.ird.govt.nz/gst/tax-invoices-for-gst)
- [IRD File your GST return](https://www.ird.govt.nz/gst/filing-and-paying-gst-and-refunds/filing-gst/file-your-gst-return)
- [Income Tax Act 2007](https://www.legislation.govt.nz/act/public/2007/0097/latest/DLM1512301.html)
- [IRD Tax rates for individuals](https://www.ird.govt.nz/income-tax/income-tax-for-individuals/tax-codes-and-tax-rates-for-individuals/tax-rates-for-individuals)
- [IRD Individual income tax return IR3](https://www.ird.govt.nz/income-tax/income-tax-for-individuals/what-happens-at-the-end-of-the-tax-year/individual-income-tax-return-ir3)
- [IRD Provisional tax standard option](https://www.ird.govt.nz/income-tax/provisional-tax/provisional-tax-options/standard-option)
- [IRD Depreciation rate finder](https://www.ird.govt.nz/income-tax/income-tax-for-businesses-and-organisations/types-of-business-expenses/depreciation/depreciation-rate-finder)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Conversational Markdown plus local JSON records, XLSX reports, and Xero-compatible CSV exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The XLSX/CSV report generator requires openpyxl and uses user-maintained local data files under ~/.openclaw/data/kiwi-receipts/.]

## Skill Version(s):

2.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
