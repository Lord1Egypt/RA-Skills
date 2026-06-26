## Description: <br>
Create and optionally send a new invoice to a client. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stanlee000](https://clawhub.ai/user/stanlee000) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees and finance operators use this skill to collect invoice details, find or create the client record, create an invoice in Norman, review the invoice summary, and optionally send it to the client. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A user may accidentally create or send a real invoice from a casual billing request. <br>
Mitigation: Require user review of invoice details before creation, and require explicit confirmation before sending the invoice email. <br>
Risk: Invoice details such as client, VAT rate, amount, due date, or notes may be incomplete or incorrect. <br>
Mitigation: Ask for missing details, resolve ambiguous client matches before using a client_id, and show a summary including the total amount before sending. <br>


## Reference(s): <br>
- [Norman Finance](https://norman.finance) <br>
- [ClawHub skill page](https://clawhub.ai/stanlee000/norman-create-invoice) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Text, API Calls] <br>
**Output Format:** [Markdown or plain text with MCP tool calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates invoice records and may send invoice email after user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
