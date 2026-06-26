## Description: <br>
Design premium luxury travel experiences — first class flights, 5-star resorts, private tours, Michelin dining, and VIP access to exclusive venues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel planners use this skill to assemble premium travel options with first-class flights, luxury hotels, attractions, and itinerary support from live flyai CLI results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may install and run the global flyai CLI to retrieve travel data. <br>
Mitigation: Install only after confirming the package source is trusted, and approve CLI execution before using it for real-time travel results. <br>
Risk: Trip requests may be retained in a hidden local execution log when file writes are available. <br>
Mitigation: Disable, review, or delete .flyai-execution-log.json if raw trip requests should not be stored locally. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dingtom336-gif/luxury-trip) <br>
- [Templates — luxury-trip](references/templates.md) <br>
- [Playbooks — luxury-trip](references/playbooks.md) <br>
- [Fallbacks — Trip Planning Category](references/fallbacks.md) <br>
- [Runbook — Execution Log Schema](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with comparison tables, booking links, concise recommendations, and retry commands when live data is unavailable] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires flyai CLI output for travel results; should not answer travel availability or pricing from model knowledge alone.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
