## Description: <br>
Freelancer Toolkit helps agents track freelance time, manage clients and projects, analyze profitability, generate timesheets, and prepare invoice handoffs through conversation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nollio](https://clawhub.ai/user/nollio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Freelancers and solo operators use this skill to log time in natural language, maintain local client and project records, generate timesheets and billing reports, monitor project profitability, and prepare invoice data for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Client contact information, project details, time entries, rates, billed amounts, and payment status are stored locally under ~/.freelancer-toolkit/. <br>
Mitigation: Use disk encryption, restrict account access, and keep ~/.freelancer-toolkit/ permissions locked down before storing real client or billing records. <br>
Risk: Invoice handoff can pass client and billing data to InvoiceGen Pro or to services configured by the user's agent environment. <br>
Mitigation: Review invoice drafts before approval and confirm the security posture of InvoiceGen Pro, LLM providers, and any connected services. <br>
Risk: Generated CSV, Markdown, and JSON exports can contain sensitive billing records. <br>
Mitigation: Periodically audit and remove unneeded files from ~/.freelancer-toolkit/exports/ and include required records in a controlled backup process. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/nollio/normieclaw-freelancer-toolkit) <br>
- [Publisher Profile](https://clawhub.ai/user/nollio) <br>
- [README](artifact/README.md) <br>
- [Security Notes](artifact/SECURITY.md) <br>
- [Dashboard Specification](artifact/dashboard-kit/DASHBOARD-SPEC.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Conversational guidance with Markdown reports, CSV/JSON exports, Bash commands, and local configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local JSON records under ~/.freelancer-toolkit/ and can generate timesheet, client report, and invoice handoff artifacts.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
