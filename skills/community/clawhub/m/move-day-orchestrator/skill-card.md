## Description:

Plans household moves with a dated checklist, packing waves, searchable box inventory, truck and crew estimates, and a moving-day schedule.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT

## Use Case:

People and small teams planning a home or small-business move use this skill to coordinate packing, estimate transport needs, track boxes, and organize moving day and arrival.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An explicitly chosen state-file path may overwrite an unrelated file.

Mitigation: Use a dedicated path for the move inventory and avoid pointing --state at important files.

Risk: Truck and crew estimates are planning heuristics and may not account for unusual or heavy items.

Mitigation: Confirm capacity and timing with movers; use qualified professionals for pianos, safes, and other rigging items.

## Reference(s):

- [Moving Playbook](references/moving-playbook.md)
- [Move Day Orchestrator on ClawHub](https://clawhub.ai/voronindenis5/skills/move-day-orchestrator)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Plain-text checklists, estimates, schedules, and box search results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Box and move details can be stored in a local JSON state file.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
