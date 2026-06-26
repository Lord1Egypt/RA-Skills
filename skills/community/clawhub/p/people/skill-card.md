## Description: <br>
Build a personal contact system with details, interactions, birthdays, and smart reminders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Individuals use this skill to maintain a local personal contacts notebook, capture relationship context, and surface reminders for meetings, birthdays, and follow-ups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Contact notes may contain private personal details about the user or people they know. <br>
Mitigation: Keep ~/contacts/ private, use encryption when appropriate, and avoid storing highly sensitive details unless necessary. <br>
Risk: Cloud sync or Git history can expose contact details and relationship history. <br>
Mitigation: Review sync and repository settings before storing contacts, and keep generated notes out of shared history when privacy matters. <br>
Risk: Casual mentions can lead to inaccurate or unwanted contact updates. <br>
Mitigation: Confirm new contacts and material updates before writing them to the contacts notebook. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/people) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Guidance] <br>
**Output Format:** [Markdown contact notes and concise text prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes or updates local contact notes under ~/contacts/ when the user approves.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
