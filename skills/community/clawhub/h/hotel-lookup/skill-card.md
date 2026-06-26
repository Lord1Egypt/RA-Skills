## Description: <br>
Intelligent Hotel Lookup helps agents find, compare, and hand off hotel booking options using FlyAI `search-hotel` with Fliggy MCP filters for destination, dates, POI proximity, lodging type, stars, beds, sorting, and CNY nightly caps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zuckonit](https://clawhub.ai/user/zuckonit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travel-planning agents and assistants use this skill to search hotels, compare shortlists by budget, location, rating, lodging type, and bed preference, then provide booking handoff links for final user review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Hotel prices, availability, cancellation terms, room details, and payment terms may differ from search results by the time a user books. <br>
Mitigation: Use returned results as discovery guidance only and re-check the supplier detail page before reserving or paying. <br>
Risk: The workflow depends on a third-party FlyAI CLI and may use an optional API key. <br>
Mitigation: Verify the npm CLI before installation, keep any API key scoped and out of logs, and avoid exposing local configuration in responses. <br>
Risk: Ambiguous destinations, dates, or filters can lead to irrelevant or misleading hotel recommendations. <br>
Mitigation: Confirm required destination and stay-window details, validate dates, and ask clarifying questions before running a search. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zuckonit/hotel-lookup) <br>
- [FlyAI](https://open.fly.ai/) <br>
- [search-hotel reference](references/search-hotel.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown hotel shortlists with observed JSON fields, images when available, and booking handoff links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live `flyai search-hotel` JSON results; missing hotel details should be treated as unavailable and confirmed on supplier pages.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
