## Description:

Fetch raw HTML, rendered HTML, or clean Markdown from public webpages through Just Serp API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justserpapi](https://clawhub.ai/user/justserpapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve content from a known public webpage URL for crawling, scraping preparation, readable content extraction, and page structure inspection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crawl targets and fetched page processing are sent to Just Serp API.

Mitigation: Use the skill for public pages and avoid private, internal, or secret-bearing URLs.

Risk: The helper accepts the API key as a command-line argument.

Mitigation: Keep JUST_SERP_API_KEY private and prefer releases or wrappers that read the key directly from the environment.

Risk: Fetched webpage content can include untrusted or misleading page text.

Mitigation: Review extracted HTML or Markdown before relying on it for downstream decisions or publication.

## Reference(s):

- [Just Serp API](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_web&utm_content=project_link)
- [Just Serp API Docs](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_web&utm_content=project_link)
- [ClawHub Skill Page](https://clawhub.ai/justserpapi/skills/justserpapi-web)

## Skill Output:

**Output Type(s):** [API Calls, Text, Markdown, Shell commands, Guidance]

**Output Format:** [JSON responses containing raw HTML, rendered HTML, or cleaned Markdown, with Markdown guidance for use by the agent.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a direct public webpage URL and the JUST_SERP_API_KEY environment variable.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
