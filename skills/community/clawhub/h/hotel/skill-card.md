## Description:

Local-first hotel decision engine for trip stays, hotel comparison, shortlist creation, booking readiness, and accommodation planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agistack](https://clawhub.ai/user/agistack)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use this skill to capture trip context, compare hotel candidates, shortlist best-fit stays, and check booking readiness before purchase.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Trip destinations, dates, budgets, hotel candidates, preferences, and notes are stored as plaintext JSON on the local machine.

Mitigation: Avoid saving sensitive travel details on shared machines, or restrict filesystem permissions for ~/.openclaw/workspace/memory/hotel.

Risk: The skill provides local planning and comparison support only; it does not book hotels or verify live availability, pricing, or policy changes.

Mitigation: Confirm current hotel prices, availability, cancellation terms, and booking details directly with the booking provider before purchase.

## Reference(s):

- [Hotel Philosophy](references/philosophy.md)
- [ClawHub Skill Page](https://clawhub.ai/agistack/skills/hotel)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and local JSON-backed planning records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores destinations, dates, budgets, hotel candidates, notes, and preferences as plaintext JSON under ~/.openclaw/workspace/memory/hotel.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
