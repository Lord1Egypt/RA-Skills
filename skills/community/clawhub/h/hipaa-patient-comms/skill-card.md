## Description:

Draft patient-facing communications such as appointment reminders, billing notices, follow-ups, and recall messages while flagging risky language, removing PHI from drafts, and applying the minimum necessary standard.

This skill is ready for commercial/non-commercial use.

## Publisher:

[josh4hire](https://clawhub.ai/user/josh4hire)

### License/Terms of Use:

MIT-0

## Use Case:

Front desk staff and practice managers at medical, dental, and therapy practices use this skill to draft or review patient emails, texts, and letters for routine reminders, billing notices, follow-ups, and recalls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may overstate what is safe for unsecured healthcare messages.

Mitigation: Treat output as drafting assistance only and review messages against organizational HIPAA policy before sending.

Risk: The skill should not be treated as a HIPAA compliance guarantee.

Mitigation: Use a compliance officer, healthcare attorney, or approved internal process for final compliance decisions.

Risk: The requested file-writing authority is unnecessary for many drafting and review workflows.

Mitigation: Avoid granting write_file unless there is a specific, scoped output need.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/josh4hire/skills/hipaa-patient-comms)
- [OpenClaw homepage](https://gaffneyits.com/openclaw)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with drafted messages, review findings, risk explanations, and suggested replacements]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include template variables for patient first name, appointment date, appointment time, practice name, phone number, portal link, and other message-specific inputs.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
