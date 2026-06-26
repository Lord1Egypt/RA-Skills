## Description: <br>
Game Informer section RSS skill for fetching news, reviews, previews, and features, then formatting populated sections as Markdown linked headlines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maximedogawa](https://clawhub.ai/user/maximedogawa) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to retrieve current Game Informer headlines from public RSS feeds and present them in ordered Markdown sections. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may request public RSS feeds from Game Informer when invoked. <br>
Mitigation: Review the feed URLs and allow outbound network access only when that external source is acceptable. <br>
Risk: RSS feed content can be unavailable or include HTML descriptions that are unsuitable for direct output. <br>
Mitigation: Use only successfully loaded feed items, omit empty sections, and avoid pasting raw HTML from descriptions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/maximedogawa/news-gameinfomer) <br>
- [Game Informer source site](https://www.gameinformer.com/) <br>
- [Game Informer RSS feed](https://www.gameinformer.com/rss.xml) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown headings with numbered linked headlines] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to 3-5 items per populated section and omits empty or unavailable sections.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
