## Description: <br>
Horus Pro -- Full Meeting Intelligence Suite. Summary, decisions, action tracker, stakeholder-specific briefs, next meeting agenda, risk flags, and follow-up emails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[occupythemilkyway](https://clawhub.ai/user/occupythemilkyway) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external collaborators, and operations teams use this skill to turn raw meeting notes or transcripts into a complete meeting intelligence package with a brief, decisions, action tracker, stakeholder briefs, next agenda, risk flags, and follow-up email. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Confidential meeting notes may appear in local terminal output during processing. <br>
Mitigation: Use the skill only in private sessions, avoid shared terminals and CI logs, and remove or suppress raw MEETING_NOTES printing for confidential meetings. <br>
Risk: Generated meeting documents may contain sensitive decisions, action items, or stakeholder-specific information. <br>
Mitigation: Set OUTPUT_DIR to a private location with appropriate access controls and review generated files before sharing. <br>
Risk: Meeting summaries, risks, and action items may be incomplete or misleading if the transcript is unclear or incomplete. <br>
Mitigation: Have a meeting owner review the generated brief, tracker, agenda, and emails before using them as records or sending them externally. <br>


## Reference(s): <br>
- [Horus Pro ClawHub listing](https://clawhub.ai/occupythemilkyway/horus-pro) <br>
- [occupythemilkyway publisher profile](https://clawhub.ai/user/occupythemilkyway) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, shell commands, configuration] <br>
**Output Format:** [Markdown documents saved to an output directory, with setup and validation commands shown in shell and Python blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces five meeting documents: meeting brief, action tracker, follow-up email, next meeting agenda, and stakeholder briefs.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
