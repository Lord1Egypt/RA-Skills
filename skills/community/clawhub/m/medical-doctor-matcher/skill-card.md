## Description:

Helps match users to appropriate hospitals and doctors from chief complaint, medical history, location, and visit preferences, with simulated registration and escort arrangements when requested.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunlinlin-aragon](https://clawhub.ai/user/sunlinlin-aragon)

### License/Terms of Use:

MIT License

## Use Case:

External users can use this skill for healthcare navigation: symptom-informed specialty routing, hospital and doctor matching, and simulated appointment or escort planning. It is informational guidance and does not replace diagnosis, treatment, prescriptions, emergency triage, or clinician judgment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat healthcare navigation output as medical diagnosis, treatment advice, prescription guidance, or emergency triage.

Mitigation: State that the output is informational navigation help only, recommend clinician evaluation, and direct serious or worsening symptoms to emergency services.

Risk: The skill uses simulated hospital, appointment, and escort data rather than live provider systems.

Mitigation: Label registration and escort outputs as simulated and require confirmation through real hospital, appointment, or service channels before acting.

Risk: Healthcare matching can involve sensitive health and location details.

Mitigation: Ask only for details needed for routing and matching, and avoid collecting unnecessary personal health or precise location information.

## Reference(s):

- [Workflow](references/workflow.md)
- [Symptom To Specialty](references/symptom_to_specialty.md)
- [Output Template](references/output_template.md)
- [Request Schema](schemas/request_schema.json)
- [Response Schema](schemas/response_schema.json)
- [ClawHub Skill Page](https://clawhub.ai/sunlinlin-aragon/skills/medical-doctor-matcher)

## Skill Output:

**Output Type(s):** [text, markdown, json, code, shell commands, guidance]

**Output Format:** [Markdown guidance and JSON-compatible recommendation records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Top 3 hospital and doctor recommendations may include risk level, specialty suggestions, match scores, simulated registration details, simulated escort details, and safety notes.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
