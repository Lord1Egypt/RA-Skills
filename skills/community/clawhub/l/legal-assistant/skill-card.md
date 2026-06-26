## Description: <br>
法务助手（Legal Assistant） assists legal and business teams with contract intake, key-term extraction, clause risk review, template comparison, revision suggestions, legal Q&A, approval-opinion drafts, and contract ledger updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[afeicn](https://clawhub.ai/user/afeicn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Legal, sales, procurement, and management teams use this skill to triage contract materials, extract key terms, identify clause risks, draft review notes, prepare approval opinions, and maintain contract records. It is intended to support review workflows while keeping final legal decisions and external commitments under human control. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Contract review outputs or legal Q&A could be mistaken for binding legal advice or final approval. <br>
Mitigation: Require human review before relying on legal advice, external replies, final approvals, seal or signature workflows, or high-risk clause decisions. <br>
Risk: Contract and legal-operation workflows can expose confidential business, customer, employee, financial, or contract data. <br>
Mitigation: Limit Feishu, Hermes Agent, knowledge-base, archive, and ledger permissions to authorized users and use test data or desensitized examples outside production. <br>
Risk: Archive or ledger updates may affect operational contract records. <br>
Mitigation: Restrict archive and ledger write permissions and require confirmation before binding record updates. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/afeicn/legal-assistant) <br>
- [README.md](README.md) <br>
- [Workflows](workflows.md) <br>
- [Runbook](runbook.md) <br>
- [Knowledge Base](knowledge/README.md) <br>
- [Templates](templates/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Configuration] <br>
**Output Format:** [Markdown and structured text templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes risk notes, suggested actions, human-confirmation items, and archive or ledger records when applicable.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and README.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
