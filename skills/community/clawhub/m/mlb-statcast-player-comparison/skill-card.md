## Description:

Compare MLB players using Crawlora Statcast leaderboards and player statistics with board-specific discovery, season, role, qualification, metric units, and sample controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Baseball analysts and developers use this skill to compare selected MLB players or a defined cohort for performance briefs, pitch-arsenal comparisons, and role-specific shortlists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A Crawlora API key could be exposed in shared logs or other output.

Mitigation: Treat CRAWLORA_API_KEY as a password and avoid sharing logs that contain it.

Risk: Broad requests may exceed the intended player, team, date, or credit scope.

Mitigation: Limit requests and pages to the intended comparison scope and credit budget.

Risk: Unequal samples or differently defined metrics can make player comparisons misleading.

Mitigation: Show role, season, board qualification, event counts, metric units, and missing-player reasons alongside results.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/crawlora-org/skills/mlb-statcast-player-comparison)
- [MLB endpoint reference](reference/endpoints.md)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown tables and narrative]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes player identity, comparison scope, metric units, qualification, sample counts, source context, and unknowns.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
