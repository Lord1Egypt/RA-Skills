## Description:

Search the web and read web pages with Oxylabs AI Studio, returning search results, optional page text, or scraped URL content as Markdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oxylabs](https://clawhub.ai/user/oxylabs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to search the current web, gather source links, fetch optional page text, or scrape a specific page into Markdown through Oxylabs AI Studio.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms, target URLs, geo options, and fetched page content are sent to Oxylabs.

Mitigation: Use the skill only when third-party processing by Oxylabs is approved; avoid secrets, private or internal URLs, regulated data, and confidential research unless that use is explicitly allowed.

Risk: Fetched web content may be incomplete, stale, or affected by geo and JavaScript rendering options.

Mitigation: Review returned sources and choose geo or JavaScript rendering settings deliberately when result quality matters.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/oxylabs/skills/oxylabs-web-search)
- [Oxylabs AI Studio API key](https://aistudio.oxylabs.io/api-key)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with command-line and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OXYLABS_AI_STUDIO_API_KEY; search can return titles, URLs, descriptions, and optional page text, while scrape returns page content as Markdown.]

## Skill Version(s):

0.1.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
