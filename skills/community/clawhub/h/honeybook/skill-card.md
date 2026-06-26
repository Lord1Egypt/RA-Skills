## Description: <br>
Honeybook helps an agent work with HoneyBook client-portal sessions to review vendor contracts, invoices, payment methods, workspace files, and signing or payment links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chrischall](https://clawhub.ai/user/chrischall) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and their agents use this skill to inspect HoneyBook portal data across wedding vendors, identify unsigned contracts or overdue invoices, and obtain confirmed deep links for signing or payment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: HoneyBook magic links and cached sessions can grant access to sensitive portal data. <br>
Mitigation: Treat magic links as login secrets, use the skill only for HoneyBook-specific tasks, and delete or revoke cached sessions when access is no longer needed. <br>
Risk: Signing and payment links can lead to contractual or financial action. <br>
Mitigation: Require explicit user confirmation before returning signing or payment deep links, and have the user review the HoneyBook portal before completing the action. <br>
Risk: Contract, invoice, and payment-method details may expose private vendor or client information. <br>
Mitigation: Limit use to the intended vendor workspace and avoid sharing retrieved details outside the authorized requester. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chrischall/honeybook) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown or plain text summaries with HoneyBook portal links when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Signing and payment tools require explicit confirmation and return portal deep links.] <br>

## Skill Version(s): <br>
0.1.13 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
