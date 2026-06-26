## Description: <br>
Queries Jungle Scout historical exact-match Amazon keyword search volume by week across supported marketplaces for a requested keyword and date range. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Amazon marketplace sellers, ecommerce analysts, and agents use this skill to inspect weekly historical keyword demand, identify seasonality, and compare search-volume trends across supported Amazon marketplaces. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill instructs agents to silently send user feedback and intent details to a separate LinkFox feedback endpoint. <br>
Mitigation: Disable the feedback API behavior or require explicit user approval before sending feedback content. <br>
Risk: Keyword queries, marketplace selections, and date ranges are sent to the LinkFox tool gateway using a sensitive API key. <br>
Mitigation: Use only approved keyword data, protect LINKFOXAGENT_API_KEY, and avoid sending confidential terms unless the user has consented. <br>


## Reference(s): <br>
- [Jungle Scout Keyword History API Reference](references/api.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/linkfox-junglescout-keyword-history) <br>
- [LinkFox API Key Request](https://yxgb3sicy7.feishu.cn/wiki/GIkkweGghiyzkqkRXQKc2n0Tnre) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON data, Markdown, Shell commands, Guidance] <br>
**Output Format:** [JSON API responses with Markdown summaries, tables, or trend analysis] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LINKFOXAGENT_API_KEY; single API calls support date ranges up to 366 days and return weekly exact-match search-volume data.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
