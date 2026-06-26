## Description: <br>
Aggregates Chinese A-share market news from hot news, technology media, securities sites, and official channels, with include and exclude keyword filtering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mc82465](https://clawhub.ai/user/mc82465) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill to fetch, filter, and summarize current Chinese market and technology news for users who ask about A-share market developments or specific news topics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts third-party Chinese news, RSSHub, finance, technology, and government sites and returns external article text and links. <br>
Mitigation: Treat returned content and links as untrusted external content and verify important market or financial information with original sources before acting on it. <br>
Risk: RSS feeds and website structures can change or become unavailable, which may produce incomplete or missing results. <br>
Mitigation: Use the skill's source listing and alternate RSSHub mirrors when a feed fails, and disclose gaps when requested news cannot be retrieved. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/mc82465/news-market) <br>
- [Original adapted skill reference](https://skillsmp.com/zh/skills/countbot-ai-countbot-skills-news-skill-md) <br>
- [RSSHub official source](https://rsshub.app) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, guidance] <br>
**Output Format:** [Plain text or JSON news lists with titles, sources, timestamps, summaries, and links; agents may present the results as concise Markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports category selection, include and exclude keyword filters, result limits, and configurable summary length.] <br>

## Skill Version(s): <br>
1.1.9 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
