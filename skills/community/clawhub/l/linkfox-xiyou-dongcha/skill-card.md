## Description: <br>
Xiyou Keyword Research helps agents query Xiyou Insights through the LinkFox gateway for Amazon ASIN and keyword traffic, ranking, trend, BSR, ABA, competition, and suggested bid analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
E-commerce operators, marketplace analysts, and agents use this skill to research Amazon ASINs and keywords with Xiyou data, including reverse ASIN keyword lookup, trend analysis, BSR history, ABA weekly volume, competition, and suggested CPC across supported marketplaces. <br>

### Deployment Geography for Use: <br>
Global for supported Amazon marketplaces: US, CA, MX, BR, UK, DE, ES, IT, FR, JP, AU, SA, and AE. <br>

## Known Risks and Mitigations: <br>
Risk: Queries send ASINs, keywords, account-linked API credentials, and related metadata to LinkFox and Xiyou services. <br>
Mitigation: Install only when those services are intended, keep credentials in environment variables, avoid placing secrets in prompts or parameters, and limit submitted queries to data appropriate for those services. <br>
Risk: The skill includes feedback-reporting behavior to a separate LinkFox endpoint, which may disclose user intent or result details without clear consent. <br>
Mitigation: Report feedback only after explicit user opt-in and review the feedback content before sending it. <br>
Risk: Large response files can persist locally and may contain sensitive commercial, pricing, or query data. <br>
Mitigation: Write large responses to a temporary directory outside any git working tree and delete them after the task is complete. <br>


## Reference(s): <br>
- [Xiyou API reference](references/api.md) <br>
- [Xiyou OpenAPI console](https://www.xydc.com/openapi?xiyou-insights-web=%2Fopenapi) <br>
- [LinkFox API key setup](https://yxgb3sicy7.feishu.cn/wiki/GIkkweGghiyzkqkRXQKc2n0Tnre) <br>
- [ClawHub skill page](https://clawhub.ai/linkfox-ai/linkfox-xiyou-dongcha) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON request examples; API responses are JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Large API responses can be persisted to local files and read back as selected fields, JSON, JSONL, CSV, or tables.] <br>

## Skill Version(s): <br>
0.0.1 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
