## Description:

Create a clinician-ready timeline and visit brief for possible side effects after a medication or supplement start, stop, or change.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

Patients, caregivers, and family members use this skill to organize symptoms, context factors, timelines, clinician or pharmacist questions, and a visit brief after a medication or supplement change.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may mistake the generated log or visit brief for medical advice.

Mitigation: The skill frames outputs as an organizer for discussion with a doctor or pharmacist and avoids diagnosis, causality claims, dosing advice, or medication changes.

Risk: Users may include unnecessary sensitive identifiers while describing medication concerns.

Mitigation: The skill tells users not to provide prescription numbers, insurance IDs, national IDs, payment details, credentials, or private medical records.

Risk: Urgent symptoms could be delayed if treated as routine visit-prep information.

Mitigation: The skill includes emergency escalation language for severe or rapidly worsening symptoms and directs users to seek emergency care or local emergency services.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/harrylabsj/skills/medication-side-effect-visit-log)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown tables with a plain-text visit brief]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompt-only organizer; no code execution, network access, API calls, or credentials required.]

## Skill Version(s):

1.0.1 (source: server release metadata and skill.json; SKILL.md frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
