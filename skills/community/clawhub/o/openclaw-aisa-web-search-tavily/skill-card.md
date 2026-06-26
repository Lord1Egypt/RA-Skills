## Description: <br>
AI-optimized web search via AIsa's Tavily API proxy, providing concise and relevant results with options for deep or news-focused queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AIsaDocs](https://clawhub.ai/user/AIsaDocs) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and AI agents use this skill to run web searches, deep searches, news-focused searches, and URL content extraction through AIsa's Tavily API proxy. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries, target URLs, and the AISA_API_KEY are sent to AIsa's external API service. <br>
Mitigation: Use only with organization-approved data flows, and avoid secrets, private internal URLs, regulated data, or confidential research targets unless approved. <br>
Risk: The skill returns web search results and extracted page content that may be incomplete, stale, or misleading. <br>
Mitigation: Review generated answers and cited sources before relying on them for decisions or downstream agent actions. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/AIsaDocs/openclaw-aisa-web-search-tavily) <br>
- [AIsa](https://aisa.one) <br>
- [AIsa Marketplace](https://marketplace.aisa.one) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands] <br>
**Output Format:** [Markdown-like command output with answers, source lists, extracted page content, and failed URL reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search supports result count, basic or advanced depth, general or news topic, and optional news day range; extraction accepts one or more URLs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
