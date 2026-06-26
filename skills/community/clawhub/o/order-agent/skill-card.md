## Description: <br>
order-agent 智能订单处理 helps users query goods and create WMS shipment orders from single requests or Excel/CSV order files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NeroD9408](https://clawhub.ai/user/NeroD9408) <br>

### License/Terms of Use: <br>
MIT License <br>


## Use Case: <br>
Operations users and agents use this skill to look up book inventory by title or ISBN, collect recipient and order details, and create single or batch WMS shipment orders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create real WMS shipment orders. <br>
Mitigation: Verify the API destination and credentials, then require a final human confirmation before every single or batch submission. <br>
Risk: Order submissions may send recipient names, phone numbers, addresses, and spreadsheet data to external APIs. <br>
Mitigation: Use only approved endpoints and avoid uploading spreadsheets with personal data unless the backend privacy and retention practices are acceptable. <br>
Risk: Broad purchase or order wording may lead the agent toward order creation. <br>
Mitigation: Separate lookup and selection from submission, and confirm item, quantity, recipient, address, and endpoint before running create commands. <br>


## Reference(s): <br>
- [WMS API documentation](references/wms_api.md) <br>
- [ClawHub skill page](https://clawhub.ai/NeroD9408/order-agent) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, guidance] <br>
**Output Format:** [Markdown/text with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call external WMS APIs and produce order numbers, detail URLs, and batch result summaries.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
