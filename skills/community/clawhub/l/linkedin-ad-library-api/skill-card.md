## Description:

Search ads running across LinkedIn by keyword and/or advertiser company id, returning each ad's advertiser, ad copy, format, promoted label, thumbnail and a detail link, then open one ad in full with its media, headline, who paid for it and the advertiser's company URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing, demand generation, and competitive intelligence teams use this skill to search LinkedIn ads by keyword or advertiser and retrieve structured ad details for analysis. Developers and agents can use it to call Scavio's LinkedIn ads endpoints with a SCAVIO_API_KEY and return only API-provided ad data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends LinkedIn ad research queries and the SCAVIO_API_KEY to Scavio's external service.

Mitigation: Use an approved Scavio account, keep the API key in environment or secret storage, and avoid submitting sensitive queries unless permitted.

Risk: API calls consume paid or free Scavio account credits, and LinkedIn Ads endpoints cost 6 credits per call.

Mitigation: Scope searches deliberately, check remaining credits in API responses, and avoid unnecessary retries or broad repeated queries.

Risk: Ad details such as impressions, demographics, dates, and media URLs may be null or temporary when the API or LinkedIn does not provide them.

Mitigation: Report only returned fields, do not infer missing reach or spend data, and fetch CDN media promptly when needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/scavio-ai/skills/linkedin-ad-library-api)
- [Scavio API documentation](https://scavio.dev/docs?utm_source=agent-skills&utm_medium=skill&utm_campaign=linkedin-ad-library-api)
- [Scavio rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=linkedin-ad-library-api)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, code, shell commands, configuration, json]

**Output Format:** [Markdown guidance with Python and curl examples that call an external API returning structured JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SCAVIO_API_KEY; LinkedIn Ads endpoints consume 6 Scavio credits per call.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
