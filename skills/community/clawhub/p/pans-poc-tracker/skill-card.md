## Description:

Pans Poc Tracker helps teams manage AI compute sales proof-of-concept lifecycles, including stage tracking, blocker records, follow-up reminders, and conversion reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dashiming](https://clawhub.ai/user/dashiming)

### License/Terms of Use:

MIT-0

## Use Case:

Sales, solution engineering, and technical account teams use this skill to track AI compute POCs from request through commercial conversion. It records GPU configuration, owners, blockers, customer feedback, status, reminders, and reports for active or closed POCs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: POC and customer details are stored in a local plaintext JSON file.

Mitigation: Use the skill only on protected machines, avoid regulated secrets or highly confidential customer data, and apply appropriate access controls to local files and backups.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text CLI output and local JSON records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores user-entered POC records in ~/.qclaw/skills/pans-poc-tracker/data/pocs.json.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
