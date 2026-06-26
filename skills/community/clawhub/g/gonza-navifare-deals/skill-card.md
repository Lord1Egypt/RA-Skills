## Description: <br>
Verify and compare flight prices across multiple booking sites using Navifare, returning ranked results and booking links for round-trip itineraries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gonzachee](https://clawhub.ai/user/gonzachee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travelers and travel-planning agents use this skill to validate a flight price before booking, compare a round-trip itinerary across booking providers, and receive ranked booking options with savings context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Flight itinerary details, passenger counts, travel class, and reference prices are sent to Navifare's hosted MCP service. <br>
Mitigation: Install only when the user trusts the hosted service and share only the itinerary details needed for price comparison. <br>
Risk: Screenshots can contain passenger names, booking references, loyalty numbers, passport details, or payment information. <br>
Mitigation: Extract only route, flight, timing, class, passenger count, and price details before calling the MCP service. <br>
Risk: Flight prices and booking links may change after the search result is returned. <br>
Mitigation: Tell users to verify the booking link, price, fare terms, and provider details directly before purchase. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/gonzachee/gonza-navifare-deals) <br>
- [Navifare MCP Documentation](https://www.navifare.com/mcp) <br>
- [Navifare MCP Server](https://mcp.navifare.com/mcp) <br>
- [AIRPORTS.md](references/AIRPORTS.md) <br>
- [AIRLINES.md](references/AIRLINES.md) <br>
- [EXAMPLES.md](references/EXAMPLES.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, configuration, guidance] <br>
**Output Format:** [Markdown summaries with tables, booking links, and parsed JSON-derived flight price results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the hosted Navifare MCP server; supports round-trip flight price checking and does not book flights automatically.] <br>

## Skill Version(s): <br>
1.2.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
