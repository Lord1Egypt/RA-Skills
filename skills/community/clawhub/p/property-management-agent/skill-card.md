## Description:

Autonomous tenant maintenance and ticketing agent that triages tenant requests, distinguishes emergencies from routine maintenance, validates tenant details, and syncs tickets with Buildium, AppFolio, or Google Sheets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[igorganapolsky](https://clawhub.ai/user/igorganapolsky)

### License/Terms of Use:

MIT-0

## Use Case:

External property managers and landlords use this skill to handle tenant maintenance intake, validate tenant and unit information, classify emergencies versus routine repairs, and create or sync maintenance tickets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Autonomous emergency triage and repair approval rules are under-specified and could affect tenant safety or spending decisions.

Mitigation: Require human review for emergencies, ambiguous maintenance reports, and repair quotes before dispatch or approval.

Risk: The spending cap is documented as 00, which omits an explicit currency amount.

Mitigation: Replace the placeholder with a specific currency-denominated cap and require explicit landlord approval above that amount.

Risk: Tenant and owner data may be sent to external systems such as CRM, ticketing, voice, or automation integrations.

Mitigation: Document exactly what tenant data is sent to each integration and keep privacy rules active for door codes, owner phone numbers, and other sensitive data.

Risk: The setup guide uses a mutable npx ThumbGate install command.

Mitigation: Use a pinned, verified ThumbGate install path before deploying the skill in a real property-management workflow.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/igorganapolsky/skills/property-management-agent)
- [Setup Guide](artifact/setup-guide.md)
- [ThumbGate Prevention Rules - Property Management](artifact/thumbgate-rules.md)
- [ElevenLabs](https://elevenlabs.io/affiliates)
- [Make.com](https://make.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce maintenance triage guidance, ticketing setup steps, emergency escalation rules, and integration instructions for property-management workflows.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
