## Description: <br>
Draft patient-facing communications (appointment reminders, billing notices, follow-ups, recall messages) that avoid HIPAA violations, flag risky language, strip PHI from drafts, and follow the minimum necessary standard. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[josh4hire](https://clawhub.ai/user/josh4hire) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External healthcare practice staff and practice managers use this skill to draft and review patient-facing emails, texts, and letters for appointment reminders, billing notices, follow-ups, and recall messages while avoiding unnecessary PHI. It is a drafting and review aid, not a substitute for compliance, legal, or medical review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Drafts may still include unnecessary patient details or rely on an unsuitable communication channel. <br>
Mitigation: Provide only the minimum patient details, limit file access to selected drafts, and review all output before sending. <br>
Risk: Users may treat drafted language as final HIPAA policy, legal advice, or approved-channel guidance. <br>
Mitigation: Use the skill as a drafting and review aid, and rely on a compliance officer or healthcare attorney for HIPAA policy, consent, and approved-channel decisions. <br>
Risk: Patient information could be exposed if broad files or unnecessary identifiers are supplied for review. <br>
Mitigation: Restrict input files to the drafts being reviewed and remove unnecessary PHI or identifiers before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/josh4hire/hipaa-patient-comms) <br>
- [OpenClaw homepage](https://gaffneyits.com/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown drafts, templates, and compliance review notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Review all output before sending; the skill may write draft or corrected-message files when asked to save output.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
