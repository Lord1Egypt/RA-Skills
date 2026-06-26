## Description: <br>
Audits hospital surgical logs against billing to find revenue leakage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[srikanth-hn](https://clawhub.ai/user/srikanth-hn) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Healthcare billing and revenue-cycle staff can use this skill to compare hospital surgical notes or procedure summaries with billed items, identify possible missed charges, and draft an administrator-facing follow-up message. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated audit tables or follow-up messages may contain patient identifiers, procedure details, or financial information. <br>
Mitigation: Review and redact sensitive information before sharing any output. <br>
Risk: The skill suggests drafting a WhatsApp message for billing updates, which may not match an organization's approved communication practices. <br>
Mitigation: Use the organization's approved secure communication channel for administrator follow-up. <br>
Risk: Billing discrepancy findings may be incomplete or incorrect if the hospital log is incomplete or the notes are ambiguous. <br>
Mitigation: Have authorized billing staff validate findings against source records before updating bills. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown table and short message draft] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include estimated revenue leakage and administrator-facing billing update guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
