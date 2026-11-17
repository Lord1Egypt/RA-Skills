## Description:

Find hidden flight deals by comparing prices across 10+ booking sites when users share flight prices, booking-site screenshots, or requests to validate whether a round-trip fare is a good deal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simonenavifare](https://clawhub.ai/user/simonenavifare)

### License/Terms of Use:

MIT-0

## Use Case:

Travelers and travel-support agents use this skill to double-check round-trip flight prices before purchase, compare live options across booking providers, and present ranked booking links with savings calculations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends pre-booking flight itinerary details to Navifare for price comparison.

Mitigation: Use it only for itinerary, price, passenger-count, and class details needed for comparison; avoid passenger names, booking references, loyalty numbers, passport data, and payment details.

Risk: Optional local npm setup introduces normal package and API-key supply-chain exposure.

Mitigation: Prefer the hosted MCP endpoint when appropriate; if running locally, pin package versions where possible and use a dedicated low-quota Gemini API key.

Risk: Returned booking links point to third-party provider sites.

Mitigation: Verify the destination domain and fare details before entering personal or payment information.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/simonenavifare/skills/navifare-hidden-flight-deals)
- [Publisher profile](https://clawhub.ai/user/simonenavifare)
- [Navifare website](https://navifare.com)
- [Navifare MCP documentation](https://www.navifare.com/mcp)
- [Repository metadata](https://github.com/navifare/navifare-mcp)
- [Airport code reference](artifact/references/AIRPORTS.md)
- [Airline code reference](artifact/references/AIRLINES.md)
- [Usage examples](artifact/references/EXAMPLES.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown summaries, comparison tables, configuration snippets, and booking-link guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are based on real-time provider checks and may include third-party booking URLs whose prices can change after the search.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
