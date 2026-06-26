## Description: <br>
Comprehensive news aggregator that fetches, filters, and deeply analyzes real-time content from 8 major sources: Hacker News, GitHub Trending, Product Hunt, 36Kr, Tencent News, WallStreetCN, V2EX, and Weibo. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AdministratorFung](https://clawhub.ai/user/AdministratorFung) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external users use this skill to fetch public technology, open-source, social, and finance news from supported sources, then turn the results into concise Chinese briefings or deeper topic reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches public web sources and, in deep mode, sends network requests to article URLs that may reveal query interest through normal web traffic. <br>
Mitigation: Use it in a normal project directory and avoid deep scans for sensitive queries when third-party sites should not see that network activity. <br>
Risk: The skill depends on Python packages for HTTP requests and HTML parsing. <br>
Mitigation: Review or pin dependencies before installation in controlled environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AdministratorFung/news-aggregator-skill-3) <br>
- [README](README.md) <br>
- [Command templates](templates.md) <br>
- [Repository link referenced by README](https://github.com/cclank/news-aggregator-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance, files] <br>
**Output Format:** [Markdown reports and chat responses, with JSON returned by the fetch_news.py helper script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports are intended to be saved under reports/ with timestamped Markdown filenames; deep fetch may include extracted article text.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
