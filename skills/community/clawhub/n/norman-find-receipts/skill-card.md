## Description: <br>
Find and attach missing receipts for business transactions. Search Gmail, email, or other sources for invoices and receipts, then upload them to Norman. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stanlee000](https://clawhub.ai/user/stanlee000) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and finance operators use this skill to identify Norman Finance transactions missing receipts, locate matching invoices or receipts from email, vendor portals, cloud storage, or photo libraries, and attach them for verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent could upload or link an incorrect receipt to a transaction. <br>
Mitigation: Summarize each receipt-to-transaction match before upload, linking, or verification so the user can confirm it. <br>
Risk: Broad email or cloud access can expose unrelated personal or business documents. <br>
Mitigation: Prefer manually provided receipt files or grant only narrow access to trusted connected tools. <br>


## Reference(s): <br>
- [Norman Finance](https://norman.finance) <br>
- [ClawHub skill page](https://clawhub.ai/stanlee000/norman-find-receipts) <br>
- [Publisher profile](https://clawhub.ai/user/stanlee000) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, text, markdown] <br>
**Output Format:** [Markdown guidance with transaction, receipt, attachment, and verification summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the Norman Finance MCP integration and should summarize receipt-to-transaction matches before upload, linking, or verification.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
