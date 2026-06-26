## Description: <br>
Voyage builds constraint-aware travel itineraries from a destination, dates, budget, dietary preferences, and pace, then assembles lodging, dining, and activity recommendations into a logistics-optimized plan without auto-booking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[indigokarasu](https://clawhub.ai/user/indigokarasu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travelers and agents use Voyage to plan multi-day trips, compare lodging, dining, and activity options, optimize itinerary feasibility, and track reservation-ready decisions without treating uncertain availability as confirmed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Voyage can create a daily self-update task that silently replaces its own files from GitHub. <br>
Mitigation: Review or disable the voyage:update cron job before use, and prefer manual updates from a pinned or verified release. <br>
Risk: The skill stores local itinerary, reservation, decision, and journal data. <br>
Mitigation: Use it only where local travel data storage is acceptable, and review the configured data and journal directories before deployment. <br>


## Reference(s): <br>
- [Voyage Itinerary Constraints](references/itinerary_constraints.md) <br>
- [Voyage Recommendation Style](references/recommendation_style.md) <br>
- [Voyage Schemas](references/voyage_schemas.md) <br>
- [Journal](references/journal.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, shell commands, guidance] <br>
**Output Format:** [Markdown and JSON-backed local plan, state, decision, reservation, and journal files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces reservation-ready planning artifacts and local journals; it does not auto-book unless explicitly enabled.] <br>

## Skill Version(s): <br>
2.3.0 (source: server release evidence and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
