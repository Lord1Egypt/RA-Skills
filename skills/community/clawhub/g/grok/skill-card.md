## Description:

Search the web and X (Twitter) using xAI's Grok API with real-time access, citations, and image understanding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[castanley](https://clawhub.ai/user/castanley)

### License/Terms of Use:


## Use Case:

Developers and external agent users use this skill to retrieve current web information and X discussion through xAI's Grok API, with optional domain, handle, date, image, and video controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries, filters, and optional media-understanding requests are sent to xAI's API.

Mitigation: Avoid confidential, regulated, or sensitive internal searches unless the xAI account and data-handling terms permit that use.

Risk: The skill requires an XAI_API_KEY credential.

Mitigation: Keep the API key protected in environment configuration and do not expose it in prompts, logs, or shared output.

Risk: Current web and X search results can include incomplete, misleading, or low-quality source material.

Mitigation: Review returned citations and source context before using results for important decisions.

## Reference(s):

- [xAI Web Search documentation](https://docs.x.ai/developers/tools/web-search)
- [xAI X Search documentation](https://docs.x.ai/developers/tools/x-search)
- [xAI API base](https://api.x.ai/v1)
- [ClawHub skill page](https://clawhub.ai/castanley/skills/grok)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Text or Markdown responses with citations, usage metadata, and optional raw API response data.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires XAI_API_KEY and sends search queries, filters, and optional media-understanding requests to xAI's API.]

## Skill Version(s):

1.0.3 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
