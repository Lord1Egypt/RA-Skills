## Description: <br>
Call GET /api/v1/google/hotels/search for Google SERP Hotels Search through Just Serp API with check_in_date, check_out_date, and query. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justserpapi](https://clawhub.ai/user/justserpapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to query Google hotel search data through Just Serp API for destinations, dates, prices, ratings, availability, and travel-comparison filters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Hotel search terms, travel dates, destinations, and filters are sent to Just Serp API using the user's API key. <br>
Mitigation: Use the skill only when sharing those search parameters with Just Serp API is acceptable, and avoid sensitive travel plans unless that sharing is approved. <br>
Risk: The skill requires a JUST_SERP_API_KEY credential. <br>
Mitigation: Provide the key through the environment and avoid pasting key values into chat messages, screenshots, or logs. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/justserpapi/justserpapi-google-hotels-search) <br>
- [Just Serp API](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_hotels_search&utm_content=project_link) <br>
- [Just Serp API Docs](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_hotels_search&utm_content=project_link) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown summary with optional raw JSON response data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JUST_SERP_API_KEY and sends hotel search parameters to Just Serp API.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
