## Description: <br>
Search Korean news articles using Naver Search API. Use when searching for Korean news, getting latest news updates, finding news about specific topics, or preparing daily news summaries. Supports relevance and date-based sorting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[steamb23](https://clawhub.ai/user/steamb23) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to search Korean news through the Naver Search API, monitor topics, and collect article data for daily summaries, alerts, or custom news feeds. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: News search queries are sent to Naver using user-provided developer credentials. <br>
Mitigation: Use a dedicated Naver application key where possible and keep NAVER_CLIENT_ID and NAVER_CLIENT_SECRET in environment configuration rather than source files or prompts. <br>
Risk: Automated summaries or scheduled monitoring can consume Naver API quota. <br>
Mitigation: Set conservative display, pagination, and scheduling limits, and monitor usage against the Naver application quota. <br>


## Reference(s): <br>
- [Naver News Search API Reference](references/api.md) <br>
- [Naver Developers Search News API](https://developers.naver.com/docs/serviceapi/search/news/news.md) <br>
- [Daily News Summary Example](examples/daily-summary.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Plain text or JSON from the Python search helper, with Markdown usage guidance and workflow examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 plus NAVER_CLIENT_ID and NAVER_CLIENT_SECRET; supports date filtering, pagination, and relevance or date sorting.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
