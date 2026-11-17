## Description:

Extract content from specific URLs using Tavily's extraction API. Returns clean markdown/text from web pages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[matthew77](https://clawhub.ai/user/matthew77)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to extract clean page content from known URLs, optionally focusing extraction with a query and returning markdown, text, or raw JSON.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Target URLs and optional query terms are sent to Tavily for extraction.

Mitigation: Avoid internal, private, signed, personal, regulated, or confidential URLs unless the organization has approved Tavily for that data.

Risk: The skill requires a Tavily API key.

Mitigation: Provide the key through approved secret or environment configuration and avoid committing it in skill configuration.

Risk: Some URLs may fail or return incomplete content.

Mitigation: Review failed results and compare basic versus advanced extraction when output quality matters.

## Reference(s):

- [Tavily](https://tavily.com)
- [ClawHub Skill Page](https://clawhub.ai/matthew77/skills/liang-tavily-extract)

## Skill Output:

**Output Type(s):** [text, markdown, JSON]

**Output Format:** [Markdown, plain text, or raw JSON from Tavily extraction results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports up to 20 URLs per request, optional query-focused chunks, basic or advanced extraction depth, and timeout settings up to 60 seconds.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
