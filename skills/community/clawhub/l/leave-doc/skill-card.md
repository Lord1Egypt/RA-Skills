## Description:

Leave Doc generates Chinese leave-application templates for personal, sick, annual, marriage, maternity, paternity, bereavement, and compensatory leave, including multi-day workday calculations, emergency messages, and annual leave planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and workplace agents use this skill to draft Chinese leave requests, emergency leave messages, work handoff text, and annual leave plans for common leave types. It is most relevant for Chinese/PRC-oriented workplace leave practices.

### Deployment Geography for Use:

Global, with content oriented toward Chinese/PRC workplace leave practices.

## Known Risks and Mitigations:

Risk: An extra undocumented utility can retain entered text and command history as plaintext under the local leave-doc data directory.

Mitigation: Use the documented scripts/doc.sh path for generation, and avoid entering personal, medical, family, employment, or secret information into scripts/script.sh unless plaintext local retention is acceptable.

Risk: Generated multi-day leave dates exclude weekends but do not account for statutory holidays or adjusted workdays.

Mitigation: Review generated dates against the applicable workplace calendar before submitting a leave request.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ckchzh/skills/leave-doc)
- [Publisher profile](https://clawhub.ai/user/ckchzh)
- [Declared homepage](https://bytesagain.com)
- [Declared source URL](https://github.com/bytesagain/ai-skills)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Plain text and Markdown with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language templates; generated dates are based on the local runtime date; multi-day calculations exclude weekends but require manual adjustment for statutory holidays and adjusted workdays.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
