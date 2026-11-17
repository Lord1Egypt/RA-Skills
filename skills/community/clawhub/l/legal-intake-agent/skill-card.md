## Description:

Ultra-high-ticket intake agent for Law Firms. Qualifies leads, performs preliminary conflict-of-interest checks, and books consultations. Hardened with ThumbGate to prevent illegal legal advice or unauthorized practice of law (UPL).

This skill is ready for commercial/non-commercial use.

## Publisher:

[igorganapolsky](https://clawhub.ai/user/igorganapolsky)

### License/Terms of Use:

MIT-0

## Use Case:

Law firms use this agent to screen prospective clients, perform preliminary conflict checks against adverse-party records, qualify matters by case type, limitations period, and budget, and route or book consultations. It is intended for intake support and requires attorney-approved policies before use in a real law-firm workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive legal intake data and external bookings.

Mitigation: Restrict CRM, calendar, Google Sheets, Make.com, and voice-service integrations to least privilege and require human confirmation before bookings.

Risk: Advertised legal-safety blocking may be insufficient without deterministic controls and attorney-approved policy review.

Mitigation: Pin and verify ThumbGate, test conflict and limitations-period blocking, and approve policies with qualified legal staff before production use.

Risk: The setup command uses the identifier legal-intake-agent while the skill frontmatter name is legal-intake-conflict-check-agent.

Mitigation: Resolve the skill identifier mismatch before installation or automation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/igorganapolsky/skills/legal-intake-agent)
- [Setup Guide](artifact/setup-guide.md)
- [ThumbGate Prevention Rules](artifact/thumbgate-rules.md)
- [Make.com](https://make.com)
- [ElevenLabs](https://elevenlabs.io/affiliates)

## Skill Output:

**Output Type(s):** [Text, Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with setup steps, policy rules, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May route conflict matches to a senior partner and create bookings through configured CRM or calendar integrations.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
