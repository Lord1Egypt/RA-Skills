## Description:

Use when checking into a hotel, hostel, or rental room — runs the first-15-minute protective sweep (bedbug harborage inspection order, hidden-camera RF/lens/emission checks ranked by risk, safe-vs-dresser valuables protocol, exit-route count) and logs evidence with timestamps if something IS found, so a bad room is caught before you unpack, not after you wake up with bites.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT

## Use Case:

Travelers checking into hotels, hostels, and rentals use this skill to inspect for bedbug signs and possible hidden cameras, secure valuables, check exits, and record findings for follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Visual, network, or supplemental detector checks may miss a hidden camera and cannot establish that a room is surveillance-free.

Mitigation: Treat the sweep as a manual checklist rather than a detector or guarantee, and follow the documented escalation steps if you find a suspected device.

Risk: The local evidence log may contain sensitive travel and room details.

Mitigation: Protect the log and delete it when it is no longer needed.

Risk: A drafted escalation letter may include details that should not be shared as written.

Mitigation: Review the letter before sending or sharing it.

## Reference(s):

- [Hotel Room Sweep Field Reference](artifact/references/sweep-field-guide.md)
- [ClawHub release page](https://clawhub.ai/voronindenis5/skills/hotel-room-safeguard)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON, Markdown]

**Output Format:** [Markdown checklists and guidance, shell commands, a local JSON evidence log, and a drafted Markdown escalation letter]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The optional local log records timestamps, room and property details, findings, photo counts, and guest name.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata, SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
