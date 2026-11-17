## Description:

Google Hotels toolkit for search, availability, price quotes, and cross-OTA price comparison through StayingAPI, excluding listing details and reviews.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stayingapi](https://clawhub.ai/user/stayingapi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to have an agent retrieve Google Hotels search results, availability, price quotes, and cross-OTA comparisons through StayingAPI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hotel search parameters, dates, occupancy, and property identifiers are sent to StayingAPI.

Mitigation: Use the skill only when that data sharing is acceptable for the user and task.

Risk: A live StayingAPI key can make real billable requests.

Mitigation: Use a sandbox key for evaluation, store keys in an environment-variable or secret store, and review live-key pricing before production use.

Risk: Sandbox fixtures may not mirror the requested listing, dates, or occupancy.

Mitigation: Use sandbox responses for wiring and parsing only, then verify real hotel data with a live key before relying on results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/stayingapi/skills/google-hotels-full)
- [StayingAPI homepage](https://stayingapi.com)
- [StayingAPI docs](https://stayingapi.com/docs)
- [StayingAPI OpenAPI contract](https://api.stayingapi.com/openapi.json)
- [StayingAPI - getting and storing your API key](references/auth-setup.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and API request guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires STAYINGAPI_KEY and internet access to api.stayingapi.com.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
