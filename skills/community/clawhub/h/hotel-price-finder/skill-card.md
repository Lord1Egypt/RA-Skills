## Description: <br>
Compare hotel prices across Booking.com, Agoda, Trip.com in real-time. Free multi-OTA price comparison with direct booking links. No API key required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yangms30](https://clawhub.ai/user/yangms30) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travelers, travel planners, and agent users use this skill to search hotels by destination and dates, compare OTA prices, identify the cheapest option, and generate direct booking links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Hotel search details may be sent to Xotelo, Agoda, OTA booking sites, and optionally Apify. <br>
Mitigation: Use the skill only with travel search details suitable for those services, and set APIFY_API_KEY only when the Apify workflow is trusted. <br>
Risk: Optional Apify mode uses an API token and sends travel parameters to an external actor workflow. <br>
Mitigation: Keep APIFY_API_KEY scoped and private, and use the default Xotelo mode when Apify data handling is not acceptable. <br>
Risk: Generated prices and booking links may differ from final OTA checkout prices or availability. <br>
Mitigation: Verify final rates, taxes, cancellation terms, and availability on the linked OTA before booking. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yangms30/hotel-price-finder) <br>
- [Xotelo hotel search API](https://data.xotelo.com/api/search?q=DESTINATION&limit=5) <br>
- [Xotelo hotel list API](https://data.xotelo.com/api/list?location_key=${LOCATION_KEY}&limit=${LIMIT}) <br>
- [Xotelo hotel rates API](https://data.xotelo.com/api/rates?hotel_key=${HOTEL_KEY}&chk_in=${CHECK_IN}&chk_out=${CHECK_OUT}&currency=${CURRENCY}) <br>
- [Agoda destination suggestion API](https://www.agoda.com/api/cronos/search/GetUnifiedSuggestResult/3/1/1/0/en-us/?searchText=DESTINATION&origin=US) <br>
- [Apify API](https://api.apify.com/v2/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with hotel comparison tables, direct booking links, savings notes, and inline shell commands for API calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include generated OTA booking URLs, hotel ratings, review counts, taxes, total prices, savings calculations, and optional Apify-powered Agoda details.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
