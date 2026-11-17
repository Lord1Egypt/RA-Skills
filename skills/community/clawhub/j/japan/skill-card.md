## Description:

Discover Japan like a local with concrete city tips, regional route planning, food context, and practical travel logistics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

External users planning travel to Japan use this skill to get city and regional recommendations, itinerary pacing, food and nightlife guidance, transport planning, and practical safety context. It can also maintain local trip preferences in ~/japan/memory.md when the user wants persistent trip context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local trip memory may retain personal trip details on shared machines.

Mitigation: Avoid storing sensitive confirmation numbers, and ask the agent to show, edit, or delete ~/japan/memory.md when old trip context should not be reused.

Risk: Travel logistics, bookings, weather, and operator conditions can change after guidance is produced.

Mitigation: Verify high-value bookings, transport schedules, weather alerts, closures, and emergency information with current official or operator sources before acting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/japan)
- [ClawHub publisher profile](https://clawhub.ai/user/ivangdavila)
- [Skill homepage](https://clawic.com/skills/japan)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and concise text with occasional shell commands for local memory setup.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local trip memory at ~/japan/memory.md when the user wants persistent trip context.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
