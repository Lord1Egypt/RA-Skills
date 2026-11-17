## Description:

A high-security legal intake agent for law firms that helps qualify leads while preventing unauthorized legal advice and PHI leaks through ThumbGate rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[igorganapolsky](https://clawhub.ai/user/igorganapolsky)

### License/Terms of Use:

MIT-0

## Use Case:

External law firm teams use this skill to conduct first-contact legal intake, capture lead details, flag conflicts and statute-of-limitations risks, and prepare attorney review without providing legal advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill collects, stores, and may share sensitive legal intake data, including PHI or PII.

Mitigation: Add an upfront privacy notice, obtain consent before saving or sending intake details to a CRM, and limit collected data to the intake purpose.

Risk: Legal intake records may be retained or accessed beyond the firm's approved process.

Mitigation: Define retention, access controls, and lead database handling before deployment.

Risk: The assistant could be mistaken for legal counsel or provide jurisdictionally inappropriate disclaimers.

Mitigation: Localize the disclaimer for the firm's jurisdiction and require attorney review for conflict checks, legal advice boundaries, and statute-of-limitations flags.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/igorganapolsky/skills/legal-intake-pilot)
- [Setup Guide](artifact/setup-guide.md)
- [ThumbGate Prevention Rules](artifact/thumbgate-rules.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Conversational text and Markdown intake summaries with configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include intake summaries, conflict flags, statute alerts, disclaimers, and redacted lead records.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
