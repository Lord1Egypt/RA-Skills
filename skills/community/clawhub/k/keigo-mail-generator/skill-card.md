## Description: <br>
Keigo Mail Generator helps draft structured Japanese business emails with appropriate honorific language, optional internal template use, and locally managed signature details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[transmind](https://clawhub.ai/user/transmind) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and business users use this skill to create Japanese business email drafts for apologies, invitations, follow-ups, outreach, and other workplace communication while reusing saved signature details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores signature and contact details locally for future email drafts. <br>
Mitigation: Avoid entering contact details that should not be saved, and use the documented rm flow to remove stored fields when needed. <br>
Risk: Generated business emails may contain wording, factual, or compliance issues. <br>
Mitigation: Review and edit generated drafts before sending, especially when handling sensitive, legal, or customer-facing communication. <br>


## Reference(s): <br>
- [Keigo Mail Generator on ClawHub](https://clawhub.ai/transmind/keigo-mail-generator) <br>
- [Demo Video](https://www.youtube.com/watch?v=_UD1pcth0Dc) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Plain text or Markdown email draft, with an optional signature update notice before the draft.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 for local signature processing; generated emails should be reviewed before sending.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata; SKILL.md frontmatter reports 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
