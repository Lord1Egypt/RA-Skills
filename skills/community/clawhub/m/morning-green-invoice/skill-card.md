## Description: <br>
Use to authenticate with Morning (GreenInvoice) and create or manage clients, items, and accounting documents such as invoices, receipts, quotes, orders, and credits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[k0renn](https://clawhub.ai/user/k0renn) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to let an agent work with Morning (GreenInvoice) accounts, including authentication, client and item management, and creation of accounting documents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create or update real accounting records using API credentials without an explicit final confirmation requirement. <br>
Mitigation: Use a least-privilege API key where available, avoid exposing secrets in untrusted sessions, and manually review client, item, and document payloads before creation or update. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Guidance] <br>
**Output Format:** [JSON tool payloads and concise text summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return created resource IDs and document URLs when the connected Morning tool provides them.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
