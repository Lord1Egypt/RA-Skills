## Description: <br>
PANews helps agents read and summarize cryptocurrency and blockchain news, market narratives, rankings, searches, articles, topics, columns, series, events, calendars, and editorial picks from PANews coverage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[medz](https://clawhub.ai/user/medz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill for structured PANews cryptocurrency and blockchain news discovery, including daily briefings, article search, topic research, rankings, columns, series, events, calendars, and editorial picks. It is suited for explaining PANews-reported developments without adding investment advice or unsupported outside context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad prompts such as "latest news" or "what happened today" may activate this PANews-focused skill when the user intended general news. <br>
Mitigation: Ask a clarifying question or clearly state that the response is based on PANews cryptocurrency and blockchain coverage. <br>
Risk: Crypto news summaries may be mistaken for investment advice or price prediction. <br>
Mitigation: Present reported developments as news context only and avoid predicting price movements or recommending trades. <br>
Risk: PANews coverage may be weak, missing, or narrower than the user's topic. <br>
Mitigation: Say when PANews results are sparse and do not fill gaps with outside information unless the user asks for broader research. <br>


## Reference(s): <br>
- [PANews Skill Page](https://clawhub.ai/medz/panews) <br>
- [Today’s Briefing](references/workflow-today-briefing.md) <br>
- [Latest News](references/workflow-latest-news.md) <br>
- [Search](references/workflow-search.md) <br>
- [Deep Topic Research](references/workflow-topic-research.md) <br>
- [Understand an Article](references/workflow-read-article.md) <br>
- [Discover Trending](references/workflow-trending.md) <br>
- [Browse Columns](references/workflow-columns.md) <br>
- [Browse Series](references/workflow-series.md) <br>
- [Browse Topics](references/workflow-topics.md) <br>
- [Events](references/workflow-events.md) <br>
- [Event Calendar](references/workflow-calendar.md) <br>
- [Platform Hooks](references/workflow-hooks.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown summaries, lists, briefings, and explanations grounded in PANews results, with shell commands used internally by the agent when needed.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses should stay grounded in PANews coverage, match the user's language when possible, and avoid price predictions or investment advice.] <br>

## Skill Version(s): <br>
0.2.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
