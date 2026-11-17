## Description:

24/7 Voice & Text Dispatch Agent for HVAC & Plumbing. Qualifies leads, checks service zones, books appointments into ServiceTitan/Housecall Pro, and uses ThumbGate to prevent dangerous misquotes or out-of-zone bookings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[igorganapolsky](https://clawhub.ai/user/igorganapolsky)

### License/Terms of Use:

MIT-0

## Use Case:

External HVAC and plumbing businesses use this skill to handle after-hours voice and text inquiries, qualify leads, validate service zones, triage emergencies, and book qualified appointments into CRM or calendar systems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connected CRM, calendar, or voice-provider permissions could exceed dispatch needs.

Mitigation: Limit integration permissions to dispatch workflows and confirm access before installation.

Risk: Incorrect service-zone or emergency-routing configuration could create out-of-zone bookings or delay human escalation.

Mitigation: Configure service zones and emergency routing before use, and keep staff review or reversal available for bookings.

Risk: The agent could provide unsafe or misleading repair-price commitments if quoting controls are not enforced.

Mitigation: Use ThumbGate rules to block exact repair quotes and allow only standard dispatch or diagnostic fees before an onsite technician assessment.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/igorganapolsky/skills/hvac-dispatch-agent)
- [ClawHub publisher profile](https://clawhub.ai/user/igorganapolsky)

## Skill Output:

**Output Type(s):** [Text, Guidance, Configuration]

**Output Format:** [Markdown instructions and operational rules]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires configured CRM or calendar integration, voice provider access, service-zone rules, emergency routing, and ThumbGate.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata; artifact SKILL.md frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
