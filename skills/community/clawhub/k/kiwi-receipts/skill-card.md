## Description: <br>
NZ tax assistant for sole traders. Process receipt photos into IRD-ready GST reports, track sales income for GST Box 5, calculate IR3 annual income tax, provisional tax, asset depreciation, and export to Xero CSV. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maxazure](https://clawhub.ai/user/maxazure) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, especially New Zealand sole traders, builders, and contractors, use this skill to capture receipt and income records, prepare GST and IR3 summaries, calculate provisional tax and depreciation, and export files for filing or accounting review. <br>

### Deployment Geography for Use: <br>
New Zealand <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive financial and tax records stored on the user's device. <br>
Mitigation: Install only on a trusted device and protect ~/.openclaw/data/kiwi-receipts with restricted OS account access, disk encryption, careful backups, and deletion of records no longer needed. <br>
Risk: Generated tax summaries, XLSX reports, and Xero CSV files may contain OCR, categorization, or calculation errors. <br>
Mitigation: Review generated files before filing, importing to Xero, or sharing, and verify figures with IRD guidance or a qualified accountant. <br>


## Reference(s): <br>
- [Kiwi Receipts ClawHub listing](https://clawhub.ai/maxazure/kiwi-receipts) <br>
- [NZ GST Compliance Reference for Receipt Processing](references/nz-gst-guide.md) <br>
- [NZ Income Tax Reference -- Sole Traders](references/nz-income-tax-guide.md) <br>
- [NZ IRD Depreciation Rates for Construction/Builder Assets](references/nz-depreciation-rates.md) <br>
- [IRD GST guidance](https://www.ird.govt.nz/gst) <br>
- [IRD individual tax rates](https://www.ird.govt.nz/income-tax/income-tax-for-individuals/tax-codes-and-tax-rates-for-individuals/tax-rates-for-individuals) <br>
- [IRD provisional tax standard option](https://www.ird.govt.nz/income-tax/provisional-tax/provisional-tax-options/standard-option) <br>
- [IRD depreciation rate finder](https://www.ird.govt.nz/income-tax/income-tax-for-businesses-and-organisations/types-of-business-expenses/depreciation/claiming-depreciation/work-out-your-assets-rate-and-depreciation-value) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance] <br>
**Output Format:** [Chat-native Markdown plus JSON records, shell commands, XLSX reports, and Xero CSV exports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores records locally under ~/.openclaw/data/kiwi-receipts and requires openpyxl for XLSX report generation.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
