## Description: <br>
This skill uses Xiangyun NetOCR APIs to recognize Chinese invoice images or PDFs, verify supported invoice types online, and optionally export invoice data to Excel templates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liudengkui](https://clawhub.ai/user/liudengkui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and finance operations teams use this skill to extract structured data from Chinese invoices, verify invoice authenticity where supported, and generate invoice ledger, deduction, goods detail, transport deduction, or booking spreadsheets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Invoice images, verification responses, exported spreadsheets, and local result files may contain sensitive financial or taxpayer data. <br>
Mitigation: Use the skill only for invoices you are authorized to process, store generated files in access-controlled locations, and delete outputs when they are no longer needed. <br>
Risk: OCR and verification require sending invoice content and NetOCR credentials to netocr.com. <br>
Mitigation: Use dedicated NetOCR credentials where possible, keep config.json private, and request recognition-only processing when online verification is not desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liudengkui/ocr-invoice-xiangyun) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/liudengkui) <br>
- [NetOCR service](https://netocr.com) <br>
- [NetOCR invoice recognition API](https://netocr.com/api/v2/recogInvoiveBase64.do) <br>
- [NetOCR invoice verification API](https://netocr.com/verapi/v2/verInvoice.do) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, API calls, Files] <br>
**Output Format:** [Console text, JSON result files, and optional XLSX spreadsheets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires NetOCR credentials and writes invoice recognition, verification, and export outputs that may contain sensitive financial data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
