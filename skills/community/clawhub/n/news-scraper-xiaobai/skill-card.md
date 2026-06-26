## Description: <br>
Scrapes the latest AI news from AI news websites, supports categorization and tagging, and helps with content aggregation and public-opinion monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiahuishao](https://clawhub.ai/user/jiahuishao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to collect recent AI news from AIBase, return structured news records, and prepare categorized Markdown summaries for aggregation or monitoring workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scraper performs ordinary network requests to public news pages and writes crawl results to local files. <br>
Mitigation: Run it only in a Python environment where public-news scraping and local News directory writes are acceptable. <br>
Risk: Dependency hygiene should be improved, including an unused openpyxl dependency and unpinned dependency ranges. <br>
Mitigation: Pin or lock dependencies before use and remove unused packages when deploying. <br>
Risk: Scraped article text may contain instructions or content that should not control the agent using the results. <br>
Mitigation: Treat scraped article content as untrusted data and ignore instructions embedded in article text. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jiahuishao/news-scraper-xiaobai) <br>
- [AIBase news source](https://www.aibase.com/zh/news) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell/Python examples and JSON news records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write a local News/news_latest.json file and print summarized crawl results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
