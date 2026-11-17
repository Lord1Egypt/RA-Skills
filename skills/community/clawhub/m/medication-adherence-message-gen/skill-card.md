## Description:

Generates personalized medication adherence reminder messages using behavioral psychology principles, with command-line and Python API controls for medication, patient name, tone, principle, language, and output format.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users, care teams, and developers can use this skill to draft SMS or push-notification medication reminder copy with configurable reminder details, tone, behavioral principle, language, and output format. Patient-facing use should require human review because the security evidence flags unsupported medical claims and persuasive medication-reminder content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package labels itself as academic writing while generating persuasive patient-facing medication reminders.

Mitigation: Use it only after the publisher narrows the description and activation guidance to medication reminder drafting.

Risk: Generated reminders may contain unsupported statistics, categorical dosing claims, or medication guidance.

Mitigation: Require clinician or qualified human review before any patient-facing use and remove unsupported claims from templates.

Risk: The package declares unnecessary unpinned dependencies.

Mitigation: Install in an isolated environment and avoid unnecessary unpinned dependencies.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aipoch-ai/skills/medication-adherence-message-gen)
- [Audit Reference](references/audit-reference.md)

## Skill Output:

**Output Type(s):** [text, json, guidance]

**Output Format:** [Plain text or JSON medication-reminder content, with optional alternative messages and psychology insight.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires medication; optional patient name, dosage, time, psychology principle, tone, language, day, and progress.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
