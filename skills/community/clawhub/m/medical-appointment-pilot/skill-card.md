## Description:

A high-trust, HIPAA-aware appointment agent for medical and dental clinics that uses ThumbGate rules to reduce scheduling errors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[igorganapolsky](https://clawhub.ai/user/igorganapolsky)

### License/Terms of Use:

MIT-0

## Use Case:

External clinic staff and appointment agents use this skill to handle medical or dental appointment intake, verify scheduling constraints, screen insurance, and avoid unsafe bookings or logs. It is intended for clinic scheduling workflows that require human review of privacy, retention, audit, and system-access controls before patient-facing use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may handle sensitive patient appointment data without sufficiently specific privacy, retention, audit, and secure-storage controls.

Mitigation: Require explicit privacy disclosures, approved secure storage, retention rules, audit controls, and scoped access before using it in a real clinic workflow.

Risk: The operational instructions include an unrelated Gumroad upsell link that could be exposed in patient-facing use.

Mitigation: Remove the sales link and premium upsell text from runtime instructions before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/igorganapolsky/skills/medical-appointment-pilot)
- [Publisher profile](https://clawhub.ai/user/igorganapolsky)
- [thumbgate-rules.md](artifact/thumbgate-rules.md)

## Skill Output:

**Output Type(s):** [text, guidance, markdown, configuration]

**Output Format:** [Markdown instructions and rule lists for an appointment-booking agent]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes patient-intake, scheduling, insurance, emergency-handoff, logging, and ThumbGate prevention rules.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
