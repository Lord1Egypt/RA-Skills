## Description:

Builds a structured US interview question set and scoring rubric for one role, with unlawful questions flagged for removal. Use when the user asks for interview question kit, behavioral interview questions, illegal interview questions. For US hiring managers, recruiters and interview panels hiring hourly and salaried staff.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rapidworker1](https://clawhub.ai/user/rapidworker1)

### License/Terms of Use:

MIT-0

## Use Case:

US hiring managers, recruiters, and interview panels use this skill to prepare structured, role-specific interview questions, follow-up probes, and a scoring rubric. It also provides a basic lint report to flag checklist issues before the kit is used.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: The basic lint checks cannot guarantee that interview questions meet legal requirements.

Mitigation: Have employment counsel review the questions before use.

Risk: Real candidate information could be exposed when preparing or sharing a kit.

Mitigation: Use fictional examples and keep candidate names, resumes, contact details, and answers out of the kit.

Risk: The optional Windows application is unnecessary for the documented workflow and has a separate trust requirement.

Mitigation: Use the local documented workflow; do not run the optional application unless it has been independently reviewed and is needed.

## Reference(s):

- [Interview question rules](references/interview-question-rules.md)
- [Interview kit template](templates/interview-kit.yaml)
- [ClawHub release](https://clawhub.ai/rapidworker1/skills/interview-question-kit)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Markdown interview kit and lint report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Role-specific questions, follow-up probes, scoring rubric, and review guardrails.]

## Skill Version(s):

1.0.6 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
