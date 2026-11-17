## Description:

Use this skill when the user asks about travel planning, trip research, flight searches, visa requirements, airport/airline lookups, destination info, travel safety, or activities at a destination.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simonenavifare](https://clawhub.ai/user/simonenavifare)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to plan trips, research destinations, search flights, compare prices, check visa requirements, review travel advisories, and find activities through the MolTravel MCP server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Travel-related details may be sent to the MolTravel MCP service and downstream travel providers.

Mitigation: Share only the details needed for the trip-planning task and avoid unnecessary sensitive personal information.

Risk: Prices, visa rules, and travel advisories can change or be incomplete.

Mitigation: Verify prices, visa requirements, and safety advisories with official sources before booking or traveling.

Risk: Flight and activity results may include booking links, but the skill is not a booking authority.

Mitigation: Use returned links for comparison and review only; complete any booking directly with the relevant provider after independent verification.

## Reference(s):

- [MolTravel Skill Page](https://clawhub.ai/simonenavifare/skills/moltravel)
- [MolTravel](https://molttravel.com)
- [MolTravel MCP Server](https://mcp.molttravel.com/mcp)
- [Navifare](https://navifare.com)
- [Publisher Profile](https://clawhub.ai/user/simonenavifare)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown travel summaries, comparison tables, and concise recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include flight, price, visa, country, advisory, activity, airport, airline, and booking-link information; does not complete bookings.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, plugin metadata, and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
