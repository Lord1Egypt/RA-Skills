## Description:

Guides an agent through planning, scheduling, logging, and safety checklists for handbuilt pottery and pit firing from local clay while the user performs the physical craft work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[howtousehumans](https://clawhub.ai/user/howtousehumans)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to plan local-clay pottery projects, generate material lists and firing schedules, maintain filesystem logs and reminders, and troubleshoot drying, firing, watertightness, and repair issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer is an unpinned npx command and should be verified before use.

Mitigation: Install only from a trusted ClawHub source, avoid elevated privileges, and review the command before running it.

Risk: The skill may use location, soil, or project-site details for clay sourcing and fire-safety planning.

Mitigation: Share only the details needed for planning and review where filesystem logs and reminders will be written.

Risk: Pit firing and local clay use involve fire, contaminant, and food-safety hazards.

Mitigation: Verify local fire rules, soil-contaminant concerns, and food-safety requirements before following physical protocols.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/howtousehumans/skills/handbuilt-pottery-pit-firing-basics)
- [Publisher profile](https://clawhub.ai/user/howtousehumans)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown with checklists, tables, schedules, and decision trees]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write filesystem project logs, inventory trackers, firing schedules, reminders, and safety checklists when the agent has filesystem access.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
