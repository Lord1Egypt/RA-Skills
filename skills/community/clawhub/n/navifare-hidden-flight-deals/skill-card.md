## Description: <br>
Find hidden flight deals by comparing prices across 10+ booking sites when users share flight prices from booking sites or upload flight screenshots. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[simonenavifare](https://clawhub.ai/user/simonenavifare) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travelers and travel-support agents use this skill to double-check round-trip flight prices, compare real-time offers across booking providers, and return ranked booking options with savings calculations. It is intended for pre-booking itinerary validation, not automatic ticket purchase. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Flight itinerary details are sent to the remote Navifare MCP service for price comparison. <br>
Mitigation: Use the skill only when sharing route, date, time, passenger-count, class, price, and currency details with Navifare is acceptable. <br>
Risk: Screenshots from booking sites may include passenger names, booking references, loyalty numbers, passport details, or payment information. <br>
Mitigation: Redact screenshots or extract only itinerary details before sending data to the Navifare MCP tools. <br>
Risk: The optional local npm setup uses a Gemini API key. <br>
Mitigation: Protect the API key, pin or review the package source, and prefer the hosted MCP endpoint when that matches the deployment policy. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/simonenavifare/navifare-hidden-flight-deals) <br>
- [Publisher site](https://navifare.com) <br>
- [Navifare MCP documentation](https://www.navifare.com/mcp) <br>
- [Navifare MCP repository](https://github.com/navifare/navifare-mcp) <br>
- [Airport code reference](references/AIRPORTS.md) <br>
- [Airline code reference](references/AIRLINES.md) <br>
- [Usage examples](references/EXAMPLES.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Configuration] <br>
**Output Format:** [Markdown summaries with comparison tables, booking links, savings calculations, and setup snippets when needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns advisory results only; booking is completed by the user on provider sites.] <br>

## Skill Version(s): <br>
1.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
