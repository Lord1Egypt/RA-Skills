## Description: <br>
Generates Chinese leave application templates, emergency leave messages, multi-day workday calculations, and annual leave planning guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckchzh](https://clawhub.ai/user/ckchzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and agents use this skill to draft leave requests, emergency leave notices, and annual leave plans for workplace approval workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Leave requests may contain sensitive personal, medical, or family details, and the auxiliary helper script can store local logs if invoked. <br>
Mitigation: Avoid entering sensitive details unless local storage is acceptable, and review or clear the leave-doc data directory when needed. <br>
Risk: Generated leave guidance and dates may not reflect local law, company policy, public holidays, or adjusted workdays. <br>
Mitigation: Review generated templates and date calculations against the employer's leave policy and applicable regional requirements before submitting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ckchzh/leave-doc) <br>
- [Usage tips](artifact/tips.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown and terminal text containing leave application templates, message drafts, date calculations, and planning guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated templates may include placeholders for names, dates, approvers, handoff contacts, and leave-specific details.] <br>

## Skill Version(s): <br>
2.0.0 (source: evidence release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
