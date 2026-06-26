## Description: <br>
Submits a daily PENS MIS Kerja Praktek logbook entry after approval by gathering same-day work evidence, drafting concise Indonesian activity text, signing in with local secrets, saving the entry, and verifying the saved row. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mozaldy](https://clawhub.ai/user/mozaldy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Students or agents assisting a PENS Kerja Praktek participant use this skill to prepare, review, and submit a daily MIS logbook entry from same-day work evidence after explicit approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can submit real PENS MIS logbook entries using locally stored credentials. <br>
Mitigation: Keep the secrets file private and run the submission helper only after reviewing the date, hours, and generated Indonesian activity text. <br>
Risk: An unreviewed or unsupported activity summary could create an inaccurate logbook entry. <br>
Mitigation: Use the approval-first workflow and require same-day commit or other strong evidence before submission. <br>


## Reference(s): <br>
- [Workflow Reference](references/workflow.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/mozaldy/mis-logbook-submit) <br>
- [PENS MIS Portal](https://online.mis.pens.ac.id) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Concise chat guidance and, when executed, JSON status from the submission helper] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local MIS credentials and requires explicit user approval before submission.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
