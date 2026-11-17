## Description:

Plan Norway trips with fjord and Arctic routing, verified entry rules, multimodal logistics, and practical seasonal safety.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to plan Norway trips that balance Schengen entry checks, fjord and Arctic route choices, domestic transport, seasonality, budget, accessibility, and outdoor safety. It is most useful when a traveler needs an operational itinerary with realistic bases, transfer windows, booking cautions, and weather fallback options.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Trip preferences and route constraints may persist in ~/norway/memory.md after planning is complete.

Mitigation: Avoid storing sensitive booking identifiers or personal details, and review or delete ~/norway/memory.md when the trip ends or when using a shared machine.

Risk: Entry, road, weather, ferry, and outdoor conditions can change after a plan is drafted.

Mitigation: Confirm entry rules, transport schedules, road status, weather, and outdoor safety guidance with the official sources linked in the skill before booking or departure.

Risk: Overpacked Norway routes can create missed connections, fatigue, weather exposure, or unsafe winter-driving assumptions.

Mitigation: Keep plans corridor-based, include buffer time and downgrade options, and prefer transit-first or guided plans when snow-driving or remote outdoor skill is uncertain.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/skills/norway)
- [UDI Visitor and Visa Guidance](https://www.udi.no/en/want-to-apply/visit-and-holiday/)
- [UDI Visa Requirement Checker](https://www.udi.no/en/want-to-apply/visit-and-holiday/visa-to-visit-norway/)
- [Norway Schengen Overview](https://www.regjeringen.no/en/topics/european-policy/european-cooperation/schengen--justis-og-politisamarbeid/id68512/)
- [Entur National Journey Planner](https://entur.no/)
- [Norwegian Public Roads Administration](https://www.vegvesen.no/en/)
- [SafeTravel Norway](https://www.safetravel.no/en/)
- [Yr Weather Service](https://www.yr.no/en)
- [Visit Norway](https://www.visitnorway.com/)
- [Norwegian Polar Institute Svalbard Guidance](https://www.npolar.no/en/)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Configuration instructions, Shell commands]

**Output Format:** [Markdown with practical itinerary structure, checklists, tables, and occasional shell commands for local memory setup]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce day-by-day route plans, base recommendations, transport tradeoffs, booking cautions, weather fallback options, safety notes, and local memory setup guidance.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
