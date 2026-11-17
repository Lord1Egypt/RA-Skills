## Description:

First aid protocols for sprains, strains, minor wounds, and common injuries. Use when someone is hurt and wants to know if they need emergency care or can treat at home, and how to do it correctly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[howtousehumans](https://clawhub.ai/user/howtousehumans)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill for immediate first-aid triage and step-by-step home-care guidance for minor sprains, strains, cuts, wounds, and bruises, including when to seek emergency or professional care.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive injury details may be retained across sessions for follow-up without explicit consent, retention limits, or deletion controls.

Mitigation: Require explicit opt-in before persistence, document retention duration, provide clear deletion commands, and avoid storing unnecessary medical details.

Risk: First-aid guidance could be mistaken for professional medical evaluation in borderline or escalating injury cases.

Mitigation: Keep emergency red-flag checks first, preserve conservative referral criteria, and instruct users to seek professional care when symptoms are severe, unclear, or worsening.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/howtousehumans/skills/minor-injury-first-response)
- [Publisher profile](https://clawhub.ai/user/howtousehumans)
- [Rest, ice, compression and elevation therapy evidence review](https://doi.org/10.4085/1062-6050-47.4.435)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown conversational guidance with checklists and follow-up state configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist injury details for follow-up prompts; review consent, retention, and deletion handling before deployment.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
