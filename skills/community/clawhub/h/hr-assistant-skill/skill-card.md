## Description:

HR Assistant helps HR teams and managers draft, review, and structure outputs for recruiting, resume screening, interviews, onboarding, labor contract review, training, and employee policy Q&A workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[afeicn](https://clawhub.ai/user/afeicn)

### License/Terms of Use:

MIT-0

## Use Case:

HR staff, recruiting leads, department managers, interviewers, and management use this skill to prepare structured HR drafts, risk notes, review materials, checklists, and archive records across common HR workflows. Human approval remains required for final hiring, compensation, contract, sensitive-data, and external-offer actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles candidate and employee data, including potentially sensitive HR, compensation, and contract information.

Mitigation: Restrict access to authorized users, mask sensitive details in outputs, and review permissions before deployment.

Risk: The skill creates archive and audit records that may retain sensitive HR material.

Mitigation: Define archive retention, deletion, and audit-log handling before production use.

Risk: Employee policy Q&A may provide unsupported answers if it does not use approved policy sources.

Mitigation: Require approved policy knowledge sources and citations for policy answers.

Risk: The skill may draft recommendations related to hiring, compensation, labor contracts, or external offers.

Mitigation: Require human approval for final hiring, compensation, contract, sensitive-data, and external-offer actions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/afeicn/skills/hr-assistant-skill)
- [HR Assistant README](artifact/README.md)
- [HR Assistant Workflows](artifact/workflows.md)
- [HR Skill Catalog](artifact/skills/hr_skills.yaml)
- [Knowledge Base Guidance](artifact/knowledge/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Structured Markdown and text templates with tables, checklists, risk notes, review notes, and archive records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are designed to include conclusions, key facts, risks or gaps, suggested actions, required human confirmations, and archive metadata.]

## Skill Version(s):

0.1.0 (source: server release evidence and artifact README/employee.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
