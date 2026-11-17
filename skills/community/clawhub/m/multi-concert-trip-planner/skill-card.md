## Description:

Helps users plan a trip around multiple concerts by finding tour dates, matching nearby shows, and optionally searching flights and hotels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[piaowenhao152-glitch](https://clawhub.ai/user/piaowenhao152-glitch)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use this skill to compare upcoming concerts for one or more artists, identify shows that can fit into a single trip, and assemble a concert itinerary with ticket links and optional flight or hotel options.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dynamic travel queries can be passed into local command templates.

Mitigation: Validate command arguments, avoid shell interpolation for dynamic values, and review commands before execution.

Risk: Search-history snapshots may retain user trip preferences and artist lists locally.

Mitigation: Let users opt in to snapshot retention, inspect saved snapshots, and delete them when they are no longer needed.

Risk: Concert availability, ticket status, flight prices, and hotel prices can change quickly.

Mitigation: Present prices as estimates and direct users to verify current availability and booking terms before purchase.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/piaowenhao152-glitch/skills/multi-concert-trip-planner)
- [Concert search workflow](concert-search.md)
- [Combination matching algorithm](combination-matching.md)
- [Flight search workflow](flight-search.md)
- [Hotel search workflow](hotel-search.md)
- [Diff tracking workflow](diff-tracking.md)
- [Output template](output-template.md)
- [Blocked sites and fallback handling](BLOCKED_SITES.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown travel plan with tables, ticket and booking links, optional fare and hotel data, and JSON search snapshots.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May retain local JSON snapshots for diff tracking; concert, flight, and hotel availability or prices are time-sensitive.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
