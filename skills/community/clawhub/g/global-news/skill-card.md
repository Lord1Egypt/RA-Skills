## Description: <br>
Stay informed with Global News - get breaking news, top headlines, local city news, and full-text article search across Europe, Americas, Latin America, and Africa. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zerokileom](https://clawhub.ai/user/zerokileom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to fetch top headlines, city news, topic-based article search, and trending video results from Opera News/FeedNews across supported countries and languages. <br>

### Deployment Geography for Use: <br>
Europe, Americas, Latin America, and Africa <br>

## Known Risks and Mitigations: <br>
Risk: News topics, city names, and coarse country/language choices are sent to the external FeedNews/Opera News API. <br>
Mitigation: Avoid sensitive queries and install only where sending those request details to the external API is acceptable. <br>
Risk: Broad activation terms and the default us/en market can return results for the wrong region or language. <br>
Mitigation: Ask users to specify country and language for non-US or multilingual requests, and verify the selected market before relying on results. <br>


## Reference(s): <br>
- [Global News on ClawHub](https://clawhub.ai/zerokileom/global-news) <br>
- [Opera News](https://www.operanewsapp.com) <br>
- [FeedNews news API base](https://news-af.feednews.com/{country}/{language}/v1/mcp/news) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown news briefings with headlines, summaries, article links, and optional video result details.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses country/language market codes, city or topic queries, result-count and pagination options, and optional video look-back windows.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
