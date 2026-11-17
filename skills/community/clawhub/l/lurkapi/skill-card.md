## Description:

Retrieves current public data as JSON from social platforms, ad libraries, eBay, and web pages, mapping each question to a suitable LurkAPI endpoint, its parameters, and price.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mesmerlord](https://clawhub.ai/user/mesmerlord)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use LurkAPI to retrieve up-to-date public social, advertising, marketplace, and web data and answer questions about profiles, posts, engagement, transcripts, ads, or pages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted searches, handles, and URLs are sent to LurkAPI; URLs may contain access tokens or other sensitive data.

Mitigation: Use public, non-sensitive queries and remove credentials or tokens from URLs. Check provider terms for data-retention details before use.

Risk: API calls consume credits, and some scraping requests can incur automatic additional charges.

Mitigation: Review the endpoint price and available credit balance before repeated or high-cost requests.

Risk: An exposed API key could allow unauthorized use of the account.

Mitigation: Keep the key in the LURKAPI_API_KEY environment variable and do not share it in chat or expose it in logs.

## Reference(s):

- [LurkAPI ClawHub skill page](https://clawhub.ai/mesmerlord/skills/lurkapi)
- [LurkAPI endpoint documentation example](https://lurkapi.com/docs/tiktok/profile-videos.md)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [Structured JSON data with concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Result fields vary by endpoint; long responses may be paginated.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
