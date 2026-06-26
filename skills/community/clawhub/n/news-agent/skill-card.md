## Description: <br>
News Agent Skills integrates with a news intelligence API to query articles, trigger collection and analysis tasks, retrieve dashboard data, and analyze trends. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[swipth](https://clawhub.ai/user/swipth) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage news data through a configured backend API, including article lookup, dashboard review, trend analysis, and backend task triggering. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scripts always send a development authorization bypass to the configured API endpoint. <br>
Mitigation: Use the skill only with a trusted local or internal NEWS_API_BASE_URL and avoid the development bearer bypass against production systems. <br>
Risk: Crawl, analyze, and trend commands can trigger backend-changing jobs that may consume compute or paid LLM/API quota. <br>
Mitigation: Restrict task-triggering commands to authorized operators and review backend cost, quota, and job controls before deployment. <br>


## Reference(s): <br>
- [News Agent API Reference](references/api_docs.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/swipth/news-agent) <br>
- [Publisher Profile](https://clawhub.ai/user/swipth) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON] <br>
**Output Format:** [Markdown guidance with shell command examples and optional JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires NEWS_API_BASE_URL for non-default backend targets.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
