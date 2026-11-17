## Description:

Global News By Opera News helps agents retrieve breaking news, top headlines, local city news, article search results, and trending video search results across supported countries in Europe, the Americas, Latin America, and Africa.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zerokileom](https://clawhub.ai/user/zerokileom)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to fetch current news briefings, city-specific local news, topic search results, and hot video search results from Opera News-backed feeds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to make shell-based external requests to the Opera News feed with user-influenced inputs.

Mitigation: Use a scoped HTTP tool where available, validate country and language codes, and URL-encode user-controlled query fields before requests are made.

Risk: The skill directs the agent to display third-party news and video links without enough validation.

Mitigation: Check returned links before displaying them and present third-party content as sourced news results rather than verified facts.

Risk: The skill defaults to a locale when country or language cannot be determined.

Mitigation: Ask the user to confirm the desired country and language before using a default market for news retrieval.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zerokileom/skills/global-news)
- [Opera News](https://www.operanewsapp.com)
- [Opera News feed API base URL](https://news-af.feednews.com/{country}/{language}/v1/mcp/news)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, API calls, guidance]

**Output Format:** [Markdown summaries with article or video links, plus shell-based HTTP request guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may include third-party headlines, summaries, thumbnails, article links, video metadata, and pagination indicators returned by the Opera News feed.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
