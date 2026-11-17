## Description:

Compare real-time hotel prices across Booking.com, Agoda, Trip.com, and other OTAs with direct booking links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangms30](https://clawhub.ai/user/yangms30)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use this skill to search destinations, compare hotel rates across OTAs, identify lower-priced options, and return direct booking links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hotel destinations, dates, room counts, and related search details may be sent to external travel providers.

Mitigation: Avoid sensitive travel details where possible and review provider policies before using returned links or external APIs.

Risk: Optional Apify mode uses an API key for Agoda-specific deep search.

Mitigation: Use Apify mode only when needed, keep APIFY_API_KEY in a secure environment variable, and avoid exposing it in prompts, logs, or shared output.

Risk: Live OTA availability and rates can change or be incomplete.

Mitigation: Present prices as time-sensitive search results and have users confirm final totals, taxes, and cancellation terms on the booking provider site.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yangms30/skills/hotel-price-finder)
- [Xotelo destination search API](https://data.xotelo.com/api/search?q=DESTINATION&limit=5)
- [Xotelo hotel list API](https://data.xotelo.com/api/list?location_key=${LOCATION_KEY}&limit=${LIMIT})
- [Xotelo OTA rates API](https://data.xotelo.com/api/rates?hotel_key=${HOTEL_KEY}&chk_in=${CHECK_IN}&chk_out=${CHECK_OUT}&currency=${CURRENCY})
- [Agoda destination autocomplete API](https://www.agoda.com/api/cronos/search/GetUnifiedSuggestResult/3/1/1/0/en-us/?searchText=DESTINATION&origin=US)
- [Apify Agoda scraper run API](https://api.apify.com/v2/acts/knagymate~fast-agoda-scraper/runs?token=${APIFY_API_KEY})

## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance]

**Output Format:** [Markdown hotel comparison with tables, savings notes, and direct booking links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API call commands, generated OTA booking URLs, and optional Apify-mode guidance using APIFY_API_KEY.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
