## Description: <br>
AI compute sales teams use this skill to analyze customer usage trends, support tickets, and contract status to identify churn risk, classify risk level, explain likely causes, and generate retention suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dashiming](https://clawhub.ai/user/dashiming) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Customer success, sales, and account teams use this skill to run churn health checks, inspect high-risk customers, and generate retention guidance before renewal or escalation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads and reports on commercially sensitive customer usage, support-ticket, and contract data stored locally. <br>
Mitigation: Install and run it only in workspaces where this local data handling is approved, and restrict filesystem and machine access for shared environments. <br>
Risk: Broad trigger phrases could invoke churn analysis when the user intended a narrower customer-success task. <br>
Mitigation: Use explicit commands such as --analyze, --list, --client, --reason, or --suggest when requesting analysis. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dashiming/pans-churn-predictor) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/dashiming) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Shell commands, Guidance] <br>
**Output Format:** [Terminal text reports with risk levels, reasons, and retention suggestions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local JSON customer, usage, support-ticket, and contract data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
