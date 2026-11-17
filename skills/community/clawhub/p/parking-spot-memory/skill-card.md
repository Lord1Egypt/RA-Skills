## Description:

Helps drivers record parking details, find their car with level-first search guidance, and check when paid parking expires.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT

## Use Case:

Drivers use this skill to save a parking spot's location, level, row, landmarks, photo reference, and payment deadline, then retrieve the details when returning to the car.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Parking history, plate numbers, notes, and photo references are kept in a local plaintext JSON file.

Mitigation: Avoid cloud-synced or shared installations and manually remove old entries when no longer needed.

Risk: Paid-parking expiry status is shown only when checked; missed checks may leave an expired session unnoticed.

Mitigation: Run the expiry check before payment runs out and do not rely on automatic alerts.

## Reference(s):

- [Parking Spot Memory on ClawHub](https://clawhub.ai/voronindenis5/skills/parking-spot-memory)
- [Publisher profile](https://clawhub.ai/user/voronindenis5)
- [Parking memory and garage navigation reference](references/memory-protocol.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text with command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [On-demand parking records, location search tips, and payment-expiry status.]

## Skill Version(s):

1.0.0 (source: skill frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
