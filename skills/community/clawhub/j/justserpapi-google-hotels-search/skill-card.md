## Description:

Call GET /api/v1/google/hotels/search for Google SERP Hotels Search through Just Serp API with check_in_date, check_out_date, and query.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justserpapi](https://clawhub.ai/user/justserpapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to query Just Serp API for Google Hotels search results by destination or hotel name and check-in/check-out dates. It supports travel comparison and hospitality market analysis using returned prices, ratings, and availability details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hotel search details are sent to Just Serp API.

Mitigation: Use the skill only when sharing the submitted destination, dates, and filters with Just Serp API is acceptable.

Risk: The helper accepts JUST_SERP_API_KEY through command-line arguments during execution.

Mitigation: Run on trusted systems, avoid logging invocation commands, scope the API key where possible, and rotate the key if exposure is suspected.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/justserpapi/skills/justserpapi-google-hotels-search)
- [Just Serp API](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_hotels_search&utm_content=project_link)
- [Just Serp API Docs](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_hotels_search&utm_content=project_link)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, API calls, JSON]

**Output Format:** [Markdown guidance with shell command examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and the JUST_SERP_API_KEY environment variable; the endpoint requires query, check_in_date, and check_out_date.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
