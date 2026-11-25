## Description:

Use when a trip is being planned, a passport/ID/license/visa expiry is mentioned, or someone asks 'is my passport still valid for X'. Tracks whole-family travel document validity, applies destination entry rules (6-month / Schengen 3-month-beyond-exit), and back-plans renewal deadlines from real processing times so nobody is denied boarding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT

## Use Case:

External travelers and families use the skill to track travel-document expiry dates, check whether passports meet destination requirements for planned trips, and plan renewals around processing times.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The registry can contain sensitive family travel-document details.

Mitigation: Review what information is stored and control access and retention; keep document numbers to the last four digits where possible.

Risk: The security review flags undeclared file access and uncertainty about when stored data may be checked.

Mitigation: Review file access and the skill's trigger behavior before use, and limit access to the registry and files needed for the task.

## Reference(s):

- [Destination Validity Rules](references/destination-rules.md)
- [Renewal Processing Times & Back-Planning](references/renewal-times.md)
- [Passport Expiry Radar on ClawHub](https://clawhub.ai/voronindenis5/skills/passport-expiry-radar)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Plain-text document status and trip verdicts, with a JSON travel-document registry]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
