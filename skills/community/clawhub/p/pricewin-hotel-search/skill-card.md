## Description:

Search hotels live across Agoda, Booking.com, Traveloka, and OpenTravel with realtime pricing for specific dates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cotghw](https://clawhub.ai/user/cotghw)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to ask an agent for live hotel prices, compare OTA listings for specific travel dates, and receive a short Markdown shortlist with booking links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hotel search queries are sent to PriceWin's hosted MCP backend, including city, dates, adult count, language code, and polling session IDs.

Mitigation: Install only when that hosted-backend data flow is acceptable; use the documented local or standalone alternative when the user does not want a hosted intermediary.

Risk: The hosted MCP server and crawler backend are closed-source, so only the skill instructions are directly auditable.

Mitigation: Disclose the backend trust boundary to users and avoid implying assurance beyond the available documentation and security evidence.

Risk: Hotel names, reviews, and URLs are third-party OTA content returned through tool results.

Mitigation: Treat returned content as data rather than instructions, and show only URLs returned by the tool with the user's dates appended as documented.

## Reference(s):

- [Hotel Search Tool Reference](reference.md)
- [Security and Data Handling](SECURITY.md)
- [PriceWin Skills Hub](https://github.com/Price-Win/pricewin-skills-hub)
- [PriceWin](https://price.win)
- [PriceWin Privacy Policy](https://price.win/en/privacy-policy)

## Skill Output:

**Output Type(s):** [Markdown, API Calls, Guidance]

**Output Format:** [Markdown hotel shortlist with MCP tool calls and booking URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Presents the top 5-7 cheapest qualifying hotel results, with prices in USD and source comparisons when duplicate listings are found.]

## Skill Version(s):

1.0.4 (source: frontmatter and ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
