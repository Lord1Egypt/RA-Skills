## Description:

Automate HR workflows including benefits enrollment, onboarding, and payroll integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ncreighton](https://clawhub.ai/user/ncreighton)

### License/Terms of Use:

MIT-0

## Use Case:

HR, People Operations, and payroll teams use this skill to draft and operate onboarding, benefits enrollment, payroll sync, notification, document automation, and audit-reporting workflows across HR systems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad HRIS, payroll, messaging, SendGrid, and DocuSign access without enough enforced scoping or per-action control.

Mitigation: Start with test or narrowly scoped credentials, endpoint limits, read-only defaults, human approval for writes, redacted logs, and a clear audit process outside the skill.

Risk: Generated HR workflow guidance could affect sensitive employee records, payroll data, benefits enrollment, or employee communications if applied without review.

Mitigation: Require HR or Finance review before syncing data, sending employee-facing messages, approving compensation changes, or running offboarding-related actions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ncreighton/skills/hrflow)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include workflow plans, status reports, validation summaries, environment-variable setup, and operational guidance for HR integrations.]

## Skill Version(s):

1.0.0 (source: server release and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
