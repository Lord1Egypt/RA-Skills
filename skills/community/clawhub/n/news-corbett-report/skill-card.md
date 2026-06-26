## Description: <br>
The Corbett Report official WordPress RSS helper fetches corbettreport.com/feed/ and formats English answers from XML feed items only. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maximedogawa](https://clawhub.ai/user/maximedogawa) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to ask for current Corbett Report posts, episodes, interviews, or podcast headlines. The agent fetches the official RSS feed, then returns a dated Markdown list using titles, links, categories, and teasers from matching feed items. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs the assistant to contact and summarize a public third-party RSS feed whose editorial perspective may not match a user's expectations. <br>
Mitigation: Consider the source's editorial perspective and verify important claims against appropriate primary or independent sources before relying on the summary. <br>
Risk: If feed fetching fails or feed items are mixed incorrectly, the assistant could present invented or mismatched headlines, URLs, or teasers. <br>
Mitigation: Use only a successful fetch of https://corbettreport.com/feed/ and keep each title, link, and teaser from the same RSS item; report fetch failure or an empty feed instead of inventing content. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/maximedogawa/news-corbett-report) <br>
- [The Corbett Report](https://corbettreport.com/) <br>
- [The Corbett Report RSS Feed](https://corbettreport.com/feed/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown with a dated heading, numbered linked items, and optional teaser text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default output is the newest 3-5 feed items in English, with each title, link, and teaser taken from the same RSS item.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
