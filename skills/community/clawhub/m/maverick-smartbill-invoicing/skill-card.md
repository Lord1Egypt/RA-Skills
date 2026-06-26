## Description: <br>
Issue SmartBill invoices through the SmartBill.ro API with local automation for payload validation, invoice creation, document series lookup, and invoice PDF download. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maverick](https://clawhub.ai/user/maverick) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and finance automation users can use this skill to validate SmartBill invoice payloads, create draft or final invoices after review, list available document series, and download invoice PDFs by series and number. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use real SmartBill credentials and issue real invoices. <br>
Mitigation: Keep the SmartBill token private, run dry-run validation first, and use --allow-final only after reviewing invoice details. <br>
Risk: Debug logging can expose invoice, client, request, or response details. <br>
Mitigation: Leave debug logging disabled unless those details are acceptable in logs. <br>
Risk: Incorrect invoice numbers can affect PDF retrieval because SmartBill returns zero-padded number strings. <br>
Mitigation: Store and reuse the invoice number exactly as returned by SmartBill without stripping leading zeros or converting it to an integer. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/maverick/maverick-smartbill-invoicing) <br>
- [SmartBill API Notes](references/smartbill-api.md) <br>
- [Invoice Example](references/invoice-example.json) <br>
- [SmartBill API base URL](https://ws.smartbill.ro/SBORO/api) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, JSON, files] <br>
**Output Format:** [Markdown guidance with shell commands, JSON CLI output, and PDF file output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and SmartBill environment variables MAVERICK_SMARTBILL_USERNAME, MAVERICK_SMARTBILL_TOKEN, and MAVERICK_SMARTBILL_COMPANY_VAT_CODE.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
