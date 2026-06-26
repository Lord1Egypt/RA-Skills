## Description: <br>
Search news articles via NewsAPI with filtering by time windows, sources, domains, and languages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Hegghammer](https://clawhub.ai/user/Hegghammer) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, researchers, and analysts use this skill to query NewsAPI for article discovery, breaking headlines, source lists, and filtered news-monitoring workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms and filters are sent to NewsAPI, which may expose sensitive topics or internal names to an external service. <br>
Mitigation: Avoid highly sensitive searches and review planned queries before running the skill. <br>
Risk: The skill reads NEWSAPI_KEY from ~/.openclaw/.env, so unrelated secrets in that file could increase credential exposure risk. <br>
Mitigation: Use a dedicated NewsAPI key with limited quota and keep unrelated secrets out of ~/.openclaw/.env. <br>


## Reference(s): <br>
- [NewsAPI](https://newsapi.org) <br>
- [NewsAPI Parameter Reference](artifact/references/api-reference.md) <br>
- [NewsAPI Search Examples](artifact/references/examples.md) <br>
- [ClawHub release page](https://clawhub.ai/Hegghammer/newsapi-search) <br>


## Skill Output: <br>
**Output Type(s):** [json, shell commands, code, guidance] <br>
**Output Format:** [JSON search and source-list responses, with Markdown usage guidance and JavaScript helper functions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a NEWSAPI_KEY and sends search terms, filters, and source queries to newsapi.org.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
