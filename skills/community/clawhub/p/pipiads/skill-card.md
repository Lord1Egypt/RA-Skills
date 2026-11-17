## Description:

AI-powered TikTok & Facebook Adspy and Ad Library research for ads, products, stores, landing pages, advertisers, and competitors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fanyanggod](https://clawhub.ai/user/fanyanggod)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to research TikTok and Facebook advertising intelligence, including ads, products, stores, advertisers, competitors, and campaign trends through PipiAds. It also supports monitoring workflows and image-based searches when the user explicitly requests them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and runs a third-party npm package that receives the configured PipiAds API key.

Mitigation: Install only if the npm package is trusted, prefer an isolated environment, and use a limited, revocable API key where possible.

Risk: Search queries and optional image inputs are sent to the external PipiAds service.

Mitigation: Avoid sending sensitive personal data, confidential customer information, private campaign assets, or unnecessary images.

Risk: Broad searches and detail requests can consume PipiAds account credits.

Mitigation: Clarify platform, region, time range, category, and target object before running expensive or broad queries.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fanyanggod/skills/pipiads)
- [PipiAds homepage](https://www.pipiads.com)
- [PipiAds API portal](https://www.pipispy.com/)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, shell commands, configuration, guidance]

**Output Format:** [Markdown with concise analysis, tool-selection guidance, and inline shell or configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return ad, product, store, advertiser, ranking, monitor, or image-search results from the configured PipiAds MCP server.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
