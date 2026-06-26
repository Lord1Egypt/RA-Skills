## Description: <br>
Fetch and display international tech news from curated RSS feeds, including TechCrunch, The Verge, Wired, Ars Technica, Engadget, Hacker News, MIT Technology Review, and Gizmodo. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[goog](https://clawhub.ai/user/goog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers can use this skill to retrieve a broad international technology news digest from curated public RSS feeds and receive the results as a markdown table with links, timestamps, and optional summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes outbound requests to public news RSS feeds and depends on third-party feed availability and content. <br>
Mitigation: Review the listed RSS sources before use and expect empty, delayed, or changed results when a source is unavailable or modifies its feed. <br>
Risk: The bundled script stores cached feed data under the user's home directory. <br>
Mitigation: Use a virtual environment or isolated user profile when dependency or cache isolation is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/goog/no-news) <br>
- [TechCrunch RSS feed](https://techcrunch.com/feed/) <br>
- [The Verge RSS feed](https://www.theverge.com/rss/index.xml) <br>
- [Wired RSS feed](https://www.wired.com/feed/rss) <br>
- [Ars Technica RSS feed](https://feeds.arstechnica.com/arstechnica/index) <br>
- [Engadget RSS feed](https://www.engadget.com/rss.xml) <br>
- [Hacker News RSS feed](https://hnrss.org/frontpage) <br>
- [MIT Technology Review RSS feed](https://www.technologyreview.com/feed/) <br>
- [Gizmodo RSS feed](https://gizmodo.com/rss) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Markdown table with article titles, source links, publish times, and optional summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses public RSS feeds and may cache fetched feed data under the user's home directory for 30 minutes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
