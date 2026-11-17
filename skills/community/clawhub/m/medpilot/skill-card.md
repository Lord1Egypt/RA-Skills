## Description:

Manage a single-patient medication and health-tracking workflow with MedPilot. Use when the user wants to ingest doctor orders, confirm active medications, record intakes or skipped doses, log blood pressure or glucose, generate follow-up summaries, or operate the MedPilot self-use edition through its CLI or local API. NOT for: multi-patient clinic workflows, diagnosis, treatment decisions, or replacing physician judgment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to manage one local patient profile by recording doctor orders, medication intake events, skipped or missed doses, blood pressure or glucose readings, and follow-up summaries. It is intended for health-management record keeping and should not be used for diagnosis, treatment decisions, medication changes, or multi-patient clinic workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence flags that examples can provide overly specific medical interpretation or follow-up advice beyond the stated non-diagnostic scope.

Mitigation: Use outputs only for local tracking and summaries, require clinician review for diagnosis or follow-up decisions, and avoid presenting medication changes as autonomous medical advice.

Risk: The skill handles sensitive health and medication information for a local patient profile.

Mitigation: Confirm privacy and storage handling before entering real health data, and keep use limited to the intended single-patient local deployment.

## Reference(s):

- [MedPilot Self-Use Quickstart](references/quickstart.md)
- [ClawHub Skill Page](https://clawhub.ai/harrylabsj/skills/medpilot)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with structured summaries and inline CLI or API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include medication records, intake logs, abnormal metric alerts, and follow-up summaries for a single local patient profile.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
