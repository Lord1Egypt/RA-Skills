## Description: <br>
Plans trips for users who want to attend multiple concerts by searching tour dates, matching nearby shows, and optionally adding flight and hotel options. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[piaowenhao152-glitch](https://clawhub.ai/user/piaowenhao152-glitch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to compare concert dates for one or more artists, identify viable multi-show itineraries, and optionally add flight and nearby hotel options. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local snapshots may retain concert search history and travel-planning context on shared machines. <br>
Mitigation: Review or delete the snapshots directory after use when privacy or shared-device access matters. <br>
Risk: Flight, hotel, ticket availability, and prices can change after the skill reports them. <br>
Mitigation: Verify live booking pages before purchasing and treat estimates as planning guidance. <br>
Risk: The Taiwan-related ranking penalty may not match every user's travel documents or preferences. <br>
Mitigation: Ask the agent to ignore or adjust that ranking rule when it is not applicable. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/piaowenhao152-glitch/multi-concert-trip-planner) <br>
- [Skill Workflow](artifact/SKILL.md) <br>
- [Concert Search Strategy](artifact/concert-search.md) <br>
- [Combination Matching Algorithm](artifact/combination-matching.md) <br>
- [Flight Search](artifact/flight-search.md) <br>
- [Hotel Search](artifact/hotel-search.md) <br>
- [Output Template](artifact/output-template.md) <br>
- [Diff Tracking](artifact/diff-tracking.md) <br>
- [Blocked Sites](artifact/BLOCKED_SITES.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown itinerary summaries with tables, links, optional shell commands, and optional JSON snapshot records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include concert combinations, ticket links, flight and hotel options, cost estimates, and change summaries when prior snapshots exist.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
