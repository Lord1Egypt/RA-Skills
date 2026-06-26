## Description: <br>
Query Japanese seasonal data - cherry blossom forecasts, autumn foliage tracking, and festival search - when a user asks about sakura bloom dates, best time to visit Japan, autumn leaves, Japanese festivals, or Japan travel timing questions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ko-syun](https://clawhub.ai/user/ko-syun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to query Japan-specific seasonal timing, including sakura forecasts, autumn foliage status, historical records, and festival search results. It is intended for natural-language answers backed by calls to the Japan Seasons API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires use of an external seasonal-data API and an API key. <br>
Mitigation: Use a dedicated low-sensitivity API key and avoid sharing unrelated personal travel details in API queries. <br>
Risk: The API is scoped to sakura, autumn foliage, and festival timing rather than general Japan travel planning. <br>
Mitigation: Use the skill for seasonal and festival timing questions, and rely on other sources for broader itinerary, lodging, or transportation planning. <br>


## Reference(s): <br>
- [Japan Seasons API dashboard](https://jpseasons.dokos.dev/dashboard) <br>
- [Japan Seasons API base URL](https://jpseasons.dokos.dev) <br>
- [ClawHub skill page](https://clawhub.ai/ko-syun/japan-seasons) <br>


## Skill Output: <br>
**Output Type(s):** [API calls, Shell commands, Guidance, Markdown] <br>
**Output Format:** [Markdown with inline curl examples and natural-language summaries of JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an X-API-Key header for Japan Seasons API requests.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
