## Description: <br>
Fetches and formats hot news ranking data from multiple platforms through the NewsLatest API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[violetlength](https://clawhub.ai/user/violetlength) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to request current hot-topic lists from supported news, social, finance, and technology platforms, then receive ranked summaries with links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Results depend on a third-party API service, so availability, freshness, and response quality can vary. <br>
Mitigation: Avoid sensitive details in news-source requests, respect the documented request interval, and verify important results against the linked source items. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/violetlength/newslatest) <br>
- [NewsLatest API base](https://newslatest-server.up.railway.app) <br>
- [NewsLatest combined endpoint](https://newslatest-server.up.railway.app/news/combined?sources=baidu,weibo,zhihu) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown summaries with ranked news items and source links; fetched API responses are JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports single-source and combined-source rankings, with fallback text for missing descriptions or hot scores.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
