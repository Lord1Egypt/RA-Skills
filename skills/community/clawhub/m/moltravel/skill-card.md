## Description: <br>
MolTravel helps agents research trips using the MolTravel MCP server for flight search, price comparison, visa checks, destination information, travel advisories, airport and airline lookup, and activities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[simonenavifare](https://clawhub.ai/user/simonenavifare) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and agents use this skill to plan trips, compare flights, check visa requirements, review destination facts and travel advisories, and find activities through MolTravel-connected tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Travel prompts and lookup parameters are sent to MolTravel's remote MCP service. <br>
Mitigation: Avoid sending passport numbers, payment details, account credentials, or unusually sensitive itinerary information unless the provider's privacy practices have been verified. <br>
Risk: Travel, visa, price, availability, and advisory results can become stale or vary by source. <br>
Mitigation: Treat outputs as planning guidance and verify critical booking, entry, safety, and pricing details with authoritative providers before acting. <br>
Risk: The skill provides comparison and booking links but is not intended to complete purchases. <br>
Mitigation: Use the skill for research and comparison only; complete bookings directly with the selected provider after reviewing terms and final prices. <br>


## Reference(s): <br>
- [Moltravel ClawHub release](https://clawhub.ai/simonenavifare/moltravel) <br>
- [MolTravel homepage](https://molttravel.com) <br>
- [MolTravel MCP endpoint](https://mcp.molttravel.com/mcp) <br>
- [Navifare publisher site](https://navifare.com) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, API Calls, Configuration, Guidance] <br>
**Output Format:** [Markdown with tables, summaries, links, and structured tool-call guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include flight comparison tables, visa summaries, country facts, travel advisory summaries, activity options, booking links, and MCP configuration snippets.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter, plugin.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
