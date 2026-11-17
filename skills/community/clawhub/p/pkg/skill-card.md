## Description:

Helps plan trips around existing commitments and manage Apple Calendar events through iCloud.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alan1527061](https://clawhub.ai/user/alan1527061)

### License/Terms of Use:

MIT-0

## Use Case:

People with an Apple Calendar can import recurring schedules, check availability, plan outings using weather and travel estimates, and add or cancel calendar events after review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Calendar writes or deletions could change the wrong event or bypass the intended consent workflow.

Mitigation: Review every proposed write or deletion before applying it; avoid cancel --uid until UID-prefix and calendar-scope checks are fixed.

Risk: An Apple app-specific password and private schedule data could be exposed.

Mitigation: Keep data/profile.json private and provide credentials only if comfortable granting calendar access.

Risk: Trip planning contacts iCloud and mapping or weather services.

Mitigation: Use the skill only if sharing relevant calendar and trip information with those services is acceptable.

## Reference(s):

- [apple-calpal on ClawHub](https://clawhub.ai/alan1527061/skills/pkg)

## Skill Output:

**Output Type(s):** [Text, JSON, Calendar event changes]

**Output Format:** [Conversational guidance, structured event data, and iCloud calendar updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes availability checks, suggested departure times, and event proposals for user review.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
